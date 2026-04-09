"""Tests for aws_util.codedeploy module."""
from __future__ import annotations

import time
import time as _time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.codedeploy as cd_mod
from aws_util.codedeploy import (
    ApplicationResult,
    DeploymentConfigResult,
    DeploymentGroupResult,
    DeploymentResult,
    RevisionResult,
    continue_deployment,
    create_application,
    create_deployment,
    create_deployment_config,
    create_deployment_group,
    delete_application,
    delete_deployment_group,
    deploy_and_wait,
    get_application,
    get_application_revision,
    get_deployment,
    get_deployment_config,
    get_deployment_group,
    list_application_revisions,
    list_applications,
    list_deployment_groups,
    list_deployments,
    register_application_revision,
    stop_deployment,
    wait_for_deployment,
    add_tags_to_on_premises_instances,
    batch_get_application_revisions,
    batch_get_applications,
    batch_get_deployment_groups,
    batch_get_deployment_instances,
    batch_get_deployment_targets,
    batch_get_deployments,
    batch_get_on_premises_instances,
    delete_deployment_config,
    delete_git_hub_account_token,
    delete_resources_by_external_id,
    deregister_on_premises_instance,
    get_deployment_instance,
    get_deployment_target,
    get_on_premises_instance,
    list_deployment_configs,
    list_deployment_instances,
    list_deployment_targets,
    list_git_hub_account_token_names,
    list_on_premises_instances,
    list_tags_for_resource,
    put_lifecycle_event_hook_execution_status,
    register_on_premises_instance,
    remove_tags_from_on_premises_instances,
    skip_wait_time_for_instance_termination,
    tag_resource,
    untag_resource,
    update_application,
    update_deployment_group,
)

REGION = "us-east-1"
APP_NAME = "test-app"
DG_NAME = "test-dg"
DEPLOYMENT_ID = "d-ABCDEF123"
ROLE_ARN = "arn:aws:iam::123456789012:role/CodeDeployRole"
CONFIG_NAME = "test-config"

_REVISION = {
    "revisionType": "S3",
    "s3Location": {
        "bucket": "my-bucket",
        "key": "app.zip",
        "bundleType": "zip",
    },
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_application_result_model():
    r = ApplicationResult(
        application_id="app-123",
        application_name=APP_NAME,
        compute_platform="Server",
    )
    assert r.application_name == APP_NAME
    assert r.compute_platform == "Server"


def test_application_result_defaults():
    r = ApplicationResult()
    assert r.application_id == ""
    assert r.application_name == ""
    assert r.compute_platform == ""
    assert r.create_time is None
    assert r.linked_to_github is False
    assert r.extra == {}


def test_deployment_group_result_model():
    r = DeploymentGroupResult(
        deployment_group_id="dg-123",
        deployment_group_name=DG_NAME,
        application_name=APP_NAME,
        service_role_arn=ROLE_ARN,
    )
    assert r.deployment_group_name == DG_NAME
    assert r.service_role_arn == ROLE_ARN


def test_deployment_group_result_defaults():
    r = DeploymentGroupResult()
    assert r.deployment_group_id == ""
    assert r.deployment_group_name == ""
    assert r.application_name == ""
    assert r.service_role_arn == ""
    assert r.deployment_config_name == ""
    assert r.compute_platform == ""
    assert r.extra == {}


def test_deployment_result_model():
    r = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        status="Succeeded",
        revision=_REVISION,
    )
    assert r.status == "Succeeded"
    assert r.deployment_id == DEPLOYMENT_ID


def test_deployment_result_defaults():
    r = DeploymentResult()
    assert r.deployment_id == ""
    assert r.application_name == ""
    assert r.deployment_group_name == ""
    assert r.status == ""
    assert r.revision == {}
    assert r.description == ""
    assert r.create_time is None
    assert r.complete_time is None
    assert r.extra == {}


def test_deployment_config_result_model():
    r = DeploymentConfigResult(
        deployment_config_id="cfg-123",
        deployment_config_name=CONFIG_NAME,
        compute_platform="Server",
        minimum_healthy_hosts={"type": "HOST_COUNT", "value": 1},
    )
    assert r.deployment_config_name == CONFIG_NAME


def test_deployment_config_result_defaults():
    r = DeploymentConfigResult()
    assert r.deployment_config_id == ""
    assert r.deployment_config_name == ""
    assert r.compute_platform == ""
    assert r.minimum_healthy_hosts == {}
    assert r.create_time is None
    assert r.extra == {}


def test_revision_result_model():
    r = RevisionResult(
        application_name=APP_NAME,
        revision=_REVISION,
        description="first revision",
    )
    assert r.application_name == APP_NAME
    assert r.description == "first revision"


def test_revision_result_defaults():
    r = RevisionResult()
    assert r.application_name == ""
    assert r.revision == {}
    assert r.description == ""
    assert r.register_time is None
    assert r.first_used_time is None
    assert r.last_used_time is None
    assert r.extra == {}


# ---------------------------------------------------------------------------
# _parse helpers
# ---------------------------------------------------------------------------


def test_parse_application():
    from aws_util.codedeploy import _parse_application

    result = _parse_application(
        {
            "applicationId": "app-1",
            "applicationName": APP_NAME,
            "computePlatform": "Lambda",
            "createTime": "2024-01-01",
            "linkedToGitHub": True,
            "customField": "value",
        }
    )
    assert result.application_id == "app-1"
    assert result.application_name == APP_NAME
    assert result.compute_platform == "Lambda"
    assert result.create_time == "2024-01-01"
    assert result.linked_to_github is True
    assert "customField" in result.extra


