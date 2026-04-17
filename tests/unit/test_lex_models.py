"""Tests for aws_util.lex_models -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.exceptions import AwsServiceError
from aws_util.lex_models import (
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

REGION = "us-east-1"
_ERR = ClientError({"Error": {"Code": "X", "Message": "fail"}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_bot_summary_minimal():
    m = BotSummary(bot_id="b1", bot_name="mybot")
    assert m.bot_id == "b1"
    assert m.bot_status == ""
    assert m.description == ""


def test_bot_summary_full():
    m = BotSummary(
        bot_id="b1", bot_name="mybot", bot_status="Available",
        description="desc",
    )
    assert m.bot_status == "Available"


def test_intent_summary_minimal():
    m = IntentSummary(intent_id="i1", intent_name="Order")
    assert m.description == ""


def test_intent_summary_full():
    m = IntentSummary(
        intent_id="i1", intent_name="Order", description="desc",
    )
    assert m.description == "desc"


def test_bot_locale_info_minimal():
    m = BotLocaleInfo()
    assert m.bot_id == ""
    assert m.bot_locale_status == ""


def test_bot_locale_info_full():
    m = BotLocaleInfo(
        bot_id="b1", bot_version="DRAFT", locale_id="en_US",
        locale_name="English", bot_locale_status="Built",
    )
    assert m.locale_name == "English"


# ---------------------------------------------------------------------------
# create_bot
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_create_bot_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_bot.return_value = {"botId": "b1"}
    r = create_bot("mybot", "arn:role")
    assert r["botId"] == "b1"


@patch("aws_util.lex_models.get_client")
def test_create_bot_with_description(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_bot.return_value = {"botId": "b1"}
    r = create_bot("mybot", "arn:role", description="desc")
    assert r["botId"] == "b1"


@patch("aws_util.lex_models.get_client")
def test_create_bot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_bot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_bot failed"):
        create_bot("mybot", "arn:role")


# ---------------------------------------------------------------------------
# describe_bot
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_describe_bot_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_bot.return_value = {"botId": "b1"}
    r = describe_bot("b1")
    assert r["botId"] == "b1"


@patch("aws_util.lex_models.get_client")
def test_describe_bot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_bot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_bot failed"):
        describe_bot("b1")


# ---------------------------------------------------------------------------
# list_bots
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_list_bots_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_bots.return_value = {
        "botSummaries": [
            {"botId": "b1", "botName": "mybot", "botStatus": "Available"},
        ],
    }
    r = list_bots()
    assert len(r) == 1
    assert r[0].bot_id == "b1"


@patch("aws_util.lex_models.get_client")
def test_list_bots_empty(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_bots.return_value = {}
    assert list_bots() == []


@patch("aws_util.lex_models.get_client")
def test_list_bots_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_bots.side_effect = _ERR
    with pytest.raises(RuntimeError, match="list_bots failed"):
        list_bots()


# ---------------------------------------------------------------------------
# delete_bot
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_delete_bot_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_bot("b1")
    client.delete_bot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_bot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_bot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_bot failed"):
        delete_bot("b1")


# ---------------------------------------------------------------------------
# create_intent
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_create_intent_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_intent.return_value = {"intentId": "i1"}
    r = create_intent("b1", "DRAFT", "en_US", "Order")
    assert r["intentId"] == "i1"


@patch("aws_util.lex_models.get_client")
def test_create_intent_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_intent.return_value = {"intentId": "i1"}
    r = create_intent(
        "b1", "DRAFT", "en_US", "Order",
        description="desc", sample_utterances=["order a pizza"],
    )
    assert r["intentId"] == "i1"


@patch("aws_util.lex_models.get_client")
def test_create_intent_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_intent.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_intent failed"):
        create_intent("b1", "DRAFT", "en_US", "Order")


# ---------------------------------------------------------------------------
# describe_intent
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_describe_intent_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_intent.return_value = {"intentId": "i1"}
    r = describe_intent("b1", "DRAFT", "en_US", "i1")
    assert r["intentId"] == "i1"


@patch("aws_util.lex_models.get_client")
def test_describe_intent_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_intent.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_intent failed"):
        describe_intent("b1", "DRAFT", "en_US", "i1")


# ---------------------------------------------------------------------------
# list_intents
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_list_intents_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_intents.return_value = {
        "intentSummaries": [
            {"intentId": "i1", "intentName": "Order"},
        ],
    }
    r = list_intents("b1", "DRAFT", "en_US")
    assert len(r) == 1
    assert r[0].intent_id == "i1"


@patch("aws_util.lex_models.get_client")
def test_list_intents_empty(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_intents.return_value = {}
    assert list_intents("b1", "DRAFT", "en_US") == []


@patch("aws_util.lex_models.get_client")
def test_list_intents_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_intents.side_effect = _ERR
    with pytest.raises(RuntimeError, match="list_intents failed"):
        list_intents("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# delete_intent
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_delete_intent_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_intent("b1", "DRAFT", "en_US", "i1")
    client.delete_intent.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_intent_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_intent.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_intent failed"):
        delete_intent("b1", "DRAFT", "en_US", "i1")


# ---------------------------------------------------------------------------
# create_slot_type
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_create_slot_type_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_slot_type.return_value = {"slotTypeId": "s1"}
    r = create_slot_type("b1", "DRAFT", "en_US", "PizzaType")
    assert r["slotTypeId"] == "s1"


@patch("aws_util.lex_models.get_client")
def test_create_slot_type_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_slot_type.return_value = {"slotTypeId": "s1"}
    r = create_slot_type(
        "b1", "DRAFT", "en_US", "PizzaType",
        value_selection_setting={"resolutionStrategy": "TopResolution"},
        slot_type_values=[{"sampleValue": {"value": "pepperoni"}}],
        description="pizza types",
    )
    assert r["slotTypeId"] == "s1"


@patch("aws_util.lex_models.get_client")
def test_create_slot_type_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_slot_type.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_slot_type failed"):
        create_slot_type("b1", "DRAFT", "en_US", "PizzaType")


# ---------------------------------------------------------------------------
# build_bot_locale
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_build_bot_locale_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.build_bot_locale.return_value = {"botLocaleStatus": "Building"}
    r = build_bot_locale("b1", "DRAFT", "en_US")
    assert r["botLocaleStatus"] == "Building"


@patch("aws_util.lex_models.get_client")
def test_build_bot_locale_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.build_bot_locale.side_effect = _ERR
    with pytest.raises(RuntimeError, match="build_bot_locale failed"):
        build_bot_locale("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# describe_bot_locale
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.get_client")
def test_describe_bot_locale_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_bot_locale.return_value = {
        "botId": "b1", "botVersion": "DRAFT", "localeId": "en_US",
        "localeName": "English", "botLocaleStatus": "Built",
    }
    r = describe_bot_locale("b1", "DRAFT", "en_US")
    assert r.locale_name == "English"


@patch("aws_util.lex_models.get_client")
def test_describe_bot_locale_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_bot_locale.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_bot_locale failed"):
        describe_bot_locale("b1", "DRAFT", "en_US")


# ---------------------------------------------------------------------------
# wait_for_bot_locale
# ---------------------------------------------------------------------------


@patch("aws_util.lex_models.time")
@patch("aws_util.lex_models.describe_bot_locale")
def test_wait_for_bot_locale_ok(mock_desc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_time.sleep = MagicMock()
    mock_desc.return_value = BotLocaleInfo(bot_locale_status="Built")
    r = wait_for_bot_locale("b1", "DRAFT", "en_US")
    assert r.bot_locale_status == "Built"


@patch("aws_util.lex_models.time")
@patch("aws_util.lex_models.describe_bot_locale")
def test_wait_for_bot_locale_failed_status(mock_desc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_desc.return_value = BotLocaleInfo(bot_locale_status="Failed")
    with pytest.raises(AwsServiceError, match="terminal status"):
        wait_for_bot_locale("b1", "DRAFT", "en_US")


@patch("aws_util.lex_models.time")
@patch("aws_util.lex_models.describe_bot_locale")
def test_wait_for_bot_locale_deleting_status(mock_desc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_desc.return_value = BotLocaleInfo(bot_locale_status="Deleting")
    with pytest.raises(AwsServiceError, match="terminal status"):
        wait_for_bot_locale("b1", "DRAFT", "en_US")


@patch("aws_util.lex_models.time")
@patch("aws_util.lex_models.describe_bot_locale")
def test_wait_for_bot_locale_timeout(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0.0, 2.0]
    mock_time.sleep = MagicMock()
    mock_desc.return_value = BotLocaleInfo(bot_locale_status="Building")
    with pytest.raises(AwsServiceError, match="timed out"):
        wait_for_bot_locale("b1", "DRAFT", "en_US", max_wait=1.0)


@patch("aws_util.lex_models.time")
@patch("aws_util.lex_models.describe_bot_locale")
def test_wait_for_bot_locale_polls_then_succeeds(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0.0, 1.0, 2.0]
    mock_time.sleep = MagicMock()
    mock_desc.side_effect = [
        BotLocaleInfo(bot_locale_status="Building"),
        BotLocaleInfo(bot_locale_status="Built"),
    ]
    r = wait_for_bot_locale("b1", "DRAFT", "en_US", max_wait=600.0)
    assert r.bot_locale_status == "Built"
    mock_time.sleep.assert_called()


@patch("aws_util.lex_models.get_client")
def test_batch_create_custom_vocabulary_item(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_create_custom_vocabulary_item.return_value = {}
    batch_create_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)
    mock_client.batch_create_custom_vocabulary_item.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_batch_create_custom_vocabulary_item_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_create_custom_vocabulary_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_create_custom_vocabulary_item",
    )
    with pytest.raises(RuntimeError, match="Failed to batch create custom vocabulary item"):
        batch_create_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_batch_delete_custom_vocabulary_item(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_custom_vocabulary_item.return_value = {}
    batch_delete_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)
    mock_client.batch_delete_custom_vocabulary_item.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_batch_delete_custom_vocabulary_item_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_custom_vocabulary_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_custom_vocabulary_item",
    )
    with pytest.raises(RuntimeError, match="Failed to batch delete custom vocabulary item"):
        batch_delete_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_batch_update_custom_vocabulary_item(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_custom_vocabulary_item.return_value = {}
    batch_update_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)
    mock_client.batch_update_custom_vocabulary_item.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_batch_update_custom_vocabulary_item_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_custom_vocabulary_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_custom_vocabulary_item",
    )
    with pytest.raises(RuntimeError, match="Failed to batch update custom vocabulary item"):
        batch_update_custom_vocabulary_item("test-bot_id", "test-bot_version", "test-locale_id", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_bot_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_alias.return_value = {}
    create_bot_alias("test-bot_alias_name", "test-bot_id", region_name=REGION)
    mock_client.create_bot_alias.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_bot_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bot_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to create bot alias"):
        create_bot_alias("test-bot_alias_name", "test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_bot_locale(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_locale.return_value = {}
    create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", region_name=REGION)
    mock_client.create_bot_locale.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_bot_locale_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_locale.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bot_locale",
    )
    with pytest.raises(RuntimeError, match="Failed to create bot locale"):
        create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_bot_replica(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_replica.return_value = {}
    create_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)
    mock_client.create_bot_replica.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_bot_replica_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bot_replica",
    )
    with pytest.raises(RuntimeError, match="Failed to create bot replica"):
        create_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_bot_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_version.return_value = {}
    create_bot_version("test-bot_id", {}, region_name=REGION)
    mock_client.create_bot_version.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_bot_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bot_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bot_version",
    )
    with pytest.raises(RuntimeError, match="Failed to create bot version"):
        create_bot_version("test-bot_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_export(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_export.return_value = {}
    create_export({}, "test-file_format", region_name=REGION)
    mock_client.create_export.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_export_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_export",
    )
    with pytest.raises(RuntimeError, match="Failed to create export"):
        create_export({}, "test-file_format", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_policy.return_value = {}
    create_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.create_resource_policy.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to create resource policy"):
        create_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_resource_policy_statement(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_policy_statement.return_value = {}
    create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", [], [], region_name=REGION)
    mock_client.create_resource_policy_statement.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_resource_policy_statement_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_policy_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_policy_statement",
    )
    with pytest.raises(RuntimeError, match="Failed to create resource policy statement"):
        create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", [], [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_slot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_slot.return_value = {}
    create_slot("test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)
    mock_client.create_slot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_slot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_slot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_slot",
    )
    with pytest.raises(RuntimeError, match="Failed to create slot"):
        create_slot("test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_test_set_discrepancy_report(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_test_set_discrepancy_report.return_value = {}
    create_test_set_discrepancy_report("test-run_set_id", {}, region_name=REGION)
    mock_client.create_test_set_discrepancy_report.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_test_set_discrepancy_report_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_test_set_discrepancy_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_test_set_discrepancy_report",
    )
    with pytest.raises(RuntimeError, match="Failed to create test set discrepancy report"):
        create_test_set_discrepancy_report("test-run_set_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_create_upload_url(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_upload_url.return_value = {}
    create_upload_url(region_name=REGION)
    mock_client.create_upload_url.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_create_upload_url_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_upload_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_upload_url",
    )
    with pytest.raises(RuntimeError, match="Failed to create upload url"):
        create_upload_url(region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_bot_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_alias.return_value = {}
    delete_bot_alias("test-bot_alias_id", "test-bot_id", region_name=REGION)
    mock_client.delete_bot_alias.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_bot_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bot_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bot alias"):
        delete_bot_alias("test-bot_alias_id", "test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_bot_locale(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_locale.return_value = {}
    delete_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.delete_bot_locale.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_bot_locale_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_locale.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bot_locale",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bot locale"):
        delete_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_bot_replica(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_replica.return_value = {}
    delete_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)
    mock_client.delete_bot_replica.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_bot_replica_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bot_replica",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bot replica"):
        delete_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_bot_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_version.return_value = {}
    delete_bot_version("test-bot_id", "test-bot_version", region_name=REGION)
    mock_client.delete_bot_version.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_bot_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bot_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bot_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bot version"):
        delete_bot_version("test-bot_id", "test-bot_version", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_custom_vocabulary(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_vocabulary.return_value = {}
    delete_custom_vocabulary("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.delete_custom_vocabulary.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_custom_vocabulary_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_vocabulary",
    )
    with pytest.raises(RuntimeError, match="Failed to delete custom vocabulary"):
        delete_custom_vocabulary("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_export(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_export.return_value = {}
    delete_export("test-export_id", region_name=REGION)
    mock_client.delete_export.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_export_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_export",
    )
    with pytest.raises(RuntimeError, match="Failed to delete export"):
        delete_export("test-export_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_import(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_import.return_value = {}
    delete_import("test-import_id", region_name=REGION)
    mock_client.delete_import.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_import_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_import",
    )
    with pytest.raises(RuntimeError, match="Failed to delete import"):
        delete_import("test-import_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy.return_value = {}
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_resource_policy_statement(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy_statement.return_value = {}
    delete_resource_policy_statement("test-resource_arn", "test-statement_id", region_name=REGION)
    mock_client.delete_resource_policy_statement.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_resource_policy_statement_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy_statement",
    )
    with pytest.raises(RuntimeError, match="Failed to delete resource policy statement"):
        delete_resource_policy_statement("test-resource_arn", "test-statement_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_slot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_slot.return_value = {}
    delete_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)
    mock_client.delete_slot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_slot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_slot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_slot",
    )
    with pytest.raises(RuntimeError, match="Failed to delete slot"):
        delete_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_slot_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_slot_type.return_value = {}
    delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.delete_slot_type.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_slot_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_slot_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_slot_type",
    )
    with pytest.raises(RuntimeError, match="Failed to delete slot type"):
        delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_test_set(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_test_set.return_value = {}
    delete_test_set("test-run_set_id", region_name=REGION)
    mock_client.delete_test_set.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_test_set_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_test_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_test_set",
    )
    with pytest.raises(RuntimeError, match="Failed to delete test set"):
        delete_test_set("test-run_set_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_delete_utterances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_utterances.return_value = {}
    delete_utterances("test-bot_id", region_name=REGION)
    mock_client.delete_utterances.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_delete_utterances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_utterances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_utterances",
    )
    with pytest.raises(RuntimeError, match="Failed to delete utterances"):
        delete_utterances("test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_bot_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_alias.return_value = {}
    describe_bot_alias("test-bot_alias_id", "test-bot_id", region_name=REGION)
    mock_client.describe_bot_alias.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_bot_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bot_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bot alias"):
        describe_bot_alias("test-bot_alias_id", "test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_bot_recommendation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_recommendation.return_value = {}
    describe_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)
    mock_client.describe_bot_recommendation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_bot_recommendation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bot_recommendation",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bot recommendation"):
        describe_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_bot_replica(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_replica.return_value = {}
    describe_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)
    mock_client.describe_bot_replica.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_bot_replica_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bot_replica",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bot replica"):
        describe_bot_replica("test-bot_id", "test-replica_region", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_bot_resource_generation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_resource_generation.return_value = {}
    describe_bot_resource_generation("test-bot_id", "test-bot_version", "test-locale_id", "test-generation_id", region_name=REGION)
    mock_client.describe_bot_resource_generation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_bot_resource_generation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_resource_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bot_resource_generation",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bot resource generation"):
        describe_bot_resource_generation("test-bot_id", "test-bot_version", "test-locale_id", "test-generation_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_bot_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_version.return_value = {}
    describe_bot_version("test-bot_id", "test-bot_version", region_name=REGION)
    mock_client.describe_bot_version.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_bot_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bot_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bot_version",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bot version"):
        describe_bot_version("test-bot_id", "test-bot_version", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_custom_vocabulary_metadata(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_custom_vocabulary_metadata.return_value = {}
    describe_custom_vocabulary_metadata("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.describe_custom_vocabulary_metadata.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_custom_vocabulary_metadata_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_custom_vocabulary_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_vocabulary_metadata",
    )
    with pytest.raises(RuntimeError, match="Failed to describe custom vocabulary metadata"):
        describe_custom_vocabulary_metadata("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_export(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_export.return_value = {}
    describe_export("test-export_id", region_name=REGION)
    mock_client.describe_export.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_export_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_export",
    )
    with pytest.raises(RuntimeError, match="Failed to describe export"):
        describe_export("test-export_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_import(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_import.return_value = {}
    describe_import("test-import_id", region_name=REGION)
    mock_client.describe_import.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_import_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_import",
    )
    with pytest.raises(RuntimeError, match="Failed to describe import"):
        describe_import("test-import_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_resource_policy.return_value = {}
    describe_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.describe_resource_policy.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to describe resource policy"):
        describe_resource_policy("test-resource_arn", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_slot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_slot.return_value = {}
    describe_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)
    mock_client.describe_slot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_slot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_slot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_slot",
    )
    with pytest.raises(RuntimeError, match="Failed to describe slot"):
        describe_slot("test-slot_id", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_slot_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_slot_type.return_value = {}
    describe_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.describe_slot_type.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_slot_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_slot_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_slot_type",
    )
    with pytest.raises(RuntimeError, match="Failed to describe slot type"):
        describe_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_test_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_execution.return_value = {}
    describe_test_execution("test-run_execution_id", region_name=REGION)
    mock_client.describe_test_execution.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_test_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_test_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to describe test execution"):
        describe_test_execution("test-run_execution_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_test_set(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set.return_value = {}
    describe_test_set("test-run_set_id", region_name=REGION)
    mock_client.describe_test_set.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_test_set_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_test_set",
    )
    with pytest.raises(RuntimeError, match="Failed to describe test set"):
        describe_test_set("test-run_set_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_test_set_discrepancy_report(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set_discrepancy_report.return_value = {}
    describe_test_set_discrepancy_report("test-run_set_discrepancy_report_id", region_name=REGION)
    mock_client.describe_test_set_discrepancy_report.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_test_set_discrepancy_report_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set_discrepancy_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_test_set_discrepancy_report",
    )
    with pytest.raises(RuntimeError, match="Failed to describe test set discrepancy report"):
        describe_test_set_discrepancy_report("test-run_set_discrepancy_report_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_describe_test_set_generation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set_generation.return_value = {}
    describe_test_set_generation("test-run_set_generation_id", region_name=REGION)
    mock_client.describe_test_set_generation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_describe_test_set_generation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_set_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_test_set_generation",
    )
    with pytest.raises(RuntimeError, match="Failed to describe test set generation"):
        describe_test_set_generation("test-run_set_generation_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_generate_bot_element(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.generate_bot_element.return_value = {}
    generate_bot_element("test-intent_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.generate_bot_element.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_generate_bot_element_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.generate_bot_element.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_bot_element",
    )
    with pytest.raises(RuntimeError, match="Failed to generate bot element"):
        generate_bot_element("test-intent_id", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_get_test_execution_artifacts_url(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_test_execution_artifacts_url.return_value = {}
    get_test_execution_artifacts_url("test-run_execution_id", region_name=REGION)
    mock_client.get_test_execution_artifacts_url.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_get_test_execution_artifacts_url_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_test_execution_artifacts_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_test_execution_artifacts_url",
    )
    with pytest.raises(RuntimeError, match="Failed to get test execution artifacts url"):
        get_test_execution_artifacts_url("test-run_execution_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_aggregated_utterances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_aggregated_utterances.return_value = {}
    list_aggregated_utterances("test-bot_id", "test-locale_id", {}, region_name=REGION)
    mock_client.list_aggregated_utterances.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_aggregated_utterances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_aggregated_utterances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aggregated_utterances",
    )
    with pytest.raises(RuntimeError, match="Failed to list aggregated utterances"):
        list_aggregated_utterances("test-bot_id", "test-locale_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_alias_replicas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_alias_replicas.return_value = {}
    list_bot_alias_replicas("test-bot_id", "test-replica_region", region_name=REGION)
    mock_client.list_bot_alias_replicas.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_alias_replicas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_alias_replicas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_alias_replicas",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot alias replicas"):
        list_bot_alias_replicas("test-bot_id", "test-replica_region", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_aliases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_aliases.return_value = {}
    list_bot_aliases("test-bot_id", region_name=REGION)
    mock_client.list_bot_aliases.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_aliases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_aliases",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot aliases"):
        list_bot_aliases("test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_locales(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_locales.return_value = {}
    list_bot_locales("test-bot_id", "test-bot_version", region_name=REGION)
    mock_client.list_bot_locales.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_locales_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_locales.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_locales",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot locales"):
        list_bot_locales("test-bot_id", "test-bot_version", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_recommendations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_recommendations.return_value = {}
    list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.list_bot_recommendations.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_recommendations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_recommendations",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot recommendations"):
        list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_replicas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_replicas.return_value = {}
    list_bot_replicas("test-bot_id", region_name=REGION)
    mock_client.list_bot_replicas.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_replicas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_replicas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_replicas",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot replicas"):
        list_bot_replicas("test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_resource_generations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_resource_generations.return_value = {}
    list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.list_bot_resource_generations.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_resource_generations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_resource_generations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_resource_generations",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot resource generations"):
        list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_version_replicas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_version_replicas.return_value = {}
    list_bot_version_replicas("test-bot_id", "test-replica_region", region_name=REGION)
    mock_client.list_bot_version_replicas.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_version_replicas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_version_replicas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_version_replicas",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot version replicas"):
        list_bot_version_replicas("test-bot_id", "test-replica_region", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_bot_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_versions.return_value = {}
    list_bot_versions("test-bot_id", region_name=REGION)
    mock_client.list_bot_versions.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_bot_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bot_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bot_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list bot versions"):
        list_bot_versions("test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_built_in_intents(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_built_in_intents.return_value = {}
    list_built_in_intents("test-locale_id", region_name=REGION)
    mock_client.list_built_in_intents.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_built_in_intents_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_built_in_intents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_built_in_intents",
    )
    with pytest.raises(RuntimeError, match="Failed to list built in intents"):
        list_built_in_intents("test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_built_in_slot_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_built_in_slot_types.return_value = {}
    list_built_in_slot_types("test-locale_id", region_name=REGION)
    mock_client.list_built_in_slot_types.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_built_in_slot_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_built_in_slot_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_built_in_slot_types",
    )
    with pytest.raises(RuntimeError, match="Failed to list built in slot types"):
        list_built_in_slot_types("test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_custom_vocabulary_items(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_vocabulary_items.return_value = {}
    list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.list_custom_vocabulary_items.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_custom_vocabulary_items_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_vocabulary_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_vocabulary_items",
    )
    with pytest.raises(RuntimeError, match="Failed to list custom vocabulary items"):
        list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_exports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_exports.return_value = {}
    list_exports(region_name=REGION)
    mock_client.list_exports.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_exports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_exports",
    )
    with pytest.raises(RuntimeError, match="Failed to list exports"):
        list_exports(region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_imports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_imports.return_value = {}
    list_imports(region_name=REGION)
    mock_client.list_imports.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_imports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_imports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_imports",
    )
    with pytest.raises(RuntimeError, match="Failed to list imports"):
        list_imports(region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_intent_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_metrics.return_value = {}
    list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)
    mock_client.list_intent_metrics.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_intent_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_intent_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list intent metrics"):
        list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_intent_paths(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_paths.return_value = {}
    list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", region_name=REGION)
    mock_client.list_intent_paths.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_intent_paths_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_paths.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_intent_paths",
    )
    with pytest.raises(RuntimeError, match="Failed to list intent paths"):
        list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_intent_stage_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_stage_metrics.return_value = {}
    list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)
    mock_client.list_intent_stage_metrics.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_intent_stage_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_intent_stage_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_intent_stage_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list intent stage metrics"):
        list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_recommended_intents(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_recommended_intents.return_value = {}
    list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)
    mock_client.list_recommended_intents.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_recommended_intents_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_recommended_intents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recommended_intents",
    )
    with pytest.raises(RuntimeError, match="Failed to list recommended intents"):
        list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_session_analytics_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_session_analytics_data.return_value = {}
    list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", region_name=REGION)
    mock_client.list_session_analytics_data.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_session_analytics_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_session_analytics_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_session_analytics_data",
    )
    with pytest.raises(RuntimeError, match="Failed to list session analytics data"):
        list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_session_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_session_metrics.return_value = {}
    list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)
    mock_client.list_session_metrics.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_session_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_session_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_session_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list session metrics"):
        list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_slot_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_slot_types.return_value = {}
    list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.list_slot_types.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_slot_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_slot_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_slot_types",
    )
    with pytest.raises(RuntimeError, match="Failed to list slot types"):
        list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_slots(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_slots.return_value = {}
    list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)
    mock_client.list_slots.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_slots_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_slots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_slots",
    )
    with pytest.raises(RuntimeError, match="Failed to list slots"):
        list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_test_execution_result_items(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_execution_result_items.return_value = {}
    list_test_execution_result_items("test-run_execution_id", {}, region_name=REGION)
    mock_client.list_test_execution_result_items.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_test_execution_result_items_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_execution_result_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_test_execution_result_items",
    )
    with pytest.raises(RuntimeError, match="Failed to list test execution result items"):
        list_test_execution_result_items("test-run_execution_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_test_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_executions.return_value = {}
    list_test_executions(region_name=REGION)
    mock_client.list_test_executions.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_test_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_test_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list test executions"):
        list_test_executions(region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_test_set_records(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_set_records.return_value = {}
    list_test_set_records("test-run_set_id", region_name=REGION)
    mock_client.list_test_set_records.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_test_set_records_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_set_records.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_test_set_records",
    )
    with pytest.raises(RuntimeError, match="Failed to list test set records"):
        list_test_set_records("test-run_set_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_test_sets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_sets.return_value = {}
    list_test_sets(region_name=REGION)
    mock_client.list_test_sets.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_test_sets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_test_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_test_sets",
    )
    with pytest.raises(RuntimeError, match="Failed to list test sets"):
        list_test_sets(region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_utterance_analytics_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_utterance_analytics_data.return_value = {}
    list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", region_name=REGION)
    mock_client.list_utterance_analytics_data.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_utterance_analytics_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_utterance_analytics_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_utterance_analytics_data",
    )
    with pytest.raises(RuntimeError, match="Failed to list utterance analytics data"):
        list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_list_utterance_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_utterance_metrics.return_value = {}
    list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)
    mock_client.list_utterance_metrics.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_list_utterance_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_utterance_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_utterance_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list utterance metrics"):
        list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_search_associated_transcripts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_associated_transcripts.return_value = {}
    search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [], region_name=REGION)
    mock_client.search_associated_transcripts.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_search_associated_transcripts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_associated_transcripts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_associated_transcripts",
    )
    with pytest.raises(RuntimeError, match="Failed to search associated transcripts"):
        search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_start_bot_recommendation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_bot_recommendation.return_value = {}
    start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", {}, region_name=REGION)
    mock_client.start_bot_recommendation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_start_bot_recommendation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_bot_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_bot_recommendation",
    )
    with pytest.raises(RuntimeError, match="Failed to start bot recommendation"):
        start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_start_bot_resource_generation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_bot_resource_generation.return_value = {}
    start_bot_resource_generation("test-generation_input_prompt", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.start_bot_resource_generation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_start_bot_resource_generation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_bot_resource_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_bot_resource_generation",
    )
    with pytest.raises(RuntimeError, match="Failed to start bot resource generation"):
        start_bot_resource_generation("test-generation_input_prompt", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_start_import(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_import.return_value = {}
    start_import("test-import_id", {}, "test-merge_strategy", region_name=REGION)
    mock_client.start_import.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_start_import_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_import",
    )
    with pytest.raises(RuntimeError, match="Failed to start import"):
        start_import("test-import_id", {}, "test-merge_strategy", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_start_test_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_test_execution.return_value = {}
    start_test_execution("test-run_set_id", {}, "test-api_mode", region_name=REGION)
    mock_client.start_test_execution.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_start_test_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_test_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_test_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to start test execution"):
        start_test_execution("test-run_set_id", {}, "test-api_mode", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_start_test_set_generation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_test_set_generation.return_value = {}
    start_test_set_generation("test-run_set_name", {}, {}, "test-role_arn", region_name=REGION)
    mock_client.start_test_set_generation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_start_test_set_generation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_test_set_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_test_set_generation",
    )
    with pytest.raises(RuntimeError, match="Failed to start test set generation"):
        start_test_set_generation("test-run_set_name", {}, {}, "test-role_arn", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_stop_bot_recommendation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_bot_recommendation.return_value = {}
    stop_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)
    mock_client.stop_bot_recommendation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_stop_bot_recommendation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_bot_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_bot_recommendation",
    )
    with pytest.raises(RuntimeError, match="Failed to stop bot recommendation"):
        stop_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_bot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot.return_value = {}
    update_bot("test-bot_id", "test-bot_name", "test-role_arn", {}, 1, region_name=REGION)
    mock_client.update_bot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_bot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bot",
    )
    with pytest.raises(RuntimeError, match="Failed to update bot"):
        update_bot("test-bot_id", "test-bot_name", "test-role_arn", {}, 1, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_bot_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_alias.return_value = {}
    update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", region_name=REGION)
    mock_client.update_bot_alias.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_bot_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bot_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to update bot alias"):
        update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_bot_locale(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_locale.return_value = {}
    update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", region_name=REGION)
    mock_client.update_bot_locale.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_bot_locale_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_locale.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bot_locale",
    )
    with pytest.raises(RuntimeError, match="Failed to update bot locale"):
        update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_bot_recommendation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_recommendation.return_value = {}
    update_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", {}, region_name=REGION)
    mock_client.update_bot_recommendation.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_bot_recommendation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bot_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bot_recommendation",
    )
    with pytest.raises(RuntimeError, match="Failed to update bot recommendation"):
        update_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", {}, region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_export(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_export.return_value = {}
    update_export("test-export_id", region_name=REGION)
    mock_client.update_export.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_export_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_export",
    )
    with pytest.raises(RuntimeError, match="Failed to update export"):
        update_export("test-export_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_intent(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_intent.return_value = {}
    update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.update_intent.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_intent_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_intent.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_intent",
    )
    with pytest.raises(RuntimeError, match="Failed to update intent"):
        update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_policy.return_value = {}
    update_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.update_resource_policy.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to update resource policy"):
        update_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_slot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_slot.return_value = {}
    update_slot("test-slot_id", "test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)
    mock_client.update_slot.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_slot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_slot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_slot",
    )
    with pytest.raises(RuntimeError, match="Failed to update slot"):
        update_slot("test-slot_id", "test-slot_name", {}, "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_slot_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_slot_type.return_value = {}
    update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)
    mock_client.update_slot_type.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_slot_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_slot_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_slot_type",
    )
    with pytest.raises(RuntimeError, match="Failed to update slot type"):
        update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", region_name=REGION)


@patch("aws_util.lex_models.get_client")
def test_update_test_set(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_test_set.return_value = {}
    update_test_set("test-run_set_id", "test-run_set_name", region_name=REGION)
    mock_client.update_test_set.assert_called_once()


@patch("aws_util.lex_models.get_client")
def test_update_test_set_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_test_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_test_set",
    )
    with pytest.raises(RuntimeError, match="Failed to update test set"):
        update_test_set("test-run_set_id", "test-run_set_name", region_name=REGION)


def test_create_bot_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_bot_alias
    mock_client = MagicMock()
    mock_client.create_bot_alias.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_bot_alias("test-bot_alias_name", "test-bot_id", description="test-description", bot_version="test-bot_version", bot_alias_locale_settings={}, conversation_log_settings={}, sentiment_analysis_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_bot_alias.assert_called_once()

def test_create_bot_locale_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_bot_locale
    mock_client = MagicMock()
    mock_client.create_bot_locale.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", description="test-description", voice_settings={}, generative_ai_settings={}, region_name="us-east-1")
    mock_client.create_bot_locale.assert_called_once()

def test_create_bot_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_bot_version
    mock_client = MagicMock()
    mock_client.create_bot_version.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_bot_version("test-bot_id", {}, description="test-description", region_name="us-east-1")
    mock_client.create_bot_version.assert_called_once()

def test_create_export_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_export
    mock_client = MagicMock()
    mock_client.create_export.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_export({}, "test-file_format", file_password="test-file_password", region_name="us-east-1")
    mock_client.create_export.assert_called_once()

def test_create_resource_policy_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_resource_policy_statement
    mock_client = MagicMock()
    mock_client.create_resource_policy_statement.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_resource_policy_statement("test-resource_arn", "test-statement_id", "test-effect", "test-principal", "test-action", condition="test-condition", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.create_resource_policy_statement.assert_called_once()

def test_create_slot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import create_slot
    mock_client = MagicMock()
    mock_client.create_slot.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    create_slot("test-slot_name", "test-value_elicitation_setting", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", description="test-description", slot_type_id="test-slot_type_id", obfuscation_setting="test-obfuscation_setting", multiple_values_setting=True, sub_slot_setting="test-sub_slot_setting", region_name="us-east-1")
    mock_client.create_slot.assert_called_once()

def test_delete_bot_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_bot_alias
    mock_client = MagicMock()
    mock_client.delete_bot_alias.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_bot_alias("test-bot_alias_id", "test-bot_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_bot_alias.assert_called_once()

def test_delete_bot_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_bot_version
    mock_client = MagicMock()
    mock_client.delete_bot_version.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_bot_version("test-bot_id", "test-bot_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_bot_version.assert_called_once()

def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_resource_policy
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.delete_resource_policy.assert_called_once()

def test_delete_resource_policy_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_resource_policy_statement
    mock_client = MagicMock()
    mock_client.delete_resource_policy_statement.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy_statement("test-resource_arn", "test-statement_id", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.delete_resource_policy_statement.assert_called_once()

def test_delete_slot_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_slot_type
    mock_client = MagicMock()
    mock_client.delete_slot_type.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_slot_type("test-slot_type_id", "test-bot_id", "test-bot_version", "test-locale_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_slot_type.assert_called_once()

def test_delete_utterances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import delete_utterances
    mock_client = MagicMock()
    mock_client.delete_utterances.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    delete_utterances("test-bot_id", locale_id="test-locale_id", session_id="test-session_id", region_name="us-east-1")
    mock_client.delete_utterances.assert_called_once()

def test_list_aggregated_utterances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_aggregated_utterances
    mock_client = MagicMock()
    mock_client.list_aggregated_utterances.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_aggregated_utterances("test-bot_id", "test-locale_id", 1, bot_alias_id="test-bot_alias_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_aggregated_utterances.assert_called_once()

def test_list_bot_alias_replicas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_alias_replicas
    mock_client = MagicMock()
    mock_client.list_bot_alias_replicas.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_alias_replicas("test-bot_id", "test-replica_region", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_alias_replicas.assert_called_once()

def test_list_bot_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_aliases
    mock_client = MagicMock()
    mock_client.list_bot_aliases.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_aliases("test-bot_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_aliases.assert_called_once()

def test_list_bot_locales_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_locales
    mock_client = MagicMock()
    mock_client.list_bot_locales.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_locales("test-bot_id", "test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_locales.assert_called_once()

def test_list_bot_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_recommendations
    mock_client = MagicMock()
    mock_client.list_bot_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_recommendations("test-bot_id", "test-bot_version", "test-locale_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_recommendations.assert_called_once()

def test_list_bot_resource_generations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_resource_generations
    mock_client = MagicMock()
    mock_client.list_bot_resource_generations.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_resource_generations("test-bot_id", "test-bot_version", "test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_resource_generations.assert_called_once()

def test_list_bot_version_replicas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_version_replicas
    mock_client = MagicMock()
    mock_client.list_bot_version_replicas.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_version_replicas("test-bot_id", "test-replica_region", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.list_bot_version_replicas.assert_called_once()

def test_list_bot_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_bot_versions
    mock_client = MagicMock()
    mock_client.list_bot_versions.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_bot_versions("test-bot_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_bot_versions.assert_called_once()

def test_list_built_in_intents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_built_in_intents
    mock_client = MagicMock()
    mock_client.list_built_in_intents.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_built_in_intents("test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_built_in_intents.assert_called_once()

def test_list_built_in_slot_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_built_in_slot_types
    mock_client = MagicMock()
    mock_client.list_built_in_slot_types.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_built_in_slot_types("test-locale_id", sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_built_in_slot_types.assert_called_once()

def test_list_custom_vocabulary_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_custom_vocabulary_items
    mock_client = MagicMock()
    mock_client.list_custom_vocabulary_items.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_custom_vocabulary_items("test-bot_id", "test-bot_version", "test-locale_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_custom_vocabulary_items.assert_called_once()

def test_list_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_exports
    mock_client = MagicMock()
    mock_client.list_exports.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_exports(bot_id="test-bot_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", locale_id="test-locale_id", region_name="us-east-1")
    mock_client.list_exports.assert_called_once()

def test_list_imports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_imports
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_imports(bot_id="test-bot_id", bot_version="test-bot_version", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", locale_id="test-locale_id", region_name="us-east-1")
    mock_client.list_imports.assert_called_once()

def test_list_intent_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_intent_metrics
    mock_client = MagicMock()
    mock_client.list_intent_metrics.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_intent_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_intent_metrics.assert_called_once()

def test_list_intent_paths_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_intent_paths
    mock_client = MagicMock()
    mock_client.list_intent_paths.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_intent_paths("test-bot_id", "test-start_date_time", "test-end_date_time", "test-intent_path", filters=[{}], region_name="us-east-1")
    mock_client.list_intent_paths.assert_called_once()

def test_list_intent_stage_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_intent_stage_metrics
    mock_client = MagicMock()
    mock_client.list_intent_stage_metrics.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_intent_stage_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_intent_stage_metrics.assert_called_once()

def test_list_recommended_intents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_recommended_intents
    mock_client = MagicMock()
    mock_client.list_recommended_intents.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_recommended_intents("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_recommended_intents.assert_called_once()

def test_list_session_analytics_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_session_analytics_data
    mock_client = MagicMock()
    mock_client.list_session_analytics_data.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_session_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_session_analytics_data.assert_called_once()

def test_list_session_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_session_metrics
    mock_client = MagicMock()
    mock_client.list_session_metrics.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_session_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_session_metrics.assert_called_once()

def test_list_slot_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_slot_types
    mock_client = MagicMock()
    mock_client.list_slot_types.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_slot_types("test-bot_id", "test-bot_version", "test-locale_id", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_slot_types.assert_called_once()

def test_list_slots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_slots
    mock_client = MagicMock()
    mock_client.list_slots.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_slots("test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_slots.assert_called_once()

def test_list_test_execution_result_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_test_execution_result_items
    mock_client = MagicMock()
    mock_client.list_test_execution_result_items.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_test_execution_result_items("test-run_execution_id", "test-result_filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_test_execution_result_items.assert_called_once()

def test_list_test_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_test_executions
    mock_client = MagicMock()
    mock_client.list_test_executions.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_test_executions(sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_test_executions.assert_called_once()

def test_list_test_set_records_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_test_set_records
    mock_client = MagicMock()
    mock_client.list_test_set_records.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_test_set_records("test-run_set_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_test_set_records.assert_called_once()

def test_list_test_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_test_sets
    mock_client = MagicMock()
    mock_client.list_test_sets.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_test_sets(sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_test_sets.assert_called_once()

def test_list_utterance_analytics_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_utterance_analytics_data
    mock_client = MagicMock()
    mock_client.list_utterance_analytics_data.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_utterance_analytics_data("test-bot_id", "test-start_date_time", "test-end_date_time", sort_by="test-sort_by", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_utterance_analytics_data.assert_called_once()

def test_list_utterance_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import list_utterance_metrics
    mock_client = MagicMock()
    mock_client.list_utterance_metrics.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    list_utterance_metrics("test-bot_id", "test-start_date_time", "test-end_date_time", "test-metrics", bin_by="test-bin_by", group_by="test-group_by", attributes="test-attributes", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_utterance_metrics.assert_called_once()

def test_search_associated_transcripts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import search_associated_transcripts
    mock_client = MagicMock()
    mock_client.search_associated_transcripts.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    search_associated_transcripts("test-bot_id", "test-bot_version", "test-locale_id", "test-bot_recommendation_id", [{}], search_order="test-search_order", max_results=1, next_index="test-next_index", region_name="us-east-1")
    mock_client.search_associated_transcripts.assert_called_once()

def test_start_bot_recommendation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import start_bot_recommendation
    mock_client = MagicMock()
    mock_client.start_bot_recommendation.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    start_bot_recommendation("test-bot_id", "test-bot_version", "test-locale_id", "test-transcript_source_setting", encryption_setting="test-encryption_setting", region_name="us-east-1")
    mock_client.start_bot_recommendation.assert_called_once()

def test_start_import_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import start_import
    mock_client = MagicMock()
    mock_client.start_import.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    start_import(1, {}, "test-merge_strategy", file_password="test-file_password", region_name="us-east-1")
    mock_client.start_import.assert_called_once()

def test_start_test_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import start_test_execution
    mock_client = MagicMock()
    mock_client.start_test_execution.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    start_test_execution("test-run_set_id", "test-target", "test-api_mode", run_execution_modality="test-run_execution_modality", region_name="us-east-1")
    mock_client.start_test_execution.assert_called_once()

def test_start_test_set_generation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import start_test_set_generation
    mock_client = MagicMock()
    mock_client.start_test_set_generation.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    start_test_set_generation("test-run_set_name", "test-storage_location", "test-generation_data_source", "test-role_arn", description="test-description", run_set_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_test_set_generation.assert_called_once()

def test_update_bot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_bot
    mock_client = MagicMock()
    mock_client.update_bot.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_bot("test-bot_id", "test-bot_name", "test-role_arn", "test-data_privacy", "test-idle_session_ttl_in_seconds", description="test-description", bot_type="test-bot_type", bot_members="test-bot_members", error_log_settings={}, region_name="us-east-1")
    mock_client.update_bot.assert_called_once()

def test_update_bot_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_bot_alias
    mock_client = MagicMock()
    mock_client.update_bot_alias.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_bot_alias("test-bot_alias_id", "test-bot_alias_name", "test-bot_id", description="test-description", bot_version="test-bot_version", bot_alias_locale_settings={}, conversation_log_settings={}, sentiment_analysis_settings={}, region_name="us-east-1")
    mock_client.update_bot_alias.assert_called_once()

def test_update_bot_locale_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_bot_locale
    mock_client = MagicMock()
    mock_client.update_bot_locale.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_bot_locale("test-bot_id", "test-bot_version", "test-locale_id", "test-nlu_intent_confidence_threshold", description="test-description", voice_settings={}, generative_ai_settings={}, region_name="us-east-1")
    mock_client.update_bot_locale.assert_called_once()

def test_update_export_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_export
    mock_client = MagicMock()
    mock_client.update_export.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_export(1, file_password="test-file_password", region_name="us-east-1")
    mock_client.update_export.assert_called_once()

def test_update_intent_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_intent
    mock_client = MagicMock()
    mock_client.update_intent.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_intent("test-intent_id", "test-intent_name", "test-bot_id", "test-bot_version", "test-locale_id", description="test-description", parent_intent_signature="test-parent_intent_signature", sample_utterances="test-sample_utterances", dialog_code_hook="test-dialog_code_hook", fulfillment_code_hook="test-fulfillment_code_hook", slot_priorities="test-slot_priorities", intent_confirmation_setting="test-intent_confirmation_setting", intent_closing_setting="test-intent_closing_setting", input_contexts={}, output_contexts={}, kendra_configuration={}, initial_response_setting="test-initial_response_setting", qn_a_intent_configuration={}, q_in_connect_intent_configuration={}, region_name="us-east-1")
    mock_client.update_intent.assert_called_once()

def test_update_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_resource_policy
    mock_client = MagicMock()
    mock_client.update_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_resource_policy("test-resource_arn", "{}", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.update_resource_policy.assert_called_once()

def test_update_slot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_slot
    mock_client = MagicMock()
    mock_client.update_slot.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_slot("test-slot_id", "test-slot_name", "test-value_elicitation_setting", "test-bot_id", "test-bot_version", "test-locale_id", "test-intent_id", description="test-description", slot_type_id="test-slot_type_id", obfuscation_setting="test-obfuscation_setting", multiple_values_setting=True, sub_slot_setting="test-sub_slot_setting", region_name="us-east-1")
    mock_client.update_slot.assert_called_once()

def test_update_slot_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_slot_type
    mock_client = MagicMock()
    mock_client.update_slot_type.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_slot_type("test-slot_type_id", "test-slot_type_name", "test-bot_id", "test-bot_version", "test-locale_id", description="test-description", slot_type_values="test-slot_type_values", value_selection_setting="test-value_selection_setting", parent_slot_type_signature="test-parent_slot_type_signature", external_source_setting="test-external_source_setting", composite_slot_type_setting="test-composite_slot_type_setting", region_name="us-east-1")
    mock_client.update_slot_type.assert_called_once()

def test_update_test_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lex_models import update_test_set
    mock_client = MagicMock()
    mock_client.update_test_set.return_value = {}
    monkeypatch.setattr("aws_util.lex_models.get_client", lambda *a, **kw: mock_client)
    update_test_set("test-run_set_id", "test-run_set_name", description="test-description", region_name="us-east-1")
    mock_client.update_test_set.assert_called_once()
