"""Native async Bedrock Agent Runtime utilities using the async engine."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.bedrock_agent_runtime import (
    Citation,
    CreateInvocationResult,
    CreateSessionResult,
    EndSessionResult,
    GenerateQueryResult,
    GetAgentMemoryResult,
    GetExecutionFlowSnapshotResult,
    GetFlowExecutionResult,
    GetInvocationStepResult,
    GetSessionResult,
    InvokeAgentResult,
    InvokeFlowResult,
    InvokeInlineAgentResult,
    KnowledgeBaseQuery,
    ListFlowExecutionEventsResult,
    ListFlowExecutionsResult,
    ListInvocationsResult,
    ListInvocationStepsResult,
    ListSessionsResult,
    ListTagsForResourceResult,
    OptimizePromptResult,
    PutInvocationStepResult,
    RerankResult,
    RetrievalResult,
    RetrieveAndGenerateResult,
    RetrieveAndGenerateStreamResult,
    RetrievedReference,
    StartFlowExecutionResult,
    StopFlowExecutionResult,
    UpdateSessionResult,
    _parse_citations,
)
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "Citation",
    "CreateInvocationResult",
    "CreateSessionResult",
    "EndSessionResult",
    "GenerateQueryResult",
    "GetAgentMemoryResult",
    "GetExecutionFlowSnapshotResult",
    "GetFlowExecutionResult",
    "GetInvocationStepResult",
    "GetSessionResult",
    "InvokeAgentResult",
    "InvokeFlowResult",
    "InvokeInlineAgentResult",
    "KnowledgeBaseQuery",
    "ListFlowExecutionEventsResult",
    "ListFlowExecutionsResult",
    "ListInvocationStepsResult",
    "ListInvocationsResult",
    "ListSessionsResult",
    "ListTagsForResourceResult",
    "OptimizePromptResult",
    "PutInvocationStepResult",
    "RerankResult",
    "RetrievalResult",
    "RetrieveAndGenerateResult",
    "RetrieveAndGenerateStreamResult",
    "RetrievedReference",
    "StartFlowExecutionResult",
    "StopFlowExecutionResult",
    "UpdateSessionResult",
    "create_invocation",
    "create_session",
    "delete_agent_memory",
    "delete_session",
    "end_session",
    "generate_query",
    "get_agent_memory",
    "get_execution_flow_snapshot",
    "get_flow_execution",
    "get_invocation_step",
    "get_session",
    "invoke_agent",
    "invoke_flow",
    "invoke_inline_agent",
    "list_flow_execution_events",
    "list_flow_executions",
    "list_invocation_steps",
    "list_invocations",
    "list_sessions",
    "list_tags_for_resource",
    "optimize_prompt",
    "put_invocation_step",
    "rerank",
    "retrieve",
    "retrieve_and_generate",
    "retrieve_and_generate_stream",
    "start_flow_execution",
    "stop_flow_execution",
    "tag_resource",
    "untag_resource",
    "update_session",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_completion_response(
    resp: dict[str, Any],
) -> tuple[str, list[Citation]]:
    """Extract completion text and citations from an agent response."""
    completion_data = resp.get("completion", [])
    parts: list[str] = []
    citations: list[Citation] = []

    if isinstance(completion_data, list):
        for event in completion_data:
            chunk = event.get("chunk") if isinstance(event, dict) else None
            if chunk:
                raw_bytes = chunk.get("bytes", b"")
                if isinstance(raw_bytes, (bytes, bytearray)):
                    parts.append(raw_bytes.decode("utf-8"))
                elif isinstance(raw_bytes, str):
                    parts.append(raw_bytes)
                attribution = chunk.get("attribution", {})
                raw_citations = attribution.get("citations", [])
                if raw_citations:
                    citations.extend(_parse_citations(raw_citations))
    elif isinstance(completion_data, (bytes, bytearray)):
        parts.append(completion_data.decode("utf-8"))
    elif isinstance(completion_data, str):
        parts.append(completion_data)

    return "".join(parts), citations


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


async def invoke_agent(
    agent_id: str,
    agent_alias_id: str,
    session_id: str,
    input_text: str,
    *,
    enable_trace: bool = False,
    end_session: bool = False,
    region_name: str | None = None,
) -> InvokeAgentResult:
    """Invoke a Bedrock agent and return the completed response.

    Streams the agent's event-based response and assembles the full
    completion text along with any citations.

    Args:
        agent_id: The unique identifier of the agent.
        agent_alias_id: The alias identifier of the agent.
        session_id: Session identifier for multi-turn conversations.
        input_text: The user's input prompt.
        enable_trace: Whether to enable trace output (default ``False``).
        end_session: Whether to end the session after this turn
            (default ``False``).
        region_name: AWS region override.

    Returns:
        An :class:`InvokeAgentResult` with the completion text and
        citations.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    try:
        resp = await client.call(
            "InvokeAgent",
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text,
            enableTrace=enable_trace,
            endSession=end_session,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"invoke_agent failed for agent {agent_id!r}") from exc

    completion, citations = _parse_completion_response(resp)

    return InvokeAgentResult(
        completion=completion,
        session_id=session_id,
        content_type=resp.get("contentType", "text/plain"),
        citations=citations,
    )


