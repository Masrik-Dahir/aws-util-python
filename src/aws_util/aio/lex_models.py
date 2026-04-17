"""Native async Lex V2 Models utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error
from aws_util.lex_models import (
    BatchCreateCustomVocabularyItemResult,
    BatchDeleteCustomVocabularyItemResult,
    BatchUpdateCustomVocabularyItemResult,
    BotLocaleInfo,
    BotSummary,
    CreateBotAliasResult,
    CreateBotLocaleResult,
    CreateBotReplicaResult,
    CreateBotVersionResult,
    CreateExportResult,
    CreateResourcePolicyResult,
    CreateResourcePolicyStatementResult,
    CreateSlotResult,
    CreateTestSetDiscrepancyReportResult,
    CreateUploadUrlResult,
    DeleteBotAliasResult,
    DeleteBotLocaleResult,
    DeleteBotReplicaResult,
    DeleteBotVersionResult,
    DeleteCustomVocabularyResult,
    DeleteExportResult,
    DeleteImportResult,
    DeleteResourcePolicyResult,
    DeleteResourcePolicyStatementResult,
    DescribeBotAliasResult,
    DescribeBotRecommendationResult,
    DescribeBotReplicaResult,
    DescribeBotResourceGenerationResult,
    DescribeBotVersionResult,
    DescribeCustomVocabularyMetadataResult,
    DescribeExportResult,
    DescribeImportResult,
    DescribeResourcePolicyResult,
    DescribeSlotResult,
    DescribeSlotTypeResult,
    DescribeTestExecutionResult,
    DescribeTestSetDiscrepancyReportResult,
    DescribeTestSetGenerationResult,
    DescribeTestSetResult,
    GenerateBotElementResult,
    GetTestExecutionArtifactsUrlResult,
    IntentSummary,
    ListAggregatedUtterancesResult,
    ListBotAliasesResult,
    ListBotAliasReplicasResult,
    ListBotLocalesResult,
    ListBotRecommendationsResult,
    ListBotReplicasResult,
    ListBotResourceGenerationsResult,
    ListBotVersionReplicasResult,
    ListBotVersionsResult,
    ListBuiltInIntentsResult,
    ListBuiltInSlotTypesResult,
    ListCustomVocabularyItemsResult,
    ListExportsResult,
    ListImportsResult,
    ListIntentMetricsResult,
    ListIntentPathsResult,
    ListIntentStageMetricsResult,
    ListRecommendedIntentsResult,
    ListSessionAnalyticsDataResult,
    ListSessionMetricsResult,
    ListSlotsResult,
    ListSlotTypesResult,
    ListTagsForResourceResult,
    ListTestExecutionResultItemsResult,
    ListTestExecutionsResult,
    ListTestSetRecordsResult,
    ListTestSetsResult,
    ListUtteranceAnalyticsDataResult,
    ListUtteranceMetricsResult,
    SearchAssociatedTranscriptsResult,
    StartBotRecommendationResult,
    StartBotResourceGenerationResult,
    StartImportResult,
    StartTestExecutionResult,
    StartTestSetGenerationResult,
    StopBotRecommendationResult,
    UpdateBotAliasResult,
    UpdateBotLocaleResult,
    UpdateBotRecommendationResult,
    UpdateBotResult,
    UpdateExportResult,
    UpdateIntentResult,
    UpdateResourcePolicyResult,
    UpdateSlotResult,
    UpdateSlotTypeResult,
    UpdateTestSetResult,
)

__all__ = [
    "BatchCreateCustomVocabularyItemResult",
    "BatchDeleteCustomVocabularyItemResult",
    "BatchUpdateCustomVocabularyItemResult",
    "BotLocaleInfo",
    "BotSummary",
    "CreateBotAliasResult",
    "CreateBotLocaleResult",
    "CreateBotReplicaResult",
    "CreateBotVersionResult",
    "CreateExportResult",
    "CreateResourcePolicyResult",
    "CreateResourcePolicyStatementResult",
    "CreateSlotResult",
    "CreateTestSetDiscrepancyReportResult",
    "CreateUploadUrlResult",
    "DeleteBotAliasResult",
    "DeleteBotLocaleResult",
    "DeleteBotReplicaResult",
    "DeleteBotVersionResult",
    "DeleteCustomVocabularyResult",
    "DeleteExportResult",
    "DeleteImportResult",
    "DeleteResourcePolicyResult",
    "DeleteResourcePolicyStatementResult",
    "DescribeBotAliasResult",
    "DescribeBotRecommendationResult",
    "DescribeBotReplicaResult",
    "DescribeBotResourceGenerationResult",
    "DescribeBotVersionResult",
    "DescribeCustomVocabularyMetadataResult",
    "DescribeExportResult",
    "DescribeImportResult",
    "DescribeResourcePolicyResult",
    "DescribeSlotResult",
    "DescribeSlotTypeResult",
    "DescribeTestExecutionResult",
    "DescribeTestSetDiscrepancyReportResult",
    "DescribeTestSetGenerationResult",
    "DescribeTestSetResult",
    "GenerateBotElementResult",
    "GetTestExecutionArtifactsUrlResult",
    "IntentSummary",
    "ListAggregatedUtterancesResult",
    "ListBotAliasReplicasResult",
    "ListBotAliasesResult",
    "ListBotLocalesResult",
    "ListBotRecommendationsResult",
    "ListBotReplicasResult",
    "ListBotResourceGenerationsResult",
    "ListBotVersionReplicasResult",
    "ListBotVersionsResult",
    "ListBuiltInIntentsResult",
    "ListBuiltInSlotTypesResult",
    "ListCustomVocabularyItemsResult",
    "ListExportsResult",
    "ListImportsResult",
    "ListIntentMetricsResult",
    "ListIntentPathsResult",
    "ListIntentStageMetricsResult",
    "ListRecommendedIntentsResult",
    "ListSessionAnalyticsDataResult",
    "ListSessionMetricsResult",
    "ListSlotTypesResult",
    "ListSlotsResult",
    "ListTagsForResourceResult",
    "ListTestExecutionResultItemsResult",
    "ListTestExecutionsResult",
    "ListTestSetRecordsResult",
    "ListTestSetsResult",
    "ListUtteranceAnalyticsDataResult",
    "ListUtteranceMetricsResult",
    "SearchAssociatedTranscriptsResult",
    "StartBotRecommendationResult",
    "StartBotResourceGenerationResult",
    "StartImportResult",
    "StartTestExecutionResult",
    "StartTestSetGenerationResult",
    "StopBotRecommendationResult",
    "UpdateBotAliasResult",
    "UpdateBotLocaleResult",
    "UpdateBotRecommendationResult",
    "UpdateBotResult",
    "UpdateExportResult",
    "UpdateIntentResult",
    "UpdateResourcePolicyResult",
    "UpdateSlotResult",
    "UpdateSlotTypeResult",
    "UpdateTestSetResult",
    "batch_create_custom_vocabulary_item",
    "batch_delete_custom_vocabulary_item",
    "batch_update_custom_vocabulary_item",
    "build_bot_locale",
    "create_bot",
    "create_bot_alias",
    "create_bot_locale",
    "create_bot_replica",
    "create_bot_version",
    "create_export",
    "create_intent",
    "create_resource_policy",
    "create_resource_policy_statement",
    "create_slot",
    "create_slot_type",
    "create_test_set_discrepancy_report",
    "create_upload_url",
    "delete_bot",
    "delete_bot_alias",
    "delete_bot_locale",
    "delete_bot_replica",
    "delete_bot_version",
    "delete_custom_vocabulary",
    "delete_export",
    "delete_import",
    "delete_intent",
    "delete_resource_policy",
    "delete_resource_policy_statement",
    "delete_slot",
    "delete_slot_type",
    "delete_test_set",
    "delete_utterances",
    "describe_bot",
    "describe_bot_alias",
    "describe_bot_locale",
    "describe_bot_recommendation",
    "describe_bot_replica",
    "describe_bot_resource_generation",
    "describe_bot_version",
    "describe_custom_vocabulary_metadata",
    "describe_export",
    "describe_import",
    "describe_resource_policy",
    "describe_slot",
    "describe_slot_type",
    "describe_test_execution",
    "describe_test_set",
    "describe_test_set_discrepancy_report",
    "describe_test_set_generation",
    "generate_bot_element",
    "get_test_execution_artifacts_url",
    "list_aggregated_utterances",
    "list_bot_alias_replicas",
    "list_bot_aliases",
    "list_bot_locales",
    "list_bot_recommendations",
    "list_bot_replicas",
    "list_bot_resource_generations",
    "list_bot_version_replicas",
    "list_bot_versions",
    "list_bots",
    "list_built_in_intents",
    "list_built_in_slot_types",
    "list_custom_vocabulary_items",
    "list_exports",
    "list_imports",
    "list_intent_metrics",
    "list_intent_paths",
    "list_intent_stage_metrics",
    "list_intents",
    "list_recommended_intents",
    "list_session_analytics_data",
    "list_session_metrics",
    "list_slot_types",
    "list_slots",
    "list_tags_for_resource",
    "list_test_execution_result_items",
    "list_test_executions",
    "list_test_set_records",
    "list_test_sets",
    "list_utterance_analytics_data",
    "list_utterance_metrics",
    "search_associated_transcripts",
    "start_bot_recommendation",
    "start_bot_resource_generation",
    "start_import",
    "start_test_execution",
    "start_test_set_generation",
    "stop_bot_recommendation",
    "tag_resource",
    "untag_resource",
    "update_bot",
    "update_bot_alias",
    "update_bot_locale",
    "update_bot_recommendation",
    "update_export",
    "update_intent",
    "update_resource_policy",
    "update_slot",
    "update_slot_type",
    "update_test_set",
    "wait_for_bot_locale",
]


# ---------------------------------------------------------------------------
# Bot operations
# ---------------------------------------------------------------------------


async def create_bot(
    bot_name: str,
    role_arn: str,
    data_privacy_child_directed: bool = False,
    idle_session_ttl: int = 300,
    description: str = "",
    bot_type: str = "Bot",
    region_name: str | None = None,
) -> dict[str, Any]:
    """Create a new Lex V2 bot.

    Args:
        bot_name: Name of the bot.
        role_arn: IAM role ARN for the bot.
        data_privacy_child_directed: Whether the bot is directed at children.
        idle_session_ttl: Session idle timeout in seconds.
        description: Optional bot description.
        bot_type: Bot type (default ``"Bot"``).
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {
        "botName": bot_name,
        "roleArn": role_arn,
        "dataPrivacy": {"childDirected": data_privacy_child_directed},
        "idleSessionTTLInSeconds": idle_session_ttl,
        "botType": bot_type,
    }
    if description:
        kwargs["description"] = description
    try:
        return await client.call("CreateBot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_bot failed") from exc


