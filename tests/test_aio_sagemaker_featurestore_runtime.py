"""Tests for aws_util.aio.sagemaker_featurestore_runtime — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.sagemaker_featurestore_runtime import (
    BatchGetRecordResult,
    FeatureRecord,
    batch_get_record,
    delete_record,
    get_record,
    put_record,
)

FG = "my-feature-group"
RID = "rec-123"
RECORD = [{"FeatureName": "id", "ValueAsString": "123"}]


def _factory(client):
    return lambda *a, **kw: client


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------


async def test_put_record_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    await put_record(FG, RECORD)
    client.call.assert_called_once()


async def test_put_record_with_target_stores(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    await put_record(FG, RECORD, target_stores=["OnlineStore"])


async def test_put_record_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(RuntimeError):
        await put_record(FG, RECORD)


async def test_put_record_non_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(Exception):
        await put_record(FG, RECORD)


# ---------------------------------------------------------------------------
# get_record
# ---------------------------------------------------------------------------


async def test_get_record_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Record": RECORD}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    result = await get_record(FG, RID)
    assert isinstance(result, FeatureRecord)
    assert result.features == RECORD


async def test_get_record_with_feature_names(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Record": RECORD}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    await get_record(FG, RID, feature_names=["id"])


async def test_get_record_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(RuntimeError):
        await get_record(FG, RID)


async def test_get_record_non_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(Exception):
        await get_record(FG, RID)


# ---------------------------------------------------------------------------
# delete_record
# ---------------------------------------------------------------------------


async def test_delete_record_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    await delete_record(FG, RID, "2024-01-01T00:00:00Z")


async def test_delete_record_with_target_stores(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    await delete_record(FG, RID, "2024-01-01T00:00:00Z", target_stores=["OnlineStore"])


async def test_delete_record_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_record(FG, RID, "2024-01-01T00:00:00Z")


async def test_delete_record_non_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(Exception):
        await delete_record(FG, RID, "2024-01-01T00:00:00Z")


# ---------------------------------------------------------------------------
# batch_get_record
# ---------------------------------------------------------------------------


async def test_batch_get_record_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Records": [
            {
                "FeatureGroupName": FG,
                "RecordIdentifierValueAsString": RID,
                "Record": RECORD,
            }
        ],
        "Errors": [],
        "UnprocessedIdentifiers": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    result = await batch_get_record([{"FeatureGroupName": FG}])
    assert isinstance(result, BatchGetRecordResult)
    assert len(result.records) == 1


async def test_batch_get_record_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    result = await batch_get_record([])
    assert result.records == []


async def test_batch_get_record_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(RuntimeError):
        await batch_get_record([])


async def test_batch_get_record_non_runtime_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = ValueError("oops")
    monkeypatch.setattr(
        "aws_util.aio.sagemaker_featurestore_runtime.async_client",
        _factory(client),
    )
    with pytest.raises(Exception):
        await batch_get_record([])