async def retrieve(
    knowledge_base_id: str,
    query: str,
    *,
    top_k: int = 5,
    next_token: str | None = None,
    region_name: str | None = None,
) -> RetrievalResult:
    """Retrieve relevant passages from a Bedrock knowledge base.

    Args:
        knowledge_base_id: The knowledge-base identifier.
        query: The natural-language query string.
        top_k: Maximum number of results to return (default ``5``).
        next_token: Pagination token for subsequent pages.
        region_name: AWS region override.

    Returns:
        A :class:`RetrievalResult` with the retrieved references.

    Raises:
        RuntimeError: If the retrieval fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {
        "knowledgeBaseId": knowledge_base_id,
        "retrievalQuery": {"text": query},
        "retrievalConfiguration": {
            "vectorSearchConfiguration": {
                "numberOfResults": top_k,
            },
        },
    }
    if next_token:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("Retrieve", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"retrieve failed for knowledge base {knowledge_base_id!r}",
        ) from exc

    references = [
        RetrievedReference(
            content=r.get("content", {}).get("text", ""),
            location=r.get("location", {}),
            score=r.get("score"),
            metadata=r.get("metadata", {}),
        )
        for r in resp.get("retrievalResults", [])
    ]
    return RetrievalResult(
        references=references,
        next_token=resp.get("nextToken"),
    )


async def retrieve_and_generate(
    input_text: str,
    knowledge_base_id: str,
    model_arn: str,
    *,
    session_id: str | None = None,
    region_name: str | None = None,
) -> RetrieveAndGenerateResult:
    """Retrieve from a knowledge base and generate a response.

    Combines retrieval-augmented generation (RAG) in a single API call,
    querying the knowledge base and feeding the results into the
    specified foundation model.

    Args:
        input_text: The user's natural-language question.
        knowledge_base_id: The knowledge-base identifier.
        model_arn: ARN of the foundation model to use for generation.
        session_id: Optional session identifier for multi-turn
            conversations.
        region_name: AWS region override.

    Returns:
        A :class:`RetrieveAndGenerateResult` with the generated answer
        and citations.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {
        "input": {"text": input_text},
        "retrieveAndGenerateConfiguration": {
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": knowledge_base_id,
                "modelArn": model_arn,
            },
        },
    }
    if session_id:
        kwargs["sessionId"] = session_id
    try:
        resp = await client.call("RetrieveAndGenerate", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "retrieve_and_generate failed") from exc

    raw_citations = resp.get("citations", [])
    citations = _parse_citations(raw_citations)
    output = resp.get("output", {})
    output_text = output.get("text", "") if isinstance(output, dict) else ""

    return RetrieveAndGenerateResult(
        output_text=output_text,
        session_id=resp.get("sessionId"),
        citations=citations,
    )


