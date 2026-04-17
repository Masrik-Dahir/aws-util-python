"""Tests for aws_util.bedrock_agent_runtime module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.bedrock_agent_runtime as mod
from aws_util.bedrock_agent_runtime import (
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
)

REGION = "us-east-1"
AGENT_ID = "AGENT123"
ALIAS_ID = "ALIAS456"
SESSION_ID = "sess-001"
KB_ID = "KB789"
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-v2"


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


def test_retrieved_reference_defaults():
    ref = RetrievedReference()
    assert ref.content == ""
    assert ref.location == {}
    assert ref.score is None
    assert ref.metadata == {}


def test_retrieved_reference_with_values():
    ref = RetrievedReference(
        content="hello",
        location={"type": "S3", "uri": "s3://bucket/key"},
        score=0.95,
        metadata={"source": "doc.pdf"},
    )
    assert ref.content == "hello"
    assert ref.score == 0.95


def test_citation_defaults():
    c = Citation()
    assert c.generated_response_part == {}
    assert c.retrieved_references == []


def test_invoke_agent_result():
    r = InvokeAgentResult(
        completion="Hello!",
        session_id=SESSION_ID,
    )
    assert r.completion == "Hello!"
    assert r.content_type == "text/plain"
    assert r.citations == []


def test_retrieval_result():
    r = RetrievalResult()
    assert r.references == []
    assert r.next_token is None


def test_knowledge_base_query():
    q = KnowledgeBaseQuery(text="What is AWS?")
    assert q.text == "What is AWS?"
    assert q.top_k == 5
    assert q.search_type == "SEMANTIC"


def test_retrieve_and_generate_result():
    r = RetrieveAndGenerateResult(output_text="Answer here")
    assert r.output_text == "Answer here"
    assert r.session_id is None
    assert r.citations == []


def test_invoke_inline_agent_result():
    r = InvokeInlineAgentResult(
        completion="Done",
        session_id=SESSION_ID,
    )
    assert r.completion == "Done"
    assert r.content_type == "text/plain"


# ---------------------------------------------------------------------------
# _parse_citations
# ---------------------------------------------------------------------------


def test_parse_citations_empty():
    from aws_util.bedrock_agent_runtime import _parse_citations

    assert _parse_citations([]) == []


def test_parse_citations_with_refs():
    from aws_util.bedrock_agent_runtime import _parse_citations

    raw = [
        {
            "generatedResponsePart": {"textResponsePart": {"text": "Answer"}},
            "retrievedReferences": [
                {
                    "content": {"text": "Source text"},
                    "location": {"type": "S3"},
                    "score": 0.9,
                    "metadata": {"page": "1"},
                },
            ],
        }
    ]
    citations = _parse_citations(raw)
    assert len(citations) == 1
    assert len(citations[0].retrieved_references) == 1
    assert citations[0].retrieved_references[0].content == "Source text"
    assert citations[0].retrieved_references[0].score == 0.9


def test_parse_citations_missing_fields():
    from aws_util.bedrock_agent_runtime import _parse_citations

    raw = [{"retrievedReferences": [{}]}]
    citations = _parse_citations(raw)
    assert len(citations) == 1
    ref = citations[0].retrieved_references[0]
    assert ref.content == ""
    assert ref.score is None


# ---------------------------------------------------------------------------
# _read_event_stream
# ---------------------------------------------------------------------------


def test_read_event_stream_with_bytes():
    from aws_util.bedrock_agent_runtime import _read_event_stream

    events = [
        {"chunk": {"bytes": b"Hello ", "attribution": {}}},
        {"chunk": {"bytes": b"world"}},
    ]
    text, citations = _read_event_stream(events)
    assert text == "Hello world"
    assert citations == []


def test_read_event_stream_with_string_bytes():
    from aws_util.bedrock_agent_runtime import _read_event_stream

    events = [{"chunk": {"bytes": "text content"}}]
    text, citations = _read_event_stream(events)
    assert text == "text content"


def test_read_event_stream_with_citations():
    from aws_util.bedrock_agent_runtime import _read_event_stream

    events = [
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
    ]
    text, citations = _read_event_stream(events)
    assert text == "Answer"
    assert len(citations) == 1


def test_read_event_stream_no_chunk():
    from aws_util.bedrock_agent_runtime import _read_event_stream

    events = [{"trace": {"some": "data"}}]
    text, citations = _read_event_stream(events)
    assert text == ""
    assert citations == []


def test_read_event_stream_empty_bytes():
    from aws_util.bedrock_agent_runtime import _read_event_stream

    events = [{"chunk": {"bytes": b""}}]
    text, citations = _read_event_stream(events)
    assert text == ""


# ---------------------------------------------------------------------------
# invoke_agent
# ---------------------------------------------------------------------------


def test_invoke_agent_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_agent.return_value = {
        "completion": [
            {"chunk": {"bytes": b"Hello from agent!"}},
        ],
        "contentType": "text/plain",
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = invoke_agent(
        AGENT_ID, ALIAS_ID, SESSION_ID, "Hi", region_name=REGION
    )
    assert isinstance(result, InvokeAgentResult)
    assert result.completion == "Hello from agent!"
    assert result.session_id == SESSION_ID


def test_invoke_agent_with_trace(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_agent.return_value = {
        "completion": [{"chunk": {"bytes": b"ok"}}],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = invoke_agent(
        AGENT_ID,
        ALIAS_ID,
        SESSION_ID,
        "Hi",
        enable_trace=True,
        end_session=True,
        region_name=REGION,
    )
    assert result.completion == "ok"
    call_kwargs = mock_client.invoke_agent.call_args[1]
    assert call_kwargs["enableTrace"] is True
    assert call_kwargs["endSession"] is True


def test_invoke_agent_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_agent.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "InvokeAgent",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    with pytest.raises(RuntimeError, match="invoke_agent failed"):
        invoke_agent(AGENT_ID, ALIAS_ID, SESSION_ID, "Hi", region_name=REGION)


def test_invoke_agent_empty_completion(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_agent.return_value = {"completion": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = invoke_agent(
        AGENT_ID, ALIAS_ID, SESSION_ID, "Hi", region_name=REGION
    )
    assert result.completion == ""


# ---------------------------------------------------------------------------
# retrieve
# ---------------------------------------------------------------------------


def test_retrieve_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.return_value = {
        "retrievalResults": [
            {
                "content": {"text": "Relevant passage"},
                "location": {"type": "S3", "s3Location": {"uri": "s3://b/k"}},
                "score": 0.92,
                "metadata": {},
            },
        ],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve(KB_ID, "What is X?", region_name=REGION)
    assert isinstance(result, RetrievalResult)
    assert len(result.references) == 1
    assert result.references[0].content == "Relevant passage"
    assert result.references[0].score == 0.92
    assert result.next_token is None


def test_retrieve_with_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.return_value = {
        "retrievalResults": [
            {"content": {"text": "page2"}, "score": 0.8},
        ],
        "nextToken": "token-2",
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve(
        KB_ID, "Q?", next_token="token-1", region_name=REGION
    )
    assert result.next_token == "token-2"
    call_kwargs = mock_client.retrieve.call_args[1]
    assert call_kwargs["nextToken"] == "token-1"


def test_retrieve_custom_top_k(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.return_value = {"retrievalResults": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    retrieve(KB_ID, "Q?", top_k=10, region_name=REGION)
    call_kwargs = mock_client.retrieve.call_args[1]
    config = call_kwargs["retrievalConfiguration"]["vectorSearchConfiguration"]
    assert config["numberOfResults"] == 10


def test_retrieve_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "Retrieve",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    with pytest.raises(RuntimeError, match="retrieve failed"):
        retrieve(KB_ID, "Q?", region_name=REGION)


def test_retrieve_empty_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.return_value = {"retrievalResults": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve(KB_ID, "Q?", region_name=REGION)
    assert result.references == []


def test_retrieve_missing_content_fields(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve.return_value = {
        "retrievalResults": [{}],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve(KB_ID, "Q?", region_name=REGION)
    assert result.references[0].content == ""
    assert result.references[0].score is None


# ---------------------------------------------------------------------------
# retrieve_and_generate
# ---------------------------------------------------------------------------


def test_retrieve_and_generate_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.return_value = {
        "output": {"text": "Generated answer"},
        "sessionId": "rag-sess-1",
        "citations": [],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve_and_generate(
        "What is X?", KB_ID, MODEL_ARN, region_name=REGION
    )
    assert isinstance(result, RetrieveAndGenerateResult)
    assert result.output_text == "Generated answer"
    assert result.session_id == "rag-sess-1"


def test_retrieve_and_generate_with_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.return_value = {
        "output": {"text": "ok"},
        "sessionId": "s1",
        "citations": [],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    retrieve_and_generate(
        "Q?", KB_ID, MODEL_ARN, session_id="s1", region_name=REGION
    )
    call_kwargs = mock_client.retrieve_and_generate.call_args[1]
    assert call_kwargs["sessionId"] == "s1"


def test_retrieve_and_generate_with_citations(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.return_value = {
        "output": {"text": "Answer"},
        "citations": [
            {
                "generatedResponsePart": {"textResponsePart": {"text": "A"}},
                "retrievedReferences": [
                    {"content": {"text": "Source"}, "score": 0.85},
                ],
            },
        ],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve_and_generate("Q?", KB_ID, MODEL_ARN, region_name=REGION)
    assert len(result.citations) == 1
    assert result.citations[0].retrieved_references[0].content == "Source"


def test_retrieve_and_generate_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}},
        "RetrieveAndGenerate",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    with pytest.raises(RuntimeError, match="retrieve_and_generate failed"):
        retrieve_and_generate("Q?", KB_ID, MODEL_ARN, region_name=REGION)


def test_retrieve_and_generate_non_dict_output(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.return_value = {
        "output": "not a dict",
        "citations": [],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve_and_generate("Q?", KB_ID, MODEL_ARN, region_name=REGION)
    assert result.output_text == ""


def test_retrieve_and_generate_missing_output(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate.return_value = {"citations": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = retrieve_and_generate("Q?", KB_ID, MODEL_ARN, region_name=REGION)
    assert result.output_text == ""


# ---------------------------------------------------------------------------
# invoke_inline_agent
# ---------------------------------------------------------------------------


def test_invoke_inline_agent_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.return_value = {
        "completion": [
            {"chunk": {"bytes": b"Inline response"}},
        ],
        "contentType": "text/plain",
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = invoke_inline_agent(
        "anthropic.claude-v2",
        SESSION_ID,
        "Hello",
        "You are helpful",
        region_name=REGION,
    )
    assert isinstance(result, InvokeInlineAgentResult)
    assert result.completion == "Inline response"
    assert result.session_id == SESSION_ID


def test_invoke_inline_agent_with_action_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.return_value = {
        "completion": [{"chunk": {"bytes": b"ok"}}],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    action_groups = [{"actionGroupName": "MyAction"}]
    invoke_inline_agent(
        "model",
        SESSION_ID,
        "Hi",
        "instr",
        action_groups=action_groups,
        region_name=REGION,
    )
    call_kwargs = mock_client.invoke_inline_agent.call_args[1]
    assert call_kwargs["actionGroups"] == action_groups


def test_invoke_inline_agent_with_knowledge_bases(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.return_value = {
        "completion": [{"chunk": {"bytes": b"ok"}}],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    kbs = [{"knowledgeBaseId": KB_ID}]
    invoke_inline_agent(
        "model",
        SESSION_ID,
        "Hi",
        "instr",
        knowledge_bases=kbs,
        region_name=REGION,
    )
    call_kwargs = mock_client.invoke_inline_agent.call_args[1]
    assert call_kwargs["knowledgeBases"] == kbs


def test_invoke_inline_agent_with_trace_and_end_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.return_value = {
        "completion": [{"chunk": {"bytes": b"done"}}],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    invoke_inline_agent(
        "model",
        SESSION_ID,
        "Hi",
        "instr",
        enable_trace=True,
        end_session=True,
        region_name=REGION,
    )
    call_kwargs = mock_client.invoke_inline_agent.call_args[1]
    assert call_kwargs["enableTrace"] is True
    assert call_kwargs["endSession"] is True


def test_invoke_inline_agent_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.side_effect = ClientError(
        {"Error": {"Code": "ThrottlingException", "Message": "slow down"}},
        "InvokeInlineAgent",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    with pytest.raises(RuntimeError, match="invoke_inline_agent failed"):
        invoke_inline_agent(
            "model", SESSION_ID, "Hi", "instr", region_name=REGION
        )


def test_invoke_inline_agent_empty_completion(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_inline_agent.return_value = {"completion": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)

    result = invoke_inline_agent(
        "model", SESSION_ID, "Hi", "instr", region_name=REGION
    )
    assert result.completion == ""


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


def test_create_invocation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_invocation.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    create_invocation("test-session_identifier", region_name=REGION)
    mock_client.create_invocation.assert_called_once()


def test_create_invocation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_invocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_invocation",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create invocation"):
        create_invocation("test-session_identifier", region_name=REGION)


def test_create_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    create_session(region_name=REGION)
    mock_client.create_session.assert_called_once()


def test_create_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_session",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create session"):
        create_session(region_name=REGION)


def test_delete_agent_memory(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_memory.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    delete_agent_memory("test-agent_id", "test-agent_alias_id", region_name=REGION)
    mock_client.delete_agent_memory.assert_called_once()


def test_delete_agent_memory_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_memory.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_agent_memory",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete agent memory"):
        delete_agent_memory("test-agent_id", "test-agent_alias_id", region_name=REGION)


def test_delete_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    delete_session("test-session_identifier", region_name=REGION)
    mock_client.delete_session.assert_called_once()


def test_delete_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_session",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete session"):
        delete_session("test-session_identifier", region_name=REGION)


def test_end_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.end_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    end_session("test-session_identifier", region_name=REGION)
    mock_client.end_session.assert_called_once()


def test_end_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.end_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "end_session",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to end session"):
        end_session("test-session_identifier", region_name=REGION)


def test_generate_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_query.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    generate_query({}, {}, region_name=REGION)
    mock_client.generate_query.assert_called_once()


def test_generate_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_query",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate query"):
        generate_query({}, {}, region_name=REGION)


def test_get_agent_memory(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_memory.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", region_name=REGION)
    mock_client.get_agent_memory.assert_called_once()


def test_get_agent_memory_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_memory.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_memory",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent memory"):
        get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", region_name=REGION)


def test_get_execution_flow_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_execution_flow_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_execution_flow_snapshot("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)
    mock_client.get_execution_flow_snapshot.assert_called_once()


def test_get_execution_flow_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_execution_flow_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_execution_flow_snapshot",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get execution flow snapshot"):
        get_execution_flow_snapshot("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)


def test_get_flow_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_execution.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)
    mock_client.get_flow_execution.assert_called_once()


def test_get_flow_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_execution",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow execution"):
        get_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)


def test_get_invocation_step(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invocation_step.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_invocation_step("test-invocation_identifier", "test-invocation_step_id", "test-session_identifier", region_name=REGION)
    mock_client.get_invocation_step.assert_called_once()


def test_get_invocation_step_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invocation_step.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_invocation_step",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get invocation step"):
        get_invocation_step("test-invocation_identifier", "test-invocation_step_id", "test-session_identifier", region_name=REGION)


def test_get_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_session("test-session_identifier", region_name=REGION)
    mock_client.get_session.assert_called_once()


def test_get_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session"):
        get_session("test-session_identifier", region_name=REGION)


def test_invoke_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    invoke_flow("test-flow_identifier", "test-flow_alias_identifier", [], region_name=REGION)
    mock_client.invoke_flow.assert_called_once()


def test_invoke_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "invoke_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to invoke flow"):
        invoke_flow("test-flow_identifier", "test-flow_alias_identifier", [], region_name=REGION)


def test_list_flow_execution_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_execution_events.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", region_name=REGION)
    mock_client.list_flow_execution_events.assert_called_once()


def test_list_flow_execution_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_execution_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flow_execution_events",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flow execution events"):
        list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", region_name=REGION)


def test_list_flow_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_executions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_flow_executions("test-flow_identifier", region_name=REGION)
    mock_client.list_flow_executions.assert_called_once()


def test_list_flow_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flow_executions",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flow executions"):
        list_flow_executions("test-flow_identifier", region_name=REGION)


def test_list_invocation_steps(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invocation_steps.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_invocation_steps("test-session_identifier", region_name=REGION)
    mock_client.list_invocation_steps.assert_called_once()


def test_list_invocation_steps_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invocation_steps.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_invocation_steps",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list invocation steps"):
        list_invocation_steps("test-session_identifier", region_name=REGION)


def test_list_invocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invocations.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_invocations("test-session_identifier", region_name=REGION)
    mock_client.list_invocations.assert_called_once()


def test_list_invocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_invocations",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list invocations"):
        list_invocations("test-session_identifier", region_name=REGION)


def test_list_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_sessions(region_name=REGION)
    mock_client.list_sessions.assert_called_once()


def test_list_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sessions",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list sessions"):
        list_sessions(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_optimize_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.optimize_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    optimize_prompt({}, "test-target_model_id", region_name=REGION)
    mock_client.optimize_prompt.assert_called_once()


def test_optimize_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.optimize_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "optimize_prompt",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to optimize prompt"):
        optimize_prompt({}, "test-target_model_id", region_name=REGION)


def test_put_invocation_step(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_invocation_step.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", {}, region_name=REGION)
    mock_client.put_invocation_step.assert_called_once()


def test_put_invocation_step_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_invocation_step.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_invocation_step",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put invocation step"):
        put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", {}, region_name=REGION)


def test_rerank(monkeypatch):
    mock_client = MagicMock()
    mock_client.rerank.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    rerank([], [], {}, region_name=REGION)
    mock_client.rerank.assert_called_once()


def test_rerank_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rerank.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rerank",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rerank"):
        rerank([], [], {}, region_name=REGION)


def test_retrieve_and_generate_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate_stream.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    retrieve_and_generate_stream({}, region_name=REGION)
    mock_client.retrieve_and_generate_stream.assert_called_once()


def test_retrieve_and_generate_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_and_generate_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retrieve_and_generate_stream",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to retrieve and generate stream"):
        retrieve_and_generate_stream({}, region_name=REGION)


def test_start_flow_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_flow_execution.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", [], region_name=REGION)
    mock_client.start_flow_execution.assert_called_once()


def test_start_flow_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_flow_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_flow_execution",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start flow execution"):
        start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", [], region_name=REGION)


def test_stop_flow_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_flow_execution.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    stop_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)
    mock_client.stop_flow_execution.assert_called_once()


def test_stop_flow_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_flow_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_flow_execution",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop flow execution"):
        stop_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    update_session("test-session_identifier", region_name=REGION)
    mock_client.update_session.assert_called_once()


def test_update_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_session",
    )
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update session"):
        update_session("test-session_identifier", region_name=REGION)


def test_create_invocation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import create_invocation
    mock_client = MagicMock()
    mock_client.create_invocation.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    create_invocation("test-session_identifier", invocation_id="test-invocation_id", description="test-description", region_name="us-east-1")
    mock_client.create_invocation.assert_called_once()

def test_create_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import create_session
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    create_session(session_metadata="test-session_metadata", encryption_key_arn="test-encryption_key_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_session.assert_called_once()

def test_delete_agent_memory_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import delete_agent_memory
    mock_client = MagicMock()
    mock_client.delete_agent_memory.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    delete_agent_memory("test-agent_id", "test-agent_alias_id", memory_id="test-memory_id", session_id="test-session_id", region_name="us-east-1")
    mock_client.delete_agent_memory.assert_called_once()

def test_get_agent_memory_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import get_agent_memory
    mock_client = MagicMock()
    mock_client.get_agent_memory.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    get_agent_memory("test-agent_id", "test-agent_alias_id", "test-memory_type", "test-memory_id", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.get_agent_memory.assert_called_once()

def test_invoke_flow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import invoke_flow
    mock_client = MagicMock()
    mock_client.invoke_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    invoke_flow("test-flow_identifier", "test-flow_alias_identifier", "test-inputs", enable_trace=True, model_performance_configuration={}, execution_id="test-execution_id", region_name="us-east-1")
    mock_client.invoke_flow.assert_called_once()

def test_list_flow_execution_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import list_flow_execution_events
    mock_client = MagicMock()
    mock_client.list_flow_execution_events.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_flow_execution_events("test-flow_identifier", "test-flow_alias_identifier", "test-execution_identifier", "test-event_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_flow_execution_events.assert_called_once()

def test_list_flow_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import list_flow_executions
    mock_client = MagicMock()
    mock_client.list_flow_executions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_flow_executions("test-flow_identifier", flow_alias_identifier="test-flow_alias_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_flow_executions.assert_called_once()

def test_list_invocation_steps_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import list_invocation_steps
    mock_client = MagicMock()
    mock_client.list_invocation_steps.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_invocation_steps("test-session_identifier", invocation_identifier="test-invocation_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_invocation_steps.assert_called_once()

def test_list_invocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import list_invocations
    mock_client = MagicMock()
    mock_client.list_invocations.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_invocations("test-session_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_invocations.assert_called_once()

def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import list_sessions
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    list_sessions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sessions.assert_called_once()

def test_put_invocation_step_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import put_invocation_step
    mock_client = MagicMock()
    mock_client.put_invocation_step.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    put_invocation_step("test-session_identifier", "test-invocation_identifier", "test-invocation_step_time", "test-payload", invocation_step_id="test-invocation_step_id", region_name="us-east-1")
    mock_client.put_invocation_step.assert_called_once()

def test_rerank_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import rerank
    mock_client = MagicMock()
    mock_client.rerank.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    rerank("test-queries", "test-sources", {}, next_token="test-next_token", region_name="us-east-1")
    mock_client.rerank.assert_called_once()

def test_retrieve_and_generate_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import retrieve_and_generate_stream
    mock_client = MagicMock()
    mock_client.retrieve_and_generate_stream.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    retrieve_and_generate_stream("test-input", session_id="test-session_id", retrieve_and_generate_configuration={}, session_configuration={}, region_name="us-east-1")
    mock_client.retrieve_and_generate_stream.assert_called_once()

def test_start_flow_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import start_flow_execution
    mock_client = MagicMock()
    mock_client.start_flow_execution.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    start_flow_execution("test-flow_identifier", "test-flow_alias_identifier", "test-inputs", flow_execution_name="test-flow_execution_name", model_performance_configuration={}, region_name="us-east-1")
    mock_client.start_flow_execution.assert_called_once()

def test_update_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent_runtime import update_session
    mock_client = MagicMock()
    mock_client.update_session.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent_runtime.get_client", lambda *a, **kw: mock_client)
    update_session("test-session_identifier", session_metadata="test-session_metadata", region_name="us-east-1")
    mock_client.update_session.assert_called_once()
