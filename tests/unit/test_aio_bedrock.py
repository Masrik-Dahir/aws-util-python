

"""Tests for aws_util.aio.bedrock — native async Bedrock utilities."""
from __future__ import annotations

import io
import json
from unittest.mock import AsyncMock

import pytest

import aws_util.aio.bedrock as bedrock_mod
from aws_util.aio.bedrock import (

    BedrockModel,
    InvokeModelResult,
    chat,
    embed_text,
    invoke_claude,
    invoke_model,
    invoke_titan_text,
    list_foundation_models,
    stream_invoke_claude,
    apply_guardrail,
    converse,
    converse_stream,
    count_tokens,
    get_async_invoke,
    invoke_model_with_response_stream,
    list_async_invokes,
    start_async_invoke,
    create_automated_reasoning_policy,
    create_automated_reasoning_policy_test_case,
    create_automated_reasoning_policy_version,
    create_custom_model,
    create_custom_model_deployment,
    create_evaluation_job,
    create_guardrail,
    create_guardrail_version,
    create_inference_profile,
    create_marketplace_model_endpoint,
    create_model_copy_job,
    create_model_customization_job,
    create_model_import_job,
    create_model_invocation_job,
    create_prompt_router,
    create_provisioned_model_throughput,
    delete_automated_reasoning_policy,
    delete_guardrail,
    get_guardrail,
    list_automated_reasoning_policies,
    list_automated_reasoning_policy_build_workflows,
    list_automated_reasoning_policy_test_cases,
    list_automated_reasoning_policy_test_results,
    list_custom_model_deployments,
    list_custom_models,
    list_evaluation_jobs,
    list_foundation_model_agreement_offers,
    list_guardrails,
    list_imported_models,
    list_inference_profiles,
    list_marketplace_model_endpoints,
    list_model_copy_jobs,
    list_model_customization_jobs,
    list_model_import_jobs,
    list_model_invocation_jobs,
    list_prompt_routers,
    list_provisioned_model_throughputs,
    start_automated_reasoning_policy_build_workflow,
    start_automated_reasoning_policy_test_workflow,
    update_automated_reasoning_policy,
    update_automated_reasoning_policy_test_case,
    update_guardrail,
    update_marketplace_model_endpoint,
    update_provisioned_model_throughput,
)



REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.bedrock.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# invoke_model — body parsing branches
# ---------------------------------------------------------------------------


async def test_invoke_model_body_bytes(mock_client):
    body_data = {"content": [{"text": "hello"}]}
    mock_client.call.return_value = {
        "body": json.dumps(body_data).encode(),
        "contentType": "application/json",
    }
    result = await invoke_model("model-1", {"prompt": "hi"})
    assert result.body == body_data
    assert result.model_id == "model-1"


async def test_invoke_model_body_bytes_not_json(mock_client):
    mock_client.call.return_value = {
        "body": b"plain text response",
        "contentType": "text/plain",
    }
    result = await invoke_model("model-1", {"prompt": "hi"})
    assert result.body == "plain text response"


async def test_invoke_model_body_bytearray(mock_client):
    body_data = {"result": "ok"}
    mock_client.call.return_value = {
        "body": bytearray(json.dumps(body_data).encode()),
        "contentType": "application/json",
    }
    result = await invoke_model("model-1", {})
    assert result.body == body_data


async def test_invoke_model_body_string_json(mock_client):
    body_data = {"result": "ok"}
    mock_client.call.return_value = {
        "body": json.dumps(body_data),
        "contentType": "application/json",
    }
    result = await invoke_model("model-1", {})
    assert result.body == body_data


async def test_invoke_model_body_string_not_json(mock_client):
    mock_client.call.return_value = {
        "body": "plain text",
        "contentType": "text/plain",
    }
    result = await invoke_model("model-1", {})
    assert result.body == "plain text"


async def test_invoke_model_body_readable(mock_client):
    """Body has a .read() method (like a StreamingBody)."""
    body_data = {"result": "ok"}

    class FakeStream:
        def read(self):
            return json.dumps(body_data).encode()

    mock_client.call.return_value = {
        "body": FakeStream(),
        "contentType": "application/json",
    }
    result = await invoke_model("model-1", {})
    assert result.body == body_data


async def test_invoke_model_body_other_type(mock_client):
    """Body is neither bytes, str, nor readable — returned as-is (dict)."""
    mock_client.call.return_value = {
        "body": {"already": "parsed"},
        "contentType": "application/json",
    }
    result = await invoke_model("model-1", {})
    assert result.body == {"already": "parsed"}


