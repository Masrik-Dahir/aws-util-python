"""aws_util.personalize_runtime — Utilities for Amazon Personalize Runtime.

Wraps the ``personalize-runtime`` boto3 service to fetch real-time
recommendations and personalized rankings from deployed campaigns.

Usage::

    from aws_util.personalize_runtime import (
        get_recommendations,
        get_personalized_ranking,
    )

    recs = get_recommendations(campaign_arn="arn:...", user_id="user-1")
    ranked = get_personalized_ranking(
        campaign_arn="arn:...",
        user_id="user-1",
        input_list=["item-A", "item-B", "item-C"],
    )
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "GetActionRecommendationsResult",
    "PersonalizedItem",
    "get_action_recommendations",
    "get_personalized_ranking",
    "get_recommendations",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class PersonalizedItem(BaseModel):
    """A single recommended or ranked item."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    item_id: str
    score: float = 0.0


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_recommendations(
    campaign_arn: str,
    *,
    user_id: str | None = None,
    item_id: str | None = None,
    num_results: int = 25,
    region_name: str | None = None,
) -> list[PersonalizedItem]:
    """Get real-time item recommendations from a Personalize campaign.

    Provide *user_id* for user-personalisation recipes or *item_id* for
    related-items recipes.

    Args:
        campaign_arn: ARN of the deployed campaign.
        user_id: User ID for personalised recommendations.
        item_id: Item ID for related-items recommendations.
        num_results: Maximum number of items to return (default ``25``).
        region_name: AWS region override.

    Returns:
        A list of :class:`PersonalizedItem` objects ordered by relevance.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("personalize-runtime", region_name)
    kwargs: dict[str, object] = {
        "campaignArn": campaign_arn,
        "numResults": num_results,
    }
    if user_id is not None:
        kwargs["userId"] = user_id
    if item_id is not None:
        kwargs["itemId"] = item_id
    try:
        resp = client.get_recommendations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_recommendations failed") from exc
    return [
        PersonalizedItem(
            item_id=item.get("itemId", ""),
            score=item.get("score", 0.0),
        )
        for item in resp.get("itemList", [])
    ]


def get_personalized_ranking(
    campaign_arn: str,
    user_id: str,
    input_list: list[str],
    *,
    region_name: str | None = None,
) -> list[PersonalizedItem]:
    """Re-rank a list of items for a specific user.

    Args:
        campaign_arn: ARN of the deployed campaign (must use a
            personalised-ranking recipe).
        user_id: The user to rank items for.
        input_list: Item IDs to rank.
        region_name: AWS region override.

    Returns:
        A list of :class:`PersonalizedItem` in personalised order.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("personalize-runtime", region_name)
    try:
        resp = client.get_personalized_ranking(
            campaignArn=campaign_arn,
            userId=user_id,
            inputList=input_list,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_personalized_ranking failed") from exc
    return [
        PersonalizedItem(
            item_id=item.get("itemId", ""),
            score=item.get("score", 0.0),
        )
        for item in resp.get("personalizedRanking", [])
    ]


class GetActionRecommendationsResult(BaseModel):
    """Result of get_action_recommendations."""

    model_config = ConfigDict(frozen=True)

    action_list: list[dict[str, Any]] | None = None
    recommendation_id: str | None = None


def get_action_recommendations(
    *,
    campaign_arn: str | None = None,
    user_id: str | None = None,
    num_results: int | None = None,
    filter_arn: str | None = None,
    filter_values: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetActionRecommendationsResult:
    """Get action recommendations.

    Args:
        campaign_arn: Campaign arn.
        user_id: User id.
        num_results: Num results.
        filter_arn: Filter arn.
        filter_values: Filter values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("personalize-runtime", region_name)
    kwargs: dict[str, Any] = {}
    if campaign_arn is not None:
        kwargs["campaignArn"] = campaign_arn
    if user_id is not None:
        kwargs["userId"] = user_id
    if num_results is not None:
        kwargs["numResults"] = num_results
    if filter_arn is not None:
        kwargs["filterArn"] = filter_arn
    if filter_values is not None:
        kwargs["filterValues"] = filter_values
    try:
        resp = client.get_action_recommendations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get action recommendations") from exc
    return GetActionRecommendationsResult(
        action_list=resp.get("actionList"),
        recommendation_id=resp.get("recommendationId"),
    )
