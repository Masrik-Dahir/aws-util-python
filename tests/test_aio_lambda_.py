"""Tests for aws_util.aio.lambda_ — 100 % line coverage."""
from __future__ import annotations

import base64
import json
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.lambda_ import (
    InvokeResult,
    fan_out,
    invoke,
    invoke_async,
    invoke_with_retry,
    add_layer_version_permission,
    add_permission,
    create_alias,
    create_code_signing_config,
    create_event_source_mapping,
    create_function,
    create_function_url_config,
    delete_alias,
    delete_code_signing_config,
    delete_event_source_mapping,
    delete_function,
    delete_function_code_signing_config,
    delete_function_concurrency,
    delete_function_event_invoke_config,
    delete_function_url_config,
    delete_layer_version,
    delete_provisioned_concurrency_config,
    get_account_settings,
    get_alias,
    get_code_signing_config,
    get_event_source_mapping,
    get_function,
    get_function_code_signing_config,
    get_function_concurrency,
    get_function_configuration,
    get_function_event_invoke_config,
    get_function_recursion_config,
    get_function_url_config,
    get_layer_version,
    get_layer_version_by_arn,
    get_layer_version_policy,
    get_policy,
    get_provisioned_concurrency_config,
    get_runtime_management_config,
    invoke_with_response_stream,
    list_aliases,
    list_code_signing_configs,
    list_event_source_mappings,
    list_function_event_invoke_configs,
    list_function_url_configs,
    list_functions,
    list_functions_by_code_signing_config,
    list_layer_versions,
    list_layers,
    list_provisioned_concurrency_configs,
    list_tags,
    list_versions_by_function,
    publish_layer_version,
    publish_version,
    put_function_code_signing_config,
    put_function_concurrency,
    put_function_event_invoke_config,
    put_function_recursion_config,
    put_provisioned_concurrency_config,
    put_runtime_management_config,
    remove_layer_version_permission,
    remove_permission,
    tag_resource,
    untag_resource,
    update_alias,
    update_code_signing_config,
    update_event_source_mapping,
    update_function_code,
    update_function_configuration,
    update_function_event_invoke_config,
    update_function_url_config,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_client_factory(mock_client):
    """Return a lambda suitable for monkeypatching ``async_client``."""
    return lambda *a, **kw: mock_client


def _invoke_response(
    payload: bytes = b'{"ok": true}',
    status_code: int = 200,
    function_error: str | None = None,
    log_result: str | None = None,
) -> dict:
    resp: dict = {
        "StatusCode": status_code,
        "Payload": payload,
    }
    if function_error:
        resp["FunctionError"] = function_error
    if log_result:
        resp["LogResult"] = base64.b64encode(
            log_result.encode()
        ).decode()
    return resp


# ---------------------------------------------------------------------------
# invoke — success paths
# ---------------------------------------------------------------------------


async def test_invoke_dict_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("my-fn", payload={"key": "val"})
    assert isinstance(result, InvokeResult)
    assert result.status_code == 200
    assert result.payload == {"ok": True}
    assert result.function_error is None
    assert result.log_result is None
    mock_client.call.assert_awaited_once()
    call_kwargs = mock_client.call.call_args
    assert call_kwargs[1]["Payload"] == json.dumps({"key": "val"}).encode()


async def test_invoke_list_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response(
        payload=b"[1,2,3]"
    )
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn", payload=[1, 2, 3])
    assert result.payload == [1, 2, 3]


async def test_invoke_string_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response(
        payload=b'"hello"'
    )
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn", payload="hello")
    assert result.payload == "hello"
    call_kwargs = mock_client.call.call_args
    assert call_kwargs[1]["Payload"] == b"hello"


async def test_invoke_none_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    assert "Payload" not in mock_client.call.call_args[1]


async def test_invoke_with_qualifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    await invoke("fn", qualifier="$LATEST")
    assert mock_client.call.call_args[1]["Qualifier"] == "$LATEST"


async def test_invoke_no_qualifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    await invoke("fn")
    assert "Qualifier" not in mock_client.call.call_args[1]


async def test_invoke_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    await invoke("fn", region_name="eu-west-1")


async def test_invoke_with_log_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response(
        log_result="START RequestId ..."
    )
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn", log_type="Tail")
    assert result.log_result == "START RequestId ..."


async def test_invoke_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response(
        function_error="Unhandled"
    )
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn", payload={"x": 1})
    assert result.function_error == "Unhandled"
    assert not result.succeeded


# ---------------------------------------------------------------------------
# invoke — response payload edge cases
# ---------------------------------------------------------------------------


async def test_invoke_payload_has_read_method(monkeypatch):
    """When Payload has a .read() method (StreamingBody), call it."""

    class FakeStream:
        def read(self):
            return b'{"stream": true}'

    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StatusCode": 200,
        "Payload": FakeStream(),
    }
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    assert result.payload == {"stream": True}


