"""Tests for aws_util.bedrock module."""
from __future__ import annotations

import json
import pytest
from io import BytesIO
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.bedrock as bedrock_mod
from aws_util.bedrock import (
    BedrockModel,
    InvokeModelResult,
    invoke_model,
    invoke_claude,
    invoke_titan_text,
    chat,
    embed_text,
    stream_invoke_claude,
    list_foundation_models,
    apply_guardrail,
    converse,
    converse_stream,
    count_tokens,
    get_async_invoke,
    invoke_model_with_response_stream,
    list_async_invokes,
    start_async_invoke,
)

REGION = "us-east-1"
CLAUDE_MODEL = "anthropic.claude-3-5-sonnet-20241022-v2:0"
TITAN_MODEL = "amazon.titan-text-express-v1"


def _mock_invoke_response(body_dict: dict) -> dict:
    return {
        "body": BytesIO(json.dumps(body_dict).encode("utf-8")),
        "contentType": "application/json",
    }


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_bedrock_model():
    m = BedrockModel(
        model_id=CLAUDE_MODEL,
        model_name="Claude 3.5 Sonnet",
        provider_name="Anthropic",
        input_modalities=["TEXT"],
        output_modalities=["TEXT"],
        response_streaming_supported=True,
    )
    assert m.model_id == CLAUDE_MODEL
    assert m.response_streaming_supported is True


def test_invoke_model_result():
    r = InvokeModelResult(model_id=CLAUDE_MODEL, body={"text": "hello"})
    assert r.content_type == "application/json"


# ---------------------------------------------------------------------------
# invoke_model
# ---------------------------------------------------------------------------

def test_invoke_model_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = _mock_invoke_response({"result": "ok"})
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    result = invoke_model(CLAUDE_MODEL, {"prompt": "hello"}, region_name=REGION)
    assert isinstance(result, InvokeModelResult)
    assert result.body == {"result": "ok"}


def test_invoke_model_non_json_body(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model.return_value = {
        "body": BytesIO(b"plain text response"),
        "contentType": "text/plain",
    }
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    result = invoke_model(CLAUDE_MODEL, {"prompt": "hello"}, region_name=REGION)
    assert result.body == "plain text response"


def test_invoke_model_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "invalid model"}}, "InvokeModel"
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to invoke Bedrock model"):
        invoke_model(CLAUDE_MODEL, {}, region_name=REGION)


# ---------------------------------------------------------------------------
# invoke_claude
# ---------------------------------------------------------------------------

def test_invoke_claude_success(monkeypatch):
    claude_resp = {
        "content": [{"type": "text", "text": "Hello, world!"}]
    }
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body=claude_resp),
    )
    result = invoke_claude("Say hello", region_name=REGION)
    assert result == "Hello, world!"


def test_invoke_claude_with_system_prompt(monkeypatch):
    claude_resp = {"content": [{"type": "text", "text": "Response"}]}
    called_with = {}

    def fake_invoke(model_id, body, **kw):
        called_with["body"] = body
        return InvokeModelResult(model_id=model_id, body=claude_resp)

    monkeypatch.setattr(bedrock_mod, "invoke_model", fake_invoke)
    invoke_claude("Hello", system="You are a helpful assistant.", region_name=REGION)
    assert "system" in called_with["body"]


def test_invoke_claude_non_dict_body(monkeypatch):
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body="raw text"),
    )
    result = invoke_claude("Hello", region_name=REGION)
    assert result == "raw text"


def test_invoke_claude_empty_content(monkeypatch):
    # When content list is empty, str(body) is returned
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body={"content": []}),
    )
    result = invoke_claude("Hello", region_name=REGION)
    assert isinstance(result, str)
    assert "content" in result


# ---------------------------------------------------------------------------
# invoke_titan_text
# ---------------------------------------------------------------------------

def test_invoke_titan_text_success(monkeypatch):
    titan_resp = {"results": [{"outputText": "Generated text"}]}
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body=titan_resp),
    )
    result = invoke_titan_text("Generate some text", region_name=REGION)
    assert result == "Generated text"


def test_invoke_titan_text_empty_results(monkeypatch):
    # When results list is empty, str(body) is returned
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body={"results": []}),
    )
    result = invoke_titan_text("Hello", region_name=REGION)
    assert isinstance(result, str)
    assert "results" in result


# ---------------------------------------------------------------------------
# chat
# ---------------------------------------------------------------------------

def test_chat_success(monkeypatch):
    chat_resp = {"content": [{"type": "text", "text": "Hi there!"}]}
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body=chat_resp),
    )
    messages = [{"role": "user", "content": "Hello"}]
    result = chat(messages, region_name=REGION)
    assert result == "Hi there!"


def test_chat_with_system(monkeypatch):
    chat_resp = {"content": [{"type": "text", "text": "Response"}]}
    called_with = {}

    def fake_invoke(model_id, body, **kw):
        called_with["body"] = body
        return InvokeModelResult(model_id=model_id, body=chat_resp)

    monkeypatch.setattr(bedrock_mod, "invoke_model", fake_invoke)
    chat([{"role": "user", "content": "Hi"}], system="Be brief.", region_name=REGION)
    assert called_with["body"].get("system") == "Be brief."


# ---------------------------------------------------------------------------
# embed_text
# ---------------------------------------------------------------------------

def test_embed_text_success(monkeypatch):
    embed_resp = {"embedding": [0.1, 0.2, 0.3]}
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body=embed_resp),
    )
    result = embed_text("Hello world", region_name=REGION)
    assert result == [0.1, 0.2, 0.3]


def test_embed_text_non_dict_body(monkeypatch):
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body="not a dict"),
    )
    result = embed_text("Hello", region_name=REGION)
    assert result == []


# ---------------------------------------------------------------------------
# stream_invoke_claude
# ---------------------------------------------------------------------------

def test_stream_invoke_claude_yields_text(monkeypatch):
    chunk_data = json.dumps({
        "type": "content_block_delta",
        "delta": {"type": "text_delta", "text": "hello"},
    }).encode("utf-8")
    mock_stream = [{"chunk": {"bytes": chunk_data}}]
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {"body": mock_stream}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    chunks = list(stream_invoke_claude("Say hello", region_name=REGION))
    assert chunks == ["hello"]


