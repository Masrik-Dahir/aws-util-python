"""Tests for aws_util.iot_greengrass -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.iot_greengrass import (
    ComponentResult,
    DeploymentResult,
    InstalledComponentResult,
    _parse_component,
    _parse_deployment,
    _parse_installed_component,
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

COMP_ARN = "arn:aws:greengrass:us-east-1:123:components:my-comp:versions:1.0.0"


def _ce(code="ValidationException"):
    return ClientError({"Error": {"Code": code, "Message": "boom"}}, "Op")


# Parsers
def test_parse_component_dict_status(monkeypatch):
    c = _parse_component({"arn": COMP_ARN, "componentName": "c", "componentVersion": "1.0", "status": {"componentState": "DEPLOYABLE"}, "description": "d", "extra": 1})
    assert isinstance(c, ComponentResult)
    assert c.status == "DEPLOYABLE"
    assert c.extra == {"extra": 1}

def test_parse_component_string_status():
    c = _parse_component({"componentName": "c", "status": "ACTIVE"})
    assert c.status == "ACTIVE"

def test_parse_component_latest_version():
    c = _parse_component({"componentName": "c", "latestVersion": {"componentVersion": "2.0"}})
    assert c.component_version == "2.0"

def test_parse_deployment():
    d = _parse_deployment({"deploymentId": "d1", "deploymentName": "dep", "deploymentStatus": "ACTIVE", "targetArn": "arn:t", "revisionId": "r1", "extra": True})
    assert isinstance(d, DeploymentResult)
    assert d.extra == {"extra": True}

def test_parse_installed_component():
    ic = _parse_installed_component({"componentName": "c", "componentVersion": "1.0", "lifecycleState": "RUNNING", "isRoot": True, "extra": 1})
    assert isinstance(ic, InstalledComponentResult)
    assert ic.is_root is True

# Component operations
@patch("aws_util.iot_greengrass.get_client")
def test_create_component_version_inline(mock_gc):
    client = MagicMock()
    client.create_component_version.return_value = {"arn": COMP_ARN, "componentName": "c", "componentVersion": "1.0", "status": {"componentState": "REQUESTED"}}
    mock_gc.return_value = client
    r = create_component_version(inline_recipe="recipe-yaml")
    assert isinstance(r, ComponentResult)
    assert client.create_component_version.call_args[1]["inlineRecipe"] == b"recipe-yaml"

@patch("aws_util.iot_greengrass.get_client")
def test_create_component_version_lambda(mock_gc):
    client = MagicMock()
    client.create_component_version.return_value = {"arn": COMP_ARN, "componentName": "c"}
    mock_gc.return_value = client
    create_component_version(lambda_function_recipe_source={"lambdaArn": "arn"}, tags={"k": "v"})
    kw = client.create_component_version.call_args[1]
    assert "lambdaFunction" in kw
    assert kw["tags"] == {"k": "v"}

@patch("aws_util.iot_greengrass.get_client")
def test_create_component_version_error(mock_gc):
    client = MagicMock(); client.create_component_version.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): create_component_version()

@patch("aws_util.iot_greengrass.get_client")
def test_describe_component(mock_gc):
    client = MagicMock()
    client.describe_component.return_value = {"arn": COMP_ARN, "componentName": "c"}
    mock_gc.return_value = client
    r = describe_component(COMP_ARN)
    assert isinstance(r, ComponentResult)

@patch("aws_util.iot_greengrass.get_client")
def test_describe_component_error(mock_gc):
    client = MagicMock(); client.describe_component.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): describe_component(COMP_ARN)

@patch("aws_util.iot_greengrass.get_client")
def test_list_components(mock_gc):
    client = MagicMock()
    client.list_components.return_value = {"components": [{"arn": COMP_ARN, "componentName": "c"}]}
    mock_gc.return_value = client
    assert len(list_components()) == 1

@patch("aws_util.iot_greengrass.get_client")
def test_list_components_pagination(mock_gc):
    client = MagicMock()
    client.list_components.side_effect = [
        {"components": [{"arn": "a1", "componentName": "c1"}], "nextToken": "t"},
        {"components": [{"arn": "a2", "componentName": "c2"}]},
    ]
    mock_gc.return_value = client
    assert len(list_components()) == 2

@patch("aws_util.iot_greengrass.get_client")
def test_list_components_error(mock_gc):
    client = MagicMock(); client.list_components.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): list_components()

@patch("aws_util.iot_greengrass.get_client")
def test_delete_component(mock_gc):
    client = MagicMock(); mock_gc.return_value = client
    delete_component(COMP_ARN)
    client.delete_component.assert_called_once_with(arn=COMP_ARN)

@patch("aws_util.iot_greengrass.get_client")
def test_delete_component_error(mock_gc):
    client = MagicMock(); client.delete_component.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): delete_component(COMP_ARN)

@patch("aws_util.iot_greengrass.get_client")
def test_get_component(mock_gc):
    client = MagicMock()
    client.get_component.return_value = {"recipe": b"yaml", "recipeOutputFormat": "YAML"}
    mock_gc.return_value = client
    r = get_component(COMP_ARN)
    assert "recipe" in r

@patch("aws_util.iot_greengrass.get_client")
def test_get_component_with_format(mock_gc):
    client = MagicMock()
    client.get_component.return_value = {"recipe": b"json", "recipeOutputFormat": "JSON"}
    mock_gc.return_value = client
    get_component(COMP_ARN, recipe_output_format="JSON")
    assert client.get_component.call_args[1]["recipeOutputFormat"] == "JSON"

@patch("aws_util.iot_greengrass.get_client")
def test_get_component_error(mock_gc):
    client = MagicMock(); client.get_component.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): get_component(COMP_ARN)

# Deployment operations
@patch("aws_util.iot_greengrass.get_client")
def test_create_deployment(mock_gc):
    client = MagicMock()
    client.create_deployment.return_value = {"deploymentId": "d1"}
    mock_gc.return_value = client
    r = create_deployment("arn:target")
    assert isinstance(r, DeploymentResult)

@patch("aws_util.iot_greengrass.get_client")
def test_create_deployment_error(mock_gc):
    client = MagicMock(); client.create_deployment.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): create_deployment("arn:t")

@patch("aws_util.iot_greengrass.get_client")
def test_get_deployment(mock_gc):
    client = MagicMock()
    client.get_deployment.return_value = {"deploymentId": "d1", "deploymentName": "dep"}
    mock_gc.return_value = client
    r = get_deployment("d1")
    assert r.deployment_id == "d1"

@patch("aws_util.iot_greengrass.get_client")
def test_get_deployment_error(mock_gc):
    client = MagicMock(); client.get_deployment.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): get_deployment("d1")

@patch("aws_util.iot_greengrass.get_client")
def test_list_deployments(mock_gc):
    client = MagicMock()
    client.list_deployments.return_value = {"deployments": [{"deploymentId": "d1"}]}
    mock_gc.return_value = client
    assert len(list_deployments()) == 1

@patch("aws_util.iot_greengrass.get_client")
def test_list_deployments_with_target(mock_gc):
    client = MagicMock()
    client.list_deployments.return_value = {"deployments": []}
    mock_gc.return_value = client
    list_deployments(target_arn="arn:t")
    assert client.list_deployments.call_args[1]["targetArn"] == "arn:t"

@patch("aws_util.iot_greengrass.get_client")
def test_list_deployments_pagination(mock_gc):
    client = MagicMock()
    client.list_deployments.side_effect = [
        {"deployments": [{"deploymentId": "d1"}], "nextToken": "t"},
        {"deployments": [{"deploymentId": "d2"}]},
    ]
    mock_gc.return_value = client
    assert len(list_deployments()) == 2

@patch("aws_util.iot_greengrass.get_client")
def test_list_deployments_error(mock_gc):
    client = MagicMock(); client.list_deployments.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): list_deployments()

@patch("aws_util.iot_greengrass.get_client")
def test_cancel_deployment(mock_gc):
    client = MagicMock()
    client.cancel_deployment.return_value = {"message": "ok"}
    mock_gc.return_value = client
    r = cancel_deployment("d1")
    assert "message" in r

@patch("aws_util.iot_greengrass.get_client")
def test_cancel_deployment_error(mock_gc):
    client = MagicMock(); client.cancel_deployment.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): cancel_deployment("d1")

# Core device operations
@patch("aws_util.iot_greengrass.get_client")
def test_list_effective_deployments(mock_gc):
    client = MagicMock()
    client.list_effective_deployments.return_value = {"effectiveDeployments": [{"deploymentId": "d1"}]}
    mock_gc.return_value = client
    assert len(list_effective_deployments("thing1")) == 1

@patch("aws_util.iot_greengrass.get_client")
def test_list_effective_deployments_pagination(mock_gc):
    client = MagicMock()
    client.list_effective_deployments.side_effect = [
        {"effectiveDeployments": [{"deploymentId": "d1"}], "nextToken": "t"},
        {"effectiveDeployments": [{"deploymentId": "d2"}]},
    ]
    mock_gc.return_value = client
    assert len(list_effective_deployments("thing1")) == 2

@patch("aws_util.iot_greengrass.get_client")
def test_list_effective_deployments_error(mock_gc):
    client = MagicMock(); client.list_effective_deployments.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): list_effective_deployments("thing1")

@patch("aws_util.iot_greengrass.get_client")
def test_list_installed_components(mock_gc):
    client = MagicMock()
    client.list_installed_components.return_value = {"installedComponents": [{"componentName": "c"}]}
    mock_gc.return_value = client
    assert len(list_installed_components("thing1")) == 1

@patch("aws_util.iot_greengrass.get_client")
def test_list_installed_components_pagination(mock_gc):
    client = MagicMock()
    client.list_installed_components.side_effect = [
        {"installedComponents": [{"componentName": "c1"}], "nextToken": "t"},
        {"installedComponents": [{"componentName": "c2"}]},
    ]
    mock_gc.return_value = client
    assert len(list_installed_components("thing1")) == 2

@patch("aws_util.iot_greengrass.get_client")
def test_list_installed_components_error(mock_gc):
    client = MagicMock(); client.list_installed_components.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): list_installed_components("thing1")

# Tagging
@patch("aws_util.iot_greengrass.get_client")
def test_tag_resource(mock_gc):
    client = MagicMock(); mock_gc.return_value = client
    tag_resource(COMP_ARN, tags={"k": "v"})
    client.tag_resource.assert_called_once_with(resourceArn=COMP_ARN, tags={"k": "v"})

@patch("aws_util.iot_greengrass.get_client")
def test_tag_resource_error(mock_gc):
    client = MagicMock(); client.tag_resource.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): tag_resource(COMP_ARN, tags={"k": "v"})

@patch("aws_util.iot_greengrass.get_client")
def test_list_tags_for_resource(mock_gc):
    client = MagicMock()
    client.list_tags_for_resource.return_value = {"tags": {"k": "v"}}
    mock_gc.return_value = client
    assert list_tags_for_resource(COMP_ARN) == {"k": "v"}

@patch("aws_util.iot_greengrass.get_client")
def test_list_tags_for_resource_error(mock_gc):
    client = MagicMock(); client.list_tags_for_resource.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError): list_tags_for_resource(COMP_ARN)


REGION = "us-east-1"


@patch("aws_util.iot_greengrass.get_client")
def test_associate_service_role_to_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_service_role_to_account.return_value = {}
    associate_service_role_to_account("test-role_arn", region_name=REGION)
    mock_client.associate_service_role_to_account.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_associate_service_role_to_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_service_role_to_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_service_role_to_account",
    )
    with pytest.raises(RuntimeError, match="Failed to associate service role to account"):
        associate_service_role_to_account("test-role_arn", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_batch_associate_client_device_with_core_device(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_client_device_with_core_device.return_value = {}
    batch_associate_client_device_with_core_device("test-core_device_thing_name", region_name=REGION)
    mock_client.batch_associate_client_device_with_core_device.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_batch_associate_client_device_with_core_device_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_client_device_with_core_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_client_device_with_core_device",
    )
    with pytest.raises(RuntimeError, match="Failed to batch associate client device with core device"):
        batch_associate_client_device_with_core_device("test-core_device_thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_batch_disassociate_client_device_from_core_device(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_client_device_from_core_device.return_value = {}
    batch_disassociate_client_device_from_core_device("test-core_device_thing_name", region_name=REGION)
    mock_client.batch_disassociate_client_device_from_core_device.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_batch_disassociate_client_device_from_core_device_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_client_device_from_core_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_client_device_from_core_device",
    )
    with pytest.raises(RuntimeError, match="Failed to batch disassociate client device from core device"):
        batch_disassociate_client_device_from_core_device("test-core_device_thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_delete_core_device(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_core_device.return_value = {}
    delete_core_device("test-core_device_thing_name", region_name=REGION)
    mock_client.delete_core_device.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_delete_core_device_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_core_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_core_device",
    )
    with pytest.raises(RuntimeError, match="Failed to delete core device"):
        delete_core_device("test-core_device_thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_delete_deployment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_deployment.return_value = {}
    delete_deployment("test-deployment_id", region_name=REGION)
    mock_client.delete_deployment.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_delete_deployment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_deployment",
    )
    with pytest.raises(RuntimeError, match="Failed to delete deployment"):
        delete_deployment("test-deployment_id", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_disassociate_service_role_from_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_service_role_from_account.return_value = {}
    disassociate_service_role_from_account(region_name=REGION)
    mock_client.disassociate_service_role_from_account.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_disassociate_service_role_from_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_service_role_from_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_service_role_from_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate service role from account"):
        disassociate_service_role_from_account(region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_get_component_version_artifact(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_component_version_artifact.return_value = {}
    get_component_version_artifact("test-arn", "test-artifact_name", region_name=REGION)
    mock_client.get_component_version_artifact.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_get_component_version_artifact_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_component_version_artifact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_component_version_artifact",
    )
    with pytest.raises(RuntimeError, match="Failed to get component version artifact"):
        get_component_version_artifact("test-arn", "test-artifact_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_get_connectivity_info(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_connectivity_info.return_value = {}
    get_connectivity_info("test-thing_name", region_name=REGION)
    mock_client.get_connectivity_info.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_get_connectivity_info_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_connectivity_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connectivity_info",
    )
    with pytest.raises(RuntimeError, match="Failed to get connectivity info"):
        get_connectivity_info("test-thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_get_core_device(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_core_device.return_value = {}
    get_core_device("test-core_device_thing_name", region_name=REGION)
    mock_client.get_core_device.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_get_core_device_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_core_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_core_device",
    )
    with pytest.raises(RuntimeError, match="Failed to get core device"):
        get_core_device("test-core_device_thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_get_service_role_for_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_service_role_for_account.return_value = {}
    get_service_role_for_account(region_name=REGION)
    mock_client.get_service_role_for_account.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_get_service_role_for_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_service_role_for_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_role_for_account",
    )
    with pytest.raises(RuntimeError, match="Failed to get service role for account"):
        get_service_role_for_account(region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_list_client_devices_associated_with_core_device(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_client_devices_associated_with_core_device.return_value = {}
    list_client_devices_associated_with_core_device("test-core_device_thing_name", region_name=REGION)
    mock_client.list_client_devices_associated_with_core_device.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_list_client_devices_associated_with_core_device_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_client_devices_associated_with_core_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_client_devices_associated_with_core_device",
    )
    with pytest.raises(RuntimeError, match="Failed to list client devices associated with core device"):
        list_client_devices_associated_with_core_device("test-core_device_thing_name", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_list_component_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_component_versions.return_value = {}
    list_component_versions("test-arn", region_name=REGION)
    mock_client.list_component_versions.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_list_component_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_component_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_component_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list component versions"):
        list_component_versions("test-arn", region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_list_core_devices(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_core_devices.return_value = {}
    list_core_devices(region_name=REGION)
    mock_client.list_core_devices.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_list_core_devices_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_core_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_core_devices",
    )
    with pytest.raises(RuntimeError, match="Failed to list core devices"):
        list_core_devices(region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_resolve_component_candidates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.resolve_component_candidates.return_value = {}
    resolve_component_candidates(region_name=REGION)
    mock_client.resolve_component_candidates.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_resolve_component_candidates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.resolve_component_candidates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resolve_component_candidates",
    )
    with pytest.raises(RuntimeError, match="Failed to resolve component candidates"):
        resolve_component_candidates(region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.iot_greengrass.get_client")
def test_update_connectivity_info(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_connectivity_info.return_value = {}
    update_connectivity_info("test-thing_name", [], region_name=REGION)
    mock_client.update_connectivity_info.assert_called_once()


@patch("aws_util.iot_greengrass.get_client")
def test_update_connectivity_info_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_connectivity_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connectivity_info",
    )
    with pytest.raises(RuntimeError, match="Failed to update connectivity info"):
        update_connectivity_info("test-thing_name", [], region_name=REGION)


def test_create_component_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import create_component_version
    mock_client = MagicMock()
    mock_client.create_component_version.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    create_component_version(inline_recipe="test-inline_recipe", lambda_function_recipe_source="test-lambda_function_recipe_source", region_name="us-east-1")
    mock_client.create_component_version.assert_called_once()

def test_get_component_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import get_component
    mock_client = MagicMock()
    mock_client.get_component.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    get_component("test-arn", recipe_output_format="test-recipe_output_format", region_name="us-east-1")
    mock_client.get_component.assert_called_once()

def test_batch_associate_client_device_with_core_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import batch_associate_client_device_with_core_device
    mock_client = MagicMock()
    mock_client.batch_associate_client_device_with_core_device.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    batch_associate_client_device_with_core_device("test-core_device_thing_name", entries="test-entries", region_name="us-east-1")
    mock_client.batch_associate_client_device_with_core_device.assert_called_once()

def test_batch_disassociate_client_device_from_core_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import batch_disassociate_client_device_from_core_device
    mock_client = MagicMock()
    mock_client.batch_disassociate_client_device_from_core_device.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    batch_disassociate_client_device_from_core_device("test-core_device_thing_name", entries="test-entries", region_name="us-east-1")
    mock_client.batch_disassociate_client_device_from_core_device.assert_called_once()

def test_get_component_version_artifact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import get_component_version_artifact
    mock_client = MagicMock()
    mock_client.get_component_version_artifact.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    get_component_version_artifact("test-arn", "test-artifact_name", s3_endpoint_type="test-s3_endpoint_type", iot_endpoint_type="test-iot_endpoint_type", region_name="us-east-1")
    mock_client.get_component_version_artifact.assert_called_once()

def test_list_client_devices_associated_with_core_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import list_client_devices_associated_with_core_device
    mock_client = MagicMock()
    mock_client.list_client_devices_associated_with_core_device.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    list_client_devices_associated_with_core_device("test-core_device_thing_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_client_devices_associated_with_core_device.assert_called_once()

def test_list_component_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import list_component_versions
    mock_client = MagicMock()
    mock_client.list_component_versions.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    list_component_versions("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_component_versions.assert_called_once()

def test_list_core_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import list_core_devices
    mock_client = MagicMock()
    mock_client.list_core_devices.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    list_core_devices(thing_group_arn="test-thing_group_arn", status="test-status", max_results=1, next_token="test-next_token", runtime="test-runtime", region_name="us-east-1")
    mock_client.list_core_devices.assert_called_once()

def test_resolve_component_candidates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import resolve_component_candidates
    mock_client = MagicMock()
    mock_client.resolve_component_candidates.return_value = {}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    resolve_component_candidates(platform="test-platform", component_candidates="test-component_candidates", region_name="us-east-1")
    mock_client.resolve_component_candidates.assert_called_once()


def test_create_deployment_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import create_deployment
    mock_client = MagicMock()
    mock_client.create_deployment.return_value = {"deploymentId": "d-1", "iotJobId": "j-1"}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: mock_client)
    create_deployment("arn:target", tags={"k": "v"}, region_name="us-east-1")
    mock_client.create_deployment.assert_called_once()


def test_create_deployment_all_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_greengrass import create_deployment
    m = MagicMock(); m.create_deployment.return_value = {"deploymentId": "d", "iotJobId": "j"}
    monkeypatch.setattr("aws_util.iot_greengrass.get_client", lambda *a, **kw: m)
    create_deployment("arn:target", deployment_name="dn", components={"c": {}}, deployment_policies={}, iot_job_configuration={}, tags={"k": "v"}, region_name="us-east-1")