async def invoke_inline_agent(
    foundation_model: str,
    session_id: str,
    input_text: str,
    instruction: str,
    *,
    action_groups: list[dict[str, Any]] | None = None,
    knowledge_bases: list[dict[str, Any]] | None = None,
    enable_trace: bool = False,
    end_session: bool = False,
    region_name: str | None = None,
) -> InvokeInlineAgentResult:
    """Invoke an inline Bedrock agent without a pre-created agent resource.

    Inline agents let you define agent behaviour at call time by
    specifying the foundation model, instructions, action groups, and
    knowledge bases directly in the request.

    Args:
        foundation_model: The foundation model identifier.
        session_id: Session identifier for multi-turn conversations.
        input_text: The user's input prompt.
        instruction: The agent instruction/system prompt.
        action_groups: Optional list of inline action-group definitions.
        knowledge_bases: Optional list of knowledge-base configurations.
        enable_trace: Whether to enable trace output (default ``False``).
        end_session: Whether to end the session after this turn
            (default ``False``).
        region_name: AWS region override.

    Returns:
        An :class:`InvokeInlineAgentResult` with the completion text
        and citations.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {
        "foundationModel": foundation_model,
        "sessionId": session_id,
        "inputText": input_text,
        "instruction": instruction,
        "enableTrace": enable_trace,
        "endSession": end_session,
    }
    if action_groups:
        kwargs["actionGroups"] = action_groups
    if knowledge_bases:
        kwargs["knowledgeBases"] = knowledge_bases
    try:
        resp = await client.call("InvokeInlineAgent", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "invoke_inline_agent failed") from exc

    completion, citations = _parse_completion_response(resp)

    return InvokeInlineAgentResult(
        completion=completion,
        session_id=session_id,
        content_type=resp.get("contentType", "text/plain"),
        citations=citations,
    )


async def create_invocation(
    session_identifier: str,
    *,
    invocation_id: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateInvocationResult:
    """Create invocation.

    Args:
        session_identifier: Session identifier.
        invocation_id: Invocation id.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if invocation_id is not None:
        kwargs["invocationId"] = invocation_id
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("CreateInvocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create invocation") from exc
    return CreateInvocationResult(
        session_id=resp.get("sessionId"),
        invocation_id=resp.get("invocationId"),
        created_at=resp.get("createdAt"),
    )


async def create_session(
    *,
    session_metadata: dict[str, Any] | None = None,
    encryption_key_arn: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateSessionResult:
    """Create session.

    Args:
        session_metadata: Session metadata.
        encryption_key_arn: Encryption key arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if session_metadata is not None:
        kwargs["sessionMetadata"] = session_metadata
    if encryption_key_arn is not None:
        kwargs["encryptionKeyArn"] = encryption_key_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create session") from exc
    return CreateSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
        created_at=resp.get("createdAt"),
    )


async def delete_agent_memory(
    agent_id: str,
    agent_alias_id: str,
    *,
    memory_id: str | None = None,
    session_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete agent memory.

    Args:
        agent_id: Agent id.
        agent_alias_id: Agent alias id.
        memory_id: Memory id.
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    if memory_id is not None:
        kwargs["memoryId"] = memory_id
    if session_id is not None:
        kwargs["sessionId"] = session_id
    try:
        await client.call("DeleteAgentMemory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete agent memory") from exc
    return None


async def delete_session(
    session_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete session.

    Args:
        session_identifier: Session identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        await client.call("DeleteSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete session") from exc
    return None


async def end_session(
    session_identifier: str,
    region_name: str | None = None,
) -> EndSessionResult:
    """End session.

    Args:
        session_identifier: Session identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = await client.call("EndSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to end session") from exc
    return EndSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
    )


async def generate_query(
    query_generation_input: dict[str, Any],
    transformation_configuration: dict[str, Any],
    region_name: str | None = None,
) -> GenerateQueryResult:
    """Generate query.

    Args:
        query_generation_input: Query generation input.
        transformation_configuration: Transformation configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryGenerationInput"] = query_generation_input
    kwargs["transformationConfiguration"] = transformation_configuration
    try:
        resp = await client.call("GenerateQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate query") from exc
    return GenerateQueryResult(
        queries=resp.get("queries"),
    )


async def get_agent_memory(
    agent_id: str,
    agent_alias_id: str,
    memory_type: str,
    memory_id: str,
    *,
    next_token: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> GetAgentMemoryResult:
    """Get agent memory.

    Args:
        agent_id: Agent id.
        agent_alias_id: Agent alias id.
        memory_type: Memory type.
        memory_id: Memory id.
        next_token: Next token.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    kwargs["memoryType"] = memory_type
    kwargs["memoryId"] = memory_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_items is not None:
        kwargs["maxItems"] = max_items
    try:
        resp = await client.call("GetAgentMemory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get agent memory") from exc
    return GetAgentMemoryResult(
        next_token=resp.get("nextToken"),
        memory_contents=resp.get("memoryContents"),
    )