def test_stream_invoke_claude_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.side_effect = ClientError(
        {"Error": {"Code": "ModelNotReadyException", "Message": "not ready"}},
        "InvokeModelWithResponseStream",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stream Bedrock model"):
        list(stream_invoke_claude("Hello", region_name=REGION))


def test_stream_invoke_claude_skips_non_text_delta(monkeypatch):
    chunk_data = json.dumps({
        "type": "message_start",
        "message": {"role": "assistant"},
    }).encode("utf-8")
    mock_stream = [{"chunk": {"bytes": chunk_data}}]
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {"body": mock_stream}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    chunks = list(stream_invoke_claude("Hello", region_name=REGION))
    assert chunks == []


# ---------------------------------------------------------------------------
# list_foundation_models
# ---------------------------------------------------------------------------

def test_list_foundation_models_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_models.return_value = {
        "modelSummaries": [
            {
                "modelId": CLAUDE_MODEL,
                "modelName": "Claude 3.5 Sonnet",
                "providerName": "Anthropic",
                "inputModalities": ["TEXT"],
                "outputModalities": ["TEXT"],
                "responseStreamingSupported": True,
            }
        ]
    }
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_foundation_models(region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], BedrockModel)
    assert result[0].model_id == CLAUDE_MODEL


def test_list_foundation_models_with_provider_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_models.return_value = {"modelSummaries": []}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_foundation_models(provider_name="Anthropic", region_name=REGION)
    assert result == []
    call_kwargs = mock_client.list_foundation_models.call_args[1]
    assert call_kwargs.get("byProvider") == "Anthropic"


def test_list_foundation_models_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_models.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "ListFoundationModels"
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_foundation_models failed"):
        list_foundation_models(region_name=REGION)


def test_chat_empty_content(monkeypatch):
    """Covers chat fallback return str(response_body) when content=[] (line 223)."""
    monkeypatch.setattr(
        bedrock_mod,
        "invoke_model",
        lambda model_id, body, **kw: InvokeModelResult(model_id=model_id, body={"content": []}),
    )
    from aws_util.bedrock import chat
    result = chat([{"role": "user", "content": "hi"}], region_name=REGION)
    assert isinstance(result, str)
    assert "content" in result


def test_stream_invoke_claude_with_system(monkeypatch):
    """Covers stream_invoke_claude system prompt branch (line 287)."""
    import json as _json
    chunk_data = _json.dumps({
        "type": "content_block_delta",
        "delta": {"type": "text_delta", "text": "hi"},
    }).encode("utf-8")
    mock_stream = [{"chunk": {"bytes": chunk_data}}]
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {"body": mock_stream}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    chunks = list(stream_invoke_claude("Say hi", system="Be brief", region_name=REGION))
    assert chunks == ["hi"]
    call_body = _json.loads(mock_client.invoke_model_with_response_stream.call_args[1]["body"])
    assert call_body.get("system") == "Be brief"


def test_stream_invoke_claude_malformed_chunk(monkeypatch):
    """Covers json.JSONDecodeError exception handler in stream_invoke_claude (lines 307-308)."""
    mock_stream = [{"chunk": {"bytes": b"not valid json {"}}]
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {"body": mock_stream}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    chunks = list(stream_invoke_claude("Hello", region_name=REGION))
    assert chunks == []


def test_apply_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_guardrail.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", [], region_name=REGION)
    mock_client.apply_guardrail.assert_called_once()


def test_apply_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_guardrail.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_guardrail",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to apply guardrail"):
        apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", [], region_name=REGION)


def test_converse(monkeypatch):
    mock_client = MagicMock()
    mock_client.converse.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    converse("test-model_id", region_name=REGION)
    mock_client.converse.assert_called_once()


def test_converse_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.converse.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "converse",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to converse"):
        converse("test-model_id", region_name=REGION)


def test_converse_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.converse_stream.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    converse_stream("test-model_id", region_name=REGION)
    mock_client.converse_stream.assert_called_once()


def test_converse_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.converse_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "converse_stream",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to converse stream"):
        converse_stream("test-model_id", region_name=REGION)


def test_count_tokens(monkeypatch):
    mock_client = MagicMock()
    mock_client.count_tokens.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    count_tokens("test-model_id", {}, region_name=REGION)
    mock_client.count_tokens.assert_called_once()


def test_count_tokens_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.count_tokens.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "count_tokens",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to count tokens"):
        count_tokens("test-model_id", {}, region_name=REGION)


def test_get_async_invoke(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_async_invoke.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    get_async_invoke("test-invocation_arn", region_name=REGION)
    mock_client.get_async_invoke.assert_called_once()


def test_get_async_invoke_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_async_invoke.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_async_invoke",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get async invoke"):
        get_async_invoke("test-invocation_arn", region_name=REGION)


def test_invoke_model_with_response_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    invoke_model_with_response_stream("test-model_id", region_name=REGION)
    mock_client.invoke_model_with_response_stream.assert_called_once()


def test_invoke_model_with_response_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "invoke_model_with_response_stream",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to invoke model with response stream"):
        invoke_model_with_response_stream("test-model_id", region_name=REGION)


def test_list_async_invokes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_async_invokes.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    list_async_invokes(region_name=REGION)
    mock_client.list_async_invokes.assert_called_once()


def test_list_async_invokes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_async_invokes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_async_invokes",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list async invokes"):
        list_async_invokes(region_name=REGION)