def test_parse_application_minimal():
    from aws_util.codedeploy import _parse_application

    result = _parse_application({})
    assert result.application_id == ""
    assert result.create_time is None


def test_parse_deployment_group():
    from aws_util.codedeploy import _parse_deployment_group

    result = _parse_deployment_group(
        {
            "deploymentGroupId": "dg-1",
            "deploymentGroupName": DG_NAME,
            "applicationName": APP_NAME,
            "serviceRoleArn": ROLE_ARN,
            "deploymentConfigName": CONFIG_NAME,
            "computePlatform": "Server",
            "customField": "val",
        }
    )
    assert result.deployment_group_id == "dg-1"
    assert "customField" in result.extra


def test_parse_deployment():
    from aws_util.codedeploy import _parse_deployment

    result = _parse_deployment(
        {
            "deploymentId": DEPLOYMENT_ID,
            "applicationName": APP_NAME,
            "deploymentGroupName": DG_NAME,
            "status": "Succeeded",
            "revision": _REVISION,
            "description": "test deploy",
            "createTime": "2024-01-01",
            "completeTime": "2024-01-02",
            "creator": "user",
        }
    )
    assert result.deployment_id == DEPLOYMENT_ID
    assert result.create_time == "2024-01-01"
    assert result.complete_time == "2024-01-02"
    assert "creator" in result.extra


def test_parse_deployment_minimal():
    from aws_util.codedeploy import _parse_deployment

    result = _parse_deployment({})
    assert result.deployment_id == ""
    assert result.create_time is None
    assert result.complete_time is None


def test_parse_deployment_config():
    from aws_util.codedeploy import _parse_deployment_config

    result = _parse_deployment_config(
        {
            "deploymentConfigId": "cfg-1",
            "deploymentConfigName": CONFIG_NAME,
            "computePlatform": "Server",
            "minimumHealthyHosts": {
                "type": "HOST_COUNT",
                "value": 1,
            },
            "createTime": "2024-01-01",
            "trafficRoutingConfig": {},
        }
    )
    assert result.deployment_config_id == "cfg-1"
    assert result.create_time == "2024-01-01"
    assert "trafficRoutingConfig" in result.extra


def test_parse_deployment_config_minimal():
    from aws_util.codedeploy import _parse_deployment_config

    result = _parse_deployment_config({})
    assert result.deployment_config_id == ""
    assert result.create_time is None


def test_parse_revision():
    from aws_util.codedeploy import _parse_revision

    result = _parse_revision(
        {
            "applicationName": APP_NAME,
            "revisionLocation": _REVISION,
            "genericRevisionInfo": {
                "description": "rev desc",
                "registerTime": "2024-01-01",
                "firstUsedTime": "2024-01-02",
                "lastUsedTime": "2024-01-03",
                "deploymentGroups": ["dg-1"],
            },
        },
        application_name=APP_NAME,
    )
    assert result.application_name == APP_NAME
    assert result.revision == _REVISION
    assert result.description == "rev desc"
    assert result.register_time == "2024-01-01"
    assert result.first_used_time == "2024-01-02"
    assert result.last_used_time == "2024-01-03"
    assert "deploymentGroups" in result.extra


def test_parse_revision_minimal():
    from aws_util.codedeploy import _parse_revision

    result = _parse_revision({}, application_name="fallback")
    assert result.application_name == "fallback"
    assert result.description == ""
    assert result.register_time is None
    assert result.first_used_time is None
    assert result.last_used_time is None


def test_parse_revision_with_revisionInfo_wrapper():
    from aws_util.codedeploy import _parse_revision

    result = _parse_revision(
        {
            "revisionInfo": {
                "applicationName": APP_NAME,
                "revisionLocation": _REVISION,
                "genericRevisionInfo": {
                    "description": "wrapped",
                },
            },
        },
        application_name="ignored",
    )
    assert result.application_name == APP_NAME
    assert result.description == "wrapped"


def test_parse_revision_with_revision_key():
    """Covers the fallback to 'revision' key."""
    from aws_util.codedeploy import _parse_revision

    result = _parse_revision(
        {
            "revision": _REVISION,
            "genericRevisionInfo": {},
        },
        application_name=APP_NAME,
    )
    assert result.revision == _REVISION


# ---------------------------------------------------------------------------
# create_application
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_create_application_success(mock_gc):
    mock_client = MagicMock()
    mock_client.create_application.return_value = {
        "applicationId": "app-123",
    }
    mock_gc.return_value = mock_client

    result = create_application(APP_NAME, region_name=REGION)
    assert isinstance(result, ApplicationResult)
    assert result.application_id == "app-123"
    assert result.application_name == APP_NAME
    assert result.compute_platform == "Server"


@patch("aws_util.codedeploy.get_client")
def test_create_application_custom_platform(mock_gc):
    mock_client = MagicMock()
    mock_client.create_application.return_value = {
        "applicationId": "app-456",
    }
    mock_gc.return_value = mock_client

    result = create_application(
        APP_NAME, compute_platform="Lambda", region_name=REGION
    )
    assert result.compute_platform == "Lambda"


