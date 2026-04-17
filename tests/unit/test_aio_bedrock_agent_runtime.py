

"""Tests for aws_util.aio.bedrock_agent_runtime — native async module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.bedrock_agent_runtime as mod
from aws_util.aio.bedrock_agent_runtime import (

    Citation,
    InvokeAgentResult,
    InvokeInlineAgentResult,
    KnowledgeBaseQuery,
    RetrievalResult,
    RetrieveAndGenerateResult,
    RetrievedReference,
    invoke_agent,
    invoke_inline_agent,
    retrieve,
    retrieve_and_generate,
    create_invocation,
    create_session,
    delete_agent_memory,
    delete_session,
    end_session,
    generate_query,
    get_agent_memory,
    get_execution_flow_snapshot,
    get_flow_execution,
    get_invocation_step,
    get_session,
    invoke_flow,
    list_flow_execution_events,
    list_flow_executions,
    list_invocation_steps,
    list_invocations,
    list_sessions,
    list_tags_for_resource,
    optimize_prompt,
    put_invocation_step,
    rerank,
    retrieve_and_generate_stream,
    start_flow_execution,
    stop_flow_execution,
    tag_resource,
    untag_resource,
    update_session,
    _parse_completion_response,
)

AGENT_ID = "AGENT123"
ALIAS_ID = "ALIAS456"
SESSION_ID = "sess-001"
KB_ID = "KB789"
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent_runtime.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# _parse_completion_response
# ---------------------------------------------------------------------------


def test_parse_completion_response_list_events():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {
        "completion": [
            {"chunk": {"bytes": b"Hello "}},
            {"chunk": {"bytes": b"world"}},
        ],
    }
    text, citations = _parse_completion_response(resp)
    assert text == "Hello world"
    assert citations == []


def test_parse_completion_response_string_bytes():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {
        "completion": [{"chunk": {"bytes": "text content"}}],
    }
    text, citations = _parse_completion_response(resp)
    assert text == "text content"


def test_parse_completion_response_with_citations():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {
        "completion": [
            {
                "chunk": {
                    "bytes": b"Answer",
                    "attribution": {
                        "citations": [
                            {
                                "generatedResponsePart": {},
                                "retrievedReferences": [
                                    {"content": {"text": "ref"}, "score": 0.8},
                                ],
                            },
                        ],
                    },
                },
            },
        ],
    }
    text, citations = _parse_completion_response(resp)
    assert text == "Answer"
    assert len(citations) == 1


def test_parse_completion_response_bytes_type():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {"completion": b"raw bytes"}
    text, citations = _parse_completion_response(resp)
    assert text == "raw bytes"
    assert citations == []


def test_parse_completion_response_string_type():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {"completion": "raw string"}
    text, citations = _parse_completion_response(resp)
    assert text == "raw string"
    assert citations == []


def test_parse_completion_response_empty():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {"completion": []}
    text, citations = _parse_completion_response(resp)
    assert text == ""
    assert citations == []


def test_parse_completion_response_no_chunk():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {"completion": [{"trace": {"data": "info"}}]}
    text, citations = _parse_completion_response(resp)
    assert text == ""


def test_parse_completion_response_non_dict_event():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {"completion": ["not a dict"]}
    text, citations = _parse_completion_response(resp)
    assert text == ""


REGION = "us-east-1"

def test_parse_completion_response_missing_key():
    from aws_util.aio.bedrock_agent_runtime import _parse_completion_response

    resp = {}
    text, citations = _parse_completion_response(resp)
    assert text == ""
    assert citations == []


# ---------------------------------------------------------------------------
# invoke_agent
# ---------------------------------------------------------------------------


async def test_invoke_agent_success(mock_client):
    mock_client.call.return_value = {
        "completion": [
            {"chunk": {"bytes": b"Agent says hello"}},
        ],
        "contentType": "text/plain",
    }
    result = await invoke_agent(AGENT_ID, ALIAS_ID, SESSION_ID, "Hi")
    assert isinstance(result, InvokeAgentResult)
    assert result.completion == "Agent says hello"
    assert result.session_id == SESSION_ID
    assert result.content_type == "text/plain"

async def test_invoke_agent_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="invoke_agent failed"):
        await invoke_agent(AGENT_ID, ALIAS_ID, SESSION_ID, "Hi")


async def test_invoke_agent_empty_completion(mock_client):
    mock_client.call.return_value = {"completion": []}
    result = await invoke_agent(AGENT_ID, ALIAS_ID, SESSION_ID, "Hi")
    assert result.completion == ""


async def test_invoke_agent_default_content_type(mock_client):
    mock_client.call.return_value = {"completion": []}
    result = await invoke_agent(AGENT_ID, ALIAS_ID, SESSION_ID, "Hi")
    assert result.content_type == "text/plain"


# ---------------------------------------------------------------------------
# retrieve
# ---------------------------------------------------------------------------


async def test_retrieve_success(mock_client):
    mock_client.call.return_value = {
        "retrievalResults": [
            {
                "content": {"text": "Passage 1"},
                "location": {"type": "S3"},
                "score": 0.95,
                "metadata": {"doc": "a.pdf"},
            },
        ],
    }
    result = await retrieve(KB_ID, "What is X?")
    assert isinstance(result, RetrievalResult)
    assert len(result.references) == 1
    assert result.references[0].content == "Passage 1"
    assert result.references[0].score == 0.95
    assert result.next_token is None


async def test_retrieve_with_pagination(mock_client):
    mock_client.call.return_value = {
        "retrievalResults": [],
        "nextToken": "tok-2",
    }
    result = await retrieve(KB_ID, "Q?", next_token="tok-1")
    assert result.next_token == "tok-2"
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["nextToken"] == "tok-1"


async def test_retrieve_custom_top_k(mock_client):
    mock_client.call.return_value = {"retrievalResults": []}
    await retrieve(KB_ID, "Q?", top_k=20)
    call_kwargs = mock_client.call.call_args[1]
    config = call_kwargs["retrievalConfiguration"]["vectorSearchConfiguration"]
    assert config["numberOfResults"] == 20


async def test_retrieve_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="retrieve failed"):
        await retrieve(KB_ID, "Q?")


async def test_retrieve_empty_results(mock_client):
    mock_client.call.return_value = {"retrievalResults": []}
    result = await retrieve(KB_ID, "Q?")
    assert result.references == []


async def test_retrieve_missing_content_fields(mock_client):
    mock_client.call.return_value = {"retrievalResults": [{}]}
    result = await retrieve(KB_ID, "Q?")
    assert result.references[0].content == ""
    assert result.references[0].score is None


# ---------------------------------------------------------------------------
# retrieve_and_generate
# ---------------------------------------------------------------------------


async def test_retrieve_and_generate_success(mock_client):
    mock_client.call.return_value = {
        "output": {"text": "Generated answer"},
        "sessionId": "rag-sess-1",
        "citations": [],
    }
    result = await retrieve_and_generate("What is X?", KB_ID, MODEL_ARN)
    assert isinstance(result, RetrieveAndGenerateResult)
    assert result.output_text == "Generated answer"
    assert result.session_id == "rag-sess-1"


async def test_retrieve_and_generate_with_session(mock_client):
    mock_client.call.return_value = {
        "output": {"text": "ok"},
        "sessionId": "s1",
        "citations": [],
    }
    await retrieve_and_generate(
        "Q?", KB_ID, MODEL_ARN, session_id="s1"
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["sessionId"] == "s1"


async def test_retrieve_and_generate_with_citations(mock_client):
    mock_client.call.return_value = {
        "output": {"text": "Answer"},
        "citations": [
            {
                "generatedResponsePart": {},
                "retrievedReferences": [
                    {"content": {"text": "Source"}, "score": 0.85},
                ],
            },
        ],
    }
    result = await retrieve_and_generate("Q?", KB_ID, MODEL_ARN)
    assert len(result.citations) == 1
    assert result.citations[0].retrieved_references[0].content == "Source"


async def test_retrieve_and_generate_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="retrieve_and_generate failed"):
        await retrieve_and_generate("Q?", KB_ID, MODEL_ARN)


async def test_retrieve_and_generate_non_dict_output(mock_client):
    mock_client.call.return_value = {
        "output": "not a dict",
        "citations": [],
    }
    result = await retrieve_and_generate("Q?", KB_ID, MODEL_ARN)
    assert result.output_text == ""


async def test_retrieve_and_generate_missing_output(mock_client):
    mock_client.call.return_value = {"citations": []}
    result = await retrieve_and_generate("Q?", KB_ID, MODEL_ARN)
    assert result.output_text == ""


# ---------------------------------------------------------------------------
# invoke_inline_agent
# ---------------------------------------------------------------------------


async def test_invoke_inline_agent_success(mock_client):
    mock_client.call.return_value = {
        "completion": [
            {"chunk": {"bytes": b"Inline response"}},
        ],
        "contentType": "text/plain",
    }
    result = await invoke_inline_agent(
        "anthropic.claude-v2", SESSION_ID, "Hello", "You are helpful"
    )
    assert isinstance(result, InvokeInlineAgentResult)
    assert result.completion == "Inline response"
    assert result.session_id == SESSION_ID


async def test_invoke_inline_agent_with_action_groups(mock_client):
    mock_client.call.return_value = {
        "completion": [{"chunk": {"bytes": b"ok"}}],
    }
    action_groups = [{"actionGroupName": "MyAction"}]
    await invoke_inline_agent(
        "model",
        SESSION_ID,
        "Hi",
        "instr",
        action_groups=action_groups,
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["actionGroups"] == action_groups


async def test_invoke_inline_agent_with_knowledge_bases(mock_client):
    mock_client.call.return_value = {
        "completion": [{"chunk": {"bytes": b"ok"}}],
    }
    kbs = [{"knowledgeBaseId": KB_ID}]
    await invoke_inline_agent(
        "model",
        SESSION_ID,
        "Hi",
        "instr",
        knowledge_bases=kbs,
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["knowledgeBases"] == kbs

async def test_invoke_inline_agent_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="invoke_inline_agent failed"):
        await invoke_inline_agent(
            "model", SESSION_ID, "Hi", "instr"
        )


async def test_invoke_inline_agent_empty_completion(mock_client):
    mock_client.call.return_value = {"completion": []}
    result = await invoke_inline_agent(
        "model", SESSION_ID, "Hi", "instr"
    )
    assert result.completion == ""


async def test_invoke_inline_agent_default_content_type(mock_client):
    mock_client.call.return_value = {"completion": []}
    result = await invoke_inline_agent(
        "model", SESSION_ID, "Hi", "instr"
    )
    assert result.content_type == "text/plain"


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    assert "invoke_agent" in mod.__all__
    assert "retrieve" in mod.__all__
    assert "retrieve_and_generate" in mod.__all__
    assert "invoke_inline_agent" in mod.__all__
    assert "InvokeAgentResult" in mod.__all__
    assert "RetrievalResult" in mod.__all__
    assert "RetrieveAndGenerateResult" in mod.__all__
    assert "InvokeInlineAgentResult" in mod.__all__
    assert "RetrievedReference" in mod.__all__
    assert "Citation" in mod.__all__
    assert "KnowledgeBaseQuery" in mod.__all__


async def test_create_invocation(mock_client):
    mock_client.call.return_value = {}
    await create_invocation("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_create_invocation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_invocation("test-session_identifier", )


async def test_create_invocation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create invocation"):
        await create_invocation("test-session_identifier", )


async def test_create_session(mock_client):
    mock_client.call.return_value = {}
    await create_session()
    mock_client.call.assert_called_once()


async def test_create_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_session()


async def test_create_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create session"):
        await create_session()


async def test_delete_agent_memory(mock_client):
    mock_client.call.return_value = {}
    await delete_agent_memory("test-agent_id", "test-agent_alias_id", )
    mock_client.call.assert_called_once()


async def test_delete_agent_memory_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_agent_memory("test-agent_id", "test-agent_alias_id", )


async def test_delete_agent_memory_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete agent memory"):
        await delete_agent_memory("test-agent_id", "test-agent_alias_id", )


async def test_delete_session(mock_client):
    mock_client.call.return_value = {}
    await delete_session("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_session("test-session_identifier", )


async def test_delete_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete session"):
        await delete_session("test-session_identifier", )


async def test_end_session(mock_client):
    mock_client.call.return_value = {}
    await end_session("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_end_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await end_session("test-session_identifier", )


async def test_end_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to end session"):
        await end_session("test-session_identifier", )


async def test_generate_query(mock_client):
    mock_client.call.return_value = {}
    await generate_query({}, {}, )
    mock_client.call.assert_called_once()


async def test_generate_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await generate_query({}, {}, )


async def test_generate_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to generate query"):
        await generate_query({}, {}, )


async def test_get_agent_memory(mock_client):
    mock_client.call.return_value = {}
    await get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", )
    mock_client.call.assert_called_once()


async def test_get_agent_memory_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", )


async def test_get_agent_memory_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get agent memory"):
        await get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", )


async def test_get_execution_flow_snapshot(mock_client):
    mock_client.call.return_value = {}
    await get_execution_flow_snapshot("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )
    mock_client.call.assert_called_once()


async def test_get_execution_flow_snapshot_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_execution_flow_snapshot("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_get_execution_flow_snapshot_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get execution flow snapshot"):
        await get_execution_flow_snapshot("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_get_flow_execution(mock_client):
    mock_client.call.return_value = {}
    await get_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )
    mock_client.call.assert_called_once()


async def test_get_flow_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_get_flow_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get flow execution"):
        await get_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_get_invocation_step(mock_client):
    mock_client.call.return_value = {}
    await get_invocation_step("test-invocation_identifier", "test-invocation_step_id", "test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_get_invocation_step_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_invocation_step("test-invocation_identifier", "test-invocation_step_id", "test-session_identifier", )


async def test_get_invocation_step_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get invocation step"):
        await get_invocation_step("test-invocation_identifier", "test-invocation_step_id", "test-session_identifier", )


async def test_get_session(mock_client):
    mock_client.call.return_value = {}
    await get_session("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_get_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_session("test-session_identifier", )


async def test_get_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get session"):
        await get_session("test-session_identifier", )


async def test_invoke_flow(mock_client):
    mock_client.call.return_value = {}
    await invoke_flow("test-flow_identifier", "test-flow_alias_identifier", [], )
    mock_client.call.assert_called_once()


async def test_invoke_flow_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await invoke_flow("test-flow_identifier", "test-flow_alias_identifier", [], )


async def test_invoke_flow_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to invoke flow"):
        await invoke_flow("test-flow_identifier", "test-flow_alias_identifier", [], )


async def test_list_flow_execution_events(mock_client):
    mock_client.call.return_value = {}
    await list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", )
    mock_client.call.assert_called_once()


async def test_list_flow_execution_events_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", )


async def test_list_flow_execution_events_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list flow execution events"):
        await list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", )


async def test_list_flow_executions(mock_client):
    mock_client.call.return_value = {}
    await list_flow_executions("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_list_flow_executions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_flow_executions("test-flow_identifier", )


async def test_list_flow_executions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list flow executions"):
        await list_flow_executions("test-flow_identifier", )


async def test_list_invocation_steps(mock_client):
    mock_client.call.return_value = {}
    await list_invocation_steps("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_list_invocation_steps_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_invocation_steps("test-session_identifier", )


async def test_list_invocation_steps_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list invocation steps"):
        await list_invocation_steps("test-session_identifier", )


async def test_list_invocations(mock_client):
    mock_client.call.return_value = {}
    await list_invocations("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_list_invocations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_invocations("test-session_identifier", )


async def test_list_invocations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list invocations"):
        await list_invocations("test-session_identifier", )


async def test_list_sessions(mock_client):
    mock_client.call.return_value = {}
    await list_sessions()
    mock_client.call.assert_called_once()


async def test_list_sessions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_sessions()


async def test_list_sessions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list sessions"):
        await list_sessions()


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_optimize_prompt(mock_client):
    mock_client.call.return_value = {}
    await optimize_prompt({}, "test-target_model_id", )
    mock_client.call.assert_called_once()


async def test_optimize_prompt_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await optimize_prompt({}, "test-target_model_id", )


async def test_optimize_prompt_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to optimize prompt"):
        await optimize_prompt({}, "test-target_model_id", )


async def test_put_invocation_step(mock_client):
    mock_client.call.return_value = {}
    await put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", {}, )
    mock_client.call.assert_called_once()


async def test_put_invocation_step_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", {}, )


async def test_put_invocation_step_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put invocation step"):
        await put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", {}, )


async def test_rerank(mock_client):
    mock_client.call.return_value = {}
    await rerank([], [], {}, )
    mock_client.call.assert_called_once()


async def test_rerank_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await rerank([], [], {}, )


async def test_rerank_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to rerank"):
        await rerank([], [], {}, )


async def test_retrieve_and_generate_stream(mock_client):
    mock_client.call.return_value = {}
    await retrieve_and_generate_stream({}, )
    mock_client.call.assert_called_once()


async def test_retrieve_and_generate_stream_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await retrieve_and_generate_stream({}, )


async def test_retrieve_and_generate_stream_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to retrieve and generate stream"):
        await retrieve_and_generate_stream({}, )


async def test_start_flow_execution(mock_client):
    mock_client.call.return_value = {}
    await start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", [], )
    mock_client.call.assert_called_once()


async def test_start_flow_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", [], )


async def test_start_flow_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start flow execution"):
        await start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", [], )


async def test_stop_flow_execution(mock_client):
    mock_client.call.return_value = {}
    await stop_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_flow_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_stop_flow_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop flow execution"):
        await stop_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


async def test_update_session(mock_client):
    mock_client.call.return_value = {}
    await update_session("test-session_identifier", )
    mock_client.call.assert_called_once()


async def test_update_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_session("test-session_identifier", )


async def test_update_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update session"):
        await update_session("test-session_identifier", )


@pytest.mark.asyncio
async def test_create_invocation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import create_invocation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await create_invocation("test-session_identifier", invocation_id="test-invocation_id", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import create_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await create_session(session_metadata="test-session_metadata", encryption_key_arn="test-encryption_key_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_agent_memory_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import delete_agent_memory
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await delete_agent_memory("test-agent_id", "test-agent_alias_id", memory_id="test-memory_id", session_id="test-session_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_agent_memory_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import get_agent_memory
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_invoke_flow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import invoke_flow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await invoke_flow("test-flow_identifier", "test-flow_alias_identifier", "test-inputs", enable_trace=True, model_performance_configuration={}, execution_id="test-execution_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flow_execution_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import list_flow_execution_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flow_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import list_flow_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await list_flow_executions("test-flow_identifier", flow_alias_identifier="test-flow_alias_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invocation_steps_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import list_invocation_steps
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await list_invocation_steps("test-session_identifier", invocation_identifier="test-invocation_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import list_invocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await list_invocations("test-session_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import list_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await list_sessions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_invocation_step_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import put_invocation_step
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", "test-payload", invocation_step_id="test-invocation_step_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_rerank_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import rerank
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await rerank("test-queries", "test-sources", {}, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_and_generate_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import retrieve_and_generate_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await retrieve_and_generate_stream("test-input", session_id="test-session_id", retrieve_and_generate_configuration={}, session_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_flow_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import start_flow_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-inputs", flow_execution_name="test-flow_execution_name", model_performance_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent_runtime import update_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent_runtime.async_client", lambda *a, **kw: mock_client)
    await update_session("test-session_identifier", session_metadata="test-session_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()
