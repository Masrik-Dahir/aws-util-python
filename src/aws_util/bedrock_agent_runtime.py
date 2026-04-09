"""aws_util.bedrock_agent_runtime — Bedrock Agent Runtime utilities.

Provides high-level helpers for invoking Bedrock agents, retrieving
from knowledge bases, and performing retrieval-augmented generation
(RAG) via the ``bedrock-agent-runtime`` service.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
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
# Models
# ---------------------------------------------------------------------------


class RetrievedReference(BaseModel):
    """A single reference retrieved from a knowledge base."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    content: str = ""
    location: dict[str, Any] = {}
    score: float | None = None
    metadata: dict[str, Any] = {}


class Citation(BaseModel):
    """A citation linking generated text to retrieved references."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    generated_response_part: dict[str, Any] = {}
    retrieved_references: list[RetrievedReference] = []


class InvokeAgentResult(BaseModel):
    """The response from invoking a Bedrock agent."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    completion: str
    session_id: str
    content_type: str = "text/plain"
    citations: list[Citation] = []


class RetrievalResult(BaseModel):
    """The response from a knowledge-base retrieval query."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    references: list[RetrievedReference] = []
    next_token: str | None = None


class KnowledgeBaseQuery(BaseModel):
    """Input query configuration for knowledge-base retrieval."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    text: str
    top_k: int = 5
    search_type: str = "SEMANTIC"


class RetrieveAndGenerateResult(BaseModel):
    """The response from a retrieve-and-generate call."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    output_text: str
    session_id: str | None = None
    citations: list[Citation] = []


class InvokeInlineAgentResult(BaseModel):
    """The response from invoking an inline Bedrock agent."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    completion: str
    session_id: str
    content_type: str = "text/plain"
    citations: list[Citation] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_citations(raw_citations: list[dict[str, Any]]) -> list[Citation]:
    """Parse raw citation dicts into :class:`Citation` models."""
    citations: list[Citation] = []
    for raw in raw_citations:
        refs = [
            RetrievedReference(
                content=ref.get("content", {}).get("text", ""),
                location=ref.get("location", {}),
                score=ref.get("score"),
                metadata=ref.get("metadata", {}),
            )
            for ref in raw.get("retrievedReferences", [])
        ]
        citations.append(
            Citation(
                generated_response_part=raw.get("generatedResponsePart", {}),
                retrieved_references=refs,
            )
        )
    return citations


def _read_event_stream(event_stream: Any) -> tuple[str, list[Citation]]:
    """Read an agent event stream and return (completion_text, citations)."""
    parts: list[str] = []
    citations: list[Citation] = []
    for event in event_stream:
        chunk = event.get("chunk")
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
    return "".join(parts), citations


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def invoke_agent(
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
    client = get_client("bedrock-agent-runtime", region_name)
    try:
        resp = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text,
            enableTrace=enable_trace,
            endSession=end_session,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"invoke_agent failed for agent {agent_id!r}") from exc

    completion, citations = _read_event_stream(resp.get("completion", []))

    return InvokeAgentResult(
        completion=completion,
        session_id=session_id,
        content_type=resp.get("contentType", "text/plain"),
        citations=citations,
    )