async def describe_bot(
    bot_id: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Describe a Lex V2 bot.

    Args:
        bot_id: The bot identifier.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        return await client.call("DescribeBot", botId=bot_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_bot failed") from exc


async def list_bots(
    region_name: str | None = None,
) -> list[BotSummary]:
    """List all Lex V2 bots.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`BotSummary` objects.

    Raises:
        RuntimeError: If the list call fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        resp = await client.call("ListBots")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_bots failed") from exc
    return [
        BotSummary(
            bot_id=b["botId"],
            bot_name=b["botName"],
            bot_status=b.get("botStatus", ""),
            description=b.get("description", ""),
        )
        for b in resp.get("botSummaries", [])
    ]


async def delete_bot(
    bot_id: str,
    skip_resource_in_use_check: bool = True,
    region_name: str | None = None,
) -> None:
    """Delete a Lex V2 bot.

    Args:
        bot_id: The bot identifier.
        skip_resource_in_use_check: Skip the in-use check (default ``True``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        await client.call(
            "DeleteBot",
            botId=bot_id,
            skipResourceInUseCheck=skip_resource_in_use_check,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_bot failed") from exc


# ---------------------------------------------------------------------------
# Intent operations
# ---------------------------------------------------------------------------


async def create_intent(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_name: str,
    description: str = "",
    sample_utterances: list[str] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Create a new intent for a Lex V2 bot.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version (typically ``"DRAFT"``).
        locale_id: The locale identifier (e.g. ``"en_US"``).
        intent_name: Name of the intent.
        description: Optional description.
        sample_utterances: Optional list of sample utterance strings.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {
        "intentName": intent_name,
        "botId": bot_id,
        "botVersion": bot_version,
        "localeId": locale_id,
    }
    if description:
        kwargs["description"] = description
    if sample_utterances:
        kwargs["sampleUtterances"] = [{"utterance": u} for u in sample_utterances]
    try:
        return await client.call("CreateIntent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_intent failed") from exc


async def describe_intent(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Describe an intent.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        intent_id: The intent identifier.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        return await client.call(
            "DescribeIntent",
            intentId=intent_id,
            botId=bot_id,
            botVersion=bot_version,
            localeId=locale_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_intent failed") from exc


async def list_intents(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> list[IntentSummary]:
    """List intents for a Lex V2 bot locale.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        region_name: AWS region override.

    Returns:
        A list of :class:`IntentSummary` objects.

    Raises:
        RuntimeError: If the list call fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        resp = await client.call(
            "ListIntents",
            botId=bot_id,
            botVersion=bot_version,
            localeId=locale_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "list_intents failed") from exc
    return [
        IntentSummary(
            intent_id=i["intentId"],
            intent_name=i["intentName"],
            description=i.get("description", ""),
        )
        for i in resp.get("intentSummaries", [])
    ]


async def delete_intent(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    region_name: str | None = None,
) -> None:
    """Delete an intent from a Lex V2 bot.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        intent_id: The intent identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        await client.call(
            "DeleteIntent",
            intentId=intent_id,
            botId=bot_id,
            botVersion=bot_version,
            localeId=locale_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_intent failed") from exc


# ---------------------------------------------------------------------------
# Slot type operations
# ---------------------------------------------------------------------------


async def create_slot_type(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    slot_type_name: str,
    value_selection_setting: dict[str, Any] | None = None,
    slot_type_values: list[dict[str, Any]] | None = None,
    description: str = "",
    region_name: str | None = None,
) -> dict[str, Any]:
    """Create a slot type for a Lex V2 bot locale.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        slot_type_name: Name of the slot type.
        value_selection_setting: How slot values are selected.
        slot_type_values: List of slot type value definitions.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {
        "slotTypeName": slot_type_name,
        "botId": bot_id,
        "botVersion": bot_version,
        "localeId": locale_id,
        "valueSelectionSetting": value_selection_setting
        or {
            "resolutionStrategy": "OriginalValue",
        },
    }
    if slot_type_values:
        kwargs["slotTypeValues"] = slot_type_values
    if description:
        kwargs["description"] = description
    try:
        return await client.call("CreateSlotType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_slot_type failed") from exc


# ---------------------------------------------------------------------------
# Bot locale operations
# ---------------------------------------------------------------------------


async def build_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Trigger a build for a Lex V2 bot locale.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the build request fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        return await client.call(
            "BuildBotLocale",
            botId=bot_id,
            botVersion=bot_version,
            localeId=locale_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "build_bot_locale failed") from exc


async def describe_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> BotLocaleInfo:
    """Describe a Lex V2 bot locale.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        region_name: AWS region override.

    Returns:
        A :class:`BotLocaleInfo` with locale details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("lexv2-models", region_name)
    try:
        resp = await client.call(
            "DescribeBotLocale",
            botId=bot_id,
            botVersion=bot_version,
            localeId=locale_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_bot_locale failed") from exc
    return BotLocaleInfo(
        bot_id=resp.get("botId", ""),
        bot_version=resp.get("botVersion", ""),
        locale_id=resp.get("localeId", ""),
        locale_name=resp.get("localeName", ""),
        bot_locale_status=resp.get("botLocaleStatus", ""),
    )


async def wait_for_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    target_status: str = "Built",
    interval: float = 5.0,
    max_wait: float = 300.0,
    region_name: str | None = None,
) -> BotLocaleInfo:
    """Poll until a bot locale reaches *target_status*.

    Args:
        bot_id: The bot identifier.
        bot_version: The bot version.
        locale_id: The locale identifier.
        target_status: Desired status (default ``"Built"``).
        interval: Seconds between polls.
        max_wait: Maximum wait time in seconds.
        region_name: AWS region override.

    Returns:
        The final :class:`BotLocaleInfo`.

    Raises:
        RuntimeError: If the wait times out or a failure status is detected.
    """
    deadline = time.monotonic() + max_wait
    while True:
        info = await describe_bot_locale(
            bot_id,
            bot_version,
            locale_id,
            region_name=region_name,
        )
        if info.bot_locale_status == target_status:
            return info
        if info.bot_locale_status in ("Failed", "Deleting"):
            raise AwsServiceError(f"Bot locale reached terminal status: {info.bot_locale_status}")
        if time.monotonic() + interval > deadline:
            raise AwsServiceError(
                f"wait_for_bot_locale timed out after {max_wait}s "
                f"(current status: {info.bot_locale_status})"
            )
        await asyncio.sleep(interval)


async def batch_create_custom_vocabulary_item(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    custom_vocabulary_item_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchCreateCustomVocabularyItemResult:
    """Batch create custom vocabulary item.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        custom_vocabulary_item_list: Custom vocabulary item list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["customVocabularyItemList"] = custom_vocabulary_item_list
    try:
        resp = await client.call("BatchCreateCustomVocabularyItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch create custom vocabulary item") from exc
    return BatchCreateCustomVocabularyItemResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        errors=resp.get("errors"),
        resources=resp.get("resources"),
    )


async def batch_delete_custom_vocabulary_item(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    custom_vocabulary_item_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchDeleteCustomVocabularyItemResult:
    """Batch delete custom vocabulary item.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        custom_vocabulary_item_list: Custom vocabulary item list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["customVocabularyItemList"] = custom_vocabulary_item_list
    try:
        resp = await client.call("BatchDeleteCustomVocabularyItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete custom vocabulary item") from exc
    return BatchDeleteCustomVocabularyItemResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        errors=resp.get("errors"),
        resources=resp.get("resources"),
    )


async def batch_update_custom_vocabulary_item(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    custom_vocabulary_item_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchUpdateCustomVocabularyItemResult:
    """Batch update custom vocabulary item.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        custom_vocabulary_item_list: Custom vocabulary item list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["customVocabularyItemList"] = custom_vocabulary_item_list
    try:
        resp = await client.call("BatchUpdateCustomVocabularyItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update custom vocabulary item") from exc
    return BatchUpdateCustomVocabularyItemResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        errors=resp.get("errors"),
        resources=resp.get("resources"),
    )


async def create_bot_alias(
    bot_alias_name: str,
    bot_id: str,
    *,
    description: str | None = None,
    bot_version: str | None = None,
    bot_alias_locale_settings: dict[str, Any] | None = None,
    conversation_log_settings: dict[str, Any] | None = None,
    sentiment_analysis_settings: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateBotAliasResult:
    """Create bot alias.

    Args:
        bot_alias_name: Bot alias name.
        bot_id: Bot id.
        description: Description.
        bot_version: Bot version.
        bot_alias_locale_settings: Bot alias locale settings.
        conversation_log_settings: Conversation log settings.
        sentiment_analysis_settings: Sentiment analysis settings.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botAliasName"] = bot_alias_name
    kwargs["botId"] = bot_id
    if description is not None:
        kwargs["description"] = description
    if bot_version is not None:
        kwargs["botVersion"] = bot_version
    if bot_alias_locale_settings is not None:
        kwargs["botAliasLocaleSettings"] = bot_alias_locale_settings
    if conversation_log_settings is not None:
        kwargs["conversationLogSettings"] = conversation_log_settings
    if sentiment_analysis_settings is not None:
        kwargs["sentimentAnalysisSettings"] = sentiment_analysis_settings
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateBotAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bot alias") from exc
    return CreateBotAliasResult(
        bot_alias_id=resp.get("botAliasId"),
        bot_alias_name=resp.get("botAliasName"),
        description=resp.get("description"),
        bot_version=resp.get("botVersion"),
        bot_alias_locale_settings=resp.get("botAliasLocaleSettings"),
        conversation_log_settings=resp.get("conversationLogSettings"),
        sentiment_analysis_settings=resp.get("sentimentAnalysisSettings"),
        bot_alias_status=resp.get("botAliasStatus"),
        bot_id=resp.get("botId"),
        creation_date_time=resp.get("creationDateTime"),
        tags=resp.get("tags"),
    )


async def create_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    nlu_intent_confidence_threshold: float,
    *,
    description: str | None = None,
    voice_settings: dict[str, Any] | None = None,
    generative_ai_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateBotLocaleResult:
    """Create bot locale.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        nlu_intent_confidence_threshold: Nlu intent confidence threshold.
        description: Description.
        voice_settings: Voice settings.
        generative_ai_settings: Generative ai settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["nluIntentConfidenceThreshold"] = nlu_intent_confidence_threshold
    if description is not None:
        kwargs["description"] = description
    if voice_settings is not None:
        kwargs["voiceSettings"] = voice_settings
    if generative_ai_settings is not None:
        kwargs["generativeAISettings"] = generative_ai_settings
    try:
        resp = await client.call("CreateBotLocale", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bot locale") from exc
    return CreateBotLocaleResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_name=resp.get("localeName"),
        locale_id=resp.get("localeId"),
        description=resp.get("description"),
        nlu_intent_confidence_threshold=resp.get("nluIntentConfidenceThreshold"),
        voice_settings=resp.get("voiceSettings"),
        bot_locale_status=resp.get("botLocaleStatus"),
        creation_date_time=resp.get("creationDateTime"),
        generative_ai_settings=resp.get("generativeAISettings"),
    )


async def create_bot_replica(
    bot_id: str,
    replica_region: str,
    region_name: str | None = None,
) -> CreateBotReplicaResult:
    """Create bot replica.

    Args:
        bot_id: Bot id.
        replica_region: Replica region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["replicaRegion"] = replica_region
    try:
        resp = await client.call("CreateBotReplica", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bot replica") from exc
    return CreateBotReplicaResult(
        bot_id=resp.get("botId"),
        replica_region=resp.get("replicaRegion"),
        source_region=resp.get("sourceRegion"),
        creation_date_time=resp.get("creationDateTime"),
        bot_replica_status=resp.get("botReplicaStatus"),
    )


async def create_bot_version(
    bot_id: str,
    bot_version_locale_specification: dict[str, Any],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateBotVersionResult:
    """Create bot version.

    Args:
        bot_id: Bot id.
        bot_version_locale_specification: Bot version locale specification.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersionLocaleSpecification"] = bot_version_locale_specification
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("CreateBotVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bot version") from exc
    return CreateBotVersionResult(
        bot_id=resp.get("botId"),
        description=resp.get("description"),
        bot_version=resp.get("botVersion"),
        bot_version_locale_specification=resp.get("botVersionLocaleSpecification"),
        bot_status=resp.get("botStatus"),
        creation_date_time=resp.get("creationDateTime"),
    )


async def create_export(
    resource_specification: dict[str, Any],
    file_format: str,
    *,
    file_password: str | None = None,
    region_name: str | None = None,
) -> CreateExportResult:
    """Create export.

    Args:
        resource_specification: Resource specification.
        file_format: File format.
        file_password: File password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceSpecification"] = resource_specification
    kwargs["fileFormat"] = file_format
    if file_password is not None:
        kwargs["filePassword"] = file_password
    try:
        resp = await client.call("CreateExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create export") from exc
    return CreateExportResult(
        export_id=resp.get("exportId"),
        resource_specification=resp.get("resourceSpecification"),
        file_format=resp.get("fileFormat"),
        export_status=resp.get("exportStatus"),
        creation_date_time=resp.get("creationDateTime"),
    )


async def create_resource_policy(
    resource_arn: str,
    policy: str,
    region_name: str | None = None,
) -> CreateResourcePolicyResult:
    """Create resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["policy"] = policy
    try:
        resp = await client.call("CreateResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create resource policy") from exc
    return CreateResourcePolicyResult(
        resource_arn=resp.get("resourceArn"),
        revision_id=resp.get("revisionId"),
    )


async def create_resource_policy_statement(
    resource_arn: str,
    statement_id: str,
    effect: str,
    principal: list[dict[str, Any]],
    action: list[str],
    *,
    condition: dict[str, Any] | None = None,
    expected_revision_id: str | None = None,
    region_name: str | None = None,
) -> CreateResourcePolicyStatementResult:
    """Create resource policy statement.

    Args:
        resource_arn: Resource arn.
        statement_id: Statement id.
        effect: Effect.
        principal: Principal.
        action: Action.
        condition: Condition.
        expected_revision_id: Expected revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["statementId"] = statement_id
    kwargs["effect"] = effect
    kwargs["principal"] = principal
    kwargs["action"] = action
    if condition is not None:
        kwargs["condition"] = condition
    if expected_revision_id is not None:
        kwargs["expectedRevisionId"] = expected_revision_id
    try:
        resp = await client.call("CreateResourcePolicyStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create resource policy statement") from exc
    return CreateResourcePolicyStatementResult(
        resource_arn=resp.get("resourceArn"),
        revision_id=resp.get("revisionId"),
    )


async def create_slot(
    slot_name: str,
    value_elicitation_setting: dict[str, Any],
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    *,
    description: str | None = None,
    slot_type_id: str | None = None,
    obfuscation_setting: dict[str, Any] | None = None,
    multiple_values_setting: dict[str, Any] | None = None,
    sub_slot_setting: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateSlotResult:
    """Create slot.

    Args:
        slot_name: Slot name.
        value_elicitation_setting: Value elicitation setting.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        intent_id: Intent id.
        description: Description.
        slot_type_id: Slot type id.
        obfuscation_setting: Obfuscation setting.
        multiple_values_setting: Multiple values setting.
        sub_slot_setting: Sub slot setting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotName"] = slot_name
    kwargs["valueElicitationSetting"] = value_elicitation_setting
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["intentId"] = intent_id
    if description is not None:
        kwargs["description"] = description
    if slot_type_id is not None:
        kwargs["slotTypeId"] = slot_type_id
    if obfuscation_setting is not None:
        kwargs["obfuscationSetting"] = obfuscation_setting
    if multiple_values_setting is not None:
        kwargs["multipleValuesSetting"] = multiple_values_setting
    if sub_slot_setting is not None:
        kwargs["subSlotSetting"] = sub_slot_setting
    try:
        resp = await client.call("CreateSlot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create slot") from exc
    return CreateSlotResult(
        slot_id=resp.get("slotId"),
        slot_name=resp.get("slotName"),
        description=resp.get("description"),
        slot_type_id=resp.get("slotTypeId"),
        value_elicitation_setting=resp.get("valueElicitationSetting"),
        obfuscation_setting=resp.get("obfuscationSetting"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        intent_id=resp.get("intentId"),
        creation_date_time=resp.get("creationDateTime"),
        multiple_values_setting=resp.get("multipleValuesSetting"),
        sub_slot_setting=resp.get("subSlotSetting"),
    )


async def create_test_set_discrepancy_report(
    run_set_id: str,
    target: dict[str, Any],
    region_name: str | None = None,
) -> CreateTestSetDiscrepancyReportResult:
    """Create test set discrepancy report.

    Args:
        run_set_id: Run set id.
        target: Target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    kwargs["target"] = target
    try:
        resp = await client.call("CreateTestSetDiscrepancyReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create test set discrepancy report") from exc
    return CreateTestSetDiscrepancyReportResult(
        run_set_discrepancy_report_id=resp.get("testSetDiscrepancyReportId"),
        creation_date_time=resp.get("creationDateTime"),
        run_set_id=resp.get("testSetId"),
        target=resp.get("target"),
    )


async def create_upload_url(
    region_name: str | None = None,
) -> CreateUploadUrlResult:
    """Create upload url.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("CreateUploadUrl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create upload url") from exc
    return CreateUploadUrlResult(
        import_id=resp.get("importId"),
        upload_url=resp.get("uploadUrl"),
    )


async def delete_bot_alias(
    bot_alias_id: str,
    bot_id: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> DeleteBotAliasResult:
    """Delete bot alias.

    Args:
        bot_alias_id: Bot alias id.
        bot_id: Bot id.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botAliasId"] = bot_alias_id
    kwargs["botId"] = bot_id
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        resp = await client.call("DeleteBotAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bot alias") from exc
    return DeleteBotAliasResult(
        bot_alias_id=resp.get("botAliasId"),
        bot_id=resp.get("botId"),
        bot_alias_status=resp.get("botAliasStatus"),
    )


async def delete_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> DeleteBotLocaleResult:
    """Delete bot locale.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("DeleteBotLocale", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bot locale") from exc
    return DeleteBotLocaleResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_locale_status=resp.get("botLocaleStatus"),
    )


async def delete_bot_replica(
    bot_id: str,
    replica_region: str,
    region_name: str | None = None,
) -> DeleteBotReplicaResult:
    """Delete bot replica.

    Args:
        bot_id: Bot id.
        replica_region: Replica region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["replicaRegion"] = replica_region
    try:
        resp = await client.call("DeleteBotReplica", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bot replica") from exc
    return DeleteBotReplicaResult(
        bot_id=resp.get("botId"),
        replica_region=resp.get("replicaRegion"),
        bot_replica_status=resp.get("botReplicaStatus"),
    )


async def delete_bot_version(
    bot_id: str,
    bot_version: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> DeleteBotVersionResult:
    """Delete bot version.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        resp = await client.call("DeleteBotVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bot version") from exc
    return DeleteBotVersionResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        bot_status=resp.get("botStatus"),
    )


async def delete_custom_vocabulary(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> DeleteCustomVocabularyResult:
    """Delete custom vocabulary.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("DeleteCustomVocabulary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom vocabulary") from exc
    return DeleteCustomVocabularyResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        custom_vocabulary_status=resp.get("customVocabularyStatus"),
    )


async def delete_export(
    export_id: str,
    region_name: str | None = None,
) -> DeleteExportResult:
    """Delete export.

    Args:
        export_id: Export id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["exportId"] = export_id
    try:
        resp = await client.call("DeleteExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete export") from exc
    return DeleteExportResult(
        export_id=resp.get("exportId"),
        export_status=resp.get("exportStatus"),
    )


async def delete_import(
    import_id: str,
    region_name: str | None = None,
) -> DeleteImportResult:
    """Delete import.

    Args:
        import_id: Import id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["importId"] = import_id
    try:
        resp = await client.call("DeleteImport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete import") from exc
    return DeleteImportResult(
        import_id=resp.get("importId"),
        import_status=resp.get("importStatus"),
    )


async def delete_resource_policy(
    resource_arn: str,
    *,
    expected_revision_id: str | None = None,
    region_name: str | None = None,
) -> DeleteResourcePolicyResult:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        expected_revision_id: Expected revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if expected_revision_id is not None:
        kwargs["expectedRevisionId"] = expected_revision_id
    try:
        resp = await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return DeleteResourcePolicyResult(
        resource_arn=resp.get("resourceArn"),
        revision_id=resp.get("revisionId"),
    )


async def delete_resource_policy_statement(
    resource_arn: str,
    statement_id: str,
    *,
    expected_revision_id: str | None = None,
    region_name: str | None = None,
) -> DeleteResourcePolicyStatementResult:
    """Delete resource policy statement.

    Args:
        resource_arn: Resource arn.
        statement_id: Statement id.
        expected_revision_id: Expected revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["statementId"] = statement_id
    if expected_revision_id is not None:
        kwargs["expectedRevisionId"] = expected_revision_id
    try:
        resp = await client.call("DeleteResourcePolicyStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy statement") from exc
    return DeleteResourcePolicyStatementResult(
        resource_arn=resp.get("resourceArn"),
        revision_id=resp.get("revisionId"),
    )


async def delete_slot(
    slot_id: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    region_name: str | None = None,
) -> None:
    """Delete slot.

    Args:
        slot_id: Slot id.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        intent_id: Intent id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotId"] = slot_id
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["intentId"] = intent_id
    try:
        await client.call("DeleteSlot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete slot") from exc
    return None


async def delete_slot_type(
    slot_type_id: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete slot type.

    Args:
        slot_type_id: Slot type id.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotTypeId"] = slot_type_id
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        await client.call("DeleteSlotType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete slot type") from exc
    return None


async def delete_test_set(
    run_set_id: str,
    region_name: str | None = None,
) -> None:
    """Delete test set.

    Args:
        run_set_id: Run set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    try:
        await client.call("DeleteTestSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete test set") from exc
    return None


async def delete_utterances(
    bot_id: str,
    *,
    locale_id: str | None = None,
    session_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete utterances.

    Args:
        bot_id: Bot id.
        locale_id: Locale id.
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    if locale_id is not None:
        kwargs["localeId"] = locale_id
    if session_id is not None:
        kwargs["sessionId"] = session_id
    try:
        await client.call("DeleteUtterances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete utterances") from exc
    return None


async def describe_bot_alias(
    bot_alias_id: str,
    bot_id: str,
    region_name: str | None = None,
) -> DescribeBotAliasResult:
    """Describe bot alias.

    Args:
        bot_alias_id: Bot alias id.
        bot_id: Bot id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botAliasId"] = bot_alias_id
    kwargs["botId"] = bot_id
    try:
        resp = await client.call("DescribeBotAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bot alias") from exc
    return DescribeBotAliasResult(
        bot_alias_id=resp.get("botAliasId"),
        bot_alias_name=resp.get("botAliasName"),
        description=resp.get("description"),
        bot_version=resp.get("botVersion"),
        bot_alias_locale_settings=resp.get("botAliasLocaleSettings"),
        conversation_log_settings=resp.get("conversationLogSettings"),
        sentiment_analysis_settings=resp.get("sentimentAnalysisSettings"),
        bot_alias_history_events=resp.get("botAliasHistoryEvents"),
        bot_alias_status=resp.get("botAliasStatus"),
        bot_id=resp.get("botId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        parent_bot_networks=resp.get("parentBotNetworks"),
    )


async def describe_bot_recommendation(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    bot_recommendation_id: str,
    region_name: str | None = None,
) -> DescribeBotRecommendationResult:
    """Describe bot recommendation.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        bot_recommendation_id: Bot recommendation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["botRecommendationId"] = bot_recommendation_id
    try:
        resp = await client.call("DescribeBotRecommendation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bot recommendation") from exc
    return DescribeBotRecommendationResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_status=resp.get("botRecommendationStatus"),
        bot_recommendation_id=resp.get("botRecommendationId"),
        failure_reasons=resp.get("failureReasons"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        transcript_source_setting=resp.get("transcriptSourceSetting"),
        encryption_setting=resp.get("encryptionSetting"),
        bot_recommendation_results=resp.get("botRecommendationResults"),
    )


async def describe_bot_replica(
    bot_id: str,
    replica_region: str,
    region_name: str | None = None,
) -> DescribeBotReplicaResult:
    """Describe bot replica.

    Args:
        bot_id: Bot id.
        replica_region: Replica region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["replicaRegion"] = replica_region
    try:
        resp = await client.call("DescribeBotReplica", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bot replica") from exc
    return DescribeBotReplicaResult(
        bot_id=resp.get("botId"),
        replica_region=resp.get("replicaRegion"),
        source_region=resp.get("sourceRegion"),
        creation_date_time=resp.get("creationDateTime"),
        bot_replica_status=resp.get("botReplicaStatus"),
        failure_reasons=resp.get("failureReasons"),
    )


async def describe_bot_resource_generation(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    generation_id: str,
    region_name: str | None = None,
) -> DescribeBotResourceGenerationResult:
    """Describe bot resource generation.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        generation_id: Generation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["generationId"] = generation_id
    try:
        resp = await client.call("DescribeBotResourceGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bot resource generation") from exc
    return DescribeBotResourceGenerationResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        generation_id=resp.get("generationId"),
        failure_reasons=resp.get("failureReasons"),
        generation_status=resp.get("generationStatus"),
        generation_input_prompt=resp.get("generationInputPrompt"),
        generated_bot_locale_url=resp.get("generatedBotLocaleUrl"),
        creation_date_time=resp.get("creationDateTime"),
        model_arn=resp.get("modelArn"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def describe_bot_version(
    bot_id: str,
    bot_version: str,
    region_name: str | None = None,
) -> DescribeBotVersionResult:
    """Describe bot version.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    try:
        resp = await client.call("DescribeBotVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bot version") from exc
    return DescribeBotVersionResult(
        bot_id=resp.get("botId"),
        bot_name=resp.get("botName"),
        bot_version=resp.get("botVersion"),
        description=resp.get("description"),
        role_arn=resp.get("roleArn"),
        data_privacy=resp.get("dataPrivacy"),
        idle_session_ttl_in_seconds=resp.get("idleSessionTTLInSeconds"),
        bot_status=resp.get("botStatus"),
        failure_reasons=resp.get("failureReasons"),
        creation_date_time=resp.get("creationDateTime"),
        parent_bot_networks=resp.get("parentBotNetworks"),
        bot_type=resp.get("botType"),
        bot_members=resp.get("botMembers"),
    )


async def describe_custom_vocabulary_metadata(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> DescribeCustomVocabularyMetadataResult:
    """Describe custom vocabulary metadata.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("DescribeCustomVocabularyMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe custom vocabulary metadata") from exc
    return DescribeCustomVocabularyMetadataResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        custom_vocabulary_status=resp.get("customVocabularyStatus"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def describe_export(
    export_id: str,
    region_name: str | None = None,
) -> DescribeExportResult:
    """Describe export.

    Args:
        export_id: Export id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["exportId"] = export_id
    try:
        resp = await client.call("DescribeExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe export") from exc
    return DescribeExportResult(
        export_id=resp.get("exportId"),
        resource_specification=resp.get("resourceSpecification"),
        file_format=resp.get("fileFormat"),
        export_status=resp.get("exportStatus"),
        failure_reasons=resp.get("failureReasons"),
        download_url=resp.get("downloadUrl"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def describe_import(
    import_id: str,
    region_name: str | None = None,
) -> DescribeImportResult:
    """Describe import.

    Args:
        import_id: Import id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["importId"] = import_id
    try:
        resp = await client.call("DescribeImport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe import") from exc
    return DescribeImportResult(
        import_id=resp.get("importId"),
        resource_specification=resp.get("resourceSpecification"),
        imported_resource_id=resp.get("importedResourceId"),
        imported_resource_name=resp.get("importedResourceName"),
        merge_strategy=resp.get("mergeStrategy"),
        import_status=resp.get("importStatus"),
        failure_reasons=resp.get("failureReasons"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def describe_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> DescribeResourcePolicyResult:
    """Describe resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("DescribeResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe resource policy") from exc
    return DescribeResourcePolicyResult(
        resource_arn=resp.get("resourceArn"),
        policy=resp.get("policy"),
        revision_id=resp.get("revisionId"),
    )


async def describe_slot(
    slot_id: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    region_name: str | None = None,
) -> DescribeSlotResult:
    """Describe slot.

    Args:
        slot_id: Slot id.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        intent_id: Intent id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotId"] = slot_id
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["intentId"] = intent_id
    try:
        resp = await client.call("DescribeSlot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe slot") from exc
    return DescribeSlotResult(
        slot_id=resp.get("slotId"),
        slot_name=resp.get("slotName"),
        description=resp.get("description"),
        slot_type_id=resp.get("slotTypeId"),
        value_elicitation_setting=resp.get("valueElicitationSetting"),
        obfuscation_setting=resp.get("obfuscationSetting"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        intent_id=resp.get("intentId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        multiple_values_setting=resp.get("multipleValuesSetting"),
        sub_slot_setting=resp.get("subSlotSetting"),
    )


async def describe_slot_type(
    slot_type_id: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> DescribeSlotTypeResult:
    """Describe slot type.

    Args:
        slot_type_id: Slot type id.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotTypeId"] = slot_type_id
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("DescribeSlotType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe slot type") from exc
    return DescribeSlotTypeResult(
        slot_type_id=resp.get("slotTypeId"),
        slot_type_name=resp.get("slotTypeName"),
        description=resp.get("description"),
        slot_type_values=resp.get("slotTypeValues"),
        value_selection_setting=resp.get("valueSelectionSetting"),
        parent_slot_type_signature=resp.get("parentSlotTypeSignature"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        external_source_setting=resp.get("externalSourceSetting"),
        composite_slot_type_setting=resp.get("compositeSlotTypeSetting"),
    )


async def describe_test_execution(
    run_execution_id: str,
    region_name: str | None = None,
) -> DescribeTestExecutionResult:
    """Describe test execution.

    Args:
        run_execution_id: Run execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testExecutionId"] = run_execution_id
    try:
        resp = await client.call("DescribeTestExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe test execution") from exc
    return DescribeTestExecutionResult(
        run_execution_id=resp.get("testExecutionId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        run_execution_status=resp.get("testExecutionStatus"),
        run_set_id=resp.get("testSetId"),
        run_set_name=resp.get("testSetName"),
        target=resp.get("target"),
        api_mode=resp.get("apiMode"),
        run_execution_modality=resp.get("testExecutionModality"),
        failure_reasons=resp.get("failureReasons"),
    )


async def describe_test_set(
    run_set_id: str,
    region_name: str | None = None,
) -> DescribeTestSetResult:
    """Describe test set.

    Args:
        run_set_id: Run set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    try:
        resp = await client.call("DescribeTestSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe test set") from exc
    return DescribeTestSetResult(
        run_set_id=resp.get("testSetId"),
        run_set_name=resp.get("testSetName"),
        description=resp.get("description"),
        modality=resp.get("modality"),
        status=resp.get("status"),
        role_arn=resp.get("roleArn"),
        num_turns=resp.get("numTurns"),
        storage_location=resp.get("storageLocation"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def describe_test_set_discrepancy_report(
    run_set_discrepancy_report_id: str,
    region_name: str | None = None,
) -> DescribeTestSetDiscrepancyReportResult:
    """Describe test set discrepancy report.

    Args:
        run_set_discrepancy_report_id: Run set discrepancy report id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetDiscrepancyReportId"] = run_set_discrepancy_report_id
    try:
        resp = await client.call("DescribeTestSetDiscrepancyReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe test set discrepancy report") from exc
    return DescribeTestSetDiscrepancyReportResult(
        run_set_discrepancy_report_id=resp.get("testSetDiscrepancyReportId"),
        run_set_id=resp.get("testSetId"),
        creation_date_time=resp.get("creationDateTime"),
        target=resp.get("target"),
        run_set_discrepancy_report_status=resp.get("testSetDiscrepancyReportStatus"),
        last_updated_data_time=resp.get("lastUpdatedDataTime"),
        run_set_discrepancy_top_errors=resp.get("testSetDiscrepancyTopErrors"),
        run_set_discrepancy_raw_output_url=resp.get("testSetDiscrepancyRawOutputUrl"),
        failure_reasons=resp.get("failureReasons"),
    )


async def describe_test_set_generation(
    run_set_generation_id: str,
    region_name: str | None = None,
) -> DescribeTestSetGenerationResult:
    """Describe test set generation.

    Args:
        run_set_generation_id: Run set generation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetGenerationId"] = run_set_generation_id
    try:
        resp = await client.call("DescribeTestSetGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe test set generation") from exc
    return DescribeTestSetGenerationResult(
        run_set_generation_id=resp.get("testSetGenerationId"),
        run_set_generation_status=resp.get("testSetGenerationStatus"),
        failure_reasons=resp.get("failureReasons"),
        run_set_id=resp.get("testSetId"),
        run_set_name=resp.get("testSetName"),
        description=resp.get("description"),
        storage_location=resp.get("storageLocation"),
        generation_data_source=resp.get("generationDataSource"),
        role_arn=resp.get("roleArn"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def generate_bot_element(
    intent_id: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> GenerateBotElementResult:
    """Generate bot element.

    Args:
        intent_id: Intent id.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["intentId"] = intent_id
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("GenerateBotElement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate bot element") from exc
    return GenerateBotElementResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        intent_id=resp.get("intentId"),
        sample_utterances=resp.get("sampleUtterances"),
    )


async def get_test_execution_artifacts_url(
    run_execution_id: str,
    region_name: str | None = None,
) -> GetTestExecutionArtifactsUrlResult:
    """Get test execution artifacts url.

    Args:
        run_execution_id: Run execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testExecutionId"] = run_execution_id
    try:
        resp = await client.call("GetTestExecutionArtifactsUrl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get test execution artifacts url") from exc
    return GetTestExecutionArtifactsUrlResult(
        run_execution_id=resp.get("testExecutionId"),
        download_artifacts_url=resp.get("downloadArtifactsUrl"),
    )


async def list_aggregated_utterances(
    bot_id: str,
    locale_id: str,
    aggregation_duration: dict[str, Any],
    *,
    bot_alias_id: str | None = None,
    bot_version: str | None = None,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAggregatedUtterancesResult:
    """List aggregated utterances.

    Args:
        bot_id: Bot id.
        locale_id: Locale id.
        aggregation_duration: Aggregation duration.
        bot_alias_id: Bot alias id.
        bot_version: Bot version.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["localeId"] = locale_id
    kwargs["aggregationDuration"] = aggregation_duration
    if bot_alias_id is not None:
        kwargs["botAliasId"] = bot_alias_id
    if bot_version is not None:
        kwargs["botVersion"] = bot_version
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAggregatedUtterances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list aggregated utterances") from exc
    return ListAggregatedUtterancesResult(
        bot_id=resp.get("botId"),
        bot_alias_id=resp.get("botAliasId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        aggregation_duration=resp.get("aggregationDuration"),
        aggregation_window_start_time=resp.get("aggregationWindowStartTime"),
        aggregation_window_end_time=resp.get("aggregationWindowEndTime"),
        aggregation_last_refreshed_date_time=resp.get("aggregationLastRefreshedDateTime"),
        aggregated_utterances_summaries=resp.get("aggregatedUtterancesSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bot_alias_replicas(
    bot_id: str,
    replica_region: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotAliasReplicasResult:
    """List bot alias replicas.

    Args:
        bot_id: Bot id.
        replica_region: Replica region.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["replicaRegion"] = replica_region
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotAliasReplicas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot alias replicas") from exc
    return ListBotAliasReplicasResult(
        bot_id=resp.get("botId"),
        source_region=resp.get("sourceRegion"),
        replica_region=resp.get("replicaRegion"),
        bot_alias_replica_summaries=resp.get("botAliasReplicaSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bot_aliases(
    bot_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotAliasesResult:
    """List bot aliases.

    Args:
        bot_id: Bot id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot aliases") from exc
    return ListBotAliasesResult(
        bot_alias_summaries=resp.get("botAliasSummaries"),
        next_token=resp.get("nextToken"),
        bot_id=resp.get("botId"),
    )


async def list_bot_locales(
    bot_id: str,
    bot_version: str,
    *,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotLocalesResult:
    """List bot locales.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotLocales", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot locales") from exc
    return ListBotLocalesResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        next_token=resp.get("nextToken"),
        bot_locale_summaries=resp.get("botLocaleSummaries"),
    )


async def list_bot_recommendations(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotRecommendationsResult:
    """List bot recommendations.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot recommendations") from exc
    return ListBotRecommendationsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_summaries=resp.get("botRecommendationSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bot_replicas(
    bot_id: str,
    region_name: str | None = None,
) -> ListBotReplicasResult:
    """List bot replicas.

    Args:
        bot_id: Bot id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    try:
        resp = await client.call("ListBotReplicas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot replicas") from exc
    return ListBotReplicasResult(
        bot_id=resp.get("botId"),
        source_region=resp.get("sourceRegion"),
        bot_replica_summaries=resp.get("botReplicaSummaries"),
    )


async def list_bot_resource_generations(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotResourceGenerationsResult:
    """List bot resource generations.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotResourceGenerations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot resource generations") from exc
    return ListBotResourceGenerationsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        generation_summaries=resp.get("generationSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bot_version_replicas(
    bot_id: str,
    replica_region: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListBotVersionReplicasResult:
    """List bot version replicas.

    Args:
        bot_id: Bot id.
        replica_region: Replica region.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["replicaRegion"] = replica_region
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    try:
        resp = await client.call("ListBotVersionReplicas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot version replicas") from exc
    return ListBotVersionReplicasResult(
        bot_id=resp.get("botId"),
        source_region=resp.get("sourceRegion"),
        replica_region=resp.get("replicaRegion"),
        bot_version_replica_summaries=resp.get("botVersionReplicaSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bot_versions(
    bot_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBotVersionsResult:
    """List bot versions.

    Args:
        bot_id: Bot id.
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBotVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bot versions") from exc
    return ListBotVersionsResult(
        bot_id=resp.get("botId"),
        bot_version_summaries=resp.get("botVersionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_built_in_intents(
    locale_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBuiltInIntentsResult:
    """List built in intents.

    Args:
        locale_id: Locale id.
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["localeId"] = locale_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBuiltInIntents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list built in intents") from exc
    return ListBuiltInIntentsResult(
        built_in_intent_summaries=resp.get("builtInIntentSummaries"),
        next_token=resp.get("nextToken"),
        locale_id=resp.get("localeId"),
    )


async def list_built_in_slot_types(
    locale_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBuiltInSlotTypesResult:
    """List built in slot types.

    Args:
        locale_id: Locale id.
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["localeId"] = locale_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListBuiltInSlotTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list built in slot types") from exc
    return ListBuiltInSlotTypesResult(
        built_in_slot_type_summaries=resp.get("builtInSlotTypeSummaries"),
        next_token=resp.get("nextToken"),
        locale_id=resp.get("localeId"),
    )


async def list_custom_vocabulary_items(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCustomVocabularyItemsResult:
    """List custom vocabulary items.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListCustomVocabularyItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom vocabulary items") from exc
    return ListCustomVocabularyItemsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        custom_vocabulary_items=resp.get("customVocabularyItems"),
        next_token=resp.get("nextToken"),
    )


async def list_exports(
    *,
    bot_id: str | None = None,
    bot_version: str | None = None,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    locale_id: str | None = None,
    region_name: str | None = None,
) -> ListExportsResult:
    """List exports.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    if bot_id is not None:
        kwargs["botId"] = bot_id
    if bot_version is not None:
        kwargs["botVersion"] = bot_version
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if locale_id is not None:
        kwargs["localeId"] = locale_id
    try:
        resp = await client.call("ListExports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list exports") from exc
    return ListExportsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        export_summaries=resp.get("exportSummaries"),
        next_token=resp.get("nextToken"),
        locale_id=resp.get("localeId"),
    )


async def list_imports(
    *,
    bot_id: str | None = None,
    bot_version: str | None = None,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    locale_id: str | None = None,
    region_name: str | None = None,
) -> ListImportsResult:
    """List imports.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    if bot_id is not None:
        kwargs["botId"] = bot_id
    if bot_version is not None:
        kwargs["botVersion"] = bot_version
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if locale_id is not None:
        kwargs["localeId"] = locale_id
    try:
        resp = await client.call("ListImports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list imports") from exc
    return ListImportsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        import_summaries=resp.get("importSummaries"),
        next_token=resp.get("nextToken"),
        locale_id=resp.get("localeId"),
    )


async def list_intent_metrics(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    metrics: list[dict[str, Any]],
    *,
    bin_by: list[dict[str, Any]] | None = None,
    group_by: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIntentMetricsResult:
    """List intent metrics.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        metrics: Metrics.
        bin_by: Bin by.
        group_by: Group by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    kwargs["metrics"] = metrics
    if bin_by is not None:
        kwargs["binBy"] = bin_by
    if group_by is not None:
        kwargs["groupBy"] = group_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListIntentMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list intent metrics") from exc
    return ListIntentMetricsResult(
        bot_id=resp.get("botId"),
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


async def list_intent_paths(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    intent_path: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListIntentPathsResult:
    """List intent paths.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        intent_path: Intent path.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    kwargs["intentPath"] = intent_path
    if filters is not None:
        kwargs["filters"] = filters
    try:
        resp = await client.call("ListIntentPaths", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list intent paths") from exc
    return ListIntentPathsResult(
        node_summaries=resp.get("nodeSummaries"),
    )


async def list_intent_stage_metrics(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    metrics: list[dict[str, Any]],
    *,
    bin_by: list[dict[str, Any]] | None = None,
    group_by: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIntentStageMetricsResult:
    """List intent stage metrics.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        metrics: Metrics.
        bin_by: Bin by.
        group_by: Group by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    kwargs["metrics"] = metrics
    if bin_by is not None:
        kwargs["binBy"] = bin_by
    if group_by is not None:
        kwargs["groupBy"] = group_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListIntentStageMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list intent stage metrics") from exc
    return ListIntentStageMetricsResult(
        bot_id=resp.get("botId"),
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


async def list_recommended_intents(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    bot_recommendation_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRecommendedIntentsResult:
    """List recommended intents.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        bot_recommendation_id: Bot recommendation id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["botRecommendationId"] = bot_recommendation_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListRecommendedIntents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recommended intents") from exc
    return ListRecommendedIntentsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_id=resp.get("botRecommendationId"),
        summary_list=resp.get("summaryList"),
        next_token=resp.get("nextToken"),
    )


async def list_session_analytics_data(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    *,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSessionAnalyticsDataResult:
    """List session analytics data.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSessionAnalyticsData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list session analytics data") from exc
    return ListSessionAnalyticsDataResult(
        bot_id=resp.get("botId"),
        next_token=resp.get("nextToken"),
        sessions=resp.get("sessions"),
    )


async def list_session_metrics(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    metrics: list[dict[str, Any]],
    *,
    bin_by: list[dict[str, Any]] | None = None,
    group_by: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSessionMetricsResult:
    """List session metrics.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        metrics: Metrics.
        bin_by: Bin by.
        group_by: Group by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    kwargs["metrics"] = metrics
    if bin_by is not None:
        kwargs["binBy"] = bin_by
    if group_by is not None:
        kwargs["groupBy"] = group_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSessionMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list session metrics") from exc
    return ListSessionMetricsResult(
        bot_id=resp.get("botId"),
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


async def list_slot_types(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSlotTypesResult:
    """List slot types.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSlotTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list slot types") from exc
    return ListSlotTypesResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        slot_type_summaries=resp.get("slotTypeSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_slots(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    *,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSlotsResult:
    """List slots.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        intent_id: Intent id.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["intentId"] = intent_id
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSlots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list slots") from exc
    return ListSlotsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        intent_id=resp.get("intentId"),
        slot_summaries=resp.get("slotSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def list_test_execution_result_items(
    run_execution_id: str,
    result_filter_by: dict[str, Any],
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTestExecutionResultItemsResult:
    """List test execution result items.

    Args:
        run_execution_id: Run execution id.
        result_filter_by: Result filter by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testExecutionId"] = run_execution_id
    kwargs["resultFilterBy"] = result_filter_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTestExecutionResultItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list test execution result items") from exc
    return ListTestExecutionResultItemsResult(
        run_execution_results=resp.get("testExecutionResults"),
        next_token=resp.get("nextToken"),
    )


async def list_test_executions(
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTestExecutionsResult:
    """List test executions.

    Args:
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTestExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list test executions") from exc
    return ListTestExecutionsResult(
        run_executions=resp.get("testExecutions"),
        next_token=resp.get("nextToken"),
    )


async def list_test_set_records(
    run_set_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTestSetRecordsResult:
    """List test set records.

    Args:
        run_set_id: Run set id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTestSetRecords", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list test set records") from exc
    return ListTestSetRecordsResult(
        run_set_records=resp.get("testSetRecords"),
        next_token=resp.get("nextToken"),
    )


async def list_test_sets(
    *,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTestSetsResult:
    """List test sets.

    Args:
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTestSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list test sets") from exc
    return ListTestSetsResult(
        run_sets=resp.get("testSets"),
        next_token=resp.get("nextToken"),
    )


async def list_utterance_analytics_data(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    *,
    sort_by: dict[str, Any] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListUtteranceAnalyticsDataResult:
    """List utterance analytics data.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        sort_by: Sort by.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListUtteranceAnalyticsData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list utterance analytics data") from exc
    return ListUtteranceAnalyticsDataResult(
        bot_id=resp.get("botId"),
        next_token=resp.get("nextToken"),
        utterances=resp.get("utterances"),
    )


async def list_utterance_metrics(
    bot_id: str,
    start_date_time: str,
    end_date_time: str,
    metrics: list[dict[str, Any]],
    *,
    bin_by: list[dict[str, Any]] | None = None,
    group_by: list[dict[str, Any]] | None = None,
    attributes: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListUtteranceMetricsResult:
    """List utterance metrics.

    Args:
        bot_id: Bot id.
        start_date_time: Start date time.
        end_date_time: End date time.
        metrics: Metrics.
        bin_by: Bin by.
        group_by: Group by.
        attributes: Attributes.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["startDateTime"] = start_date_time
    kwargs["endDateTime"] = end_date_time
    kwargs["metrics"] = metrics
    if bin_by is not None:
        kwargs["binBy"] = bin_by
    if group_by is not None:
        kwargs["groupBy"] = group_by
    if attributes is not None:
        kwargs["attributes"] = attributes
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListUtteranceMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list utterance metrics") from exc
    return ListUtteranceMetricsResult(
        bot_id=resp.get("botId"),
        results=resp.get("results"),
        next_token=resp.get("nextToken"),
    )


async def search_associated_transcripts(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    bot_recommendation_id: str,
    filters: list[dict[str, Any]],
    *,
    search_order: str | None = None,
    max_results: int | None = None,
    next_index: int | None = None,
    region_name: str | None = None,
) -> SearchAssociatedTranscriptsResult:
    """Search associated transcripts.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        bot_recommendation_id: Bot recommendation id.
        filters: Filters.
        search_order: Search order.
        max_results: Max results.
        next_index: Next index.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["botRecommendationId"] = bot_recommendation_id
    kwargs["filters"] = filters
    if search_order is not None:
        kwargs["searchOrder"] = search_order
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_index is not None:
        kwargs["nextIndex"] = next_index
    try:
        resp = await client.call("SearchAssociatedTranscripts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search associated transcripts") from exc
    return SearchAssociatedTranscriptsResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_id=resp.get("botRecommendationId"),
        next_index=resp.get("nextIndex"),
        associated_transcripts=resp.get("associatedTranscripts"),
        total_results=resp.get("totalResults"),
    )


async def start_bot_recommendation(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    transcript_source_setting: dict[str, Any],
    *,
    encryption_setting: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartBotRecommendationResult:
    """Start bot recommendation.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        transcript_source_setting: Transcript source setting.
        encryption_setting: Encryption setting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["transcriptSourceSetting"] = transcript_source_setting
    if encryption_setting is not None:
        kwargs["encryptionSetting"] = encryption_setting
    try:
        resp = await client.call("StartBotRecommendation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start bot recommendation") from exc
    return StartBotRecommendationResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_status=resp.get("botRecommendationStatus"),
        bot_recommendation_id=resp.get("botRecommendationId"),
        creation_date_time=resp.get("creationDateTime"),
        transcript_source_setting=resp.get("transcriptSourceSetting"),
        encryption_setting=resp.get("encryptionSetting"),
    )


async def start_bot_resource_generation(
    generation_input_prompt: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    region_name: str | None = None,
) -> StartBotResourceGenerationResult:
    """Start bot resource generation.

    Args:
        generation_input_prompt: Generation input prompt.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["generationInputPrompt"] = generation_input_prompt
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    try:
        resp = await client.call("StartBotResourceGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start bot resource generation") from exc
    return StartBotResourceGenerationResult(
        generation_input_prompt=resp.get("generationInputPrompt"),
        generation_id=resp.get("generationId"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        generation_status=resp.get("generationStatus"),
        creation_date_time=resp.get("creationDateTime"),
    )


async def start_import(
    import_id: str,
    resource_specification: dict[str, Any],
    merge_strategy: str,
    *,
    file_password: str | None = None,
    region_name: str | None = None,
) -> StartImportResult:
    """Start import.

    Args:
        import_id: Import id.
        resource_specification: Resource specification.
        merge_strategy: Merge strategy.
        file_password: File password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["importId"] = import_id
    kwargs["resourceSpecification"] = resource_specification
    kwargs["mergeStrategy"] = merge_strategy
    if file_password is not None:
        kwargs["filePassword"] = file_password
    try:
        resp = await client.call("StartImport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start import") from exc
    return StartImportResult(
        import_id=resp.get("importId"),
        resource_specification=resp.get("resourceSpecification"),
        merge_strategy=resp.get("mergeStrategy"),
        import_status=resp.get("importStatus"),
        creation_date_time=resp.get("creationDateTime"),
    )


async def start_test_execution(
    run_set_id: str,
    target: dict[str, Any],
    api_mode: str,
    *,
    run_execution_modality: str | None = None,
    region_name: str | None = None,
) -> StartTestExecutionResult:
    """Start test execution.

    Args:
        run_set_id: Run set id.
        target: Target.
        api_mode: Api mode.
        run_execution_modality: Run execution modality.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    kwargs["target"] = target
    kwargs["apiMode"] = api_mode
    if run_execution_modality is not None:
        kwargs["testExecutionModality"] = run_execution_modality
    try:
        resp = await client.call("StartTestExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start test execution") from exc
    return StartTestExecutionResult(
        run_execution_id=resp.get("testExecutionId"),
        creation_date_time=resp.get("creationDateTime"),
        run_set_id=resp.get("testSetId"),
        target=resp.get("target"),
        api_mode=resp.get("apiMode"),
        run_execution_modality=resp.get("testExecutionModality"),
    )


async def start_test_set_generation(
    run_set_name: str,
    storage_location: dict[str, Any],
    generation_data_source: dict[str, Any],
    role_arn: str,
    *,
    description: str | None = None,
    run_set_tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartTestSetGenerationResult:
    """Start test set generation.

    Args:
        run_set_name: Run set name.
        storage_location: Storage location.
        generation_data_source: Generation data source.
        role_arn: Role arn.
        description: Description.
        run_set_tags: Run set tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetName"] = run_set_name
    kwargs["storageLocation"] = storage_location
    kwargs["generationDataSource"] = generation_data_source
    kwargs["roleArn"] = role_arn
    if description is not None:
        kwargs["description"] = description
    if run_set_tags is not None:
        kwargs["testSetTags"] = run_set_tags
    try:
        resp = await client.call("StartTestSetGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start test set generation") from exc
    return StartTestSetGenerationResult(
        run_set_generation_id=resp.get("testSetGenerationId"),
        creation_date_time=resp.get("creationDateTime"),
        run_set_generation_status=resp.get("testSetGenerationStatus"),
        run_set_name=resp.get("testSetName"),
        description=resp.get("description"),
        storage_location=resp.get("storageLocation"),
        generation_data_source=resp.get("generationDataSource"),
        role_arn=resp.get("roleArn"),
        run_set_tags=resp.get("testSetTags"),
    )


async def stop_bot_recommendation(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    bot_recommendation_id: str,
    region_name: str | None = None,
) -> StopBotRecommendationResult:
    """Stop bot recommendation.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        bot_recommendation_id: Bot recommendation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["botRecommendationId"] = bot_recommendation_id
    try:
        resp = await client.call("StopBotRecommendation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop bot recommendation") from exc
    return StopBotRecommendationResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_status=resp.get("botRecommendationStatus"),
        bot_recommendation_id=resp.get("botRecommendationId"),
    )


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceARN"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_bot(
    bot_id: str,
    bot_name: str,
    role_arn: str,
    data_privacy: dict[str, Any],
    idle_session_ttl_in_seconds: int,
    *,
    description: str | None = None,
    bot_type: str | None = None,
    bot_members: list[dict[str, Any]] | None = None,
    error_log_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateBotResult:
    """Update bot.

    Args:
        bot_id: Bot id.
        bot_name: Bot name.
        role_arn: Role arn.
        data_privacy: Data privacy.
        idle_session_ttl_in_seconds: Idle session ttl in seconds.
        description: Description.
        bot_type: Bot type.
        bot_members: Bot members.
        error_log_settings: Error log settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botName"] = bot_name
    kwargs["roleArn"] = role_arn
    kwargs["dataPrivacy"] = data_privacy
    kwargs["idleSessionTTLInSeconds"] = idle_session_ttl_in_seconds
    if description is not None:
        kwargs["description"] = description
    if bot_type is not None:
        kwargs["botType"] = bot_type
    if bot_members is not None:
        kwargs["botMembers"] = bot_members
    if error_log_settings is not None:
        kwargs["errorLogSettings"] = error_log_settings
    try:
        resp = await client.call("UpdateBot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bot") from exc
    return UpdateBotResult(
        bot_id=resp.get("botId"),
        bot_name=resp.get("botName"),
        description=resp.get("description"),
        role_arn=resp.get("roleArn"),
        data_privacy=resp.get("dataPrivacy"),
        idle_session_ttl_in_seconds=resp.get("idleSessionTTLInSeconds"),
        bot_status=resp.get("botStatus"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        bot_type=resp.get("botType"),
        bot_members=resp.get("botMembers"),
        error_log_settings=resp.get("errorLogSettings"),
    )


async def update_bot_alias(
    bot_alias_id: str,
    bot_alias_name: str,
    bot_id: str,
    *,
    description: str | None = None,
    bot_version: str | None = None,
    bot_alias_locale_settings: dict[str, Any] | None = None,
    conversation_log_settings: dict[str, Any] | None = None,
    sentiment_analysis_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateBotAliasResult:
    """Update bot alias.

    Args:
        bot_alias_id: Bot alias id.
        bot_alias_name: Bot alias name.
        bot_id: Bot id.
        description: Description.
        bot_version: Bot version.
        bot_alias_locale_settings: Bot alias locale settings.
        conversation_log_settings: Conversation log settings.
        sentiment_analysis_settings: Sentiment analysis settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botAliasId"] = bot_alias_id
    kwargs["botAliasName"] = bot_alias_name
    kwargs["botId"] = bot_id
    if description is not None:
        kwargs["description"] = description
    if bot_version is not None:
        kwargs["botVersion"] = bot_version
    if bot_alias_locale_settings is not None:
        kwargs["botAliasLocaleSettings"] = bot_alias_locale_settings
    if conversation_log_settings is not None:
        kwargs["conversationLogSettings"] = conversation_log_settings
    if sentiment_analysis_settings is not None:
        kwargs["sentimentAnalysisSettings"] = sentiment_analysis_settings
    try:
        resp = await client.call("UpdateBotAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bot alias") from exc
    return UpdateBotAliasResult(
        bot_alias_id=resp.get("botAliasId"),
        bot_alias_name=resp.get("botAliasName"),
        description=resp.get("description"),
        bot_version=resp.get("botVersion"),
        bot_alias_locale_settings=resp.get("botAliasLocaleSettings"),
        conversation_log_settings=resp.get("conversationLogSettings"),
        sentiment_analysis_settings=resp.get("sentimentAnalysisSettings"),
        bot_alias_status=resp.get("botAliasStatus"),
        bot_id=resp.get("botId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def update_bot_locale(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    nlu_intent_confidence_threshold: float,
    *,
    description: str | None = None,
    voice_settings: dict[str, Any] | None = None,
    generative_ai_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateBotLocaleResult:
    """Update bot locale.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        nlu_intent_confidence_threshold: Nlu intent confidence threshold.
        description: Description.
        voice_settings: Voice settings.
        generative_ai_settings: Generative ai settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["nluIntentConfidenceThreshold"] = nlu_intent_confidence_threshold
    if description is not None:
        kwargs["description"] = description
    if voice_settings is not None:
        kwargs["voiceSettings"] = voice_settings
    if generative_ai_settings is not None:
        kwargs["generativeAISettings"] = generative_ai_settings
    try:
        resp = await client.call("UpdateBotLocale", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bot locale") from exc
    return UpdateBotLocaleResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        locale_name=resp.get("localeName"),
        description=resp.get("description"),
        nlu_intent_confidence_threshold=resp.get("nluIntentConfidenceThreshold"),
        voice_settings=resp.get("voiceSettings"),
        bot_locale_status=resp.get("botLocaleStatus"),
        failure_reasons=resp.get("failureReasons"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        recommended_actions=resp.get("recommendedActions"),
        generative_ai_settings=resp.get("generativeAISettings"),
    )


async def update_bot_recommendation(
    bot_id: str,
    bot_version: str,
    locale_id: str,
    bot_recommendation_id: str,
    encryption_setting: dict[str, Any],
    region_name: str | None = None,
) -> UpdateBotRecommendationResult:
    """Update bot recommendation.

    Args:
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        bot_recommendation_id: Bot recommendation id.
        encryption_setting: Encryption setting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["botRecommendationId"] = bot_recommendation_id
    kwargs["encryptionSetting"] = encryption_setting
    try:
        resp = await client.call("UpdateBotRecommendation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bot recommendation") from exc
    return UpdateBotRecommendationResult(
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        bot_recommendation_status=resp.get("botRecommendationStatus"),
        bot_recommendation_id=resp.get("botRecommendationId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        transcript_source_setting=resp.get("transcriptSourceSetting"),
        encryption_setting=resp.get("encryptionSetting"),
    )


async def update_export(
    export_id: str,
    *,
    file_password: str | None = None,
    region_name: str | None = None,
) -> UpdateExportResult:
    """Update export.

    Args:
        export_id: Export id.
        file_password: File password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["exportId"] = export_id
    if file_password is not None:
        kwargs["filePassword"] = file_password
    try:
        resp = await client.call("UpdateExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update export") from exc
    return UpdateExportResult(
        export_id=resp.get("exportId"),
        resource_specification=resp.get("resourceSpecification"),
        file_format=resp.get("fileFormat"),
        export_status=resp.get("exportStatus"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )


async def update_intent(
    intent_id: str,
    intent_name: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    description: str | None = None,
    parent_intent_signature: str | None = None,
    sample_utterances: list[dict[str, Any]] | None = None,
    dialog_code_hook: dict[str, Any] | None = None,
    fulfillment_code_hook: dict[str, Any] | None = None,
    slot_priorities: list[dict[str, Any]] | None = None,
    intent_confirmation_setting: dict[str, Any] | None = None,
    intent_closing_setting: dict[str, Any] | None = None,
    input_contexts: list[dict[str, Any]] | None = None,
    output_contexts: list[dict[str, Any]] | None = None,
    kendra_configuration: dict[str, Any] | None = None,
    initial_response_setting: dict[str, Any] | None = None,
    qn_a_intent_configuration: dict[str, Any] | None = None,
    q_in_connect_intent_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateIntentResult:
    """Update intent.

    Args:
        intent_id: Intent id.
        intent_name: Intent name.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        description: Description.
        parent_intent_signature: Parent intent signature.
        sample_utterances: Sample utterances.
        dialog_code_hook: Dialog code hook.
        fulfillment_code_hook: Fulfillment code hook.
        slot_priorities: Slot priorities.
        intent_confirmation_setting: Intent confirmation setting.
        intent_closing_setting: Intent closing setting.
        input_contexts: Input contexts.
        output_contexts: Output contexts.
        kendra_configuration: Kendra configuration.
        initial_response_setting: Initial response setting.
        qn_a_intent_configuration: Qn a intent configuration.
        q_in_connect_intent_configuration: Q in connect intent configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["intentId"] = intent_id
    kwargs["intentName"] = intent_name
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if description is not None:
        kwargs["description"] = description
    if parent_intent_signature is not None:
        kwargs["parentIntentSignature"] = parent_intent_signature
    if sample_utterances is not None:
        kwargs["sampleUtterances"] = sample_utterances
    if dialog_code_hook is not None:
        kwargs["dialogCodeHook"] = dialog_code_hook
    if fulfillment_code_hook is not None:
        kwargs["fulfillmentCodeHook"] = fulfillment_code_hook
    if slot_priorities is not None:
        kwargs["slotPriorities"] = slot_priorities
    if intent_confirmation_setting is not None:
        kwargs["intentConfirmationSetting"] = intent_confirmation_setting
    if intent_closing_setting is not None:
        kwargs["intentClosingSetting"] = intent_closing_setting
    if input_contexts is not None:
        kwargs["inputContexts"] = input_contexts
    if output_contexts is not None:
        kwargs["outputContexts"] = output_contexts
    if kendra_configuration is not None:
        kwargs["kendraConfiguration"] = kendra_configuration
    if initial_response_setting is not None:
        kwargs["initialResponseSetting"] = initial_response_setting
    if qn_a_intent_configuration is not None:
        kwargs["qnAIntentConfiguration"] = qn_a_intent_configuration
    if q_in_connect_intent_configuration is not None:
        kwargs["qInConnectIntentConfiguration"] = q_in_connect_intent_configuration
    try:
        resp = await client.call("UpdateIntent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update intent") from exc
    return UpdateIntentResult(
        intent_id=resp.get("intentId"),
        intent_name=resp.get("intentName"),
        description=resp.get("description"),
        parent_intent_signature=resp.get("parentIntentSignature"),
        sample_utterances=resp.get("sampleUtterances"),
        dialog_code_hook=resp.get("dialogCodeHook"),
        fulfillment_code_hook=resp.get("fulfillmentCodeHook"),
        slot_priorities=resp.get("slotPriorities"),
        intent_confirmation_setting=resp.get("intentConfirmationSetting"),
        intent_closing_setting=resp.get("intentClosingSetting"),
        input_contexts=resp.get("inputContexts"),
        output_contexts=resp.get("outputContexts"),
        kendra_configuration=resp.get("kendraConfiguration"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        initial_response_setting=resp.get("initialResponseSetting"),
        qn_a_intent_configuration=resp.get("qnAIntentConfiguration"),
        q_in_connect_intent_configuration=resp.get("qInConnectIntentConfiguration"),
    )


async def update_resource_policy(
    resource_arn: str,
    policy: str,
    *,
    expected_revision_id: str | None = None,
    region_name: str | None = None,
) -> UpdateResourcePolicyResult:
    """Update resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        expected_revision_id: Expected revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["policy"] = policy
    if expected_revision_id is not None:
        kwargs["expectedRevisionId"] = expected_revision_id
    try:
        resp = await client.call("UpdateResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update resource policy") from exc
    return UpdateResourcePolicyResult(
        resource_arn=resp.get("resourceArn"),
        revision_id=resp.get("revisionId"),
    )


async def update_slot(
    slot_id: str,
    slot_name: str,
    value_elicitation_setting: dict[str, Any],
    bot_id: str,
    bot_version: str,
    locale_id: str,
    intent_id: str,
    *,
    description: str | None = None,
    slot_type_id: str | None = None,
    obfuscation_setting: dict[str, Any] | None = None,
    multiple_values_setting: dict[str, Any] | None = None,
    sub_slot_setting: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateSlotResult:
    """Update slot.

    Args:
        slot_id: Slot id.
        slot_name: Slot name.
        value_elicitation_setting: Value elicitation setting.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        intent_id: Intent id.
        description: Description.
        slot_type_id: Slot type id.
        obfuscation_setting: Obfuscation setting.
        multiple_values_setting: Multiple values setting.
        sub_slot_setting: Sub slot setting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotId"] = slot_id
    kwargs["slotName"] = slot_name
    kwargs["valueElicitationSetting"] = value_elicitation_setting
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    kwargs["intentId"] = intent_id
    if description is not None:
        kwargs["description"] = description
    if slot_type_id is not None:
        kwargs["slotTypeId"] = slot_type_id
    if obfuscation_setting is not None:
        kwargs["obfuscationSetting"] = obfuscation_setting
    if multiple_values_setting is not None:
        kwargs["multipleValuesSetting"] = multiple_values_setting
    if sub_slot_setting is not None:
        kwargs["subSlotSetting"] = sub_slot_setting
    try:
        resp = await client.call("UpdateSlot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update slot") from exc
    return UpdateSlotResult(
        slot_id=resp.get("slotId"),
        slot_name=resp.get("slotName"),
        description=resp.get("description"),
        slot_type_id=resp.get("slotTypeId"),
        value_elicitation_setting=resp.get("valueElicitationSetting"),
        obfuscation_setting=resp.get("obfuscationSetting"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        intent_id=resp.get("intentId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        multiple_values_setting=resp.get("multipleValuesSetting"),
        sub_slot_setting=resp.get("subSlotSetting"),
    )


async def update_slot_type(
    slot_type_id: str,
    slot_type_name: str,
    bot_id: str,
    bot_version: str,
    locale_id: str,
    *,
    description: str | None = None,
    slot_type_values: list[dict[str, Any]] | None = None,
    value_selection_setting: dict[str, Any] | None = None,
    parent_slot_type_signature: str | None = None,
    external_source_setting: dict[str, Any] | None = None,
    composite_slot_type_setting: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateSlotTypeResult:
    """Update slot type.

    Args:
        slot_type_id: Slot type id.
        slot_type_name: Slot type name.
        bot_id: Bot id.
        bot_version: Bot version.
        locale_id: Locale id.
        description: Description.
        slot_type_values: Slot type values.
        value_selection_setting: Value selection setting.
        parent_slot_type_signature: Parent slot type signature.
        external_source_setting: External source setting.
        composite_slot_type_setting: Composite slot type setting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["slotTypeId"] = slot_type_id
    kwargs["slotTypeName"] = slot_type_name
    kwargs["botId"] = bot_id
    kwargs["botVersion"] = bot_version
    kwargs["localeId"] = locale_id
    if description is not None:
        kwargs["description"] = description
    if slot_type_values is not None:
        kwargs["slotTypeValues"] = slot_type_values
    if value_selection_setting is not None:
        kwargs["valueSelectionSetting"] = value_selection_setting
    if parent_slot_type_signature is not None:
        kwargs["parentSlotTypeSignature"] = parent_slot_type_signature
    if external_source_setting is not None:
        kwargs["externalSourceSetting"] = external_source_setting
    if composite_slot_type_setting is not None:
        kwargs["compositeSlotTypeSetting"] = composite_slot_type_setting
    try:
        resp = await client.call("UpdateSlotType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update slot type") from exc
    return UpdateSlotTypeResult(
        slot_type_id=resp.get("slotTypeId"),
        slot_type_name=resp.get("slotTypeName"),
        description=resp.get("description"),
        slot_type_values=resp.get("slotTypeValues"),
        value_selection_setting=resp.get("valueSelectionSetting"),
        parent_slot_type_signature=resp.get("parentSlotTypeSignature"),
        bot_id=resp.get("botId"),
        bot_version=resp.get("botVersion"),
        locale_id=resp.get("localeId"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
        external_source_setting=resp.get("externalSourceSetting"),
        composite_slot_type_setting=resp.get("compositeSlotTypeSetting"),
    )


async def update_test_set(
    run_set_id: str,
    run_set_name: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateTestSetResult:
    """Update test set.

    Args:
        run_set_id: Run set id.
        run_set_name: Run set name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lexv2-models", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["testSetId"] = run_set_id
    kwargs["testSetName"] = run_set_name
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("UpdateTestSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update test set") from exc
    return UpdateTestSetResult(
        run_set_id=resp.get("testSetId"),
        run_set_name=resp.get("testSetName"),
        description=resp.get("description"),
        modality=resp.get("modality"),
        status=resp.get("status"),
        role_arn=resp.get("roleArn"),
        num_turns=resp.get("numTurns"),
        storage_location=resp.get("storageLocation"),
        creation_date_time=resp.get("creationDateTime"),
        last_updated_date_time=resp.get("lastUpdatedDateTime"),
    )
