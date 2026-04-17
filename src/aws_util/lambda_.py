from __future__ import annotations

import base64
import json
import time as _time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Literal

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AddLayerVersionPermissionResult",
    "AddPermissionResult",
    "CreateAliasResult",
    "CreateCodeSigningConfigResult",
    "CreateEventSourceMappingResult",
    "CreateFunctionResult",
    "CreateFunctionUrlConfigResult",
    "DeleteEventSourceMappingResult",
    "GetAccountSettingsResult",
    "GetAliasResult",
    "GetCodeSigningConfigResult",
    "GetEventSourceMappingResult",
    "GetFunctionCodeSigningConfigResult",
    "GetFunctionConcurrencyResult",
    "GetFunctionConfigurationResult",
    "GetFunctionEventInvokeConfigResult",
    "GetFunctionRecursionConfigResult",
    "GetFunctionResult",
    "GetFunctionUrlConfigResult",
    "GetLayerVersionByArnResult",
    "GetLayerVersionPolicyResult",
    "GetLayerVersionResult",
    "GetPolicyResult",
    "GetProvisionedConcurrencyConfigResult",
    "GetRuntimeManagementConfigResult",
    "InvokeResult",
    "InvokeWithResponseStreamResult",
    "ListAliasesResult",
    "ListCodeSigningConfigsResult",
    "ListEventSourceMappingsResult",
    "ListFunctionEventInvokeConfigsResult",
    "ListFunctionUrlConfigsResult",
    "ListFunctionsByCodeSigningConfigResult",
    "ListFunctionsResult",
    "ListLayerVersionsResult",
    "ListLayersResult",
    "ListProvisionedConcurrencyConfigsResult",
    "ListTagsResult",
    "ListVersionsByFunctionResult",
    "PublishLayerVersionResult",
    "PublishVersionResult",
    "PutFunctionCodeSigningConfigResult",
    "PutFunctionConcurrencyResult",
    "PutFunctionEventInvokeConfigResult",
    "PutFunctionRecursionConfigResult",
    "PutProvisionedConcurrencyConfigResult",
    "PutRuntimeManagementConfigResult",
    "UpdateAliasResult",
    "UpdateCodeSigningConfigResult",
    "UpdateEventSourceMappingResult",
    "UpdateFunctionCodeResult",
    "UpdateFunctionConfigurationResult",
    "UpdateFunctionEventInvokeConfigResult",
    "UpdateFunctionUrlConfigResult",
    "add_layer_version_permission",
    "add_permission",
    "create_alias",
    "create_code_signing_config",
    "create_event_source_mapping",
    "create_function",
    "create_function_url_config",
    "delete_alias",
    "delete_code_signing_config",
    "delete_event_source_mapping",
    "delete_function",
    "delete_function_code_signing_config",
    "delete_function_concurrency",
    "delete_function_event_invoke_config",
    "delete_function_url_config",
    "delete_layer_version",
    "delete_provisioned_concurrency_config",
    "fan_out",
    "get_account_settings",
    "get_alias",
    "get_code_signing_config",
    "get_event_source_mapping",
    "get_function",
    "get_function_code_signing_config",
    "get_function_concurrency",
    "get_function_configuration",
    "get_function_event_invoke_config",
    "get_function_recursion_config",
    "get_function_url_config",
    "get_layer_version",
    "get_layer_version_by_arn",
    "get_layer_version_policy",
    "get_policy",
    "get_provisioned_concurrency_config",
    "get_runtime_management_config",
    "invoke",
    "invoke_async",
    "invoke_with_response_stream",
    "invoke_with_retry",
    "list_aliases",
    "list_code_signing_configs",
    "list_event_source_mappings",
    "list_function_event_invoke_configs",
    "list_function_url_configs",
    "list_functions",
    "list_functions_by_code_signing_config",
    "list_layer_versions",
    "list_layers",
    "list_provisioned_concurrency_configs",
    "list_tags",
    "list_versions_by_function",
    "publish_layer_version",
    "publish_version",
    "put_function_code_signing_config",
    "put_function_concurrency",
    "put_function_event_invoke_config",
    "put_function_recursion_config",
    "put_provisioned_concurrency_config",
    "put_runtime_management_config",
    "remove_layer_version_permission",
    "remove_permission",
    "tag_resource",
    "untag_resource",
    "update_alias",
    "update_code_signing_config",
    "update_event_source_mapping",
    "update_function_code",
    "update_function_configuration",
    "update_function_event_invoke_config",
    "update_function_url_config",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class InvokeResult(BaseModel):
    """Result of a Lambda ``Invoke`` call."""

    model_config = ConfigDict(frozen=True)

    status_code: int
    payload: Any
    function_error: str | None = None
    log_result: str | None = None

    @property
    def succeeded(self) -> bool:
        """``True`` if the invocation completed without a function error."""
        return self.function_error is None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def invoke(
    function_name: str,
    payload: dict | list | str | None = None,
    invocation_type: Literal["RequestResponse", "Event", "DryRun"] = "RequestResponse",
    log_type: Literal["None", "Tail"] = "None",
    qualifier: str | None = None,
    region_name: str | None = None,
) -> InvokeResult:
    """Invoke an AWS Lambda function.

    Args:
        function_name: Function name, ARN, or partial ARN.
        payload: Event payload sent to the function.  Dicts/lists are
            JSON-encoded; ``None`` sends an empty payload.
        invocation_type: ``"RequestResponse"`` (default) — synchronous,
            waits for the result.  ``"Event"`` — asynchronous, returns
            immediately.  ``"DryRun"`` — validates parameters only.
        log_type: ``"Tail"`` returns the last 4 KB of execution logs in the
            response (synchronous invocations only).
        qualifier: Function version or alias to invoke.
        region_name: AWS region override.

    Returns:
        An :class:`InvokeResult`.  For ``"RequestResponse"`` invocations the
        ``payload`` field holds the deserialised JSON response (or the raw
        string if it is not valid JSON).

    Raises:
        RuntimeError: If the API call itself fails (not a function error).
    """
    client = get_client("lambda", region_name)

    raw_payload: bytes | None = None
    if payload is not None:
        raw_payload = (
            json.dumps(payload).encode() if isinstance(payload, (dict, list)) else payload.encode()
        )

    kwargs: dict[str, Any] = {
        "FunctionName": function_name,
        "InvocationType": invocation_type,
        "LogType": log_type,
    }
    if raw_payload is not None:
        kwargs["Payload"] = raw_payload
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier

    try:
        resp = client.invoke(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to invoke Lambda {function_name!r}") from exc

    raw_response = resp["Payload"].read()
    try:
        parsed_payload: Any = json.loads(raw_response) if raw_response else None
    except json.JSONDecodeError:
        parsed_payload = raw_response.decode("utf-8")

    log_result: str | None = None
    if resp.get("LogResult"):
        log_result = base64.b64decode(resp["LogResult"]).decode("utf-8")

    return InvokeResult(
        status_code=resp["StatusCode"],
        payload=parsed_payload,
        function_error=resp.get("FunctionError"),
        log_result=log_result,
    )


def invoke_async(
    function_name: str,
    payload: dict | list | str | None = None,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Fire-and-forget Lambda invocation (``Event`` invocation type).

    Args:
        function_name: Function name, ARN, or partial ARN.
        payload: Event payload.  Dicts/lists are JSON-encoded.
        qualifier: Function version or alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    invoke(
        function_name=function_name,
        payload=payload,
        invocation_type="Event",
        qualifier=qualifier,
        region_name=region_name,
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def invoke_with_retry(
    function_name: str,
    payload: dict | list | str | None = None,
    max_retries: int = 3,
    backoff_base: float = 1.0,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> InvokeResult:
    """Invoke a Lambda function and retry on transient failures with exponential back-off.

    Retries on ``TooManyRequestsException`` (throttling) and service-side
    errors (5xx).  Function-level errors (``FunctionError`` set) are **not**
    retried — they indicate application logic failures.

    Args:
        function_name: Function name, ARN, or partial ARN.
        payload: Event payload.
        max_retries: Maximum additional attempts after the first failure
            (default ``3``).
        backoff_base: Base seconds for exponential back-off.  Attempt *n*
            sleeps for ``backoff_base * 2 ** (n-1)`` seconds.
        qualifier: Function version or alias.
        region_name: AWS region override.

    Returns:
        An :class:`InvokeResult` from the first successful invocation.

    Raises:
        RuntimeError: If all attempts fail.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            result = invoke(
                function_name,
                payload=payload,
                qualifier=qualifier,
                region_name=region_name,
            )
            # Function-level errors are not retried — they indicate
            # application logic failures, not transient API problems.
            if result.function_error is not None:
                return result
            return result
        except RuntimeError as exc:
            last_exc = exc
            if attempt < max_retries:
                sleep_time = backoff_base * (2**attempt)
                _time.sleep(sleep_time)

    raise wrap_aws_error(
        last_exc,  # type: ignore[arg-type]
        f"invoke_with_retry: all {max_retries + 1} attempts failed for {function_name!r}",
    ) from last_exc


def fan_out(
    function_name: str,
    payloads: list[dict | list | str | None],
    max_concurrency: int = 10,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> list[InvokeResult]:
    """Invoke a Lambda function concurrently with multiple payloads.

    Sends all invocations as ``RequestResponse`` (synchronous) using a thread
    pool.  Results are returned in the same order as *payloads*.

    Args:
        function_name: Function name, ARN, or partial ARN.
        payloads: List of per-invocation payloads.
        max_concurrency: Maximum simultaneous invocations (default ``10``).
        qualifier: Function version or alias.
        region_name: AWS region override.

    Returns:
        A list of :class:`InvokeResult` objects in the same order as
        *payloads*.

    Raises:
        RuntimeError: If any invocation raises unexpectedly.
    """
    results: dict[int, InvokeResult] = {}

    def _invoke(index: int, p: dict | list | str | None) -> tuple[int, InvokeResult]:
        return index, invoke(function_name, payload=p, qualifier=qualifier, region_name=region_name)

    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
        futures = {pool.submit(_invoke, i, p): i for i, p in enumerate(payloads)}
        for future in as_completed(futures):
            idx, result = future.result()
            results[idx] = result

    return [results[i] for i in range(len(payloads))]


class AddLayerVersionPermissionResult(BaseModel):
    """Result of add_layer_version_permission."""

    model_config = ConfigDict(frozen=True)

    statement: str | None = None
    revision_id: str | None = None


class AddPermissionResult(BaseModel):
    """Result of add_permission."""

    model_config = ConfigDict(frozen=True)

    statement: str | None = None


class CreateAliasResult(BaseModel):
    """Result of create_alias."""

    model_config = ConfigDict(frozen=True)

    alias_arn: str | None = None
    name: str | None = None
    function_version: str | None = None
    description: str | None = None
    routing_config: dict[str, Any] | None = None
    revision_id: str | None = None


class CreateCodeSigningConfigResult(BaseModel):
    """Result of create_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    code_signing_config: dict[str, Any] | None = None


class CreateEventSourceMappingResult(BaseModel):
    """Result of create_event_source_mapping."""

    model_config = ConfigDict(frozen=True)

    uuid: str | None = None
    starting_position: str | None = None
    starting_position_timestamp: str | None = None
    batch_size: int | None = None
    maximum_batching_window_in_seconds: int | None = None
    parallelization_factor: int | None = None
    event_source_arn: str | None = None
    filter_criteria: dict[str, Any] | None = None
    function_arn: str | None = None
    last_modified: str | None = None
    last_processing_result: str | None = None
    state: str | None = None
    state_transition_reason: str | None = None
    destination_config: dict[str, Any] | None = None
    topics: list[str] | None = None
    queues: list[str] | None = None
    source_access_configurations: list[dict[str, Any]] | None = None
    self_managed_event_source: dict[str, Any] | None = None
    maximum_record_age_in_seconds: int | None = None
    bisect_batch_on_function_error: bool | None = None
    maximum_retry_attempts: int | None = None
    tumbling_window_in_seconds: int | None = None
    function_response_types: list[str] | None = None
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None
    self_managed_kafka_event_source_config: dict[str, Any] | None = None
    scaling_config: dict[str, Any] | None = None
    document_db_event_source_config: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    filter_criteria_error: dict[str, Any] | None = None
    event_source_mapping_arn: str | None = None
    metrics_config: dict[str, Any] | None = None
    provisioned_poller_config: dict[str, Any] | None = None


class CreateFunctionResult(BaseModel):
    """Result of create_function."""

    model_config = ConfigDict(frozen=True)

    function_name: str | None = None
    function_arn: str | None = None
    runtime: str | None = None
    role: str | None = None
    handler: str | None = None
    code_size: int | None = None
    description: str | None = None
    timeout: int | None = None
    memory_size: int | None = None
    last_modified: str | None = None
    code_sha256: str | None = None
    version: str | None = None
    vpc_config: dict[str, Any] | None = None
    dead_letter_config: dict[str, Any] | None = None
    environment: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    tracing_config: dict[str, Any] | None = None
    master_arn: str | None = None
    revision_id: str | None = None
    layers: list[dict[str, Any]] | None = None
    state: str | None = None
    state_reason: str | None = None
    state_reason_code: str | None = None
    last_update_status: str | None = None
    last_update_status_reason: str | None = None
    last_update_status_reason_code: str | None = None
    file_system_configs: list[dict[str, Any]] | None = None
    package_type: str | None = None
    image_config_response: dict[str, Any] | None = None
    signing_profile_version_arn: str | None = None
    signing_job_arn: str | None = None
    architectures: list[str] | None = None
    ephemeral_storage: dict[str, Any] | None = None
    snap_start: dict[str, Any] | None = None
    runtime_version_config: dict[str, Any] | None = None
    logging_config: dict[str, Any] | None = None


class CreateFunctionUrlConfigResult(BaseModel):
    """Result of create_function_url_config."""

    model_config = ConfigDict(frozen=True)

    function_url: str | None = None
    function_arn: str | None = None
    auth_type: str | None = None
    cors: dict[str, Any] | None = None
    creation_time: str | None = None
    invoke_mode: str | None = None


class DeleteEventSourceMappingResult(BaseModel):
    """Result of delete_event_source_mapping."""

    model_config = ConfigDict(frozen=True)

    uuid: str | None = None
    starting_position: str | None = None
    starting_position_timestamp: str | None = None
    batch_size: int | None = None
    maximum_batching_window_in_seconds: int | None = None
    parallelization_factor: int | None = None
    event_source_arn: str | None = None
    filter_criteria: dict[str, Any] | None = None
    function_arn: str | None = None
    last_modified: str | None = None
    last_processing_result: str | None = None
    state: str | None = None
    state_transition_reason: str | None = None
    destination_config: dict[str, Any] | None = None
    topics: list[str] | None = None
    queues: list[str] | None = None
    source_access_configurations: list[dict[str, Any]] | None = None
    self_managed_event_source: dict[str, Any] | None = None
    maximum_record_age_in_seconds: int | None = None
    bisect_batch_on_function_error: bool | None = None
    maximum_retry_attempts: int | None = None
    tumbling_window_in_seconds: int | None = None
    function_response_types: list[str] | None = None
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None
    self_managed_kafka_event_source_config: dict[str, Any] | None = None
    scaling_config: dict[str, Any] | None = None
    document_db_event_source_config: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    filter_criteria_error: dict[str, Any] | None = None
    event_source_mapping_arn: str | None = None
    metrics_config: dict[str, Any] | None = None
    provisioned_poller_config: dict[str, Any] | None = None


class GetAccountSettingsResult(BaseModel):
    """Result of get_account_settings."""

    model_config = ConfigDict(frozen=True)

    account_limit: dict[str, Any] | None = None
    account_usage: dict[str, Any] | None = None


class GetAliasResult(BaseModel):
    """Result of get_alias."""

    model_config = ConfigDict(frozen=True)

    alias_arn: str | None = None
    name: str | None = None
    function_version: str | None = None
    description: str | None = None
    routing_config: dict[str, Any] | None = None
    revision_id: str | None = None


class GetCodeSigningConfigResult(BaseModel):
    """Result of get_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    code_signing_config: dict[str, Any] | None = None


class GetEventSourceMappingResult(BaseModel):
    """Result of get_event_source_mapping."""

    model_config = ConfigDict(frozen=True)

    uuid: str | None = None
    starting_position: str | None = None
    starting_position_timestamp: str | None = None
    batch_size: int | None = None
    maximum_batching_window_in_seconds: int | None = None
    parallelization_factor: int | None = None
    event_source_arn: str | None = None
    filter_criteria: dict[str, Any] | None = None
    function_arn: str | None = None
    last_modified: str | None = None
    last_processing_result: str | None = None
    state: str | None = None
    state_transition_reason: str | None = None
    destination_config: dict[str, Any] | None = None
    topics: list[str] | None = None
    queues: list[str] | None = None
    source_access_configurations: list[dict[str, Any]] | None = None
    self_managed_event_source: dict[str, Any] | None = None
    maximum_record_age_in_seconds: int | None = None
    bisect_batch_on_function_error: bool | None = None
    maximum_retry_attempts: int | None = None
    tumbling_window_in_seconds: int | None = None
    function_response_types: list[str] | None = None
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None
    self_managed_kafka_event_source_config: dict[str, Any] | None = None
    scaling_config: dict[str, Any] | None = None
    document_db_event_source_config: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    filter_criteria_error: dict[str, Any] | None = None
    event_source_mapping_arn: str | None = None
    metrics_config: dict[str, Any] | None = None
    provisioned_poller_config: dict[str, Any] | None = None


class GetFunctionResult(BaseModel):
    """Result of get_function."""

    model_config = ConfigDict(frozen=True)

    configuration: dict[str, Any] | None = None
    code: dict[str, Any] | None = None
    tags: dict[str, Any] | None = None
    tags_error: dict[str, Any] | None = None
    concurrency: dict[str, Any] | None = None


class GetFunctionCodeSigningConfigResult(BaseModel):
    """Result of get_function_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    code_signing_config_arn: str | None = None
    function_name: str | None = None


class GetFunctionConcurrencyResult(BaseModel):
    """Result of get_function_concurrency."""

    model_config = ConfigDict(frozen=True)

    reserved_concurrent_executions: int | None = None


class GetFunctionConfigurationResult(BaseModel):
    """Result of get_function_configuration."""

    model_config = ConfigDict(frozen=True)

    function_name: str | None = None
    function_arn: str | None = None
    runtime: str | None = None
    role: str | None = None
    handler: str | None = None
    code_size: int | None = None
    description: str | None = None
    timeout: int | None = None
    memory_size: int | None = None
    last_modified: str | None = None
    code_sha256: str | None = None
    version: str | None = None
    vpc_config: dict[str, Any] | None = None
    dead_letter_config: dict[str, Any] | None = None
    environment: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    tracing_config: dict[str, Any] | None = None
    master_arn: str | None = None
    revision_id: str | None = None
    layers: list[dict[str, Any]] | None = None
    state: str | None = None
    state_reason: str | None = None
    state_reason_code: str | None = None
    last_update_status: str | None = None
    last_update_status_reason: str | None = None
    last_update_status_reason_code: str | None = None
    file_system_configs: list[dict[str, Any]] | None = None
    package_type: str | None = None
    image_config_response: dict[str, Any] | None = None
    signing_profile_version_arn: str | None = None
    signing_job_arn: str | None = None
    architectures: list[str] | None = None
    ephemeral_storage: dict[str, Any] | None = None
    snap_start: dict[str, Any] | None = None
    runtime_version_config: dict[str, Any] | None = None
    logging_config: dict[str, Any] | None = None


class GetFunctionEventInvokeConfigResult(BaseModel):
    """Result of get_function_event_invoke_config."""

    model_config = ConfigDict(frozen=True)

    last_modified: str | None = None
    function_arn: str | None = None
    maximum_retry_attempts: int | None = None
    maximum_event_age_in_seconds: int | None = None
    destination_config: dict[str, Any] | None = None


class GetFunctionRecursionConfigResult(BaseModel):
    """Result of get_function_recursion_config."""

    model_config = ConfigDict(frozen=True)

    recursive_loop: str | None = None


class GetFunctionUrlConfigResult(BaseModel):
    """Result of get_function_url_config."""

    model_config = ConfigDict(frozen=True)

    function_url: str | None = None
    function_arn: str | None = None
    auth_type: str | None = None
    cors: dict[str, Any] | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    invoke_mode: str | None = None


class GetLayerVersionResult(BaseModel):
    """Result of get_layer_version."""

    model_config = ConfigDict(frozen=True)

    content: dict[str, Any] | None = None
    layer_arn: str | None = None
    layer_version_arn: str | None = None
    description: str | None = None
    created_date: str | None = None
    version: int | None = None
    compatible_runtimes: list[str] | None = None
    license_info: str | None = None
    compatible_architectures: list[str] | None = None


class GetLayerVersionByArnResult(BaseModel):
    """Result of get_layer_version_by_arn."""

    model_config = ConfigDict(frozen=True)

    content: dict[str, Any] | None = None
    layer_arn: str | None = None
    layer_version_arn: str | None = None
    description: str | None = None
    created_date: str | None = None
    version: int | None = None
    compatible_runtimes: list[str] | None = None
    license_info: str | None = None
    compatible_architectures: list[str] | None = None


class GetLayerVersionPolicyResult(BaseModel):
    """Result of get_layer_version_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None
    revision_id: str | None = None


class GetPolicyResult(BaseModel):
    """Result of get_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None
    revision_id: str | None = None


class GetProvisionedConcurrencyConfigResult(BaseModel):
    """Result of get_provisioned_concurrency_config."""

    model_config = ConfigDict(frozen=True)

    requested_provisioned_concurrent_executions: int | None = None
    available_provisioned_concurrent_executions: int | None = None
    allocated_provisioned_concurrent_executions: int | None = None
    status: str | None = None
    status_reason: str | None = None
    last_modified: str | None = None


class GetRuntimeManagementConfigResult(BaseModel):
    """Result of get_runtime_management_config."""

    model_config = ConfigDict(frozen=True)

    update_runtime_on: str | None = None
    runtime_version_arn: str | None = None
    function_arn: str | None = None


class InvokeWithResponseStreamResult(BaseModel):
    """Result of invoke_with_response_stream."""

    model_config = ConfigDict(frozen=True)

    status_code: int | None = None
    executed_version: str | None = None
    event_stream: dict[str, Any] | None = None
    response_stream_content_type: str | None = None


class ListAliasesResult(BaseModel):
    """Result of list_aliases."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    aliases: list[dict[str, Any]] | None = None


class ListCodeSigningConfigsResult(BaseModel):
    """Result of list_code_signing_configs."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    code_signing_configs: list[dict[str, Any]] | None = None


class ListEventSourceMappingsResult(BaseModel):
    """Result of list_event_source_mappings."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    event_source_mappings: list[dict[str, Any]] | None = None


class ListFunctionEventInvokeConfigsResult(BaseModel):
    """Result of list_function_event_invoke_configs."""

    model_config = ConfigDict(frozen=True)

    function_event_invoke_configs: list[dict[str, Any]] | None = None
    next_marker: str | None = None


class ListFunctionUrlConfigsResult(BaseModel):
    """Result of list_function_url_configs."""

    model_config = ConfigDict(frozen=True)

    function_url_configs: list[dict[str, Any]] | None = None
    next_marker: str | None = None


class ListFunctionsResult(BaseModel):
    """Result of list_functions."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    functions: list[dict[str, Any]] | None = None


class ListFunctionsByCodeSigningConfigResult(BaseModel):
    """Result of list_functions_by_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    function_arns: list[str] | None = None


class ListLayerVersionsResult(BaseModel):
    """Result of list_layer_versions."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    layer_versions: list[dict[str, Any]] | None = None


class ListLayersResult(BaseModel):
    """Result of list_layers."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    layers: list[dict[str, Any]] | None = None


class ListProvisionedConcurrencyConfigsResult(BaseModel):
    """Result of list_provisioned_concurrency_configs."""

    model_config = ConfigDict(frozen=True)

    provisioned_concurrency_configs: list[dict[str, Any]] | None = None
    next_marker: str | None = None


class ListTagsResult(BaseModel):
    """Result of list_tags."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListVersionsByFunctionResult(BaseModel):
    """Result of list_versions_by_function."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    versions: list[dict[str, Any]] | None = None


class PublishLayerVersionResult(BaseModel):
    """Result of publish_layer_version."""

    model_config = ConfigDict(frozen=True)

    content: dict[str, Any] | None = None
    layer_arn: str | None = None
    layer_version_arn: str | None = None
    description: str | None = None
    created_date: str | None = None
    version: int | None = None
    compatible_runtimes: list[str] | None = None
    license_info: str | None = None
    compatible_architectures: list[str] | None = None


class PublishVersionResult(BaseModel):
    """Result of publish_version."""

    model_config = ConfigDict(frozen=True)

    function_name: str | None = None
    function_arn: str | None = None
    runtime: str | None = None
    role: str | None = None
    handler: str | None = None
    code_size: int | None = None
    description: str | None = None
    timeout: int | None = None
    memory_size: int | None = None
    last_modified: str | None = None
    code_sha256: str | None = None
    version: str | None = None
    vpc_config: dict[str, Any] | None = None
    dead_letter_config: dict[str, Any] | None = None
    environment: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    tracing_config: dict[str, Any] | None = None
    master_arn: str | None = None
    revision_id: str | None = None
    layers: list[dict[str, Any]] | None = None
    state: str | None = None
    state_reason: str | None = None
    state_reason_code: str | None = None
    last_update_status: str | None = None
    last_update_status_reason: str | None = None
    last_update_status_reason_code: str | None = None
    file_system_configs: list[dict[str, Any]] | None = None
    package_type: str | None = None
    image_config_response: dict[str, Any] | None = None
    signing_profile_version_arn: str | None = None
    signing_job_arn: str | None = None
    architectures: list[str] | None = None
    ephemeral_storage: dict[str, Any] | None = None
    snap_start: dict[str, Any] | None = None
    runtime_version_config: dict[str, Any] | None = None
    logging_config: dict[str, Any] | None = None


class PutFunctionCodeSigningConfigResult(BaseModel):
    """Result of put_function_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    code_signing_config_arn: str | None = None
    function_name: str | None = None


class PutFunctionConcurrencyResult(BaseModel):
    """Result of put_function_concurrency."""

    model_config = ConfigDict(frozen=True)

    reserved_concurrent_executions: int | None = None


class PutFunctionEventInvokeConfigResult(BaseModel):
    """Result of put_function_event_invoke_config."""

    model_config = ConfigDict(frozen=True)

    last_modified: str | None = None
    function_arn: str | None = None
    maximum_retry_attempts: int | None = None
    maximum_event_age_in_seconds: int | None = None
    destination_config: dict[str, Any] | None = None


class PutFunctionRecursionConfigResult(BaseModel):
    """Result of put_function_recursion_config."""

    model_config = ConfigDict(frozen=True)

    recursive_loop: str | None = None


class PutProvisionedConcurrencyConfigResult(BaseModel):
    """Result of put_provisioned_concurrency_config."""

    model_config = ConfigDict(frozen=True)

    requested_provisioned_concurrent_executions: int | None = None
    available_provisioned_concurrent_executions: int | None = None
    allocated_provisioned_concurrent_executions: int | None = None
    status: str | None = None
    status_reason: str | None = None
    last_modified: str | None = None


class PutRuntimeManagementConfigResult(BaseModel):
    """Result of put_runtime_management_config."""

    model_config = ConfigDict(frozen=True)

    update_runtime_on: str | None = None
    function_arn: str | None = None
    runtime_version_arn: str | None = None


class UpdateAliasResult(BaseModel):
    """Result of update_alias."""

    model_config = ConfigDict(frozen=True)

    alias_arn: str | None = None
    name: str | None = None
    function_version: str | None = None
    description: str | None = None
    routing_config: dict[str, Any] | None = None
    revision_id: str | None = None


class UpdateCodeSigningConfigResult(BaseModel):
    """Result of update_code_signing_config."""

    model_config = ConfigDict(frozen=True)

    code_signing_config: dict[str, Any] | None = None


class UpdateEventSourceMappingResult(BaseModel):
    """Result of update_event_source_mapping."""

    model_config = ConfigDict(frozen=True)

    uuid: str | None = None
    starting_position: str | None = None
    starting_position_timestamp: str | None = None
    batch_size: int | None = None
    maximum_batching_window_in_seconds: int | None = None
    parallelization_factor: int | None = None
    event_source_arn: str | None = None
    filter_criteria: dict[str, Any] | None = None
    function_arn: str | None = None
    last_modified: str | None = None
    last_processing_result: str | None = None
    state: str | None = None
    state_transition_reason: str | None = None
    destination_config: dict[str, Any] | None = None
    topics: list[str] | None = None
    queues: list[str] | None = None
    source_access_configurations: list[dict[str, Any]] | None = None
    self_managed_event_source: dict[str, Any] | None = None
    maximum_record_age_in_seconds: int | None = None
    bisect_batch_on_function_error: bool | None = None
    maximum_retry_attempts: int | None = None
    tumbling_window_in_seconds: int | None = None
    function_response_types: list[str] | None = None
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None
    self_managed_kafka_event_source_config: dict[str, Any] | None = None
    scaling_config: dict[str, Any] | None = None
    document_db_event_source_config: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    filter_criteria_error: dict[str, Any] | None = None
    event_source_mapping_arn: str | None = None
    metrics_config: dict[str, Any] | None = None
    provisioned_poller_config: dict[str, Any] | None = None


class UpdateFunctionCodeResult(BaseModel):
    """Result of update_function_code."""

    model_config = ConfigDict(frozen=True)

    function_name: str | None = None
    function_arn: str | None = None
    runtime: str | None = None
    role: str | None = None
    handler: str | None = None
    code_size: int | None = None
    description: str | None = None
    timeout: int | None = None
    memory_size: int | None = None
    last_modified: str | None = None
    code_sha256: str | None = None
    version: str | None = None
    vpc_config: dict[str, Any] | None = None
    dead_letter_config: dict[str, Any] | None = None
    environment: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    tracing_config: dict[str, Any] | None = None
    master_arn: str | None = None
    revision_id: str | None = None
    layers: list[dict[str, Any]] | None = None
    state: str | None = None
    state_reason: str | None = None
    state_reason_code: str | None = None
    last_update_status: str | None = None
    last_update_status_reason: str | None = None
    last_update_status_reason_code: str | None = None
    file_system_configs: list[dict[str, Any]] | None = None
    package_type: str | None = None
    image_config_response: dict[str, Any] | None = None
    signing_profile_version_arn: str | None = None
    signing_job_arn: str | None = None
    architectures: list[str] | None = None
    ephemeral_storage: dict[str, Any] | None = None
    snap_start: dict[str, Any] | None = None
    runtime_version_config: dict[str, Any] | None = None
    logging_config: dict[str, Any] | None = None


class UpdateFunctionConfigurationResult(BaseModel):
    """Result of update_function_configuration."""

    model_config = ConfigDict(frozen=True)

    function_name: str | None = None
    function_arn: str | None = None
    runtime: str | None = None
    role: str | None = None
    handler: str | None = None
    code_size: int | None = None
    description: str | None = None
    timeout: int | None = None
    memory_size: int | None = None
    last_modified: str | None = None
    code_sha256: str | None = None
    version: str | None = None
    vpc_config: dict[str, Any] | None = None
    dead_letter_config: dict[str, Any] | None = None
    environment: dict[str, Any] | None = None
    kms_key_arn: str | None = None
    tracing_config: dict[str, Any] | None = None
    master_arn: str | None = None
    revision_id: str | None = None
    layers: list[dict[str, Any]] | None = None
    state: str | None = None
    state_reason: str | None = None
    state_reason_code: str | None = None
    last_update_status: str | None = None
    last_update_status_reason: str | None = None
    last_update_status_reason_code: str | None = None
    file_system_configs: list[dict[str, Any]] | None = None
    package_type: str | None = None
    image_config_response: dict[str, Any] | None = None
    signing_profile_version_arn: str | None = None
    signing_job_arn: str | None = None
    architectures: list[str] | None = None
    ephemeral_storage: dict[str, Any] | None = None
    snap_start: dict[str, Any] | None = None
    runtime_version_config: dict[str, Any] | None = None
    logging_config: dict[str, Any] | None = None


class UpdateFunctionEventInvokeConfigResult(BaseModel):
    """Result of update_function_event_invoke_config."""

    model_config = ConfigDict(frozen=True)

    last_modified: str | None = None
    function_arn: str | None = None
    maximum_retry_attempts: int | None = None
    maximum_event_age_in_seconds: int | None = None
    destination_config: dict[str, Any] | None = None


class UpdateFunctionUrlConfigResult(BaseModel):
    """Result of update_function_url_config."""

    model_config = ConfigDict(frozen=True)

    function_url: str | None = None
    function_arn: str | None = None
    auth_type: str | None = None
    cors: dict[str, Any] | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    invoke_mode: str | None = None


def add_layer_version_permission(
    layer_name: str,
    version_number: int,
    statement_id: str,
    action: str,
    principal: str,
    *,
    organization_id: str | None = None,
    revision_id: str | None = None,
    region_name: str | None = None,
) -> AddLayerVersionPermissionResult:
    """Add layer version permission.

    Args:
        layer_name: Layer name.
        version_number: Version number.
        statement_id: Statement id.
        action: Action.
        principal: Principal.
        organization_id: Organization id.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["VersionNumber"] = version_number
    kwargs["StatementId"] = statement_id
    kwargs["Action"] = action
    kwargs["Principal"] = principal
    if organization_id is not None:
        kwargs["OrganizationId"] = organization_id
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    try:
        resp = client.add_layer_version_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add layer version permission") from exc
    return AddLayerVersionPermissionResult(
        statement=resp.get("Statement"),
        revision_id=resp.get("RevisionId"),
    )


def add_permission(
    function_name: str,
    statement_id: str,
    action: str,
    principal: str,
    *,
    source_arn: str | None = None,
    source_account: str | None = None,
    event_source_token: str | None = None,
    qualifier: str | None = None,
    revision_id: str | None = None,
    principal_org_id: str | None = None,
    function_url_auth_type: str | None = None,
    invoked_via_function_url: bool | None = None,
    region_name: str | None = None,
) -> AddPermissionResult:
    """Add permission.

    Args:
        function_name: Function name.
        statement_id: Statement id.
        action: Action.
        principal: Principal.
        source_arn: Source arn.
        source_account: Source account.
        event_source_token: Event source token.
        qualifier: Qualifier.
        revision_id: Revision id.
        principal_org_id: Principal org id.
        function_url_auth_type: Function url auth type.
        invoked_via_function_url: Invoked via function url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["StatementId"] = statement_id
    kwargs["Action"] = action
    kwargs["Principal"] = principal
    if source_arn is not None:
        kwargs["SourceArn"] = source_arn
    if source_account is not None:
        kwargs["SourceAccount"] = source_account
    if event_source_token is not None:
        kwargs["EventSourceToken"] = event_source_token
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    if principal_org_id is not None:
        kwargs["PrincipalOrgID"] = principal_org_id
    if function_url_auth_type is not None:
        kwargs["FunctionUrlAuthType"] = function_url_auth_type
    if invoked_via_function_url is not None:
        kwargs["InvokedViaFunctionUrl"] = invoked_via_function_url
    try:
        resp = client.add_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add permission") from exc
    return AddPermissionResult(
        statement=resp.get("Statement"),
    )


def create_alias(
    function_name: str,
    name: str,
    function_version: str,
    *,
    description: str | None = None,
    routing_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAliasResult:
    """Create alias.

    Args:
        function_name: Function name.
        name: Name.
        function_version: Function version.
        description: Description.
        routing_config: Routing config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Name"] = name
    kwargs["FunctionVersion"] = function_version
    if description is not None:
        kwargs["Description"] = description
    if routing_config is not None:
        kwargs["RoutingConfig"] = routing_config
    try:
        resp = client.create_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create alias") from exc
    return CreateAliasResult(
        alias_arn=resp.get("AliasArn"),
        name=resp.get("Name"),
        function_version=resp.get("FunctionVersion"),
        description=resp.get("Description"),
        routing_config=resp.get("RoutingConfig"),
        revision_id=resp.get("RevisionId"),
    )


def create_code_signing_config(
    allowed_publishers: dict[str, Any],
    *,
    description: str | None = None,
    code_signing_policies: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCodeSigningConfigResult:
    """Create code signing config.

    Args:
        allowed_publishers: Allowed publishers.
        description: Description.
        code_signing_policies: Code signing policies.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AllowedPublishers"] = allowed_publishers
    if description is not None:
        kwargs["Description"] = description
    if code_signing_policies is not None:
        kwargs["CodeSigningPolicies"] = code_signing_policies
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create code signing config") from exc
    return CreateCodeSigningConfigResult(
        code_signing_config=resp.get("CodeSigningConfig"),
    )


def create_event_source_mapping(
    function_name: str,
    *,
    event_source_arn: str | None = None,
    enabled: bool | None = None,
    batch_size: int | None = None,
    filter_criteria: dict[str, Any] | None = None,
    maximum_batching_window_in_seconds: int | None = None,
    parallelization_factor: int | None = None,
    starting_position: str | None = None,
    starting_position_timestamp: str | None = None,
    destination_config: dict[str, Any] | None = None,
    maximum_record_age_in_seconds: int | None = None,
    bisect_batch_on_function_error: bool | None = None,
    maximum_retry_attempts: int | None = None,
    tags: dict[str, Any] | None = None,
    tumbling_window_in_seconds: int | None = None,
    topics: list[str] | None = None,
    queues: list[str] | None = None,
    source_access_configurations: list[dict[str, Any]] | None = None,
    self_managed_event_source: dict[str, Any] | None = None,
    function_response_types: list[str] | None = None,
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None,
    self_managed_kafka_event_source_config: dict[str, Any] | None = None,
    scaling_config: dict[str, Any] | None = None,
    document_db_event_source_config: dict[str, Any] | None = None,
    kms_key_arn: str | None = None,
    metrics_config: dict[str, Any] | None = None,
    provisioned_poller_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateEventSourceMappingResult:
    """Create event source mapping.

    Args:
        function_name: Function name.
        event_source_arn: Event source arn.
        enabled: Enabled.
        batch_size: Batch size.
        filter_criteria: Filter criteria.
        maximum_batching_window_in_seconds: Maximum batching window in seconds.
        parallelization_factor: Parallelization factor.
        starting_position: Starting position.
        starting_position_timestamp: Starting position timestamp.
        destination_config: Destination config.
        maximum_record_age_in_seconds: Maximum record age in seconds.
        bisect_batch_on_function_error: Bisect batch on function error.
        maximum_retry_attempts: Maximum retry attempts.
        tags: Tags.
        tumbling_window_in_seconds: Tumbling window in seconds.
        topics: Topics.
        queues: Queues.
        source_access_configurations: Source access configurations.
        self_managed_event_source: Self managed event source.
        function_response_types: Function response types.
        amazon_managed_kafka_event_source_config: Amazon managed kafka event source config.
        self_managed_kafka_event_source_config: Self managed kafka event source config.
        scaling_config: Scaling config.
        document_db_event_source_config: Document db event source config.
        kms_key_arn: Kms key arn.
        metrics_config: Metrics config.
        provisioned_poller_config: Provisioned poller config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if event_source_arn is not None:
        kwargs["EventSourceArn"] = event_source_arn
    if enabled is not None:
        kwargs["Enabled"] = enabled
    if batch_size is not None:
        kwargs["BatchSize"] = batch_size
    if filter_criteria is not None:
        kwargs["FilterCriteria"] = filter_criteria
    if maximum_batching_window_in_seconds is not None:
        kwargs["MaximumBatchingWindowInSeconds"] = maximum_batching_window_in_seconds
    if parallelization_factor is not None:
        kwargs["ParallelizationFactor"] = parallelization_factor
    if starting_position is not None:
        kwargs["StartingPosition"] = starting_position
    if starting_position_timestamp is not None:
        kwargs["StartingPositionTimestamp"] = starting_position_timestamp
    if destination_config is not None:
        kwargs["DestinationConfig"] = destination_config
    if maximum_record_age_in_seconds is not None:
        kwargs["MaximumRecordAgeInSeconds"] = maximum_record_age_in_seconds
    if bisect_batch_on_function_error is not None:
        kwargs["BisectBatchOnFunctionError"] = bisect_batch_on_function_error
    if maximum_retry_attempts is not None:
        kwargs["MaximumRetryAttempts"] = maximum_retry_attempts
    if tags is not None:
        kwargs["Tags"] = tags
    if tumbling_window_in_seconds is not None:
        kwargs["TumblingWindowInSeconds"] = tumbling_window_in_seconds
    if topics is not None:
        kwargs["Topics"] = topics
    if queues is not None:
        kwargs["Queues"] = queues
    if source_access_configurations is not None:
        kwargs["SourceAccessConfigurations"] = source_access_configurations
    if self_managed_event_source is not None:
        kwargs["SelfManagedEventSource"] = self_managed_event_source
    if function_response_types is not None:
        kwargs["FunctionResponseTypes"] = function_response_types
    if amazon_managed_kafka_event_source_config is not None:
        kwargs["AmazonManagedKafkaEventSourceConfig"] = amazon_managed_kafka_event_source_config
    if self_managed_kafka_event_source_config is not None:
        kwargs["SelfManagedKafkaEventSourceConfig"] = self_managed_kafka_event_source_config
    if scaling_config is not None:
        kwargs["ScalingConfig"] = scaling_config
    if document_db_event_source_config is not None:
        kwargs["DocumentDBEventSourceConfig"] = document_db_event_source_config
    if kms_key_arn is not None:
        kwargs["KMSKeyArn"] = kms_key_arn
    if metrics_config is not None:
        kwargs["MetricsConfig"] = metrics_config
    if provisioned_poller_config is not None:
        kwargs["ProvisionedPollerConfig"] = provisioned_poller_config
    try:
        resp = client.create_event_source_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create event source mapping") from exc
    return CreateEventSourceMappingResult(
        uuid=resp.get("UUID"),
        starting_position=resp.get("StartingPosition"),
        starting_position_timestamp=resp.get("StartingPositionTimestamp"),
        batch_size=resp.get("BatchSize"),
        maximum_batching_window_in_seconds=resp.get("MaximumBatchingWindowInSeconds"),
        parallelization_factor=resp.get("ParallelizationFactor"),
        event_source_arn=resp.get("EventSourceArn"),
        filter_criteria=resp.get("FilterCriteria"),
        function_arn=resp.get("FunctionArn"),
        last_modified=resp.get("LastModified"),
        last_processing_result=resp.get("LastProcessingResult"),
        state=resp.get("State"),
        state_transition_reason=resp.get("StateTransitionReason"),
        destination_config=resp.get("DestinationConfig"),
        topics=resp.get("Topics"),
        queues=resp.get("Queues"),
        source_access_configurations=resp.get("SourceAccessConfigurations"),
        self_managed_event_source=resp.get("SelfManagedEventSource"),
        maximum_record_age_in_seconds=resp.get("MaximumRecordAgeInSeconds"),
        bisect_batch_on_function_error=resp.get("BisectBatchOnFunctionError"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        tumbling_window_in_seconds=resp.get("TumblingWindowInSeconds"),
        function_response_types=resp.get("FunctionResponseTypes"),
        amazon_managed_kafka_event_source_config=resp.get("AmazonManagedKafkaEventSourceConfig"),
        self_managed_kafka_event_source_config=resp.get("SelfManagedKafkaEventSourceConfig"),
        scaling_config=resp.get("ScalingConfig"),
        document_db_event_source_config=resp.get("DocumentDBEventSourceConfig"),
        kms_key_arn=resp.get("KMSKeyArn"),
        filter_criteria_error=resp.get("FilterCriteriaError"),
        event_source_mapping_arn=resp.get("EventSourceMappingArn"),
        metrics_config=resp.get("MetricsConfig"),
        provisioned_poller_config=resp.get("ProvisionedPollerConfig"),
    )


def create_function(
    function_name: str,
    role: str,
    code: dict[str, Any],
    *,
    runtime: str | None = None,
    handler: str | None = None,
    description: str | None = None,
    timeout: int | None = None,
    memory_size: int | None = None,
    publish: bool | None = None,
    vpc_config: dict[str, Any] | None = None,
    package_type: str | None = None,
    dead_letter_config: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    kms_key_arn: str | None = None,
    tracing_config: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    layers: list[str] | None = None,
    file_system_configs: list[dict[str, Any]] | None = None,
    image_config: dict[str, Any] | None = None,
    code_signing_config_arn: str | None = None,
    architectures: list[str] | None = None,
    ephemeral_storage: dict[str, Any] | None = None,
    snap_start: dict[str, Any] | None = None,
    logging_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateFunctionResult:
    """Create function.

    Args:
        function_name: Function name.
        role: Role.
        code: Code.
        runtime: Runtime.
        handler: Handler.
        description: Description.
        timeout: Timeout.
        memory_size: Memory size.
        publish: Publish.
        vpc_config: Vpc config.
        package_type: Package type.
        dead_letter_config: Dead letter config.
        environment: Environment.
        kms_key_arn: Kms key arn.
        tracing_config: Tracing config.
        tags: Tags.
        layers: Layers.
        file_system_configs: File system configs.
        image_config: Image config.
        code_signing_config_arn: Code signing config arn.
        architectures: Architectures.
        ephemeral_storage: Ephemeral storage.
        snap_start: Snap start.
        logging_config: Logging config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Role"] = role
    kwargs["Code"] = code
    if runtime is not None:
        kwargs["Runtime"] = runtime
    if handler is not None:
        kwargs["Handler"] = handler
    if description is not None:
        kwargs["Description"] = description
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if memory_size is not None:
        kwargs["MemorySize"] = memory_size
    if publish is not None:
        kwargs["Publish"] = publish
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if package_type is not None:
        kwargs["PackageType"] = package_type
    if dead_letter_config is not None:
        kwargs["DeadLetterConfig"] = dead_letter_config
    if environment is not None:
        kwargs["Environment"] = environment
    if kms_key_arn is not None:
        kwargs["KMSKeyArn"] = kms_key_arn
    if tracing_config is not None:
        kwargs["TracingConfig"] = tracing_config
    if tags is not None:
        kwargs["Tags"] = tags
    if layers is not None:
        kwargs["Layers"] = layers
    if file_system_configs is not None:
        kwargs["FileSystemConfigs"] = file_system_configs
    if image_config is not None:
        kwargs["ImageConfig"] = image_config
    if code_signing_config_arn is not None:
        kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    if architectures is not None:
        kwargs["Architectures"] = architectures
    if ephemeral_storage is not None:
        kwargs["EphemeralStorage"] = ephemeral_storage
    if snap_start is not None:
        kwargs["SnapStart"] = snap_start
    if logging_config is not None:
        kwargs["LoggingConfig"] = logging_config
    try:
        resp = client.create_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create function") from exc
    return CreateFunctionResult(
        function_name=resp.get("FunctionName"),
        function_arn=resp.get("FunctionArn"),
        runtime=resp.get("Runtime"),
        role=resp.get("Role"),
        handler=resp.get("Handler"),
        code_size=resp.get("CodeSize"),
        description=resp.get("Description"),
        timeout=resp.get("Timeout"),
        memory_size=resp.get("MemorySize"),
        last_modified=resp.get("LastModified"),
        code_sha256=resp.get("CodeSha256"),
        version=resp.get("Version"),
        vpc_config=resp.get("VpcConfig"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        environment=resp.get("Environment"),
        kms_key_arn=resp.get("KMSKeyArn"),
        tracing_config=resp.get("TracingConfig"),
        master_arn=resp.get("MasterArn"),
        revision_id=resp.get("RevisionId"),
        layers=resp.get("Layers"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        state_reason_code=resp.get("StateReasonCode"),
        last_update_status=resp.get("LastUpdateStatus"),
        last_update_status_reason=resp.get("LastUpdateStatusReason"),
        last_update_status_reason_code=resp.get("LastUpdateStatusReasonCode"),
        file_system_configs=resp.get("FileSystemConfigs"),
        package_type=resp.get("PackageType"),
        image_config_response=resp.get("ImageConfigResponse"),
        signing_profile_version_arn=resp.get("SigningProfileVersionArn"),
        signing_job_arn=resp.get("SigningJobArn"),
        architectures=resp.get("Architectures"),
        ephemeral_storage=resp.get("EphemeralStorage"),
        snap_start=resp.get("SnapStart"),
        runtime_version_config=resp.get("RuntimeVersionConfig"),
        logging_config=resp.get("LoggingConfig"),
    )


def create_function_url_config(
    function_name: str,
    auth_type: str,
    *,
    qualifier: str | None = None,
    cors: dict[str, Any] | None = None,
    invoke_mode: str | None = None,
    region_name: str | None = None,
) -> CreateFunctionUrlConfigResult:
    """Create function url config.

    Args:
        function_name: Function name.
        auth_type: Auth type.
        qualifier: Qualifier.
        cors: Cors.
        invoke_mode: Invoke mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["AuthType"] = auth_type
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if cors is not None:
        kwargs["Cors"] = cors
    if invoke_mode is not None:
        kwargs["InvokeMode"] = invoke_mode
    try:
        resp = client.create_function_url_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create function url config") from exc
    return CreateFunctionUrlConfigResult(
        function_url=resp.get("FunctionUrl"),
        function_arn=resp.get("FunctionArn"),
        auth_type=resp.get("AuthType"),
        cors=resp.get("Cors"),
        creation_time=resp.get("CreationTime"),
        invoke_mode=resp.get("InvokeMode"),
    )


def delete_alias(
    function_name: str,
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete alias.

    Args:
        function_name: Function name.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Name"] = name
    try:
        client.delete_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete alias") from exc
    return None


def delete_code_signing_config(
    code_signing_config_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete code signing config.

    Args:
        code_signing_config_arn: Code signing config arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    try:
        client.delete_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete code signing config") from exc
    return None


def delete_event_source_mapping(
    uuid: str,
    region_name: str | None = None,
) -> DeleteEventSourceMappingResult:
    """Delete event source mapping.

    Args:
        uuid: Uuid.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UUID"] = uuid
    try:
        resp = client.delete_event_source_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete event source mapping") from exc
    return DeleteEventSourceMappingResult(
        uuid=resp.get("UUID"),
        starting_position=resp.get("StartingPosition"),
        starting_position_timestamp=resp.get("StartingPositionTimestamp"),
        batch_size=resp.get("BatchSize"),
        maximum_batching_window_in_seconds=resp.get("MaximumBatchingWindowInSeconds"),
        parallelization_factor=resp.get("ParallelizationFactor"),
        event_source_arn=resp.get("EventSourceArn"),
        filter_criteria=resp.get("FilterCriteria"),
        function_arn=resp.get("FunctionArn"),
        last_modified=resp.get("LastModified"),
        last_processing_result=resp.get("LastProcessingResult"),
        state=resp.get("State"),
        state_transition_reason=resp.get("StateTransitionReason"),
        destination_config=resp.get("DestinationConfig"),
        topics=resp.get("Topics"),
        queues=resp.get("Queues"),
        source_access_configurations=resp.get("SourceAccessConfigurations"),
        self_managed_event_source=resp.get("SelfManagedEventSource"),
        maximum_record_age_in_seconds=resp.get("MaximumRecordAgeInSeconds"),
        bisect_batch_on_function_error=resp.get("BisectBatchOnFunctionError"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        tumbling_window_in_seconds=resp.get("TumblingWindowInSeconds"),
        function_response_types=resp.get("FunctionResponseTypes"),
        amazon_managed_kafka_event_source_config=resp.get("AmazonManagedKafkaEventSourceConfig"),
        self_managed_kafka_event_source_config=resp.get("SelfManagedKafkaEventSourceConfig"),
        scaling_config=resp.get("ScalingConfig"),
        document_db_event_source_config=resp.get("DocumentDBEventSourceConfig"),
        kms_key_arn=resp.get("KMSKeyArn"),
        filter_criteria_error=resp.get("FilterCriteriaError"),
        event_source_mapping_arn=resp.get("EventSourceMappingArn"),
        metrics_config=resp.get("MetricsConfig"),
        provisioned_poller_config=resp.get("ProvisionedPollerConfig"),
    )


def delete_function(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete function.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        client.delete_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function") from exc
    return None


def delete_function_code_signing_config(
    function_name: str,
    region_name: str | None = None,
) -> None:
    """Delete function code signing config.

    Args:
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    try:
        client.delete_function_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function code signing config") from exc
    return None


def delete_function_concurrency(
    function_name: str,
    region_name: str | None = None,
) -> None:
    """Delete function concurrency.

    Args:
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    try:
        client.delete_function_concurrency(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function concurrency") from exc
    return None


def delete_function_event_invoke_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete function event invoke config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        client.delete_function_event_invoke_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function event invoke config") from exc
    return None


def delete_function_url_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete function url config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        client.delete_function_url_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function url config") from exc
    return None


def delete_layer_version(
    layer_name: str,
    version_number: int,
    region_name: str | None = None,
) -> None:
    """Delete layer version.

    Args:
        layer_name: Layer name.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["VersionNumber"] = version_number
    try:
        client.delete_layer_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete layer version") from exc
    return None


def delete_provisioned_concurrency_config(
    function_name: str,
    qualifier: str,
    region_name: str | None = None,
) -> None:
    """Delete provisioned concurrency config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Qualifier"] = qualifier
    try:
        client.delete_provisioned_concurrency_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete provisioned concurrency config") from exc
    return None


def get_account_settings(
    region_name: str | None = None,
) -> GetAccountSettingsResult:
    """Get account settings.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_account_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get account settings") from exc
    return GetAccountSettingsResult(
        account_limit=resp.get("AccountLimit"),
        account_usage=resp.get("AccountUsage"),
    )


def get_alias(
    function_name: str,
    name: str,
    region_name: str | None = None,
) -> GetAliasResult:
    """Get alias.

    Args:
        function_name: Function name.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Name"] = name
    try:
        resp = client.get_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get alias") from exc
    return GetAliasResult(
        alias_arn=resp.get("AliasArn"),
        name=resp.get("Name"),
        function_version=resp.get("FunctionVersion"),
        description=resp.get("Description"),
        routing_config=resp.get("RoutingConfig"),
        revision_id=resp.get("RevisionId"),
    )


def get_code_signing_config(
    code_signing_config_arn: str,
    region_name: str | None = None,
) -> GetCodeSigningConfigResult:
    """Get code signing config.

    Args:
        code_signing_config_arn: Code signing config arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    try:
        resp = client.get_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get code signing config") from exc
    return GetCodeSigningConfigResult(
        code_signing_config=resp.get("CodeSigningConfig"),
    )


def get_event_source_mapping(
    uuid: str,
    region_name: str | None = None,
) -> GetEventSourceMappingResult:
    """Get event source mapping.

    Args:
        uuid: Uuid.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UUID"] = uuid
    try:
        resp = client.get_event_source_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get event source mapping") from exc
    return GetEventSourceMappingResult(
        uuid=resp.get("UUID"),
        starting_position=resp.get("StartingPosition"),
        starting_position_timestamp=resp.get("StartingPositionTimestamp"),
        batch_size=resp.get("BatchSize"),
        maximum_batching_window_in_seconds=resp.get("MaximumBatchingWindowInSeconds"),
        parallelization_factor=resp.get("ParallelizationFactor"),
        event_source_arn=resp.get("EventSourceArn"),
        filter_criteria=resp.get("FilterCriteria"),
        function_arn=resp.get("FunctionArn"),
        last_modified=resp.get("LastModified"),
        last_processing_result=resp.get("LastProcessingResult"),
        state=resp.get("State"),
        state_transition_reason=resp.get("StateTransitionReason"),
        destination_config=resp.get("DestinationConfig"),
        topics=resp.get("Topics"),
        queues=resp.get("Queues"),
        source_access_configurations=resp.get("SourceAccessConfigurations"),
        self_managed_event_source=resp.get("SelfManagedEventSource"),
        maximum_record_age_in_seconds=resp.get("MaximumRecordAgeInSeconds"),
        bisect_batch_on_function_error=resp.get("BisectBatchOnFunctionError"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        tumbling_window_in_seconds=resp.get("TumblingWindowInSeconds"),
        function_response_types=resp.get("FunctionResponseTypes"),
        amazon_managed_kafka_event_source_config=resp.get("AmazonManagedKafkaEventSourceConfig"),
        self_managed_kafka_event_source_config=resp.get("SelfManagedKafkaEventSourceConfig"),
        scaling_config=resp.get("ScalingConfig"),
        document_db_event_source_config=resp.get("DocumentDBEventSourceConfig"),
        kms_key_arn=resp.get("KMSKeyArn"),
        filter_criteria_error=resp.get("FilterCriteriaError"),
        event_source_mapping_arn=resp.get("EventSourceMappingArn"),
        metrics_config=resp.get("MetricsConfig"),
        provisioned_poller_config=resp.get("ProvisionedPollerConfig"),
    )


def get_function(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetFunctionResult:
    """Get function.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function") from exc
    return GetFunctionResult(
        configuration=resp.get("Configuration"),
        code=resp.get("Code"),
        tags=resp.get("Tags"),
        tags_error=resp.get("TagsError"),
        concurrency=resp.get("Concurrency"),
    )


def get_function_code_signing_config(
    function_name: str,
    region_name: str | None = None,
) -> GetFunctionCodeSigningConfigResult:
    """Get function code signing config.

    Args:
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    try:
        resp = client.get_function_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function code signing config") from exc
    return GetFunctionCodeSigningConfigResult(
        code_signing_config_arn=resp.get("CodeSigningConfigArn"),
        function_name=resp.get("FunctionName"),
    )


def get_function_concurrency(
    function_name: str,
    region_name: str | None = None,
) -> GetFunctionConcurrencyResult:
    """Get function concurrency.

    Args:
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    try:
        resp = client.get_function_concurrency(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function concurrency") from exc
    return GetFunctionConcurrencyResult(
        reserved_concurrent_executions=resp.get("ReservedConcurrentExecutions"),
    )


def get_function_configuration(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetFunctionConfigurationResult:
    """Get function configuration.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_function_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function configuration") from exc
    return GetFunctionConfigurationResult(
        function_name=resp.get("FunctionName"),
        function_arn=resp.get("FunctionArn"),
        runtime=resp.get("Runtime"),
        role=resp.get("Role"),
        handler=resp.get("Handler"),
        code_size=resp.get("CodeSize"),
        description=resp.get("Description"),
        timeout=resp.get("Timeout"),
        memory_size=resp.get("MemorySize"),
        last_modified=resp.get("LastModified"),
        code_sha256=resp.get("CodeSha256"),
        version=resp.get("Version"),
        vpc_config=resp.get("VpcConfig"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        environment=resp.get("Environment"),
        kms_key_arn=resp.get("KMSKeyArn"),
        tracing_config=resp.get("TracingConfig"),
        master_arn=resp.get("MasterArn"),
        revision_id=resp.get("RevisionId"),
        layers=resp.get("Layers"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        state_reason_code=resp.get("StateReasonCode"),
        last_update_status=resp.get("LastUpdateStatus"),
        last_update_status_reason=resp.get("LastUpdateStatusReason"),
        last_update_status_reason_code=resp.get("LastUpdateStatusReasonCode"),
        file_system_configs=resp.get("FileSystemConfigs"),
        package_type=resp.get("PackageType"),
        image_config_response=resp.get("ImageConfigResponse"),
        signing_profile_version_arn=resp.get("SigningProfileVersionArn"),
        signing_job_arn=resp.get("SigningJobArn"),
        architectures=resp.get("Architectures"),
        ephemeral_storage=resp.get("EphemeralStorage"),
        snap_start=resp.get("SnapStart"),
        runtime_version_config=resp.get("RuntimeVersionConfig"),
        logging_config=resp.get("LoggingConfig"),
    )


def get_function_event_invoke_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetFunctionEventInvokeConfigResult:
    """Get function event invoke config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_function_event_invoke_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function event invoke config") from exc
    return GetFunctionEventInvokeConfigResult(
        last_modified=resp.get("LastModified"),
        function_arn=resp.get("FunctionArn"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        maximum_event_age_in_seconds=resp.get("MaximumEventAgeInSeconds"),
        destination_config=resp.get("DestinationConfig"),
    )


def get_function_recursion_config(
    function_name: str,
    region_name: str | None = None,
) -> GetFunctionRecursionConfigResult:
    """Get function recursion config.

    Args:
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    try:
        resp = client.get_function_recursion_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function recursion config") from exc
    return GetFunctionRecursionConfigResult(
        recursive_loop=resp.get("RecursiveLoop"),
    )


def get_function_url_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetFunctionUrlConfigResult:
    """Get function url config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_function_url_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function url config") from exc
    return GetFunctionUrlConfigResult(
        function_url=resp.get("FunctionUrl"),
        function_arn=resp.get("FunctionArn"),
        auth_type=resp.get("AuthType"),
        cors=resp.get("Cors"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        invoke_mode=resp.get("InvokeMode"),
    )


def get_layer_version(
    layer_name: str,
    version_number: int,
    region_name: str | None = None,
) -> GetLayerVersionResult:
    """Get layer version.

    Args:
        layer_name: Layer name.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["VersionNumber"] = version_number
    try:
        resp = client.get_layer_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get layer version") from exc
    return GetLayerVersionResult(
        content=resp.get("Content"),
        layer_arn=resp.get("LayerArn"),
        layer_version_arn=resp.get("LayerVersionArn"),
        description=resp.get("Description"),
        created_date=resp.get("CreatedDate"),
        version=resp.get("Version"),
        compatible_runtimes=resp.get("CompatibleRuntimes"),
        license_info=resp.get("LicenseInfo"),
        compatible_architectures=resp.get("CompatibleArchitectures"),
    )


def get_layer_version_by_arn(
    arn: str,
    region_name: str | None = None,
) -> GetLayerVersionByArnResult:
    """Get layer version by arn.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = client.get_layer_version_by_arn(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get layer version by arn") from exc
    return GetLayerVersionByArnResult(
        content=resp.get("Content"),
        layer_arn=resp.get("LayerArn"),
        layer_version_arn=resp.get("LayerVersionArn"),
        description=resp.get("Description"),
        created_date=resp.get("CreatedDate"),
        version=resp.get("Version"),
        compatible_runtimes=resp.get("CompatibleRuntimes"),
        license_info=resp.get("LicenseInfo"),
        compatible_architectures=resp.get("CompatibleArchitectures"),
    )


def get_layer_version_policy(
    layer_name: str,
    version_number: int,
    region_name: str | None = None,
) -> GetLayerVersionPolicyResult:
    """Get layer version policy.

    Args:
        layer_name: Layer name.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["VersionNumber"] = version_number
    try:
        resp = client.get_layer_version_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get layer version policy") from exc
    return GetLayerVersionPolicyResult(
        policy=resp.get("Policy"),
        revision_id=resp.get("RevisionId"),
    )


def get_policy(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetPolicyResult:
    """Get policy.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get policy") from exc
    return GetPolicyResult(
        policy=resp.get("Policy"),
        revision_id=resp.get("RevisionId"),
    )


def get_provisioned_concurrency_config(
    function_name: str,
    qualifier: str,
    region_name: str | None = None,
) -> GetProvisionedConcurrencyConfigResult:
    """Get provisioned concurrency config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_provisioned_concurrency_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get provisioned concurrency config") from exc
    return GetProvisionedConcurrencyConfigResult(
        requested_provisioned_concurrent_executions=resp.get(
            "RequestedProvisionedConcurrentExecutions"
        ),
        available_provisioned_concurrent_executions=resp.get(
            "AvailableProvisionedConcurrentExecutions"
        ),
        allocated_provisioned_concurrent_executions=resp.get(
            "AllocatedProvisionedConcurrentExecutions"
        ),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        last_modified=resp.get("LastModified"),
    )


def get_runtime_management_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    region_name: str | None = None,
) -> GetRuntimeManagementConfigResult:
    """Get runtime management config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    try:
        resp = client.get_runtime_management_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get runtime management config") from exc
    return GetRuntimeManagementConfigResult(
        update_runtime_on=resp.get("UpdateRuntimeOn"),
        runtime_version_arn=resp.get("RuntimeVersionArn"),
        function_arn=resp.get("FunctionArn"),
    )


def invoke_with_response_stream(
    function_name: str,
    *,
    invocation_type: str | None = None,
    log_type: str | None = None,
    client_context: str | None = None,
    qualifier: str | None = None,
    payload: bytes | None = None,
    region_name: str | None = None,
) -> InvokeWithResponseStreamResult:
    """Invoke with response stream.

    Args:
        function_name: Function name.
        invocation_type: Invocation type.
        log_type: Log type.
        client_context: Client context.
        qualifier: Qualifier.
        payload: Payload.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if invocation_type is not None:
        kwargs["InvocationType"] = invocation_type
    if log_type is not None:
        kwargs["LogType"] = log_type
    if client_context is not None:
        kwargs["ClientContext"] = client_context
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if payload is not None:
        kwargs["Payload"] = payload
    try:
        resp = client.invoke_with_response_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to invoke with response stream") from exc
    return InvokeWithResponseStreamResult(
        status_code=resp.get("StatusCode"),
        executed_version=resp.get("ExecutedVersion"),
        event_stream=resp.get("EventStream"),
        response_stream_content_type=resp.get("ResponseStreamContentType"),
    )


def list_aliases(
    function_name: str,
    *,
    function_version: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAliasesResult:
    """List aliases.

    Args:
        function_name: Function name.
        function_version: Function version.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if function_version is not None:
        kwargs["FunctionVersion"] = function_version
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_aliases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list aliases") from exc
    return ListAliasesResult(
        next_marker=resp.get("NextMarker"),
        aliases=resp.get("Aliases"),
    )


def list_code_signing_configs(
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListCodeSigningConfigsResult:
    """List code signing configs.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_code_signing_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list code signing configs") from exc
    return ListCodeSigningConfigsResult(
        next_marker=resp.get("NextMarker"),
        code_signing_configs=resp.get("CodeSigningConfigs"),
    )


def list_event_source_mappings(
    *,
    event_source_arn: str | None = None,
    function_name: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListEventSourceMappingsResult:
    """List event source mappings.

    Args:
        event_source_arn: Event source arn.
        function_name: Function name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    if event_source_arn is not None:
        kwargs["EventSourceArn"] = event_source_arn
    if function_name is not None:
        kwargs["FunctionName"] = function_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_event_source_mappings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list event source mappings") from exc
    return ListEventSourceMappingsResult(
        next_marker=resp.get("NextMarker"),
        event_source_mappings=resp.get("EventSourceMappings"),
    )


def list_function_event_invoke_configs(
    function_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListFunctionEventInvokeConfigsResult:
    """List function event invoke configs.

    Args:
        function_name: Function name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_function_event_invoke_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list function event invoke configs") from exc
    return ListFunctionEventInvokeConfigsResult(
        function_event_invoke_configs=resp.get("FunctionEventInvokeConfigs"),
        next_marker=resp.get("NextMarker"),
    )


def list_function_url_configs(
    function_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListFunctionUrlConfigsResult:
    """List function url configs.

    Args:
        function_name: Function name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_function_url_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list function url configs") from exc
    return ListFunctionUrlConfigsResult(
        function_url_configs=resp.get("FunctionUrlConfigs"),
        next_marker=resp.get("NextMarker"),
    )


def list_functions(
    *,
    master_region: str | None = None,
    function_version: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListFunctionsResult:
    """List functions.

    Args:
        master_region: Master region.
        function_version: Function version.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    if master_region is not None:
        kwargs["MasterRegion"] = master_region
    if function_version is not None:
        kwargs["FunctionVersion"] = function_version
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_functions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list functions") from exc
    return ListFunctionsResult(
        next_marker=resp.get("NextMarker"),
        functions=resp.get("Functions"),
    )


def list_functions_by_code_signing_config(
    code_signing_config_arn: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListFunctionsByCodeSigningConfigResult:
    """List functions by code signing config.

    Args:
        code_signing_config_arn: Code signing config arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_functions_by_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list functions by code signing config") from exc
    return ListFunctionsByCodeSigningConfigResult(
        next_marker=resp.get("NextMarker"),
        function_arns=resp.get("FunctionArns"),
    )


def list_layer_versions(
    layer_name: str,
    *,
    compatible_runtime: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    compatible_architecture: str | None = None,
    region_name: str | None = None,
) -> ListLayerVersionsResult:
    """List layer versions.

    Args:
        layer_name: Layer name.
        compatible_runtime: Compatible runtime.
        marker: Marker.
        max_items: Max items.
        compatible_architecture: Compatible architecture.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    if compatible_runtime is not None:
        kwargs["CompatibleRuntime"] = compatible_runtime
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if compatible_architecture is not None:
        kwargs["CompatibleArchitecture"] = compatible_architecture
    try:
        resp = client.list_layer_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list layer versions") from exc
    return ListLayerVersionsResult(
        next_marker=resp.get("NextMarker"),
        layer_versions=resp.get("LayerVersions"),
    )


def list_layers(
    *,
    compatible_runtime: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    compatible_architecture: str | None = None,
    region_name: str | None = None,
) -> ListLayersResult:
    """List layers.

    Args:
        compatible_runtime: Compatible runtime.
        marker: Marker.
        max_items: Max items.
        compatible_architecture: Compatible architecture.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    if compatible_runtime is not None:
        kwargs["CompatibleRuntime"] = compatible_runtime
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if compatible_architecture is not None:
        kwargs["CompatibleArchitecture"] = compatible_architecture
    try:
        resp = client.list_layers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list layers") from exc
    return ListLayersResult(
        next_marker=resp.get("NextMarker"),
        layers=resp.get("Layers"),
    )


def list_provisioned_concurrency_configs(
    function_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListProvisionedConcurrencyConfigsResult:
    """List provisioned concurrency configs.

    Args:
        function_name: Function name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_provisioned_concurrency_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list provisioned concurrency configs") from exc
    return ListProvisionedConcurrencyConfigsResult(
        provisioned_concurrency_configs=resp.get("ProvisionedConcurrencyConfigs"),
        next_marker=resp.get("NextMarker"),
    )


def list_tags(
    resource: str,
    region_name: str | None = None,
) -> ListTagsResult:
    """List tags.

    Args:
        resource: Resource.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    try:
        resp = client.list_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags") from exc
    return ListTagsResult(
        tags=resp.get("Tags"),
    )


def list_versions_by_function(
    function_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListVersionsByFunctionResult:
    """List versions by function.

    Args:
        function_name: Function name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_versions_by_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list versions by function") from exc
    return ListVersionsByFunctionResult(
        next_marker=resp.get("NextMarker"),
        versions=resp.get("Versions"),
    )


def publish_layer_version(
    layer_name: str,
    content: dict[str, Any],
    *,
    description: str | None = None,
    compatible_runtimes: list[str] | None = None,
    license_info: str | None = None,
    compatible_architectures: list[str] | None = None,
    region_name: str | None = None,
) -> PublishLayerVersionResult:
    """Publish layer version.

    Args:
        layer_name: Layer name.
        content: Content.
        description: Description.
        compatible_runtimes: Compatible runtimes.
        license_info: License info.
        compatible_architectures: Compatible architectures.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["Content"] = content
    if description is not None:
        kwargs["Description"] = description
    if compatible_runtimes is not None:
        kwargs["CompatibleRuntimes"] = compatible_runtimes
    if license_info is not None:
        kwargs["LicenseInfo"] = license_info
    if compatible_architectures is not None:
        kwargs["CompatibleArchitectures"] = compatible_architectures
    try:
        resp = client.publish_layer_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish layer version") from exc
    return PublishLayerVersionResult(
        content=resp.get("Content"),
        layer_arn=resp.get("LayerArn"),
        layer_version_arn=resp.get("LayerVersionArn"),
        description=resp.get("Description"),
        created_date=resp.get("CreatedDate"),
        version=resp.get("Version"),
        compatible_runtimes=resp.get("CompatibleRuntimes"),
        license_info=resp.get("LicenseInfo"),
        compatible_architectures=resp.get("CompatibleArchitectures"),
    )


def publish_version(
    function_name: str,
    *,
    code_sha256: str | None = None,
    description: str | None = None,
    revision_id: str | None = None,
    region_name: str | None = None,
) -> PublishVersionResult:
    """Publish version.

    Args:
        function_name: Function name.
        code_sha256: Code sha256.
        description: Description.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if code_sha256 is not None:
        kwargs["CodeSha256"] = code_sha256
    if description is not None:
        kwargs["Description"] = description
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    try:
        resp = client.publish_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish version") from exc
    return PublishVersionResult(
        function_name=resp.get("FunctionName"),
        function_arn=resp.get("FunctionArn"),
        runtime=resp.get("Runtime"),
        role=resp.get("Role"),
        handler=resp.get("Handler"),
        code_size=resp.get("CodeSize"),
        description=resp.get("Description"),
        timeout=resp.get("Timeout"),
        memory_size=resp.get("MemorySize"),
        last_modified=resp.get("LastModified"),
        code_sha256=resp.get("CodeSha256"),
        version=resp.get("Version"),
        vpc_config=resp.get("VpcConfig"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        environment=resp.get("Environment"),
        kms_key_arn=resp.get("KMSKeyArn"),
        tracing_config=resp.get("TracingConfig"),
        master_arn=resp.get("MasterArn"),
        revision_id=resp.get("RevisionId"),
        layers=resp.get("Layers"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        state_reason_code=resp.get("StateReasonCode"),
        last_update_status=resp.get("LastUpdateStatus"),
        last_update_status_reason=resp.get("LastUpdateStatusReason"),
        last_update_status_reason_code=resp.get("LastUpdateStatusReasonCode"),
        file_system_configs=resp.get("FileSystemConfigs"),
        package_type=resp.get("PackageType"),
        image_config_response=resp.get("ImageConfigResponse"),
        signing_profile_version_arn=resp.get("SigningProfileVersionArn"),
        signing_job_arn=resp.get("SigningJobArn"),
        architectures=resp.get("Architectures"),
        ephemeral_storage=resp.get("EphemeralStorage"),
        snap_start=resp.get("SnapStart"),
        runtime_version_config=resp.get("RuntimeVersionConfig"),
        logging_config=resp.get("LoggingConfig"),
    )


def put_function_code_signing_config(
    code_signing_config_arn: str,
    function_name: str,
    region_name: str | None = None,
) -> PutFunctionCodeSigningConfigResult:
    """Put function code signing config.

    Args:
        code_signing_config_arn: Code signing config arn.
        function_name: Function name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    kwargs["FunctionName"] = function_name
    try:
        resp = client.put_function_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put function code signing config") from exc
    return PutFunctionCodeSigningConfigResult(
        code_signing_config_arn=resp.get("CodeSigningConfigArn"),
        function_name=resp.get("FunctionName"),
    )


def put_function_concurrency(
    function_name: str,
    reserved_concurrent_executions: int,
    region_name: str | None = None,
) -> PutFunctionConcurrencyResult:
    """Put function concurrency.

    Args:
        function_name: Function name.
        reserved_concurrent_executions: Reserved concurrent executions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["ReservedConcurrentExecutions"] = reserved_concurrent_executions
    try:
        resp = client.put_function_concurrency(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put function concurrency") from exc
    return PutFunctionConcurrencyResult(
        reserved_concurrent_executions=resp.get("ReservedConcurrentExecutions"),
    )


def put_function_event_invoke_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    maximum_retry_attempts: int | None = None,
    maximum_event_age_in_seconds: int | None = None,
    destination_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutFunctionEventInvokeConfigResult:
    """Put function event invoke config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        maximum_retry_attempts: Maximum retry attempts.
        maximum_event_age_in_seconds: Maximum event age in seconds.
        destination_config: Destination config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if maximum_retry_attempts is not None:
        kwargs["MaximumRetryAttempts"] = maximum_retry_attempts
    if maximum_event_age_in_seconds is not None:
        kwargs["MaximumEventAgeInSeconds"] = maximum_event_age_in_seconds
    if destination_config is not None:
        kwargs["DestinationConfig"] = destination_config
    try:
        resp = client.put_function_event_invoke_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put function event invoke config") from exc
    return PutFunctionEventInvokeConfigResult(
        last_modified=resp.get("LastModified"),
        function_arn=resp.get("FunctionArn"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        maximum_event_age_in_seconds=resp.get("MaximumEventAgeInSeconds"),
        destination_config=resp.get("DestinationConfig"),
    )


def put_function_recursion_config(
    function_name: str,
    recursive_loop: str,
    region_name: str | None = None,
) -> PutFunctionRecursionConfigResult:
    """Put function recursion config.

    Args:
        function_name: Function name.
        recursive_loop: Recursive loop.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["RecursiveLoop"] = recursive_loop
    try:
        resp = client.put_function_recursion_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put function recursion config") from exc
    return PutFunctionRecursionConfigResult(
        recursive_loop=resp.get("RecursiveLoop"),
    )


def put_provisioned_concurrency_config(
    function_name: str,
    qualifier: str,
    provisioned_concurrent_executions: int,
    region_name: str | None = None,
) -> PutProvisionedConcurrencyConfigResult:
    """Put provisioned concurrency config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        provisioned_concurrent_executions: Provisioned concurrent executions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Qualifier"] = qualifier
    kwargs["ProvisionedConcurrentExecutions"] = provisioned_concurrent_executions
    try:
        resp = client.put_provisioned_concurrency_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put provisioned concurrency config") from exc
    return PutProvisionedConcurrencyConfigResult(
        requested_provisioned_concurrent_executions=resp.get(
            "RequestedProvisionedConcurrentExecutions"
        ),
        available_provisioned_concurrent_executions=resp.get(
            "AvailableProvisionedConcurrentExecutions"
        ),
        allocated_provisioned_concurrent_executions=resp.get(
            "AllocatedProvisionedConcurrentExecutions"
        ),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        last_modified=resp.get("LastModified"),
    )


def put_runtime_management_config(
    function_name: str,
    update_runtime_on: str,
    *,
    qualifier: str | None = None,
    runtime_version_arn: str | None = None,
    region_name: str | None = None,
) -> PutRuntimeManagementConfigResult:
    """Put runtime management config.

    Args:
        function_name: Function name.
        update_runtime_on: Update runtime on.
        qualifier: Qualifier.
        runtime_version_arn: Runtime version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["UpdateRuntimeOn"] = update_runtime_on
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if runtime_version_arn is not None:
        kwargs["RuntimeVersionArn"] = runtime_version_arn
    try:
        resp = client.put_runtime_management_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put runtime management config") from exc
    return PutRuntimeManagementConfigResult(
        update_runtime_on=resp.get("UpdateRuntimeOn"),
        function_arn=resp.get("FunctionArn"),
        runtime_version_arn=resp.get("RuntimeVersionArn"),
    )


def remove_layer_version_permission(
    layer_name: str,
    version_number: int,
    statement_id: str,
    *,
    revision_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove layer version permission.

    Args:
        layer_name: Layer name.
        version_number: Version number.
        statement_id: Statement id.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LayerName"] = layer_name
    kwargs["VersionNumber"] = version_number
    kwargs["StatementId"] = statement_id
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    try:
        client.remove_layer_version_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove layer version permission") from exc
    return None


def remove_permission(
    function_name: str,
    statement_id: str,
    *,
    qualifier: str | None = None,
    revision_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove permission.

    Args:
        function_name: Function name.
        statement_id: Statement id.
        qualifier: Qualifier.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["StatementId"] = statement_id
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    try:
        client.remove_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove permission") from exc
    return None


def tag_resource(
    resource: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource: Resource.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource: Resource.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_alias(
    function_name: str,
    name: str,
    *,
    function_version: str | None = None,
    description: str | None = None,
    routing_config: dict[str, Any] | None = None,
    revision_id: str | None = None,
    region_name: str | None = None,
) -> UpdateAliasResult:
    """Update alias.

    Args:
        function_name: Function name.
        name: Name.
        function_version: Function version.
        description: Description.
        routing_config: Routing config.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    kwargs["Name"] = name
    if function_version is not None:
        kwargs["FunctionVersion"] = function_version
    if description is not None:
        kwargs["Description"] = description
    if routing_config is not None:
        kwargs["RoutingConfig"] = routing_config
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    try:
        resp = client.update_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update alias") from exc
    return UpdateAliasResult(
        alias_arn=resp.get("AliasArn"),
        name=resp.get("Name"),
        function_version=resp.get("FunctionVersion"),
        description=resp.get("Description"),
        routing_config=resp.get("RoutingConfig"),
        revision_id=resp.get("RevisionId"),
    )


def update_code_signing_config(
    code_signing_config_arn: str,
    *,
    description: str | None = None,
    allowed_publishers: dict[str, Any] | None = None,
    code_signing_policies: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateCodeSigningConfigResult:
    """Update code signing config.

    Args:
        code_signing_config_arn: Code signing config arn.
        description: Description.
        allowed_publishers: Allowed publishers.
        code_signing_policies: Code signing policies.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CodeSigningConfigArn"] = code_signing_config_arn
    if description is not None:
        kwargs["Description"] = description
    if allowed_publishers is not None:
        kwargs["AllowedPublishers"] = allowed_publishers
    if code_signing_policies is not None:
        kwargs["CodeSigningPolicies"] = code_signing_policies
    try:
        resp = client.update_code_signing_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update code signing config") from exc
    return UpdateCodeSigningConfigResult(
        code_signing_config=resp.get("CodeSigningConfig"),
    )


def update_event_source_mapping(
    uuid: str,
    *,
    function_name: str | None = None,
    enabled: bool | None = None,
    batch_size: int | None = None,
    filter_criteria: dict[str, Any] | None = None,
    maximum_batching_window_in_seconds: int | None = None,
    destination_config: dict[str, Any] | None = None,
    maximum_record_age_in_seconds: int | None = None,
    bisect_batch_on_function_error: bool | None = None,
    maximum_retry_attempts: int | None = None,
    parallelization_factor: int | None = None,
    source_access_configurations: list[dict[str, Any]] | None = None,
    tumbling_window_in_seconds: int | None = None,
    function_response_types: list[str] | None = None,
    scaling_config: dict[str, Any] | None = None,
    amazon_managed_kafka_event_source_config: dict[str, Any] | None = None,
    self_managed_kafka_event_source_config: dict[str, Any] | None = None,
    document_db_event_source_config: dict[str, Any] | None = None,
    kms_key_arn: str | None = None,
    metrics_config: dict[str, Any] | None = None,
    provisioned_poller_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateEventSourceMappingResult:
    """Update event source mapping.

    Args:
        uuid: Uuid.
        function_name: Function name.
        enabled: Enabled.
        batch_size: Batch size.
        filter_criteria: Filter criteria.
        maximum_batching_window_in_seconds: Maximum batching window in seconds.
        destination_config: Destination config.
        maximum_record_age_in_seconds: Maximum record age in seconds.
        bisect_batch_on_function_error: Bisect batch on function error.
        maximum_retry_attempts: Maximum retry attempts.
        parallelization_factor: Parallelization factor.
        source_access_configurations: Source access configurations.
        tumbling_window_in_seconds: Tumbling window in seconds.
        function_response_types: Function response types.
        scaling_config: Scaling config.
        amazon_managed_kafka_event_source_config: Amazon managed kafka event source config.
        self_managed_kafka_event_source_config: Self managed kafka event source config.
        document_db_event_source_config: Document db event source config.
        kms_key_arn: Kms key arn.
        metrics_config: Metrics config.
        provisioned_poller_config: Provisioned poller config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UUID"] = uuid
    if function_name is not None:
        kwargs["FunctionName"] = function_name
    if enabled is not None:
        kwargs["Enabled"] = enabled
    if batch_size is not None:
        kwargs["BatchSize"] = batch_size
    if filter_criteria is not None:
        kwargs["FilterCriteria"] = filter_criteria
    if maximum_batching_window_in_seconds is not None:
        kwargs["MaximumBatchingWindowInSeconds"] = maximum_batching_window_in_seconds
    if destination_config is not None:
        kwargs["DestinationConfig"] = destination_config
    if maximum_record_age_in_seconds is not None:
        kwargs["MaximumRecordAgeInSeconds"] = maximum_record_age_in_seconds
    if bisect_batch_on_function_error is not None:
        kwargs["BisectBatchOnFunctionError"] = bisect_batch_on_function_error
    if maximum_retry_attempts is not None:
        kwargs["MaximumRetryAttempts"] = maximum_retry_attempts
    if parallelization_factor is not None:
        kwargs["ParallelizationFactor"] = parallelization_factor
    if source_access_configurations is not None:
        kwargs["SourceAccessConfigurations"] = source_access_configurations
    if tumbling_window_in_seconds is not None:
        kwargs["TumblingWindowInSeconds"] = tumbling_window_in_seconds
    if function_response_types is not None:
        kwargs["FunctionResponseTypes"] = function_response_types
    if scaling_config is not None:
        kwargs["ScalingConfig"] = scaling_config
    if amazon_managed_kafka_event_source_config is not None:
        kwargs["AmazonManagedKafkaEventSourceConfig"] = amazon_managed_kafka_event_source_config
    if self_managed_kafka_event_source_config is not None:
        kwargs["SelfManagedKafkaEventSourceConfig"] = self_managed_kafka_event_source_config
    if document_db_event_source_config is not None:
        kwargs["DocumentDBEventSourceConfig"] = document_db_event_source_config
    if kms_key_arn is not None:
        kwargs["KMSKeyArn"] = kms_key_arn
    if metrics_config is not None:
        kwargs["MetricsConfig"] = metrics_config
    if provisioned_poller_config is not None:
        kwargs["ProvisionedPollerConfig"] = provisioned_poller_config
    try:
        resp = client.update_event_source_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update event source mapping") from exc
    return UpdateEventSourceMappingResult(
        uuid=resp.get("UUID"),
        starting_position=resp.get("StartingPosition"),
        starting_position_timestamp=resp.get("StartingPositionTimestamp"),
        batch_size=resp.get("BatchSize"),
        maximum_batching_window_in_seconds=resp.get("MaximumBatchingWindowInSeconds"),
        parallelization_factor=resp.get("ParallelizationFactor"),
        event_source_arn=resp.get("EventSourceArn"),
        filter_criteria=resp.get("FilterCriteria"),
        function_arn=resp.get("FunctionArn"),
        last_modified=resp.get("LastModified"),
        last_processing_result=resp.get("LastProcessingResult"),
        state=resp.get("State"),
        state_transition_reason=resp.get("StateTransitionReason"),
        destination_config=resp.get("DestinationConfig"),
        topics=resp.get("Topics"),
        queues=resp.get("Queues"),
        source_access_configurations=resp.get("SourceAccessConfigurations"),
        self_managed_event_source=resp.get("SelfManagedEventSource"),
        maximum_record_age_in_seconds=resp.get("MaximumRecordAgeInSeconds"),
        bisect_batch_on_function_error=resp.get("BisectBatchOnFunctionError"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        tumbling_window_in_seconds=resp.get("TumblingWindowInSeconds"),
        function_response_types=resp.get("FunctionResponseTypes"),
        amazon_managed_kafka_event_source_config=resp.get("AmazonManagedKafkaEventSourceConfig"),
        self_managed_kafka_event_source_config=resp.get("SelfManagedKafkaEventSourceConfig"),
        scaling_config=resp.get("ScalingConfig"),
        document_db_event_source_config=resp.get("DocumentDBEventSourceConfig"),
        kms_key_arn=resp.get("KMSKeyArn"),
        filter_criteria_error=resp.get("FilterCriteriaError"),
        event_source_mapping_arn=resp.get("EventSourceMappingArn"),
        metrics_config=resp.get("MetricsConfig"),
        provisioned_poller_config=resp.get("ProvisionedPollerConfig"),
    )


def update_function_code(
    function_name: str,
    *,
    zip_file: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    s3_object_version: str | None = None,
    image_uri: str | None = None,
    publish: bool | None = None,
    revision_id: str | None = None,
    architectures: list[str] | None = None,
    source_kms_key_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateFunctionCodeResult:
    """Update function code.

    Args:
        function_name: Function name.
        zip_file: Zip file.
        s3_bucket: S3 bucket.
        s3_key: S3 key.
        s3_object_version: S3 object version.
        image_uri: Image uri.
        publish: Publish.
        revision_id: Revision id.
        architectures: Architectures.
        source_kms_key_arn: Source kms key arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if zip_file is not None:
        kwargs["ZipFile"] = zip_file
    if s3_bucket is not None:
        kwargs["S3Bucket"] = s3_bucket
    if s3_key is not None:
        kwargs["S3Key"] = s3_key
    if s3_object_version is not None:
        kwargs["S3ObjectVersion"] = s3_object_version
    if image_uri is not None:
        kwargs["ImageUri"] = image_uri
    if publish is not None:
        kwargs["Publish"] = publish
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    if architectures is not None:
        kwargs["Architectures"] = architectures
    if source_kms_key_arn is not None:
        kwargs["SourceKMSKeyArn"] = source_kms_key_arn
    try:
        resp = client.update_function_code(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update function code") from exc
    return UpdateFunctionCodeResult(
        function_name=resp.get("FunctionName"),
        function_arn=resp.get("FunctionArn"),
        runtime=resp.get("Runtime"),
        role=resp.get("Role"),
        handler=resp.get("Handler"),
        code_size=resp.get("CodeSize"),
        description=resp.get("Description"),
        timeout=resp.get("Timeout"),
        memory_size=resp.get("MemorySize"),
        last_modified=resp.get("LastModified"),
        code_sha256=resp.get("CodeSha256"),
        version=resp.get("Version"),
        vpc_config=resp.get("VpcConfig"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        environment=resp.get("Environment"),
        kms_key_arn=resp.get("KMSKeyArn"),
        tracing_config=resp.get("TracingConfig"),
        master_arn=resp.get("MasterArn"),
        revision_id=resp.get("RevisionId"),
        layers=resp.get("Layers"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        state_reason_code=resp.get("StateReasonCode"),
        last_update_status=resp.get("LastUpdateStatus"),
        last_update_status_reason=resp.get("LastUpdateStatusReason"),
        last_update_status_reason_code=resp.get("LastUpdateStatusReasonCode"),
        file_system_configs=resp.get("FileSystemConfigs"),
        package_type=resp.get("PackageType"),
        image_config_response=resp.get("ImageConfigResponse"),
        signing_profile_version_arn=resp.get("SigningProfileVersionArn"),
        signing_job_arn=resp.get("SigningJobArn"),
        architectures=resp.get("Architectures"),
        ephemeral_storage=resp.get("EphemeralStorage"),
        snap_start=resp.get("SnapStart"),
        runtime_version_config=resp.get("RuntimeVersionConfig"),
        logging_config=resp.get("LoggingConfig"),
    )


def update_function_configuration(
    function_name: str,
    *,
    role: str | None = None,
    handler: str | None = None,
    description: str | None = None,
    timeout: int | None = None,
    memory_size: int | None = None,
    vpc_config: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    runtime: str | None = None,
    dead_letter_config: dict[str, Any] | None = None,
    kms_key_arn: str | None = None,
    tracing_config: dict[str, Any] | None = None,
    revision_id: str | None = None,
    layers: list[str] | None = None,
    file_system_configs: list[dict[str, Any]] | None = None,
    image_config: dict[str, Any] | None = None,
    ephemeral_storage: dict[str, Any] | None = None,
    snap_start: dict[str, Any] | None = None,
    logging_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFunctionConfigurationResult:
    """Update function configuration.

    Args:
        function_name: Function name.
        role: Role.
        handler: Handler.
        description: Description.
        timeout: Timeout.
        memory_size: Memory size.
        vpc_config: Vpc config.
        environment: Environment.
        runtime: Runtime.
        dead_letter_config: Dead letter config.
        kms_key_arn: Kms key arn.
        tracing_config: Tracing config.
        revision_id: Revision id.
        layers: Layers.
        file_system_configs: File system configs.
        image_config: Image config.
        ephemeral_storage: Ephemeral storage.
        snap_start: Snap start.
        logging_config: Logging config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if role is not None:
        kwargs["Role"] = role
    if handler is not None:
        kwargs["Handler"] = handler
    if description is not None:
        kwargs["Description"] = description
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if memory_size is not None:
        kwargs["MemorySize"] = memory_size
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if environment is not None:
        kwargs["Environment"] = environment
    if runtime is not None:
        kwargs["Runtime"] = runtime
    if dead_letter_config is not None:
        kwargs["DeadLetterConfig"] = dead_letter_config
    if kms_key_arn is not None:
        kwargs["KMSKeyArn"] = kms_key_arn
    if tracing_config is not None:
        kwargs["TracingConfig"] = tracing_config
    if revision_id is not None:
        kwargs["RevisionId"] = revision_id
    if layers is not None:
        kwargs["Layers"] = layers
    if file_system_configs is not None:
        kwargs["FileSystemConfigs"] = file_system_configs
    if image_config is not None:
        kwargs["ImageConfig"] = image_config
    if ephemeral_storage is not None:
        kwargs["EphemeralStorage"] = ephemeral_storage
    if snap_start is not None:
        kwargs["SnapStart"] = snap_start
    if logging_config is not None:
        kwargs["LoggingConfig"] = logging_config
    try:
        resp = client.update_function_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update function configuration") from exc
    return UpdateFunctionConfigurationResult(
        function_name=resp.get("FunctionName"),
        function_arn=resp.get("FunctionArn"),
        runtime=resp.get("Runtime"),
        role=resp.get("Role"),
        handler=resp.get("Handler"),
        code_size=resp.get("CodeSize"),
        description=resp.get("Description"),
        timeout=resp.get("Timeout"),
        memory_size=resp.get("MemorySize"),
        last_modified=resp.get("LastModified"),
        code_sha256=resp.get("CodeSha256"),
        version=resp.get("Version"),
        vpc_config=resp.get("VpcConfig"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        environment=resp.get("Environment"),
        kms_key_arn=resp.get("KMSKeyArn"),
        tracing_config=resp.get("TracingConfig"),
        master_arn=resp.get("MasterArn"),
        revision_id=resp.get("RevisionId"),
        layers=resp.get("Layers"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        state_reason_code=resp.get("StateReasonCode"),
        last_update_status=resp.get("LastUpdateStatus"),
        last_update_status_reason=resp.get("LastUpdateStatusReason"),
        last_update_status_reason_code=resp.get("LastUpdateStatusReasonCode"),
        file_system_configs=resp.get("FileSystemConfigs"),
        package_type=resp.get("PackageType"),
        image_config_response=resp.get("ImageConfigResponse"),
        signing_profile_version_arn=resp.get("SigningProfileVersionArn"),
        signing_job_arn=resp.get("SigningJobArn"),
        architectures=resp.get("Architectures"),
        ephemeral_storage=resp.get("EphemeralStorage"),
        snap_start=resp.get("SnapStart"),
        runtime_version_config=resp.get("RuntimeVersionConfig"),
        logging_config=resp.get("LoggingConfig"),
    )


def update_function_event_invoke_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    maximum_retry_attempts: int | None = None,
    maximum_event_age_in_seconds: int | None = None,
    destination_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFunctionEventInvokeConfigResult:
    """Update function event invoke config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        maximum_retry_attempts: Maximum retry attempts.
        maximum_event_age_in_seconds: Maximum event age in seconds.
        destination_config: Destination config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if maximum_retry_attempts is not None:
        kwargs["MaximumRetryAttempts"] = maximum_retry_attempts
    if maximum_event_age_in_seconds is not None:
        kwargs["MaximumEventAgeInSeconds"] = maximum_event_age_in_seconds
    if destination_config is not None:
        kwargs["DestinationConfig"] = destination_config
    try:
        resp = client.update_function_event_invoke_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update function event invoke config") from exc
    return UpdateFunctionEventInvokeConfigResult(
        last_modified=resp.get("LastModified"),
        function_arn=resp.get("FunctionArn"),
        maximum_retry_attempts=resp.get("MaximumRetryAttempts"),
        maximum_event_age_in_seconds=resp.get("MaximumEventAgeInSeconds"),
        destination_config=resp.get("DestinationConfig"),
    )


def update_function_url_config(
    function_name: str,
    *,
    qualifier: str | None = None,
    auth_type: str | None = None,
    cors: dict[str, Any] | None = None,
    invoke_mode: str | None = None,
    region_name: str | None = None,
) -> UpdateFunctionUrlConfigResult:
    """Update function url config.

    Args:
        function_name: Function name.
        qualifier: Qualifier.
        auth_type: Auth type.
        cors: Cors.
        invoke_mode: Invoke mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("lambda", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FunctionName"] = function_name
    if qualifier is not None:
        kwargs["Qualifier"] = qualifier
    if auth_type is not None:
        kwargs["AuthType"] = auth_type
    if cors is not None:
        kwargs["Cors"] = cors
    if invoke_mode is not None:
        kwargs["InvokeMode"] = invoke_mode
    try:
        resp = client.update_function_url_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update function url config") from exc
    return UpdateFunctionUrlConfigResult(
        function_url=resp.get("FunctionUrl"),
        function_arn=resp.get("FunctionArn"),
        auth_type=resp.get("AuthType"),
        cors=resp.get("Cors"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        invoke_mode=resp.get("InvokeMode"),
    )
