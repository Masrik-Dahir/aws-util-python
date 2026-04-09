"""Tests for aws_util.aio.lex_models -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.lex_models import (
    BotLocaleInfo,
    BotSummary,
    IntentSummary,
    build_bot_locale,
    create_bot,
    create_intent,
    create_slot_type,
    delete_bot,
    delete_intent,
    describe_bot,
    describe_bot_locale,
    describe_intent,
    list_bots,
    list_intents,
    wait_for_bot_locale,
    batch_create_custom_vocabulary_item,
    batch_delete_custom_vocabulary_item,
    batch_update_custom_vocabulary_item,
    create_bot_alias,
    create_bot_locale,
    create_bot_replica,
    create_bot_version,
    create_export,
    create_resource_policy,
    create_resource_policy_statement,
    create_slot,
    create_test_set_discrepancy_report,
    create_upload_url,
    delete_bot_alias,
    delete_bot_locale,
    delete_bot_replica,
    delete_bot_version,
    delete_custom_vocabulary,
    delete_export,
    delete_import,
    delete_resource_policy,
    delete_resource_policy_statement,
    delete_slot,
    delete_slot_type,
    delete_test_set,
    delete_utterances,
    describe_bot_alias,
    describe_bot_recommendation,
    describe_bot_replica,
    describe_bot_resource_generation,
    describe_bot_version,
    describe_custom_vocabulary_metadata,
    describe_export,
    describe_import,
    describe_resource_policy,
    describe_slot,
    describe_slot_type,
    describe_test_execution,
    describe_test_set,
    describe_test_set_discrepancy_report,
    describe_test_set_generation,
    generate_bot_element,
    get_test_execution_artifacts_url,
    list_aggregated_utterances,
    list_bot_alias_replicas,
    list_bot_aliases,
    list_bot_locales,
    list_bot_recommendations,
    list_bot_replicas,
    list_bot_resource_generations,
    list_bot_version_replicas,
    list_bot_versions,
    list_built_in_intents,
    list_built_in_slot_types,
    list_custom_vocabulary_items,
    list_exports,
    list_imports,
    list_intent_metrics,
    list_intent_paths,
    list_intent_stage_metrics,
    list_recommended_intents,
    list_session_analytics_data,
    list_session_metrics,
    list_slot_types,
    list_slots,
    list_tags_for_resource,
    list_test_execution_result_items,
    list_test_executions,
    list_test_set_records,
    list_test_sets,
    list_utterance_analytics_data,
    list_utterance_metrics,
    search_associated_transcripts,
    start_bot_recommendation,
    start_bot_resource_generation,
    start_import,
    start_test_execution,
    start_test_set_generation,
    stop_bot_recommendation,
    tag_resource,
    untag_resource,
    update_bot,
    update_bot_alias,
    update_bot_locale,
    update_bot_recommendation,
    update_export,
    update_intent,
    update_resource_policy,
    update_slot,
    update_slot_type,
    update_test_set,
)
from aws_util.exceptions import AwsServiceError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# create_bot
# ---------------------------------------------------------------------------


async def test_create_bot_ok(monkeypatch):
    mc = _mc({"botId": "b1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_bot("mybot", "arn:role")
    assert r["botId"] == "b1"


async def test_create_bot_with_description(monkeypatch):
    mc = _mc({"botId": "b1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_bot("mybot", "arn:role", description="desc")
    assert r["botId"] == "b1"


async def test_create_bot_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await create_bot("mybot", "arn:role")


async def test_create_bot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_bot failed"):
        await create_bot("mybot", "arn:role")


# ---------------------------------------------------------------------------
# describe_bot
# ---------------------------------------------------------------------------


async def test_describe_bot_ok(monkeypatch):
    mc = _mc({"botId": "b1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await describe_bot("b1")
    assert r["botId"] == "b1"


async def test_describe_bot_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_bot failed"):
        await describe_bot("b1")


# ---------------------------------------------------------------------------
# list_bots
# ---------------------------------------------------------------------------


async def test_list_bots_ok(monkeypatch):
    mc = _mc({
        "botSummaries": [
            {"botId": "b1", "botName": "mybot", "botStatus": "Available"},
        ],
    })
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await list_bots()
    assert len(r) == 1
    assert r[0].bot_id == "b1"


async def test_list_bots_empty(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    assert await list_bots() == []


async def test_list_bots_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_bots failed"):
        await list_bots()


# ---------------------------------------------------------------------------
# delete_bot
# ---------------------------------------------------------------------------


async def test_delete_bot_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    await delete_bot("b1")
    mc.call.assert_awaited_once()


async def test_delete_bot_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_bot failed"):
        await delete_bot("b1")


# ---------------------------------------------------------------------------
# create_intent
# ---------------------------------------------------------------------------


async def test_create_intent_ok(monkeypatch):
    mc = _mc({"intentId": "i1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_intent("b1", "DRAFT", "en_US", "Order")
    assert r["intentId"] == "i1"


async def test_create_intent_with_opts(monkeypatch):
    mc = _mc({"intentId": "i1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_intent(
        "b1", "DRAFT", "en_US", "Order",
        description="desc", sample_utterances=["order a pizza"],
    )
    assert r["intentId"] == "i1"


async def test_create_intent_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_intent failed"):
        await create_intent("b1", "DRAFT", "en_US", "Order")


# ---------------------------------------------------------------------------
# describe_intent
# ---------------------------------------------------------------------------


async def test_describe_intent_ok(monkeypatch):
    mc = _mc({"intentId": "i1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await describe_intent("b1", "DRAFT", "en_US", "i1")
    assert r["intentId"] == "i1"


async def test_describe_intent_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_intent failed"):
        await describe_intent("b1", "DRAFT", "en_US", "i1")


# ---------------------------------------------------------------------------
# list_intents
# ---------------------------------------------------------------------------


async def test_list_intents_ok(monkeypatch):
    mc = _mc({
        "intentSummaries": [
            {"intentId": "i1", "intentName": "Order"},
        ],
    })
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await list_intents("b1", "DRAFT", "en_US")
    assert len(r) == 1


async def test_list_intents_empty(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    assert await list_intents("b1", "DRAFT", "en_US") == []


async def test_list_intents_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_intents failed"):
        await list_intents("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# delete_intent
# ---------------------------------------------------------------------------


async def test_delete_intent_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    await delete_intent("b1", "DRAFT", "en_US", "i1")
    mc.call.assert_awaited_once()


async def test_delete_intent_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_intent failed"):
        await delete_intent("b1", "DRAFT", "en_US", "i1")


# ---------------------------------------------------------------------------
# create_slot_type
# ---------------------------------------------------------------------------


async def test_create_slot_type_ok(monkeypatch):
    mc = _mc({"slotTypeId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_slot_type("b1", "DRAFT", "en_US", "PizzaType")
    assert r["slotTypeId"] == "s1"


async def test_create_slot_type_with_opts(monkeypatch):
    mc = _mc({"slotTypeId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await create_slot_type(
        "b1", "DRAFT", "en_US", "PizzaType",
        value_selection_setting={"resolutionStrategy": "TopResolution"},
        slot_type_values=[{"sampleValue": {"value": "pepperoni"}}],
        description="pizza types",
    )
    assert r["slotTypeId"] == "s1"


async def test_create_slot_type_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_slot_type failed"):
        await create_slot_type("b1", "DRAFT", "en_US", "PizzaType")


# ---------------------------------------------------------------------------
# build_bot_locale
# ---------------------------------------------------------------------------


async def test_build_bot_locale_ok(monkeypatch):
    mc = _mc({"botLocaleStatus": "Building"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await build_bot_locale("b1", "DRAFT", "en_US")
    assert r["botLocaleStatus"] == "Building"


async def test_build_bot_locale_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="build_bot_locale failed"):
        await build_bot_locale("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# describe_bot_locale
# ---------------------------------------------------------------------------


async def test_describe_bot_locale_ok(monkeypatch):
    mc = _mc({
        "botId": "b1", "botVersion": "DRAFT", "localeId": "en_US",
        "localeName": "English", "botLocaleStatus": "Built",
    })
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await describe_bot_locale("b1", "DRAFT", "en_US")
    assert r.locale_name == "English"


async def test_describe_bot_locale_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_bot_locale failed"):
        await describe_bot_locale("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# wait_for_bot_locale
# ---------------------------------------------------------------------------


async def test_wait_for_bot_locale_ok(monkeypatch):
    mc = _mc({
        "botId": "b1", "botVersion": "DRAFT", "localeId": "en_US",
        "localeName": "English", "botLocaleStatus": "Built",
    })
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    r = await wait_for_bot_locale("b1", "DRAFT", "en_US")
    assert r.bot_locale_status == "Built"


async def test_wait_for_bot_locale_failed(monkeypatch):
    mc = _mc({"botLocaleStatus": "Failed"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(AwsServiceError, match="terminal status"):
        await wait_for_bot_locale("b1", "DRAFT", "en_US")


async def test_wait_for_bot_locale_deleting(monkeypatch):
    mc = _mc({"botLocaleStatus": "Deleting"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    with pytest.raises(AwsServiceError, match="terminal status"):
        await wait_for_bot_locale("b1", "DRAFT", "en_US")


async def test_wait_for_bot_locale_timeout(monkeypatch):
    mc = _mc({"botLocaleStatus": "Building"})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.lex_models.time.monotonic", lambda: 999.0)
    with pytest.raises(AwsServiceError, match="timed out"):
        await wait_for_bot_locale(
            "b1", "DRAFT", "en_US", max_wait=1.0,
        )


async def test_wait_for_bot_locale_polls_then_succeeds(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"botLocaleStatus": "Building"},
        {"botLocaleStatus": "Built"},
    ]
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.lex_models.time.monotonic", lambda: 0.0)
    monkeypatch.setattr("aws_util.aio.lex_models.asyncio.sleep", AsyncMock())
    r = await wait_for_bot_locale("b1", "DRAFT", "en_US", max_wait=600.0)
    assert r.bot_locale_status == "Built"


async def test_batch_create_custom_vocabulary_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_create_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_create_custom_vocabulary_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_create_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )


async def test_batch_delete_custom_vocabulary_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_custom_vocabulary_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )


async def test_batch_update_custom_vocabulary_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_update_custom_vocabulary_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], )


async def test_create_bot_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bot_alias("test-bot_alias_name", "test-bot_id", )
    mock_client.call.assert_called_once()


async def test_create_bot_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bot_alias("test-bot_alias_name", "test-bot_id", )


async def test_create_bot_locale(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", )
    mock_client.call.assert_called_once()


async def test_create_bot_locale_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", )


async def test_create_bot_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bot_replica("test-bot_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_create_bot_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bot_replica("test-bot_id", "test-replica_region", )


async def test_create_bot_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bot_version("test-bot_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_bot_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bot_version("test-bot_id", {}, )


async def test_create_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_export({}, "test-file_format", )
    mock_client.call.assert_called_once()


async def test_create_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_export({}, "test-file_format", )


async def test_create_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_create_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_policy("test-resource_arn", "test-policy", )


async def test_create_resource_policy_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", [], [], )
    mock_client.call.assert_called_once()


async def test_create_resource_policy_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", [], [], )


async def test_create_slot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_slot("test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )
    mock_client.call.assert_called_once()


async def test_create_slot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_slot("test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )


async def test_create_test_set_discrepancy_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_test_set_discrepancy_report("test-run_set_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_test_set_discrepancy_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_test_set_discrepancy_report("test-run_set_id", {}, )


async def test_create_upload_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_upload_url()
    mock_client.call.assert_called_once()


async def test_create_upload_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_upload_url()


async def test_delete_bot_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bot_alias("test-bot_alias_id", "test-bot_id", )
    mock_client.call.assert_called_once()


async def test_delete_bot_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bot_alias("test-bot_alias_id", "test-bot_id", )


async def test_delete_bot_locale(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_delete_bot_locale_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_delete_bot_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bot_replica("test-bot_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_delete_bot_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bot_replica("test-bot_id", "test-replica_region", )


async def test_delete_bot_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bot_version("test-bot_id", "test-bot_version", )
    mock_client.call.assert_called_once()


async def test_delete_bot_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bot_version("test-bot_id", "test-bot_version", )


async def test_delete_custom_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_vocabulary("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_delete_custom_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_vocabulary("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_delete_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_export("test-export_id", )
    mock_client.call.assert_called_once()


async def test_delete_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_export("test-export_id", )


async def test_delete_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_import("test-import_id", )
    mock_client.call.assert_called_once()


async def test_delete_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_import("test-import_id", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_resource_policy_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy_statement("test-resource_arn", "test-statement_id", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy_statement("test-resource_arn", "test-statement_id", )


async def test_delete_slot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )
    mock_client.call.assert_called_once()


async def test_delete_slot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )


async def test_delete_slot_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_delete_slot_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_delete_test_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_test_set("test-run_set_id", )
    mock_client.call.assert_called_once()


async def test_delete_test_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_test_set("test-run_set_id", )


async def test_delete_utterances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_utterances("test-bot_id", )
    mock_client.call.assert_called_once()


async def test_delete_utterances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_utterances("test-bot_id", )


async def test_describe_bot_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bot_alias("test-bot_alias_id", "test-bot_id", )
    mock_client.call.assert_called_once()


async def test_describe_bot_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bot_alias("test-bot_alias_id", "test-bot_id", )


async def test_describe_bot_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )
    mock_client.call.assert_called_once()


async def test_describe_bot_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )


async def test_describe_bot_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bot_replica("test-bot_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_describe_bot_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bot_replica("test-bot_id", "test-replica_region", )


async def test_describe_bot_resource_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bot_resource_generation("test-bot_id", "test-bot_version", "test-locale_id", "test-generation_id", )
    mock_client.call.assert_called_once()


async def test_describe_bot_resource_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bot_resource_generation("test-bot_id", "test-bot_version", "test-locale_id", "test-generation_id", )


async def test_describe_bot_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bot_version("test-bot_id", "test-bot_version", )
    mock_client.call.assert_called_once()


async def test_describe_bot_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bot_version("test-bot_id", "test-bot_version", )


async def test_describe_custom_vocabulary_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_vocabulary_metadata("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_describe_custom_vocabulary_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_vocabulary_metadata("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_describe_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_export("test-export_id", )
    mock_client.call.assert_called_once()


async def test_describe_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_export("test-export_id", )


async def test_describe_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_import("test-import_id", )
    mock_client.call.assert_called_once()


async def test_describe_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_import("test-import_id", )


async def test_describe_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_describe_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resource_policy("test-resource_arn", )


async def test_describe_slot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )
    mock_client.call.assert_called_once()


async def test_describe_slot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )


async def test_describe_slot_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_describe_slot_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_describe_test_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_test_execution("test-run_execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_test_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_test_execution("test-run_execution_id", )


async def test_describe_test_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_test_set("test-run_set_id", )
    mock_client.call.assert_called_once()


async def test_describe_test_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_test_set("test-run_set_id", )


async def test_describe_test_set_discrepancy_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_test_set_discrepancy_report("test-run_set_discrepancy_report_id", )
    mock_client.call.assert_called_once()


async def test_describe_test_set_discrepancy_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_test_set_discrepancy_report("test-run_set_discrepancy_report_id", )


async def test_describe_test_set_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_test_set_generation("test-run_set_generation_id", )
    mock_client.call.assert_called_once()


async def test_describe_test_set_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_test_set_generation("test-run_set_generation_id", )


async def test_generate_bot_element(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_bot_element("test-intent_id", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_generate_bot_element_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_bot_element("test-intent_id", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_get_test_execution_artifacts_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_test_execution_artifacts_url("test-run_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_test_execution_artifacts_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_test_execution_artifacts_url("test-run_execution_id", )


async def test_list_aggregated_utterances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_aggregated_utterances("test-bot_id", "test-locale_id", {}, )
    mock_client.call.assert_called_once()


async def test_list_aggregated_utterances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_aggregated_utterances("test-bot_id", "test-locale_id", {}, )


async def test_list_bot_alias_replicas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_alias_replicas("test-bot_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_list_bot_alias_replicas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_alias_replicas("test-bot_id", "test-replica_region", )


async def test_list_bot_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_aliases("test-bot_id", )
    mock_client.call.assert_called_once()


async def test_list_bot_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_aliases("test-bot_id", )


async def test_list_bot_locales(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_locales("test-bot_id", "test-bot_version", )
    mock_client.call.assert_called_once()


async def test_list_bot_locales_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_locales("test-bot_id", "test-bot_version", )


async def test_list_bot_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_bot_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_list_bot_replicas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_replicas("test-bot_id", )
    mock_client.call.assert_called_once()


async def test_list_bot_replicas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_replicas("test-bot_id", )


async def test_list_bot_resource_generations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_bot_resource_generations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_list_bot_version_replicas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_version_replicas("test-bot_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_list_bot_version_replicas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_version_replicas("test-bot_id", "test-replica_region", )


async def test_list_bot_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bot_versions("test-bot_id", )
    mock_client.call.assert_called_once()


async def test_list_bot_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bot_versions("test-bot_id", )


async def test_list_built_in_intents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_built_in_intents("test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_built_in_intents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_built_in_intents("test-locale_id", )


async def test_list_built_in_slot_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_built_in_slot_types("test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_built_in_slot_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_built_in_slot_types("test-locale_id", )


async def test_list_custom_vocabulary_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_custom_vocabulary_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_list_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_exports()
    mock_client.call.assert_called_once()


async def test_list_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_exports()


async def test_list_imports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_imports()
    mock_client.call.assert_called_once()


async def test_list_imports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_imports()


async def test_list_intent_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )
    mock_client.call.assert_called_once()


async def test_list_intent_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )


async def test_list_intent_paths(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", )
    mock_client.call.assert_called_once()


async def test_list_intent_paths_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", )


async def test_list_intent_stage_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )
    mock_client.call.assert_called_once()


async def test_list_intent_stage_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )


async def test_list_recommended_intents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )
    mock_client.call.assert_called_once()


async def test_list_recommended_intents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )


async def test_list_session_analytics_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", )
    mock_client.call.assert_called_once()


async def test_list_session_analytics_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", )


async def test_list_session_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )
    mock_client.call.assert_called_once()


async def test_list_session_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )


async def test_list_slot_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_list_slot_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", )


async def test_list_slots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )
    mock_client.call.assert_called_once()


async def test_list_slots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_test_execution_result_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_test_execution_result_items("test-run_execution_id", {}, )
    mock_client.call.assert_called_once()


async def test_list_test_execution_result_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_test_execution_result_items("test-run_execution_id", {}, )


async def test_list_test_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_test_executions()
    mock_client.call.assert_called_once()


async def test_list_test_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_test_executions()


async def test_list_test_set_records(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_test_set_records("test-run_set_id", )
    mock_client.call.assert_called_once()


async def test_list_test_set_records_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_test_set_records("test-run_set_id", )


async def test_list_test_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_test_sets()
    mock_client.call.assert_called_once()


async def test_list_test_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_test_sets()


async def test_list_utterance_analytics_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", )
    mock_client.call.assert_called_once()


async def test_list_utterance_analytics_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", )


async def test_list_utterance_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )
    mock_client.call.assert_called_once()


async def test_list_utterance_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], )


async def test_search_associated_transcripts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [], )
    mock_client.call.assert_called_once()


async def test_search_associated_transcripts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [], )


async def test_start_bot_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_bot_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", {}, )


async def test_start_bot_resource_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_bot_resource_generation("test-generation_input_prompt", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_start_bot_resource_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_bot_resource_generation("test-generation_input_prompt", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_start_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_import("test-import_id", {}, "test-merge_strategy", )
    mock_client.call.assert_called_once()


async def test_start_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_import("test-import_id", {}, "test-merge_strategy", )


async def test_start_test_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_test_execution("test-run_set_id", {}, "test-api_mode", )
    mock_client.call.assert_called_once()


async def test_start_test_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_test_execution("test-run_set_id", {}, "test-api_mode", )


async def test_start_test_set_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_test_set_generation("test-run_set_name", {}, {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_start_test_set_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_test_set_generation("test-run_set_name", {}, {}, "test-role_arn", )


async def test_stop_bot_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )
    mock_client.call.assert_called_once()


async def test_stop_bot_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_bot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bot("test-bot_id", "test-bot_name", "test-role_arn", {}, 1, )
    mock_client.call.assert_called_once()


async def test_update_bot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bot("test-bot_id", "test-bot_name", "test-role_arn", {}, 1, )


async def test_update_bot_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", )
    mock_client.call.assert_called_once()


async def test_update_bot_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", )


async def test_update_bot_locale(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", )
    mock_client.call.assert_called_once()


async def test_update_bot_locale_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", )


async def test_update_bot_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_bot_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", {}, )


async def test_update_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_export("test-export_id", )
    mock_client.call.assert_called_once()


async def test_update_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_export("test-export_id", )


async def test_update_intent(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_update_intent_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_update_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_update_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_policy("test-resource_arn", "test-policy", )


async def test_update_slot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_slot("test-slot_id", "test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )
    mock_client.call.assert_called_once()


async def test_update_slot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_slot("test-slot_id", "test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", )


async def test_update_slot_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", )
    mock_client.call.assert_called_once()


async def test_update_slot_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", )


async def test_update_test_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_test_set("test-run_set_id", "test-run_set_name", )
    mock_client.call.assert_called_once()


async def test_update_test_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lex_models.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_test_set("test-run_set_id", "test-run_set_name", )


@pytest.mark.asyncio
async def test_create_bot_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_bot_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_bot_alias("test-bot_alias_name", "test-bot_id", description="test-description", bot_version="test-bot_version", bot_alias_locale_settings={}, conversation_log_settings={}, sentiment_analysis_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bot_locale_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_bot_locale
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", description="test-description", voice_settings={}, generative_ai_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bot_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_bot_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_bot_version("test-bot_id", {}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_export_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_export
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_export({}, "test-file_format", file_password="test-file_password", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_resource_policy_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_resource_policy_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", "test-principal", "test-action", condition="test-condition", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_slot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import create_slot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await create_slot("test-slot_name", "test-value_elicitation_setting", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", description="test-description", slot_type_id="test-slot_type_id", obfuscation_setting="test-obfuscation_setting", multiple_values_setting=True, sub_slot_setting="test-sub_slot_setting", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bot_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_bot_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_bot_alias("test-bot_alias_id", "test-bot_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bot_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_bot_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_bot_version("test-bot_id", "test-bot_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_resource_policy("test-resource_arn", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_policy_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_resource_policy_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_resource_policy_statement("test-resource_arn", "test-statement_id", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_slot_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_slot_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_utterances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import delete_utterances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await delete_utterances("test-bot_id", locale_id="test-locale_id", session_id="test-session_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aggregated_utterances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_aggregated_utterances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_aggregated_utterances("test-bot_id", "test-locale_id", 1, bot_alias_id="test-bot_alias_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_alias_replicas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_alias_replicas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_alias_replicas("test-bot_id", "test-replica_region", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_aliases("test-bot_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_locales_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_locales
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_locales("test-bot_id", "test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_resource_generations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_resource_generations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_version_replicas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_version_replicas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_version_replicas("test-bot_id", "test-replica_region", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bot_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_bot_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_bot_versions("test-bot_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_built_in_intents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_built_in_intents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_built_in_intents("test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_built_in_slot_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_built_in_slot_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_built_in_slot_types("test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_vocabulary_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_custom_vocabulary_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_exports(bot_id="test-bot_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", locale_id="test-locale_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_imports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_imports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_imports(bot_id="test-bot_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", locale_id="test-locale_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_intent_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_intent_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_intent_paths_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_intent_paths
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_intent_stage_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_intent_stage_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recommended_intents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_recommended_intents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_session_analytics_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_session_analytics_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_session_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_session_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_slot_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_slot_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_slots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_slots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_test_execution_result_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_test_execution_result_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_test_execution_result_items("test-run_execution_id", "test-result_filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_test_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_test_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_test_executions(sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_test_set_records_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_test_set_records
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_test_set_records("test-run_set_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_test_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_test_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_test_sets(sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_utterance_analytics_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_utterance_analytics_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_utterance_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import list_utterance_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", attributes="test-attributes", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_associated_transcripts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import search_associated_transcripts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [{}], search_order="test-search_order", max_results=1, next_index="test-next_index", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_bot_recommendation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import start_bot_recommendation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-transcript_source_setting", encryption_setting="test-encryption_setting", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_import_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import start_import
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await start_import(1, {}, "test-merge_strategy", file_password="test-file_password", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_test_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import start_test_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await start_test_execution("test-run_set_id", "test-target", "test-api_mode", run_execution_modality="test-run_execution_modality", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_test_set_generation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import start_test_set_generation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await start_test_set_generation("test-run_set_name", "test-storage_location", "test-generation_data_source", "test-role_arn", description="test-description", run_set_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_bot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_bot("test-bot_id", "test-bot_name", "test-role_arn", "test-data_privacy", "test-idle_session_ttl_in_seconds", description="test-description", bot_type="test-bot_type", bot_members="test-bot_members", error_log_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bot_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_bot_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", description="test-description", bot_version="test-bot_version", bot_alias_locale_settings={}, conversation_log_settings={}, sentiment_analysis_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bot_locale_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_bot_locale
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", description="test-description", voice_settings={}, generative_ai_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_export_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_export
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_export(1, file_password="test-file_password", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_intent_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_intent
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", description="test-description", parent_intent_signature="test-parent_intent_signature", sample_utterances="test-sample_utterances", dialog_code_hook="test-dialog_code_hook", fulfillment_code_hook="test-fulfillment_code_hook", slot_priorities="test-slot_priorities", intent_confirmation_setting="test-intent_confirmation_setting", intent_closing_setting="test-intent_closing_setting", input_contexts={}, output_contexts={}, kendra_configuration={}, initial_response_setting="test-initial_response_setting", qn_a_intent_configuration={}, q_in_connect_intent_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_resource_policy("test-resource_arn", "{}", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_slot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_slot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_slot("test-slot_id", "test-slot_name", "test-value_elicitation_setting", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", description="test-description", slot_type_id="test-slot_type_id", obfuscation_setting="test-obfuscation_setting", multiple_values_setting=True, sub_slot_setting="test-sub_slot_setting", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_slot_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_slot_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", description="test-description", slot_type_values="test-slot_type_values", value_selection_setting="test-value_selection_setting", parent_slot_type_signature="test-parent_slot_type_signature", external_source_setting="test-external_source_setting", composite_slot_type_setting="test-composite_slot_type_setting", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_test_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lex_models import update_test_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lex_models.async_client", lambda *a, **kw: mock_client)
    await update_test_set("test-run_set_id", "test-run_set_name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()
