"""Tests for aws_util.aio.iot_greengrass -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.iot_greengrass import (
    ComponentResult,
    DeploymentResult,
    InstalledComponentResult,
    cancel_deployment,
    create_component_version,
    create_deployment,
    delete_component,
    describe_component,
    get_component,
    get_deployment,
    list_components,
    list_deployments,
    list_effective_deployments,
    list_installed_components,
    list_tags_for_resource,
    tag_resource,
    associate_service_role_to_account,
    batch_associate_client_device_with_core_device,
    batch_disassociate_client_device_from_core_device,
    delete_core_device,
    delete_deployment,
    disassociate_service_role_from_account,
    get_component_version_artifact,
    get_connectivity_info,
    get_core_device,
    get_service_role_for_account,
    list_client_devices_associated_with_core_device,
    list_component_versions,
    list_core_devices,
    resolve_component_candidates,
    untag_resource,
    update_connectivity_info,
)

COMP_ARN = "arn:aws:greengrass:us-east-1:123:components:c:versions:1.0"


def _mf(mc):
    return lambda *a, **kw: mc


async def test_create_component_version_inline(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"arn": COMP_ARN, "componentName": "c", "status": {"componentState": "REQUESTED"}}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await create_component_version(inline_recipe="yaml")
    assert isinstance(r, ComponentResult)
    assert mc.call.call_args[1]["inlineRecipe"] == b"yaml"

async def test_create_component_version_lambda(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"arn": COMP_ARN, "componentName": "c"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    await create_component_version(lambda_function_recipe_source={"lambdaArn": "arn"}, tags={"k": "v"})
    kw = mc.call.call_args[1]; assert "lambdaFunction" in kw

async def test_create_component_version_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_component_version()

async def test_describe_component(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"arn": COMP_ARN, "componentName": "c"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await describe_component(COMP_ARN); assert isinstance(r, ComponentResult)

async def test_describe_component_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_component(COMP_ARN)

async def test_list_components(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"components": [{"arn": COMP_ARN, "componentName": "c"}]}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_components()) == 1

async def test_list_components_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"components": [{"arn": "a1", "componentName": "c1"}], "nextToken": "t"}, {"components": [{"arn": "a2", "componentName": "c2"}]}]
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_components()) == 2

async def test_list_components_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_components()

async def test_delete_component(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    await delete_component(COMP_ARN)

async def test_delete_component_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await delete_component(COMP_ARN)

async def test_get_component(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"recipe": b"yaml", "recipeOutputFormat": "YAML"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await get_component(COMP_ARN); assert "recipe" in r

async def test_get_component_with_format(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"recipe": b"json"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    await get_component(COMP_ARN, recipe_output_format="JSON")
    assert mc.call.call_args[1]["recipeOutputFormat"] == "JSON"

async def test_get_component_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await get_component(COMP_ARN)

async def test_create_deployment(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"deploymentId": "d1"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await create_deployment("arn:t"); assert isinstance(r, DeploymentResult)
async def test_create_deployment_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_deployment("arn:t")

async def test_get_deployment(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"deploymentId": "d1"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await get_deployment("d1"); assert r.deployment_id == "d1"

async def test_get_deployment_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await get_deployment("d1")

async def test_list_deployments(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"deployments": [{"deploymentId": "d1"}]}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_deployments()) == 1

async def test_list_deployments_with_target(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"deployments": []}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    await list_deployments(target_arn="arn:t")

async def test_list_deployments_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"deployments": [{"deploymentId": "d1"}], "nextToken": "t"}, {"deployments": [{"deploymentId": "d2"}]}]
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_deployments()) == 2

async def test_list_deployments_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_deployments()

async def test_cancel_deployment(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"message": "ok"}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    r = await cancel_deployment("d1"); assert "message" in r

async def test_cancel_deployment_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await cancel_deployment("d1")

async def test_list_effective_deployments(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"effectiveDeployments": [{"deploymentId": "d1"}]}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_effective_deployments("thing1")) == 1

async def test_list_effective_deployments_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"effectiveDeployments": [{"deploymentId": "d1"}], "nextToken": "t"}, {"effectiveDeployments": [{"deploymentId": "d2"}]}]
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_effective_deployments("thing1")) == 2

async def test_list_effective_deployments_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_effective_deployments("thing1")

async def test_list_installed_components(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"installedComponents": [{"componentName": "c"}]}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_installed_components("thing1")) == 1

async def test_list_installed_components_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"installedComponents": [{"componentName": "c1"}], "nextToken": "t"}, {"installedComponents": [{"componentName": "c2"}]}]
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert len(await list_installed_components("thing1")) == 2

async def test_list_installed_components_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_installed_components("thing1")

async def test_tag_resource(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    await tag_resource(COMP_ARN, tags={"k": "v"})

async def test_tag_resource_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await tag_resource(COMP_ARN, tags={"k": "v"})

async def test_list_tags_for_resource(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"tags": {"k": "v"}}
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    assert (await list_tags_for_resource(COMP_ARN)) == {"k": "v"}

async def test_list_tags_for_resource_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_tags_for_resource(COMP_ARN)


async def test_associate_service_role_to_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_service_role_to_account("test-role_arn", )
    mock_client.call.assert_called_once()


async def test_associate_service_role_to_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_service_role_to_account("test-role_arn", )


async def test_batch_associate_client_device_with_core_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_client_device_with_core_device("test-core_device_thing_name", )
    mock_client.call.assert_called_once()


async def test_batch_associate_client_device_with_core_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_client_device_with_core_device("test-core_device_thing_name", )


async def test_batch_disassociate_client_device_from_core_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_client_device_from_core_device("test-core_device_thing_name", )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_client_device_from_core_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_client_device_from_core_device("test-core_device_thing_name", )


async def test_delete_core_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_core_device("test-core_device_thing_name", )
    mock_client.call.assert_called_once()


async def test_delete_core_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_core_device("test-core_device_thing_name", )


async def test_delete_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_deployment("test-deployment_id", )
    mock_client.call.assert_called_once()


async def test_delete_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_deployment("test-deployment_id", )


async def test_disassociate_service_role_from_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_service_role_from_account()
    mock_client.call.assert_called_once()


async def test_disassociate_service_role_from_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_service_role_from_account()


async def test_get_component_version_artifact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_component_version_artifact("test-arn", "test-artifact_name", )
    mock_client.call.assert_called_once()


async def test_get_component_version_artifact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_component_version_artifact("test-arn", "test-artifact_name", )


async def test_get_connectivity_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_connectivity_info("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_get_connectivity_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_connectivity_info("test-thing_name", )


async def test_get_core_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_core_device("test-core_device_thing_name", )
    mock_client.call.assert_called_once()


async def test_get_core_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_core_device("test-core_device_thing_name", )


async def test_get_service_role_for_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_role_for_account()
    mock_client.call.assert_called_once()


async def test_get_service_role_for_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_role_for_account()


async def test_list_client_devices_associated_with_core_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_client_devices_associated_with_core_device("test-core_device_thing_name", )
    mock_client.call.assert_called_once()


async def test_list_client_devices_associated_with_core_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_client_devices_associated_with_core_device("test-core_device_thing_name", )


async def test_list_component_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_component_versions("test-arn", )
    mock_client.call.assert_called_once()


async def test_list_component_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_component_versions("test-arn", )


async def test_list_core_devices(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_core_devices()
    mock_client.call.assert_called_once()


async def test_list_core_devices_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_core_devices()


async def test_resolve_component_candidates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await resolve_component_candidates()
    mock_client.call.assert_called_once()


async def test_resolve_component_candidates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resolve_component_candidates()


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_connectivity_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_connectivity_info("test-thing_name", [], )
    mock_client.call.assert_called_once()


async def test_update_connectivity_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_greengrass.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_connectivity_info("test-thing_name", [], )


@pytest.mark.asyncio
async def test_create_component_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import create_component_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await create_component_version(inline_recipe="test-inline_recipe", lambda_function_recipe_source="test-lambda_function_recipe_source", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_component_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import get_component
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await get_component("test-arn", recipe_output_format="test-recipe_output_format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_associate_client_device_with_core_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import batch_associate_client_device_with_core_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await batch_associate_client_device_with_core_device("test-core_device_thing_name", entries="test-entries", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_disassociate_client_device_from_core_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import batch_disassociate_client_device_from_core_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await batch_disassociate_client_device_from_core_device("test-core_device_thing_name", entries="test-entries", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_component_version_artifact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import get_component_version_artifact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await get_component_version_artifact("test-arn", "test-artifact_name", s3_endpoint_type="test-s3_endpoint_type", iot_endpoint_type="test-iot_endpoint_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_client_devices_associated_with_core_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import list_client_devices_associated_with_core_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await list_client_devices_associated_with_core_device("test-core_device_thing_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_component_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import list_component_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await list_component_versions("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_core_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import list_core_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await list_core_devices(thing_group_arn="test-thing_group_arn", status="test-status", max_results=1, next_token="test-next_token", runtime="test-runtime", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resolve_component_candidates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import resolve_component_candidates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: mock_client)
    await resolve_component_candidates(platform="test-platform", component_candidates="test-component_candidates", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_deployment_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import create_deployment
    m = AsyncMock(); m.call = AsyncMock(return_value={"deploymentId": "d", "iotJobId": "j"})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: m)
    await create_deployment("arn:target", tags={"k": "v"}, region_name="us-east-1")

@pytest.mark.asyncio
async def test_create_deployment_all_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_greengrass import create_deployment
    m = AsyncMock(); m.call = AsyncMock(return_value={"deploymentId": "d", "iotJobId": "j"})
    monkeypatch.setattr("aws_util.aio.iot_greengrass.async_client", lambda *a, **kw: m)
    await create_deployment("arn:target", deployment_name="dn", components={"c": {}}, deployment_policies={}, iot_job_configuration={}, tags={"k": "v"}, region_name="us-east-1")