async def test_invoke_payload_is_string(monkeypatch):
    """When Payload is already a str, it gets encoded to bytes."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StatusCode": 200,
        "Payload": '{"str": true}',
    }
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    assert result.payload == {"str": True}


async def test_invoke_payload_empty_bytes(monkeypatch):
    """Empty Payload should parse to None."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StatusCode": 200,
        "Payload": b"",
    }
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    assert result.payload is None


async def test_invoke_payload_invalid_json_bytes(monkeypatch):
    """Non-JSON bytes payload should be decoded as string."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StatusCode": 200,
        "Payload": b"not-valid-json!!!",
    }
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    # It should fall through json decoding to the except branch
    assert result.payload == "not-valid-json!!!"


async def test_invoke_payload_missing(monkeypatch):
    """When Payload key is absent, raw_response is b''."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StatusCode": 200}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke("fn")
    assert result.payload is None


# ---------------------------------------------------------------------------
# invoke — error path
# ---------------------------------------------------------------------------


async def test_invoke_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to invoke Lambda"):
        await invoke("fn", payload={"a": 1})


# ---------------------------------------------------------------------------
# invoke_async
# ---------------------------------------------------------------------------


async def test_invoke_async_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke_async("fn", payload={"x": 1})
    assert result is None
    assert mock_client.call.call_args[1]["InvocationType"] == "Event"


async def test_invoke_async_with_qualifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    await invoke_async("fn", qualifier="v1", region_name="us-west-2")


# ---------------------------------------------------------------------------
# invoke_with_retry — success
# ---------------------------------------------------------------------------


async def test_invoke_with_retry_success_first_try(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke_with_retry("fn", payload={"k": "v"})
    assert result.status_code == 200
    assert mock_client.call.await_count == 1


async def test_invoke_with_retry_success_after_retries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        RuntimeError("transient"),
        RuntimeError("transient"),
        _invoke_response(),
    ]
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    with patch("aws_util.aio.lambda_.asyncio.sleep", new_callable=AsyncMock):
        result = await invoke_with_retry(
            "fn", max_retries=3, backoff_base=0.001
        )
    assert result.status_code == 200


