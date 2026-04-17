"""Tests for aws_util.personalize_runtime module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.personalize_runtime import (
    PersonalizedItem,
    get_personalized_ranking,
    get_recommendations,
    get_action_recommendations,
)

REGION = "us-east-1"
CAMPAIGN_ARN = "arn:aws:personalize:us-east-1:123456789012:campaign/my-camp"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_personalized_item_model():
    item = PersonalizedItem(item_id="item-1", score=0.95)
    assert item.item_id == "item-1"
    assert item.score == 0.95


def test_personalized_item_defaults():
    item = PersonalizedItem(item_id="item-2")
    assert item.score == 0.0


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------


@patch("aws_util.personalize_runtime.get_client")
def test_get_recommendations_with_user_id(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_recommendations.return_value = {
        "itemList": [
            {"itemId": "i1", "score": 0.9},
            {"itemId": "i2", "score": 0.8},
        ],
    }
    result = get_recommendations(
        CAMPAIGN_ARN, user_id="user-1", region_name=REGION,
    )
    assert len(result) == 2
    assert result[0].item_id == "i1"
    assert result[0].score == 0.9


@patch("aws_util.personalize_runtime.get_client")
def test_get_recommendations_with_item_id(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_recommendations.return_value = {
        "itemList": [{"itemId": "related-1", "score": 0.7}],
    }
    result = get_recommendations(
        CAMPAIGN_ARN, item_id="item-src", num_results=10, region_name=REGION,
    )
    assert len(result) == 1
    assert result[0].item_id == "related-1"


@patch("aws_util.personalize_runtime.get_client")
def test_get_recommendations_empty(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_recommendations.return_value = {}
    result = get_recommendations(CAMPAIGN_ARN, region_name=REGION)
    assert result == []


@patch("aws_util.personalize_runtime.get_client")
def test_get_recommendations_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_recommendations.side_effect = _client_error("ValidationException")
    with pytest.raises(RuntimeError):
        get_recommendations(CAMPAIGN_ARN, user_id="u1", region_name=REGION)


# ---------------------------------------------------------------------------
# get_personalized_ranking
# ---------------------------------------------------------------------------


@patch("aws_util.personalize_runtime.get_client")
def test_get_personalized_ranking_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_personalized_ranking.return_value = {
        "personalizedRanking": [
            {"itemId": "a", "score": 0.95},
            {"itemId": "b", "score": 0.80},
            {"itemId": "c", "score": 0.60},
        ],
    }
    result = get_personalized_ranking(
        CAMPAIGN_ARN, "user-1", ["a", "b", "c"], region_name=REGION,
    )
    assert len(result) == 3
    assert result[0].item_id == "a"
    assert result[2].score == 0.60


@patch("aws_util.personalize_runtime.get_client")
def test_get_personalized_ranking_empty(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_personalized_ranking.return_value = {}
    result = get_personalized_ranking(
        CAMPAIGN_ARN, "user-1", ["x"], region_name=REGION,
    )
    assert result == []


@patch("aws_util.personalize_runtime.get_client")
def test_get_personalized_ranking_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_personalized_ranking.side_effect = _client_error(
        "ResourceNotFoundException",
    )
    with pytest.raises(RuntimeError):
        get_personalized_ranking(
            CAMPAIGN_ARN, "user-1", ["a"], region_name=REGION,
        )


@patch("aws_util.personalize_runtime.get_client")
def test_get_action_recommendations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_action_recommendations.return_value = {}
    get_action_recommendations(region_name=REGION)
    mock_client.get_action_recommendations.assert_called_once()


@patch("aws_util.personalize_runtime.get_client")
def test_get_action_recommendations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_action_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_action_recommendations",
    )
    with pytest.raises(RuntimeError, match="Failed to get action recommendations"):
        get_action_recommendations(region_name=REGION)


def test_get_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize_runtime import get_recommendations
    mock_client = MagicMock()
    mock_client.get_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.personalize_runtime.get_client", lambda *a, **kw: mock_client)
    get_recommendations("test-campaign_arn", user_id="test-user_id", item_id="test-item_id", region_name="us-east-1")
    mock_client.get_recommendations.assert_called_once()

def test_get_action_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize_runtime import get_action_recommendations
    mock_client = MagicMock()
    mock_client.get_action_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.personalize_runtime.get_client", lambda *a, **kw: mock_client)
    get_action_recommendations(campaign_arn="test-campaign_arn", user_id="test-user_id", num_results="test-num_results", filter_arn="test-filter_arn", filter_values="test-filter_values", region_name="us-east-1")
    mock_client.get_action_recommendations.assert_called_once()