def test_start_async_invoke(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_async_invoke.return_value = {}
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    start_async_invoke("test-model_id", {}, {}, region_name=REGION)
    mock_client.start_async_invoke.assert_called_once()


def test_start_async_invoke_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_async_invoke.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_async_invoke",
    )
    monkeypatch.setattr(bedrock_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start async invoke"):
        start_async_invoke("test-model_id", {}, {}, region_name=REGION)


def test_apply_guardrail_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import apply_guardrail
    mock_client = MagicMock()
    mock_client.apply_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    apply_guardrail("test-guardrail_identifier", "test-guardrail_version", "test-source", "test-content", output_scope="test-output_scope", region_name="us-east-1")
    mock_client.apply_guardrail.assert_called_once()

def test_converse_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import converse
    mock_client = MagicMock()
    mock_client.converse.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    converse("test-model_id", messages="test-messages", system="test-system", inference_config={}, tool_config={}, guardrail_config={}, additional_model_request_fields="test-additional_model_request_fields", prompt_variables="test-prompt_variables", additional_model_response_field_paths="test-additional_model_response_field_paths", request_metadata="test-request_metadata", performance_config={}, region_name="us-east-1")
    mock_client.converse.assert_called_once()

def test_converse_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import converse_stream
    mock_client = MagicMock()
    mock_client.converse_stream.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    converse_stream("test-model_id", messages="test-messages", system="test-system", inference_config={}, tool_config={}, guardrail_config={}, additional_model_request_fields="test-additional_model_request_fields", prompt_variables="test-prompt_variables", additional_model_response_field_paths="test-additional_model_response_field_paths", request_metadata="test-request_metadata", performance_config={}, region_name="us-east-1")
    mock_client.converse_stream.assert_called_once()

def test_invoke_model_with_response_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import invoke_model_with_response_stream
    mock_client = MagicMock()
    mock_client.invoke_model_with_response_stream.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    invoke_model_with_response_stream("test-model_id", body="test-body", content_type="test-content_type", accept="test-accept", trace="test-trace", guardrail_identifier="test-guardrail_identifier", guardrail_version="test-guardrail_version", performance_config_latency={}, region_name="us-east-1")
    mock_client.invoke_model_with_response_stream.assert_called_once()

def test_list_async_invokes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import list_async_invokes
    mock_client = MagicMock()
    mock_client.list_async_invokes.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_async_invokes(submit_time_after="test-submit_time_after", submit_time_before="test-submit_time_before", status_equals="test-status_equals", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_async_invokes.assert_called_once()

def test_start_async_invoke_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock import start_async_invoke
    mock_client = MagicMock()
    mock_client.start_async_invoke.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    start_async_invoke("test-model_id", "test-model_input", {}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_async_invoke.assert_called_once()
# Generated tests for boto3 wrapper methods
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws_util.bedrock import (
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


def test_batch_delete_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_evaluation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    batch_delete_evaluation_job([], region_name="us-east-1")
    mock_client.batch_delete_evaluation_job.assert_called_once()


def test_batch_delete_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_evaluation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_evaluation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        batch_delete_evaluation_job([], region_name="us-east-1")


def test_cancel_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_automated_reasoning_policy_build_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    cancel_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.cancel_automated_reasoning_policy_build_workflow.assert_called_once()


def test_cancel_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_automated_reasoning_policy_build_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_automated_reasoning_policy_build_workflow",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        cancel_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_create_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy("test-name", region_name="us-east-1")
    mock_client.create_automated_reasoning_policy.assert_called_once()


def test_create_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_automated_reasoning_policy",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_automated_reasoning_policy("test-name", region_name="us-east-1")


def test_create_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy("test-name", description="test-description", client_request_token="test-client_request_token", policy_definition={}, kms_key_id="test-kms_key_id", tags=[], region_name="us-east-1")
    mock_client.create_automated_reasoning_policy.assert_called_once()


def test_create_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", region_name="us-east-1")
    mock_client.create_automated_reasoning_policy_test_case.assert_called_once()


def test_create_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_test_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_automated_reasoning_policy_test_case",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", region_name="us-east-1")


def test_create_automated_reasoning_policy_test_case_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy_test_case("test-policy_arn", "test-guard_content", "test-expected_aggregated_findings_result", query_content="test-query_content", client_request_token="test-client_request_token", confidence_threshold=1.0, region_name="us-east-1")
    mock_client.create_automated_reasoning_policy_test_case.assert_called_once()


def test_create_automated_reasoning_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", region_name="us-east-1")
    mock_client.create_automated_reasoning_policy_version.assert_called_once()


def test_create_automated_reasoning_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_automated_reasoning_policy_version",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", region_name="us-east-1")


def test_create_automated_reasoning_policy_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automated_reasoning_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_automated_reasoning_policy_version("test-policy_arn", "test-last_updated_definition_hash", client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.create_automated_reasoning_policy_version.assert_called_once()


def test_create_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_custom_model("test-model_name", {}, region_name="us-east-1")
    mock_client.create_custom_model.assert_called_once()


def test_create_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_custom_model("test-model_name", {}, region_name="us-east-1")


def test_create_custom_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_custom_model("test-model_name", {}, model_kms_key_arn="test-model_kms_key_arn", role_arn="test-role_arn", model_tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_custom_model.assert_called_once()


def test_create_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model_deployment.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_custom_model_deployment("test-model_deployment_name", "test-model_arn", region_name="us-east-1")
    mock_client.create_custom_model_deployment.assert_called_once()


def test_create_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_model_deployment",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_custom_model_deployment("test-model_deployment_name", "test-model_arn", region_name="us-east-1")


def test_create_custom_model_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_model_deployment.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_custom_model_deployment("test-model_deployment_name", "test-model_arn", description="test-description", tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_custom_model_deployment.assert_called_once()


def test_create_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_evaluation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, region_name="us-east-1")
    mock_client.create_evaluation_job.assert_called_once()


def test_create_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_evaluation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_evaluation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, region_name="us-east-1")


def test_create_evaluation_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_evaluation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_evaluation_job("test-job_name", "test-role_arn", {}, {}, {}, job_description="test-job_description", client_request_token="test-client_request_token", customer_encryption_key_id="test-customer_encryption_key_id", job_tags=[], application_type="test-application_type", region_name="us-east-1")
    mock_client.create_evaluation_job.assert_called_once()


def test_create_foundation_model_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_foundation_model_agreement.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_foundation_model_agreement("test-offer_token", "test-model_id", region_name="us-east-1")
    mock_client.create_foundation_model_agreement.assert_called_once()


def test_create_foundation_model_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_foundation_model_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_foundation_model_agreement",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_foundation_model_agreement("test-offer_token", "test-model_id", region_name="us-east-1")


def test_create_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")
    mock_client.create_guardrail.assert_called_once()


def test_create_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_guardrail",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")


def test_create_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_guardrail("test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", description="test-description", topic_policy_config={}, content_policy_config={}, word_policy_config={}, sensitive_information_policy_config={}, contextual_grounding_policy_config={}, automated_reasoning_policy_config={}, cross_region_config={}, kms_key_id="test-kms_key_id", tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_guardrail.assert_called_once()


def test_create_guardrail_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_guardrail_version("test-guardrail_identifier", region_name="us-east-1")
    mock_client.create_guardrail_version.assert_called_once()


def test_create_guardrail_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_guardrail_version",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_guardrail_version("test-guardrail_identifier", region_name="us-east-1")


def test_create_guardrail_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_guardrail_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_guardrail_version("test-guardrail_identifier", description="test-description", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_guardrail_version.assert_called_once()


def test_create_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_inference_profile.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_inference_profile("test-inference_profile_name", {}, region_name="us-east-1")
    mock_client.create_inference_profile.assert_called_once()


def test_create_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_inference_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_inference_profile",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_inference_profile("test-inference_profile_name", {}, region_name="us-east-1")


def test_create_inference_profile_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_inference_profile.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_inference_profile("test-inference_profile_name", {}, description="test-description", client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.create_inference_profile.assert_called_once()


def test_create_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", region_name="us-east-1")
    mock_client.create_marketplace_model_endpoint.assert_called_once()


def test_create_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", region_name="us-east-1")


def test_create_marketplace_model_endpoint_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_marketplace_model_endpoint("test-model_source_identifier", {}, "test-endpoint_name", accept_eula=True, client_request_token="test-client_request_token", tags=[], region_name="us-east-1")
    mock_client.create_marketplace_model_endpoint.assert_called_once()


def test_create_model_copy_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_copy_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_copy_job("test-source_model_arn", "test-target_model_name", region_name="us-east-1")
    mock_client.create_model_copy_job.assert_called_once()


def test_create_model_copy_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_copy_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_model_copy_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_model_copy_job("test-source_model_arn", "test-target_model_name", region_name="us-east-1")


def test_create_model_copy_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_copy_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_copy_job("test-source_model_arn", "test-target_model_name", model_kms_key_id="test-model_kms_key_id", target_model_tags=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_model_copy_job.assert_called_once()


def test_create_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_customization_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, region_name="us-east-1")
    mock_client.create_model_customization_job.assert_called_once()


def test_create_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_customization_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_model_customization_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, region_name="us-east-1")


def test_create_model_customization_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_customization_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_customization_job("test-job_name", "test-custom_model_name", "test-role_arn", "test-base_model_identifier", {}, {}, client_request_token="test-client_request_token", customization_type="test-customization_type", custom_model_kms_key_id="test-custom_model_kms_key_id", job_tags=[], custom_model_tags=[], validation_data_config={}, hyper_parameters={}, vpc_config={}, customization_config={}, region_name="us-east-1")
    mock_client.create_model_customization_job.assert_called_once()


def test_create_model_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_import_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, region_name="us-east-1")
    mock_client.create_model_import_job.assert_called_once()


def test_create_model_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_model_import_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, region_name="us-east-1")


def test_create_model_import_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_import_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_import_job("test-job_name", "test-imported_model_name", "test-role_arn", {}, job_tags=[], imported_model_tags=[], client_request_token="test-client_request_token", vpc_config={}, imported_model_kms_key_id="test-imported_model_kms_key_id", region_name="us-east-1")
    mock_client.create_model_import_job.assert_called_once()


def test_create_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_invocation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, region_name="us-east-1")
    mock_client.create_model_invocation_job.assert_called_once()


def test_create_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_invocation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_model_invocation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, region_name="us-east-1")


