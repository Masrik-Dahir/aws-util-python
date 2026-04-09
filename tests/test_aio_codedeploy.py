"""Tests for aws_util.aio.codedeploy module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codedeploy import (
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
# create_application
# ---------------------------------------------------------------------------


async def test_create_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "applicationId": "app-123",
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_application(APP_NAME)
    assert isinstance(result, ApplicationResult)
    assert result.application_id == "app-123"
    assert result.application_name == APP_NAME


async def test_create_application_custom_platform(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"applicationId": "app-456"}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_application(
        APP_NAME, compute_platform="Lambda"
    )
    assert result.compute_platform == "Lambda"


async def test_create_application_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_application(APP_NAME)


async def test_create_application_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="create_application failed"
    ):
        await create_application(APP_NAME)


# ---------------------------------------------------------------------------
# get_application
# ---------------------------------------------------------------------------


async def test_get_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "application": {
            "applicationId": "app-1",
            "applicationName": APP_NAME,
            "computePlatform": "Server",
            "createTime": "2024-01-01",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_application(APP_NAME)
    assert result.application_name == APP_NAME
    assert result.create_time == "2024-01-01"


async def test_get_application_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_application(APP_NAME)


async def test_get_application_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_application failed"
    ):
        await get_application(APP_NAME)


# ---------------------------------------------------------------------------
# list_applications
# ---------------------------------------------------------------------------


async def test_list_applications_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "applications": ["app-a", "app-b"],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_applications()
    assert result == ["app-a", "app-b"]


async def test_list_applications_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "applications": ["app-a"],
                "nextToken": "tok",
            }
        return {"applications": ["app-b"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_applications()
    assert result == ["app-a", "app-b"]


async def test_list_applications_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"applications": []}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_applications()
    assert result == []


async def test_list_applications_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_applications()


async def test_list_applications_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_applications failed"
    ):
        await list_applications()


# ---------------------------------------------------------------------------
# delete_application
# ---------------------------------------------------------------------------


async def test_delete_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application(APP_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_application_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await delete_application(APP_NAME)


async def test_delete_application_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="delete_application failed"
    ):
        await delete_application(APP_NAME)


# ---------------------------------------------------------------------------
# create_deployment_group
# ---------------------------------------------------------------------------


async def test_create_deployment_group_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentGroupId": "dg-123",
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment_group(
        APP_NAME, DG_NAME, service_role_arn=ROLE_ARN
    )
    assert result == "dg-123"


async def test_create_deployment_group_all_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentGroupId": "dg-456",
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment_group(
        APP_NAME,
        DG_NAME,
        service_role_arn=ROLE_ARN,
        deployment_config_name=CONFIG_NAME,
        ec2_tag_filters=[{"Key": "env", "Value": "prod"}],
        auto_scaling_groups=["asg-1"],
    )
    assert result == "dg-456"


async def test_create_deployment_group_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_deployment_group(
            APP_NAME, DG_NAME, service_role_arn=ROLE_ARN
        )


async def test_create_deployment_group_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="create_deployment_group failed"
    ):
        await create_deployment_group(
            APP_NAME, DG_NAME, service_role_arn=ROLE_ARN
        )


# ---------------------------------------------------------------------------
# get_deployment_group
# ---------------------------------------------------------------------------


async def test_get_deployment_group_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentGroupInfo": {
            "deploymentGroupId": "dg-1",
            "deploymentGroupName": DG_NAME,
            "applicationName": APP_NAME,
            "serviceRoleArn": ROLE_ARN,
            "deploymentConfigName": CONFIG_NAME,
            "computePlatform": "Server",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_deployment_group(APP_NAME, DG_NAME)
    assert result.deployment_group_name == DG_NAME


async def test_get_deployment_group_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_deployment_group(APP_NAME, DG_NAME)


async def test_get_deployment_group_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_deployment_group failed"
    ):
        await get_deployment_group(APP_NAME, DG_NAME)


# ---------------------------------------------------------------------------
# list_deployment_groups
# ---------------------------------------------------------------------------


async def test_list_deployment_groups_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentGroups": ["dg-a", "dg-b"],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployment_groups(APP_NAME)
    assert result == ["dg-a", "dg-b"]


async def test_list_deployment_groups_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "deploymentGroups": ["dg-a"],
                "nextToken": "tok",
            }
        return {"deploymentGroups": ["dg-b"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployment_groups(APP_NAME)
    assert result == ["dg-a", "dg-b"]


async def test_list_deployment_groups_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"deploymentGroups": []}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployment_groups(APP_NAME)
    assert result == []


async def test_list_deployment_groups_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deployment_groups(APP_NAME)


async def test_list_deployment_groups_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_deployment_groups failed"
    ):
        await list_deployment_groups(APP_NAME)


# ---------------------------------------------------------------------------
# delete_deployment_group
# ---------------------------------------------------------------------------


async def test_delete_deployment_group_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_deployment_group(APP_NAME, DG_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_deployment_group_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await delete_deployment_group(APP_NAME, DG_NAME)


async def test_delete_deployment_group_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="delete_deployment_group failed"
    ):
        await delete_deployment_group(APP_NAME, DG_NAME)


# ---------------------------------------------------------------------------
# create_deployment
# ---------------------------------------------------------------------------


async def test_create_deployment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentId": DEPLOYMENT_ID,
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
    )
    assert result == DEPLOYMENT_ID


async def test_create_deployment_all_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentId": DEPLOYMENT_ID,
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
        description="test deploy",
        deployment_config_name=CONFIG_NAME,
        auto_rollback_configuration={
            "enabled": True,
            "events": ["DEPLOYMENT_FAILURE"],
        },
    )
    assert result == DEPLOYMENT_ID


async def test_create_deployment_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_deployment(
            APP_NAME,
            deployment_group_name=DG_NAME,
            revision=_REVISION,
        )


async def test_create_deployment_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="create_deployment failed"
    ):
        await create_deployment(
            APP_NAME,
            deployment_group_name=DG_NAME,
            revision=_REVISION,
        )


# ---------------------------------------------------------------------------
# get_deployment
# ---------------------------------------------------------------------------


async def test_get_deployment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentInfo": {
            "deploymentId": DEPLOYMENT_ID,
            "applicationName": APP_NAME,
            "deploymentGroupName": DG_NAME,
            "status": "Succeeded",
            "revision": _REVISION,
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_deployment(DEPLOYMENT_ID)
    assert result.status == "Succeeded"
    assert result.deployment_id == DEPLOYMENT_ID


async def test_get_deployment_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_deployment(DEPLOYMENT_ID)


async def test_get_deployment_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_deployment failed"
    ):
        await get_deployment(DEPLOYMENT_ID)


# ---------------------------------------------------------------------------
# list_deployments
# ---------------------------------------------------------------------------


async def test_list_deployments_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deployments": ["d-1", "d-2"],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployments()
    assert result == ["d-1", "d-2"]


async def test_list_deployments_with_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deployments": ["d-1"],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployments(
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        include_only_statuses=["Succeeded"],
    )
    assert result == ["d-1"]


async def test_list_deployments_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "deployments": ["d-1"],
                "nextToken": "tok",
            }
        return {"deployments": ["d-2"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployments()
    assert result == ["d-1", "d-2"]


async def test_list_deployments_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"deployments": []}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_deployments()
    assert result == []


async def test_list_deployments_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deployments()


async def test_list_deployments_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_deployments failed"
    ):
        await list_deployments()


# ---------------------------------------------------------------------------
# stop_deployment
# ---------------------------------------------------------------------------


async def test_stop_deployment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_deployment(DEPLOYMENT_ID)
    mock_client.call.assert_awaited_once()


async def test_stop_deployment_with_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_deployment(
        DEPLOYMENT_ID, auto_rollback_enabled=True
    )
    mock_client.call.assert_awaited_once()


async def test_stop_deployment_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await stop_deployment(DEPLOYMENT_ID)


async def test_stop_deployment_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="stop_deployment failed"
    ):
        await stop_deployment(DEPLOYMENT_ID)


# ---------------------------------------------------------------------------
# continue_deployment
# ---------------------------------------------------------------------------


async def test_continue_deployment_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await continue_deployment(DEPLOYMENT_ID)
    mock_client.call.assert_awaited_once()


async def test_continue_deployment_termination_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await continue_deployment(
        DEPLOYMENT_ID,
        deployment_wait_type="TERMINATION_WAIT",
    )
    mock_client.call.assert_awaited_once()


async def test_continue_deployment_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await continue_deployment(DEPLOYMENT_ID)


async def test_continue_deployment_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="continue_deployment failed"
    ):
        await continue_deployment(DEPLOYMENT_ID)


# ---------------------------------------------------------------------------
# register_application_revision
# ---------------------------------------------------------------------------


async def test_register_application_revision_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_application_revision(
        APP_NAME, revision=_REVISION
    )
    mock_client.call.assert_awaited_once()


async def test_register_application_revision_with_description(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_application_revision(
        APP_NAME, revision=_REVISION, description="test rev"
    )
    mock_client.call.assert_awaited_once()


async def test_register_application_revision_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await register_application_revision(
            APP_NAME, revision=_REVISION
        )


async def test_register_application_revision_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="register_application_revision failed",
    ):
        await register_application_revision(
            APP_NAME, revision=_REVISION
        )


# ---------------------------------------------------------------------------
# get_application_revision
# ---------------------------------------------------------------------------


async def test_get_application_revision_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "applicationName": APP_NAME,
        "revisionLocation": _REVISION,
        "genericRevisionInfo": {
            "description": "rev desc",
            "registerTime": "2024-01-01",
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_application_revision(
        APP_NAME, revision=_REVISION
    )
    assert isinstance(result, RevisionResult)
    assert result.application_name == APP_NAME
    assert result.description == "rev desc"


async def test_get_application_revision_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_application_revision(
            APP_NAME, revision=_REVISION
        )


async def test_get_application_revision_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="get_application_revision failed",
    ):
        await get_application_revision(
            APP_NAME, revision=_REVISION
        )


# ---------------------------------------------------------------------------
# list_application_revisions
# ---------------------------------------------------------------------------


async def test_list_application_revisions_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "revisions": [_REVISION],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_application_revisions(APP_NAME)
    assert len(result) == 1
    assert result[0] == _REVISION


async def test_list_application_revisions_with_sort(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "revisions": [_REVISION],
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_application_revisions(
        APP_NAME,
        sort_by="registerTime",
        sort_order="descending",
    )
    assert len(result) == 1


async def test_list_application_revisions_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "revisions": [_REVISION],
                "nextToken": "tok",
            }
        return {"revisions": [{"revisionType": "GitHub"}]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_application_revisions(APP_NAME)
    assert len(result) == 2


async def test_list_application_revisions_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"revisions": []}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_application_revisions(APP_NAME)
    assert result == []


async def test_list_application_revisions_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_revisions(APP_NAME)


async def test_list_application_revisions_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="list_application_revisions failed",
    ):
        await list_application_revisions(APP_NAME)


# ---------------------------------------------------------------------------
# create_deployment_config
# ---------------------------------------------------------------------------


async def test_create_deployment_config_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentConfigId": "cfg-123",
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment_config(CONFIG_NAME)
    assert result == "cfg-123"


async def test_create_deployment_config_with_hosts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deploymentConfigId": "cfg-456",
    }
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_deployment_config(
        CONFIG_NAME,
        minimum_healthy_hosts={
            "type": "HOST_COUNT",
            "value": 1,
        },
        compute_platform="Lambda",
    )
    assert result == "cfg-456"


async def test_create_deployment_config_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_deployment_config(CONFIG_NAME)


async def test_create_deployment_config_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="create_deployment_config failed"
    ):
        await create_deployment_config(CONFIG_NAME)


# ---------------------------------------------------------------------------
# get_deployment_config
# ---------------------------------------------------------------------------


async def test_get_deployment_config_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
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
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_deployment_config(CONFIG_NAME)
    assert result.deployment_config_name == CONFIG_NAME
    assert result.create_time == "2024-01-01"


async def test_get_deployment_config_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_deployment_config(CONFIG_NAME)


async def test_get_deployment_config_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_deployment_config failed"
    ):
        await get_deployment_config(CONFIG_NAME)


# ---------------------------------------------------------------------------
# wait_for_deployment
# ---------------------------------------------------------------------------


async def test_wait_immediate_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finished = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="Succeeded",
    )

    async def _fake_get(did, region_name=None):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.get_deployment", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_deployment(DEPLOYMENT_ID)
    assert result.status == "Succeeded"


async def test_wait_polls_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_count = 0

    async def _fake_get(did, region_name=None):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return DeploymentResult(
                deployment_id=did,
                status="InProgress",
            )
        return DeploymentResult(
            deployment_id=did,
            status="Succeeded",
        )

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.get_deployment", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_deployment(
        DEPLOYMENT_ID, timeout=60.0
    )
    assert result.status == "Succeeded"


async def test_wait_failure_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failed = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="Failed",
    )

    async def _fake_get(did, region_name=None):
        return failed

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.get_deployment", _fake_get
    )
    with pytest.raises(
        RuntimeError, match="entered failure status"
    ):
        await wait_for_deployment(DEPLOYMENT_ID)


async def test_wait_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    running = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="InProgress",
    )

    async def _fake_get(did, region_name=None):
        return running

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.get_deployment", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.asyncio.sleep", AsyncMock()
    )
    from aws_util.exceptions import AwsTimeoutError

    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_deployment(
            DEPLOYMENT_ID, timeout=0.0
        )


async def test_wait_custom_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stopped = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        status="Stopped",
    )

    async def _fake_get(did, region_name=None):
        return stopped

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.get_deployment", _fake_get
    )
    result = await wait_for_deployment(
        DEPLOYMENT_ID,
        target_statuses=("Stopped",),
        failure_statuses=("Failed",),
    )
    assert result.status == "Stopped"


# ---------------------------------------------------------------------------
# deploy_and_wait
# ---------------------------------------------------------------------------


async def test_deploy_and_wait_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_create(app, **kw):
        return DEPLOYMENT_ID

    finished = DeploymentResult(
        deployment_id=DEPLOYMENT_ID,
        application_name=APP_NAME,
        deployment_group_name=DG_NAME,
        status="Succeeded",
    )

    async def _fake_wait(did, **kwargs):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codedeploy.create_deployment",
        _fake_create,
    )
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.wait_for_deployment",
        _fake_wait,
    )
    result = await deploy_and_wait(
        APP_NAME,
        deployment_group_name=DG_NAME,
        revision=_REVISION,
    )
    assert result.status == "Succeeded"
    assert result.deployment_id == DEPLOYMENT_ID

async def test_add_tags_to_on_premises_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_on_premises_instances([], [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_on_premises_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_on_premises_instances([], [], )


async def test_batch_get_application_revisions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_application_revisions("test-application_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_application_revisions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_application_revisions("test-application_name", [], )


async def test_batch_get_applications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_applications([], )
    mock_client.call.assert_called_once()


async def test_batch_get_applications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_applications([], )


async def test_batch_get_deployment_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_deployment_groups("test-application_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_deployment_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_deployment_groups("test-application_name", [], )


async def test_batch_get_deployment_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_deployment_instances("test-deployment_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_deployment_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_deployment_instances("test-deployment_id", [], )


async def test_batch_get_deployment_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_deployment_targets("test-deployment_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_deployment_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_deployment_targets("test-deployment_id", [], )


async def test_batch_get_deployments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_deployments([], )
    mock_client.call.assert_called_once()


async def test_batch_get_deployments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_deployments([], )


async def test_batch_get_on_premises_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_on_premises_instances([], )
    mock_client.call.assert_called_once()


async def test_batch_get_on_premises_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_on_premises_instances([], )


async def test_delete_deployment_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_deployment_config("test-deployment_config_name", )
    mock_client.call.assert_called_once()


async def test_delete_deployment_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_deployment_config("test-deployment_config_name", )


async def test_delete_git_hub_account_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_git_hub_account_token()
    mock_client.call.assert_called_once()


async def test_delete_git_hub_account_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_git_hub_account_token()


async def test_delete_resources_by_external_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resources_by_external_id()
    mock_client.call.assert_called_once()


async def test_delete_resources_by_external_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resources_by_external_id()


async def test_deregister_on_premises_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_on_premises_instance("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_deregister_on_premises_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_on_premises_instance("test-instance_name", )


async def test_get_deployment_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_deployment_instance("test-deployment_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_deployment_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_deployment_instance("test-deployment_id", "test-instance_id", )


async def test_get_deployment_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_deployment_target("test-deployment_id", "test-target_id", )
    mock_client.call.assert_called_once()


async def test_get_deployment_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_deployment_target("test-deployment_id", "test-target_id", )


async def test_get_on_premises_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_on_premises_instance("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_get_on_premises_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_on_premises_instance("test-instance_name", )


async def test_list_deployment_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_deployment_configs()
    mock_client.call.assert_called_once()


async def test_list_deployment_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deployment_configs()


async def test_list_deployment_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_deployment_instances("test-deployment_id", )
    mock_client.call.assert_called_once()


async def test_list_deployment_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deployment_instances("test-deployment_id", )


async def test_list_deployment_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_deployment_targets("test-deployment_id", )
    mock_client.call.assert_called_once()


async def test_list_deployment_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deployment_targets("test-deployment_id", )


async def test_list_git_hub_account_token_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_git_hub_account_token_names()
    mock_client.call.assert_called_once()


async def test_list_git_hub_account_token_names_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_git_hub_account_token_names()


async def test_list_on_premises_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_on_premises_instances()
    mock_client.call.assert_called_once()


async def test_list_on_premises_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_on_premises_instances()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_lifecycle_event_hook_execution_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_lifecycle_event_hook_execution_status()
    mock_client.call.assert_called_once()


async def test_put_lifecycle_event_hook_execution_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_lifecycle_event_hook_execution_status()


async def test_register_on_premises_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_on_premises_instance("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_register_on_premises_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_on_premises_instance("test-instance_name", )


async def test_remove_tags_from_on_premises_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_on_premises_instances([], [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_on_premises_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_on_premises_instances([], [], )


async def test_skip_wait_time_for_instance_termination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await skip_wait_time_for_instance_termination()
    mock_client.call.assert_called_once()


async def test_skip_wait_time_for_instance_termination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await skip_wait_time_for_instance_termination()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application()
    mock_client.call.assert_called_once()


async def test_update_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application()


async def test_update_deployment_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_deployment_group("test-application_name", "test-current_deployment_group_name", )
    mock_client.call.assert_called_once()


async def test_update_deployment_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codedeploy.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_deployment_group("test-application_name", "test-current_deployment_group_name", )


@pytest.mark.asyncio
async def test_list_deployments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_deployments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_deployments(application_name="test-application_name", deployment_group_name="test-deployment_group_name", include_only_statuses=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_revisions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_application_revisions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_application_revisions("test-application_name", sort_by="test-sort_by", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_deployment_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import create_deployment_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await create_deployment_config({}, minimum_healthy_hosts="test-minimum_healthy_hosts", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_git_hub_account_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import delete_git_hub_account_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await delete_git_hub_account_token(token_name="test-token_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resources_by_external_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import delete_resources_by_external_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await delete_resources_by_external_id(external_id="test-external_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_deployment_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_deployment_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_deployment_configs(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_deployment_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_deployment_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_deployment_instances("test-deployment_id", next_token="test-next_token", instance_status_filter=[{}], instance_type_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_deployment_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_deployment_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_deployment_targets("test-deployment_id", next_token="test-next_token", target_filters="test-target_filters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_git_hub_account_token_names_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_git_hub_account_token_names
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_git_hub_account_token_names(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_on_premises_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_on_premises_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_on_premises_instances(registration_status="test-registration_status", tag_filters="test-tag_filters", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_lifecycle_event_hook_execution_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import put_lifecycle_event_hook_execution_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await put_lifecycle_event_hook_execution_status(deployment_id="test-deployment_id", lifecycle_event_hook_execution_id="test-lifecycle_event_hook_execution_id", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_on_premises_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import register_on_premises_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await register_on_premises_instance("test-instance_name", iam_session_arn="test-iam_session_arn", iam_user_arn="test-iam_user_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_skip_wait_time_for_instance_termination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import skip_wait_time_for_instance_termination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await skip_wait_time_for_instance_termination(deployment_id="test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import update_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await update_application(application_name="test-application_name", new_application_name="test-new_application_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_deployment_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codedeploy import update_deployment_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codedeploy.async_client", lambda *a, **kw: mock_client)
    await update_deployment_group("test-application_name", "test-current_deployment_group_name", new_deployment_group_name="test-new_deployment_group_name", deployment_config_name={}, ec2_tag_filters="test-ec2_tag_filters", on_premises_instance_tag_filters="test-on_premises_instance_tag_filters", auto_scaling_groups=True, service_role_arn="test-service_role_arn", trigger_configurations={}, alarm_configuration={}, auto_rollback_configuration=True, outdated_instances_strategy="test-outdated_instances_strategy", deployment_style="test-deployment_style", blue_green_deployment_configuration={}, load_balancer_info="test-load_balancer_info", ec2_tag_set="test-ec2_tag_set", ecs_services="test-ecs_services", on_premises_tag_set="test-on_premises_tag_set", termination_hook_enabled="test-termination_hook_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()
