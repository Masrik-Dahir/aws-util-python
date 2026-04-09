"""Tests for aws_util.aio.personalize_runtime module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.personalize_runtime import (
    PersonalizedItem,
    get_personalized_ranking,
    get_recommendations,
    get_action_recommendations,
)



REGION = "us-east-1"
CAMPAIGN_ARN = "arn:aws:personalize:us-east-1:123456789012:campaign/my-camp"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------


async def test_get_recommendations_with_user_id(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "itemList": [
            {"itemId": "i1", "score": 0.9},
            {"itemId": "i2", "score": 0.8},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    result = await get_recommendations(
        CAMPAIGN_ARN, user_id="user-1", region_name=REGION,
    )
    assert len(result) == 2
    assert result[0].item_id == "i1"


async def test_get_recommendations_with_item_id(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "itemList": [{"itemId": "related-1", "score": 0.7}],
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    result = await get_recommendations(
        CAMPAIGN_ARN, item_id="src-item", num_results=5, region_name=REGION,
    )
    assert len(result) == 1
    assert result[0].item_id == "related-1"


async def test_get_recommendations_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    result = await get_recommendations(CAMPAIGN_ARN, region_name=REGION)
    assert result == []


async def test_get_recommendations_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_recommendations(
            CAMPAIGN_ARN, user_id="u1", region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_personalized_ranking
# ---------------------------------------------------------------------------


async def test_get_personalized_ranking_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "personalizedRanking": [
            {"itemId": "a", "score": 0.95},
            {"itemId": "b", "score": 0.80},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    result = await get_personalized_ranking(
        CAMPAIGN_ARN, "user-1", ["a", "b"], region_name=REGION,
    )
    assert len(result) == 2
    assert result[0].item_id == "a"


async def test_get_personalized_ranking_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    result = await get_personalized_ranking(
        CAMPAIGN_ARN, "user-1", ["x"], region_name=REGION,
    )
    assert result == []


async def test_get_personalized_ranking_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_personalized_ranking(
            CAMPAIGN_ARN, "user-1", ["a"], region_name=REGION,
        )


async def test_get_action_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_action_recommendations()
    mock_client.call.assert_called_once()


async def test_get_action_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize_runtime.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_action_recommendations()


@pytest.mark.asyncio
async def test_get_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize_runtime import get_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize_runtime.async_client", lambda *a, **kw: mock_client)
    await get_recommendations("test-campaign_arn", user_id="test-user_id", item_id="test-item_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_action_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize_runtime import get_action_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize_runtime.async_client", lambda *a, **kw: mock_client)
    await get_action_recommendations(campaign_arn="test-campaign_arn", user_id="test-user_id", num_results="test-num_results", filter_arn="test-filter_arn", filter_values="test-filter_values", region_name="us-east-1")
    mock_client.call.assert_called_once()