async def test_invoke_model_empty_body(mock_client):
    """Empty body field defaults to b""."""
    mock_client.call.return_value = {}
    result = await invoke_model("model-1", {})
    # b"" -> json.loads fails -> decode -> ""
    assert result.body == ""


async def test_invoke_model_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to invoke Bedrock model"):
        await invoke_model("model-1", {})


async def test_invoke_model_missing_content_type(mock_client):
    mock_client.call.return_value = {
        "body": json.dumps({"ok": True}).encode(),
    }
    result = await invoke_model("model-1", {})
    assert result.content_type == "application/json"


# ---------------------------------------------------------------------------
# invoke_claude
# ---------------------------------------------------------------------------


async def test_invoke_claude_success(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": [{"text": "Hello!"}]},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_claude("hi")
    assert text == "Hello!"


async def test_invoke_claude_with_system(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": [{"text": "ok"}]},
    )
    mock_invoke = AsyncMock(return_value=result)
    monkeypatch.setattr(bedrock_mod, "invoke_model", mock_invoke)
    await invoke_claude("hi", system="be helpful")
    body_arg = mock_invoke.call_args[0][1]
    assert body_arg["system"] == "be helpful"


async def test_invoke_claude_empty_content(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": []},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_claude("hi")
    # empty content -> str(response_body)
    assert "content" in text


async def test_invoke_claude_non_dict_body(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body="raw string",
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_claude("hi")
    assert text == "raw string"


async def test_invoke_claude_content_not_list(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": "not a list"},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_claude("hi")
    assert "content" in text


# ---------------------------------------------------------------------------
# invoke_titan_text
# ---------------------------------------------------------------------------


async def test_invoke_titan_text_success(monkeypatch):
    result = InvokeModelResult(
        model_id="titan",
        body={"results": [{"outputText": "Generated text"}]},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_titan_text("hi")
    assert text == "Generated text"


async def test_invoke_titan_text_empty_results(monkeypatch):
    result = InvokeModelResult(
        model_id="titan",
        body={"results": []},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_titan_text("hi")
    assert "results" in text


async def test_invoke_titan_text_non_dict_body(monkeypatch):
    result = InvokeModelResult(
        model_id="titan",
        body="raw string",
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await invoke_titan_text("hi")
    assert text == "raw string"


# ---------------------------------------------------------------------------
# chat
# ---------------------------------------------------------------------------


async def test_chat_success(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": [{"text": "Reply"}]},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    msgs = [{"role": "user", "content": "hi"}]
    text = await chat(msgs)
    assert text == "Reply"


async def test_chat_with_system(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": [{"text": "ok"}]},
    )
    mock_invoke = AsyncMock(return_value=result)
    monkeypatch.setattr(bedrock_mod, "invoke_model", mock_invoke)
    await chat([{"role": "user", "content": "hi"}], system="sys")
    body_arg = mock_invoke.call_args[0][1]
    assert body_arg["system"] == "sys"


async def test_chat_empty_content(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": []},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await chat([{"role": "user", "content": "hi"}])
    assert "content" in text


async def test_chat_non_dict_body(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body="raw",
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await chat([{"role": "user", "content": "hi"}])
    assert text == "raw"


async def test_chat_content_not_list(monkeypatch):
    result = InvokeModelResult(
        model_id="claude",
        body={"content": "not a list"},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    text = await chat([{"role": "user", "content": "hi"}])
    assert "content" in text


# ---------------------------------------------------------------------------
# embed_text
# ---------------------------------------------------------------------------


async def test_embed_text_success(monkeypatch):
    result = InvokeModelResult(
        model_id="titan-embed",
        body={"embedding": [0.1, 0.2, 0.3]},
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    vec = await embed_text("hello")
    assert vec == [0.1, 0.2, 0.3]


async def test_embed_text_non_dict_body(monkeypatch):
    result = InvokeModelResult(
        model_id="titan-embed",
        body="not a dict",
    )
    monkeypatch.setattr(
        bedrock_mod, "invoke_model", AsyncMock(return_value=result)
    )
    vec = await embed_text("hello")
    assert vec == []


# ---------------------------------------------------------------------------
# stream_invoke_claude
# ---------------------------------------------------------------------------


async def test_stream_invoke_claude_success(mock_client):
    chunk1 = json.dumps(
        {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "Hello"}}
    ).encode()
    chunk2 = json.dumps(
        {"type": "content_block_delta", "delta": {"type": "text_delta", "text": " world"}}
    ).encode()
    chunk3 = json.dumps({"type": "message_stop"}).encode()

    async def fake_stream(*args, **kwargs):
        for c in [chunk1, chunk2, chunk3]:
            yield c

    mock_client.call_with_stream = fake_stream
    chunks = []
    async for text in stream_invoke_claude("hi"):
        chunks.append(text)
    assert "Hello" in chunks
    assert " world" in chunks


async def test_stream_invoke_claude_with_system(mock_client):
    chunk = json.dumps(
        {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "ok"}}
    ).encode()

    async def fake_stream(*args, **kwargs):
        yield chunk

    mock_client.call_with_stream = fake_stream
    chunks = []
    async for text in stream_invoke_claude("hi", system="be nice"):
        chunks.append(text)
    assert "ok" in chunks


async def test_stream_invoke_claude_partial_json(mock_client):
    """Incomplete JSON chunk => JSONDecodeError => break out of inner loop."""
    async def fake_stream(*args, **kwargs):
        yield b'{"type": "content_blo'

    mock_client.call_with_stream = fake_stream
    chunks = []
    async for text in stream_invoke_claude("hi"):
        chunks.append(text)
    assert chunks == []


async def test_stream_invoke_claude_non_text_delta(mock_client):
    """content_block_delta with non-text_delta type => no yield."""
    chunk = json.dumps(
        {"type": "content_block_delta", "delta": {"type": "other"}}
    ).encode()

    async def fake_stream(*args, **kwargs):
        yield chunk

    mock_client.call_with_stream = fake_stream
    chunks = []
    async for text in stream_invoke_claude("hi"):
        chunks.append(text)
    assert chunks == []


async def test_stream_invoke_claude_runtime_error(mock_client):
    async def fail_stream(*args, **kwargs):
        raise RuntimeError("boom")
        yield  # noqa: unreachable - make it a generator

    mock_client.call_with_stream = fail_stream
    with pytest.raises(RuntimeError, match="Failed to stream Bedrock model"):
        async for _ in stream_invoke_claude("hi"):
            pass


# ---------------------------------------------------------------------------
# list_foundation_models
# ---------------------------------------------------------------------------


async def test_list_foundation_models_success(mock_client):
    mock_client.call.return_value = {
        "modelSummaries": [
            {
                "modelId": "anthropic.claude-v2",
                "modelName": "Claude v2",
                "providerName": "Anthropic",
                "inputModalities": ["TEXT"],
                "outputModalities": ["TEXT"],
                "responseStreamingSupported": True,
            }
        ]
    }
    models = await list_foundation_models()
    assert len(models) == 1
    assert models[0].model_id == "anthropic.claude-v2"
    assert models[0].response_streaming_supported is True


async def test_list_foundation_models_with_provider(mock_client):
    mock_client.call.return_value = {"modelSummaries": []}
    await list_foundation_models(provider_name="Anthropic")
    kw = mock_client.call.call_args[1]
    assert kw["byProvider"] == "Anthropic"


async def test_list_foundation_models_empty(mock_client):
    mock_client.call.return_value = {"modelSummaries": []}
    models = await list_foundation_models()
    assert models == []


async def test_list_foundation_models_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="list_foundation_models failed"):
        await list_foundation_models()


async def test_list_foundation_models_minimal_model(mock_client):
    mock_client.call.return_value = {
        "modelSummaries": [{"modelId": "m1"}]
    }
    models = await list_foundation_models()
    assert models[0].model_name == ""
    assert models[0].provider_name == ""
    assert models[0].input_modalities == []
    assert models[0].output_modalities == []
    assert models[0].response_streaming_supported is False


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_bedrock_model_in_all():
    assert "BedrockModel" in bedrock_mod.__all__
    assert "InvokeModelResult" in bedrock_mod.__all__


async def test_apply_guardrail(mock_client):
    mock_client.call.return_value = {}
    await apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", [], )
    mock_client.call.assert_called_once()


async def test_apply_guardrail_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", [], )


async def test_apply_guardrail_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to apply guardrail"):
        await apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", [], )


async def test_converse(mock_client):
    mock_client.call.return_value = {}
    await converse("test-model_id", )
    mock_client.call.assert_called_once()


async def test_converse_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await converse("test-model_id", )


async def test_converse_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to converse"):
        await converse("test-model_id", )


async def test_converse_stream(mock_client):
    mock_client.call.return_value = {}
    await converse_stream("test-model_id", )
    mock_client.call.assert_called_once()


async def test_converse_stream_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await converse_stream("test-model_id", )


async def test_converse_stream_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to converse stream"):
        await converse_stream("test-model_id", )


async def test_count_tokens(mock_client):
    mock_client.call.return_value = {}
    await count_tokens("test-model_id", {}, )
    mock_client.call.assert_called_once()


async def test_count_tokens_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await count_tokens("test-model_id", {}, )


async def test_count_tokens_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to count tokens"):
        await count_tokens("test-model_id", {}, )


async def test_get_async_invoke(mock_client):
    mock_client.call.return_value = {}
    await get_async_invoke("test-invocation_arn", )
    mock_client.call.assert_called_once()


async def test_get_async_invoke_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_async_invoke("test-invocation_arn", )


async def test_get_async_invoke_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get async invoke"):
        await get_async_invoke("test-invocation_arn", )


async def test_invoke_model_with_response_stream(mock_client):
    mock_client.call.return_value = {}
    await invoke_model_with_response_stream("test-model_id", )
    mock_client.call.assert_called_once()


async def test_invoke_model_with_response_stream_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await invoke_model_with_response_stream("test-model_id", )


async def test_invoke_model_with_response_stream_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to invoke model with response stream"):
        await invoke_model_with_response_stream("test-model_id", )


async def test_list_async_invokes(mock_client):
    mock_client.call.return_value = {}
    await list_async_invokes()
    mock_client.call.assert_called_once()


async def test_list_async_invokes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_async_invokes()


async def test_list_async_invokes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list async invokes"):
        await list_async_invokes()


async def test_start_async_invoke(mock_client):
    mock_client.call.return_value = {}
    await start_async_invoke("test-model_id", {}, {}, )
    mock_client.call.assert_called_once()


async def test_start_async_invoke_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_async_invoke("test-model_id", {}, {}, )


async def test_start_async_invoke_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start async invoke"):
        await start_async_invoke("test-model_id", {}, {}, )


@pytest.mark.asyncio
async def test_apply_guardrail_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import apply_guardrail
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", "test-content", output_scope="test-output_scope", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_converse_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import converse
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await converse("test-model_id", messages="test-messages", system="test-system", inference_config={}, tool_config={}, guardrail_config={}, additional_model_request_fields="test-additional_model_request_fields", prompt_variables="test-prompt_variables", additional_model_response_field_paths="test-additional_model_response_field_paths", request_metadata="test-request_metadata", performance_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_converse_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import converse_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await converse_stream("test-model_id", messages="test-messages", system="test-system", inference_config={}, tool_config={}, guardrail_config={}, additional_model_request_fields="test-additional_model_request_fields", prompt_variables="test-prompt_variables", additional_model_response_field_paths="test-additional_model_response_field_paths", request_metadata="test-request_metadata", performance_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_invoke_model_with_response_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import invoke_model_with_response_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await invoke_model_with_response_stream("test-model_id", body="test-body", content_type="test-content_type", accept="test-accept", trace="test-trace", guardrail_identifier="test-guardrail_identifier", guardrail_version="test-guardrail_version", performance_config_latency={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_async_invokes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import list_async_invokes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_async_invokes(submit_time_after="test-submit_time_after", submit_time_before="test-submit_time_before", status_equals="test-status_equals", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_async_invoke_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock import start_async_invoke
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await start_async_invoke("test-model_id", "test-model_input", {}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()
# Generated async tests for boto3 wrapper methods
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.bedrock import (
    list_foundation_models,
    batch_delete_evaluation_job,
    cancel_automated_reasoning_policy_build_workflow,
    create_automated_reasoning_policy,
    create_automated_reasoning_policy_test_case,
    create_automated_reasoning_policy_version,
    create_custom_model,
    create_custom_model_deployment,
    create_evaluation_job,
    create_foundation_model_agreement,
    create_guardrail,
    create_guardrail_version,
    create_inference_profile,
    create_marketplace_model_endpoint,
    create_model_copy_job,
    create_model_customization_job,
    create_model_import_job,
    create_model_invocation_job,
    create_prompt_router,
    create_provisioned_model_throughput,
    delete_automated_reasoning_policy,
    delete_automated_reasoning_policy_build_workflow,
    delete_automated_reasoning_policy_test_case,
    delete_custom_model,
    delete_custom_model_deployment,
    delete_foundation_model_agreement,
    delete_guardrail,
    delete_imported_model,
    delete_inference_profile,
    delete_marketplace_model_endpoint,
    delete_model_invocation_logging_configuration,
    delete_prompt_router,
    delete_provisioned_model_throughput,
    deregister_marketplace_model_endpoint,
    export_automated_reasoning_policy_version,
    get_automated_reasoning_policy,
    get_automated_reasoning_policy_annotations,
    get_automated_reasoning_policy_build_workflow,
    get_automated_reasoning_policy_build_workflow_result_assets,
    get_automated_reasoning_policy_next_scenario,
    get_automated_reasoning_policy_test_case,
    get_automated_reasoning_policy_test_result,
    get_custom_model,
    get_custom_model_deployment,
    get_evaluation_job,
    get_foundation_model,
    get_foundation_model_availability,
    get_guardrail,
    get_imported_model,
    get_inference_profile,
    get_marketplace_model_endpoint,
    get_model_copy_job,
    get_model_customization_job,
    get_model_import_job,
    get_model_invocation_job,
    get_model_invocation_logging_configuration,
    get_prompt_router,
    get_provisioned_model_throughput,
    get_use_case_for_model_access,
    list_automated_reasoning_policies,
    list_automated_reasoning_policy_build_workflows,
    list_automated_reasoning_policy_test_cases,
    list_automated_reasoning_policy_test_results,
    list_custom_model_deployments,
    list_custom_models,
    list_evaluation_jobs,
    list_foundation_model_agreement_offers,
    list_guardrails,
    list_imported_models,
    list_inference_profiles,
    list_marketplace_model_endpoints,
    list_model_copy_jobs,
    list_model_customization_jobs,
    list_model_import_jobs,
    list_model_invocation_jobs,
    list_prompt_routers,
    list_provisioned_model_throughputs,
    list_tags_for_resource,
    put_model_invocation_logging_configuration,
    put_use_case_for_model_access,
    register_marketplace_model_endpoint,
    start_automated_reasoning_policy_build_workflow,
    start_automated_reasoning_policy_test_workflow,
    stop_evaluation_job,
    stop_model_customization_job,
    stop_model_invocation_job,
    tag_resource,
    untag_resource,
    update_automated_reasoning_policy,
    update_automated_reasoning_policy_annotations,
    update_automated_reasoning_policy_test_case,
    update_guardrail,
    update_marketplace_model_endpoint,
    update_provisioned_model_throughput,
)


async def test_list_foundation_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_foundation_models(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_foundation_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_foundation_models(region_name="us-east-1")


async def test_batch_delete_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await batch_delete_evaluation_job([], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_batch_delete_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await batch_delete_evaluation_job([], region_name="us-east-1")


async def test_cancel_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await cancel_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_cancel_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await cancel_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_create_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy("test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_automated_reasoning_policy("test-name", region_name="us-east-1")


async def test_create_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", region_name="us-east-1")


async def test_create_automated_reasoning_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", region_name="us-east-1")


async def test_create_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_custom_model("test-model_name", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_custom_model("test-model_name", {}, region_name="us-east-1")


async def test_create_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_custom_model_deployment("test-model_deployment_name", "test-model_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_custom_model_deployment("test-model_deployment_name", "test-model_arn", region_name="us-east-1")


async def test_create_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, region_name="us-east-1")


async def test_create_foundation_model_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_foundation_model_agreement("test-offer_token", "test-model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_foundation_model_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_foundation_model_agreement("test-offer_token", "test-model_id", region_name="us-east-1")


async def test_create_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")


async def test_create_guardrail_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_guardrail_version("test-guardrail_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_guardrail_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_guardrail_version("test-guardrail_identifier", region_name="us-east-1")


async def test_create_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_inference_profile("test-inference_profile_name", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_inference_profile("test-inference_profile_name", {}, region_name="us-east-1")


async def test_create_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", region_name="us-east-1")


async def test_create_model_copy_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_copy_job("test-source_model_arn", "test-target_model_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_copy_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_model_copy_job("test-source_model_arn", "test-target_model_name", region_name="us-east-1")


async def test_create_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, region_name="us-east-1")


async def test_create_model_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, region_name="us-east-1")


async def test_create_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, region_name="us-east-1")


async def test_create_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_prompt_router("test-prompt_router_name", [], {}, {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_prompt_router("test-prompt_router_name", [], {}, {}, region_name="us-east-1")


async def test_create_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", region_name="us-east-1")


async def test_delete_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")


async def test_delete_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", "test-last_updated_at", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", "test-last_updated_at", region_name="us-east-1")


async def test_delete_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-last_updated_at", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-last_updated_at", region_name="us-east-1")


async def test_delete_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_custom_model("test-model_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_custom_model("test-model_identifier", region_name="us-east-1")


async def test_delete_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")


async def test_delete_foundation_model_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_foundation_model_agreement("test-model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_foundation_model_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_foundation_model_agreement("test-model_id", region_name="us-east-1")


async def test_delete_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_guardrail("test-guardrail_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_guardrail("test-guardrail_identifier", region_name="us-east-1")


async def test_delete_imported_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_imported_model("test-model_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_imported_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_imported_model("test-model_identifier", region_name="us-east-1")


async def test_delete_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_inference_profile("test-inference_profile_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_inference_profile("test-inference_profile_identifier", region_name="us-east-1")


async def test_delete_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


async def test_delete_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_model_invocation_logging_configuration(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_model_invocation_logging_configuration(region_name="us-east-1")


async def test_delete_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_prompt_router("test-prompt_router_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_prompt_router("test-prompt_router_arn", region_name="us-east-1")


async def test_delete_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


async def test_deregister_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await deregister_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_deregister_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await deregister_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


async def test_export_automated_reasoning_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await export_automated_reasoning_policy_version("test-policy_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_export_automated_reasoning_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await export_automated_reasoning_policy_version("test-policy_arn", region_name="us-east-1")


async def test_get_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")


async def test_get_automated_reasoning_policy_annotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_annotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_get_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_get_automated_reasoning_policy_build_workflow_result_assets(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_build_workflow_result_assets("test-policy_arn", "test-build_workflow_id", "test-asset_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_build_workflow_result_assets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_build_workflow_result_assets("test-policy_arn", "test-build_workflow_id", "test-asset_type", region_name="us-east-1")


async def test_get_automated_reasoning_policy_next_scenario(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_next_scenario("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_next_scenario_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_next_scenario("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_get_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", region_name="us-east-1")


async def test_get_automated_reasoning_policy_test_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_automated_reasoning_policy_test_result("test-policy_arn", "test-build_workflow_id", "test-test_case_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_automated_reasoning_policy_test_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_automated_reasoning_policy_test_result("test-policy_arn", "test-build_workflow_id", "test-test_case_id", region_name="us-east-1")


async def test_get_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_custom_model("test-model_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_custom_model("test-model_identifier", region_name="us-east-1")


async def test_get_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")


async def test_get_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_evaluation_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_evaluation_job("test-job_identifier", region_name="us-east-1")


async def test_get_foundation_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_foundation_model("test-model_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_foundation_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_foundation_model("test-model_identifier", region_name="us-east-1")


async def test_get_foundation_model_availability(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_foundation_model_availability("test-model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_foundation_model_availability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_foundation_model_availability("test-model_id", region_name="us-east-1")


async def test_get_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_guardrail("test-guardrail_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_guardrail("test-guardrail_identifier", region_name="us-east-1")


async def test_get_imported_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_imported_model("test-model_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_imported_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_imported_model("test-model_identifier", region_name="us-east-1")


async def test_get_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_inference_profile("test-inference_profile_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_inference_profile("test-inference_profile_identifier", region_name="us-east-1")


async def test_get_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


async def test_get_model_copy_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_model_copy_job("test-job_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_copy_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_copy_job("test-job_arn", region_name="us-east-1")


async def test_get_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_model_customization_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_customization_job("test-job_identifier", region_name="us-east-1")


async def test_get_model_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_model_import_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_import_job("test-job_identifier", region_name="us-east-1")


async def test_get_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_model_invocation_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_invocation_job("test-job_identifier", region_name="us-east-1")


async def test_get_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_model_invocation_logging_configuration(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_invocation_logging_configuration(region_name="us-east-1")


async def test_get_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_prompt_router("test-prompt_router_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_prompt_router("test-prompt_router_arn", region_name="us-east-1")


async def test_get_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


async def test_get_use_case_for_model_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_use_case_for_model_access(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_use_case_for_model_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_use_case_for_model_access(region_name="us-east-1")


async def test_list_automated_reasoning_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policies(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_automated_reasoning_policies(region_name="us-east-1")


async def test_list_automated_reasoning_policy_build_workflows(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_build_workflows("test-policy_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_build_workflows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_automated_reasoning_policy_build_workflows("test-policy_arn", region_name="us-east-1")


async def test_list_automated_reasoning_policy_test_cases(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_test_cases("test-policy_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_test_cases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_automated_reasoning_policy_test_cases("test-policy_arn", region_name="us-east-1")


async def test_list_automated_reasoning_policy_test_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_test_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_list_custom_model_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_custom_model_deployments(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_custom_model_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_custom_model_deployments(region_name="us-east-1")


async def test_list_custom_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_custom_models(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_custom_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_custom_models(region_name="us-east-1")


async def test_list_evaluation_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_evaluation_jobs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_evaluation_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_evaluation_jobs(region_name="us-east-1")


async def test_list_foundation_model_agreement_offers(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_foundation_model_agreement_offers("test-model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_foundation_model_agreement_offers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_foundation_model_agreement_offers("test-model_id", region_name="us-east-1")


async def test_list_guardrails(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_guardrails(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_guardrails_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_guardrails(region_name="us-east-1")


async def test_list_imported_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_imported_models(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_imported_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_imported_models(region_name="us-east-1")


async def test_list_inference_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_inference_profiles(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_inference_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_inference_profiles(region_name="us-east-1")


async def test_list_marketplace_model_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_marketplace_model_endpoints(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_marketplace_model_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_marketplace_model_endpoints(region_name="us-east-1")


async def test_list_model_copy_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_copy_jobs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_copy_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_model_copy_jobs(region_name="us-east-1")


async def test_list_model_customization_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_customization_jobs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_customization_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_model_customization_jobs(region_name="us-east-1")


async def test_list_model_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_import_jobs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_model_import_jobs(region_name="us-east-1")


async def test_list_model_invocation_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_invocation_jobs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_invocation_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_model_invocation_jobs(region_name="us-east-1")


async def test_list_prompt_routers(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_prompt_routers(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_prompt_routers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_prompt_routers(region_name="us-east-1")


async def test_list_provisioned_model_throughputs(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_provisioned_model_throughputs(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_provisioned_model_throughputs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_provisioned_model_throughputs(region_name="us-east-1")


async def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await list_tags_for_resource("test-resource_arn", region_name="us-east-1")


async def test_put_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await put_model_invocation_logging_configuration({}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_model_invocation_logging_configuration({}, region_name="us-east-1")


async def test_put_use_case_for_model_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await put_use_case_for_model_access("test-form_data", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_use_case_for_model_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_use_case_for_model_access("test-form_data", region_name="us-east-1")


async def test_register_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await register_marketplace_model_endpoint("test-endpoint_identifier", "test-model_source_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_register_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await register_marketplace_model_endpoint("test-endpoint_identifier", "test-model_source_identifier", region_name="us-east-1")


async def test_start_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_start_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, region_name="us-east-1")


async def test_start_automated_reasoning_policy_test_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_start_automated_reasoning_policy_test_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


async def test_stop_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await stop_evaluation_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_stop_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await stop_evaluation_job("test-job_identifier", region_name="us-east-1")


async def test_stop_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await stop_model_customization_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_stop_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await stop_model_customization_job("test-job_identifier", region_name="us-east-1")


async def test_stop_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await stop_model_invocation_job("test-job_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_stop_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await stop_model_invocation_job("test-job_identifier", region_name="us-east-1")


async def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await tag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await tag_resource("test-resource_arn", [], region_name="us-east-1")


async def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await untag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await untag_resource("test-resource_arn", [], region_name="us-east-1")


async def test_update_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_automated_reasoning_policy("test-policy_arn", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_automated_reasoning_policy("test-policy_arn", {}, region_name="us-east-1")


async def test_update_automated_reasoning_policy_annotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", [], "test-last_updated_annotation_set_hash", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_automated_reasoning_policy_annotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", [], "test-last_updated_annotation_set_hash", region_name="us-east-1")


async def test_update_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", region_name="us-east-1")


async def test_update_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")


async def test_update_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_marketplace_model_endpoint("test-endpoint_arn", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_marketplace_model_endpoint("test-endpoint_arn", {}, region_name="us-east-1")


async def test_update_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


async def test_list_foundation_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_foundation_models(provider_name="test-provider_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy("test-name", description="test-description", client_request_token="test-client_request_token", policy_definition={}, kms_key_id="test-kms_key_id", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_test_case_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", query_content="test-query_content", client_request_token="test-client_request_token", confidence_threshold=1.0, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_automated_reasoning_policy_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_custom_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_custom_model("test-model_name", {}, model_kms_key_arn="test-model_kms_key_arn", role_arn="test-role_arn", model_tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_custom_model_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_custom_model_deployment("test-model_deployment_name", "test-model_arn", description="test-description", tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_evaluation_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, job_description="test-job_description", client_request_token="test-client_request_token", customer_encryption_key_id="test-customer_encryption_key_id", job_tags=[], application_type="test-application_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", description="test-description", topic_policy_config={}, content_policy_config={}, word_policy_config={}, sensitive_information_policy_config={}, contextual_grounding_policy_config={}, automated_reasoning_policy_config={}, cross_region_config={}, kms_key_id="test-kms_key_id", tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_guardrail_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_guardrail_version("test-guardrail_identifier", description="test-description", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_inference_profile_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_inference_profile("test-inference_profile_name", {}, description="test-description", client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_marketplace_model_endpoint_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", accept_eula=True, client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_copy_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_copy_job("test-source_model_arn", "test-target_model_name", model_kms_key_id="test-model_kms_key_id", target_model_tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_customization_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, client_request_token="test-client_request_token", customization_type="test-customization_type", custom_model_kms_key_id="test-custom_model_kms_key_id", job_tags=[], custom_model_tags=[], validation_data_config={}, hyper_parameters={}, vpc_config={}, customization_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_import_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, job_tags=[], imported_model_tags=[], client_request_token="test-client_request_token", vpc_config={}, imported_model_kms_key_id="test-imported_model_kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_invocation_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, client_request_token="test-client_request_token", vpc_config={}, timeout_duration_in_hours=1, tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_prompt_router_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_prompt_router("test-prompt_router_name", [], {}, {}, client_request_token="test-client_request_token", description="test-description", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_provisioned_model_throughput_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", client_request_token="test-client_request_token", commitment_duration="test-commitment_duration", tags=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_automated_reasoning_policy("test-policy_arn", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await delete_guardrail("test-guardrail_identifier", guardrail_version="test-guardrail_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await get_guardrail("test-guardrail_identifier", guardrail_version="test-guardrail_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policies_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policies(policy_arn="test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_build_workflows_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_build_workflows("test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_test_cases_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_test_cases("test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_automated_reasoning_policy_test_results_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_custom_model_deployments_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_custom_model_deployments(created_before="test-created_before", created_after="test-created_after", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", status_equals="test-status_equals", model_arn_equals="test-model_arn_equals", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_custom_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_custom_models(creation_time_before="test-creation_time_before", creation_time_after="test-creation_time_after", name_contains="test-name_contains", base_model_arn_equals="test-base_model_arn_equals", foundation_model_arn_equals="test-foundation_model_arn_equals", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", is_owned=True, model_status="test-model_status", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_evaluation_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_evaluation_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", application_type_equals="test-application_type_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_foundation_model_agreement_offers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_foundation_model_agreement_offers("test-model_id", offer_type="test-offer_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_guardrails_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_guardrails(guardrail_identifier="test-guardrail_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_imported_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_imported_models(creation_time_before="test-creation_time_before", creation_time_after="test-creation_time_after", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_inference_profiles_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_inference_profiles(max_results=1, next_token="test-next_token", type_equals="test-type_equals", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_marketplace_model_endpoints_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_marketplace_model_endpoints(max_results=1, next_token="test-next_token", model_source_equals="test-model_source_equals", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_copy_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_copy_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", source_account_equals="test-source_account_equals", source_model_arn_equals="test-source_model_arn_equals", target_model_name_contains="test-target_model_name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_customization_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_customization_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_import_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_import_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_model_invocation_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_model_invocation_jobs(submit_time_after="test-submit_time_after", submit_time_before="test-submit_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_prompt_routers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_prompt_routers(max_results=1, next_token="test-next_token", type="test-type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_list_provisioned_model_throughputs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await list_provisioned_model_throughputs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", model_arn_equals="test-model_arn_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_start_automated_reasoning_policy_build_workflow_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_start_automated_reasoning_policy_test_workflow_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", test_case_ids=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_automated_reasoning_policy("test-policy_arn", {}, name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_automated_reasoning_policy_test_case_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", query_content="test-query_content", confidence_threshold=1.0, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", description="test-description", topic_policy_config={}, content_policy_config={}, word_policy_config={}, sensitive_information_policy_config={}, contextual_grounding_policy_config={}, automated_reasoning_policy_config={}, cross_region_config={}, kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_marketplace_model_endpoint_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_marketplace_model_endpoint("test-endpoint_arn", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_provisioned_model_throughput_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock.async_client", lambda *a, **kw: mock_client)
    await update_provisioned_model_throughput("test-provisioned_model_id", desired_provisioned_model_name="test-desired_provisioned_model_name", desired_model_id="test-desired_model_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

