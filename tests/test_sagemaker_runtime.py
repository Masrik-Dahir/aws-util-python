"""Tests for aws_util.sagemaker_runtime — 100% line coverage."""
from __future__ import annotations

import io
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.sagemaker_runtime import (
    InvokeEndpointAsyncResult,
    InvokeEndpointResult,
    invoke_endpoint,
    invoke_endpoint_async,
    invoke_endpoint_with_response_stream,
)

EP = "my-endpoint"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_invoke_endpoint_result(self):
        r = InvokeEndpointResult(body="hello")
        assert r.body == "hello"
        assert r.content_type == ""

    def test_invoke_endpoint_async_result(self):
        r = InvokeEndpointAsyncResult()
        assert r.inference_id == ""
        assert r.output_location == ""
        assert r.failure_location == ""


# ---------------------------------------------------------------------------
# invoke_endpoint
# ---------------------------------------------------------------------------


class TestInvokeEndpoint:
    @patch("aws_util.sagemaker_runtime.get_client")
    def test_success_string_body(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint.return_value = {
            "Body": io.BytesIO(b'{"result": "ok"}'),
            "ContentType": "application/json",
            "InvokedProductionVariant": "v1",
            "CustomAttributes": "attr",
        }
        result = invoke_endpoint(EP, '{"input": "data"}')
        assert isinstance(result, InvokeEndpointResult)
        assert result.body == '{"result": "ok"}'
        assert result.content_type == "application/json"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_success_bytes_body(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint.return_value = {
            "Body": io.BytesIO(b"raw"),
        }
        result = invoke_endpoint(EP, b"raw-bytes")
        assert result.body == "raw"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_all_optional_params(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint.return_value = {
            "Body": io.BytesIO(b"ok"),
        }
        invoke_endpoint(
            EP, "body",
            target_model="m1",
            target_variant="v1",
            inference_id="inf-1",
            custom_attributes="ca",
            region_name="us-west-2",
        )
        args = client.invoke_endpoint.call_args[1]
        assert args["TargetModel"] == "m1"
        assert args["TargetVariant"] == "v1"
        assert args["InferenceId"] == "inf-1"
        assert args["CustomAttributes"] == "ca"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint.side_effect = ClientError(
            {"Error": {"Code": "ModelError", "Message": "fail"}}, "InvokeEndpoint"
        )
        with pytest.raises(Exception):
            invoke_endpoint(EP, "body")


# ---------------------------------------------------------------------------
# invoke_endpoint_async
# ---------------------------------------------------------------------------


class TestInvokeEndpointAsync:
    @patch("aws_util.sagemaker_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_async.return_value = {
            "InferenceId": "inf-1",
            "OutputLocation": "s3://bucket/out",
            "FailureLocation": "",
        }
        result = invoke_endpoint_async(EP, "s3://bucket/in")
        assert isinstance(result, InvokeEndpointAsyncResult)
        assert result.output_location == "s3://bucket/out"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_with_optional_params(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_async.return_value = {}
        invoke_endpoint_async(
            EP, "s3://in",
            inference_id="inf-1",
            custom_attributes="ca",
        )
        args = client.invoke_endpoint_async.call_args[1]
        assert args["InferenceId"] == "inf-1"
        assert args["CustomAttributes"] == "ca"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_async.side_effect = ClientError(
            {"Error": {"Code": "ModelError", "Message": "fail"}}, "InvokeEndpointAsync"
        )
        with pytest.raises(Exception):
            invoke_endpoint_async(EP, "s3://in")


# ---------------------------------------------------------------------------
# invoke_endpoint_with_response_stream
# ---------------------------------------------------------------------------


class TestInvokeEndpointWithResponseStream:
    @patch("aws_util.sagemaker_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_with_response_stream.return_value = {
            "Body": [
                {"PayloadPart": {"Bytes": b"chunk1"}},
                {"PayloadPart": {"Bytes": b"chunk2"}},
            ],
        }
        result = invoke_endpoint_with_response_stream(EP, "body")
        assert result == [b"chunk1", b"chunk2"]

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_empty_chunks_skipped(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_with_response_stream.return_value = {
            "Body": [
                {"PayloadPart": {"Bytes": b""}},
                {"PayloadPart": {"Bytes": b"data"}},
                {},
            ],
        }
        result = invoke_endpoint_with_response_stream(EP, "body")
        assert result == [b"data"]

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_empty_body(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_with_response_stream.return_value = {}
        result = invoke_endpoint_with_response_stream(EP, "body")
        assert result == []

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_all_optional_params(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_with_response_stream.return_value = {"Body": []}
        invoke_endpoint_with_response_stream(
            EP, b"bytes-body",
            target_variant="v1",
            inference_id="inf-1",
            custom_attributes="ca",
        )
        args = client.invoke_endpoint_with_response_stream.call_args[1]
        assert args["TargetVariant"] == "v1"

    @patch("aws_util.sagemaker_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.invoke_endpoint_with_response_stream.side_effect = ClientError(
            {"Error": {"Code": "ModelError", "Message": "fail"}}, "Op"
        )
        with pytest.raises(Exception):
            invoke_endpoint_with_response_stream(EP, "body")
