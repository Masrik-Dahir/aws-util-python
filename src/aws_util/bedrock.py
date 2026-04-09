from __future__ import annotations

import json
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ApplyGuardrailResult",
    "BatchDeleteEvaluationJobResult",
    "BedrockModel",
    "CancelAutomatedReasoningPolicyBuildWorkflowResult",
    "ConverseResult",
    "ConverseStreamResult",
    "CountTokensResult",
    "CreateAutomatedReasoningPolicyResult",
    "CreateAutomatedReasoningPolicyTestCaseResult",
    "CreateAutomatedReasoningPolicyVersionResult",
    "CreateCustomModelDeploymentResult",
    "CreateCustomModelResult",
    "CreateEvaluationJobResult",
    "CreateFoundationModelAgreementResult",
    "CreateGuardrailResult",
    "CreateGuardrailVersionResult",
    "CreateInferenceProfileResult",
    "CreateMarketplaceModelEndpointResult",
    "CreateModelCopyJobResult",
    "CreateModelCustomizationJobResult",
    "CreateModelImportJobResult",
    "CreateModelInvocationJobResult",
    "CreatePromptRouterResult",
    "CreateProvisionedModelThroughputResult",
    "DeleteAutomatedReasoningPolicyBuildWorkflowResult",
    "DeleteAutomatedReasoningPolicyResult",
    "DeleteAutomatedReasoningPolicyTestCaseResult",
    "DeleteCustomModelDeploymentResult",
    "DeleteCustomModelResult",
    "DeleteFoundationModelAgreementResult",
    "DeleteGuardrailResult",
    "DeleteImportedModelResult",
    "DeleteInferenceProfileResult",
    "DeleteMarketplaceModelEndpointResult",
    "DeleteModelInvocationLoggingConfigurationResult",
    "DeletePromptRouterResult",
    "DeleteProvisionedModelThroughputResult",
    "DeregisterMarketplaceModelEndpointResult",
    "ExportAutomatedReasoningPolicyVersionResult",
    "GetAsyncInvokeResult",
    "GetAutomatedReasoningPolicyAnnotationsResult",
    "GetAutomatedReasoningPolicyBuildWorkflowResult",
    "GetAutomatedReasoningPolicyBuildWorkflowResultAssetsResult",
    "GetAutomatedReasoningPolicyNextScenarioResult",
    "GetAutomatedReasoningPolicyResult",
    "GetAutomatedReasoningPolicyTestCaseResult",
    "GetAutomatedReasoningPolicyTestResultResult",
    "GetCustomModelDeploymentResult",
    "GetCustomModelResult",
    "GetEvaluationJobResult",
    "GetFoundationModelAvailabilityResult",
    "GetFoundationModelResult",
    "GetGuardrailResult",
    "GetImportedModelResult",
    "GetInferenceProfileResult",
    "GetMarketplaceModelEndpointResult",
    "GetModelCopyJobResult",
    "GetModelCustomizationJobResult",
    "GetModelImportJobResult",
    "GetModelInvocationJobResult",
    "GetModelInvocationLoggingConfigurationResult",
    "GetPromptRouterResult",
    "GetProvisionedModelThroughputResult",
    "GetUseCaseForModelAccessResult",
    "InvokeModelResult",
    "InvokeModelWithResponseStreamResult",
    "ListAsyncInvokesResult",
    "ListAutomatedReasoningPoliciesResult",
    "ListAutomatedReasoningPolicyBuildWorkflowsResult",
    "ListAutomatedReasoningPolicyTestCasesResult",
    "ListAutomatedReasoningPolicyTestResultsResult",
    "ListCustomModelDeploymentsResult",
    "ListCustomModelsResult",
    "ListEvaluationJobsResult",
    "ListFoundationModelAgreementOffersResult",
    "ListGuardrailsResult",
    "ListImportedModelsResult",
    "ListInferenceProfilesResult",
    "ListMarketplaceModelEndpointsResult",
    "ListModelCopyJobsResult",
    "ListModelCustomizationJobsResult",
    "ListModelImportJobsResult",
    "ListModelInvocationJobsResult",
    "ListPromptRoutersResult",
    "ListProvisionedModelThroughputsResult",
    "ListTagsForResourceResult",
    "PutModelInvocationLoggingConfigurationResult",
    "PutUseCaseForModelAccessResult",
    "RegisterMarketplaceModelEndpointResult",
    "StartAsyncInvokeResult",
    "StartAutomatedReasoningPolicyBuildWorkflowResult",
    "StartAutomatedReasoningPolicyTestWorkflowResult",
    "StopEvaluationJobResult",
    "StopModelCustomizationJobResult",
    "StopModelInvocationJobResult",
    "TagResourceResult",
    "UntagResourceResult",
    "UpdateAutomatedReasoningPolicyAnnotationsResult",
    "UpdateAutomatedReasoningPolicyResult",
    "UpdateAutomatedReasoningPolicyTestCaseResult",
    "UpdateGuardrailResult",
    "UpdateMarketplaceModelEndpointResult",
    "UpdateProvisionedModelThroughputResult",
    "apply_guardrail",
    "batch_delete_evaluation_job",
    "cancel_automated_reasoning_policy_build_workflow",
    "chat",
    "converse",
    "converse_stream",
    "count_tokens",
    "create_automated_reasoning_policy",
    "create_automated_reasoning_policy_test_case",
    "create_automated_reasoning_policy_version",
    "create_custom_model",
    "create_custom_model_deployment",
    "create_evaluation_job",
    "create_foundation_model_agreement",
    "create_guardrail",
    "create_guardrail_version",
    "create_inference_profile",
    "create_marketplace_model_endpoint",
    "create_model_copy_job",
    "create_model_customization_job",
    "create_model_import_job",
    "create_model_invocation_job",
    "create_prompt_router",
    "create_provisioned_model_throughput",
    "delete_automated_reasoning_policy",
    "delete_automated_reasoning_policy_build_workflow",
    "delete_automated_reasoning_policy_test_case",
    "delete_custom_model",
    "delete_custom_model_deployment",
    "delete_foundation_model_agreement",
    "delete_guardrail",
    "delete_imported_model",
    "delete_inference_profile",
    "delete_marketplace_model_endpoint",
    "delete_model_invocation_logging_configuration",
    "delete_prompt_router",
    "delete_provisioned_model_throughput",
    "deregister_marketplace_model_endpoint",
    "embed_text",
    "export_automated_reasoning_policy_version",
    "get_async_invoke",
    "get_automated_reasoning_policy",
    "get_automated_reasoning_policy_annotations",
    "get_automated_reasoning_policy_build_workflow",
    "get_automated_reasoning_policy_build_workflow_result_assets",
    "get_automated_reasoning_policy_next_scenario",
    "get_automated_reasoning_policy_test_case",
    "get_automated_reasoning_policy_test_result",
    "get_custom_model",
    "get_custom_model_deployment",
    "get_evaluation_job",
    "get_foundation_model",
    "get_foundation_model_availability",
    "get_guardrail",
    "get_imported_model",
    "get_inference_profile",
    "get_marketplace_model_endpoint",
    "get_model_copy_job",
    "get_model_customization_job",
    "get_model_import_job",
    "get_model_invocation_job",
    "get_model_invocation_logging_configuration",
    "get_prompt_router",
    "get_provisioned_model_throughput",
    "get_use_case_for_model_access",
    "invoke_claude",
    "invoke_model",
    "invoke_model_with_response_stream",
    "invoke_titan_text",
    "list_async_invokes",
    "list_automated_reasoning_policies",
    "list_automated_reasoning_policy_build_workflows",
    "list_automated_reasoning_policy_test_cases",
    "list_automated_reasoning_policy_test_results",
    "list_custom_model_deployments",
    "list_custom_models",
    "list_evaluation_jobs",
    "list_foundation_model_agreement_offers",
    "list_foundation_models",
    "list_guardrails",
    "list_imported_models",
    "list_inference_profiles",
    "list_marketplace_model_endpoints",
    "list_model_copy_jobs",
    "list_model_customization_jobs",
    "list_model_import_jobs",
    "list_model_invocation_jobs",
    "list_prompt_routers",
    "list_provisioned_model_throughputs",
    "list_tags_for_resource",
    "put_model_invocation_logging_configuration",
    "put_use_case_for_model_access",
    "register_marketplace_model_endpoint",
    "start_async_invoke",
    "start_automated_reasoning_policy_build_workflow",
    "start_automated_reasoning_policy_test_workflow",
    "stop_evaluation_job",
    "stop_model_customization_job",
    "stop_model_invocation_job",
    "stream_invoke_claude",
    "tag_resource",
    "untag_resource",
    "update_automated_reasoning_policy",
    "update_automated_reasoning_policy_annotations",
    "update_automated_reasoning_policy_test_case",
    "update_guardrail",
    "update_marketplace_model_endpoint",
    "update_provisioned_model_throughput",
]
# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class BedrockModel(BaseModel):
    """A foundation model available in Amazon Bedrock."""

    model_config = ConfigDict(frozen=True)

    model_id: str
    model_name: str
    provider_name: str
    input_modalities: list[str] = []
    output_modalities: list[str] = []
    response_streaming_supported: bool = False