@patch("aws_util.codedeploy.get_client")
def test_create_application_error(mock_gc):
    mock_client = MagicMock()
    mock_client.create_application.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "CreateApplication",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="create_application failed"
    ):
        create_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# get_application
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_get_application_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_application.return_value = {
        "application": {
            "applicationId": "app-1",
            "applicationName": APP_NAME,
            "computePlatform": "Server",
            "createTime": "2024-01-01",
        }
    }
    mock_gc.return_value = mock_client

    result = get_application(APP_NAME, region_name=REGION)
    assert result.application_name == APP_NAME
    assert result.create_time == "2024-01-01"


@patch("aws_util.codedeploy.get_client")
def test_get_application_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_application.side_effect = ClientError(
        {
            "Error": {
                "Code": "ApplicationDoesNotExistException",
                "Message": "nope",
            }
        },
        "GetApplication",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="get_application failed"
    ):
        get_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# list_applications
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_list_applications_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"applications": ["app-a", "app-b"]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_applications(region_name=REGION)
    assert result == ["app-a", "app-b"]


@patch("aws_util.codedeploy.get_client")
def test_list_applications_empty(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"applications": []}]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_applications(region_name=REGION)
    assert result == []


@patch("aws_util.codedeploy.get_client")
def test_list_applications_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListApplications",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="list_applications failed"
    ):
        list_applications(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_application
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_delete_application_success(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_application.return_value = {}
    mock_gc.return_value = mock_client

    delete_application(APP_NAME, region_name=REGION)
    mock_client.delete_application.assert_called_once_with(
        applicationName=APP_NAME,
    )


@patch("aws_util.codedeploy.get_client")
def test_delete_application_error(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_application.side_effect = ClientError(
        {
            "Error": {
                "Code": "ApplicationDoesNotExistException",
                "Message": "nope",
            }
        },
        "DeleteApplication",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="delete_application failed"
    ):
        delete_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# create_deployment_group
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_group_success(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_group.return_value = {
        "deploymentGroupId": "dg-123",
    }
    mock_gc.return_value = mock_client

    result = create_deployment_group(
        APP_NAME,
        DG_NAME,
        service_role_arn=ROLE_ARN,
        region_name=REGION,
    )
    assert result == "dg-123"


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_group_all_options(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_group.return_value = {
        "deploymentGroupId": "dg-456",
    }
    mock_gc.return_value = mock_client

    result = create_deployment_group(
        APP_NAME,
        DG_NAME,
        service_role_arn=ROLE_ARN,
        deployment_config_name=CONFIG_NAME,
        ec2_tag_filters=[{"Key": "env", "Value": "prod", "Type": "KEY_AND_VALUE"}],
        auto_scaling_groups=["asg-1"],
        region_name=REGION,
    )
    assert result == "dg-456"
    call_kwargs = mock_client.create_deployment_group.call_args[1]
    assert "deploymentConfigName" in call_kwargs
    assert "ec2TagFilters" in call_kwargs
    assert "autoScalingGroups" in call_kwargs


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_group_error(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_group.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "CreateDeploymentGroup",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="create_deployment_group failed"
    ):
        create_deployment_group(
            APP_NAME,
            DG_NAME,
            service_role_arn=ROLE_ARN,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_deployment_group
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_group_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment_group.return_value = {
        "deploymentGroupInfo": {
            "deploymentGroupId": "dg-1",
            "deploymentGroupName": DG_NAME,
            "applicationName": APP_NAME,
            "serviceRoleArn": ROLE_ARN,
            "deploymentConfigName": CONFIG_NAME,
            "computePlatform": "Server",
        }
    }
    mock_gc.return_value = mock_client

    result = get_deployment_group(
        APP_NAME, DG_NAME, region_name=REGION
    )
    assert result.deployment_group_name == DG_NAME
    assert result.service_role_arn == ROLE_ARN


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_group_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment_group.side_effect = ClientError(
        {
            "Error": {
                "Code": "DeploymentGroupDoesNotExistException",
                "Message": "nope",
            }
        },
        "GetDeploymentGroup",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="get_deployment_group failed"
    ):
        get_deployment_group(
            APP_NAME, DG_NAME, region_name=REGION
        )


# ---------------------------------------------------------------------------
# list_deployment_groups
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_groups_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"deploymentGroups": ["dg-a", "dg-b"]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_deployment_groups(
        APP_NAME, region_name=REGION
    )
    assert result == ["dg-a", "dg-b"]


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_groups_empty(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"deploymentGroups": []},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_deployment_groups(
        APP_NAME, region_name=REGION
    )
    assert result == []


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_groups_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListDeploymentGroups",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="list_deployment_groups failed"
    ):
        list_deployment_groups(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_deployment_group
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_delete_deployment_group_success(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_deployment_group.return_value = {}
    mock_gc.return_value = mock_client

    delete_deployment_group(
        APP_NAME, DG_NAME, region_name=REGION
    )
    mock_client.delete_deployment_group.assert_called_once_with(
        applicationName=APP_NAME,
        deploymentGroupName=DG_NAME,
    )


@patch("aws_util.codedeploy.get_client")
def test_delete_deployment_group_error(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_deployment_group.side_effect = ClientError(
        {
            "Error": {
                "Code": "DeploymentGroupDoesNotExistException",
                "Message": "nope",
            }
        },
        "DeleteDeploymentGroup",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="delete_deployment_group failed"
    ):
        delete_deployment_group(
            APP_NAME, DG_NAME, region_name=REGION
        )


# ---------------------------------------------------------------------------
# create_deployment
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_success(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment.return_value = {
        "deploymentId": DEPLOYMENT_ID,
    }
    mock_gc.return_value = mock_client

    result = create_deployment(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
        region_name=REGION,
    )
    assert result == DEPLOYMENT_ID


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_all_options(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment.return_value = {
        "deploymentId": DEPLOYMENT_ID,
    }
    mock_gc.return_value = mock_client

    result = create_deployment(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
        description="test deploy",
        deployment_config_name=CONFIG_NAME,
        auto_rollback_configuration={
            "enabled": True,
            "events": ["DEPLOYMENT_FAILURE"],
        },
        region_name=REGION,
    )
    assert result == DEPLOYMENT_ID
    call_kwargs = mock_client.create_deployment.call_args[1]
    assert "description" in call_kwargs
    assert "deploymentConfigName" in call_kwargs
    assert "autoRollbackConfiguration" in call_kwargs


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_error(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "CreateDeployment",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="create_deployment failed"
    ):
        create_deployment(
            APP_NAME,
            deployment_group_name=DG_NAME,
            revision=_REVISION,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_deployment
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment.return_value = {
        "deploymentInfo": {
            "deploymentId": DEPLOYMENT_ID,
            "applicationName": APP_NAME,
            "deploymentGroupName": DG_NAME,
            "status": "Succeeded",
            "revision": _REVISION,
            "description": "test",
            "createTime": "2024-01-01",
            "completeTime": "2024-01-02",
        }
    }
    mock_gc.return_value = mock_client

    result = get_deployment(DEPLOYMENT_ID, region_name=REGION)
    assert result.status == "Succeeded"
    assert result.deployment_id == DEPLOYMENT_ID
    assert result.create_time == "2024-01-01"


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment.side_effect = ClientError(
        {
            "Error": {
                "Code": "DeploymentDoesNotExistException",
                "Message": "nope",
            }
        },
        "GetDeployment",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="get_deployment failed"
    ):
        get_deployment(DEPLOYMENT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# list_deployments
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_list_deployments_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"deployments": ["d-1", "d-2"]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_deployments(region_name=REGION)
    assert result == ["d-1", "d-2"]


@patch("aws_util.codedeploy.get_client")
def test_list_deployments_with_filters(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"deployments": ["d-1"]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_deployments(
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        include_only_statuses=["Succeeded"],
        region_name=REGION,
    )
    assert result == ["d-1"]
    call_kwargs = mock_paginator.paginate.call_args[1]
    assert call_kwargs["applicationName"] == APP_NAME
    assert call_kwargs["deploymentGroupName"] == DG_NAME
    assert call_kwargs["includeOnlyStatuses"] == ["Succeeded"]


@patch("aws_util.codedeploy.get_client")
def test_list_deployments_empty(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"deployments": []}]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_deployments(region_name=REGION)
    assert result == []


@patch("aws_util.codedeploy.get_client")
def test_list_deployments_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListDeployments",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="list_deployments failed"
    ):
        list_deployments(region_name=REGION)


# ---------------------------------------------------------------------------
# stop_deployment
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_stop_deployment_success(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_deployment.return_value = {}
    mock_gc.return_value = mock_client

    stop_deployment(DEPLOYMENT_ID, region_name=REGION)
    mock_client.stop_deployment.assert_called_once_with(
        deploymentId=DEPLOYMENT_ID,
        autoRollbackEnabled=False,
    )


@patch("aws_util.codedeploy.get_client")
def test_stop_deployment_with_rollback(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_deployment.return_value = {}
    mock_gc.return_value = mock_client

    stop_deployment(
        DEPLOYMENT_ID,
        auto_rollback_enabled=True,
        region_name=REGION,
    )
    call_kwargs = mock_client.stop_deployment.call_args[1]
    assert call_kwargs["autoRollbackEnabled"] is True


@patch("aws_util.codedeploy.get_client")
def test_stop_deployment_error(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_deployment.side_effect = ClientError(
        {
            "Error": {
                "Code": "DeploymentAlreadyCompletedException",
                "Message": "done",
            }
        },
        "StopDeployment",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="stop_deployment failed"
    ):
        stop_deployment(DEPLOYMENT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# continue_deployment
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_continue_deployment_success(mock_gc):
    mock_client = MagicMock()
    mock_client.continue_deployment.return_value = {}
    mock_gc.return_value = mock_client

    continue_deployment(DEPLOYMENT_ID, region_name=REGION)
    mock_client.continue_deployment.assert_called_once_with(
        deploymentId=DEPLOYMENT_ID,
        deploymentWaitType="READY_WAIT",
    )


@patch("aws_util.codedeploy.get_client")
def test_continue_deployment_termination_wait(mock_gc):
    mock_client = MagicMock()
    mock_client.continue_deployment.return_value = {}
    mock_gc.return_value = mock_client

    continue_deployment(
        DEPLOYMENT_ID,
        deployment_wait_type="TERMINATION_WAIT",
        region_name=REGION,
    )
    call_kwargs = mock_client.continue_deployment.call_args[1]
    assert call_kwargs["deploymentWaitType"] == "TERMINATION_WAIT"


@patch("aws_util.codedeploy.get_client")
def test_continue_deployment_error(mock_gc):
    mock_client = MagicMock()
    mock_client.continue_deployment.side_effect = ClientError(
        {
            "Error": {
                "Code": "InvalidDeploymentWaitTypeException",
                "Message": "bad",
            }
        },
        "ContinueDeployment",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="continue_deployment failed"
    ):
        continue_deployment(DEPLOYMENT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# register_application_revision
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_register_application_revision_success(mock_gc):
    mock_client = MagicMock()
    mock_client.register_application_revision.return_value = {}
    mock_gc.return_value = mock_client

    register_application_revision(
        APP_NAME, revision=_REVISION, region_name=REGION
    )
    mock_client.register_application_revision.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_register_application_revision_with_description(mock_gc):
    mock_client = MagicMock()
    mock_client.register_application_revision.return_value = {}
    mock_gc.return_value = mock_client

    register_application_revision(
        APP_NAME,
        revision=_REVISION,
        description="test rev",
        region_name=REGION,
    )
    call_kwargs = (
        mock_client.register_application_revision.call_args[1]
    )
    assert call_kwargs["description"] == "test rev"


@patch("aws_util.codedeploy.get_client")
def test_register_application_revision_error(mock_gc):
    mock_client = MagicMock()
    mock_client.register_application_revision.side_effect = (
        ClientError(
            {
                "Error": {
                    "Code": "ValidationException",
                    "Message": "bad",
                }
            },
            "RegisterApplicationRevision",
        )
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError,
        match="register_application_revision failed",
    ):
        register_application_revision(
            APP_NAME, revision=_REVISION, region_name=REGION
        )


# ---------------------------------------------------------------------------
# get_application_revision
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_get_application_revision_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_application_revision.return_value = {
        "applicationName": APP_NAME,
        "revisionLocation": _REVISION,
        "genericRevisionInfo": {
            "description": "rev desc",
            "registerTime": "2024-01-01",
        },
    }
    mock_gc.return_value = mock_client

    result = get_application_revision(
        APP_NAME, revision=_REVISION, region_name=REGION
    )
    assert isinstance(result, RevisionResult)
    assert result.application_name == APP_NAME
    assert result.description == "rev desc"


@patch("aws_util.codedeploy.get_client")
def test_get_application_revision_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_application_revision.side_effect = ClientError(
        {
            "Error": {
                "Code": "RevisionDoesNotExistException",
                "Message": "nope",
            }
        },
        "GetApplicationRevision",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="get_application_revision failed"
    ):
        get_application_revision(
            APP_NAME, revision=_REVISION, region_name=REGION
        )


# ---------------------------------------------------------------------------
# list_application_revisions
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_list_application_revisions_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"revisions": [_REVISION]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_application_revisions(
        APP_NAME, region_name=REGION
    )
    assert len(result) == 1
    assert result[0] == _REVISION


@patch("aws_util.codedeploy.get_client")
def test_list_application_revisions_with_sort(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"revisions": [_REVISION]},
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_application_revisions(
        APP_NAME,
        sort_by="registerTime",
        sort_order="descending",
        region_name=REGION,
    )
    assert len(result) == 1
    call_kwargs = mock_paginator.paginate.call_args[1]
    assert call_kwargs["sortBy"] == "registerTime"
    assert call_kwargs["sortOrder"] == "descending"


@patch("aws_util.codedeploy.get_client")
def test_list_application_revisions_empty(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"revisions": []}]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_application_revisions(
        APP_NAME, region_name=REGION
    )
    assert result == []


@patch("aws_util.codedeploy.get_client")
def test_list_application_revisions_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListApplicationRevisions",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="list_application_revisions failed"
    ):
        list_application_revisions(
            APP_NAME, region_name=REGION
        )


# ---------------------------------------------------------------------------
# create_deployment_config
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_config_success(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_config.return_value = {
        "deploymentConfigId": "cfg-123",
    }
    mock_gc.return_value = mock_client

    result = create_deployment_config(
        CONFIG_NAME, region_name=REGION
    )
    assert result == "cfg-123"


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_config_with_hosts(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_config.return_value = {
        "deploymentConfigId": "cfg-456",
    }
    mock_gc.return_value = mock_client

    result = create_deployment_config(
        CONFIG_NAME,
        minimum_healthy_hosts={
            "type": "HOST_COUNT",
            "value": 1,
        },
        compute_platform="Lambda",
        region_name=REGION,
    )
    assert result == "cfg-456"
    call_kwargs = (
        mock_client.create_deployment_config.call_args[1]
    )
    assert "minimumHealthyHosts" in call_kwargs
    assert call_kwargs["computePlatform"] == "Lambda"


@patch("aws_util.codedeploy.get_client")
def test_create_deployment_config_error(mock_gc):
    mock_client = MagicMock()
    mock_client.create_deployment_config.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "CreateDeploymentConfig",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="create_deployment_config failed"
    ):
        create_deployment_config(
            CONFIG_NAME, region_name=REGION
        )


# ---------------------------------------------------------------------------
# get_deployment_config
# ---------------------------------------------------------------------------


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_config_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment_config.return_value = {
        "deploymentConfigInfo": {
            "deploymentConfigId": "cfg-1",
            "deploymentConfigName": CONFIG_NAME,
            "computePlatform": "Server",
            "minimumHealthyHosts": {
                "type": "HOST_COUNT",
                "value": 1,
            },
            "createTime": "2024-01-01",
        }
    }
    mock_gc.return_value = mock_client

    result = get_deployment_config(
        CONFIG_NAME, region_name=REGION
    )
    assert result.deployment_config_name == CONFIG_NAME
    assert result.create_time == "2024-01-01"


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_config_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_deployment_config.side_effect = ClientError(
        {
            "Error": {
                "Code": "DeploymentConfigDoesNotExistException",
                "Message": "nope",
            }
        },
        "GetDeploymentConfig",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(
        RuntimeError, match="get_deployment_config failed"
    ):
        get_deployment_config(CONFIG_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_deployment
# ---------------------------------------------------------------------------


def test_wait_for_deployment_immediate_success(monkeypatch):
    result = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        status="Succeeded",
    )
    monkeypatch.setattr(
        cd_mod,
        "get_deployment",
        lambda did, region_name=None: result,
    )
    got = wait_for_deployment(
        DEPLOYMENT_ID,
        timeout=5.0,
        poll_interval=0.01,
        region_name=REGION,
    )
    assert got.status == "Succeeded"


def test_wait_for_deployment_failure_status(monkeypatch):
    result = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="Failed",
    )
    monkeypatch.setattr(
        cd_mod,
        "get_deployment",
        lambda did, region_name=None: result,
    )
    with pytest.raises(
        RuntimeError, match="entered failure status"
    ):
        wait_for_deployment(
            DEPLOYMENT_ID,
            timeout=5.0,
            poll_interval=0.01,
            region_name=REGION,
        )


def test_wait_for_deployment_timeout(monkeypatch):
    result = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="InProgress",
    )
    monkeypatch.setattr(
        cd_mod,
        "get_deployment",
        lambda did, region_name=None: result,
    )
    from aws_util.exceptions import AwsTimeoutError

    with pytest.raises(AwsTimeoutError, match="did not reach"):
        wait_for_deployment(
            DEPLOYMENT_ID,
            timeout=0.0,
            poll_interval=0.0,
            region_name=REGION,
        )


def test_wait_for_deployment_polls_then_succeeds(monkeypatch):
    monkeypatch.setattr(_time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_get(did, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 3:
            return DeploymentResult(
                deployment_id=did,
                status="InProgress",
            )
        return DeploymentResult(
            deployment_id=did,
            status="Succeeded",
        )

    monkeypatch.setattr(cd_mod, "get_deployment", fake_get)
    got = wait_for_deployment(
        DEPLOYMENT_ID,
        timeout=60.0,
        poll_interval=0.001,
        region_name=REGION,
    )
    assert got.status == "Succeeded"
    assert call_count["n"] == 3


def test_wait_for_deployment_custom_target(monkeypatch):
    result = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="Stopped",
    )
    monkeypatch.setattr(
        cd_mod,
        "get_deployment",
        lambda did, region_name=None: result,
    )
    got = wait_for_deployment(
        DEPLOYMENT_ID,
        target_statuses=("Stopped",),
        failure_statuses=("Failed",),
        timeout=5.0,
        region_name=REGION,
    )
    assert got.status == "Stopped"


# ---------------------------------------------------------------------------
# deploy_and_wait
# ---------------------------------------------------------------------------


def test_deploy_and_wait_success(monkeypatch):
    monkeypatch.setattr(
        cd_mod,
        "create_deployment",
        lambda app, **kw: DEPLOYMENT_ID,
    )
    result = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        status="Succeeded",
    )
    monkeypatch.setattr(
        cd_mod,
        "wait_for_deployment",
        lambda did, **kw: result,
    )
    got = deploy_and_wait(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
        region_name=REGION,
    )
    assert got.status == "Succeeded"
    assert got.deployment_id == DEPLOYMENT_ID

@patch("aws_util.codedeploy.get_client")
def test_add_tags_to_on_premises_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_on_premises_instances.return_value = {}
    add_tags_to_on_premises_instances([], [], region_name=REGION)
    mock_client.add_tags_to_on_premises_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_add_tags_to_on_premises_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_on_premises_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_on_premises_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to add tags to on premises instances"):
        add_tags_to_on_premises_instances([], [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_application_revisions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_application_revisions.return_value = {}
    batch_get_application_revisions("test-application_name", [], region_name=REGION)
    mock_client.batch_get_application_revisions.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_application_revisions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_application_revisions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_application_revisions",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get application revisions"):
        batch_get_application_revisions("test-application_name", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_applications(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_applications.return_value = {}
    batch_get_applications([], region_name=REGION)
    mock_client.batch_get_applications.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_applications_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_applications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_applications",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get applications"):
        batch_get_applications([], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_groups.return_value = {}
    batch_get_deployment_groups("test-application_name", [], region_name=REGION)
    mock_client.batch_get_deployment_groups.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_deployment_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get deployment groups"):
        batch_get_deployment_groups("test-application_name", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_instances.return_value = {}
    batch_get_deployment_instances("test-deployment_id", [], region_name=REGION)
    mock_client.batch_get_deployment_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_deployment_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get deployment instances"):
        batch_get_deployment_instances("test-deployment_id", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_targets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_targets.return_value = {}
    batch_get_deployment_targets("test-deployment_id", [], region_name=REGION)
    mock_client.batch_get_deployment_targets.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployment_targets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployment_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_deployment_targets",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get deployment targets"):
        batch_get_deployment_targets("test-deployment_id", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployments.return_value = {}
    batch_get_deployments([], region_name=REGION)
    mock_client.batch_get_deployments.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_deployments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_deployments",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get deployments"):
        batch_get_deployments([], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_batch_get_on_premises_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_on_premises_instances.return_value = {}
    batch_get_on_premises_instances([], region_name=REGION)
    mock_client.batch_get_on_premises_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_batch_get_on_premises_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_on_premises_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_on_premises_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get on premises instances"):
        batch_get_on_premises_instances([], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_delete_deployment_config(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_deployment_config.return_value = {}
    delete_deployment_config("test-deployment_config_name", region_name=REGION)
    mock_client.delete_deployment_config.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_delete_deployment_config_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_deployment_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_deployment_config",
    )
    with pytest.raises(RuntimeError, match="Failed to delete deployment config"):
        delete_deployment_config("test-deployment_config_name", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_delete_git_hub_account_token(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_git_hub_account_token.return_value = {}
    delete_git_hub_account_token(region_name=REGION)
    mock_client.delete_git_hub_account_token.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_delete_git_hub_account_token_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_git_hub_account_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_git_hub_account_token",
    )
    with pytest.raises(RuntimeError, match="Failed to delete git hub account token"):
        delete_git_hub_account_token(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_delete_resources_by_external_id(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resources_by_external_id.return_value = {}
    delete_resources_by_external_id(region_name=REGION)
    mock_client.delete_resources_by_external_id.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_delete_resources_by_external_id_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resources_by_external_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resources_by_external_id",
    )
    with pytest.raises(RuntimeError, match="Failed to delete resources by external id"):
        delete_resources_by_external_id(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_deregister_on_premises_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deregister_on_premises_instance.return_value = {}
    deregister_on_premises_instance("test-instance_name", region_name=REGION)
    mock_client.deregister_on_premises_instance.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_deregister_on_premises_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deregister_on_premises_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_on_premises_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to deregister on premises instance"):
        deregister_on_premises_instance("test-instance_name", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_deployment_instance.return_value = {}
    get_deployment_instance("test-deployment_id", "test-instance_id", region_name=REGION)
    mock_client.get_deployment_instance.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_deployment_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deployment_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to get deployment instance"):
        get_deployment_instance("test-deployment_id", "test-instance_id", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_target(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_deployment_target.return_value = {}
    get_deployment_target("test-deployment_id", "test-target_id", region_name=REGION)
    mock_client.get_deployment_target.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_get_deployment_target_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_deployment_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deployment_target",
    )
    with pytest.raises(RuntimeError, match="Failed to get deployment target"):
        get_deployment_target("test-deployment_id", "test-target_id", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_get_on_premises_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_on_premises_instance.return_value = {}
    get_on_premises_instance("test-instance_name", region_name=REGION)
    mock_client.get_on_premises_instance.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_get_on_premises_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_on_premises_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_on_premises_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to get on premises instance"):
        get_on_premises_instance("test-instance_name", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_configs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_configs.return_value = {}
    list_deployment_configs(region_name=REGION)
    mock_client.list_deployment_configs.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_configs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_deployment_configs",
    )
    with pytest.raises(RuntimeError, match="Failed to list deployment configs"):
        list_deployment_configs(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_instances.return_value = {}
    list_deployment_instances("test-deployment_id", region_name=REGION)
    mock_client.list_deployment_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_deployment_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to list deployment instances"):
        list_deployment_instances("test-deployment_id", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_targets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_targets.return_value = {}
    list_deployment_targets("test-deployment_id", region_name=REGION)
    mock_client.list_deployment_targets.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_deployment_targets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deployment_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_deployment_targets",
    )
    with pytest.raises(RuntimeError, match="Failed to list deployment targets"):
        list_deployment_targets("test-deployment_id", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_git_hub_account_token_names(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_git_hub_account_token_names.return_value = {}
    list_git_hub_account_token_names(region_name=REGION)
    mock_client.list_git_hub_account_token_names.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_git_hub_account_token_names_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_git_hub_account_token_names.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_git_hub_account_token_names",
    )
    with pytest.raises(RuntimeError, match="Failed to list git hub account token names"):
        list_git_hub_account_token_names(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_on_premises_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_on_premises_instances.return_value = {}
    list_on_premises_instances(region_name=REGION)
    mock_client.list_on_premises_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_on_premises_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_on_premises_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_on_premises_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to list on premises instances"):
        list_on_premises_instances(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_put_lifecycle_event_hook_execution_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_lifecycle_event_hook_execution_status.return_value = {}
    put_lifecycle_event_hook_execution_status(region_name=REGION)
    mock_client.put_lifecycle_event_hook_execution_status.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_put_lifecycle_event_hook_execution_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_lifecycle_event_hook_execution_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_lifecycle_event_hook_execution_status",
    )
    with pytest.raises(RuntimeError, match="Failed to put lifecycle event hook execution status"):
        put_lifecycle_event_hook_execution_status(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_register_on_premises_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_on_premises_instance.return_value = {}
    register_on_premises_instance("test-instance_name", region_name=REGION)
    mock_client.register_on_premises_instance.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_register_on_premises_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_on_premises_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_on_premises_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to register on premises instance"):
        register_on_premises_instance("test-instance_name", region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_remove_tags_from_on_premises_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_on_premises_instances.return_value = {}
    remove_tags_from_on_premises_instances([], [], region_name=REGION)
    mock_client.remove_tags_from_on_premises_instances.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_remove_tags_from_on_premises_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_on_premises_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_on_premises_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to remove tags from on premises instances"):
        remove_tags_from_on_premises_instances([], [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_skip_wait_time_for_instance_termination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.skip_wait_time_for_instance_termination.return_value = {}
    skip_wait_time_for_instance_termination(region_name=REGION)
    mock_client.skip_wait_time_for_instance_termination.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_skip_wait_time_for_instance_termination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.skip_wait_time_for_instance_termination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "skip_wait_time_for_instance_termination",
    )
    with pytest.raises(RuntimeError, match="Failed to skip wait time for instance termination"):
        skip_wait_time_for_instance_termination(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_update_application(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application.return_value = {}
    update_application(region_name=REGION)
    mock_client.update_application.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_update_application_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application",
    )
    with pytest.raises(RuntimeError, match="Failed to update application"):
        update_application(region_name=REGION)


@patch("aws_util.codedeploy.get_client")
def test_update_deployment_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_deployment_group.return_value = {}
    update_deployment_group("test-application_name", "test-current_deployment_group_name", region_name=REGION)
    mock_client.update_deployment_group.assert_called_once()


@patch("aws_util.codedeploy.get_client")
def test_update_deployment_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_deployment_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_deployment_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update deployment group"):
        update_deployment_group("test-application_name", "test-current_deployment_group_name", region_name=REGION)


def test_create_deployment_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import create_deployment_config
    mock_client = MagicMock()
    mock_client.create_deployment_config.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    create_deployment_config({}, minimum_healthy_hosts="test-minimum_healthy_hosts", region_name="us-east-1")
    mock_client.create_deployment_config.assert_called_once()

def test_delete_git_hub_account_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import delete_git_hub_account_token
    mock_client = MagicMock()
    mock_client.delete_git_hub_account_token.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    delete_git_hub_account_token(token_name="test-token_name", region_name="us-east-1")
    mock_client.delete_git_hub_account_token.assert_called_once()

def test_delete_resources_by_external_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import delete_resources_by_external_id
    mock_client = MagicMock()
    mock_client.delete_resources_by_external_id.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    delete_resources_by_external_id(external_id="test-external_id", region_name="us-east-1")
    mock_client.delete_resources_by_external_id.assert_called_once()

def test_list_deployment_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_deployment_configs
    mock_client = MagicMock()
    mock_client.list_deployment_configs.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_deployment_configs(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_deployment_configs.assert_called_once()

def test_list_deployment_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_deployment_instances
    mock_client = MagicMock()
    mock_client.list_deployment_instances.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_deployment_instances("test-deployment_id", next_token="test-next_token", instance_status_filter=[{}], instance_type_filter=[{}], region_name="us-east-1")
    mock_client.list_deployment_instances.assert_called_once()

def test_list_deployment_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_deployment_targets
    mock_client = MagicMock()
    mock_client.list_deployment_targets.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_deployment_targets("test-deployment_id", next_token="test-next_token", target_filters="test-target_filters", region_name="us-east-1")
    mock_client.list_deployment_targets.assert_called_once()

def test_list_git_hub_account_token_names_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_git_hub_account_token_names
    mock_client = MagicMock()
    mock_client.list_git_hub_account_token_names.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_git_hub_account_token_names(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_git_hub_account_token_names.assert_called_once()

def test_list_on_premises_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_on_premises_instances
    mock_client = MagicMock()
    mock_client.list_on_premises_instances.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_on_premises_instances(registration_status="test-registration_status", tag_filters="test-tag_filters", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_on_premises_instances.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_put_lifecycle_event_hook_execution_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import put_lifecycle_event_hook_execution_status
    mock_client = MagicMock()
    mock_client.put_lifecycle_event_hook_execution_status.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    put_lifecycle_event_hook_execution_status(deployment_id="test-deployment_id", lifecycle_event_hook_execution_id="test-lifecycle_event_hook_execution_id", status="test-status", region_name="us-east-1")
    mock_client.put_lifecycle_event_hook_execution_status.assert_called_once()

def test_register_on_premises_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import register_on_premises_instance
    mock_client = MagicMock()
    mock_client.register_on_premises_instance.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    register_on_premises_instance("test-instance_name", iam_session_arn="test-iam_session_arn", iam_user_arn="test-iam_user_arn", region_name="us-east-1")
    mock_client.register_on_premises_instance.assert_called_once()

def test_skip_wait_time_for_instance_termination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import skip_wait_time_for_instance_termination
    mock_client = MagicMock()
    mock_client.skip_wait_time_for_instance_termination.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    skip_wait_time_for_instance_termination(deployment_id="test-deployment_id", region_name="us-east-1")
    mock_client.skip_wait_time_for_instance_termination.assert_called_once()

def test_update_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import update_application
    mock_client = MagicMock()
    mock_client.update_application.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    update_application(application_name="test-application_name", new_application_name="test-new_application_name", region_name="us-east-1")
    mock_client.update_application.assert_called_once()

def test_update_deployment_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codedeploy import update_deployment_group
    mock_client = MagicMock()
    mock_client.update_deployment_group.return_value = {}
    monkeypatch.setattr("aws_util.codedeploy.get_client", lambda *a, **kw: mock_client)
    update_deployment_group("test-application_name", "test-current_deployment_group_name", new_deployment_group_name="test-new_deployment_group_name", deployment_config_name={}, ec2_tag_filters="test-ec2_tag_filters", on_premises_instance_tag_filters="test-on_premises_instance_tag_filters", auto_scaling_groups=True, service_role_arn="test-service_role_arn", trigger_configurations={}, alarm_configuration={}, auto_rollback_configuration=True, outdated_instances_strategy="test-outdated_instances_strategy", deployment_style="test-deployment_style", blue_green_deployment_configuration={}, load_balancer_info="test-load_balancer_info", ec2_tag_set="test-ec2_tag_set", ecs_services="test-ecs_services", on_premises_tag_set="test-on_premises_tag_set", termination_hook_enabled="test-termination_hook_enabled", region_name="us-east-1")
    mock_client.update_deployment_group.assert_called_once()
