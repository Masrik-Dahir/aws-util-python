"""Tests for aws_util.aio.sagemaker_runtime — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.sagemaker_runtime import (
    InvokeEndpointAsyncResult,
    InvokeEndpointResult,
    invoke_endpoint,
    invoke_endpoint_async,
    invoke_endpoint_with_response_stream,
)

EP = "my-endpoint"


def _factory(client):
    return lambda *a, **kw: client


# ---------------------------------------------------------------------------
# invoke_endpoint
# ---------------------------------------------------------------------------


async def test_invoke_endpoint_success_str(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Body": '{"result": "ok"}',
        "ContentType": "application/json",
        "InvokedProductionVariant": "v1",
        "CustomAttributes": "attr",
    }
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint(EP, '{"input": "data"}')
    assert isinstance(result, InvokeEndpointResult)
    assert result.body == '{"result": "ok"}'


async def test_invoke_endpoint_success_bytes_body(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Body": b"raw-data"}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint(EP, b"input-bytes")
    assert result.body == "raw-data"


async def test_invoke_endpoint_hasattr_read(monkeypatch):
    """Test the hasattr(resp_body, 'read') branch."""
    class FakeStream:
        def read(self):
            return b"stream-data"

    client = AsyncMock()
    client.call.return_value = {"Body": FakeStream()}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint(EP, "body")
    assert result.body == "stream-data"


async def test_invoke_endpoint_all_optional(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Body": "ok"}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    await invoke_endpoint(
        EP, "body",
        target_model="m1",
        target_variant="v1",
        inference_id="inf-1",
        custom_attributes="ca",
        region_name="us-west-2",
    )


async def test_invoke_endpoint_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(RuntimeError):
        await invoke_endpoint(EP, "body")


async def test_invoke_endpoint_other_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(Exception):
        await invoke_endpoint(EP, "body")


# ---------------------------------------------------------------------------
# invoke_endpoint_async
# ---------------------------------------------------------------------------


async def test_invoke_endpoint_async_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "InferenceId": "inf-1",
        "OutputLocation": "s3://out",
        "FailureLocation": "",
    }
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint_async(EP, "s3://in")
    assert isinstance(result, InvokeEndpointAsyncResult)
    assert result.output_location == "s3://out"


async def test_invoke_endpoint_async_optional_params(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    await invoke_endpoint_async(EP, "s3://in", inference_id="inf-1", custom_attributes="ca")


async def test_invoke_endpoint_async_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(RuntimeError):
        await invoke_endpoint_async(EP, "s3://in")


async def test_invoke_endpoint_async_other_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(Exception):
        await invoke_endpoint_async(EP, "s3://in")


# ---------------------------------------------------------------------------
# invoke_endpoint_with_response_stream
# ---------------------------------------------------------------------------


async def test_stream_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Body": [
            {"PayloadPart": {"Bytes": b"c1"}},
            {"PayloadPart": {"Bytes": b"c2"}},
        ],
    }
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint_with_response_stream(EP, "body")
    assert result == [b"c1", b"c2"]


async def test_stream_empty_chunks(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Body": [
            {"PayloadPart": {"Bytes": b""}},
            {},
            {"PayloadPart": {"Bytes": b"data"}},
        ],
    }
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint_with_response_stream(EP, "body")
    assert result == [b"data"]


async def test_stream_empty_body(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    result = await invoke_endpoint_with_response_stream(EP, b"bytes-input")
    assert result == []


async def test_stream_all_optional(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Body": []}
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    await invoke_endpoint_with_response_stream(
        EP, "body",
        target_variant="v1",
        inference_id="inf-1",
        custom_attributes="ca",
    )


async def test_stream_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(RuntimeError):
        await invoke_endpoint_with_response_stream(EP, "body")


async def test_stream_other_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr("aws_util.aio.sagemaker_runtime.async_client", _factory(client))
    with pytest.raises(Exception):
        await invoke_endpoint_with_response_stream(EP, "body")