class InvokeModelResult(BaseModel):
    """The response from a Bedrock model invocation."""

    model_config = ConfigDict(frozen=True)

    model_id: str
    body: dict | str
    content_type: str = "application/json"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def invoke_model(
    model_id: str,
    body: dict[str, Any],
    content_type: str = "application/json",
    accept: str = "application/json",
    region_name: str | None = None,
) -> InvokeModelResult:
    """Invoke any Amazon Bedrock foundation model.

    The *body* format depends on the model provider — see the Bedrock API
    documentation for each model's request schema.

    Args:
        model_id: Bedrock model ID, e.g.
            ``"anthropic.claude-3-5-sonnet-20241022-v2:0"``.
        body: Request body as a dict (serialised to JSON automatically).
        content_type: Request content type (default ``"application/json"``).
        accept: Response content type (default ``"application/json"``).
        region_name: AWS region override.

    Returns:
        An :class:`InvokeModelResult` with the parsed response body.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = get_client("bedrock-runtime", region_name)
    try:
        resp = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType=content_type,
            accept=accept,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to invoke Bedrock model {model_id!r}") from exc

    raw_body = resp["body"].read()
    try:
        parsed_body: dict | str = json.loads(raw_body)
    except json.JSONDecodeError:
        parsed_body = raw_body.decode("utf-8")

    return InvokeModelResult(
        model_id=model_id,
        body=parsed_body,
        content_type=resp.get("contentType", content_type),
    )


def invoke_claude(
    prompt: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    system: str | None = None,
    region_name: str | None = None,
) -> str:
    """Invoke an Anthropic Claude model via Bedrock and return the text response.

    Uses the Claude Messages API format.

    Args:
        prompt: User message content.
        model_id: Claude model ID (defaults to Claude 3.5 Sonnet v2).
        max_tokens: Maximum tokens in the response (default ``1024``).
        temperature: Sampling temperature 0–1 (default ``0.7``).
        system: Optional system prompt.
        region_name: AWS region override.

    Returns:
        The assistant's text response as a string.

    Raises:
        RuntimeError: If the invocation fails.
    """
    body: dict[str, Any] = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system

    result = invoke_model(model_id, body, region_name=region_name)
    response_body = result.body
    if isinstance(response_body, dict):
        content = response_body.get("content", [])
        if content and isinstance(content, list):
            return content[0].get("text", "")
    return str(response_body)


def invoke_titan_text(
    prompt: str,
    model_id: str = "amazon.titan-text-express-v1",
    max_token_count: int = 512,
    temperature: float = 0.7,
    region_name: str | None = None,
) -> str:
    """Invoke an Amazon Titan text model via Bedrock.

    Args:
        prompt: Input text prompt.
        model_id: Titan model ID (defaults to Titan Text Express).
        max_token_count: Maximum tokens in the response.
        temperature: Sampling temperature 0–1.
        region_name: AWS region override.

    Returns:
        The generated text as a string.

    Raises:
        RuntimeError: If the invocation fails.
    """
    body: dict[str, Any] = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_token_count,
            "temperature": temperature,
        },
    }
    result = invoke_model(model_id, body, region_name=region_name)
    response_body = result.body
    if isinstance(response_body, dict):
        results = response_body.get("results", [])
        if results:
            return results[0].get("outputText", "")
    return str(response_body)


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def chat(
    messages: list[dict[str, str]],
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    system: str | None = None,
    region_name: str | None = None,
) -> str:
    """Send a multi-turn conversation to a Claude model and return the reply.

    Each message dict must have ``"role"`` (``"user"`` or ``"assistant"``) and
    ``"content"`` keys.

    Args:
        messages: Conversation history in Claude Messages API format.
        model_id: Claude model ID.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature 0–1.
        system: Optional system prompt prepended to the conversation.
        region_name: AWS region override.

    Returns:
        The assistant's text reply as a string.

    Raises:
        RuntimeError: If the invocation fails.
    """
    body: dict[str, Any] = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    if system:
        body["system"] = system

    result = invoke_model(model_id, body, region_name=region_name)
    response_body = result.body
    if isinstance(response_body, dict):
        content = response_body.get("content", [])
        if content and isinstance(content, list):
            return content[0].get("text", "")
    return str(response_body)


def embed_text(
    text: str,
    model_id: str = "amazon.titan-embed-text-v1",
    region_name: str | None = None,
) -> list[float]:
    """Generate a text embedding vector using an Amazon Titan Embeddings model.

    Args:
        text: Input text to embed (max ~8,192 tokens for Titan).
        model_id: Titan Embeddings model ID
            (default ``"amazon.titan-embed-text-v1"``).
        region_name: AWS region override.

    Returns:
        A list of floats representing the embedding vector.

    Raises:
        RuntimeError: If the invocation fails.
    """
    result = invoke_model(model_id, {"inputText": text}, region_name=region_name)
    response_body = result.body
    if isinstance(response_body, dict):
        return response_body.get("embedding", [])
    return []


def stream_invoke_claude(
    prompt: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    system: str | None = None,
    region_name: str | None = None,
):
    """Stream a Claude response token-by-token using Bedrock's response streaming.

    Yields text chunks as they arrive from the model, enabling real-time
    display of long responses without waiting for the full generation.

    Args:
        prompt: User message content.
        model_id: Claude model ID.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature 0–1.
        system: Optional system prompt.
        region_name: AWS region override.

    Yields:
        Text chunks (strings) as they stream from the model.

    Raises:
        RuntimeError: If the stream invocation fails.
    """
    client = get_client("bedrock-runtime", region_name)
    body: dict[str, Any] = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system
    try:
        resp = client.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to stream Bedrock model {model_id!r}") from exc

    for event in resp.get("body", []):
        chunk = event.get("chunk")
        if chunk:
            try:
                data = json.loads(chunk["bytes"])
                if data.get("type") == "content_block_delta":
                    delta = data.get("delta", {})
                    if delta.get("type") == "text_delta":
                        yield delta.get("text", "")
            except (json.JSONDecodeError, KeyError):
                continue


def list_foundation_models(
    provider_name: str | None = None,
    region_name: str | None = None,
) -> list[BedrockModel]:
    """List foundation models available in Amazon Bedrock.

    Args:
        provider_name: Optional filter by provider, e.g. ``"Anthropic"``,
            ``"Amazon"``, ``"Meta"``, ``"Mistral AI"``.
        region_name: AWS region override.

    Returns:
        A list of :class:`BedrockModel` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if provider_name:
        kwargs["byProvider"] = provider_name
    try:
        resp = client.list_foundation_models(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_foundation_models failed") from exc
    return [
        BedrockModel(
            model_id=m["modelId"],
            model_name=m.get("modelName", ""),
            provider_name=m.get("providerName", ""),
            input_modalities=m.get("inputModalities", []),
            output_modalities=m.get("outputModalities", []),
            response_streaming_supported=m.get("responseStreamingSupported", False),
        )
        for m in resp.get("modelSummaries", [])
    ]


class ApplyGuardrailResult(BaseModel):
    """Result of apply_guardrail."""

    model_config = ConfigDict(frozen=True)

    usage: dict[str, Any] | None = None
    action: str | None = None
    action_reason: str | None = None
    outputs: list[dict[str, Any]] | None = None
    assessments: list[dict[str, Any]] | None = None
    guardrail_coverage: dict[str, Any] | None = None


class ConverseResult(BaseModel):
    """Result of converse."""

    model_config = ConfigDict(frozen=True)

    output: dict[str, Any] | None = None
    stop_reason: str | None = None
    usage: dict[str, Any] | None = None
    metrics: dict[str, Any] | None = None
    additional_model_response_fields: dict[str, Any] | None = None
    trace: dict[str, Any] | None = None
    performance_config: dict[str, Any] | None = None


class ConverseStreamResult(BaseModel):
    """Result of converse_stream."""

    model_config = ConfigDict(frozen=True)

    stream: dict[str, Any] | None = None


class CountTokensResult(BaseModel):
    """Result of count_tokens."""

    model_config = ConfigDict(frozen=True)

    input_tokens: int | None = None


class GetAsyncInvokeResult(BaseModel):
    """Result of get_async_invoke."""

    model_config = ConfigDict(frozen=True)

    invocation_arn: str | None = None
    model_arn: str | None = None
    client_request_token: str | None = None
    status: str | None = None
    failure_message: str | None = None
    submit_time: str | None = None
    last_modified_time: str | None = None
    end_time: str | None = None
    output_data_config: dict[str, Any] | None = None


class InvokeModelWithResponseStreamResult(BaseModel):
    """Result of invoke_model_with_response_stream."""

    model_config = ConfigDict(frozen=True)

    body: dict[str, Any] | None = None
    content_type: str | None = None
    performance_config_latency: str | None = None


class ListAsyncInvokesResult(BaseModel):
    """Result of list_async_invokes."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    async_invoke_summaries: list[dict[str, Any]] | None = None


class StartAsyncInvokeResult(BaseModel):
    """Result of start_async_invoke."""

    model_config = ConfigDict(frozen=True)

    invocation_arn: str | None = None


def apply_guardrail(
    guardrail_identifier: str,
    guardrail_version: str,
    source: str,
    content: list[dict[str, Any]],
    *,
    output_scope: str | None = None,
    region_name: str | None = None,
) -> ApplyGuardrailResult:
    """Apply guardrail.

    Args:
        guardrail_identifier: Guardrail identifier.
        guardrail_version: Guardrail version.
        source: Source.
        content: Content.
        output_scope: Output scope.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["guardrailIdentifier"] = guardrail_identifier
    kwargs["guardrailVersion"] = guardrail_version
    kwargs["source"] = source
    kwargs["content"] = content
    if output_scope is not None:
        kwargs["outputScope"] = output_scope
    try:
        resp = client.apply_guardrail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to apply guardrail") from exc
    return ApplyGuardrailResult(
        usage=resp.get("usage"),
        action=resp.get("action"),
        action_reason=resp.get("actionReason"),
        outputs=resp.get("outputs"),
        assessments=resp.get("assessments"),
        guardrail_coverage=resp.get("guardrailCoverage"),
    )


def converse(
    model_id: str,
    *,
    messages: list[dict[str, Any]] | None = None,
    system: list[dict[str, Any]] | None = None,
    inference_config: dict[str, Any] | None = None,
    tool_config: dict[str, Any] | None = None,
    guardrail_config: dict[str, Any] | None = None,
    additional_model_request_fields: dict[str, Any] | None = None,
    prompt_variables: dict[str, Any] | None = None,
    additional_model_response_field_paths: list[str] | None = None,
    request_metadata: dict[str, Any] | None = None,
    performance_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ConverseResult:
    """Converse.

    Args:
        model_id: Model id.
        messages: Messages.
        system: System.
        inference_config: Inference config.
        tool_config: Tool config.
        guardrail_config: Guardrail config.
        additional_model_request_fields: Additional model request fields.
        prompt_variables: Prompt variables.
        additional_model_response_field_paths: Additional model response field paths.
        request_metadata: Request metadata.
        performance_config: Performance config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    if messages is not None:
        kwargs["messages"] = messages
    if system is not None:
        kwargs["system"] = system
    if inference_config is not None:
        kwargs["inferenceConfig"] = inference_config
    if tool_config is not None:
        kwargs["toolConfig"] = tool_config
    if guardrail_config is not None:
        kwargs["guardrailConfig"] = guardrail_config
    if additional_model_request_fields is not None:
        kwargs["additionalModelRequestFields"] = additional_model_request_fields
    if prompt_variables is not None:
        kwargs["promptVariables"] = prompt_variables
    if additional_model_response_field_paths is not None:
        kwargs["additionalModelResponseFieldPaths"] = additional_model_response_field_paths
    if request_metadata is not None:
        kwargs["requestMetadata"] = request_metadata
    if performance_config is not None:
        kwargs["performanceConfig"] = performance_config
    try:
        resp = client.converse(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to converse") from exc
    return ConverseResult(
        output=resp.get("output"),
        stop_reason=resp.get("stopReason"),
        usage=resp.get("usage"),
        metrics=resp.get("metrics"),
        additional_model_response_fields=resp.get("additionalModelResponseFields"),
        trace=resp.get("trace"),
        performance_config=resp.get("performanceConfig"),
    )


def converse_stream(
    model_id: str,
    *,
    messages: list[dict[str, Any]] | None = None,
    system: list[dict[str, Any]] | None = None,
    inference_config: dict[str, Any] | None = None,
    tool_config: dict[str, Any] | None = None,
    guardrail_config: dict[str, Any] | None = None,
    additional_model_request_fields: dict[str, Any] | None = None,
    prompt_variables: dict[str, Any] | None = None,
    additional_model_response_field_paths: list[str] | None = None,
    request_metadata: dict[str, Any] | None = None,
    performance_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ConverseStreamResult:
    """Converse stream.

    Args:
        model_id: Model id.
        messages: Messages.
        system: System.
        inference_config: Inference config.
        tool_config: Tool config.
        guardrail_config: Guardrail config.
        additional_model_request_fields: Additional model request fields.
        prompt_variables: Prompt variables.
        additional_model_response_field_paths: Additional model response field paths.
        request_metadata: Request metadata.
        performance_config: Performance config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    if messages is not None:
        kwargs["messages"] = messages
    if system is not None:
        kwargs["system"] = system
    if inference_config is not None:
        kwargs["inferenceConfig"] = inference_config
    if tool_config is not None:
        kwargs["toolConfig"] = tool_config
    if guardrail_config is not None:
        kwargs["guardrailConfig"] = guardrail_config
    if additional_model_request_fields is not None:
        kwargs["additionalModelRequestFields"] = additional_model_request_fields
    if prompt_variables is not None:
        kwargs["promptVariables"] = prompt_variables
    if additional_model_response_field_paths is not None:
        kwargs["additionalModelResponseFieldPaths"] = additional_model_response_field_paths
    if request_metadata is not None:
        kwargs["requestMetadata"] = request_metadata
    if performance_config is not None:
        kwargs["performanceConfig"] = performance_config
    try:
        resp = client.converse_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to converse stream") from exc
    return ConverseStreamResult(
        stream=resp.get("stream"),
    )


def count_tokens(
    model_id: str,
    input: dict[str, Any],
    region_name: str | None = None,
) -> CountTokensResult:
    """Count tokens.

    Args:
        model_id: Model id.
        input: Input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    kwargs["input"] = input
    try:
        resp = client.count_tokens(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to count tokens") from exc
    return CountTokensResult(
        input_tokens=resp.get("inputTokens"),
    )


def get_async_invoke(
    invocation_arn: str,
    region_name: str | None = None,
) -> GetAsyncInvokeResult:
    """Get async invoke.

    Args:
        invocation_arn: Invocation arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["invocationArn"] = invocation_arn
    try:
        resp = client.get_async_invoke(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get async invoke") from exc
    return GetAsyncInvokeResult(
        invocation_arn=resp.get("invocationArn"),
        model_arn=resp.get("modelArn"),
        client_request_token=resp.get("clientRequestToken"),
        status=resp.get("status"),
        failure_message=resp.get("failureMessage"),
        submit_time=resp.get("submitTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        end_time=resp.get("endTime"),
        output_data_config=resp.get("outputDataConfig"),
    )


def invoke_model_with_response_stream(
    model_id: str,
    *,
    body: bytes | None = None,
    content_type: str | None = None,
    accept: str | None = None,
    trace: str | None = None,
    guardrail_identifier: str | None = None,
    guardrail_version: str | None = None,
    performance_config_latency: str | None = None,
    region_name: str | None = None,
) -> InvokeModelWithResponseStreamResult:
    """Invoke model with response stream.

    Args:
        model_id: Model id.
        body: Body.
        content_type: Content type.
        accept: Accept.
        trace: Trace.
        guardrail_identifier: Guardrail identifier.
        guardrail_version: Guardrail version.
        performance_config_latency: Performance config latency.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    if body is not None:
        kwargs["body"] = body
    if content_type is not None:
        kwargs["contentType"] = content_type
    if accept is not None:
        kwargs["accept"] = accept
    if trace is not None:
        kwargs["trace"] = trace
    if guardrail_identifier is not None:
        kwargs["guardrailIdentifier"] = guardrail_identifier
    if guardrail_version is not None:
        kwargs["guardrailVersion"] = guardrail_version
    if performance_config_latency is not None:
        kwargs["performanceConfigLatency"] = performance_config_latency
    try:
        resp = client.invoke_model_with_response_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to invoke model with response stream") from exc
    return InvokeModelWithResponseStreamResult(
        body=resp.get("body"),
        content_type=resp.get("contentType"),
        performance_config_latency=resp.get("performanceConfigLatency"),
    )


def list_async_invokes(
    *,
    submit_time_after: str | None = None,
    submit_time_before: str | None = None,
    status_equals: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListAsyncInvokesResult:
    """List async invokes.

    Args:
        submit_time_after: Submit time after.
        submit_time_before: Submit time before.
        status_equals: Status equals.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if submit_time_after is not None:
        kwargs["submitTimeAfter"] = submit_time_after
    if submit_time_before is not None:
        kwargs["submitTimeBefore"] = submit_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_async_invokes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list async invokes") from exc
    return ListAsyncInvokesResult(
        next_token=resp.get("nextToken"),
        async_invoke_summaries=resp.get("asyncInvokeSummaries"),
    )


def start_async_invoke(
    model_id: str,
    model_input: dict[str, Any],
    output_data_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartAsyncInvokeResult:
    """Start async invoke.

    Args:
        model_id: Model id.
        model_input: Model input.
        output_data_config: Output data config.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    kwargs["modelInput"] = model_input
    kwargs["outputDataConfig"] = output_data_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.start_async_invoke(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start async invoke") from exc
    return StartAsyncInvokeResult(
        invocation_arn=resp.get("invocationArn"),
    )


# ---------------------------------------------------------------------------
# Generated boto3 method wrappers — Result models
# ---------------------------------------------------------------------------


class BatchDeleteEvaluationJobResult(BaseModel):
    """Result of batch_delete_evaluation_job."""

    model_config = ConfigDict(frozen=True)

    errors: list[Any] | None = None
    evaluation_jobs: list[Any] | None = None


class CancelAutomatedReasoningPolicyBuildWorkflowResult(BaseModel):
    """Result of cancel_automated_reasoning_policy_build_workflow."""

    model_config = ConfigDict(frozen=True)


class CreateAutomatedReasoningPolicyResult(BaseModel):
    """Result of create_automated_reasoning_policy."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    version: str | None = None
    name: str | None = None
    description: str | None = None
    definition_hash: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateAutomatedReasoningPolicyTestCaseResult(BaseModel):
    """Result of create_automated_reasoning_policy_test_case."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    test_case_id: str | None = None


class CreateAutomatedReasoningPolicyVersionResult(BaseModel):
    """Result of create_automated_reasoning_policy_version."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    version: str | None = None
    name: str | None = None
    description: str | None = None
    definition_hash: str | None = None
    created_at: str | None = None


class CreateCustomModelResult(BaseModel):
    """Result of create_custom_model."""

    model_config = ConfigDict(frozen=True)

    model_arn: str | None = None


class CreateCustomModelDeploymentResult(BaseModel):
    """Result of create_custom_model_deployment."""

    model_config = ConfigDict(frozen=True)

    custom_model_deployment_arn: str | None = None


class CreateEvaluationJobResult(BaseModel):
    """Result of create_evaluation_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None


class CreateFoundationModelAgreementResult(BaseModel):
    """Result of create_foundation_model_agreement."""

    model_config = ConfigDict(frozen=True)

    model_id: str | None = None


class CreateGuardrailResult(BaseModel):
    """Result of create_guardrail."""

    model_config = ConfigDict(frozen=True)

    guardrail_id: str | None = None
    guardrail_arn: str | None = None
    version: str | None = None
    created_at: str | None = None


class CreateGuardrailVersionResult(BaseModel):
    """Result of create_guardrail_version."""

    model_config = ConfigDict(frozen=True)

    guardrail_id: str | None = None
    version: str | None = None


class CreateInferenceProfileResult(BaseModel):
    """Result of create_inference_profile."""

    model_config = ConfigDict(frozen=True)

    inference_profile_arn: str | None = None
    status: str | None = None


class CreateMarketplaceModelEndpointResult(BaseModel):
    """Result of create_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)

    marketplace_model_endpoint: dict[str, Any] | None = None


class CreateModelCopyJobResult(BaseModel):
    """Result of create_model_copy_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None


class CreateModelCustomizationJobResult(BaseModel):
    """Result of create_model_customization_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None


class CreateModelImportJobResult(BaseModel):
    """Result of create_model_import_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None


class CreateModelInvocationJobResult(BaseModel):
    """Result of create_model_invocation_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None


class CreatePromptRouterResult(BaseModel):
    """Result of create_prompt_router."""

    model_config = ConfigDict(frozen=True)

    prompt_router_arn: str | None = None


class CreateProvisionedModelThroughputResult(BaseModel):
    """Result of create_provisioned_model_throughput."""

    model_config = ConfigDict(frozen=True)

    provisioned_model_arn: str | None = None


class DeleteAutomatedReasoningPolicyResult(BaseModel):
    """Result of delete_automated_reasoning_policy."""

    model_config = ConfigDict(frozen=True)


class DeleteAutomatedReasoningPolicyBuildWorkflowResult(BaseModel):
    """Result of delete_automated_reasoning_policy_build_workflow."""

    model_config = ConfigDict(frozen=True)


class DeleteAutomatedReasoningPolicyTestCaseResult(BaseModel):
    """Result of delete_automated_reasoning_policy_test_case."""

    model_config = ConfigDict(frozen=True)


class DeleteCustomModelResult(BaseModel):
    """Result of delete_custom_model."""

    model_config = ConfigDict(frozen=True)


class DeleteCustomModelDeploymentResult(BaseModel):
    """Result of delete_custom_model_deployment."""

    model_config = ConfigDict(frozen=True)


class DeleteFoundationModelAgreementResult(BaseModel):
    """Result of delete_foundation_model_agreement."""

    model_config = ConfigDict(frozen=True)


class DeleteGuardrailResult(BaseModel):
    """Result of delete_guardrail."""

    model_config = ConfigDict(frozen=True)


class DeleteImportedModelResult(BaseModel):
    """Result of delete_imported_model."""

    model_config = ConfigDict(frozen=True)


class DeleteInferenceProfileResult(BaseModel):
    """Result of delete_inference_profile."""

    model_config = ConfigDict(frozen=True)


class DeleteMarketplaceModelEndpointResult(BaseModel):
    """Result of delete_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)


class DeleteModelInvocationLoggingConfigurationResult(BaseModel):
    """Result of delete_model_invocation_logging_configuration."""

    model_config = ConfigDict(frozen=True)


class DeletePromptRouterResult(BaseModel):
    """Result of delete_prompt_router."""

    model_config = ConfigDict(frozen=True)


class DeleteProvisionedModelThroughputResult(BaseModel):
    """Result of delete_provisioned_model_throughput."""

    model_config = ConfigDict(frozen=True)


class DeregisterMarketplaceModelEndpointResult(BaseModel):
    """Result of deregister_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)


class ExportAutomatedReasoningPolicyVersionResult(BaseModel):
    """Result of export_automated_reasoning_policy_version."""

    model_config = ConfigDict(frozen=True)

    policy_definition: dict[str, Any] | None = None


class GetAutomatedReasoningPolicyResult(BaseModel):
    """Result of get_automated_reasoning_policy."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    name: str | None = None
    version: str | None = None
    policy_id: str | None = None
    description: str | None = None
    definition_hash: str | None = None
    kms_key_arn: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class GetAutomatedReasoningPolicyAnnotationsResult(BaseModel):
    """Result of get_automated_reasoning_policy_annotations."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    name: str | None = None
    build_workflow_id: str | None = None
    annotations: list[Any] | None = None
    annotation_set_hash: str | None = None
    updated_at: str | None = None


class GetAutomatedReasoningPolicyBuildWorkflowResult(BaseModel):
    """Result of get_automated_reasoning_policy_build_workflow."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    build_workflow_id: str | None = None
    status: str | None = None
    build_workflow_type: str | None = None
    document_name: str | None = None
    document_content_type: str | None = None
    document_description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class GetAutomatedReasoningPolicyBuildWorkflowResultAssetsResult(BaseModel):
    """Result of get_automated_reasoning_policy_build_workflow_result_assets."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    build_workflow_id: str | None = None
    build_workflow_assets: dict[str, Any] | None = None


class GetAutomatedReasoningPolicyNextScenarioResult(BaseModel):
    """Result of get_automated_reasoning_policy_next_scenario."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    scenario: dict[str, Any] | None = None


class GetAutomatedReasoningPolicyTestCaseResult(BaseModel):
    """Result of get_automated_reasoning_policy_test_case."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    test_case: dict[str, Any] | None = None


class GetAutomatedReasoningPolicyTestResultResult(BaseModel):
    """Result of get_automated_reasoning_policy_test_result."""

    model_config = ConfigDict(frozen=True)

    test_result: dict[str, Any] | None = None


class GetCustomModelResult(BaseModel):
    """Result of get_custom_model."""

    model_config = ConfigDict(frozen=True)

    model_arn: str | None = None
    model_name: str | None = None
    job_name: str | None = None
    job_arn: str | None = None
    base_model_arn: str | None = None
    customization_type: str | None = None
    model_kms_key_arn: str | None = None
    hyper_parameters: dict[str, Any] | None = None
    training_data_config: dict[str, Any] | None = None
    validation_data_config: dict[str, Any] | None = None
    output_data_config: dict[str, Any] | None = None
    training_metrics: dict[str, Any] | None = None
    validation_metrics: list[Any] | None = None
    creation_time: str | None = None
    customization_config: dict[str, Any] | None = None
    model_status: str | None = None
    failure_message: str | None = None


class GetCustomModelDeploymentResult(BaseModel):
    """Result of get_custom_model_deployment."""

    model_config = ConfigDict(frozen=True)

    custom_model_deployment_arn: str | None = None
    model_deployment_name: str | None = None
    model_arn: str | None = None
    created_at: str | None = None
    status: str | None = None
    description: str | None = None
    failure_message: str | None = None
    last_updated_at: str | None = None


class GetEvaluationJobResult(BaseModel):
    """Result of get_evaluation_job."""

    model_config = ConfigDict(frozen=True)

    job_name: str | None = None
    status: str | None = None
    job_arn: str | None = None
    job_description: str | None = None
    role_arn: str | None = None
    customer_encryption_key_id: str | None = None
    job_type: str | None = None
    application_type: str | None = None
    evaluation_config: dict[str, Any] | None = None
    inference_config: dict[str, Any] | None = None
    output_data_config: dict[str, Any] | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    failure_messages: list[Any] | None = None


class GetFoundationModelResult(BaseModel):
    """Result of get_foundation_model."""

    model_config = ConfigDict(frozen=True)

    model_details: dict[str, Any] | None = None


class GetFoundationModelAvailabilityResult(BaseModel):
    """Result of get_foundation_model_availability."""

    model_config = ConfigDict(frozen=True)

    model_id: str | None = None
    agreement_availability: dict[str, Any] | None = None
    authorization_status: str | None = None
    entitlement_availability: str | None = None
    region_availability: str | None = None


class GetGuardrailResult(BaseModel):
    """Result of get_guardrail."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    guardrail_id: str | None = None
    guardrail_arn: str | None = None
    version: str | None = None
    status: str | None = None
    topic_policy: dict[str, Any] | None = None
    content_policy: dict[str, Any] | None = None
    word_policy: dict[str, Any] | None = None
    sensitive_information_policy: dict[str, Any] | None = None
    contextual_grounding_policy: dict[str, Any] | None = None
    automated_reasoning_policy: dict[str, Any] | None = None
    cross_region_details: dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    status_reasons: list[Any] | None = None
    failure_recommendations: list[Any] | None = None
    blocked_input_messaging: str | None = None
    blocked_outputs_messaging: str | None = None
    kms_key_arn: str | None = None


class GetImportedModelResult(BaseModel):
    """Result of get_imported_model."""

    model_config = ConfigDict(frozen=True)

    model_arn: str | None = None
    model_name: str | None = None
    job_name: str | None = None
    job_arn: str | None = None
    model_data_source: dict[str, Any] | None = None
    creation_time: str | None = None
    model_architecture: str | None = None
    model_kms_key_arn: str | None = None
    instruct_supported: bool | None = None
    custom_model_units: dict[str, Any] | None = None


class GetInferenceProfileResult(BaseModel):
    """Result of get_inference_profile."""

    model_config = ConfigDict(frozen=True)

    inference_profile_name: str | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    inference_profile_arn: str | None = None
    models: list[Any] | None = None
    inference_profile_id: str | None = None
    status: str | None = None
    type: str | None = None


class GetMarketplaceModelEndpointResult(BaseModel):
    """Result of get_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)

    marketplace_model_endpoint: dict[str, Any] | None = None


class GetModelCopyJobResult(BaseModel):
    """Result of get_model_copy_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None
    status: str | None = None
    creation_time: str | None = None
    target_model_arn: str | None = None
    target_model_name: str | None = None
    source_account_id: str | None = None
    source_model_arn: str | None = None
    target_model_kms_key_arn: str | None = None
    target_model_tags: list[Any] | None = None
    failure_message: str | None = None
    source_model_name: str | None = None


class GetModelCustomizationJobResult(BaseModel):
    """Result of get_model_customization_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None
    job_name: str | None = None
    output_model_name: str | None = None
    output_model_arn: str | None = None
    client_request_token: str | None = None
    role_arn: str | None = None
    status: str | None = None
    status_details: dict[str, Any] | None = None
    failure_message: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    end_time: str | None = None
    base_model_arn: str | None = None
    hyper_parameters: dict[str, Any] | None = None
    training_data_config: dict[str, Any] | None = None
    validation_data_config: dict[str, Any] | None = None
    output_data_config: dict[str, Any] | None = None
    customization_type: str | None = None
    output_model_kms_key_arn: str | None = None
    training_metrics: dict[str, Any] | None = None
    validation_metrics: list[Any] | None = None
    vpc_config: dict[str, Any] | None = None
    customization_config: dict[str, Any] | None = None


class GetModelImportJobResult(BaseModel):
    """Result of get_model_import_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None
    job_name: str | None = None
    imported_model_name: str | None = None
    imported_model_arn: str | None = None
    role_arn: str | None = None
    model_data_source: dict[str, Any] | None = None
    status: str | None = None
    failure_message: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    end_time: str | None = None
    vpc_config: dict[str, Any] | None = None
    imported_model_kms_key_arn: str | None = None


class GetModelInvocationJobResult(BaseModel):
    """Result of get_model_invocation_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None
    job_name: str | None = None
    model_id: str | None = None
    client_request_token: str | None = None
    role_arn: str | None = None
    status: str | None = None
    message: str | None = None
    submit_time: str | None = None
    last_modified_time: str | None = None
    end_time: str | None = None
    input_data_config: dict[str, Any] | None = None
    output_data_config: dict[str, Any] | None = None
    vpc_config: dict[str, Any] | None = None
    timeout_duration_in_hours: int | None = None
    job_expiration_time: str | None = None


class GetModelInvocationLoggingConfigurationResult(BaseModel):
    """Result of get_model_invocation_logging_configuration."""

    model_config = ConfigDict(frozen=True)

    logging_config: dict[str, Any] | None = None


class GetPromptRouterResult(BaseModel):
    """Result of get_prompt_router."""

    model_config = ConfigDict(frozen=True)

    prompt_router_name: str | None = None
    routing_criteria: dict[str, Any] | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    prompt_router_arn: str | None = None
    models: list[Any] | None = None
    fallback_model: dict[str, Any] | None = None
    status: str | None = None
    type: str | None = None


class GetProvisionedModelThroughputResult(BaseModel):
    """Result of get_provisioned_model_throughput."""

    model_config = ConfigDict(frozen=True)

    model_units: int | None = None
    desired_model_units: int | None = None
    provisioned_model_name: str | None = None
    provisioned_model_arn: str | None = None
    model_arn: str | None = None
    desired_model_arn: str | None = None
    foundation_model_arn: str | None = None
    status: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    failure_message: str | None = None
    commitment_duration: str | None = None
    commitment_expiration_time: str | None = None


class GetUseCaseForModelAccessResult(BaseModel):
    """Result of get_use_case_for_model_access."""

    model_config = ConfigDict(frozen=True)

    form_data: Any | None = None


class ListAutomatedReasoningPoliciesResult(BaseModel):
    """Result of list_automated_reasoning_policies."""

    model_config = ConfigDict(frozen=True)

    automated_reasoning_policy_summaries: list[Any] | None = None
    next_token: str | None = None


class ListAutomatedReasoningPolicyBuildWorkflowsResult(BaseModel):
    """Result of list_automated_reasoning_policy_build_workflows."""

    model_config = ConfigDict(frozen=True)

    automated_reasoning_policy_build_workflow_summaries: list[Any] | None = None
    next_token: str | None = None


class ListAutomatedReasoningPolicyTestCasesResult(BaseModel):
    """Result of list_automated_reasoning_policy_test_cases."""

    model_config = ConfigDict(frozen=True)

    test_cases: list[Any] | None = None
    next_token: str | None = None


class ListAutomatedReasoningPolicyTestResultsResult(BaseModel):
    """Result of list_automated_reasoning_policy_test_results."""

    model_config = ConfigDict(frozen=True)

    test_results: list[Any] | None = None
    next_token: str | None = None


class ListCustomModelDeploymentsResult(BaseModel):
    """Result of list_custom_model_deployments."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_deployment_summaries: list[Any] | None = None


class ListCustomModelsResult(BaseModel):
    """Result of list_custom_models."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_summaries: list[Any] | None = None


class ListEvaluationJobsResult(BaseModel):
    """Result of list_evaluation_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    job_summaries: list[Any] | None = None


class ListFoundationModelAgreementOffersResult(BaseModel):
    """Result of list_foundation_model_agreement_offers."""

    model_config = ConfigDict(frozen=True)

    model_id: str | None = None
    offers: list[Any] | None = None


class ListGuardrailsResult(BaseModel):
    """Result of list_guardrails."""

    model_config = ConfigDict(frozen=True)

    guardrails: list[Any] | None = None
    next_token: str | None = None


class ListImportedModelsResult(BaseModel):
    """Result of list_imported_models."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_summaries: list[Any] | None = None


class ListInferenceProfilesResult(BaseModel):
    """Result of list_inference_profiles."""

    model_config = ConfigDict(frozen=True)

    inference_profile_summaries: list[Any] | None = None
    next_token: str | None = None


class ListMarketplaceModelEndpointsResult(BaseModel):
    """Result of list_marketplace_model_endpoints."""

    model_config = ConfigDict(frozen=True)

    marketplace_model_endpoints: list[Any] | None = None
    next_token: str | None = None


class ListModelCopyJobsResult(BaseModel):
    """Result of list_model_copy_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_copy_job_summaries: list[Any] | None = None


class ListModelCustomizationJobsResult(BaseModel):
    """Result of list_model_customization_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_customization_job_summaries: list[Any] | None = None


class ListModelImportJobsResult(BaseModel):
    """Result of list_model_import_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    model_import_job_summaries: list[Any] | None = None


class ListModelInvocationJobsResult(BaseModel):
    """Result of list_model_invocation_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    invocation_job_summaries: list[Any] | None = None


class ListPromptRoutersResult(BaseModel):
    """Result of list_prompt_routers."""

    model_config = ConfigDict(frozen=True)

    prompt_router_summaries: list[Any] | None = None
    next_token: str | None = None


class ListProvisionedModelThroughputsResult(BaseModel):
    """Result of list_provisioned_model_throughputs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    provisioned_model_summaries: list[Any] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[Any] | None = None


class PutModelInvocationLoggingConfigurationResult(BaseModel):
    """Result of put_model_invocation_logging_configuration."""

    model_config = ConfigDict(frozen=True)


class PutUseCaseForModelAccessResult(BaseModel):
    """Result of put_use_case_for_model_access."""

    model_config = ConfigDict(frozen=True)


class RegisterMarketplaceModelEndpointResult(BaseModel):
    """Result of register_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)

    marketplace_model_endpoint: dict[str, Any] | None = None


class StartAutomatedReasoningPolicyBuildWorkflowResult(BaseModel):
    """Result of start_automated_reasoning_policy_build_workflow."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    build_workflow_id: str | None = None


class StartAutomatedReasoningPolicyTestWorkflowResult(BaseModel):
    """Result of start_automated_reasoning_policy_test_workflow."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None


class StopEvaluationJobResult(BaseModel):
    """Result of stop_evaluation_job."""

    model_config = ConfigDict(frozen=True)


class StopModelCustomizationJobResult(BaseModel):
    """Result of stop_model_customization_job."""

    model_config = ConfigDict(frozen=True)


class StopModelInvocationJobResult(BaseModel):
    """Result of stop_model_invocation_job."""

    model_config = ConfigDict(frozen=True)


class TagResourceResult(BaseModel):
    """Result of tag_resource."""

    model_config = ConfigDict(frozen=True)


class UntagResourceResult(BaseModel):
    """Result of untag_resource."""

    model_config = ConfigDict(frozen=True)


class UpdateAutomatedReasoningPolicyResult(BaseModel):
    """Result of update_automated_reasoning_policy."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    name: str | None = None
    definition_hash: str | None = None
    updated_at: str | None = None


class UpdateAutomatedReasoningPolicyAnnotationsResult(BaseModel):
    """Result of update_automated_reasoning_policy_annotations."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    build_workflow_id: str | None = None
    annotation_set_hash: str | None = None
    updated_at: str | None = None


class UpdateAutomatedReasoningPolicyTestCaseResult(BaseModel):
    """Result of update_automated_reasoning_policy_test_case."""

    model_config = ConfigDict(frozen=True)

    policy_arn: str | None = None
    test_case_id: str | None = None


class UpdateGuardrailResult(BaseModel):
    """Result of update_guardrail."""

    model_config = ConfigDict(frozen=True)

    guardrail_id: str | None = None
    guardrail_arn: str | None = None
    version: str | None = None
    updated_at: str | None = None


class UpdateMarketplaceModelEndpointResult(BaseModel):
    """Result of update_marketplace_model_endpoint."""

    model_config = ConfigDict(frozen=True)

    marketplace_model_endpoint: dict[str, Any] | None = None


class UpdateProvisionedModelThroughputResult(BaseModel):
    """Result of update_provisioned_model_throughput."""

    model_config = ConfigDict(frozen=True)


# ---------------------------------------------------------------------------
# Generated boto3 method wrappers — Functions
# ---------------------------------------------------------------------------


def batch_delete_evaluation_job(
    job_identifiers: list[Any],
    *,
    region_name: str | None = None,
) -> BatchDeleteEvaluationJobResult:
    """Batch delete evaluation job.

    Args:
        job_identifiers: Job identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifiers"] = job_identifiers
    try:
        resp = client.batch_delete_evaluation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete evaluation job") from exc
    return BatchDeleteEvaluationJobResult(
        errors=resp.get("errors"),
        evaluation_jobs=resp.get("evaluationJobs"),
    )


def cancel_automated_reasoning_policy_build_workflow(
    policy_arn: str,
    build_workflow_id: str,
    *,
    region_name: str | None = None,
) -> CancelAutomatedReasoningPolicyBuildWorkflowResult:
    """Cancel automated reasoning policy build workflow.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    try:
        client.cancel_automated_reasoning_policy_build_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to cancel automated reasoning policy build workflow"
        ) from exc
    return CancelAutomatedReasoningPolicyBuildWorkflowResult()