async def get_execution_flow_snapshot(
    flow_identifier: str,
    flow_alias_identifier: str,
    execution_identifier: str,
    region_name: str | None = None,
) -> GetExecutionFlowSnapshotResult:
    """Get execution flow snapshot.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        execution_identifier: Execution identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = await client.call("GetExecutionFlowSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get execution flow snapshot") from exc
    return GetExecutionFlowSnapshotResult(
        flow_identifier=resp.get("flowIdentifier"),
        flow_alias_identifier=resp.get("flowAliasIdentifier"),
        flow_version=resp.get("flowVersion"),
        execution_role_arn=resp.get("executionRoleArn"),
        definition=resp.get("definition"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
    )


async def get_flow_execution(
    flow_identifier: str,
    flow_alias_identifier: str,
    execution_identifier: str,
    region_name: str | None = None,
) -> GetFlowExecutionResult:
    """Get flow execution.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        execution_identifier: Execution identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = await client.call("GetFlowExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get flow execution") from exc
    return GetFlowExecutionResult(
        execution_arn=resp.get("executionArn"),
        status=resp.get("status"),
        started_at=resp.get("startedAt"),
        ended_at=resp.get("endedAt"),
        errors=resp.get("errors"),
        flow_alias_identifier=resp.get("flowAliasIdentifier"),
        flow_identifier=resp.get("flowIdentifier"),
        flow_version=resp.get("flowVersion"),
    )


async def get_invocation_step(
    invocation_identifier: str,
    invocation_step_id: str,
    session_identifier: str,
    region_name: str | None = None,
) -> GetInvocationStepResult:
    """Get invocation step.

    Args:
        invocation_identifier: Invocation identifier.
        invocation_step_id: Invocation step id.
        session_identifier: Session identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["invocationIdentifier"] = invocation_identifier
    kwargs["invocationStepId"] = invocation_step_id
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = await client.call("GetInvocationStep", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get invocation step") from exc
    return GetInvocationStepResult(
        invocation_step=resp.get("invocationStep"),
    )


async def get_session(
    session_identifier: str,
    region_name: str | None = None,
) -> GetSessionResult:
    """Get session.

    Args:
        session_identifier: Session identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = await client.call("GetSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get session") from exc
    return GetSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
        session_metadata=resp.get("sessionMetadata"),
        encryption_key_arn=resp.get("encryptionKeyArn"),
    )


async def invoke_flow(
    flow_identifier: str,
    flow_alias_identifier: str,
    inputs: list[dict[str, Any]],
    *,
    enable_trace: bool | None = None,
    model_performance_configuration: dict[str, Any] | None = None,
    execution_id: str | None = None,
    region_name: str | None = None,
) -> InvokeFlowResult:
    """Invoke flow.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        inputs: Inputs.
        enable_trace: Enable trace.
        model_performance_configuration: Model performance configuration.
        execution_id: Execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["inputs"] = inputs
    if enable_trace is not None:
        kwargs["enableTrace"] = enable_trace
    if model_performance_configuration is not None:
        kwargs["modelPerformanceConfiguration"] = model_performance_configuration
    if execution_id is not None:
        kwargs["executionId"] = execution_id
    try:
        resp = await client.call("InvokeFlow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to invoke flow") from exc
    return InvokeFlowResult(
        response_stream=resp.get("responseStream"),
        execution_id=resp.get("executionId"),
    )


async def list_flow_execution_events(
    flow_identifier: str,
    flow_alias_identifier: str,
    execution_identifier: str,
    event_type: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFlowExecutionEventsResult:
    """List flow execution events.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        execution_identifier: Execution identifier.
        event_type: Event type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    kwargs["eventType"] = event_type
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListFlowExecutionEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list flow execution events") from exc
    return ListFlowExecutionEventsResult(
        flow_execution_events=resp.get("flowExecutionEvents"),
        next_token=resp.get("nextToken"),
    )