async def test_invoke_with_retry_all_fail(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("always fails")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    with patch("aws_util.aio.lambda_.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(RuntimeError, match="all 4 attempts failed"):
            await invoke_with_retry(
                "fn", max_retries=3, backoff_base=0.001
            )


async def test_invoke_with_retry_optional_params(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    result = await invoke_with_retry(
        "fn",
        qualifier="v2",
        region_name="ap-southeast-1",
    )
    assert result.status_code == 200


# ---------------------------------------------------------------------------
# fan_out
# ---------------------------------------------------------------------------


async def test_fan_out_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    payloads = [{"i": 0}, {"i": 1}, {"i": 2}]
    results = await fan_out("fn", payloads, max_concurrency=2)
    assert len(results) == 3
    for r in results:
        assert isinstance(r, InvokeResult)
        assert r.status_code == 200


async def test_fan_out_empty(monkeypatch):
    mock_client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    results = await fan_out("fn", [])
    assert results == []
    mock_client.call.assert_not_awaited()


async def test_fan_out_with_qualifier_and_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _invoke_response()
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    results = await fan_out(
        "fn",
        [{"a": 1}],
        qualifier="v3",
        region_name="eu-central-1",
    )
    assert len(results) == 1


async def test_fan_out_propagates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api error")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        _mock_client_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to invoke Lambda"):
        await fan_out("fn", [{"x": 1}])


async def test_add_layer_version_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_layer_version_permission("test-layer_name", 1, "test-statement_id", "test-action", "test-principal", )
    mock_client.call.assert_called_once()


async def test_add_layer_version_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_layer_version_permission("test-layer_name", 1, "test-statement_id", "test-action", "test-principal", )


async def test_add_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", )
    mock_client.call.assert_called_once()


async def test_add_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", )


async def test_create_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_alias("test-function_name", "test-name", "test-function_version", )
    mock_client.call.assert_called_once()


async def test_create_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_alias("test-function_name", "test-name", "test-function_version", )


async def test_create_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_code_signing_config({}, )
    mock_client.call.assert_called_once()


async def test_create_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_code_signing_config({}, )


async def test_create_event_source_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_source_mapping("test-function_name", )
    mock_client.call.assert_called_once()


async def test_create_event_source_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_source_mapping("test-function_name", )


async def test_create_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_function("test-function_name", "test-role", {}, )
    mock_client.call.assert_called_once()


async def test_create_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_function("test-function_name", "test-role", {}, )


async def test_create_function_url_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_function_url_config("test-function_name", "test-auth_type", )
    mock_client.call.assert_called_once()


async def test_create_function_url_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_function_url_config("test-function_name", "test-auth_type", )


async def test_delete_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_alias("test-function_name", "test-name", )
    mock_client.call.assert_called_once()


async def test_delete_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_alias("test-function_name", "test-name", )


async def test_delete_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_code_signing_config("test-code_signing_config_arn", )
    mock_client.call.assert_called_once()


async def test_delete_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_code_signing_config("test-code_signing_config_arn", )


async def test_delete_event_source_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_source_mapping("test-uuid", )
    mock_client.call.assert_called_once()


async def test_delete_event_source_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_source_mapping("test-uuid", )


async def test_delete_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_function("test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function("test-function_name", )


async def test_delete_function_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_function_code_signing_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_function_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function_code_signing_config("test-function_name", )


async def test_delete_function_concurrency(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_function_concurrency("test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_function_concurrency_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function_concurrency("test-function_name", )


async def test_delete_function_event_invoke_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_function_event_invoke_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_function_event_invoke_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function_event_invoke_config("test-function_name", )


async def test_delete_function_url_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_function_url_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_function_url_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function_url_config("test-function_name", )


async def test_delete_layer_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_layer_version("test-layer_name", 1, )
    mock_client.call.assert_called_once()


async def test_delete_layer_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_layer_version("test-layer_name", 1, )


async def test_delete_provisioned_concurrency_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_provisioned_concurrency_config("test-function_name", "test-qualifier", )
    mock_client.call.assert_called_once()


async def test_delete_provisioned_concurrency_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_provisioned_concurrency_config("test-function_name", "test-qualifier", )


async def test_get_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_settings()
    mock_client.call.assert_called_once()


async def test_get_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_settings()


async def test_get_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_alias("test-function_name", "test-name", )
    mock_client.call.assert_called_once()


async def test_get_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_alias("test-function_name", "test-name", )


async def test_get_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_code_signing_config("test-code_signing_config_arn", )
    mock_client.call.assert_called_once()


async def test_get_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_code_signing_config("test-code_signing_config_arn", )


async def test_get_event_source_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_event_source_mapping("test-uuid", )
    mock_client.call.assert_called_once()


async def test_get_event_source_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_event_source_mapping("test-uuid", )


async def test_get_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function("test-function_name", )


async def test_get_function_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_code_signing_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_code_signing_config("test-function_name", )


async def test_get_function_concurrency(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_concurrency("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_concurrency_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_concurrency("test-function_name", )


async def test_get_function_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_configuration("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_configuration("test-function_name", )


async def test_get_function_event_invoke_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_event_invoke_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_event_invoke_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_event_invoke_config("test-function_name", )


async def test_get_function_recursion_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_recursion_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_recursion_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_recursion_config("test-function_name", )


async def test_get_function_url_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_function_url_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_function_url_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_function_url_config("test-function_name", )


async def test_get_layer_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_layer_version("test-layer_name", 1, )
    mock_client.call.assert_called_once()


async def test_get_layer_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_layer_version("test-layer_name", 1, )


async def test_get_layer_version_by_arn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_layer_version_by_arn("test-arn", )
    mock_client.call.assert_called_once()


async def test_get_layer_version_by_arn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_layer_version_by_arn("test-arn", )


async def test_get_layer_version_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_layer_version_policy("test-layer_name", 1, )
    mock_client.call.assert_called_once()


async def test_get_layer_version_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_layer_version_policy("test-layer_name", 1, )


async def test_get_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_policy("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_policy("test-function_name", )


async def test_get_provisioned_concurrency_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_provisioned_concurrency_config("test-function_name", "test-qualifier", )
    mock_client.call.assert_called_once()


async def test_get_provisioned_concurrency_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_provisioned_concurrency_config("test-function_name", "test-qualifier", )


async def test_get_runtime_management_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_runtime_management_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_runtime_management_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_runtime_management_config("test-function_name", )


async def test_invoke_with_response_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await invoke_with_response_stream("test-function_name", )
    mock_client.call.assert_called_once()


async def test_invoke_with_response_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await invoke_with_response_stream("test-function_name", )


async def test_list_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_aliases("test-function_name", )
    mock_client.call.assert_called_once()


async def test_list_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_aliases("test-function_name", )


async def test_list_code_signing_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_code_signing_configs()
    mock_client.call.assert_called_once()


async def test_list_code_signing_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_code_signing_configs()


async def test_list_event_source_mappings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_event_source_mappings()
    mock_client.call.assert_called_once()


async def test_list_event_source_mappings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_event_source_mappings()


async def test_list_function_event_invoke_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_function_event_invoke_configs("test-function_name", )
    mock_client.call.assert_called_once()


async def test_list_function_event_invoke_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_function_event_invoke_configs("test-function_name", )


async def test_list_function_url_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_function_url_configs("test-function_name", )
    mock_client.call.assert_called_once()


async def test_list_function_url_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_function_url_configs("test-function_name", )


async def test_list_functions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_functions()
    mock_client.call.assert_called_once()


async def test_list_functions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_functions()


async def test_list_functions_by_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_functions_by_code_signing_config("test-code_signing_config_arn", )
    mock_client.call.assert_called_once()


async def test_list_functions_by_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_functions_by_code_signing_config("test-code_signing_config_arn", )


async def test_list_layer_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_layer_versions("test-layer_name", )
    mock_client.call.assert_called_once()


async def test_list_layer_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_layer_versions("test-layer_name", )


async def test_list_layers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_layers()
    mock_client.call.assert_called_once()


async def test_list_layers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_layers()


async def test_list_provisioned_concurrency_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_provisioned_concurrency_configs("test-function_name", )
    mock_client.call.assert_called_once()


async def test_list_provisioned_concurrency_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_provisioned_concurrency_configs("test-function_name", )


async def test_list_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags("test-resource", )
    mock_client.call.assert_called_once()


async def test_list_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags("test-resource", )


async def test_list_versions_by_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_versions_by_function("test-function_name", )
    mock_client.call.assert_called_once()


async def test_list_versions_by_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_versions_by_function("test-function_name", )


async def test_publish_layer_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_layer_version("test-layer_name", {}, )
    mock_client.call.assert_called_once()


async def test_publish_layer_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_layer_version("test-layer_name", {}, )


async def test_publish_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_version("test-function_name", )
    mock_client.call.assert_called_once()


async def test_publish_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_version("test-function_name", )


async def test_put_function_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_function_code_signing_config("test-code_signing_config_arn", "test-function_name", )
    mock_client.call.assert_called_once()


async def test_put_function_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_function_code_signing_config("test-code_signing_config_arn", "test-function_name", )


async def test_put_function_concurrency(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_function_concurrency("test-function_name", 1, )
    mock_client.call.assert_called_once()


async def test_put_function_concurrency_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_function_concurrency("test-function_name", 1, )


async def test_put_function_event_invoke_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_function_event_invoke_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_put_function_event_invoke_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_function_event_invoke_config("test-function_name", )


async def test_put_function_recursion_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_function_recursion_config("test-function_name", "test-recursive_loop", )
    mock_client.call.assert_called_once()


async def test_put_function_recursion_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_function_recursion_config("test-function_name", "test-recursive_loop", )


async def test_put_provisioned_concurrency_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_provisioned_concurrency_config("test-function_name", "test-qualifier", 1, )
    mock_client.call.assert_called_once()


async def test_put_provisioned_concurrency_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_provisioned_concurrency_config("test-function_name", "test-qualifier", 1, )


async def test_put_runtime_management_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_runtime_management_config("test-function_name", "test-update_runtime_on", )
    mock_client.call.assert_called_once()


async def test_put_runtime_management_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_runtime_management_config("test-function_name", "test-update_runtime_on", )


async def test_remove_layer_version_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_layer_version_permission("test-layer_name", 1, "test-statement_id", )
    mock_client.call.assert_called_once()


async def test_remove_layer_version_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_layer_version_permission("test-layer_name", 1, "test-statement_id", )


async def test_remove_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_permission("test-function_name", "test-statement_id", )
    mock_client.call.assert_called_once()


async def test_remove_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_permission("test-function_name", "test-statement_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource", [], )


async def test_update_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_alias("test-function_name", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_alias("test-function_name", "test-name", )


async def test_update_code_signing_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_code_signing_config("test-code_signing_config_arn", )
    mock_client.call.assert_called_once()


async def test_update_code_signing_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_code_signing_config("test-code_signing_config_arn", )


async def test_update_event_source_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_event_source_mapping("test-uuid", )
    mock_client.call.assert_called_once()


async def test_update_event_source_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_event_source_mapping("test-uuid", )


async def test_update_function_code(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_function_code("test-function_name", )
    mock_client.call.assert_called_once()


async def test_update_function_code_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_function_code("test-function_name", )


async def test_update_function_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_function_configuration("test-function_name", )
    mock_client.call.assert_called_once()


async def test_update_function_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_function_configuration("test-function_name", )


async def test_update_function_event_invoke_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_function_event_invoke_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_update_function_event_invoke_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_function_event_invoke_config("test-function_name", )


async def test_update_function_url_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_function_url_config("test-function_name", )
    mock_client.call.assert_called_once()


async def test_update_function_url_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lambda_.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_function_url_config("test-function_name", )


@pytest.mark.asyncio
async def test_add_layer_version_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import add_layer_version_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await add_layer_version_permission("test-layer_name", "test-version_number", "test-statement_id", "test-action", "test-principal", organization_id="test-organization_id", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_add_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import add_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", source_arn="test-source_arn", source_account=1, event_source_token="test-event_source_token", qualifier="test-qualifier", revision_id="test-revision_id", principal_org_id="test-principal_org_id", function_url_auth_type="test-function_url_auth_type", invoked_via_function_url="test-invoked_via_function_url", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import create_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await create_alias("test-function_name", "test-name", "test-function_version", description="test-description", routing_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_code_signing_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import create_code_signing_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await create_code_signing_config(True, description="test-description", code_signing_policies="test-code_signing_policies", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_source_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import create_event_source_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await create_event_source_mapping("test-function_name", event_source_arn="test-event_source_arn", enabled=True, batch_size=1, filter_criteria="test-filter_criteria", maximum_batching_window_in_seconds=1, parallelization_factor="test-parallelization_factor", starting_position="test-starting_position", starting_position_timestamp="test-starting_position_timestamp", destination_config={}, maximum_record_age_in_seconds=1, bisect_batch_on_function_error="test-bisect_batch_on_function_error", maximum_retry_attempts=1, tags=[{"Key": "k", "Value": "v"}], tumbling_window_in_seconds="test-tumbling_window_in_seconds", topics="test-topics", queues="test-queues", source_access_configurations={}, self_managed_event_source="test-self_managed_event_source", function_response_types="test-function_response_types", amazon_managed_kafka_event_source_config={}, self_managed_kafka_event_source_config={}, scaling_config={}, document_db_event_source_config={}, kms_key_arn="test-kms_key_arn", metrics_config={}, provisioned_poller_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import create_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await create_function("test-function_name", "test-role", "test-code", runtime="test-runtime", handler="test-handler", description="test-description", timeout=1, memory_size=1, publish=True, vpc_config={}, package_type="test-package_type", dead_letter_config={}, environment="test-environment", kms_key_arn="test-kms_key_arn", tracing_config={}, tags=[{"Key": "k", "Value": "v"}], layers="test-layers", file_system_configs={}, image_config={}, code_signing_config_arn={}, architectures="test-architectures", ephemeral_storage="test-ephemeral_storage", snap_start="test-snap_start", logging_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_function_url_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import create_function_url_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await create_function_url_config("test-function_name", "test-auth_type", qualifier="test-qualifier", cors="test-cors", invoke_mode="test-invoke_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import delete_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await delete_function("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import delete_function_event_invoke_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await delete_function_event_invoke_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_function_url_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import delete_function_url_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await delete_function_url_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_function("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_function_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_function_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_function_configuration("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_function_event_invoke_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_function_event_invoke_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_function_url_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_function_url_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_function_url_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_policy("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_runtime_management_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import get_runtime_management_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await get_runtime_management_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_invoke_with_response_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import invoke_with_response_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await invoke_with_response_stream("test-function_name", invocation_type="test-invocation_type", log_type="test-log_type", client_context={}, qualifier="test-qualifier", payload="test-payload", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_aliases("test-function_name", function_version="test-function_version", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_code_signing_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_code_signing_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_code_signing_configs(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_event_source_mappings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_event_source_mappings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_event_source_mappings(event_source_arn="test-event_source_arn", function_name="test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_function_event_invoke_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_function_event_invoke_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_function_event_invoke_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_function_url_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_function_url_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_function_url_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_functions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_functions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_functions(master_region="test-master_region", function_version="test-function_version", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_functions_by_code_signing_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_functions_by_code_signing_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_functions_by_code_signing_config({}, marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_layer_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_layer_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_layer_versions("test-layer_name", compatible_runtime="test-compatible_runtime", marker="test-marker", max_items=1, compatible_architecture="test-compatible_architecture", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_layers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_layers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_layers(compatible_runtime="test-compatible_runtime", marker="test-marker", max_items=1, compatible_architecture="test-compatible_architecture", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_provisioned_concurrency_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_provisioned_concurrency_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_provisioned_concurrency_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_versions_by_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import list_versions_by_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await list_versions_by_function("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_layer_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import publish_layer_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await publish_layer_version("test-layer_name", "test-content", description="test-description", compatible_runtimes="test-compatible_runtimes", license_info="test-license_info", compatible_architectures="test-compatible_architectures", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import publish_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await publish_version("test-function_name", code_sha256="test-code_sha256", description="test-description", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import put_function_event_invoke_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await put_function_event_invoke_config("test-function_name", qualifier="test-qualifier", maximum_retry_attempts=1, maximum_event_age_in_seconds=1, destination_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_runtime_management_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import put_runtime_management_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await put_runtime_management_config("test-function_name", "test-update_runtime_on", qualifier="test-qualifier", runtime_version_arn="test-runtime_version_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_layer_version_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import remove_layer_version_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await remove_layer_version_permission("test-layer_name", "test-version_number", "test-statement_id", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import remove_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await remove_permission("test-function_name", "test-statement_id", qualifier="test-qualifier", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_alias("test-function_name", "test-name", function_version="test-function_version", description="test-description", routing_config={}, revision_id="test-revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_code_signing_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_code_signing_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_code_signing_config({}, description="test-description", allowed_publishers=True, code_signing_policies="test-code_signing_policies", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_event_source_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_event_source_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_event_source_mapping("test-uuid", function_name="test-function_name", enabled=True, batch_size=1, filter_criteria="test-filter_criteria", maximum_batching_window_in_seconds=1, destination_config={}, maximum_record_age_in_seconds=1, bisect_batch_on_function_error="test-bisect_batch_on_function_error", maximum_retry_attempts=1, parallelization_factor="test-parallelization_factor", source_access_configurations={}, tumbling_window_in_seconds="test-tumbling_window_in_seconds", function_response_types="test-function_response_types", scaling_config={}, amazon_managed_kafka_event_source_config={}, self_managed_kafka_event_source_config={}, document_db_event_source_config={}, kms_key_arn="test-kms_key_arn", metrics_config={}, provisioned_poller_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_function_code_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_function_code
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_function_code("test-function_name", zip_file="test-zip_file", s3_bucket="test-s3_bucket", s3_key="test-s3_key", s3_object_version="test-s3_object_version", image_uri="test-image_uri", publish=True, revision_id="test-revision_id", architectures="test-architectures", source_kms_key_arn="test-source_kms_key_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_function_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_function_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_function_configuration("test-function_name", role="test-role", handler="test-handler", description="test-description", timeout=1, memory_size=1, vpc_config={}, environment="test-environment", runtime="test-runtime", dead_letter_config={}, kms_key_arn="test-kms_key_arn", tracing_config={}, revision_id="test-revision_id", layers="test-layers", file_system_configs={}, image_config={}, ephemeral_storage="test-ephemeral_storage", snap_start="test-snap_start", logging_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_function_event_invoke_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_function_event_invoke_config("test-function_name", qualifier="test-qualifier", maximum_retry_attempts=1, maximum_event_age_in_seconds=1, destination_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_function_url_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lambda_ import update_function_url_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lambda_.async_client", lambda *a, **kw: mock_client)
    await update_function_url_config("test-function_name", qualifier="test-qualifier", auth_type="test-auth_type", cors="test-cors", invoke_mode="test-invoke_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()