def create_automated_reasoning_policy(
    name: str,
    *,
    description: str | None = None,
    client_request_token: str | None = None,
    policy_definition: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateAutomatedReasoningPolicyResult:
    """Create automated reasoning policy.

    Args:
        name: Name.
        description: Description.
        client_request_token: Client request token.
        policy_definition: Policy definition.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if policy_definition is not None:
        kwargs["policyDefinition"] = policy_definition
    if kms_key_id is not None:
        kwargs["kmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_automated_reasoning_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create automated reasoning policy") from exc
    return CreateAutomatedReasoningPolicyResult(
        policy_arn=resp.get("policyArn"),
        version=resp.get("version"),
        name=resp.get("name"),
        description=resp.get("description"),
        definition_hash=resp.get("definitionHash"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def create_automated_reasoning_policy_test_case(
    policy_arn: str,
    guard_content: str,
    expected_aggregated_findings_result: str,
    *,
    query_content: str | None = None,
    client_request_token: str | None = None,
    confidence_threshold: float | None = None,
    region_name: str | None = None,
) -> CreateAutomatedReasoningPolicyTestCaseResult:
    """Create automated reasoning policy test case.

    Args:
        policy_arn: Policy arn.
        guard_content: Guard content.
        expected_aggregated_findings_result: Expected aggregated findings result.
        query_content: Query content.
        client_request_token: Client request token.
        confidence_threshold: Confidence threshold.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["guardContent"] = guard_content
    kwargs["expectedAggregatedFindingsResult"] = expected_aggregated_findings_result
    if query_content is not None:
        kwargs["queryContent"] = query_content
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if confidence_threshold is not None:
        kwargs["confidenceThreshold"] = confidence_threshold
    try:
        resp = client.create_automated_reasoning_policy_test_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create automated reasoning policy test case") from exc
    return CreateAutomatedReasoningPolicyTestCaseResult(
        policy_arn=resp.get("policyArn"),
        test_case_id=resp.get("testCaseId"),
    )


def create_automated_reasoning_policy_version(
    policy_arn: str,
    last_updated_definition_hash: str,
    *,
    client_request_token: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateAutomatedReasoningPolicyVersionResult:
    """Create automated reasoning policy version.

    Args:
        policy_arn: Policy arn.
        last_updated_definition_hash: Last updated definition hash.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["lastUpdatedDefinitionHash"] = last_updated_definition_hash
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_automated_reasoning_policy_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create automated reasoning policy version") from exc
    return CreateAutomatedReasoningPolicyVersionResult(
        policy_arn=resp.get("policyArn"),
        version=resp.get("version"),
        name=resp.get("name"),
        description=resp.get("description"),
        definition_hash=resp.get("definitionHash"),
        created_at=resp.get("createdAt"),
    )


def create_custom_model(
    model_name: str,
    model_source_config: dict[str, Any],
    *,
    model_kms_key_arn: str | None = None,
    role_arn: str | None = None,
    model_tags: list[Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateCustomModelResult:
    """Create custom model.

    Args:
        model_name: Model name.
        model_source_config: Model source config.
        model_kms_key_arn: Model kms key arn.
        role_arn: Role arn.
        model_tags: Model tags.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelName"] = model_name
    kwargs["modelSourceConfig"] = model_source_config
    if model_kms_key_arn is not None:
        kwargs["modelKmsKeyArn"] = model_kms_key_arn
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if model_tags is not None:
        kwargs["modelTags"] = model_tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.create_custom_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create custom model") from exc
    return CreateCustomModelResult(
        model_arn=resp.get("modelArn"),
    )


def create_custom_model_deployment(
    model_deployment_name: str,
    model_arn: str,
    *,
    description: str | None = None,
    tags: list[Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateCustomModelDeploymentResult:
    """Create custom model deployment.

    Args:
        model_deployment_name: Model deployment name.
        model_arn: Model arn.
        description: Description.
        tags: Tags.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelDeploymentName"] = model_deployment_name
    kwargs["modelArn"] = model_arn
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.create_custom_model_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create custom model deployment") from exc
    return CreateCustomModelDeploymentResult(
        custom_model_deployment_arn=resp.get("customModelDeploymentArn"),
    )


def create_evaluation_job(
    job_name: str,
    role_arn: str,
    evaluation_config: dict[str, Any],
    inference_config: dict[str, Any],
    output_data_config: dict[str, Any],
    *,
    job_description: str | None = None,
    client_request_token: str | None = None,
    customer_encryption_key_id: str | None = None,
    job_tags: list[Any] | None = None,
    application_type: str | None = None,
    region_name: str | None = None,
) -> CreateEvaluationJobResult:
    """Create evaluation job.

    Args:
        job_name: Job name.
        role_arn: Role arn.
        evaluation_config: Evaluation config.
        inference_config: Inference config.
        output_data_config: Output data config.
        job_description: Job description.
        client_request_token: Client request token.
        customer_encryption_key_id: Customer encryption key id.
        job_tags: Job tags.
        application_type: Application type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["roleArn"] = role_arn
    kwargs["evaluationConfig"] = evaluation_config
    kwargs["inferenceConfig"] = inference_config
    kwargs["outputDataConfig"] = output_data_config
    if job_description is not None:
        kwargs["jobDescription"] = job_description
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if customer_encryption_key_id is not None:
        kwargs["customerEncryptionKeyId"] = customer_encryption_key_id
    if job_tags is not None:
        kwargs["jobTags"] = job_tags
    if application_type is not None:
        kwargs["applicationType"] = application_type
    try:
        resp = client.create_evaluation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create evaluation job") from exc
    return CreateEvaluationJobResult(
        job_arn=resp.get("jobArn"),
    )


def create_foundation_model_agreement(
    offer_token: str,
    model_id: str,
    *,
    region_name: str | None = None,
) -> CreateFoundationModelAgreementResult:
    """Create foundation model agreement.

    Args:
        offer_token: Offer token.
        model_id: Model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["offerToken"] = offer_token
    kwargs["modelId"] = model_id
    try:
        resp = client.create_foundation_model_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create foundation model agreement") from exc
    return CreateFoundationModelAgreementResult(
        model_id=resp.get("modelId"),
    )


def create_guardrail(
    name: str,
    blocked_input_messaging: str,
    blocked_outputs_messaging: str,
    *,
    description: str | None = None,
    topic_policy_config: dict[str, Any] | None = None,
    content_policy_config: dict[str, Any] | None = None,
    word_policy_config: dict[str, Any] | None = None,
    sensitive_information_policy_config: dict[str, Any] | None = None,
    contextual_grounding_policy_config: dict[str, Any] | None = None,
    automated_reasoning_policy_config: dict[str, Any] | None = None,
    cross_region_config: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    tags: list[Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateGuardrailResult:
    """Create guardrail.

    Args:
        name: Name.
        blocked_input_messaging: Blocked input messaging.
        blocked_outputs_messaging: Blocked outputs messaging.
        description: Description.
        topic_policy_config: Topic policy config.
        content_policy_config: Content policy config.
        word_policy_config: Word policy config.
        sensitive_information_policy_config: Sensitive information policy config.
        contextual_grounding_policy_config: Contextual grounding policy config.
        automated_reasoning_policy_config: Automated reasoning policy config.
        cross_region_config: Cross region config.
        kms_key_id: Kms key id.
        tags: Tags.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["blockedInputMessaging"] = blocked_input_messaging
    kwargs["blockedOutputsMessaging"] = blocked_outputs_messaging
    if description is not None:
        kwargs["description"] = description
    if topic_policy_config is not None:
        kwargs["topicPolicyConfig"] = topic_policy_config
    if content_policy_config is not None:
        kwargs["contentPolicyConfig"] = content_policy_config
    if word_policy_config is not None:
        kwargs["wordPolicyConfig"] = word_policy_config
    if sensitive_information_policy_config is not None:
        kwargs["sensitiveInformationPolicyConfig"] = sensitive_information_policy_config
    if contextual_grounding_policy_config is not None:
        kwargs["contextualGroundingPolicyConfig"] = contextual_grounding_policy_config
    if automated_reasoning_policy_config is not None:
        kwargs["automatedReasoningPolicyConfig"] = automated_reasoning_policy_config
    if cross_region_config is not None:
        kwargs["crossRegionConfig"] = cross_region_config
    if kms_key_id is not None:
        kwargs["kmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["tags"] = tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.create_guardrail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create guardrail") from exc
    return CreateGuardrailResult(
        guardrail_id=resp.get("guardrailId"),
        guardrail_arn=resp.get("guardrailArn"),
        version=resp.get("version"),
        created_at=resp.get("createdAt"),
    )


def create_guardrail_version(
    guardrail_identifier: str,
    *,
    description: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateGuardrailVersionResult:
    """Create guardrail version.

    Args:
        guardrail_identifier: Guardrail identifier.
        description: Description.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["guardrailIdentifier"] = guardrail_identifier
    if description is not None:
        kwargs["description"] = description
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.create_guardrail_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create guardrail version") from exc
    return CreateGuardrailVersionResult(
        guardrail_id=resp.get("guardrailId"),
        version=resp.get("version"),
    )


def create_inference_profile(
    inference_profile_name: str,
    model_source: dict[str, Any],
    *,
    description: str | None = None,
    client_request_token: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateInferenceProfileResult:
    """Create inference profile.

    Args:
        inference_profile_name: Inference profile name.
        model_source: Model source.
        description: Description.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["inferenceProfileName"] = inference_profile_name
    kwargs["modelSource"] = model_source
    if description is not None:
        kwargs["description"] = description
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_inference_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create inference profile") from exc
    return CreateInferenceProfileResult(
        inference_profile_arn=resp.get("inferenceProfileArn"),
        status=resp.get("status"),
    )


def create_marketplace_model_endpoint(
    model_source_identifier: str,
    endpoint_config: dict[str, Any],
    endpoint_name: str,
    *,
    accept_eula: bool | None = None,
    client_request_token: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateMarketplaceModelEndpointResult:
    """Create marketplace model endpoint.

    Args:
        model_source_identifier: Model source identifier.
        endpoint_config: Endpoint config.
        endpoint_name: Endpoint name.
        accept_eula: Accept eula.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelSourceIdentifier"] = model_source_identifier
    kwargs["endpointConfig"] = endpoint_config
    kwargs["endpointName"] = endpoint_name
    if accept_eula is not None:
        kwargs["acceptEula"] = accept_eula
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create marketplace model endpoint") from exc
    return CreateMarketplaceModelEndpointResult(
        marketplace_model_endpoint=resp.get("marketplaceModelEndpoint"),
    )


def create_model_copy_job(
    source_model_arn: str,
    target_model_name: str,
    *,
    model_kms_key_id: str | None = None,
    target_model_tags: list[Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateModelCopyJobResult:
    """Create model copy job.

    Args:
        source_model_arn: Source model arn.
        target_model_name: Target model name.
        model_kms_key_id: Model kms key id.
        target_model_tags: Target model tags.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sourceModelArn"] = source_model_arn
    kwargs["targetModelName"] = target_model_name
    if model_kms_key_id is not None:
        kwargs["modelKmsKeyId"] = model_kms_key_id
    if target_model_tags is not None:
        kwargs["targetModelTags"] = target_model_tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.create_model_copy_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create model copy job") from exc
    return CreateModelCopyJobResult(
        job_arn=resp.get("jobArn"),
    )


def create_model_customization_job(
    job_name: str,
    custom_model_name: str,
    role_arn: str,
    base_model_identifier: str,
    training_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    customization_type: str | None = None,
    custom_model_kms_key_id: str | None = None,
    job_tags: list[Any] | None = None,
    custom_model_tags: list[Any] | None = None,
    validation_data_config: dict[str, Any] | None = None,
    hyper_parameters: dict[str, Any] | None = None,
    vpc_config: dict[str, Any] | None = None,
    customization_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateModelCustomizationJobResult:
    """Create model customization job.

    Args:
        job_name: Job name.
        custom_model_name: Custom model name.
        role_arn: Role arn.
        base_model_identifier: Base model identifier.
        training_data_config: Training data config.
        output_data_config: Output data config.
        client_request_token: Client request token.
        customization_type: Customization type.
        custom_model_kms_key_id: Custom model kms key id.
        job_tags: Job tags.
        custom_model_tags: Custom model tags.
        validation_data_config: Validation data config.
        hyper_parameters: Hyper parameters.
        vpc_config: Vpc config.
        customization_config: Customization config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["customModelName"] = custom_model_name
    kwargs["roleArn"] = role_arn
    kwargs["baseModelIdentifier"] = base_model_identifier
    kwargs["trainingDataConfig"] = training_data_config
    kwargs["outputDataConfig"] = output_data_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if customization_type is not None:
        kwargs["customizationType"] = customization_type
    if custom_model_kms_key_id is not None:
        kwargs["customModelKmsKeyId"] = custom_model_kms_key_id
    if job_tags is not None:
        kwargs["jobTags"] = job_tags
    if custom_model_tags is not None:
        kwargs["customModelTags"] = custom_model_tags
    if validation_data_config is not None:
        kwargs["validationDataConfig"] = validation_data_config
    if hyper_parameters is not None:
        kwargs["hyperParameters"] = hyper_parameters
    if vpc_config is not None:
        kwargs["vpcConfig"] = vpc_config
    if customization_config is not None:
        kwargs["customizationConfig"] = customization_config
    try:
        resp = client.create_model_customization_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create model customization job") from exc
    return CreateModelCustomizationJobResult(
        job_arn=resp.get("jobArn"),
    )


def create_model_import_job(
    job_name: str,
    imported_model_name: str,
    role_arn: str,
    model_data_source: dict[str, Any],
    *,
    job_tags: list[Any] | None = None,
    imported_model_tags: list[Any] | None = None,
    client_request_token: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    imported_model_kms_key_id: str | None = None,
    region_name: str | None = None,
) -> CreateModelImportJobResult:
    """Create model import job.

    Args:
        job_name: Job name.
        imported_model_name: Imported model name.
        role_arn: Role arn.
        model_data_source: Model data source.
        job_tags: Job tags.
        imported_model_tags: Imported model tags.
        client_request_token: Client request token.
        vpc_config: Vpc config.
        imported_model_kms_key_id: Imported model kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["importedModelName"] = imported_model_name
    kwargs["roleArn"] = role_arn
    kwargs["modelDataSource"] = model_data_source
    if job_tags is not None:
        kwargs["jobTags"] = job_tags
    if imported_model_tags is not None:
        kwargs["importedModelTags"] = imported_model_tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if vpc_config is not None:
        kwargs["vpcConfig"] = vpc_config
    if imported_model_kms_key_id is not None:
        kwargs["importedModelKmsKeyId"] = imported_model_kms_key_id
    try:
        resp = client.create_model_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create model import job") from exc
    return CreateModelImportJobResult(
        job_arn=resp.get("jobArn"),
    )


def create_model_invocation_job(
    job_name: str,
    role_arn: str,
    model_id: str,
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    timeout_duration_in_hours: int | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateModelInvocationJobResult:
    """Create model invocation job.

    Args:
        job_name: Job name.
        role_arn: Role arn.
        model_id: Model id.
        input_data_config: Input data config.
        output_data_config: Output data config.
        client_request_token: Client request token.
        vpc_config: Vpc config.
        timeout_duration_in_hours: Timeout duration in hours.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["roleArn"] = role_arn
    kwargs["modelId"] = model_id
    kwargs["inputDataConfig"] = input_data_config
    kwargs["outputDataConfig"] = output_data_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if vpc_config is not None:
        kwargs["vpcConfig"] = vpc_config
    if timeout_duration_in_hours is not None:
        kwargs["timeoutDurationInHours"] = timeout_duration_in_hours
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_model_invocation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create model invocation job") from exc
    return CreateModelInvocationJobResult(
        job_arn=resp.get("jobArn"),
    )


def create_prompt_router(
    prompt_router_name: str,
    models: list[Any],
    routing_criteria: dict[str, Any],
    fallback_model: dict[str, Any],
    *,
    client_request_token: str | None = None,
    description: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreatePromptRouterResult:
    """Create prompt router.

    Args:
        prompt_router_name: Prompt router name.
        models: Models.
        routing_criteria: Routing criteria.
        fallback_model: Fallback model.
        client_request_token: Client request token.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptRouterName"] = prompt_router_name
    kwargs["models"] = models
    kwargs["routingCriteria"] = routing_criteria
    kwargs["fallbackModel"] = fallback_model
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_prompt_router(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create prompt router") from exc
    return CreatePromptRouterResult(
        prompt_router_arn=resp.get("promptRouterArn"),
    )


def create_provisioned_model_throughput(
    model_units: int,
    provisioned_model_name: str,
    model_id: str,
    *,
    client_request_token: str | None = None,
    commitment_duration: str | None = None,
    tags: list[Any] | None = None,
    region_name: str | None = None,
) -> CreateProvisionedModelThroughputResult:
    """Create provisioned model throughput.

    Args:
        model_units: Model units.
        provisioned_model_name: Provisioned model name.
        model_id: Model id.
        client_request_token: Client request token.
        commitment_duration: Commitment duration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelUnits"] = model_units
    kwargs["provisionedModelName"] = provisioned_model_name
    kwargs["modelId"] = model_id
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if commitment_duration is not None:
        kwargs["commitmentDuration"] = commitment_duration
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_provisioned_model_throughput(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create provisioned model throughput") from exc
    return CreateProvisionedModelThroughputResult(
        provisioned_model_arn=resp.get("provisionedModelArn"),
    )


def delete_automated_reasoning_policy(
    policy_arn: str,
    *,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeleteAutomatedReasoningPolicyResult:
    """Delete automated reasoning policy.

    Args:
        policy_arn: Policy arn.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    if force is not None:
        kwargs["force"] = force
    try:
        client.delete_automated_reasoning_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete automated reasoning policy") from exc
    return DeleteAutomatedReasoningPolicyResult()


def delete_automated_reasoning_policy_build_workflow(
    policy_arn: str,
    build_workflow_id: str,
    last_updated_at: str,
    *,
    region_name: str | None = None,
) -> DeleteAutomatedReasoningPolicyBuildWorkflowResult:
    """Delete automated reasoning policy build workflow.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        last_updated_at: Last updated at.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    kwargs["lastUpdatedAt"] = last_updated_at
    try:
        client.delete_automated_reasoning_policy_build_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete automated reasoning policy build workflow"
        ) from exc
    return DeleteAutomatedReasoningPolicyBuildWorkflowResult()


def delete_automated_reasoning_policy_test_case(
    policy_arn: str,
    test_case_id: str,
    last_updated_at: str,
    *,
    region_name: str | None = None,
) -> DeleteAutomatedReasoningPolicyTestCaseResult:
    """Delete automated reasoning policy test case.

    Args:
        policy_arn: Policy arn.
        test_case_id: Test case id.
        last_updated_at: Last updated at.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["testCaseId"] = test_case_id
    kwargs["lastUpdatedAt"] = last_updated_at
    try:
        client.delete_automated_reasoning_policy_test_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete automated reasoning policy test case") from exc
    return DeleteAutomatedReasoningPolicyTestCaseResult()


def delete_custom_model(
    model_identifier: str,
    *,
    region_name: str | None = None,
) -> DeleteCustomModelResult:
    """Delete custom model.

    Args:
        model_identifier: Model identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelIdentifier"] = model_identifier
    try:
        client.delete_custom_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete custom model") from exc
    return DeleteCustomModelResult()


def delete_custom_model_deployment(
    custom_model_deployment_identifier: str,
    *,
    region_name: str | None = None,
) -> DeleteCustomModelDeploymentResult:
    """Delete custom model deployment.

    Args:
        custom_model_deployment_identifier: Custom model deployment identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customModelDeploymentIdentifier"] = custom_model_deployment_identifier
    try:
        client.delete_custom_model_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete custom model deployment") from exc
    return DeleteCustomModelDeploymentResult()


def delete_foundation_model_agreement(
    model_id: str,
    *,
    region_name: str | None = None,
) -> DeleteFoundationModelAgreementResult:
    """Delete foundation model agreement.

    Args:
        model_id: Model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    try:
        client.delete_foundation_model_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete foundation model agreement") from exc
    return DeleteFoundationModelAgreementResult()


def delete_guardrail(
    guardrail_identifier: str,
    *,
    guardrail_version: str | None = None,
    region_name: str | None = None,
) -> DeleteGuardrailResult:
    """Delete guardrail.

    Args:
        guardrail_identifier: Guardrail identifier.
        guardrail_version: Guardrail version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["guardrailIdentifier"] = guardrail_identifier
    if guardrail_version is not None:
        kwargs["guardrailVersion"] = guardrail_version
    try:
        client.delete_guardrail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete guardrail") from exc
    return DeleteGuardrailResult()


def delete_imported_model(
    model_identifier: str,
    *,
    region_name: str | None = None,
) -> DeleteImportedModelResult:
    """Delete imported model.

    Args:
        model_identifier: Model identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelIdentifier"] = model_identifier
    try:
        client.delete_imported_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete imported model") from exc
    return DeleteImportedModelResult()


def delete_inference_profile(
    inference_profile_identifier: str,
    *,
    region_name: str | None = None,
) -> DeleteInferenceProfileResult:
    """Delete inference profile.

    Args:
        inference_profile_identifier: Inference profile identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["inferenceProfileIdentifier"] = inference_profile_identifier
    try:
        client.delete_inference_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete inference profile") from exc
    return DeleteInferenceProfileResult()


def delete_marketplace_model_endpoint(
    endpoint_arn: str,
    *,
    region_name: str | None = None,
) -> DeleteMarketplaceModelEndpointResult:
    """Delete marketplace model endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointArn"] = endpoint_arn
    try:
        client.delete_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete marketplace model endpoint") from exc
    return DeleteMarketplaceModelEndpointResult()


def delete_model_invocation_logging_configuration(
    *,
    region_name: str | None = None,
) -> DeleteModelInvocationLoggingConfigurationResult:
    """Delete model invocation logging configuration.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    try:
        client.delete_model_invocation_logging_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete model invocation logging configuration"
        ) from exc
    return DeleteModelInvocationLoggingConfigurationResult()


def delete_prompt_router(
    prompt_router_arn: str,
    *,
    region_name: str | None = None,
) -> DeletePromptRouterResult:
    """Delete prompt router.

    Args:
        prompt_router_arn: Prompt router arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptRouterArn"] = prompt_router_arn
    try:
        client.delete_prompt_router(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete prompt router") from exc
    return DeletePromptRouterResult()


def delete_provisioned_model_throughput(
    provisioned_model_id: str,
    *,
    region_name: str | None = None,
) -> DeleteProvisionedModelThroughputResult:
    """Delete provisioned model throughput.

    Args:
        provisioned_model_id: Provisioned model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["provisionedModelId"] = provisioned_model_id
    try:
        client.delete_provisioned_model_throughput(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete provisioned model throughput") from exc
    return DeleteProvisionedModelThroughputResult()


def deregister_marketplace_model_endpoint(
    endpoint_arn: str,
    *,
    region_name: str | None = None,
) -> DeregisterMarketplaceModelEndpointResult:
    """Deregister marketplace model endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointArn"] = endpoint_arn
    try:
        client.deregister_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister marketplace model endpoint") from exc
    return DeregisterMarketplaceModelEndpointResult()


def export_automated_reasoning_policy_version(
    policy_arn: str,
    *,
    region_name: str | None = None,
) -> ExportAutomatedReasoningPolicyVersionResult:
    """Export automated reasoning policy version.

    Args:
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    try:
        resp = client.export_automated_reasoning_policy_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to export automated reasoning policy version") from exc
    return ExportAutomatedReasoningPolicyVersionResult(
        policy_definition=resp.get("policyDefinition"),
    )


def get_automated_reasoning_policy(
    policy_arn: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyResult:
    """Get automated reasoning policy.

    Args:
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    try:
        resp = client.get_automated_reasoning_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get automated reasoning policy") from exc
    return GetAutomatedReasoningPolicyResult(
        policy_arn=resp.get("policyArn"),
        name=resp.get("name"),
        version=resp.get("version"),
        policy_id=resp.get("policyId"),
        description=resp.get("description"),
        definition_hash=resp.get("definitionHash"),
        kms_key_arn=resp.get("kmsKeyArn"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def get_automated_reasoning_policy_annotations(
    policy_arn: str,
    build_workflow_id: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyAnnotationsResult:
    """Get automated reasoning policy annotations.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    try:
        resp = client.get_automated_reasoning_policy_annotations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get automated reasoning policy annotations") from exc
    return GetAutomatedReasoningPolicyAnnotationsResult(
        policy_arn=resp.get("policyArn"),
        name=resp.get("name"),
        build_workflow_id=resp.get("buildWorkflowId"),
        annotations=resp.get("annotations"),
        annotation_set_hash=resp.get("annotationSetHash"),
        updated_at=resp.get("updatedAt"),
    )


def get_automated_reasoning_policy_build_workflow(
    policy_arn: str,
    build_workflow_id: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyBuildWorkflowResult:
    """Get automated reasoning policy build workflow.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    try:
        resp = client.get_automated_reasoning_policy_build_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get automated reasoning policy build workflow"
        ) from exc
    return GetAutomatedReasoningPolicyBuildWorkflowResult(
        policy_arn=resp.get("policyArn"),
        build_workflow_id=resp.get("buildWorkflowId"),
        status=resp.get("status"),
        build_workflow_type=resp.get("buildWorkflowType"),
        document_name=resp.get("documentName"),
        document_content_type=resp.get("documentContentType"),
        document_description=resp.get("documentDescription"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def get_automated_reasoning_policy_build_workflow_result_assets(
    policy_arn: str,
    build_workflow_id: str,
    asset_type: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyBuildWorkflowResultAssetsResult:
    """Get automated reasoning policy build workflow result assets.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        asset_type: Asset type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    kwargs["assetType"] = asset_type
    try:
        resp = client.get_automated_reasoning_policy_build_workflow_result_assets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get automated reasoning policy build workflow result assets"
        ) from exc
    return GetAutomatedReasoningPolicyBuildWorkflowResultAssetsResult(
        policy_arn=resp.get("policyArn"),
        build_workflow_id=resp.get("buildWorkflowId"),
        build_workflow_assets=resp.get("buildWorkflowAssets"),
    )


def get_automated_reasoning_policy_next_scenario(
    policy_arn: str,
    build_workflow_id: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyNextScenarioResult:
    """Get automated reasoning policy next scenario.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    try:
        resp = client.get_automated_reasoning_policy_next_scenario(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get automated reasoning policy next scenario") from exc
    return GetAutomatedReasoningPolicyNextScenarioResult(
        policy_arn=resp.get("policyArn"),
        scenario=resp.get("scenario"),
    )


def get_automated_reasoning_policy_test_case(
    policy_arn: str,
    test_case_id: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyTestCaseResult:
    """Get automated reasoning policy test case.

    Args:
        policy_arn: Policy arn.
        test_case_id: Test case id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["testCaseId"] = test_case_id
    try:
        resp = client.get_automated_reasoning_policy_test_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get automated reasoning policy test case") from exc
    return GetAutomatedReasoningPolicyTestCaseResult(
        policy_arn=resp.get("policyArn"),
        test_case=resp.get("testCase"),
    )


def get_automated_reasoning_policy_test_result(
    policy_arn: str,
    build_workflow_id: str,
    test_case_id: str,
    *,
    region_name: str | None = None,
) -> GetAutomatedReasoningPolicyTestResultResult:
    """Get automated reasoning policy test result.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        test_case_id: Test case id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    kwargs["testCaseId"] = test_case_id
    try:
        resp = client.get_automated_reasoning_policy_test_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get automated reasoning policy test result") from exc
    return GetAutomatedReasoningPolicyTestResultResult(
        test_result=resp.get("testResult"),
    )


def get_custom_model(
    model_identifier: str,
    *,
    region_name: str | None = None,
) -> GetCustomModelResult:
    """Get custom model.

    Args:
        model_identifier: Model identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelIdentifier"] = model_identifier
    try:
        resp = client.get_custom_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get custom model") from exc
    return GetCustomModelResult(
        model_arn=resp.get("modelArn"),
        model_name=resp.get("modelName"),
        job_name=resp.get("jobName"),
        job_arn=resp.get("jobArn"),
        base_model_arn=resp.get("baseModelArn"),
        customization_type=resp.get("customizationType"),
        model_kms_key_arn=resp.get("modelKmsKeyArn"),
        hyper_parameters=resp.get("hyperParameters"),
        training_data_config=resp.get("trainingDataConfig"),
        validation_data_config=resp.get("validationDataConfig"),
        output_data_config=resp.get("outputDataConfig"),
        training_metrics=resp.get("trainingMetrics"),
        validation_metrics=resp.get("validationMetrics"),
        creation_time=resp.get("creationTime"),
        customization_config=resp.get("customizationConfig"),
        model_status=resp.get("modelStatus"),
        failure_message=resp.get("failureMessage"),
    )


def get_custom_model_deployment(
    custom_model_deployment_identifier: str,
    *,
    region_name: str | None = None,
) -> GetCustomModelDeploymentResult:
    """Get custom model deployment.

    Args:
        custom_model_deployment_identifier: Custom model deployment identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customModelDeploymentIdentifier"] = custom_model_deployment_identifier
    try:
        resp = client.get_custom_model_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get custom model deployment") from exc
    return GetCustomModelDeploymentResult(
        custom_model_deployment_arn=resp.get("customModelDeploymentArn"),
        model_deployment_name=resp.get("modelDeploymentName"),
        model_arn=resp.get("modelArn"),
        created_at=resp.get("createdAt"),
        status=resp.get("status"),
        description=resp.get("description"),
        failure_message=resp.get("failureMessage"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_evaluation_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> GetEvaluationJobResult:
    """Get evaluation job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        resp = client.get_evaluation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get evaluation job") from exc
    return GetEvaluationJobResult(
        job_name=resp.get("jobName"),
        status=resp.get("status"),
        job_arn=resp.get("jobArn"),
        job_description=resp.get("jobDescription"),
        role_arn=resp.get("roleArn"),
        customer_encryption_key_id=resp.get("customerEncryptionKeyId"),
        job_type=resp.get("jobType"),
        application_type=resp.get("applicationType"),
        evaluation_config=resp.get("evaluationConfig"),
        inference_config=resp.get("inferenceConfig"),
        output_data_config=resp.get("outputDataConfig"),
        creation_time=resp.get("creationTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        failure_messages=resp.get("failureMessages"),
    )


def get_foundation_model(
    model_identifier: str,
    *,
    region_name: str | None = None,
) -> GetFoundationModelResult:
    """Get foundation model.

    Args:
        model_identifier: Model identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelIdentifier"] = model_identifier
    try:
        resp = client.get_foundation_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get foundation model") from exc
    return GetFoundationModelResult(
        model_details=resp.get("modelDetails"),
    )


def get_foundation_model_availability(
    model_id: str,
    *,
    region_name: str | None = None,
) -> GetFoundationModelAvailabilityResult:
    """Get foundation model availability.

    Args:
        model_id: Model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    try:
        resp = client.get_foundation_model_availability(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get foundation model availability") from exc
    return GetFoundationModelAvailabilityResult(
        model_id=resp.get("modelId"),
        agreement_availability=resp.get("agreementAvailability"),
        authorization_status=resp.get("authorizationStatus"),
        entitlement_availability=resp.get("entitlementAvailability"),
        region_availability=resp.get("regionAvailability"),
    )


def get_guardrail(
    guardrail_identifier: str,
    *,
    guardrail_version: str | None = None,
    region_name: str | None = None,
) -> GetGuardrailResult:
    """Get guardrail.

    Args:
        guardrail_identifier: Guardrail identifier.
        guardrail_version: Guardrail version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["guardrailIdentifier"] = guardrail_identifier
    if guardrail_version is not None:
        kwargs["guardrailVersion"] = guardrail_version
    try:
        resp = client.get_guardrail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get guardrail") from exc
    return GetGuardrailResult(
        name=resp.get("name"),
        description=resp.get("description"),
        guardrail_id=resp.get("guardrailId"),
        guardrail_arn=resp.get("guardrailArn"),
        version=resp.get("version"),
        status=resp.get("status"),
        topic_policy=resp.get("topicPolicy"),
        content_policy=resp.get("contentPolicy"),
        word_policy=resp.get("wordPolicy"),
        sensitive_information_policy=resp.get("sensitiveInformationPolicy"),
        contextual_grounding_policy=resp.get("contextualGroundingPolicy"),
        automated_reasoning_policy=resp.get("automatedReasoningPolicy"),
        cross_region_details=resp.get("crossRegionDetails"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        status_reasons=resp.get("statusReasons"),
        failure_recommendations=resp.get("failureRecommendations"),
        blocked_input_messaging=resp.get("blockedInputMessaging"),
        blocked_outputs_messaging=resp.get("blockedOutputsMessaging"),
        kms_key_arn=resp.get("kmsKeyArn"),
    )


def get_imported_model(
    model_identifier: str,
    *,
    region_name: str | None = None,
) -> GetImportedModelResult:
    """Get imported model.

    Args:
        model_identifier: Model identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelIdentifier"] = model_identifier
    try:
        resp = client.get_imported_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get imported model") from exc
    return GetImportedModelResult(
        model_arn=resp.get("modelArn"),
        model_name=resp.get("modelName"),
        job_name=resp.get("jobName"),
        job_arn=resp.get("jobArn"),
        model_data_source=resp.get("modelDataSource"),
        creation_time=resp.get("creationTime"),
        model_architecture=resp.get("modelArchitecture"),
        model_kms_key_arn=resp.get("modelKmsKeyArn"),
        instruct_supported=resp.get("instructSupported"),
        custom_model_units=resp.get("customModelUnits"),
    )


def get_inference_profile(
    inference_profile_identifier: str,
    *,
    region_name: str | None = None,
) -> GetInferenceProfileResult:
    """Get inference profile.

    Args:
        inference_profile_identifier: Inference profile identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["inferenceProfileIdentifier"] = inference_profile_identifier
    try:
        resp = client.get_inference_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get inference profile") from exc
    return GetInferenceProfileResult(
        inference_profile_name=resp.get("inferenceProfileName"),
        description=resp.get("description"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        inference_profile_arn=resp.get("inferenceProfileArn"),
        models=resp.get("models"),
        inference_profile_id=resp.get("inferenceProfileId"),
        status=resp.get("status"),
        type=resp.get("type"),
    )


def get_marketplace_model_endpoint(
    endpoint_arn: str,
    *,
    region_name: str | None = None,
) -> GetMarketplaceModelEndpointResult:
    """Get marketplace model endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointArn"] = endpoint_arn
    try:
        resp = client.get_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get marketplace model endpoint") from exc
    return GetMarketplaceModelEndpointResult(
        marketplace_model_endpoint=resp.get("marketplaceModelEndpoint"),
    )


def get_model_copy_job(
    job_arn: str,
    *,
    region_name: str | None = None,
) -> GetModelCopyJobResult:
    """Get model copy job.

    Args:
        job_arn: Job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobArn"] = job_arn
    try:
        resp = client.get_model_copy_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get model copy job") from exc
    return GetModelCopyJobResult(
        job_arn=resp.get("jobArn"),
        status=resp.get("status"),
        creation_time=resp.get("creationTime"),
        target_model_arn=resp.get("targetModelArn"),
        target_model_name=resp.get("targetModelName"),
        source_account_id=resp.get("sourceAccountId"),
        source_model_arn=resp.get("sourceModelArn"),
        target_model_kms_key_arn=resp.get("targetModelKmsKeyArn"),
        target_model_tags=resp.get("targetModelTags"),
        failure_message=resp.get("failureMessage"),
        source_model_name=resp.get("sourceModelName"),
    )


def get_model_customization_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> GetModelCustomizationJobResult:
    """Get model customization job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        resp = client.get_model_customization_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get model customization job") from exc
    return GetModelCustomizationJobResult(
        job_arn=resp.get("jobArn"),
        job_name=resp.get("jobName"),
        output_model_name=resp.get("outputModelName"),
        output_model_arn=resp.get("outputModelArn"),
        client_request_token=resp.get("clientRequestToken"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        status_details=resp.get("statusDetails"),
        failure_message=resp.get("failureMessage"),
        creation_time=resp.get("creationTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        end_time=resp.get("endTime"),
        base_model_arn=resp.get("baseModelArn"),
        hyper_parameters=resp.get("hyperParameters"),
        training_data_config=resp.get("trainingDataConfig"),
        validation_data_config=resp.get("validationDataConfig"),
        output_data_config=resp.get("outputDataConfig"),
        customization_type=resp.get("customizationType"),
        output_model_kms_key_arn=resp.get("outputModelKmsKeyArn"),
        training_metrics=resp.get("trainingMetrics"),
        validation_metrics=resp.get("validationMetrics"),
        vpc_config=resp.get("vpcConfig"),
        customization_config=resp.get("customizationConfig"),
    )


def get_model_import_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> GetModelImportJobResult:
    """Get model import job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        resp = client.get_model_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get model import job") from exc
    return GetModelImportJobResult(
        job_arn=resp.get("jobArn"),
        job_name=resp.get("jobName"),
        imported_model_name=resp.get("importedModelName"),
        imported_model_arn=resp.get("importedModelArn"),
        role_arn=resp.get("roleArn"),
        model_data_source=resp.get("modelDataSource"),
        status=resp.get("status"),
        failure_message=resp.get("failureMessage"),
        creation_time=resp.get("creationTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        end_time=resp.get("endTime"),
        vpc_config=resp.get("vpcConfig"),
        imported_model_kms_key_arn=resp.get("importedModelKmsKeyArn"),
    )


def get_model_invocation_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> GetModelInvocationJobResult:
    """Get model invocation job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        resp = client.get_model_invocation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get model invocation job") from exc
    return GetModelInvocationJobResult(
        job_arn=resp.get("jobArn"),
        job_name=resp.get("jobName"),
        model_id=resp.get("modelId"),
        client_request_token=resp.get("clientRequestToken"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        message=resp.get("message"),
        submit_time=resp.get("submitTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        end_time=resp.get("endTime"),
        input_data_config=resp.get("inputDataConfig"),
        output_data_config=resp.get("outputDataConfig"),
        vpc_config=resp.get("vpcConfig"),
        timeout_duration_in_hours=resp.get("timeoutDurationInHours"),
        job_expiration_time=resp.get("jobExpirationTime"),
    )


def get_model_invocation_logging_configuration(
    *,
    region_name: str | None = None,
) -> GetModelInvocationLoggingConfigurationResult:
    """Get model invocation logging configuration.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    try:
        resp = client.get_model_invocation_logging_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get model invocation logging configuration") from exc
    return GetModelInvocationLoggingConfigurationResult(
        logging_config=resp.get("loggingConfig"),
    )


def get_prompt_router(
    prompt_router_arn: str,
    *,
    region_name: str | None = None,
) -> GetPromptRouterResult:
    """Get prompt router.

    Args:
        prompt_router_arn: Prompt router arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptRouterArn"] = prompt_router_arn
    try:
        resp = client.get_prompt_router(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get prompt router") from exc
    return GetPromptRouterResult(
        prompt_router_name=resp.get("promptRouterName"),
        routing_criteria=resp.get("routingCriteria"),
        description=resp.get("description"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        prompt_router_arn=resp.get("promptRouterArn"),
        models=resp.get("models"),
        fallback_model=resp.get("fallbackModel"),
        status=resp.get("status"),
        type=resp.get("type"),
    )


def get_provisioned_model_throughput(
    provisioned_model_id: str,
    *,
    region_name: str | None = None,
) -> GetProvisionedModelThroughputResult:
    """Get provisioned model throughput.

    Args:
        provisioned_model_id: Provisioned model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["provisionedModelId"] = provisioned_model_id
    try:
        resp = client.get_provisioned_model_throughput(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get provisioned model throughput") from exc
    return GetProvisionedModelThroughputResult(
        model_units=resp.get("modelUnits"),
        desired_model_units=resp.get("desiredModelUnits"),
        provisioned_model_name=resp.get("provisionedModelName"),
        provisioned_model_arn=resp.get("provisionedModelArn"),
        model_arn=resp.get("modelArn"),
        desired_model_arn=resp.get("desiredModelArn"),
        foundation_model_arn=resp.get("foundationModelArn"),
        status=resp.get("status"),
        creation_time=resp.get("creationTime"),
        last_modified_time=resp.get("lastModifiedTime"),
        failure_message=resp.get("failureMessage"),
        commitment_duration=resp.get("commitmentDuration"),
        commitment_expiration_time=resp.get("commitmentExpirationTime"),
    )


def get_use_case_for_model_access(
    *,
    region_name: str | None = None,
) -> GetUseCaseForModelAccessResult:
    """Get use case for model access.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    try:
        resp = client.get_use_case_for_model_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get use case for model access") from exc
    return GetUseCaseForModelAccessResult(
        form_data=resp.get("formData"),
    )


def list_automated_reasoning_policies(
    *,
    policy_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomatedReasoningPoliciesResult:
    """List automated reasoning policies.

    Args:
        policy_arn: Policy arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if policy_arn is not None:
        kwargs["policyArn"] = policy_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_automated_reasoning_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automated reasoning policies") from exc
    return ListAutomatedReasoningPoliciesResult(
        automated_reasoning_policy_summaries=resp.get("automatedReasoningPolicySummaries"),
        next_token=resp.get("nextToken"),
    )


def list_automated_reasoning_policy_build_workflows(
    policy_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomatedReasoningPolicyBuildWorkflowsResult:
    """List automated reasoning policy build workflows.

    Args:
        policy_arn: Policy arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_automated_reasoning_policy_build_workflows(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list automated reasoning policy build workflows"
        ) from exc
    return ListAutomatedReasoningPolicyBuildWorkflowsResult(
        automated_reasoning_policy_build_workflow_summaries=resp.get(
            "automatedReasoningPolicyBuildWorkflowSummaries"
        ),
        next_token=resp.get("nextToken"),
    )


def list_automated_reasoning_policy_test_cases(
    policy_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomatedReasoningPolicyTestCasesResult:
    """List automated reasoning policy test cases.

    Args:
        policy_arn: Policy arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_automated_reasoning_policy_test_cases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automated reasoning policy test cases") from exc
    return ListAutomatedReasoningPolicyTestCasesResult(
        test_cases=resp.get("testCases"),
        next_token=resp.get("nextToken"),
    )


def list_automated_reasoning_policy_test_results(
    policy_arn: str,
    build_workflow_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomatedReasoningPolicyTestResultsResult:
    """List automated reasoning policy test results.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_automated_reasoning_policy_test_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automated reasoning policy test results") from exc
    return ListAutomatedReasoningPolicyTestResultsResult(
        test_results=resp.get("testResults"),
        next_token=resp.get("nextToken"),
    )


def list_custom_model_deployments(
    *,
    created_before: str | None = None,
    created_after: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    status_equals: str | None = None,
    model_arn_equals: str | None = None,
    region_name: str | None = None,
) -> ListCustomModelDeploymentsResult:
    """List custom model deployments.

    Args:
        created_before: Created before.
        created_after: Created after.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        status_equals: Status equals.
        model_arn_equals: Model arn equals.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if created_before is not None:
        kwargs["createdBefore"] = created_before
    if created_after is not None:
        kwargs["createdAfter"] = created_after
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if model_arn_equals is not None:
        kwargs["modelArnEquals"] = model_arn_equals
    try:
        resp = client.list_custom_model_deployments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list custom model deployments") from exc
    return ListCustomModelDeploymentsResult(
        next_token=resp.get("nextToken"),
        model_deployment_summaries=resp.get("modelDeploymentSummaries"),
    )


def list_custom_models(
    *,
    creation_time_before: str | None = None,
    creation_time_after: str | None = None,
    name_contains: str | None = None,
    base_model_arn_equals: str | None = None,
    foundation_model_arn_equals: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    is_owned: bool | None = None,
    model_status: str | None = None,
    region_name: str | None = None,
) -> ListCustomModelsResult:
    """List custom models.

    Args:
        creation_time_before: Creation time before.
        creation_time_after: Creation time after.
        name_contains: Name contains.
        base_model_arn_equals: Base model arn equals.
        foundation_model_arn_equals: Foundation model arn equals.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        is_owned: Is owned.
        model_status: Model status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if base_model_arn_equals is not None:
        kwargs["baseModelArnEquals"] = base_model_arn_equals
    if foundation_model_arn_equals is not None:
        kwargs["foundationModelArnEquals"] = foundation_model_arn_equals
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if is_owned is not None:
        kwargs["isOwned"] = is_owned
    if model_status is not None:
        kwargs["modelStatus"] = model_status
    try:
        resp = client.list_custom_models(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list custom models") from exc
    return ListCustomModelsResult(
        next_token=resp.get("nextToken"),
        model_summaries=resp.get("modelSummaries"),
    )


def list_evaluation_jobs(
    *,
    creation_time_after: str | None = None,
    creation_time_before: str | None = None,
    status_equals: str | None = None,
    application_type_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListEvaluationJobsResult:
    """List evaluation jobs.

    Args:
        creation_time_after: Creation time after.
        creation_time_before: Creation time before.
        status_equals: Status equals.
        application_type_equals: Application type equals.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if application_type_equals is not None:
        kwargs["applicationTypeEquals"] = application_type_equals
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_evaluation_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list evaluation jobs") from exc
    return ListEvaluationJobsResult(
        next_token=resp.get("nextToken"),
        job_summaries=resp.get("jobSummaries"),
    )


def list_foundation_model_agreement_offers(
    model_id: str,
    *,
    offer_type: str | None = None,
    region_name: str | None = None,
) -> ListFoundationModelAgreementOffersResult:
    """List foundation model agreement offers.

    Args:
        model_id: Model id.
        offer_type: Offer type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["modelId"] = model_id
    if offer_type is not None:
        kwargs["offerType"] = offer_type
    try:
        resp = client.list_foundation_model_agreement_offers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list foundation model agreement offers") from exc
    return ListFoundationModelAgreementOffersResult(
        model_id=resp.get("modelId"),
        offers=resp.get("offers"),
    )


def list_guardrails(
    *,
    guardrail_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListGuardrailsResult:
    """List guardrails.

    Args:
        guardrail_identifier: Guardrail identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if guardrail_identifier is not None:
        kwargs["guardrailIdentifier"] = guardrail_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_guardrails(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list guardrails") from exc
    return ListGuardrailsResult(
        guardrails=resp.get("guardrails"),
        next_token=resp.get("nextToken"),
    )


def list_imported_models(
    *,
    creation_time_before: str | None = None,
    creation_time_after: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListImportedModelsResult:
    """List imported models.

    Args:
        creation_time_before: Creation time before.
        creation_time_after: Creation time after.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_imported_models(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list imported models") from exc
    return ListImportedModelsResult(
        next_token=resp.get("nextToken"),
        model_summaries=resp.get("modelSummaries"),
    )


def list_inference_profiles(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    type_equals: str | None = None,
    region_name: str | None = None,
) -> ListInferenceProfilesResult:
    """List inference profiles.

    Args:
        max_results: Max results.
        next_token: Next token.
        type_equals: Type equals.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if type_equals is not None:
        kwargs["typeEquals"] = type_equals
    try:
        resp = client.list_inference_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list inference profiles") from exc
    return ListInferenceProfilesResult(
        inference_profile_summaries=resp.get("inferenceProfileSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_marketplace_model_endpoints(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    model_source_equals: str | None = None,
    region_name: str | None = None,
) -> ListMarketplaceModelEndpointsResult:
    """List marketplace model endpoints.

    Args:
        max_results: Max results.
        next_token: Next token.
        model_source_equals: Model source equals.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if model_source_equals is not None:
        kwargs["modelSourceEquals"] = model_source_equals
    try:
        resp = client.list_marketplace_model_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list marketplace model endpoints") from exc
    return ListMarketplaceModelEndpointsResult(
        marketplace_model_endpoints=resp.get("marketplaceModelEndpoints"),
        next_token=resp.get("nextToken"),
    )


def list_model_copy_jobs(
    *,
    creation_time_after: str | None = None,
    creation_time_before: str | None = None,
    status_equals: str | None = None,
    source_account_equals: str | None = None,
    source_model_arn_equals: str | None = None,
    target_model_name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListModelCopyJobsResult:
    """List model copy jobs.

    Args:
        creation_time_after: Creation time after.
        creation_time_before: Creation time before.
        status_equals: Status equals.
        source_account_equals: Source account equals.
        source_model_arn_equals: Source model arn equals.
        target_model_name_contains: Target model name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if source_account_equals is not None:
        kwargs["sourceAccountEquals"] = source_account_equals
    if source_model_arn_equals is not None:
        kwargs["sourceModelArnEquals"] = source_model_arn_equals
    if target_model_name_contains is not None:
        kwargs["targetModelNameContains"] = target_model_name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_model_copy_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list model copy jobs") from exc
    return ListModelCopyJobsResult(
        next_token=resp.get("nextToken"),
        model_copy_job_summaries=resp.get("modelCopyJobSummaries"),
    )


def list_model_customization_jobs(
    *,
    creation_time_after: str | None = None,
    creation_time_before: str | None = None,
    status_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListModelCustomizationJobsResult:
    """List model customization jobs.

    Args:
        creation_time_after: Creation time after.
        creation_time_before: Creation time before.
        status_equals: Status equals.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_model_customization_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list model customization jobs") from exc
    return ListModelCustomizationJobsResult(
        next_token=resp.get("nextToken"),
        model_customization_job_summaries=resp.get("modelCustomizationJobSummaries"),
    )


def list_model_import_jobs(
    *,
    creation_time_after: str | None = None,
    creation_time_before: str | None = None,
    status_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListModelImportJobsResult:
    """List model import jobs.

    Args:
        creation_time_after: Creation time after.
        creation_time_before: Creation time before.
        status_equals: Status equals.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_model_import_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list model import jobs") from exc
    return ListModelImportJobsResult(
        next_token=resp.get("nextToken"),
        model_import_job_summaries=resp.get("modelImportJobSummaries"),
    )


def list_model_invocation_jobs(
    *,
    submit_time_after: str | None = None,
    submit_time_before: str | None = None,
    status_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListModelInvocationJobsResult:
    """List model invocation jobs.

    Args:
        submit_time_after: Submit time after.
        submit_time_before: Submit time before.
        status_equals: Status equals.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if submit_time_after is not None:
        kwargs["submitTimeAfter"] = submit_time_after
    if submit_time_before is not None:
        kwargs["submitTimeBefore"] = submit_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_model_invocation_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list model invocation jobs") from exc
    return ListModelInvocationJobsResult(
        next_token=resp.get("nextToken"),
        invocation_job_summaries=resp.get("invocationJobSummaries"),
    )


def list_prompt_routers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    type: str | None = None,
    region_name: str | None = None,
) -> ListPromptRoutersResult:
    """List prompt routers.

    Args:
        max_results: Max results.
        next_token: Next token.
        type: Type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if type is not None:
        kwargs["type"] = type
    try:
        resp = client.list_prompt_routers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list prompt routers") from exc
    return ListPromptRoutersResult(
        prompt_router_summaries=resp.get("promptRouterSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_provisioned_model_throughputs(
    *,
    creation_time_after: str | None = None,
    creation_time_before: str | None = None,
    status_equals: str | None = None,
    model_arn_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListProvisionedModelThroughputsResult:
    """List provisioned model throughputs.

    Args:
        creation_time_after: Creation time after.
        creation_time_before: Creation time before.
        status_equals: Status equals.
        model_arn_equals: Model arn equals.
        name_contains: Name contains.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    if creation_time_after is not None:
        kwargs["creationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["creationTimeBefore"] = creation_time_before
    if status_equals is not None:
        kwargs["statusEquals"] = status_equals
    if model_arn_equals is not None:
        kwargs["modelArnEquals"] = model_arn_equals
    if name_contains is not None:
        kwargs["nameContains"] = name_contains
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = client.list_provisioned_model_throughputs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list provisioned model throughputs") from exc
    return ListProvisionedModelThroughputsResult(
        next_token=resp.get("nextToken"),
        provisioned_model_summaries=resp.get("provisionedModelSummaries"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def put_model_invocation_logging_configuration(
    logging_config: dict[str, Any],
    *,
    region_name: str | None = None,
) -> PutModelInvocationLoggingConfigurationResult:
    """Put model invocation logging configuration.

    Args:
        logging_config: Logging config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loggingConfig"] = logging_config
    try:
        client.put_model_invocation_logging_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put model invocation logging configuration") from exc
    return PutModelInvocationLoggingConfigurationResult()


def put_use_case_for_model_access(
    form_data: Any,
    *,
    region_name: str | None = None,
) -> PutUseCaseForModelAccessResult:
    """Put use case for model access.

    Args:
        form_data: Form data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["formData"] = form_data
    try:
        client.put_use_case_for_model_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put use case for model access") from exc
    return PutUseCaseForModelAccessResult()


def register_marketplace_model_endpoint(
    endpoint_identifier: str,
    model_source_identifier: str,
    *,
    region_name: str | None = None,
) -> RegisterMarketplaceModelEndpointResult:
    """Register marketplace model endpoint.

    Args:
        endpoint_identifier: Endpoint identifier.
        model_source_identifier: Model source identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointIdentifier"] = endpoint_identifier
    kwargs["modelSourceIdentifier"] = model_source_identifier
    try:
        resp = client.register_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register marketplace model endpoint") from exc
    return RegisterMarketplaceModelEndpointResult(
        marketplace_model_endpoint=resp.get("marketplaceModelEndpoint"),
    )


def start_automated_reasoning_policy_build_workflow(
    policy_arn: str,
    build_workflow_type: str,
    source_content: dict[str, Any],
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartAutomatedReasoningPolicyBuildWorkflowResult:
    """Start automated reasoning policy build workflow.

    Args:
        policy_arn: Policy arn.
        build_workflow_type: Build workflow type.
        source_content: Source content.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowType"] = build_workflow_type
    kwargs["sourceContent"] = source_content
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.start_automated_reasoning_policy_build_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to start automated reasoning policy build workflow"
        ) from exc
    return StartAutomatedReasoningPolicyBuildWorkflowResult(
        policy_arn=resp.get("policyArn"),
        build_workflow_id=resp.get("buildWorkflowId"),
    )


def start_automated_reasoning_policy_test_workflow(
    policy_arn: str,
    build_workflow_id: str,
    *,
    test_case_ids: list[Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartAutomatedReasoningPolicyTestWorkflowResult:
    """Start automated reasoning policy test workflow.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        test_case_ids: Test case ids.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    if test_case_ids is not None:
        kwargs["testCaseIds"] = test_case_ids
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.start_automated_reasoning_policy_test_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to start automated reasoning policy test workflow"
        ) from exc
    return StartAutomatedReasoningPolicyTestWorkflowResult(
        policy_arn=resp.get("policyArn"),
    )


def stop_evaluation_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> StopEvaluationJobResult:
    """Stop evaluation job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        client.stop_evaluation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop evaluation job") from exc
    return StopEvaluationJobResult()


def stop_model_customization_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> StopModelCustomizationJobResult:
    """Stop model customization job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        client.stop_model_customization_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop model customization job") from exc
    return StopModelCustomizationJobResult()


def stop_model_invocation_job(
    job_identifier: str,
    *,
    region_name: str | None = None,
) -> StopModelInvocationJobResult:
    """Stop model invocation job.

    Args:
        job_identifier: Job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobIdentifier"] = job_identifier
    try:
        client.stop_model_invocation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop model invocation job") from exc
    return StopModelInvocationJobResult()


def tag_resource(
    resource_arn: str,
    tags: list[Any],
    *,
    region_name: str | None = None,
) -> TagResourceResult:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return TagResourceResult()


def untag_resource(
    resource_arn: str,
    tag_keys: list[Any],
    *,
    region_name: str | None = None,
) -> UntagResourceResult:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return UntagResourceResult()


def update_automated_reasoning_policy(
    policy_arn: str,
    policy_definition: dict[str, Any],
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateAutomatedReasoningPolicyResult:
    """Update automated reasoning policy.

    Args:
        policy_arn: Policy arn.
        policy_definition: Policy definition.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["policyDefinition"] = policy_definition
    if name is not None:
        kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.update_automated_reasoning_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update automated reasoning policy") from exc
    return UpdateAutomatedReasoningPolicyResult(
        policy_arn=resp.get("policyArn"),
        name=resp.get("name"),
        definition_hash=resp.get("definitionHash"),
        updated_at=resp.get("updatedAt"),
    )


def update_automated_reasoning_policy_annotations(
    policy_arn: str,
    build_workflow_id: str,
    annotations: list[Any],
    last_updated_annotation_set_hash: str,
    *,
    region_name: str | None = None,
) -> UpdateAutomatedReasoningPolicyAnnotationsResult:
    """Update automated reasoning policy annotations.

    Args:
        policy_arn: Policy arn.
        build_workflow_id: Build workflow id.
        annotations: Annotations.
        last_updated_annotation_set_hash: Last updated annotation set hash.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["buildWorkflowId"] = build_workflow_id
    kwargs["annotations"] = annotations
    kwargs["lastUpdatedAnnotationSetHash"] = last_updated_annotation_set_hash
    try:
        resp = client.update_automated_reasoning_policy_annotations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to update automated reasoning policy annotations"
        ) from exc
    return UpdateAutomatedReasoningPolicyAnnotationsResult(
        policy_arn=resp.get("policyArn"),
        build_workflow_id=resp.get("buildWorkflowId"),
        annotation_set_hash=resp.get("annotationSetHash"),
        updated_at=resp.get("updatedAt"),
    )


def update_automated_reasoning_policy_test_case(
    policy_arn: str,
    test_case_id: str,
    guard_content: str,
    last_updated_at: str,
    expected_aggregated_findings_result: str,
    *,
    query_content: str | None = None,
    confidence_threshold: float | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateAutomatedReasoningPolicyTestCaseResult:
    """Update automated reasoning policy test case.

    Args:
        policy_arn: Policy arn.
        test_case_id: Test case id.
        guard_content: Guard content.
        last_updated_at: Last updated at.
        expected_aggregated_findings_result: Expected aggregated findings result.
        query_content: Query content.
        confidence_threshold: Confidence threshold.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyArn"] = policy_arn
    kwargs["testCaseId"] = test_case_id
    kwargs["guardContent"] = guard_content
    kwargs["lastUpdatedAt"] = last_updated_at
    kwargs["expectedAggregatedFindingsResult"] = expected_aggregated_findings_result
    if query_content is not None:
        kwargs["queryContent"] = query_content
    if confidence_threshold is not None:
        kwargs["confidenceThreshold"] = confidence_threshold
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.update_automated_reasoning_policy_test_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update automated reasoning policy test case") from exc
    return UpdateAutomatedReasoningPolicyTestCaseResult(
        policy_arn=resp.get("policyArn"),
        test_case_id=resp.get("testCaseId"),
    )


def update_guardrail(
    guardrail_identifier: str,
    name: str,
    blocked_input_messaging: str,
    blocked_outputs_messaging: str,
    *,
    description: str | None = None,
    topic_policy_config: dict[str, Any] | None = None,
    content_policy_config: dict[str, Any] | None = None,
    word_policy_config: dict[str, Any] | None = None,
    sensitive_information_policy_config: dict[str, Any] | None = None,
    contextual_grounding_policy_config: dict[str, Any] | None = None,
    automated_reasoning_policy_config: dict[str, Any] | None = None,
    cross_region_config: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> UpdateGuardrailResult:
    """Update guardrail.

    Args:
        guardrail_identifier: Guardrail identifier.
        name: Name.
        blocked_input_messaging: Blocked input messaging.
        blocked_outputs_messaging: Blocked outputs messaging.
        description: Description.
        topic_policy_config: Topic policy config.
        content_policy_config: Content policy config.
        word_policy_config: Word policy config.
        sensitive_information_policy_config: Sensitive information policy config.
        contextual_grounding_policy_config: Contextual grounding policy config.
        automated_reasoning_policy_config: Automated reasoning policy config.
        cross_region_config: Cross region config.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["guardrailIdentifier"] = guardrail_identifier
    kwargs["name"] = name
    kwargs["blockedInputMessaging"] = blocked_input_messaging
    kwargs["blockedOutputsMessaging"] = blocked_outputs_messaging
    if description is not None:
        kwargs["description"] = description
    if topic_policy_config is not None:
        kwargs["topicPolicyConfig"] = topic_policy_config
    if content_policy_config is not None:
        kwargs["contentPolicyConfig"] = content_policy_config
    if word_policy_config is not None:
        kwargs["wordPolicyConfig"] = word_policy_config
    if sensitive_information_policy_config is not None:
        kwargs["sensitiveInformationPolicyConfig"] = sensitive_information_policy_config
    if contextual_grounding_policy_config is not None:
        kwargs["contextualGroundingPolicyConfig"] = contextual_grounding_policy_config
    if automated_reasoning_policy_config is not None:
        kwargs["automatedReasoningPolicyConfig"] = automated_reasoning_policy_config
    if cross_region_config is not None:
        kwargs["crossRegionConfig"] = cross_region_config
    if kms_key_id is not None:
        kwargs["kmsKeyId"] = kms_key_id
    try:
        resp = client.update_guardrail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update guardrail") from exc
    return UpdateGuardrailResult(
        guardrail_id=resp.get("guardrailId"),
        guardrail_arn=resp.get("guardrailArn"),
        version=resp.get("version"),
        updated_at=resp.get("updatedAt"),
    )


def update_marketplace_model_endpoint(
    endpoint_arn: str,
    endpoint_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateMarketplaceModelEndpointResult:
    """Update marketplace model endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        endpoint_config: Endpoint config.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointArn"] = endpoint_arn
    kwargs["endpointConfig"] = endpoint_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.update_marketplace_model_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update marketplace model endpoint") from exc
    return UpdateMarketplaceModelEndpointResult(
        marketplace_model_endpoint=resp.get("marketplaceModelEndpoint"),
    )


def update_provisioned_model_throughput(
    provisioned_model_id: str,
    *,
    desired_provisioned_model_name: str | None = None,
    desired_model_id: str | None = None,
    region_name: str | None = None,
) -> UpdateProvisionedModelThroughputResult:
    """Update provisioned model throughput.

    Args:
        provisioned_model_id: Provisioned model id.
        desired_provisioned_model_name: Desired provisioned model name.
        desired_model_id: Desired model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["provisionedModelId"] = provisioned_model_id
    if desired_provisioned_model_name is not None:
        kwargs["desiredProvisionedModelName"] = desired_provisioned_model_name
    if desired_model_id is not None:
        kwargs["desiredModelId"] = desired_model_id
    try:
        client.update_provisioned_model_throughput(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update provisioned model throughput") from exc
    return UpdateProvisionedModelThroughputResult()
