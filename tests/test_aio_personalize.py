"""Tests for aws_util.aio.personalize module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.personalize import (
    CampaignInfo,
    DatasetGroupInfo,
    DatasetInfo,
    SchemaInfo,
    SolutionInfo,
    SolutionVersionInfo,
    create_campaign,
    create_dataset,
    create_dataset_group,
    create_schema,
    create_solution,
    create_solution_version,
    delete_campaign,
    describe_campaign,
    describe_dataset_group,
    describe_solution,
    describe_solution_version,
    list_dataset_groups,
    update_campaign,
    wait_for_campaign,
    wait_for_solution_version,
    create_batch_inference_job,
    create_batch_segment_job,
    create_data_deletion_job,
    create_dataset_export_job,
    create_dataset_import_job,
    create_event_tracker,
    create_filter,
    create_metric_attribution,
    create_recommender,
    delete_dataset,
    delete_dataset_group,
    delete_event_tracker,
    delete_filter,
    delete_metric_attribution,
    delete_recommender,
    delete_schema,
    delete_solution,
    describe_algorithm,
    describe_batch_inference_job,
    describe_batch_segment_job,
    describe_data_deletion_job,
    describe_dataset,
    describe_dataset_export_job,
    describe_dataset_import_job,
    describe_event_tracker,
    describe_feature_transformation,
    describe_filter,
    describe_metric_attribution,
    describe_recipe,
    describe_recommender,
    describe_schema,
    get_solution_metrics,
    list_batch_inference_jobs,
    list_batch_segment_jobs,
    list_campaigns,
    list_data_deletion_jobs,
    list_dataset_export_jobs,
    list_dataset_import_jobs,
    list_datasets,
    list_event_trackers,
    list_filters,
    list_metric_attribution_metrics,
    list_metric_attributions,
    list_recipes,
    list_recommenders,
    list_schemas,
    list_solution_versions,
    list_solutions,
    list_tags_for_resource,
    start_recommender,
    stop_recommender,
    stop_solution_version_creation,
    tag_resource,
    untag_resource,
    update_dataset,
    update_metric_attribution,
    update_recommender,
    update_solution,
)


# ---------------------------------------------------------------------------
# create_dataset_group
# ---------------------------------------------------------------------------


async def test_create_dataset_group_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"datasetGroupArn": "arn:dsg1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_dataset_group("g1")
    assert isinstance(result, DatasetGroupInfo)
    assert result.dataset_group_arn == "arn:dsg1"
    assert result.status == "CREATE PENDING"


async def test_create_dataset_group_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_dataset_group failed"):
        await create_dataset_group("g1")


# ---------------------------------------------------------------------------
# describe_dataset_group
# ---------------------------------------------------------------------------


async def test_describe_dataset_group_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "datasetGroup": {
            "datasetGroupArn": "arn:dsg",
            "name": "grp",
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_dataset_group("arn:dsg")
    assert result.status == "ACTIVE"


async def test_describe_dataset_group_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_dataset_group failed"):
        await describe_dataset_group("arn:dsg")


# ---------------------------------------------------------------------------
# list_dataset_groups
# ---------------------------------------------------------------------------


async def test_list_dataset_groups_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "datasetGroups": [
            {"datasetGroupArn": "arn:1", "name": "g1", "status": "ACTIVE"},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_dataset_groups()
    assert len(result) == 1
    assert result[0].name == "g1"


async def test_list_dataset_groups_paginated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "datasetGroups": [
                {"datasetGroupArn": "arn:1", "name": "p1", "status": "ACTIVE"},
            ],
            "nextToken": "tok",
        },
        {
            "datasetGroups": [
                {"datasetGroupArn": "arn:2", "name": "p2", "status": "ACTIVE"},
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_dataset_groups()
    assert len(result) == 2


async def test_list_dataset_groups_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_dataset_groups failed"):
        await list_dataset_groups()


# ---------------------------------------------------------------------------
# create_dataset
# ---------------------------------------------------------------------------


async def test_create_dataset_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"datasetArn": "arn:ds1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_dataset(
        "ds1", "arn:dsg", "Interactions", "arn:schema"
    )
    assert isinstance(result, DatasetInfo)
    assert result.dataset_arn == "arn:ds1"


async def test_create_dataset_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_dataset failed"):
        await create_dataset("ds", "arn:dsg", "Items", "arn:s")


# ---------------------------------------------------------------------------
# create_schema
# ---------------------------------------------------------------------------


async def test_create_schema_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"schemaArn": "arn:schema1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_schema("s1", '{"type":"record"}')
    assert isinstance(result, SchemaInfo)
    assert result.schema_arn == "arn:schema1"


async def test_create_schema_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_schema failed"):
        await create_schema("s", "{}")


# ---------------------------------------------------------------------------
# create_solution / describe_solution
# ---------------------------------------------------------------------------


async def test_create_solution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"solutionArn": "arn:sol1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_solution("sol1", "arn:dsg", "arn:recipe")
    assert isinstance(result, SolutionInfo)
    assert result.solution_arn == "arn:sol1"


async def test_create_solution_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_solution failed"):
        await create_solution("sol", "arn:dsg", "arn:r")


async def test_describe_solution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "solution": {
            "solutionArn": "arn:sol1",
            "name": "sol1",
            "recipeArn": "arn:recipe",
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_solution("arn:sol1")
    assert result.status == "ACTIVE"


async def test_describe_solution_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_solution failed"):
        await describe_solution("arn:sol")


# ---------------------------------------------------------------------------
# create_solution_version / describe_solution_version
# ---------------------------------------------------------------------------


async def test_create_solution_version_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"solutionVersionArn": "arn:sv1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_solution_version("arn:sol1")
    assert isinstance(result, SolutionVersionInfo)
    assert result.solution_version_arn == "arn:sv1"


async def test_create_solution_version_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_solution_version failed"):
        await create_solution_version("arn:sol")


async def test_describe_solution_version_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "ACTIVE",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_solution_version("arn:sv1")
    assert result.status == "ACTIVE"


async def test_describe_solution_version_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="describe_solution_version failed"
    ):
        await describe_solution_version("arn:sv")


# ---------------------------------------------------------------------------
# wait_for_solution_version
# ---------------------------------------------------------------------------


async def test_wait_for_solution_version_active(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "ACTIVE",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await wait_for_solution_version("arn:sv1")
    assert result.status == "ACTIVE"


async def test_wait_for_solution_version_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "CREATE FAILED",
            "failureReason": "Insufficient data",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Solution version failed"):
        await wait_for_solution_version("arn:sv1")


async def test_wait_for_solution_version_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "CREATE IN_PROGRESS",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(TimeoutError, match="did not become ACTIVE"):
        await wait_for_solution_version(
            "arn:sv1", timeout=0.0, poll_interval=0.0
        )


async def test_wait_for_solution_version_poll_then_active(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover the sleep branch: first poll in-progress, second ACTIVE."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "solutionVersion": {
                "solutionVersionArn": "arn:sv1",
                "status": "CREATE IN_PROGRESS",
                "failureReason": "",
            }
        },
        {
            "solutionVersion": {
                "solutionVersionArn": "arn:sv1",
                "status": "ACTIVE",
                "failureReason": "",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_solution_version(
        "arn:sv1", timeout=600, poll_interval=1.0
    )
    assert result.status == "ACTIVE"


# ---------------------------------------------------------------------------
# create_campaign / describe_campaign / update_campaign / delete_campaign
# ---------------------------------------------------------------------------


async def test_create_campaign_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_campaign("camp1", "arn:sv1", min_provisioned_tps=5)
    assert isinstance(result, CampaignInfo)
    assert result.campaign_arn == "arn:camp1"
    assert result.min_provisioned_tps == 5


async def test_create_campaign_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_campaign failed"):
        await create_campaign("c", "arn:sv")


async def test_describe_campaign_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_campaign("arn:camp1")
    assert result.status == "ACTIVE"


async def test_describe_campaign_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_campaign failed"):
        await describe_campaign("arn:camp")


async def test_update_campaign_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_campaign(
        "arn:camp1",
        solution_version_arn="arn:sv2",
        min_provisioned_tps=10,
    )
    assert result.status == "UPDATE PENDING"


async def test_update_campaign_no_optionals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_campaign("arn:camp1")
    assert result.campaign_arn == "arn:camp1"


async def test_update_campaign_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="update_campaign failed"):
        await update_campaign("arn:camp")


async def test_delete_campaign_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_campaign("arn:camp1")


async def test_delete_campaign_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_campaign failed"):
        await delete_campaign("arn:camp")


# ---------------------------------------------------------------------------
# wait_for_campaign
# ---------------------------------------------------------------------------


async def test_wait_for_campaign_active(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await wait_for_campaign("arn:camp1")
    assert result.status == "ACTIVE"


async def test_wait_for_campaign_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "CREATE FAILED",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Campaign.*failed"):
        await wait_for_campaign("arn:camp1")


async def test_wait_for_campaign_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "CREATE IN_PROGRESS",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(TimeoutError, match="did not become ACTIVE"):
        await wait_for_campaign(
            "arn:camp1", timeout=0.0, poll_interval=0.0
        )


async def test_wait_for_campaign_poll_then_active(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cover the sleep branch: first poll in-progress, second ACTIVE."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "campaign": {
                "campaignArn": "arn:camp1",
                "name": "camp1",
                "solutionVersionArn": "arn:sv1",
                "minProvisionedTPS": 1,
                "status": "CREATE IN_PROGRESS",
            }
        },
        {
            "campaign": {
                "campaignArn": "arn:camp1",
                "name": "camp1",
                "solutionVersionArn": "arn:sv1",
                "minProvisionedTPS": 1,
                "status": "ACTIVE",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_campaign(
        "arn:camp1", timeout=600, poll_interval=1.0
    )
    assert result.status == "ACTIVE"


async def test_create_batch_inference_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_batch_inference_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_batch_inference_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_batch_inference_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", )


async def test_create_batch_segment_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_batch_segment_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_batch_segment_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_batch_segment_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", )


async def test_create_data_deletion_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_data_deletion_job("test-job_name", "test-dataset_group_arn", {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_data_deletion_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_deletion_job("test-job_name", "test-dataset_group_arn", {}, "test-role_arn", )


async def test_create_dataset_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_dataset_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", {}, )


async def test_create_dataset_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dataset_import_job("test-job_name", "test-dataset_arn", {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_dataset_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dataset_import_job("test-job_name", "test-dataset_arn", {}, "test-role_arn", )


async def test_create_event_tracker(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_tracker("test-name", "test-dataset_group_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_tracker_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_tracker("test-name", "test-dataset_group_arn", )


async def test_create_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", )
    mock_client.call.assert_called_once()


async def test_create_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", )


async def test_create_metric_attribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_metric_attribution("test-name", "test-dataset_group_arn", [], {}, )
    mock_client.call.assert_called_once()


async def test_create_metric_attribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_metric_attribution("test-name", "test-dataset_group_arn", [], {}, )


async def test_create_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", )
    mock_client.call.assert_called_once()


async def test_create_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", )


async def test_delete_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset("test-dataset_arn", )


async def test_delete_dataset_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset_group("test-dataset_group_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset_group("test-dataset_group_arn", )


async def test_delete_event_tracker(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_tracker("test-event_tracker_arn", )
    mock_client.call.assert_called_once()


async def test_delete_event_tracker_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_tracker("test-event_tracker_arn", )


async def test_delete_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_filter("test-filter_arn", )
    mock_client.call.assert_called_once()


async def test_delete_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_filter("test-filter_arn", )


async def test_delete_metric_attribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_metric_attribution("test-metric_attribution_arn", )
    mock_client.call.assert_called_once()


async def test_delete_metric_attribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_metric_attribution("test-metric_attribution_arn", )


async def test_delete_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_recommender("test-recommender_arn", )
    mock_client.call.assert_called_once()


async def test_delete_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_recommender("test-recommender_arn", )


async def test_delete_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_schema("test-schema_arn", )
    mock_client.call.assert_called_once()


async def test_delete_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_schema("test-schema_arn", )


async def test_delete_solution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_solution("test-solution_arn", )
    mock_client.call.assert_called_once()


async def test_delete_solution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_solution("test-solution_arn", )


async def test_describe_algorithm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_algorithm("test-algorithm_arn", )
    mock_client.call.assert_called_once()


async def test_describe_algorithm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_algorithm("test-algorithm_arn", )


async def test_describe_batch_inference_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_batch_inference_job("test-batch_inference_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_batch_inference_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_batch_inference_job("test-batch_inference_job_arn", )


async def test_describe_batch_segment_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_batch_segment_job("test-batch_segment_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_batch_segment_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_batch_segment_job("test-batch_segment_job_arn", )


async def test_describe_data_deletion_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_deletion_job("test-data_deletion_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_data_deletion_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_deletion_job("test-data_deletion_job_arn", )


async def test_describe_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset("test-dataset_arn", )


async def test_describe_dataset_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset_export_job("test-dataset_export_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset_export_job("test-dataset_export_job_arn", )


async def test_describe_dataset_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset_import_job("test-dataset_import_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset_import_job("test-dataset_import_job_arn", )


async def test_describe_event_tracker(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_tracker("test-event_tracker_arn", )
    mock_client.call.assert_called_once()


async def test_describe_event_tracker_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_tracker("test-event_tracker_arn", )


async def test_describe_feature_transformation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_feature_transformation("test-feature_transformation_arn", )
    mock_client.call.assert_called_once()


async def test_describe_feature_transformation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_feature_transformation("test-feature_transformation_arn", )


async def test_describe_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_filter("test-filter_arn", )
    mock_client.call.assert_called_once()


async def test_describe_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_filter("test-filter_arn", )


async def test_describe_metric_attribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metric_attribution("test-metric_attribution_arn", )
    mock_client.call.assert_called_once()


async def test_describe_metric_attribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metric_attribution("test-metric_attribution_arn", )


async def test_describe_recipe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_recipe("test-recipe_arn", )
    mock_client.call.assert_called_once()


async def test_describe_recipe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_recipe("test-recipe_arn", )


async def test_describe_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_recommender("test-recommender_arn", )
    mock_client.call.assert_called_once()


async def test_describe_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_recommender("test-recommender_arn", )


async def test_describe_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_schema("test-schema_arn", )
    mock_client.call.assert_called_once()


async def test_describe_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_schema("test-schema_arn", )


async def test_get_solution_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_solution_metrics("test-solution_version_arn", )
    mock_client.call.assert_called_once()


async def test_get_solution_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_solution_metrics("test-solution_version_arn", )


async def test_list_batch_inference_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_batch_inference_jobs()
    mock_client.call.assert_called_once()


async def test_list_batch_inference_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_batch_inference_jobs()


async def test_list_batch_segment_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_batch_segment_jobs()
    mock_client.call.assert_called_once()


async def test_list_batch_segment_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_batch_segment_jobs()


async def test_list_campaigns(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_campaigns()
    mock_client.call.assert_called_once()


async def test_list_campaigns_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_campaigns()


async def test_list_data_deletion_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_deletion_jobs()
    mock_client.call.assert_called_once()


async def test_list_data_deletion_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_deletion_jobs()


async def test_list_dataset_export_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_export_jobs()
    mock_client.call.assert_called_once()


async def test_list_dataset_export_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_export_jobs()


async def test_list_dataset_import_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_import_jobs()
    mock_client.call.assert_called_once()


async def test_list_dataset_import_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_import_jobs()


async def test_list_datasets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_datasets()
    mock_client.call.assert_called_once()


async def test_list_datasets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_datasets()


async def test_list_event_trackers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_event_trackers()
    mock_client.call.assert_called_once()


async def test_list_event_trackers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_event_trackers()


async def test_list_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_filters()
    mock_client.call.assert_called_once()


async def test_list_filters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_filters()


async def test_list_metric_attribution_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_metric_attribution_metrics()
    mock_client.call.assert_called_once()


async def test_list_metric_attribution_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_metric_attribution_metrics()


async def test_list_metric_attributions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_metric_attributions()
    mock_client.call.assert_called_once()


async def test_list_metric_attributions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_metric_attributions()


async def test_list_recipes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recipes()
    mock_client.call.assert_called_once()


async def test_list_recipes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recipes()


async def test_list_recommenders(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recommenders()
    mock_client.call.assert_called_once()


async def test_list_recommenders_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recommenders()


async def test_list_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_schemas()
    mock_client.call.assert_called_once()


async def test_list_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_schemas()


async def test_list_solution_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_solution_versions()
    mock_client.call.assert_called_once()


async def test_list_solution_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_solution_versions()


async def test_list_solutions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_solutions()
    mock_client.call.assert_called_once()


async def test_list_solutions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_solutions()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_start_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_recommender("test-recommender_arn", )
    mock_client.call.assert_called_once()


async def test_start_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_recommender("test-recommender_arn", )


async def test_stop_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_recommender("test-recommender_arn", )
    mock_client.call.assert_called_once()


async def test_stop_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_recommender("test-recommender_arn", )


async def test_stop_solution_version_creation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_solution_version_creation("test-solution_version_arn", )
    mock_client.call.assert_called_once()


async def test_stop_solution_version_creation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_solution_version_creation("test-solution_version_arn", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dataset("test-dataset_arn", "test-schema_arn", )
    mock_client.call.assert_called_once()


async def test_update_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dataset("test-dataset_arn", "test-schema_arn", )


async def test_update_metric_attribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_metric_attribution()
    mock_client.call.assert_called_once()


async def test_update_metric_attribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_metric_attribution()


async def test_update_recommender(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_recommender("test-recommender_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_recommender_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_recommender("test-recommender_arn", {}, )


async def test_update_solution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_solution("test-solution_arn", )
    mock_client.call.assert_called_once()


async def test_update_solution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.personalize.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_solution("test-solution_arn", )


@pytest.mark.asyncio
async def test_update_campaign_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import update_campaign
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await update_campaign("test-campaign_arn", solution_version_arn="test-solution_version_arn", min_provisioned_tps="test-min_provisioned_tps", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_batch_inference_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_batch_inference_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_batch_inference_job("test-job_name", "test-solution_version_arn", "test-job_input", "test-job_output", "test-role_arn", filter_arn="test-filter_arn", num_results="test-num_results", batch_inference_job_config={}, tags=[{"Key": "k", "Value": "v"}], batch_inference_job_mode="test-batch_inference_job_mode", theme_generation_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_batch_segment_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_batch_segment_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_batch_segment_job("test-job_name", "test-solution_version_arn", "test-job_input", "test-job_output", "test-role_arn", filter_arn="test-filter_arn", num_results="test-num_results", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_deletion_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_data_deletion_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_data_deletion_job("test-job_name", "test-dataset_group_arn", "test-data_source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_export_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_dataset_export_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", "test-job_output", ingestion_mode="test-ingestion_mode", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_import_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_dataset_import_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_dataset_import_job("test-job_name", "test-dataset_arn", "test-data_source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], import_mode=1, publish_attribution_metrics_to_s3=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_tracker_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_event_tracker
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_event_tracker("test-name", "test-dataset_group_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_recommender_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import create_recommender
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", recommender_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_batch_inference_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_batch_inference_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_batch_inference_jobs(solution_version_arn="test-solution_version_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_batch_segment_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_batch_segment_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_batch_segment_jobs(solution_version_arn="test-solution_version_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_campaigns_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_campaigns
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_campaigns(solution_arn="test-solution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_deletion_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_data_deletion_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_data_deletion_jobs(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_export_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_dataset_export_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_dataset_export_jobs(dataset_arn="test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_dataset_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_dataset_import_jobs(dataset_arn="test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_datasets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_datasets(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_event_trackers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_event_trackers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_event_trackers(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_filters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_filters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_filters(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_metric_attribution_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_metric_attribution_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_metric_attribution_metrics(metric_attribution_arn="test-metric_attribution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_metric_attributions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_metric_attributions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_metric_attributions(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recipes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_recipes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_recipes(recipe_provider="test-recipe_provider", next_token="test-next_token", max_results=1, domain="test-domain", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recommenders_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_recommenders
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_recommenders(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_schemas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_schemas(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_solution_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_solution_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_solution_versions(solution_arn="test-solution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_solutions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import list_solutions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await list_solutions(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_metric_attribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import update_metric_attribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await update_metric_attribution(add_metrics="test-add_metrics", remove_metrics="test-remove_metrics", metrics_output_config={}, metric_attribution_arn="test-metric_attribution_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_solution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.personalize import update_solution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.personalize.async_client", lambda *a, **kw: mock_client)
    await update_solution("test-solution_arn", perform_auto_training="test-perform_auto_training", solution_update_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()