async def list_flow_executions(
    flow_identifier: str,
    *,
    flow_alias_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFlowExecutionsResult:
    """List flow executions.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if flow_alias_identifier is not None:
        kwargs["flowAliasIdentifier"] = flow_alias_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListFlowExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list flow executions") from exc
    return ListFlowExecutionsResult(
        flow_execution_summaries=resp.get("flowExecutionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_invocation_steps(
    session_identifier: str,
    *,
    invocation_identifier: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInvocationStepsResult:
    """List invocation steps.

    Args:
        session_identifier: Session identifier.
        invocation_identifier: Invocation identifier.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if invocation_identifier is not None:
        kwargs["invocationIdentifier"] = invocation_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListInvocationSteps", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list invocation steps") from exc
    return ListInvocationStepsResult(
        invocation_step_summaries=resp.get("invocationStepSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_invocations(
    session_identifier: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInvocationsResult:
    """List invocations.

    Args:
        session_identifier: Session identifier.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListInvocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list invocations") from exc
    return ListInvocationsResult(
        invocation_summaries=resp.get("invocationSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_sessions(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSessionsResult:
    """List sessions.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sessions") from exc
    return ListSessionsResult(
        session_summaries=resp.get("sessionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def optimize_prompt(
    input: dict[str, Any],
    target_model_id: str,
    region_name: str | None = None,
) -> OptimizePromptResult:
    """Optimize prompt.

    Args:
        input: Input.
        target_model_id: Target model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["input"] = input
    kwargs["targetModelId"] = target_model_id
    try:
        resp = await client.call("OptimizePrompt", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to optimize prompt") from exc
    return OptimizePromptResult(
        optimized_prompt=resp.get("optimizedPrompt"),
    )


async def put_invocation_step(
    session_identifier: str,
    invocation_identifier: str,
    invocation_step_time: str,
    payload: dict[str, Any],
    *,
    invocation_step_id: str | None = None,
    region_name: str | None = None,
) -> PutInvocationStepResult:
    """Put invocation step.

    Args:
        session_identifier: Session identifier.
        invocation_identifier: Invocation identifier.
        invocation_step_time: Invocation step time.
        payload: Payload.
        invocation_step_id: Invocation step id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    kwargs["invocationIdentifier"] = invocation_identifier
    kwargs["invocationStepTime"] = invocation_step_time
    kwargs["payload"] = payload
    if invocation_step_id is not None:
        kwargs["invocationStepId"] = invocation_step_id
    try:
        resp = await client.call("PutInvocationStep", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put invocation step") from exc
    return PutInvocationStepResult(
        invocation_step_id=resp.get("invocationStepId"),
    )


async def rerank(
    queries: list[dict[str, Any]],
    sources: list[dict[str, Any]],
    reranking_configuration: dict[str, Any],
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> RerankResult:
    """Rerank.

    Args:
        queries: Queries.
        sources: Sources.
        reranking_configuration: Reranking configuration.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queries"] = queries
    kwargs["sources"] = sources
    kwargs["rerankingConfiguration"] = reranking_configuration
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("Rerank", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to rerank") from exc
    return RerankResult(
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


async def retrieve_and_generate_stream(
    input: dict[str, Any],
    *,
    session_id: str | None = None,
    retrieve_and_generate_configuration: dict[str, Any] | None = None,
    session_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RetrieveAndGenerateStreamResult:
    """Retrieve and generate stream.

    Args:
        input: Input.
        session_id: Session id.
        retrieve_and_generate_configuration: Retrieve and generate configuration.
        session_configuration: Session configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["input"] = input
    if session_id is not None:
        kwargs["sessionId"] = session_id
    if retrieve_and_generate_configuration is not None:
        kwargs["retrieveAndGenerateConfiguration"] = retrieve_and_generate_configuration
    if session_configuration is not None:
        kwargs["sessionConfiguration"] = session_configuration
    try:
        resp = await client.call("RetrieveAndGenerateStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to retrieve and generate stream") from exc
    return RetrieveAndGenerateStreamResult(
        stream=resp.get("stream"),
        session_id=resp.get("sessionId"),
    )


async def start_flow_execution(
    flow_identifier: str,
    flow_alias_identifier: str,
    inputs: list[dict[str, Any]],
    *,
    flow_execution_name: str | None = None,
    model_performance_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartFlowExecutionResult:
    """Start flow execution.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        inputs: Inputs.
        flow_execution_name: Flow execution name.
        model_performance_configuration: Model performance configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["inputs"] = inputs
    if flow_execution_name is not None:
        kwargs["flowExecutionName"] = flow_execution_name
    if model_performance_configuration is not None:
        kwargs["modelPerformanceConfiguration"] = model_performance_configuration
    try:
        resp = await client.call("StartFlowExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start flow execution") from exc
    return StartFlowExecutionResult(
        execution_arn=resp.get("executionArn"),
    )


async def stop_flow_execution(
    flow_identifier: str,
    flow_alias_identifier: str,
    execution_identifier: str,
    region_name: str | None = None,
) -> StopFlowExecutionResult:
    """Stop flow execution.

    Args:
        flow_identifier: Flow identifier.
        flow_alias_identifier: Flow alias identifier.
        execution_identifier: Execution identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = await client.call("StopFlowExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop flow execution") from exc
    return StopFlowExecutionResult(
        execution_arn=resp.get("executionArn"),
        status=resp.get("status"),
    )


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
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
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_session(
    session_identifier: str,
    *,
    session_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateSessionResult:
    """Update session.

    Args:
        session_identifier: Session identifier.
        session_metadata: Session metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if session_metadata is not None:
        kwargs["sessionMetadata"] = session_metadata
    try:
        resp = await client.call("UpdateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update session") from exc
    return UpdateSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )
