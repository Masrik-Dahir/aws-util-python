"""aws_util.sagemaker_runtime -- SageMaker Runtime inference utilities.

Thin helpers around the ``sagemaker-runtime`` API for invoking hosted
model endpoints (real-time, async, and streaming).
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "InvokeEndpointAsyncResult",
    "InvokeEndpointResult",
    "invoke_endpoint",
    "invoke_endpoint_async",
    "invoke_endpoint_with_response_stream",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class InvokeEndpointResult(BaseModel):
    """Response from a real-time SageMaker endpoint invocation."""

    model_config = ConfigDict(frozen=True)

    body: str
    content_type: str = ""
    invoked_production_variant: str = ""
    custom_attributes: str = ""


class InvokeEndpointAsyncResult(BaseModel):
    """Response from an asynchronous SageMaker endpoint invocation."""

    model_config = ConfigDict(frozen=True)

    inference_id: str = ""
    output_location: str = ""
    failure_location: str = ""


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def invoke_endpoint(
    endpoint_name: str,
    body: str | bytes,
    content_type: str = "application/json",
    accept: str = "application/json",
    target_model: str | None = None,
    target_variant: str | None = None,
    inference_id: str | None = None,
    custom_attributes: str | None = None,
    region_name: str | None = None,
) -> InvokeEndpointResult:
    """Invoke a SageMaker real-time endpoint.

    Args:
        endpoint_name: Name of the deployed SageMaker endpoint.
        body: Request payload (JSON string or raw bytes).
        content_type: MIME type of the request body.
        accept: Desired MIME type for the response.
        target_model: Target model for multi-model endpoints.
        target_variant: Target variant for A/B test endpoints.
        inference_id: Identifier for tracking the request.
        custom_attributes: Custom attributes for the request.
        region_name: AWS region override.

    Returns:
        An :class:`InvokeEndpointResult` with the endpoint response.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = get_client("sagemaker-runtime", region_name)
    kwargs: dict[str, Any] = {
        "EndpointName": endpoint_name,
        "Body": body if isinstance(body, bytes) else body.encode("utf-8"),
        "ContentType": content_type,
        "Accept": accept,
    }
    if target_model is not None:
        kwargs["TargetModel"] = target_model
    if target_variant is not None:
        kwargs["TargetVariant"] = target_variant
    if inference_id is not None:
        kwargs["InferenceId"] = inference_id
    if custom_attributes is not None:
        kwargs["CustomAttributes"] = custom_attributes
    try:
        resp = client.invoke_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "invoke_endpoint failed") from exc
    resp_body = resp["Body"].read()
    if isinstance(resp_body, bytes):
        resp_body = resp_body.decode("utf-8")
    return InvokeEndpointResult(
        body=resp_body,
        content_type=resp.get("ContentType", ""),
        invoked_production_variant=resp.get("InvokedProductionVariant", ""),
        custom_attributes=resp.get("CustomAttributes", ""),
    )


def invoke_endpoint_async(
    endpoint_name: str,
    input_location: str,
    content_type: str = "application/json",
    accept: str = "application/json",
    inference_id: str | None = None,
    custom_attributes: str | None = None,
    region_name: str | None = None,
) -> InvokeEndpointAsyncResult:
    """Invoke a SageMaker async inference endpoint.

    Args:
        endpoint_name: Name of the async endpoint.
        input_location: S3 URI of the input payload.
        content_type: MIME type of the input data.
        accept: Desired MIME type for the output.
        inference_id: Identifier for tracking the request.
        custom_attributes: Custom attributes for the request.
        region_name: AWS region override.

    Returns:
        An :class:`InvokeEndpointAsyncResult` with the output location.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = get_client("sagemaker-runtime", region_name)
    kwargs: dict[str, Any] = {
        "EndpointName": endpoint_name,
        "InputLocation": input_location,
        "ContentType": content_type,
        "Accept": accept,
    }
    if inference_id is not None:
        kwargs["InferenceId"] = inference_id
    if custom_attributes is not None:
        kwargs["CustomAttributes"] = custom_attributes
    try:
        resp = client.invoke_endpoint_async(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "invoke_endpoint_async failed") from exc
    return InvokeEndpointAsyncResult(
        inference_id=resp.get("InferenceId", ""),
        output_location=resp.get("OutputLocation", ""),
        failure_location=resp.get("FailureLocation", ""),
    )


def invoke_endpoint_with_response_stream(
    endpoint_name: str,
    body: str | bytes,
    content_type: str = "application/json",
    accept: str = "application/json",
    target_variant: str | None = None,
    inference_id: str | None = None,
    custom_attributes: str | None = None,
    region_name: str | None = None,
) -> list[bytes]:
    """Invoke a SageMaker endpoint with response streaming.

    Collects all streamed chunks and returns them as a list.

    Args:
        endpoint_name: Name of the deployed SageMaker endpoint.
        body: Request payload (JSON string or raw bytes).
        content_type: MIME type of the request body.
        accept: Desired MIME type for the response.
        target_variant: Target variant for A/B test endpoints.
        inference_id: Identifier for tracking the request.
        custom_attributes: Custom attributes for the request.
        region_name: AWS region override.

    Returns:
        A list of byte chunks from the streamed response.

    Raises:
        RuntimeError: If the invocation fails.
    """
    client = get_client("sagemaker-runtime", region_name)
    kwargs: dict[str, Any] = {
        "EndpointName": endpoint_name,
        "Body": body if isinstance(body, bytes) else body.encode("utf-8"),
        "ContentType": content_type,
        "Accept": accept,
    }
    if target_variant is not None:
        kwargs["TargetVariant"] = target_variant
    if inference_id is not None:
        kwargs["InferenceId"] = inference_id
    if custom_attributes is not None:
        kwargs["CustomAttributes"] = custom_attributes
    try:
        resp = client.invoke_endpoint_with_response_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "invoke_endpoint_with_response_stream failed") from exc
    chunks: list[bytes] = []
    event_stream = resp.get("Body", [])
    for event in event_stream:
        payload = event.get("PayloadPart", {}).get("Bytes", b"")
        if payload:
            chunks.append(payload)
    return chunks
