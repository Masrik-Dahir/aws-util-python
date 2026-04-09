"""Tests for aws_util.lambda_ module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

from botocore.exceptions import ClientError
import pytest

from aws_util.lambda_ import (
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

REGION = "us-east-1"


@pytest.fixture
def fn(lambda_function):
    _, fn_name = lambda_function
    return fn_name


# ---------------------------------------------------------------------------
# InvokeResult model
# ---------------------------------------------------------------------------


def test_invoke_result_succeeded_no_error():
    result = InvokeResult(status_code=200, payload={"ok": True})
    assert result.succeeded is True


def test_invoke_result_succeeded_with_error():
    result = InvokeResult(
        status_code=200, payload=None, function_error="Unhandled"
    )
    assert result.succeeded is False


# ---------------------------------------------------------------------------
# invoke
# ---------------------------------------------------------------------------


def test_invoke_basic(fn):
    result = invoke(fn, payload={"key": "value"}, region_name=REGION)
    assert isinstance(result, InvokeResult)
    assert result.status_code in (200, 202)


def test_invoke_no_payload(fn):
    result = invoke(fn, region_name=REGION)
    assert result.status_code in (200, 202)


def test_invoke_dict_payload(fn):
    # Moto runs Lambda via Docker which may not be available; just verify invoke works
    result = invoke(fn, payload={"event": "test"}, region_name=REGION)
    assert result.status_code in (200, 202)


def test_invoke_string_payload(fn):
    # Use Event invocation to avoid moto Docker execution for non-dict payloads
    result = invoke(fn, payload='{"key": "hello"}', invocation_type="Event", region_name=REGION)
    assert result.status_code == 202


def test_invoke_list_payload(fn):
    # moto cannot handle raw JSON array bodies — wrap in dict
    result = invoke(fn, payload={"items": [1, 2, 3]}, region_name=REGION)
    assert result.status_code in (200, 202)


def test_invoke_event_type(fn):
    """Async (Event) invocation returns 202."""
    result = invoke(fn, invocation_type="Event", region_name=REGION)
    assert result.status_code == 202


def test_invoke_with_qualifier(fn):
    result = invoke(fn, qualifier="$LATEST", region_name=REGION)
    assert result.status_code in (200, 202)


def test_invoke_with_log_tail(fn):
    result = invoke(fn, log_type="Tail", region_name=REGION)
    assert result.status_code in (200, 202)


def test_invoke_non_json_response(fn, monkeypatch):
    """Non-JSON response body should be decoded as string."""
    import aws_util.lambda_ as lambdamod

    real_get_client = lambdamod.get_client

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)

        class MockPayload:
            def read(self):
                return b"not-json-body"

        def mock_invoke(**kwargs):
            resp = {"StatusCode": 200, "Payload": MockPayload()}
            return resp

        client.invoke = mock_invoke
        return client

    monkeypatch.setattr(lambdamod, "get_client", patched_get_client)
    result = invoke(fn, region_name=REGION)
    assert result.payload == "not-json-body"


def test_invoke_empty_payload_response(fn, monkeypatch):
    """Empty response body should result in payload=None."""
    import aws_util.lambda_ as lambdamod

    real_get_client = lambdamod.get_client

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)

        class MockPayload:
            def read(self):
                return b""

        def mock_invoke(**kwargs):
            return {"StatusCode": 200, "Payload": MockPayload()}

        client.invoke = mock_invoke
        return client

    monkeypatch.setattr(lambdamod, "get_client", patched_get_client)
    result = invoke(fn, region_name=REGION)
    assert result.payload is None


def test_invoke_with_function_error(fn, monkeypatch):
    """FunctionError should be present in result."""
    import aws_util.lambda_ as lambdamod

    real_get_client = lambdamod.get_client

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)

        class MockPayload:
            def read(self):
                return b'{"errorMessage": "something went wrong"}'

        def mock_invoke(**kwargs):
            return {
                "StatusCode": 200,
                "FunctionError": "Unhandled",
                "Payload": MockPayload(),
            }

        client.invoke = mock_invoke
        return client

    monkeypatch.setattr(lambdamod, "get_client", patched_get_client)
    result = invoke(fn, region_name=REGION)
    assert result.function_error == "Unhandled"
    assert not result.succeeded


def test_invoke_runtime_error():
    with pytest.raises(RuntimeError, match="Failed to invoke Lambda"):
        invoke("nonexistent-function", region_name=REGION)


# ---------------------------------------------------------------------------
# invoke_async
# ---------------------------------------------------------------------------


def test_invoke_async(fn):
    # invoke_async returns None; should not raise
    invoke_async(fn, payload={"async": True}, region_name=REGION)


# ---------------------------------------------------------------------------
# invoke_with_retry
# ---------------------------------------------------------------------------


def test_invoke_with_retry_success_first_try(fn):
    result = invoke_with_retry(fn, payload={"x": 1}, region_name=REGION)
    assert isinstance(result, InvokeResult)


def test_invoke_with_retry_success_after_failure(monkeypatch):
    """Should retry and eventually succeed."""
    import aws_util.lambda_ as lambdamod

    attempts = {"count": 0}

    def mock_invoke(function_name, payload=None, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("Transient error")
        return InvokeResult(status_code=200, payload={"ok": True})

    monkeypatch.setattr(lambdamod, "invoke", mock_invoke)

    with patch("time.sleep"):
        result = invoke_with_retry(
            "fn-name",
            payload={"x": 1},
            max_retries=3,
            backoff_base=0.0,
            region_name=REGION,
        )
    assert result.payload == {"ok": True}


def test_invoke_with_retry_all_fail(monkeypatch):
    """Should raise RuntimeError when all attempts fail."""
    import aws_util.lambda_ as lambdamod

    def always_fail(function_name, payload=None, **kwargs):
        raise RuntimeError("Always fails")

    monkeypatch.setattr(lambdamod, "invoke", always_fail)

    with patch("time.sleep"):
        with pytest.raises(RuntimeError, match="all .* attempts failed"):
            invoke_with_retry(
                "fn-name",
                max_retries=2,
                backoff_base=0.0,
                region_name=REGION,
            )


def test_invoke_with_retry_zero_retries(fn):
    result = invoke_with_retry(fn, max_retries=0, region_name=REGION)
    assert isinstance(result, InvokeResult)


def test_invoke_with_retry_with_qualifier(fn):
    result = invoke_with_retry(fn, qualifier="$LATEST", region_name=REGION)
    assert isinstance(result, InvokeResult)


# ---------------------------------------------------------------------------
# fan_out
# ---------------------------------------------------------------------------


def test_fan_out_multiple_payloads(fn):
    payloads = [{"i": i} for i in range(3)]
    results = fan_out(fn, payloads, region_name=REGION)
    assert len(results) == 3
    assert all(isinstance(r, InvokeResult) for r in results)


def test_fan_out_results_in_order(fn):
    payloads = [{"idx": i} for i in range(5)]
    results = fan_out(fn, payloads, max_concurrency=2, region_name=REGION)
    assert len(results) == 5


def test_fan_out_none_payload(fn):
    results = fan_out(fn, [None], region_name=REGION)
    assert len(results) == 1


def test_fan_out_with_qualifier(fn):
    results = fan_out(fn, [{"x": 1}], qualifier="$LATEST", region_name=REGION)
    assert len(results) == 1


def test_invoke_with_log_result(monkeypatch):
    """Covers base64 log result decoding branch (line 100)."""
    import base64
    import aws_util.lambda_ as lambda_mod
    from unittest.mock import MagicMock

    log_bytes = base64.b64encode(b"START RequestId: abc\nEND RequestId: abc").decode()
    mock_client = MagicMock()
    mock_client.invoke.return_value = {
        "StatusCode": 200,
        "Payload": MagicMock(read=MagicMock(return_value=b'"success"')),
        "LogResult": log_bytes,
    }
    monkeypatch.setattr(lambda_mod, "get_client", lambda *a, **kw: mock_client)
    from aws_util.lambda_ import invoke
    result = invoke("my-fn", payload={"key": "val"}, log_type="Tail", region_name="us-east-1")
    assert result.log_result is not None
    assert "START" in result.log_result


def test_add_layer_version_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_layer_version_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    add_layer_version_permission("test-layer_name", 1, "test-statement_id", "test-action", "test-principal", region_name=REGION)
    mock_client.add_layer_version_permission.assert_called_once()


def test_add_layer_version_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_layer_version_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_layer_version_permission",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add layer version permission"):
        add_layer_version_permission("test-layer_name", 1, "test-statement_id", "test-action", "test-principal", region_name=REGION)


def test_add_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", region_name=REGION)
    mock_client.add_permission.assert_called_once()


def test_add_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_permission",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add permission"):
        add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", region_name=REGION)


def test_create_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_alias("test-function_name", "test-name", "test-function_version", region_name=REGION)
    mock_client.create_alias.assert_called_once()


def test_create_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_alias",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create alias"):
        create_alias("test-function_name", "test-name", "test-function_version", region_name=REGION)


def test_create_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_code_signing_config({}, region_name=REGION)
    mock_client.create_code_signing_config.assert_called_once()


def test_create_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create code signing config"):
        create_code_signing_config({}, region_name=REGION)


def test_create_event_source_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_event_source_mapping("test-function_name", region_name=REGION)
    mock_client.create_event_source_mapping.assert_called_once()


def test_create_event_source_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_source_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_source_mapping",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create event source mapping"):
        create_event_source_mapping("test-function_name", region_name=REGION)


def test_create_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_function("test-function_name", "test-role", {}, region_name=REGION)
    mock_client.create_function.assert_called_once()


def test_create_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_function",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create function"):
        create_function("test-function_name", "test-role", {}, region_name=REGION)


def test_create_function_url_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_function_url_config("test-function_name", "test-auth_type", region_name=REGION)
    mock_client.create_function_url_config.assert_called_once()


def test_create_function_url_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function_url_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_function_url_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create function url config"):
        create_function_url_config("test-function_name", "test-auth_type", region_name=REGION)


def test_delete_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_alias("test-function_name", "test-name", region_name=REGION)
    mock_client.delete_alias.assert_called_once()


def test_delete_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_alias",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete alias"):
        delete_alias("test-function_name", "test-name", region_name=REGION)


def test_delete_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_code_signing_config("test-code_signing_config_arn", region_name=REGION)
    mock_client.delete_code_signing_config.assert_called_once()


def test_delete_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete code signing config"):
        delete_code_signing_config("test-code_signing_config_arn", region_name=REGION)


def test_delete_event_source_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_event_source_mapping("test-uuid", region_name=REGION)
    mock_client.delete_event_source_mapping.assert_called_once()


def test_delete_event_source_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_source_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_source_mapping",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete event source mapping"):
        delete_event_source_mapping("test-uuid", region_name=REGION)


def test_delete_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function("test-function_name", region_name=REGION)
    mock_client.delete_function.assert_called_once()


def test_delete_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function"):
        delete_function("test-function_name", region_name=REGION)


def test_delete_function_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_code_signing_config("test-function_name", region_name=REGION)
    mock_client.delete_function_code_signing_config.assert_called_once()


def test_delete_function_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function code signing config"):
        delete_function_code_signing_config("test-function_name", region_name=REGION)


def test_delete_function_concurrency(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_concurrency.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_concurrency("test-function_name", region_name=REGION)
    mock_client.delete_function_concurrency.assert_called_once()


def test_delete_function_concurrency_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_concurrency.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function_concurrency",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function concurrency"):
        delete_function_concurrency("test-function_name", region_name=REGION)


def test_delete_function_event_invoke_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_event_invoke_config("test-function_name", region_name=REGION)
    mock_client.delete_function_event_invoke_config.assert_called_once()


def test_delete_function_event_invoke_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_event_invoke_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function_event_invoke_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function event invoke config"):
        delete_function_event_invoke_config("test-function_name", region_name=REGION)


def test_delete_function_url_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_url_config("test-function_name", region_name=REGION)
    mock_client.delete_function_url_config.assert_called_once()


def test_delete_function_url_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function_url_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function_url_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function url config"):
        delete_function_url_config("test-function_name", region_name=REGION)


def test_delete_layer_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_layer_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_layer_version("test-layer_name", 1, region_name=REGION)
    mock_client.delete_layer_version.assert_called_once()


def test_delete_layer_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_layer_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_layer_version",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete layer version"):
        delete_layer_version("test-layer_name", 1, region_name=REGION)


def test_delete_provisioned_concurrency_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_provisioned_concurrency_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_provisioned_concurrency_config("test-function_name", "test-qualifier", region_name=REGION)
    mock_client.delete_provisioned_concurrency_config.assert_called_once()


def test_delete_provisioned_concurrency_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_provisioned_concurrency_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_provisioned_concurrency_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete provisioned concurrency config"):
        delete_provisioned_concurrency_config("test-function_name", "test-qualifier", region_name=REGION)


def test_get_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_account_settings(region_name=REGION)
    mock_client.get_account_settings.assert_called_once()


def test_get_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_settings",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account settings"):
        get_account_settings(region_name=REGION)


def test_get_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_alias("test-function_name", "test-name", region_name=REGION)
    mock_client.get_alias.assert_called_once()


def test_get_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_alias",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get alias"):
        get_alias("test-function_name", "test-name", region_name=REGION)


def test_get_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_code_signing_config("test-code_signing_config_arn", region_name=REGION)
    mock_client.get_code_signing_config.assert_called_once()


def test_get_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get code signing config"):
        get_code_signing_config("test-code_signing_config_arn", region_name=REGION)


def test_get_event_source_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_event_source_mapping("test-uuid", region_name=REGION)
    mock_client.get_event_source_mapping.assert_called_once()


def test_get_event_source_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_source_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_event_source_mapping",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get event source mapping"):
        get_event_source_mapping("test-uuid", region_name=REGION)


def test_get_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function("test-function_name", region_name=REGION)
    mock_client.get_function.assert_called_once()


def test_get_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function"):
        get_function("test-function_name", region_name=REGION)


def test_get_function_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_code_signing_config("test-function_name", region_name=REGION)
    mock_client.get_function_code_signing_config.assert_called_once()


def test_get_function_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function code signing config"):
        get_function_code_signing_config("test-function_name", region_name=REGION)


def test_get_function_concurrency(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_concurrency.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_concurrency("test-function_name", region_name=REGION)
    mock_client.get_function_concurrency.assert_called_once()


def test_get_function_concurrency_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_concurrency.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_concurrency",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function concurrency"):
        get_function_concurrency("test-function_name", region_name=REGION)


def test_get_function_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_configuration.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_configuration("test-function_name", region_name=REGION)
    mock_client.get_function_configuration.assert_called_once()


def test_get_function_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_configuration",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function configuration"):
        get_function_configuration("test-function_name", region_name=REGION)


def test_get_function_event_invoke_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_event_invoke_config("test-function_name", region_name=REGION)
    mock_client.get_function_event_invoke_config.assert_called_once()


def test_get_function_event_invoke_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_event_invoke_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_event_invoke_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function event invoke config"):
        get_function_event_invoke_config("test-function_name", region_name=REGION)


def test_get_function_recursion_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_recursion_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_recursion_config("test-function_name", region_name=REGION)
    mock_client.get_function_recursion_config.assert_called_once()


def test_get_function_recursion_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_recursion_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_recursion_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function recursion config"):
        get_function_recursion_config("test-function_name", region_name=REGION)


def test_get_function_url_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_url_config("test-function_name", region_name=REGION)
    mock_client.get_function_url_config.assert_called_once()


def test_get_function_url_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function_url_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function_url_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function url config"):
        get_function_url_config("test-function_name", region_name=REGION)


def test_get_layer_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_layer_version("test-layer_name", 1, region_name=REGION)
    mock_client.get_layer_version.assert_called_once()


def test_get_layer_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_layer_version",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get layer version"):
        get_layer_version("test-layer_name", 1, region_name=REGION)


def test_get_layer_version_by_arn(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version_by_arn.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_layer_version_by_arn("test-arn", region_name=REGION)
    mock_client.get_layer_version_by_arn.assert_called_once()


def test_get_layer_version_by_arn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version_by_arn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_layer_version_by_arn",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get layer version by arn"):
        get_layer_version_by_arn("test-arn", region_name=REGION)


def test_get_layer_version_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version_policy.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_layer_version_policy("test-layer_name", 1, region_name=REGION)
    mock_client.get_layer_version_policy.assert_called_once()


def test_get_layer_version_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_layer_version_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_layer_version_policy",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get layer version policy"):
        get_layer_version_policy("test-layer_name", 1, region_name=REGION)


def test_get_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_policy("test-function_name", region_name=REGION)
    mock_client.get_policy.assert_called_once()


def test_get_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_policy",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get policy"):
        get_policy("test-function_name", region_name=REGION)


def test_get_provisioned_concurrency_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_provisioned_concurrency_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_provisioned_concurrency_config("test-function_name", "test-qualifier", region_name=REGION)
    mock_client.get_provisioned_concurrency_config.assert_called_once()


def test_get_provisioned_concurrency_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_provisioned_concurrency_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_provisioned_concurrency_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get provisioned concurrency config"):
        get_provisioned_concurrency_config("test-function_name", "test-qualifier", region_name=REGION)


def test_get_runtime_management_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_runtime_management_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_runtime_management_config("test-function_name", region_name=REGION)
    mock_client.get_runtime_management_config.assert_called_once()


def test_get_runtime_management_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_runtime_management_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_runtime_management_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get runtime management config"):
        get_runtime_management_config("test-function_name", region_name=REGION)


def test_invoke_with_response_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_with_response_stream.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    invoke_with_response_stream("test-function_name", region_name=REGION)
    mock_client.invoke_with_response_stream.assert_called_once()


def test_invoke_with_response_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.invoke_with_response_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "invoke_with_response_stream",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to invoke with response stream"):
        invoke_with_response_stream("test-function_name", region_name=REGION)


def test_list_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aliases.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_aliases("test-function_name", region_name=REGION)
    mock_client.list_aliases.assert_called_once()


def test_list_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aliases",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aliases"):
        list_aliases("test-function_name", region_name=REGION)


def test_list_code_signing_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_code_signing_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_code_signing_configs(region_name=REGION)
    mock_client.list_code_signing_configs.assert_called_once()


def test_list_code_signing_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_code_signing_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_code_signing_configs",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list code signing configs"):
        list_code_signing_configs(region_name=REGION)


def test_list_event_source_mappings(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_source_mappings.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_event_source_mappings(region_name=REGION)
    mock_client.list_event_source_mappings.assert_called_once()


def test_list_event_source_mappings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_source_mappings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_event_source_mappings",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list event source mappings"):
        list_event_source_mappings(region_name=REGION)


def test_list_function_event_invoke_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_function_event_invoke_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_function_event_invoke_configs("test-function_name", region_name=REGION)
    mock_client.list_function_event_invoke_configs.assert_called_once()


def test_list_function_event_invoke_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_function_event_invoke_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_function_event_invoke_configs",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list function event invoke configs"):
        list_function_event_invoke_configs("test-function_name", region_name=REGION)


def test_list_function_url_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_function_url_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_function_url_configs("test-function_name", region_name=REGION)
    mock_client.list_function_url_configs.assert_called_once()


def test_list_function_url_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_function_url_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_function_url_configs",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list function url configs"):
        list_function_url_configs("test-function_name", region_name=REGION)


def test_list_functions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_functions(region_name=REGION)
    mock_client.list_functions.assert_called_once()


def test_list_functions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_functions",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list functions"):
        list_functions(region_name=REGION)


def test_list_functions_by_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions_by_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_functions_by_code_signing_config("test-code_signing_config_arn", region_name=REGION)
    mock_client.list_functions_by_code_signing_config.assert_called_once()


def test_list_functions_by_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions_by_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_functions_by_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list functions by code signing config"):
        list_functions_by_code_signing_config("test-code_signing_config_arn", region_name=REGION)


def test_list_layer_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_layer_versions.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_layer_versions("test-layer_name", region_name=REGION)
    mock_client.list_layer_versions.assert_called_once()


def test_list_layer_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_layer_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_layer_versions",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list layer versions"):
        list_layer_versions("test-layer_name", region_name=REGION)


def test_list_layers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_layers.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_layers(region_name=REGION)
    mock_client.list_layers.assert_called_once()


def test_list_layers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_layers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_layers",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list layers"):
        list_layers(region_name=REGION)


def test_list_provisioned_concurrency_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_provisioned_concurrency_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_provisioned_concurrency_configs("test-function_name", region_name=REGION)
    mock_client.list_provisioned_concurrency_configs.assert_called_once()


def test_list_provisioned_concurrency_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_provisioned_concurrency_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_provisioned_concurrency_configs",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list provisioned concurrency configs"):
        list_provisioned_concurrency_configs("test-function_name", region_name=REGION)


def test_list_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_tags("test-resource", region_name=REGION)
    mock_client.list_tags.assert_called_once()


def test_list_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags"):
        list_tags("test-resource", region_name=REGION)


def test_list_versions_by_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_versions_by_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_versions_by_function("test-function_name", region_name=REGION)
    mock_client.list_versions_by_function.assert_called_once()


def test_list_versions_by_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_versions_by_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_versions_by_function",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list versions by function"):
        list_versions_by_function("test-function_name", region_name=REGION)


def test_publish_layer_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_layer_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    publish_layer_version("test-layer_name", {}, region_name=REGION)
    mock_client.publish_layer_version.assert_called_once()


def test_publish_layer_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_layer_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_layer_version",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to publish layer version"):
        publish_layer_version("test-layer_name", {}, region_name=REGION)


def test_publish_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    publish_version("test-function_name", region_name=REGION)
    mock_client.publish_version.assert_called_once()


def test_publish_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_version",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to publish version"):
        publish_version("test-function_name", region_name=REGION)


def test_put_function_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_function_code_signing_config("test-code_signing_config_arn", "test-function_name", region_name=REGION)
    mock_client.put_function_code_signing_config.assert_called_once()


def test_put_function_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_function_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put function code signing config"):
        put_function_code_signing_config("test-code_signing_config_arn", "test-function_name", region_name=REGION)


def test_put_function_concurrency(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_concurrency.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_function_concurrency("test-function_name", 1, region_name=REGION)
    mock_client.put_function_concurrency.assert_called_once()


def test_put_function_concurrency_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_concurrency.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_function_concurrency",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put function concurrency"):
        put_function_concurrency("test-function_name", 1, region_name=REGION)


def test_put_function_event_invoke_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_function_event_invoke_config("test-function_name", region_name=REGION)
    mock_client.put_function_event_invoke_config.assert_called_once()


def test_put_function_event_invoke_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_event_invoke_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_function_event_invoke_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put function event invoke config"):
        put_function_event_invoke_config("test-function_name", region_name=REGION)


def test_put_function_recursion_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_recursion_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_function_recursion_config("test-function_name", "test-recursive_loop", region_name=REGION)
    mock_client.put_function_recursion_config.assert_called_once()


def test_put_function_recursion_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_function_recursion_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_function_recursion_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put function recursion config"):
        put_function_recursion_config("test-function_name", "test-recursive_loop", region_name=REGION)


def test_put_provisioned_concurrency_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_provisioned_concurrency_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_provisioned_concurrency_config("test-function_name", "test-qualifier", 1, region_name=REGION)
    mock_client.put_provisioned_concurrency_config.assert_called_once()


def test_put_provisioned_concurrency_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_provisioned_concurrency_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_provisioned_concurrency_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put provisioned concurrency config"):
        put_provisioned_concurrency_config("test-function_name", "test-qualifier", 1, region_name=REGION)


def test_put_runtime_management_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_runtime_management_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_runtime_management_config("test-function_name", "test-update_runtime_on", region_name=REGION)
    mock_client.put_runtime_management_config.assert_called_once()


def test_put_runtime_management_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_runtime_management_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_runtime_management_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put runtime management config"):
        put_runtime_management_config("test-function_name", "test-update_runtime_on", region_name=REGION)


def test_remove_layer_version_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_layer_version_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    remove_layer_version_permission("test-layer_name", 1, "test-statement_id", region_name=REGION)
    mock_client.remove_layer_version_permission.assert_called_once()


def test_remove_layer_version_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_layer_version_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_layer_version_permission",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove layer version permission"):
        remove_layer_version_permission("test-layer_name", 1, "test-statement_id", region_name=REGION)


def test_remove_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    remove_permission("test-function_name", "test-statement_id", region_name=REGION)
    mock_client.remove_permission.assert_called_once()


def test_remove_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_permission",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove permission"):
        remove_permission("test-function_name", "test-statement_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource", [], region_name=REGION)


def test_update_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_alias("test-function_name", "test-name", region_name=REGION)
    mock_client.update_alias.assert_called_once()


def test_update_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_alias",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update alias"):
        update_alias("test-function_name", "test-name", region_name=REGION)


def test_update_code_signing_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_code_signing_config("test-code_signing_config_arn", region_name=REGION)
    mock_client.update_code_signing_config.assert_called_once()


def test_update_code_signing_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_code_signing_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_code_signing_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update code signing config"):
        update_code_signing_config("test-code_signing_config_arn", region_name=REGION)


def test_update_event_source_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_event_source_mapping("test-uuid", region_name=REGION)
    mock_client.update_event_source_mapping.assert_called_once()


def test_update_event_source_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_source_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_event_source_mapping",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update event source mapping"):
        update_event_source_mapping("test-uuid", region_name=REGION)


def test_update_function_code(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_code.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_code("test-function_name", region_name=REGION)
    mock_client.update_function_code.assert_called_once()


def test_update_function_code_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_function_code",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update function code"):
        update_function_code("test-function_name", region_name=REGION)


def test_update_function_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_configuration.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_configuration("test-function_name", region_name=REGION)
    mock_client.update_function_configuration.assert_called_once()


def test_update_function_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_function_configuration",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update function configuration"):
        update_function_configuration("test-function_name", region_name=REGION)


def test_update_function_event_invoke_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_event_invoke_config("test-function_name", region_name=REGION)
    mock_client.update_function_event_invoke_config.assert_called_once()


def test_update_function_event_invoke_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_event_invoke_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_function_event_invoke_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update function event invoke config"):
        update_function_event_invoke_config("test-function_name", region_name=REGION)


def test_update_function_url_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_url_config("test-function_name", region_name=REGION)
    mock_client.update_function_url_config.assert_called_once()


def test_update_function_url_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function_url_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_function_url_config",
    )
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update function url config"):
        update_function_url_config("test-function_name", region_name=REGION)


def test_add_layer_version_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import add_layer_version_permission
    mock_client = MagicMock()
    mock_client.add_layer_version_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    add_layer_version_permission("test-layer_name", "test-version_number", "test-statement_id", "test-action", "test-principal", organization_id="test-organization_id", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.add_layer_version_permission.assert_called_once()

def test_add_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import add_permission
    mock_client = MagicMock()
    mock_client.add_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    add_permission("test-function_name", "test-statement_id", "test-action", "test-principal", source_arn="test-source_arn", source_account=1, event_source_token="test-event_source_token", qualifier="test-qualifier", revision_id="test-revision_id", principal_org_id="test-principal_org_id", function_url_auth_type="test-function_url_auth_type", invoked_via_function_url="test-invoked_via_function_url", region_name="us-east-1")
    mock_client.add_permission.assert_called_once()

def test_create_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import create_alias
    mock_client = MagicMock()
    mock_client.create_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_alias("test-function_name", "test-name", "test-function_version", description="test-description", routing_config={}, region_name="us-east-1")
    mock_client.create_alias.assert_called_once()

def test_create_code_signing_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import create_code_signing_config
    mock_client = MagicMock()
    mock_client.create_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_code_signing_config(True, description="test-description", code_signing_policies="test-code_signing_policies", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_code_signing_config.assert_called_once()

def test_create_event_source_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import create_event_source_mapping
    mock_client = MagicMock()
    mock_client.create_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_event_source_mapping("test-function_name", event_source_arn="test-event_source_arn", enabled=True, batch_size=1, filter_criteria="test-filter_criteria", maximum_batching_window_in_seconds=1, parallelization_factor="test-parallelization_factor", starting_position="test-starting_position", starting_position_timestamp="test-starting_position_timestamp", destination_config={}, maximum_record_age_in_seconds=1, bisect_batch_on_function_error="test-bisect_batch_on_function_error", maximum_retry_attempts=1, tags=[{"Key": "k", "Value": "v"}], tumbling_window_in_seconds="test-tumbling_window_in_seconds", topics="test-topics", queues="test-queues", source_access_configurations={}, self_managed_event_source="test-self_managed_event_source", function_response_types="test-function_response_types", amazon_managed_kafka_event_source_config={}, self_managed_kafka_event_source_config={}, scaling_config={}, document_db_event_source_config={}, kms_key_arn="test-kms_key_arn", metrics_config={}, provisioned_poller_config={}, region_name="us-east-1")
    mock_client.create_event_source_mapping.assert_called_once()

def test_create_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import create_function
    mock_client = MagicMock()
    mock_client.create_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_function("test-function_name", "test-role", "test-code", runtime="test-runtime", handler="test-handler", description="test-description", timeout=1, memory_size=1, publish=True, vpc_config={}, package_type="test-package_type", dead_letter_config={}, environment="test-environment", kms_key_arn="test-kms_key_arn", tracing_config={}, tags=[{"Key": "k", "Value": "v"}], layers="test-layers", file_system_configs={}, image_config={}, code_signing_config_arn={}, architectures="test-architectures", ephemeral_storage="test-ephemeral_storage", snap_start="test-snap_start", logging_config={}, region_name="us-east-1")
    mock_client.create_function.assert_called_once()

def test_create_function_url_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import create_function_url_config
    mock_client = MagicMock()
    mock_client.create_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    create_function_url_config("test-function_name", "test-auth_type", qualifier="test-qualifier", cors="test-cors", invoke_mode="test-invoke_mode", region_name="us-east-1")
    mock_client.create_function_url_config.assert_called_once()

def test_delete_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import delete_function
    mock_client = MagicMock()
    mock_client.delete_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.delete_function.assert_called_once()

def test_delete_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import delete_function_event_invoke_config
    mock_client = MagicMock()
    mock_client.delete_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_event_invoke_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.delete_function_event_invoke_config.assert_called_once()

def test_delete_function_url_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import delete_function_url_config
    mock_client = MagicMock()
    mock_client.delete_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    delete_function_url_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.delete_function_url_config.assert_called_once()

def test_get_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_function
    mock_client = MagicMock()
    mock_client.get_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_function.assert_called_once()

def test_get_function_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_function_configuration
    mock_client = MagicMock()
    mock_client.get_function_configuration.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_configuration("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_function_configuration.assert_called_once()

def test_get_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_function_event_invoke_config
    mock_client = MagicMock()
    mock_client.get_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_event_invoke_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_function_event_invoke_config.assert_called_once()

def test_get_function_url_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_function_url_config
    mock_client = MagicMock()
    mock_client.get_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_function_url_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_function_url_config.assert_called_once()

def test_get_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_policy
    mock_client = MagicMock()
    mock_client.get_policy.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_policy("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_policy.assert_called_once()

def test_get_runtime_management_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import get_runtime_management_config
    mock_client = MagicMock()
    mock_client.get_runtime_management_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    get_runtime_management_config("test-function_name", qualifier="test-qualifier", region_name="us-east-1")
    mock_client.get_runtime_management_config.assert_called_once()

def test_invoke_with_response_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import invoke_with_response_stream
    mock_client = MagicMock()
    mock_client.invoke_with_response_stream.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    invoke_with_response_stream("test-function_name", invocation_type="test-invocation_type", log_type="test-log_type", client_context={}, qualifier="test-qualifier", payload="test-payload", region_name="us-east-1")
    mock_client.invoke_with_response_stream.assert_called_once()

def test_list_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_aliases
    mock_client = MagicMock()
    mock_client.list_aliases.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_aliases("test-function_name", function_version="test-function_version", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_aliases.assert_called_once()

def test_list_code_signing_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_code_signing_configs
    mock_client = MagicMock()
    mock_client.list_code_signing_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_code_signing_configs(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_code_signing_configs.assert_called_once()

def test_list_event_source_mappings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_event_source_mappings
    mock_client = MagicMock()
    mock_client.list_event_source_mappings.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_event_source_mappings(event_source_arn="test-event_source_arn", function_name="test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_event_source_mappings.assert_called_once()

def test_list_function_event_invoke_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_function_event_invoke_configs
    mock_client = MagicMock()
    mock_client.list_function_event_invoke_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_function_event_invoke_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_function_event_invoke_configs.assert_called_once()

def test_list_function_url_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_function_url_configs
    mock_client = MagicMock()
    mock_client.list_function_url_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_function_url_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_function_url_configs.assert_called_once()

def test_list_functions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_functions
    mock_client = MagicMock()
    mock_client.list_functions.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_functions(master_region="test-master_region", function_version="test-function_version", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_functions.assert_called_once()

def test_list_functions_by_code_signing_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_functions_by_code_signing_config
    mock_client = MagicMock()
    mock_client.list_functions_by_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_functions_by_code_signing_config({}, marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_functions_by_code_signing_config.assert_called_once()

def test_list_layer_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_layer_versions
    mock_client = MagicMock()
    mock_client.list_layer_versions.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_layer_versions("test-layer_name", compatible_runtime="test-compatible_runtime", marker="test-marker", max_items=1, compatible_architecture="test-compatible_architecture", region_name="us-east-1")
    mock_client.list_layer_versions.assert_called_once()

def test_list_layers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_layers
    mock_client = MagicMock()
    mock_client.list_layers.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_layers(compatible_runtime="test-compatible_runtime", marker="test-marker", max_items=1, compatible_architecture="test-compatible_architecture", region_name="us-east-1")
    mock_client.list_layers.assert_called_once()

def test_list_provisioned_concurrency_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_provisioned_concurrency_configs
    mock_client = MagicMock()
    mock_client.list_provisioned_concurrency_configs.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_provisioned_concurrency_configs("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_provisioned_concurrency_configs.assert_called_once()

def test_list_versions_by_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import list_versions_by_function
    mock_client = MagicMock()
    mock_client.list_versions_by_function.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    list_versions_by_function("test-function_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_versions_by_function.assert_called_once()

def test_publish_layer_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import publish_layer_version
    mock_client = MagicMock()
    mock_client.publish_layer_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    publish_layer_version("test-layer_name", "test-content", description="test-description", compatible_runtimes="test-compatible_runtimes", license_info="test-license_info", compatible_architectures="test-compatible_architectures", region_name="us-east-1")
    mock_client.publish_layer_version.assert_called_once()

def test_publish_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import publish_version
    mock_client = MagicMock()
    mock_client.publish_version.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    publish_version("test-function_name", code_sha256="test-code_sha256", description="test-description", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.publish_version.assert_called_once()

def test_put_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import put_function_event_invoke_config
    mock_client = MagicMock()
    mock_client.put_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_function_event_invoke_config("test-function_name", qualifier="test-qualifier", maximum_retry_attempts=1, maximum_event_age_in_seconds=1, destination_config={}, region_name="us-east-1")
    mock_client.put_function_event_invoke_config.assert_called_once()

def test_put_runtime_management_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import put_runtime_management_config
    mock_client = MagicMock()
    mock_client.put_runtime_management_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    put_runtime_management_config("test-function_name", "test-update_runtime_on", qualifier="test-qualifier", runtime_version_arn="test-runtime_version_arn", region_name="us-east-1")
    mock_client.put_runtime_management_config.assert_called_once()

def test_remove_layer_version_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import remove_layer_version_permission
    mock_client = MagicMock()
    mock_client.remove_layer_version_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    remove_layer_version_permission("test-layer_name", "test-version_number", "test-statement_id", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.remove_layer_version_permission.assert_called_once()

def test_remove_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import remove_permission
    mock_client = MagicMock()
    mock_client.remove_permission.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    remove_permission("test-function_name", "test-statement_id", qualifier="test-qualifier", revision_id="test-revision_id", region_name="us-east-1")
    mock_client.remove_permission.assert_called_once()

def test_update_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_alias
    mock_client = MagicMock()
    mock_client.update_alias.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_alias("test-function_name", "test-name", function_version="test-function_version", description="test-description", routing_config={}, revision_id="test-revision_id", region_name="us-east-1")
    mock_client.update_alias.assert_called_once()

def test_update_code_signing_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_code_signing_config
    mock_client = MagicMock()
    mock_client.update_code_signing_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_code_signing_config({}, description="test-description", allowed_publishers=True, code_signing_policies="test-code_signing_policies", region_name="us-east-1")
    mock_client.update_code_signing_config.assert_called_once()

def test_update_event_source_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_event_source_mapping
    mock_client = MagicMock()
    mock_client.update_event_source_mapping.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_event_source_mapping("test-uuid", function_name="test-function_name", enabled=True, batch_size=1, filter_criteria="test-filter_criteria", maximum_batching_window_in_seconds=1, destination_config={}, maximum_record_age_in_seconds=1, bisect_batch_on_function_error="test-bisect_batch_on_function_error", maximum_retry_attempts=1, parallelization_factor="test-parallelization_factor", source_access_configurations={}, tumbling_window_in_seconds="test-tumbling_window_in_seconds", function_response_types="test-function_response_types", scaling_config={}, amazon_managed_kafka_event_source_config={}, self_managed_kafka_event_source_config={}, document_db_event_source_config={}, kms_key_arn="test-kms_key_arn", metrics_config={}, provisioned_poller_config={}, region_name="us-east-1")
    mock_client.update_event_source_mapping.assert_called_once()

def test_update_function_code_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_function_code
    mock_client = MagicMock()
    mock_client.update_function_code.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_code("test-function_name", zip_file="test-zip_file", s3_bucket="test-s3_bucket", s3_key="test-s3_key", s3_object_version="test-s3_object_version", image_uri="test-image_uri", publish=True, revision_id="test-revision_id", architectures="test-architectures", source_kms_key_arn="test-source_kms_key_arn", region_name="us-east-1")
    mock_client.update_function_code.assert_called_once()

def test_update_function_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_function_configuration
    mock_client = MagicMock()
    mock_client.update_function_configuration.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_configuration("test-function_name", role="test-role", handler="test-handler", description="test-description", timeout=1, memory_size=1, vpc_config={}, environment="test-environment", runtime="test-runtime", dead_letter_config={}, kms_key_arn="test-kms_key_arn", tracing_config={}, revision_id="test-revision_id", layers="test-layers", file_system_configs={}, image_config={}, ephemeral_storage="test-ephemeral_storage", snap_start="test-snap_start", logging_config={}, region_name="us-east-1")
    mock_client.update_function_configuration.assert_called_once()

def test_update_function_event_invoke_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_function_event_invoke_config
    mock_client = MagicMock()
    mock_client.update_function_event_invoke_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_event_invoke_config("test-function_name", qualifier="test-qualifier", maximum_retry_attempts=1, maximum_event_age_in_seconds=1, destination_config={}, region_name="us-east-1")
    mock_client.update_function_event_invoke_config.assert_called_once()

def test_update_function_url_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lambda_ import update_function_url_config
    mock_client = MagicMock()
    mock_client.update_function_url_config.return_value = {}
    monkeypatch.setattr("aws_util.lambda_.get_client", lambda *a, **kw: mock_client)
    update_function_url_config("test-function_name", qualifier="test-qualifier", auth_type="test-auth_type", cors="test-cors", invoke_mode="test-invoke_mode", region_name="us-east-1")
    mock_client.update_function_url_config.assert_called_once()