def test_create_model_invocation_job_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model_invocation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_model_invocation_job("test-job_name", "test-role_arn", "test-model_id", {}, {}, client_request_token="test-client_request_token", vpc_config={}, timeout_duration_in_hours=1, tags=[], region_name="us-east-1")
    mock_client.create_model_invocation_job.assert_called_once()


def test_create_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt_router.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_prompt_router("test-prompt_router_name", [], {}, {}, region_name="us-east-1")
    mock_client.create_prompt_router.assert_called_once()


def test_create_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt_router.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_prompt_router",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_prompt_router("test-prompt_router_name", [], {}, {}, region_name="us-east-1")


def test_create_prompt_router_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt_router.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_prompt_router("test-prompt_router_name", [], {}, {}, client_request_token="test-client_request_token", description="test-description", tags=[], region_name="us-east-1")
    mock_client.create_prompt_router.assert_called_once()


def test_create_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", region_name="us-east-1")
    mock_client.create_provisioned_model_throughput.assert_called_once()


def test_create_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_provisioned_model_throughput.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_provisioned_model_throughput",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", region_name="us-east-1")


def test_create_provisioned_model_throughput_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    create_provisioned_model_throughput(1, "test-provisioned_model_name", "test-model_id", client_request_token="test-client_request_token", commitment_duration="test-commitment_duration", tags=[], region_name="us-east-1")
    mock_client.create_provisioned_model_throughput.assert_called_once()


def test_delete_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")
    mock_client.delete_automated_reasoning_policy.assert_called_once()


def test_delete_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_automated_reasoning_policy",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")


def test_delete_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_automated_reasoning_policy("test-policy_arn", force=True, region_name="us-east-1")
    mock_client.delete_automated_reasoning_policy.assert_called_once()


def test_delete_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy_build_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", "test-last_updated_at", region_name="us-east-1")
    mock_client.delete_automated_reasoning_policy_build_workflow.assert_called_once()


def test_delete_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy_build_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_automated_reasoning_policy_build_workflow",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", "test-last_updated_at", region_name="us-east-1")


def test_delete_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-last_updated_at", region_name="us-east-1")
    mock_client.delete_automated_reasoning_policy_test_case.assert_called_once()


def test_delete_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automated_reasoning_policy_test_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_automated_reasoning_policy_test_case",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-last_updated_at", region_name="us-east-1")


def test_delete_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_custom_model("test-model_identifier", region_name="us-east-1")
    mock_client.delete_custom_model.assert_called_once()


def test_delete_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_custom_model("test-model_identifier", region_name="us-east-1")


def test_delete_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_model_deployment.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")
    mock_client.delete_custom_model_deployment.assert_called_once()


def test_delete_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_model_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_model_deployment",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")