def retrieve(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.retrieve(**kwargs)
    except ClientError as exc:
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


def retrieve_and_generate(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.retrieve_and_generate(**kwargs)
    except ClientError as exc:
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


def invoke_inline_agent(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.invoke_inline_agent(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "invoke_inline_agent failed") from exc

    completion, citations = _read_event_stream(resp.get("completion", []))

    return InvokeInlineAgentResult(
        completion=completion,
        session_id=session_id,
        content_type=resp.get("contentType", "text/plain"),
        citations=citations,
    )


class CreateInvocationResult(BaseModel):
    """Result of create_invocation."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    invocation_id: str | None = None
    created_at: str | None = None


class CreateSessionResult(BaseModel):
    """Result of create_session."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    session_arn: str | None = None
    session_status: str | None = None
    created_at: str | None = None


class EndSessionResult(BaseModel):
    """Result of end_session."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    session_arn: str | None = None
    session_status: str | None = None


class GenerateQueryResult(BaseModel):
    """Result of generate_query."""

    model_config = ConfigDict(frozen=True)

    queries: list[dict[str, Any]] | None = None


class GetAgentMemoryResult(BaseModel):
    """Result of get_agent_memory."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    memory_contents: list[dict[str, Any]] | None = None


class GetExecutionFlowSnapshotResult(BaseModel):
    """Result of get_execution_flow_snapshot."""

    model_config = ConfigDict(frozen=True)

    flow_identifier: str | None = None
    flow_alias_identifier: str | None = None
    flow_version: str | None = None
    execution_role_arn: str | None = None
    definition: str | None = None
    customer_encryption_key_arn: str | None = None


class GetFlowExecutionResult(BaseModel):
    """Result of get_flow_execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str | None = None
    status: str | None = None
    started_at: str | None = None
    ended_at: str | None = None
    errors: list[dict[str, Any]] | None = None
    flow_alias_identifier: str | None = None
    flow_identifier: str | None = None
    flow_version: str | None = None


class GetInvocationStepResult(BaseModel):
    """Result of get_invocation_step."""

    model_config = ConfigDict(frozen=True)

    invocation_step: dict[str, Any] | None = None


class GetSessionResult(BaseModel):
    """Result of get_session."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    session_arn: str | None = None
    session_status: str | None = None
    created_at: str | None = None
    last_updated_at: str | None = None
    session_metadata: dict[str, Any] | None = None
    encryption_key_arn: str | None = None


class InvokeFlowResult(BaseModel):
    """Result of invoke_flow."""

    model_config = ConfigDict(frozen=True)

    response_stream: dict[str, Any] | None = None
    execution_id: str | None = None


class ListFlowExecutionEventsResult(BaseModel):
    """Result of list_flow_execution_events."""

    model_config = ConfigDict(frozen=True)

    flow_execution_events: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlowExecutionsResult(BaseModel):
    """Result of list_flow_executions."""

    model_config = ConfigDict(frozen=True)

    flow_execution_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInvocationStepsResult(BaseModel):
    """Result of list_invocation_steps."""

    model_config = ConfigDict(frozen=True)

    invocation_step_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInvocationsResult(BaseModel):
    """Result of list_invocations."""

    model_config = ConfigDict(frozen=True)

    invocation_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSessionsResult(BaseModel):
    """Result of list_sessions."""

    model_config = ConfigDict(frozen=True)

    session_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class OptimizePromptResult(BaseModel):
    """Result of optimize_prompt."""

    model_config = ConfigDict(frozen=True)

    optimized_prompt: dict[str, Any] | None = None


class PutInvocationStepResult(BaseModel):
    """Result of put_invocation_step."""

    model_config = ConfigDict(frozen=True)

    invocation_step_id: str | None = None


class RerankResult(BaseModel):
    """Result of rerank."""

    model_config = ConfigDict(frozen=True)

    results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class RetrieveAndGenerateStreamResult(BaseModel):
    """Result of retrieve_and_generate_stream."""

    model_config = ConfigDict(frozen=True)

    stream: dict[str, Any] | None = None
    session_id: str | None = None


class StartFlowExecutionResult(BaseModel):
    """Result of start_flow_execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str | None = None


class StopFlowExecutionResult(BaseModel):
    """Result of stop_flow_execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str | None = None
    status: str | None = None


class UpdateSessionResult(BaseModel):
    """Result of update_session."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    session_arn: str | None = None
    session_status: str | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


def create_invocation(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if invocation_id is not None:
        kwargs["invocationId"] = invocation_id
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_invocation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create invocation") from exc
    return CreateInvocationResult(
        session_id=resp.get("sessionId"),
        invocation_id=resp.get("invocationId"),
        created_at=resp.get("createdAt"),
    )


def create_session(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if session_metadata is not None:
        kwargs["sessionMetadata"] = session_metadata
    if encryption_key_arn is not None:
        kwargs["encryptionKeyArn"] = encryption_key_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create session") from exc
    return CreateSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
        created_at=resp.get("createdAt"),
    )


def delete_agent_memory(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    if memory_id is not None:
        kwargs["memoryId"] = memory_id
    if session_id is not None:
        kwargs["sessionId"] = session_id
    try:
        client.delete_agent_memory(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete agent memory") from exc
    return None


def delete_session(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        client.delete_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete session") from exc
    return None


def end_session(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = client.end_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to end session") from exc
    return EndSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
    )


def generate_query(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryGenerationInput"] = query_generation_input
    kwargs["transformationConfiguration"] = transformation_configuration
    try:
        resp = client.generate_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to generate query") from exc
    return GenerateQueryResult(
        queries=resp.get("queries"),
    )


def get_agent_memory(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.get_agent_memory(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent memory") from exc
    return GetAgentMemoryResult(
        next_token=resp.get("nextToken"),
        memory_contents=resp.get("memoryContents"),
    )


def get_execution_flow_snapshot(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = client.get_execution_flow_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get execution flow snapshot") from exc
    return GetExecutionFlowSnapshotResult(
        flow_identifier=resp.get("flowIdentifier"),
        flow_alias_identifier=resp.get("flowAliasIdentifier"),
        flow_version=resp.get("flowVersion"),
        execution_role_arn=resp.get("executionRoleArn"),
        definition=resp.get("definition"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
    )


def get_flow_execution(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = client.get_flow_execution(**kwargs)
    except ClientError as exc:
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


def get_invocation_step(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["invocationIdentifier"] = invocation_identifier
    kwargs["invocationStepId"] = invocation_step_id
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = client.get_invocation_step(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get invocation step") from exc
    return GetInvocationStepResult(
        invocation_step=resp.get("invocationStep"),
    )


def get_session(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    try:
        resp = client.get_session(**kwargs)
    except ClientError as exc:
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


def invoke_flow(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.invoke_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to invoke flow") from exc
    return InvokeFlowResult(
        response_stream=resp.get("responseStream"),
        execution_id=resp.get("executionId"),
    )


def list_flow_execution_events(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
        resp = client.list_flow_execution_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flow execution events") from exc
    return ListFlowExecutionEventsResult(
        flow_execution_events=resp.get("flowExecutionEvents"),
        next_token=resp.get("nextToken"),
    )


def list_flow_executions(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if flow_alias_identifier is not None:
        kwargs["flowAliasIdentifier"] = flow_alias_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_flow_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flow executions") from exc
    return ListFlowExecutionsResult(
        flow_execution_summaries=resp.get("flowExecutionSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_invocation_steps(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if invocation_identifier is not None:
        kwargs["invocationIdentifier"] = invocation_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_invocation_steps(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list invocation steps") from exc
    return ListInvocationStepsResult(
        invocation_step_summaries=resp.get("invocationStepSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_invocations(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_invocations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list invocations") from exc
    return ListInvocationsResult(
        invocation_summaries=resp.get("invocationSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_sessions(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_sessions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list sessions") from exc
    return ListSessionsResult(
        session_summaries=resp.get("sessionSummaries"),
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def optimize_prompt(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["input"] = input
    kwargs["targetModelId"] = target_model_id
    try:
        resp = client.optimize_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to optimize prompt") from exc
    return OptimizePromptResult(
        optimized_prompt=resp.get("optimizedPrompt"),
    )


def put_invocation_step(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    kwargs["invocationIdentifier"] = invocation_identifier
    kwargs["invocationStepTime"] = invocation_step_time
    kwargs["payload"] = payload
    if invocation_step_id is not None:
        kwargs["invocationStepId"] = invocation_step_id
    try:
        resp = client.put_invocation_step(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put invocation step") from exc
    return PutInvocationStepResult(
        invocation_step_id=resp.get("invocationStepId"),
    )


def rerank(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queries"] = queries
    kwargs["sources"] = sources
    kwargs["rerankingConfiguration"] = reranking_configuration
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.rerank(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rerank") from exc
    return RerankResult(
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


def retrieve_and_generate_stream(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["input"] = input
    if session_id is not None:
        kwargs["sessionId"] = session_id
    if retrieve_and_generate_configuration is not None:
        kwargs["retrieveAndGenerateConfiguration"] = retrieve_and_generate_configuration
    if session_configuration is not None:
        kwargs["sessionConfiguration"] = session_configuration
    try:
        resp = client.retrieve_and_generate_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to retrieve and generate stream") from exc
    return RetrieveAndGenerateStreamResult(
        stream=resp.get("stream"),
        session_id=resp.get("sessionId"),
    )


def start_flow_execution(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["inputs"] = inputs
    if flow_execution_name is not None:
        kwargs["flowExecutionName"] = flow_execution_name
    if model_performance_configuration is not None:
        kwargs["modelPerformanceConfiguration"] = model_performance_configuration
    try:
        resp = client.start_flow_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start flow execution") from exc
    return StartFlowExecutionResult(
        execution_arn=resp.get("executionArn"),
    )


def stop_flow_execution(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowAliasIdentifier"] = flow_alias_identifier
    kwargs["executionIdentifier"] = execution_identifier
    try:
        resp = client.stop_flow_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop flow execution") from exc
    return StopFlowExecutionResult(
        execution_arn=resp.get("executionArn"),
        status=resp.get("status"),
    )


def tag_resource(
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
    client = get_client("bedrock-agent-runtime", region_name)
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_session(
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
    client = get_client("bedrock-agent-runtime", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sessionIdentifier"] = session_identifier
    if session_metadata is not None:
        kwargs["sessionMetadata"] = session_metadata
    try:
        resp = client.update_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update session") from exc
    return UpdateSessionResult(
        session_id=resp.get("sessionId"),
        session_arn=resp.get("sessionArn"),
        session_status=resp.get("sessionStatus"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )
