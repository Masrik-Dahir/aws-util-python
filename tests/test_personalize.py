"""Tests for aws_util.personalize module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

import aws_util.personalize as mod
from aws_util.personalize import (
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_dataset_group_info_model():
    dg = DatasetGroupInfo(
        dataset_group_arn="arn:dsg", name="test", status="ACTIVE"
    )
    assert dg.dataset_group_arn == "arn:dsg"
    assert dg.name == "test"
    assert dg.status == "ACTIVE"


def test_dataset_info_model():
    ds = DatasetInfo(
        dataset_arn="arn:ds", name="ds1",
        dataset_type="Interactions", status="ACTIVE",
    )
    assert ds.dataset_type == "Interactions"


def test_schema_info_model():
    si = SchemaInfo(schema_arn="arn:schema", name="s1")
    assert si.schema_arn == "arn:schema"


def test_solution_info_model():
    sol = SolutionInfo(
        solution_arn="arn:sol", name="sol1",
        recipe_arn="arn:recipe", status="ACTIVE",
    )
    assert sol.recipe_arn == "arn:recipe"


def test_solution_version_info_model():
    sv = SolutionVersionInfo(
        solution_version_arn="arn:sv", status="ACTIVE",
    )
    assert sv.failure_reason == ""


def test_campaign_info_model():
    ci = CampaignInfo(
        campaign_arn="arn:camp", name="camp1",
        solution_version_arn="arn:sv", min_provisioned_tps=2,
        status="ACTIVE",
    )
    assert ci.min_provisioned_tps == 2


def test_campaign_info_defaults():
    ci = CampaignInfo()
    assert ci.min_provisioned_tps == 1
    assert ci.status == ""


# ---------------------------------------------------------------------------
# create_dataset_group
# ---------------------------------------------------------------------------


def test_create_dataset_group_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_group.return_value = {
        "datasetGroupArn": "arn:aws:personalize:us-east-1:123:dataset-group/g1"
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_dataset_group("g1", region_name=REGION)
    assert isinstance(result, DatasetGroupInfo)
    assert "g1" in result.dataset_group_arn
    assert result.name == "g1"
    assert result.status == "CREATE PENDING"


def test_create_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "CreateDatasetGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_dataset_group failed"):
        create_dataset_group("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_dataset_group
# ---------------------------------------------------------------------------


def test_describe_dataset_group_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_group.return_value = {
        "datasetGroup": {
            "datasetGroupArn": "arn:dsg",
            "name": "grp",
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_dataset_group("arn:dsg", region_name=REGION)
    assert result.status == "ACTIVE"
    assert result.name == "grp"


def test_describe_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DescribeDatasetGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_dataset_group failed"):
        describe_dataset_group("arn:missing", region_name=REGION)


# ---------------------------------------------------------------------------
# list_dataset_groups
# ---------------------------------------------------------------------------


def test_list_dataset_groups_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_groups.return_value = {
        "datasetGroups": [
            {"datasetGroupArn": "arn:dsg1", "name": "g1", "status": "ACTIVE"},
            {"datasetGroupArn": "arn:dsg2", "name": "g2", "status": "ACTIVE"},
        ],
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = list_dataset_groups(region_name=REGION)
    assert len(result) == 2
    assert result[0].name == "g1"


def test_list_dataset_groups_paginated(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_groups.side_effect = [
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
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = list_dataset_groups(region_name=REGION)
    assert len(result) == 2


def test_list_dataset_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_groups.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}},
        "ListDatasetGroups",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_dataset_groups failed"):
        list_dataset_groups(region_name=REGION)


# ---------------------------------------------------------------------------
# create_dataset
# ---------------------------------------------------------------------------


def test_create_dataset_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {"datasetArn": "arn:ds1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_dataset(
        "ds1", "arn:dsg", "Interactions", "arn:schema", region_name=REGION
    )
    assert isinstance(result, DatasetInfo)
    assert result.dataset_arn == "arn:ds1"
    assert result.dataset_type == "Interactions"


def test_create_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "CreateDataset",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_dataset failed"):
        create_dataset("ds", "arn:dsg", "Items", "arn:s", region_name=REGION)


# ---------------------------------------------------------------------------
# create_schema
# ---------------------------------------------------------------------------


def test_create_schema_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_schema.return_value = {"schemaArn": "arn:schema1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_schema("s1", '{"type":"record"}', region_name=REGION)
    assert isinstance(result, SchemaInfo)
    assert result.schema_arn == "arn:schema1"


def test_create_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_schema.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "CreateSchema",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_schema failed"):
        create_schema("s", "{}", region_name=REGION)


# ---------------------------------------------------------------------------
# create_solution / describe_solution
# ---------------------------------------------------------------------------


def test_create_solution_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_solution.return_value = {"solutionArn": "arn:sol1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_solution(
        "sol1", "arn:dsg", "arn:recipe", region_name=REGION
    )
    assert isinstance(result, SolutionInfo)
    assert result.solution_arn == "arn:sol1"


def test_create_solution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_solution.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "CreateSolution",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_solution failed"):
        create_solution("sol", "arn:dsg", "arn:r", region_name=REGION)


def test_describe_solution_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution.return_value = {
        "solution": {
            "solutionArn": "arn:sol1",
            "name": "sol1",
            "recipeArn": "arn:recipe",
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_solution("arn:sol1", region_name=REGION)
    assert result.status == "ACTIVE"


def test_describe_solution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DescribeSolution",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_solution failed"):
        describe_solution("arn:missing", region_name=REGION)


# ---------------------------------------------------------------------------
# create_solution_version / describe_solution_version
# ---------------------------------------------------------------------------


def test_create_solution_version_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_solution_version.return_value = {
        "solutionVersionArn": "arn:sv1"
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_solution_version("arn:sol1", region_name=REGION)
    assert isinstance(result, SolutionVersionInfo)
    assert result.solution_version_arn == "arn:sv1"


def test_create_solution_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_solution_version.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "CreateSolutionVersion",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_solution_version failed"):
        create_solution_version("arn:missing", region_name=REGION)


def test_describe_solution_version_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution_version.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "ACTIVE",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_solution_version("arn:sv1", region_name=REGION)
    assert result.status == "ACTIVE"


def test_describe_solution_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution_version.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DescribeSolutionVersion",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(
        RuntimeError, match="describe_solution_version failed"
    ):
        describe_solution_version("arn:missing", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_solution_version
# ---------------------------------------------------------------------------


def test_wait_for_solution_version_active(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution_version.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "ACTIVE",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = wait_for_solution_version("arn:sv1", region_name=REGION)
    assert result.status == "ACTIVE"


def test_wait_for_solution_version_failed(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution_version.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "CREATE FAILED",
            "failureReason": "Insufficient data",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Solution version failed"):
        wait_for_solution_version("arn:sv1", region_name=REGION)


def test_wait_for_solution_version_timeout(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_solution_version.return_value = {
        "solutionVersion": {
            "solutionVersionArn": "arn:sv1",
            "status": "CREATE IN_PROGRESS",
            "failureReason": "",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(TimeoutError, match="did not become ACTIVE"):
        wait_for_solution_version(
            "arn:sv1", timeout=0.0, poll_interval=0.0, region_name=REGION
        )


def test_wait_for_solution_version_poll_then_active(monkeypatch):
    """Cover the sleep branch: first poll returns in-progress, second ACTIVE."""
    mock_client = MagicMock()
    mock_client.describe_solution_version.side_effect = [
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
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    monkeypatch.setattr(mod._time, "sleep", lambda s: None)
    result = wait_for_solution_version(
        "arn:sv1", timeout=600, poll_interval=1.0, region_name=REGION
    )
    assert result.status == "ACTIVE"


# ---------------------------------------------------------------------------
# create_campaign / describe_campaign / update_campaign / delete_campaign
# ---------------------------------------------------------------------------


def test_create_campaign_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_campaign.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = create_campaign(
        "camp1", "arn:sv1", min_provisioned_tps=5, region_name=REGION
    )
    assert isinstance(result, CampaignInfo)
    assert result.campaign_arn == "arn:camp1"
    assert result.min_provisioned_tps == 5


def test_create_campaign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_campaign.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "CreateCampaign",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_campaign failed"):
        create_campaign("c", "arn:sv", region_name=REGION)


def test_describe_campaign_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_campaign.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_campaign("arn:camp1", region_name=REGION)
    assert result.status == "ACTIVE"


def test_describe_campaign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_campaign.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DescribeCampaign",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_campaign failed"):
        describe_campaign("arn:missing", region_name=REGION)


def test_update_campaign_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_campaign.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = update_campaign(
        "arn:camp1",
        solution_version_arn="arn:sv2",
        min_provisioned_tps=10,
        region_name=REGION,
    )
    assert result.status == "UPDATE PENDING"


def test_update_campaign_no_optionals(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_campaign.return_value = {"campaignArn": "arn:camp1"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = update_campaign("arn:camp1", region_name=REGION)
    assert result.campaign_arn == "arn:camp1"


def test_update_campaign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_campaign.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "UpdateCampaign",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="update_campaign failed"):
        update_campaign("arn:c", region_name=REGION)


def test_delete_campaign_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_campaign.return_value = {}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    delete_campaign("arn:camp1", region_name=REGION)
    mock_client.delete_campaign.assert_called_once()


def test_delete_campaign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_campaign.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DeleteCampaign",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_campaign failed"):
        delete_campaign("arn:missing", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_campaign
# ---------------------------------------------------------------------------


def test_wait_for_campaign_active(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_campaign.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    result = wait_for_campaign("arn:camp1", region_name=REGION)
    assert result.status == "ACTIVE"


def test_wait_for_campaign_failed(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_campaign.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "CREATE FAILED",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Campaign.*failed"):
        wait_for_campaign("arn:camp1", region_name=REGION)


def test_wait_for_campaign_timeout(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_campaign.return_value = {
        "campaign": {
            "campaignArn": "arn:camp1",
            "name": "camp1",
            "solutionVersionArn": "arn:sv1",
            "minProvisionedTPS": 1,
            "status": "CREATE IN_PROGRESS",
        }
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(TimeoutError, match="did not become ACTIVE"):
        wait_for_campaign(
            "arn:camp1", timeout=0.0, poll_interval=0.0, region_name=REGION
        )


def test_wait_for_campaign_poll_then_active(monkeypatch):
    """Cover the sleep branch: first poll returns in-progress, second ACTIVE."""
    mock_client = MagicMock()
    mock_client.describe_campaign.side_effect = [
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
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    monkeypatch.setattr(mod._time, "sleep", lambda s: None)
    result = wait_for_campaign(
        "arn:camp1", timeout=600, poll_interval=1.0, region_name=REGION
    )
    assert result.status == "ACTIVE"


def test_create_batch_inference_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_inference_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_batch_inference_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", region_name=REGION)
    mock_client.create_batch_inference_job.assert_called_once()


def test_create_batch_inference_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_inference_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_batch_inference_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create batch inference job"):
        create_batch_inference_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", region_name=REGION)


def test_create_batch_segment_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_segment_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_batch_segment_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", region_name=REGION)
    mock_client.create_batch_segment_job.assert_called_once()


def test_create_batch_segment_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_segment_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_batch_segment_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create batch segment job"):
        create_batch_segment_job("test-job_name", "test-solution_version_arn", {}, {}, "test-role_arn", region_name=REGION)


def test_create_data_deletion_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_deletion_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_data_deletion_job("test-job_name", "test-dataset_group_arn", {}, "test-role_arn", region_name=REGION)
    mock_client.create_data_deletion_job.assert_called_once()


def test_create_data_deletion_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_deletion_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_deletion_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create data deletion job"):
        create_data_deletion_job("test-job_name", "test-dataset_group_arn", {}, "test-role_arn", region_name=REGION)


def test_create_dataset_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_export_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", {}, region_name=REGION)
    mock_client.create_dataset_export_job.assert_called_once()


def test_create_dataset_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dataset_export_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dataset export job"):
        create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", {}, region_name=REGION)


def test_create_dataset_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_import_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_dataset_import_job("test-job_name", "test-dataset_arn", {}, "test-role_arn", region_name=REGION)
    mock_client.create_dataset_import_job.assert_called_once()


def test_create_dataset_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dataset_import_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dataset import job"):
        create_dataset_import_job("test-job_name", "test-dataset_arn", {}, "test-role_arn", region_name=REGION)


def test_create_event_tracker(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_tracker.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_event_tracker("test-name", "test-dataset_group_arn", region_name=REGION)
    mock_client.create_event_tracker.assert_called_once()


def test_create_event_tracker_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_tracker.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_tracker",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create event tracker"):
        create_event_tracker("test-name", "test-dataset_group_arn", region_name=REGION)


def test_create_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_filter.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", region_name=REGION)
    mock_client.create_filter.assert_called_once()


def test_create_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_filter",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create filter"):
        create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", region_name=REGION)


def test_create_metric_attribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_metric_attribution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_metric_attribution("test-name", "test-dataset_group_arn", [], {}, region_name=REGION)
    mock_client.create_metric_attribution.assert_called_once()


def test_create_metric_attribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_metric_attribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_metric_attribution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create metric attribution"):
        create_metric_attribution("test-name", "test-dataset_group_arn", [], {}, region_name=REGION)


def test_create_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", region_name=REGION)
    mock_client.create_recommender.assert_called_once()


def test_create_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create recommender"):
        create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", region_name=REGION)


def test_delete_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_dataset("test-dataset_arn", region_name=REGION)
    mock_client.delete_dataset.assert_called_once()


def test_delete_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset"):
        delete_dataset("test-dataset_arn", region_name=REGION)


def test_delete_dataset_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_group.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_dataset_group("test-dataset_group_arn", region_name=REGION)
    mock_client.delete_dataset_group.assert_called_once()


def test_delete_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset_group",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset group"):
        delete_dataset_group("test-dataset_group_arn", region_name=REGION)


def test_delete_event_tracker(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_tracker.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_event_tracker("test-event_tracker_arn", region_name=REGION)
    mock_client.delete_event_tracker.assert_called_once()


def test_delete_event_tracker_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_tracker.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_tracker",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete event tracker"):
        delete_event_tracker("test-event_tracker_arn", region_name=REGION)


def test_delete_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_filter.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_filter("test-filter_arn", region_name=REGION)
    mock_client.delete_filter.assert_called_once()


def test_delete_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_filter",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete filter"):
        delete_filter("test-filter_arn", region_name=REGION)


def test_delete_metric_attribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_metric_attribution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_metric_attribution("test-metric_attribution_arn", region_name=REGION)
    mock_client.delete_metric_attribution.assert_called_once()


def test_delete_metric_attribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_metric_attribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_metric_attribution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete metric attribution"):
        delete_metric_attribution("test-metric_attribution_arn", region_name=REGION)


def test_delete_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_recommender("test-recommender_arn", region_name=REGION)
    mock_client.delete_recommender.assert_called_once()


def test_delete_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete recommender"):
        delete_recommender("test-recommender_arn", region_name=REGION)


def test_delete_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_schema("test-schema_arn", region_name=REGION)
    mock_client.delete_schema.assert_called_once()


def test_delete_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_schema",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete schema"):
        delete_schema("test-schema_arn", region_name=REGION)


def test_delete_solution(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_solution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    delete_solution("test-solution_arn", region_name=REGION)
    mock_client.delete_solution.assert_called_once()


def test_delete_solution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_solution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_solution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete solution"):
        delete_solution("test-solution_arn", region_name=REGION)


def test_describe_algorithm(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_algorithm.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_algorithm("test-algorithm_arn", region_name=REGION)
    mock_client.describe_algorithm.assert_called_once()


def test_describe_algorithm_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_algorithm.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_algorithm",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe algorithm"):
        describe_algorithm("test-algorithm_arn", region_name=REGION)


def test_describe_batch_inference_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_inference_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_batch_inference_job("test-batch_inference_job_arn", region_name=REGION)
    mock_client.describe_batch_inference_job.assert_called_once()


def test_describe_batch_inference_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_inference_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_batch_inference_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe batch inference job"):
        describe_batch_inference_job("test-batch_inference_job_arn", region_name=REGION)


def test_describe_batch_segment_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_segment_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_batch_segment_job("test-batch_segment_job_arn", region_name=REGION)
    mock_client.describe_batch_segment_job.assert_called_once()


def test_describe_batch_segment_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_segment_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_batch_segment_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe batch segment job"):
        describe_batch_segment_job("test-batch_segment_job_arn", region_name=REGION)


def test_describe_data_deletion_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_deletion_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_data_deletion_job("test-data_deletion_job_arn", region_name=REGION)
    mock_client.describe_data_deletion_job.assert_called_once()


def test_describe_data_deletion_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_deletion_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_deletion_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data deletion job"):
        describe_data_deletion_job("test-data_deletion_job_arn", region_name=REGION)


def test_describe_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_dataset("test-dataset_arn", region_name=REGION)
    mock_client.describe_dataset.assert_called_once()


def test_describe_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        describe_dataset("test-dataset_arn", region_name=REGION)


def test_describe_dataset_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_export_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_dataset_export_job("test-dataset_export_job_arn", region_name=REGION)
    mock_client.describe_dataset_export_job.assert_called_once()


def test_describe_dataset_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset_export_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset export job"):
        describe_dataset_export_job("test-dataset_export_job_arn", region_name=REGION)


def test_describe_dataset_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_import_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_dataset_import_job("test-dataset_import_job_arn", region_name=REGION)
    mock_client.describe_dataset_import_job.assert_called_once()


def test_describe_dataset_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset_import_job",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset import job"):
        describe_dataset_import_job("test-dataset_import_job_arn", region_name=REGION)


def test_describe_event_tracker(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_tracker.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_event_tracker("test-event_tracker_arn", region_name=REGION)
    mock_client.describe_event_tracker.assert_called_once()


def test_describe_event_tracker_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_tracker.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_tracker",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event tracker"):
        describe_event_tracker("test-event_tracker_arn", region_name=REGION)


def test_describe_feature_transformation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_feature_transformation.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_feature_transformation("test-feature_transformation_arn", region_name=REGION)
    mock_client.describe_feature_transformation.assert_called_once()


def test_describe_feature_transformation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_feature_transformation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_feature_transformation",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe feature transformation"):
        describe_feature_transformation("test-feature_transformation_arn", region_name=REGION)


def test_describe_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_filter.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_filter("test-filter_arn", region_name=REGION)
    mock_client.describe_filter.assert_called_once()


def test_describe_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_filter",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe filter"):
        describe_filter("test-filter_arn", region_name=REGION)


def test_describe_metric_attribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_metric_attribution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_metric_attribution("test-metric_attribution_arn", region_name=REGION)
    mock_client.describe_metric_attribution.assert_called_once()


def test_describe_metric_attribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_metric_attribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metric_attribution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe metric attribution"):
        describe_metric_attribution("test-metric_attribution_arn", region_name=REGION)


def test_describe_recipe(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_recipe.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_recipe("test-recipe_arn", region_name=REGION)
    mock_client.describe_recipe.assert_called_once()


def test_describe_recipe_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_recipe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_recipe",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe recipe"):
        describe_recipe("test-recipe_arn", region_name=REGION)


def test_describe_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_recommender("test-recommender_arn", region_name=REGION)
    mock_client.describe_recommender.assert_called_once()


def test_describe_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe recommender"):
        describe_recommender("test-recommender_arn", region_name=REGION)


def test_describe_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_schema.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    describe_schema("test-schema_arn", region_name=REGION)
    mock_client.describe_schema.assert_called_once()


def test_describe_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_schema",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe schema"):
        describe_schema("test-schema_arn", region_name=REGION)


def test_get_solution_metrics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_solution_metrics.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    get_solution_metrics("test-solution_version_arn", region_name=REGION)
    mock_client.get_solution_metrics.assert_called_once()


def test_get_solution_metrics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_solution_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_solution_metrics",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get solution metrics"):
        get_solution_metrics("test-solution_version_arn", region_name=REGION)


def test_list_batch_inference_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_inference_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_batch_inference_jobs(region_name=REGION)
    mock_client.list_batch_inference_jobs.assert_called_once()


def test_list_batch_inference_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_inference_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_batch_inference_jobs",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list batch inference jobs"):
        list_batch_inference_jobs(region_name=REGION)


def test_list_batch_segment_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_segment_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_batch_segment_jobs(region_name=REGION)
    mock_client.list_batch_segment_jobs.assert_called_once()


def test_list_batch_segment_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_segment_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_batch_segment_jobs",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list batch segment jobs"):
        list_batch_segment_jobs(region_name=REGION)


def test_list_campaigns(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_campaigns.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_campaigns(region_name=REGION)
    mock_client.list_campaigns.assert_called_once()


def test_list_campaigns_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_campaigns.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_campaigns",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list campaigns"):
        list_campaigns(region_name=REGION)


def test_list_data_deletion_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_deletion_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_data_deletion_jobs(region_name=REGION)
    mock_client.list_data_deletion_jobs.assert_called_once()


def test_list_data_deletion_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_deletion_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_deletion_jobs",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data deletion jobs"):
        list_data_deletion_jobs(region_name=REGION)


def test_list_dataset_export_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_dataset_export_jobs(region_name=REGION)
    mock_client.list_dataset_export_jobs.assert_called_once()


def test_list_dataset_export_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_export_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_export_jobs",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset export jobs"):
        list_dataset_export_jobs(region_name=REGION)


def test_list_dataset_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_dataset_import_jobs(region_name=REGION)
    mock_client.list_dataset_import_jobs.assert_called_once()


def test_list_dataset_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_import_jobs",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset import jobs"):
        list_dataset_import_jobs(region_name=REGION)


def test_list_datasets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_datasets.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_datasets(region_name=REGION)
    mock_client.list_datasets.assert_called_once()


def test_list_datasets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_datasets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_datasets",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list datasets"):
        list_datasets(region_name=REGION)


def test_list_event_trackers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_trackers.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_event_trackers(region_name=REGION)
    mock_client.list_event_trackers.assert_called_once()


def test_list_event_trackers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_trackers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_event_trackers",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list event trackers"):
        list_event_trackers(region_name=REGION)


def test_list_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_filters.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_filters(region_name=REGION)
    mock_client.list_filters.assert_called_once()


def test_list_filters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_filters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_filters",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list filters"):
        list_filters(region_name=REGION)


def test_list_metric_attribution_metrics(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_metric_attribution_metrics.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_metric_attribution_metrics(region_name=REGION)
    mock_client.list_metric_attribution_metrics.assert_called_once()


def test_list_metric_attribution_metrics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_metric_attribution_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_metric_attribution_metrics",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list metric attribution metrics"):
        list_metric_attribution_metrics(region_name=REGION)


def test_list_metric_attributions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_metric_attributions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_metric_attributions(region_name=REGION)
    mock_client.list_metric_attributions.assert_called_once()


def test_list_metric_attributions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_metric_attributions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_metric_attributions",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list metric attributions"):
        list_metric_attributions(region_name=REGION)


def test_list_recipes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recipes.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_recipes(region_name=REGION)
    mock_client.list_recipes.assert_called_once()


def test_list_recipes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recipes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recipes",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list recipes"):
        list_recipes(region_name=REGION)


def test_list_recommenders(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommenders.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_recommenders(region_name=REGION)
    mock_client.list_recommenders.assert_called_once()


def test_list_recommenders_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommenders.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recommenders",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list recommenders"):
        list_recommenders(region_name=REGION)


def test_list_schemas(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_schemas(region_name=REGION)
    mock_client.list_schemas.assert_called_once()


def test_list_schemas_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_schemas",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list schemas"):
        list_schemas(region_name=REGION)


def test_list_solution_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_solution_versions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_solution_versions(region_name=REGION)
    mock_client.list_solution_versions.assert_called_once()


def test_list_solution_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_solution_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_solution_versions",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list solution versions"):
        list_solution_versions(region_name=REGION)


def test_list_solutions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_solutions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_solutions(region_name=REGION)
    mock_client.list_solutions.assert_called_once()


def test_list_solutions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_solutions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_solutions",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list solutions"):
        list_solutions(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_start_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    start_recommender("test-recommender_arn", region_name=REGION)
    mock_client.start_recommender.assert_called_once()


def test_start_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start recommender"):
        start_recommender("test-recommender_arn", region_name=REGION)


def test_stop_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    stop_recommender("test-recommender_arn", region_name=REGION)
    mock_client.stop_recommender.assert_called_once()


def test_stop_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop recommender"):
        stop_recommender("test-recommender_arn", region_name=REGION)


def test_stop_solution_version_creation(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_solution_version_creation.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    stop_solution_version_creation("test-solution_version_arn", region_name=REGION)
    mock_client.stop_solution_version_creation.assert_called_once()


def test_stop_solution_version_creation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_solution_version_creation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_solution_version_creation",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop solution version creation"):
        stop_solution_version_creation("test-solution_version_arn", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_dataset("test-dataset_arn", "test-schema_arn", region_name=REGION)
    mock_client.update_dataset.assert_called_once()


def test_update_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dataset",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dataset"):
        update_dataset("test-dataset_arn", "test-schema_arn", region_name=REGION)


def test_update_metric_attribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_metric_attribution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_metric_attribution(region_name=REGION)
    mock_client.update_metric_attribution.assert_called_once()


def test_update_metric_attribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_metric_attribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_metric_attribution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update metric attribution"):
        update_metric_attribution(region_name=REGION)


def test_update_recommender(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_recommender("test-recommender_arn", {}, region_name=REGION)
    mock_client.update_recommender.assert_called_once()


def test_update_recommender_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_recommender.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_recommender",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update recommender"):
        update_recommender("test-recommender_arn", {}, region_name=REGION)


def test_update_solution(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_solution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_solution("test-solution_arn", region_name=REGION)
    mock_client.update_solution.assert_called_once()


def test_update_solution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_solution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_solution",
    )
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update solution"):
        update_solution("test-solution_arn", region_name=REGION)


def test_update_campaign_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import update_campaign
    mock_client = MagicMock()
    mock_client.update_campaign.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_campaign("test-campaign_arn", solution_version_arn="test-solution_version_arn", min_provisioned_tps="test-min_provisioned_tps", region_name="us-east-1")
    mock_client.update_campaign.assert_called_once()

def test_create_batch_inference_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_batch_inference_job
    mock_client = MagicMock()
    mock_client.create_batch_inference_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_batch_inference_job("test-job_name", "test-solution_version_arn", "test-job_input", "test-job_output", "test-role_arn", filter_arn="test-filter_arn", num_results="test-num_results", batch_inference_job_config={}, tags=[{"Key": "k", "Value": "v"}], batch_inference_job_mode="test-batch_inference_job_mode", theme_generation_config={}, region_name="us-east-1")
    mock_client.create_batch_inference_job.assert_called_once()

def test_create_batch_segment_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_batch_segment_job
    mock_client = MagicMock()
    mock_client.create_batch_segment_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_batch_segment_job("test-job_name", "test-solution_version_arn", "test-job_input", "test-job_output", "test-role_arn", filter_arn="test-filter_arn", num_results="test-num_results", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_batch_segment_job.assert_called_once()

def test_create_data_deletion_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_data_deletion_job
    mock_client = MagicMock()
    mock_client.create_data_deletion_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_data_deletion_job("test-job_name", "test-dataset_group_arn", "test-data_source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_data_deletion_job.assert_called_once()

def test_create_dataset_export_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_dataset_export_job
    mock_client = MagicMock()
    mock_client.create_dataset_export_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_dataset_export_job("test-job_name", "test-dataset_arn", "test-role_arn", "test-job_output", ingestion_mode="test-ingestion_mode", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dataset_export_job.assert_called_once()

def test_create_dataset_import_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_dataset_import_job
    mock_client = MagicMock()
    mock_client.create_dataset_import_job.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_dataset_import_job("test-job_name", "test-dataset_arn", "test-data_source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], import_mode=1, publish_attribution_metrics_to_s3=True, region_name="us-east-1")
    mock_client.create_dataset_import_job.assert_called_once()

def test_create_event_tracker_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_event_tracker
    mock_client = MagicMock()
    mock_client.create_event_tracker.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_event_tracker("test-name", "test-dataset_group_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_tracker.assert_called_once()

def test_create_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_filter
    mock_client = MagicMock()
    mock_client.create_filter.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_filter("test-name", "test-dataset_group_arn", "test-filter_expression", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_filter.assert_called_once()

def test_create_recommender_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import create_recommender
    mock_client = MagicMock()
    mock_client.create_recommender.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    create_recommender("test-name", "test-dataset_group_arn", "test-recipe_arn", recommender_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_recommender.assert_called_once()

def test_list_batch_inference_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_batch_inference_jobs
    mock_client = MagicMock()
    mock_client.list_batch_inference_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_batch_inference_jobs(solution_version_arn="test-solution_version_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_batch_inference_jobs.assert_called_once()

def test_list_batch_segment_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_batch_segment_jobs
    mock_client = MagicMock()
    mock_client.list_batch_segment_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_batch_segment_jobs(solution_version_arn="test-solution_version_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_batch_segment_jobs.assert_called_once()

def test_list_campaigns_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_campaigns
    mock_client = MagicMock()
    mock_client.list_campaigns.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_campaigns(solution_arn="test-solution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_campaigns.assert_called_once()

def test_list_data_deletion_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_data_deletion_jobs
    mock_client = MagicMock()
    mock_client.list_data_deletion_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_data_deletion_jobs(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_data_deletion_jobs.assert_called_once()

def test_list_dataset_export_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_dataset_export_jobs
    mock_client = MagicMock()
    mock_client.list_dataset_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_dataset_export_jobs(dataset_arn="test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dataset_export_jobs.assert_called_once()

def test_list_dataset_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_dataset_import_jobs
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_dataset_import_jobs(dataset_arn="test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dataset_import_jobs.assert_called_once()

def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_datasets
    mock_client = MagicMock()
    mock_client.list_datasets.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_datasets(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_datasets.assert_called_once()

def test_list_event_trackers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_event_trackers
    mock_client = MagicMock()
    mock_client.list_event_trackers.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_event_trackers(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_event_trackers.assert_called_once()

def test_list_filters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_filters
    mock_client = MagicMock()
    mock_client.list_filters.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_filters(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_filters.assert_called_once()

def test_list_metric_attribution_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_metric_attribution_metrics
    mock_client = MagicMock()
    mock_client.list_metric_attribution_metrics.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_metric_attribution_metrics(metric_attribution_arn="test-metric_attribution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_metric_attribution_metrics.assert_called_once()

def test_list_metric_attributions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_metric_attributions
    mock_client = MagicMock()
    mock_client.list_metric_attributions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_metric_attributions(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_metric_attributions.assert_called_once()

def test_list_recipes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_recipes
    mock_client = MagicMock()
    mock_client.list_recipes.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_recipes(recipe_provider="test-recipe_provider", next_token="test-next_token", max_results=1, domain="test-domain", region_name="us-east-1")
    mock_client.list_recipes.assert_called_once()

def test_list_recommenders_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_recommenders
    mock_client = MagicMock()
    mock_client.list_recommenders.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_recommenders(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_recommenders.assert_called_once()

def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_schemas
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_schemas(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_schemas.assert_called_once()

def test_list_solution_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_solution_versions
    mock_client = MagicMock()
    mock_client.list_solution_versions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_solution_versions(solution_arn="test-solution_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_solution_versions.assert_called_once()

def test_list_solutions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import list_solutions
    mock_client = MagicMock()
    mock_client.list_solutions.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    list_solutions(dataset_group_arn="test-dataset_group_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_solutions.assert_called_once()

def test_update_metric_attribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import update_metric_attribution
    mock_client = MagicMock()
    mock_client.update_metric_attribution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_metric_attribution(add_metrics="test-add_metrics", remove_metrics="test-remove_metrics", metrics_output_config={}, metric_attribution_arn="test-metric_attribution_arn", region_name="us-east-1")
    mock_client.update_metric_attribution.assert_called_once()

def test_update_solution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.personalize import update_solution
    mock_client = MagicMock()
    mock_client.update_solution.return_value = {}
    monkeypatch.setattr("aws_util.personalize.get_client", lambda *a, **kw: mock_client)
    update_solution("test-solution_arn", perform_auto_training="test-perform_auto_training", solution_update_config={}, region_name="us-east-1")
    mock_client.update_solution.assert_called_once()