def test_delete_foundation_model_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_foundation_model_agreement.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_foundation_model_agreement("test-model_id", region_name="us-east-1")
    mock_client.delete_foundation_model_agreement.assert_called_once()


def test_delete_foundation_model_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_foundation_model_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_foundation_model_agreement",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_foundation_model_agreement("test-model_id", region_name="us-east-1")


def test_delete_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_guardrail("test-guardrail_identifier", region_name="us-east-1")
    mock_client.delete_guardrail.assert_called_once()


def test_delete_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_guardrail.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_guardrail",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_guardrail("test-guardrail_identifier", region_name="us-east-1")


def test_delete_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_guardrail("test-guardrail_identifier", guardrail_version="test-guardrail_version", region_name="us-east-1")
    mock_client.delete_guardrail.assert_called_once()


def test_delete_imported_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_imported_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_imported_model("test-model_identifier", region_name="us-east-1")
    mock_client.delete_imported_model.assert_called_once()


def test_delete_imported_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_imported_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_imported_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_imported_model("test-model_identifier", region_name="us-east-1")


def test_delete_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_inference_profile.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_inference_profile("test-inference_profile_identifier", region_name="us-east-1")
    mock_client.delete_inference_profile.assert_called_once()


def test_delete_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_inference_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_inference_profile",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_inference_profile("test-inference_profile_identifier", region_name="us-east-1")


def test_delete_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.delete_marketplace_model_endpoint.assert_called_once()


def test_delete_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


def test_delete_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_model_invocation_logging_configuration.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_model_invocation_logging_configuration(region_name="us-east-1")
    mock_client.delete_model_invocation_logging_configuration.assert_called_once()


def test_delete_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_model_invocation_logging_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_model_invocation_logging_configuration",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_model_invocation_logging_configuration(region_name="us-east-1")


def test_delete_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt_router.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_prompt_router("test-prompt_router_arn", region_name="us-east-1")
    mock_client.delete_prompt_router.assert_called_once()


def test_delete_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt_router.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_prompt_router",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_prompt_router("test-prompt_router_arn", region_name="us-east-1")


def test_delete_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    delete_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.delete_provisioned_model_throughput.assert_called_once()


def test_delete_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_provisioned_model_throughput.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_provisioned_model_throughput",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


def test_deregister_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    deregister_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.deregister_marketplace_model_endpoint.assert_called_once()


def test_deregister_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        deregister_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


def test_export_automated_reasoning_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_automated_reasoning_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    export_automated_reasoning_policy_version("test-policy_arn", region_name="us-east-1")
    mock_client.export_automated_reasoning_policy_version.assert_called_once()


def test_export_automated_reasoning_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_automated_reasoning_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_automated_reasoning_policy_version",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        export_automated_reasoning_policy_version("test-policy_arn", region_name="us-east-1")


def test_get_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy.assert_called_once()


def test_get_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy("test-policy_arn", region_name="us-east-1")


def test_get_automated_reasoning_policy_annotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_annotations.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_annotations.assert_called_once()


def test_get_automated_reasoning_policy_annotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_annotations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_annotations",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_get_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_build_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_build_workflow.assert_called_once()


def test_get_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_build_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_build_workflow",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_get_automated_reasoning_policy_build_workflow_result_assets(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_build_workflow_result_assets.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_build_workflow_result_assets("test-policy_arn", "test-build_workflow_id", "test-asset_type", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_build_workflow_result_assets.assert_called_once()


def test_get_automated_reasoning_policy_build_workflow_result_assets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_build_workflow_result_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_build_workflow_result_assets",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_build_workflow_result_assets("test-policy_arn", "test-build_workflow_id", "test-asset_type", region_name="us-east-1")


def test_get_automated_reasoning_policy_next_scenario(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_next_scenario.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_next_scenario("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_next_scenario.assert_called_once()


def test_get_automated_reasoning_policy_next_scenario_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_next_scenario.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_next_scenario",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_next_scenario("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_get_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_test_case.assert_called_once()


def test_get_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_test_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_test_case",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", region_name="us-east-1")


def test_get_automated_reasoning_policy_test_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_test_result.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_automated_reasoning_policy_test_result("test-policy_arn", "test-build_workflow_id", "test-test_case_id", region_name="us-east-1")
    mock_client.get_automated_reasoning_policy_test_result.assert_called_once()


def test_get_automated_reasoning_policy_test_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automated_reasoning_policy_test_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_reasoning_policy_test_result",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_automated_reasoning_policy_test_result("test-policy_arn", "test-build_workflow_id", "test-test_case_id", region_name="us-east-1")


def test_get_custom_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_custom_model("test-model_identifier", region_name="us-east-1")
    mock_client.get_custom_model.assert_called_once()


def test_get_custom_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_custom_model("test-model_identifier", region_name="us-east-1")


def test_get_custom_model_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_model_deployment.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")
    mock_client.get_custom_model_deployment.assert_called_once()


def test_get_custom_model_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_model_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_model_deployment",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_custom_model_deployment("test-custom_model_deployment_identifier", region_name="us-east-1")


def test_get_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_evaluation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_evaluation_job("test-job_identifier", region_name="us-east-1")
    mock_client.get_evaluation_job.assert_called_once()


def test_get_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_evaluation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_evaluation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_evaluation_job("test-job_identifier", region_name="us-east-1")


def test_get_foundation_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_foundation_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_foundation_model("test-model_identifier", region_name="us-east-1")
    mock_client.get_foundation_model.assert_called_once()


def test_get_foundation_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_foundation_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_foundation_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_foundation_model("test-model_identifier", region_name="us-east-1")


def test_get_foundation_model_availability(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_foundation_model_availability.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_foundation_model_availability("test-model_id", region_name="us-east-1")
    mock_client.get_foundation_model_availability.assert_called_once()


def test_get_foundation_model_availability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_foundation_model_availability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_foundation_model_availability",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_foundation_model_availability("test-model_id", region_name="us-east-1")


def test_get_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_guardrail("test-guardrail_identifier", region_name="us-east-1")
    mock_client.get_guardrail.assert_called_once()


def test_get_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_guardrail.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_guardrail",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_guardrail("test-guardrail_identifier", region_name="us-east-1")


def test_get_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_guardrail("test-guardrail_identifier", guardrail_version="test-guardrail_version", region_name="us-east-1")
    mock_client.get_guardrail.assert_called_once()


def test_get_imported_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_imported_model.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_imported_model("test-model_identifier", region_name="us-east-1")
    mock_client.get_imported_model.assert_called_once()


def test_get_imported_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_imported_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_imported_model",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_imported_model("test-model_identifier", region_name="us-east-1")


def test_get_inference_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inference_profile.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_inference_profile("test-inference_profile_identifier", region_name="us-east-1")
    mock_client.get_inference_profile.assert_called_once()


def test_get_inference_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inference_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_inference_profile",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_inference_profile("test-inference_profile_identifier", region_name="us-east-1")


def test_get_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")
    mock_client.get_marketplace_model_endpoint.assert_called_once()


def test_get_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_marketplace_model_endpoint("test-endpoint_arn", region_name="us-east-1")


def test_get_model_copy_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_copy_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_model_copy_job("test-job_arn", region_name="us-east-1")
    mock_client.get_model_copy_job.assert_called_once()


def test_get_model_copy_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_copy_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_copy_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_copy_job("test-job_arn", region_name="us-east-1")


def test_get_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_customization_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_model_customization_job("test-job_identifier", region_name="us-east-1")
    mock_client.get_model_customization_job.assert_called_once()


def test_get_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_customization_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_customization_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_customization_job("test-job_identifier", region_name="us-east-1")


def test_get_model_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_import_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_model_import_job("test-job_identifier", region_name="us-east-1")
    mock_client.get_model_import_job.assert_called_once()


def test_get_model_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_import_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_import_job("test-job_identifier", region_name="us-east-1")


def test_get_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_invocation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_model_invocation_job("test-job_identifier", region_name="us-east-1")
    mock_client.get_model_invocation_job.assert_called_once()


def test_get_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_invocation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_invocation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_invocation_job("test-job_identifier", region_name="us-east-1")


def test_get_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_invocation_logging_configuration.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_model_invocation_logging_configuration(region_name="us-east-1")
    mock_client.get_model_invocation_logging_configuration.assert_called_once()


def test_get_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_invocation_logging_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_invocation_logging_configuration",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_invocation_logging_configuration(region_name="us-east-1")


def test_get_prompt_router(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt_router.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_prompt_router("test-prompt_router_arn", region_name="us-east-1")
    mock_client.get_prompt_router.assert_called_once()


def test_get_prompt_router_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt_router.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_prompt_router",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_prompt_router("test-prompt_router_arn", region_name="us-east-1")


def test_get_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.get_provisioned_model_throughput.assert_called_once()


def test_get_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_provisioned_model_throughput.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_provisioned_model_throughput",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


def test_get_use_case_for_model_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_use_case_for_model_access.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    get_use_case_for_model_access(region_name="us-east-1")
    mock_client.get_use_case_for_model_access.assert_called_once()


def test_get_use_case_for_model_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_use_case_for_model_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_use_case_for_model_access",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_use_case_for_model_access(region_name="us-east-1")


def test_list_automated_reasoning_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policies.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policies(region_name="us-east-1")
    mock_client.list_automated_reasoning_policies.assert_called_once()


def test_list_automated_reasoning_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automated_reasoning_policies",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_automated_reasoning_policies(region_name="us-east-1")


def test_list_automated_reasoning_policies_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policies.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policies(policy_arn="test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automated_reasoning_policies.assert_called_once()


def test_list_automated_reasoning_policy_build_workflows(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_build_workflows.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_build_workflows("test-policy_arn", region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_build_workflows.assert_called_once()


def test_list_automated_reasoning_policy_build_workflows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_build_workflows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automated_reasoning_policy_build_workflows",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_automated_reasoning_policy_build_workflows("test-policy_arn", region_name="us-east-1")


def test_list_automated_reasoning_policy_build_workflows_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_build_workflows.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_build_workflows("test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_build_workflows.assert_called_once()


def test_list_automated_reasoning_policy_test_cases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_cases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_test_cases("test-policy_arn", region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_test_cases.assert_called_once()


def test_list_automated_reasoning_policy_test_cases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_cases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automated_reasoning_policy_test_cases",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_automated_reasoning_policy_test_cases("test-policy_arn", region_name="us-east-1")


def test_list_automated_reasoning_policy_test_cases_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_cases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_test_cases("test-policy_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_test_cases.assert_called_once()


def test_list_automated_reasoning_policy_test_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_results.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_test_results.assert_called_once()


def test_list_automated_reasoning_policy_test_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automated_reasoning_policy_test_results",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_list_automated_reasoning_policy_test_results_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automated_reasoning_policy_test_results.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_automated_reasoning_policy_test_results("test-policy_arn", "test-build_workflow_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automated_reasoning_policy_test_results.assert_called_once()


def test_list_custom_model_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_model_deployments.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_custom_model_deployments(region_name="us-east-1")
    mock_client.list_custom_model_deployments.assert_called_once()


def test_list_custom_model_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_model_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_model_deployments",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_custom_model_deployments(region_name="us-east-1")


def test_list_custom_model_deployments_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_model_deployments.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_custom_model_deployments(created_before="test-created_before", created_after="test-created_after", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", status_equals="test-status_equals", model_arn_equals="test-model_arn_equals", region_name="us-east-1")
    mock_client.list_custom_model_deployments.assert_called_once()


def test_list_custom_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_models.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_custom_models(region_name="us-east-1")
    mock_client.list_custom_models.assert_called_once()


def test_list_custom_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_models",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_custom_models(region_name="us-east-1")


def test_list_custom_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_models.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_custom_models(creation_time_before="test-creation_time_before", creation_time_after="test-creation_time_after", name_contains="test-name_contains", base_model_arn_equals="test-base_model_arn_equals", foundation_model_arn_equals="test-foundation_model_arn_equals", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", is_owned=True, model_status="test-model_status", region_name="us-east-1")
    mock_client.list_custom_models.assert_called_once()


def test_list_evaluation_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_evaluation_jobs(region_name="us-east-1")
    mock_client.list_evaluation_jobs.assert_called_once()


def test_list_evaluation_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_evaluation_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_evaluation_jobs(region_name="us-east-1")


def test_list_evaluation_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_evaluation_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", application_type_equals="test-application_type_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_evaluation_jobs.assert_called_once()


def test_list_foundation_model_agreement_offers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_model_agreement_offers.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_foundation_model_agreement_offers("test-model_id", region_name="us-east-1")
    mock_client.list_foundation_model_agreement_offers.assert_called_once()


def test_list_foundation_model_agreement_offers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_model_agreement_offers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_foundation_model_agreement_offers",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_foundation_model_agreement_offers("test-model_id", region_name="us-east-1")


def test_list_foundation_model_agreement_offers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_foundation_model_agreement_offers.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_foundation_model_agreement_offers("test-model_id", offer_type="test-offer_type", region_name="us-east-1")
    mock_client.list_foundation_model_agreement_offers.assert_called_once()


def test_list_guardrails(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_guardrails(region_name="us-east-1")
    mock_client.list_guardrails.assert_called_once()


def test_list_guardrails_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_guardrails.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_guardrails",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_guardrails(region_name="us-east-1")


def test_list_guardrails_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_guardrails.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_guardrails(guardrail_identifier="test-guardrail_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_guardrails.assert_called_once()


def test_list_imported_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imported_models.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_imported_models(region_name="us-east-1")
    mock_client.list_imported_models.assert_called_once()


def test_list_imported_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imported_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_imported_models",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_imported_models(region_name="us-east-1")


def test_list_imported_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imported_models.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_imported_models(creation_time_before="test-creation_time_before", creation_time_after="test-creation_time_after", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_imported_models.assert_called_once()


def test_list_inference_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_inference_profiles.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_inference_profiles(region_name="us-east-1")
    mock_client.list_inference_profiles.assert_called_once()


def test_list_inference_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_inference_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_inference_profiles",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_inference_profiles(region_name="us-east-1")


def test_list_inference_profiles_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_inference_profiles.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_inference_profiles(max_results=1, next_token="test-next_token", type_equals="test-type_equals", region_name="us-east-1")
    mock_client.list_inference_profiles.assert_called_once()


def test_list_marketplace_model_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_marketplace_model_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_marketplace_model_endpoints(region_name="us-east-1")
    mock_client.list_marketplace_model_endpoints.assert_called_once()


def test_list_marketplace_model_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_marketplace_model_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_marketplace_model_endpoints",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_marketplace_model_endpoints(region_name="us-east-1")


def test_list_marketplace_model_endpoints_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_marketplace_model_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_marketplace_model_endpoints(max_results=1, next_token="test-next_token", model_source_equals="test-model_source_equals", region_name="us-east-1")
    mock_client.list_marketplace_model_endpoints.assert_called_once()


def test_list_model_copy_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_copy_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_copy_jobs(region_name="us-east-1")
    mock_client.list_model_copy_jobs.assert_called_once()


def test_list_model_copy_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_copy_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_model_copy_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_model_copy_jobs(region_name="us-east-1")


def test_list_model_copy_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_copy_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_copy_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", source_account_equals="test-source_account_equals", source_model_arn_equals="test-source_model_arn_equals", target_model_name_contains="test-target_model_name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_model_copy_jobs.assert_called_once()


def test_list_model_customization_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_customization_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_customization_jobs(region_name="us-east-1")
    mock_client.list_model_customization_jobs.assert_called_once()


def test_list_model_customization_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_customization_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_model_customization_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_model_customization_jobs(region_name="us-east-1")


def test_list_model_customization_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_customization_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_customization_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_model_customization_jobs.assert_called_once()


def test_list_model_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_import_jobs(region_name="us-east-1")
    mock_client.list_model_import_jobs.assert_called_once()


def test_list_model_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_model_import_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_model_import_jobs(region_name="us-east-1")


def test_list_model_import_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_import_jobs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_model_import_jobs.assert_called_once()


def test_list_model_invocation_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_invocation_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_invocation_jobs(region_name="us-east-1")
    mock_client.list_model_invocation_jobs.assert_called_once()


def test_list_model_invocation_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_invocation_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_model_invocation_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_model_invocation_jobs(region_name="us-east-1")


def test_list_model_invocation_jobs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_model_invocation_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_model_invocation_jobs(submit_time_after="test-submit_time_after", submit_time_before="test-submit_time_before", status_equals="test-status_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_model_invocation_jobs.assert_called_once()


def test_list_prompt_routers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompt_routers.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_prompt_routers(region_name="us-east-1")
    mock_client.list_prompt_routers.assert_called_once()


def test_list_prompt_routers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompt_routers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_prompt_routers",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_prompt_routers(region_name="us-east-1")


def test_list_prompt_routers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompt_routers.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_prompt_routers(max_results=1, next_token="test-next_token", type="test-type", region_name="us-east-1")
    mock_client.list_prompt_routers.assert_called_once()


def test_list_provisioned_model_throughputs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_provisioned_model_throughputs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_provisioned_model_throughputs(region_name="us-east-1")
    mock_client.list_provisioned_model_throughputs.assert_called_once()


def test_list_provisioned_model_throughputs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_provisioned_model_throughputs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_provisioned_model_throughputs",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_provisioned_model_throughputs(region_name="us-east-1")


def test_list_provisioned_model_throughputs_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_provisioned_model_throughputs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_provisioned_model_throughputs(creation_time_after="test-creation_time_after", creation_time_before="test-creation_time_before", status_equals="test-status_equals", model_arn_equals="test-model_arn_equals", name_contains="test-name_contains", max_results=1, next_token="test-next_token", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_provisioned_model_throughputs.assert_called_once()


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        list_tags_for_resource("test-resource_arn", region_name="us-east-1")


def test_put_model_invocation_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_model_invocation_logging_configuration.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    put_model_invocation_logging_configuration({}, region_name="us-east-1")
    mock_client.put_model_invocation_logging_configuration.assert_called_once()


def test_put_model_invocation_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_model_invocation_logging_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_model_invocation_logging_configuration",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_model_invocation_logging_configuration({}, region_name="us-east-1")


def test_put_use_case_for_model_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_use_case_for_model_access.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    put_use_case_for_model_access("test-form_data", region_name="us-east-1")
    mock_client.put_use_case_for_model_access.assert_called_once()


def test_put_use_case_for_model_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_use_case_for_model_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_use_case_for_model_access",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_use_case_for_model_access("test-form_data", region_name="us-east-1")


def test_register_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    register_marketplace_model_endpoint("test-endpoint_identifier", "test-model_source_identifier", region_name="us-east-1")
    mock_client.register_marketplace_model_endpoint.assert_called_once()


def test_register_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        register_marketplace_model_endpoint("test-endpoint_identifier", "test-model_source_identifier", region_name="us-east-1")


def test_start_automated_reasoning_policy_build_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_build_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, region_name="us-east-1")
    mock_client.start_automated_reasoning_policy_build_workflow.assert_called_once()


def test_start_automated_reasoning_policy_build_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_build_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_automated_reasoning_policy_build_workflow",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, region_name="us-east-1")


def test_start_automated_reasoning_policy_build_workflow_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_build_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    start_automated_reasoning_policy_build_workflow("test-policy_arn", "test-build_workflow_type", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_automated_reasoning_policy_build_workflow.assert_called_once()


def test_start_automated_reasoning_policy_test_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_test_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")
    mock_client.start_automated_reasoning_policy_test_workflow.assert_called_once()


def test_start_automated_reasoning_policy_test_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_test_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_automated_reasoning_policy_test_workflow",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", region_name="us-east-1")


def test_start_automated_reasoning_policy_test_workflow_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automated_reasoning_policy_test_workflow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    start_automated_reasoning_policy_test_workflow("test-policy_arn", "test-build_workflow_id", test_case_ids=[], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_automated_reasoning_policy_test_workflow.assert_called_once()


def test_stop_evaluation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_evaluation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    stop_evaluation_job("test-job_identifier", region_name="us-east-1")
    mock_client.stop_evaluation_job.assert_called_once()


def test_stop_evaluation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_evaluation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_evaluation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        stop_evaluation_job("test-job_identifier", region_name="us-east-1")


def test_stop_model_customization_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_model_customization_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    stop_model_customization_job("test-job_identifier", region_name="us-east-1")
    mock_client.stop_model_customization_job.assert_called_once()


def test_stop_model_customization_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_model_customization_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_model_customization_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        stop_model_customization_job("test-job_identifier", region_name="us-east-1")


def test_stop_model_invocation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_model_invocation_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    stop_model_invocation_job("test-job_identifier", region_name="us-east-1")
    mock_client.stop_model_invocation_job.assert_called_once()


def test_stop_model_invocation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_model_invocation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_model_invocation_job",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        stop_model_invocation_job("test-job_identifier", region_name="us-east-1")


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        tag_resource("test-resource_arn", [], region_name="us-east-1")


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        untag_resource("test-resource_arn", [], region_name="us-east-1")


def test_update_automated_reasoning_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_automated_reasoning_policy("test-policy_arn", {}, region_name="us-east-1")
    mock_client.update_automated_reasoning_policy.assert_called_once()


def test_update_automated_reasoning_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automated_reasoning_policy",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_automated_reasoning_policy("test-policy_arn", {}, region_name="us-east-1")


def test_update_automated_reasoning_policy_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_automated_reasoning_policy("test-policy_arn", {}, name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_automated_reasoning_policy.assert_called_once()


def test_update_automated_reasoning_policy_annotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy_annotations.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", [], "test-last_updated_annotation_set_hash", region_name="us-east-1")
    mock_client.update_automated_reasoning_policy_annotations.assert_called_once()


def test_update_automated_reasoning_policy_annotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy_annotations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automated_reasoning_policy_annotations",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_automated_reasoning_policy_annotations("test-policy_arn", "test-build_workflow_id", [], "test-last_updated_annotation_set_hash", region_name="us-east-1")


def test_update_automated_reasoning_policy_test_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", region_name="us-east-1")
    mock_client.update_automated_reasoning_policy_test_case.assert_called_once()


def test_update_automated_reasoning_policy_test_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy_test_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automated_reasoning_policy_test_case",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", region_name="us-east-1")


def test_update_automated_reasoning_policy_test_case_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automated_reasoning_policy_test_case.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_automated_reasoning_policy_test_case("test-policy_arn", "test-test_case_id", "test-guard_content", "test-last_updated_at", "test-expected_aggregated_findings_result", query_content="test-query_content", confidence_threshold=1.0, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_automated_reasoning_policy_test_case.assert_called_once()


def test_update_guardrail(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")
    mock_client.update_guardrail.assert_called_once()


def test_update_guardrail_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_guardrail.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_guardrail",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", region_name="us-east-1")


def test_update_guardrail_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_guardrail.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_guardrail("test-guardrail_identifier", "test-name", "test-blocked_input_messaging", "test-blocked_outputs_messaging", description="test-description", topic_policy_config={}, content_policy_config={}, word_policy_config={}, sensitive_information_policy_config={}, contextual_grounding_policy_config={}, automated_reasoning_policy_config={}, cross_region_config={}, kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.update_guardrail.assert_called_once()


def test_update_marketplace_model_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_marketplace_model_endpoint("test-endpoint_arn", {}, region_name="us-east-1")
    mock_client.update_marketplace_model_endpoint.assert_called_once()


def test_update_marketplace_model_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_marketplace_model_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_marketplace_model_endpoint",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_marketplace_model_endpoint("test-endpoint_arn", {}, region_name="us-east-1")


def test_update_marketplace_model_endpoint_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_marketplace_model_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_marketplace_model_endpoint("test-endpoint_arn", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_marketplace_model_endpoint.assert_called_once()


def test_update_provisioned_model_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")
    mock_client.update_provisioned_model_throughput.assert_called_once()


def test_update_provisioned_model_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_provisioned_model_throughput.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_provisioned_model_throughput",
    )
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_provisioned_model_throughput("test-provisioned_model_id", region_name="us-east-1")


def test_update_provisioned_model_throughput_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_provisioned_model_throughput.return_value = {}
    monkeypatch.setattr("aws_util.bedrock.get_client", lambda *a, **kw: mock_client)
    update_provisioned_model_throughput("test-provisioned_model_id", desired_provisioned_model_name="test-desired_provisioned_model_name", desired_model_id="test-desired_model_id", region_name="us-east-1")
    mock_client.update_provisioned_model_throughput.assert_called_once()


