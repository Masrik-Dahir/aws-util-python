"""Tests for aws_util.aio.elastic_beanstalk -- 100% line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

import aws_util.aio.elastic_beanstalk as mod
from aws_util.aio.elastic_beanstalk import (
    ApplicationResult,
    ApplicationVersionResult,
    EnvironmentResult,
    EventResult,
    InstanceHealthResult,
    create_application,
    create_application_version,
    create_environment,
    delete_application,
    delete_application_version,
    describe_application_versions,
    describe_applications,
    describe_environments,
    describe_events,
    describe_instances_health,
    terminate_environment,
    update_environment,
    wait_for_environment,
    abort_environment_update,
    apply_environment_managed_action,
    associate_environment_operations_role,
    check_dns_availability,
    compose_environments,
    create_configuration_template,
    create_platform_version,
    create_storage_location,
    delete_configuration_template,
    delete_environment_configuration,
    delete_platform_version,
    describe_account_attributes,
    describe_configuration_options,
    describe_configuration_settings,
    describe_environment_health,
    describe_environment_managed_action_history,
    describe_environment_managed_actions,
    describe_environment_resources,
    describe_platform_version,
    disassociate_environment_operations_role,
    list_available_solution_stacks,
    list_platform_branches,
    list_platform_versions,
    list_tags_for_resource,
    rebuild_environment,
    request_environment_info,
    restart_app_server,
    retrieve_environment_info,
    swap_environment_cnames,
    update_application,
    update_application_resource_lifecycle,
    update_application_version,
    update_configuration_template,
    update_tags_for_resource,
    validate_configuration_settings,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError


REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------


_APP = {
    "ApplicationName": "myapp",
    "Description": "desc",
    "DateCreated": "2025-01-01",
    "DateUpdated": "2025-01-02",
    "Versions": ["v1"],
    "ExtraKey": "x",
}

_ENV = {
    "EnvironmentId": "e-123",
    "EnvironmentName": "myenv",
    "ApplicationName": "myapp",
    "Status": "Ready",
    "Health": "Green",
    "SolutionStackName": "64bit Amazon Linux 2",
    "CNAME": "myenv.elasticbeanstalk.com",
    "EndpointURL": "http://myenv.us-east-1.elasticbeanstalk.com",
    "VersionLabel": "v1",
    "ExtraEnv": "y",
}

_AV = {
    "ApplicationName": "myapp",
    "VersionLabel": "v1",
    "Description": "ver desc",
    "Status": "PROCESSED",
    "SourceBundle": {"S3Bucket": "b", "S3Key": "k"},
    "DateCreated": "2025-01-01",
    "ExtraAv": "z",
}

_EVT = {
    "EventDate": "2025-01-01T00:00:00Z",
    "Message": "event msg",
    "ApplicationName": "myapp",
    "EnvironmentName": "myenv",
    "Severity": "INFO",
    "ExtraEvt": "w",
}

_IH = {
    "InstanceId": "i-123",
    "HealthStatus": "Ok",
    "Color": "Green",
    "Causes": ["cause1"],
    "ExtraIh": "q",
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mc(monkeypatch):
    """Replace ``async_client`` so every function gets a mock client."""
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# create_application
# ---------------------------------------------------------------------------


async def test_create_application_success(mc):
    mc.call.return_value = {"Application": _APP}
    r = await create_application("myapp", description="desc")
    assert r.application_name == "myapp"


async def test_create_application_no_desc(mc):
    mc.call.return_value = {"Application": _APP}
    r = await create_application("myapp")
    assert isinstance(r, ApplicationResult)


async def test_create_application_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_application("myapp")


async def test_create_application_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_application failed"):
        await create_application("myapp")


# ---------------------------------------------------------------------------
# describe_applications
# ---------------------------------------------------------------------------


async def test_describe_applications_success(mc):
    mc.call.return_value = {"Applications": [_APP]}
    r = await describe_applications()
    assert len(r) == 1


async def test_describe_applications_with_names(mc):
    mc.call.return_value = {"Applications": [_APP]}
    r = await describe_applications(application_names=["myapp"])
    assert len(r) == 1


async def test_describe_applications_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_applications()


async def test_describe_applications_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_applications failed"):
        await describe_applications()


# ---------------------------------------------------------------------------
# delete_application
# ---------------------------------------------------------------------------


async def test_delete_application_success(mc):
    mc.call.return_value = {}
    await delete_application("myapp")
    mc.call.assert_called_once()


async def test_delete_application_force(mc):
    mc.call.return_value = {}
    await delete_application("myapp", terminate_env_by_force=True)
    kw = mc.call.call_args[1]
    assert kw["TerminateEnvByForce"] is True


async def test_delete_application_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application("myapp")


async def test_delete_application_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_application failed"):
        await delete_application("myapp")


# ---------------------------------------------------------------------------
# create_environment
# ---------------------------------------------------------------------------


async def test_create_environment_success(mc):
    mc.call.return_value = _ENV
    r = await create_environment("myapp", "myenv")
    assert r.environment_name == "myenv"


async def test_create_environment_all_opts(mc):
    mc.call.return_value = _ENV
    r = await create_environment(
        "myapp",
        "myenv",
        solution_stack_name="stack",
        version_label="v1",
        option_settings=[
            {"Namespace": "ns", "OptionName": "on", "Value": "v"}
        ],
    )
    assert r.environment_name == "myenv"


async def test_create_environment_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_environment("myapp", "myenv")


async def test_create_environment_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_environment failed"):
        await create_environment("myapp", "myenv")


# ---------------------------------------------------------------------------
# describe_environments
# ---------------------------------------------------------------------------


async def test_describe_environments_success(mc):
    mc.call.return_value = {"Environments": [_ENV]}
    r = await describe_environments()
    assert len(r) == 1


async def test_describe_environments_all_filters(mc):
    mc.call.return_value = {"Environments": [_ENV]}
    r = await describe_environments(
        application_name="myapp",
        environment_names=["myenv"],
        environment_ids=["e-123"],
    )
    assert len(r) == 1


async def test_describe_environments_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_environments()


async def test_describe_environments_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="describe_environments failed"
    ):
        await describe_environments()


# ---------------------------------------------------------------------------
# update_environment
# ---------------------------------------------------------------------------


async def test_update_environment_success(mc):
    mc.call.return_value = _ENV
    r = await update_environment("myenv")
    assert r.environment_name == "myenv"


async def test_update_environment_all_opts(mc):
    mc.call.return_value = _ENV
    r = await update_environment(
        "myenv",
        version_label="v2",
        option_settings=[
            {"Namespace": "ns", "OptionName": "on", "Value": "v"}
        ],
    )
    assert r.environment_name == "myenv"


async def test_update_environment_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_environment("myenv")


async def test_update_environment_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="update_environment failed"
    ):
        await update_environment("myenv")


# ---------------------------------------------------------------------------
# terminate_environment
# ---------------------------------------------------------------------------


async def test_terminate_environment_success(mc):
    mc.call.return_value = _ENV
    r = await terminate_environment("myenv")
    assert isinstance(r, EnvironmentResult)


async def test_terminate_environment_force(mc):
    mc.call.return_value = _ENV
    await terminate_environment("myenv", force_terminate=True)
    kw = mc.call.call_args[1]
    assert kw["ForceTerminate"] is True


async def test_terminate_environment_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await terminate_environment("myenv")


async def test_terminate_environment_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="terminate_environment failed"
    ):
        await terminate_environment("myenv")


# ---------------------------------------------------------------------------
# create_application_version
# ---------------------------------------------------------------------------


async def test_create_application_version_success(mc):
    mc.call.return_value = {"ApplicationVersion": _AV}
    r = await create_application_version(
        "myapp", "v1", description="d"
    )
    assert r.version_label == "v1"


async def test_create_application_version_with_source(mc):
    mc.call.return_value = {"ApplicationVersion": _AV}
    r = await create_application_version(
        "myapp",
        "v1",
        source_bundle={"S3Bucket": "b", "S3Key": "k"},
    )
    assert isinstance(r, ApplicationVersionResult)


async def test_create_application_version_no_desc(mc):
    mc.call.return_value = {"ApplicationVersion": _AV}
    r = await create_application_version("myapp", "v1")
    assert isinstance(r, ApplicationVersionResult)


async def test_create_application_version_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_application_version("myapp", "v1")


async def test_create_application_version_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="create_application_version failed"
    ):
        await create_application_version("myapp", "v1")


# ---------------------------------------------------------------------------
# describe_application_versions
# ---------------------------------------------------------------------------


async def test_describe_application_versions_success(mc):
    mc.call.return_value = {"ApplicationVersions": [_AV]}
    r = await describe_application_versions("myapp")
    assert len(r) == 1


async def test_describe_application_versions_with_labels(mc):
    mc.call.return_value = {"ApplicationVersions": [_AV]}
    r = await describe_application_versions(
        "myapp", version_labels=["v1"]
    )
    assert len(r) == 1


async def test_describe_application_versions_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_versions("myapp")


async def test_describe_application_versions_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="describe_application_versions failed"
    ):
        await describe_application_versions("myapp")


# ---------------------------------------------------------------------------
# delete_application_version
# ---------------------------------------------------------------------------


async def test_delete_application_version_success(mc):
    mc.call.return_value = {}
    await delete_application_version("myapp", "v1")
    mc.call.assert_called_once()


async def test_delete_application_version_with_source(mc):
    mc.call.return_value = {}
    await delete_application_version(
        "myapp", "v1", delete_source_bundle=True
    )
    kw = mc.call.call_args[1]
    assert kw["DeleteSourceBundle"] is True


async def test_delete_application_version_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_version("myapp", "v1")


async def test_delete_application_version_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="delete_application_version failed"
    ):
        await delete_application_version("myapp", "v1")


# ---------------------------------------------------------------------------
# describe_events
# ---------------------------------------------------------------------------


async def test_describe_events_success(mc):
    mc.call.return_value = {"Events": [_EVT]}
    r = await describe_events()
    assert len(r) == 1


async def test_describe_events_all_opts(mc):
    mc.call.return_value = {"Events": [_EVT]}
    r = await describe_events(
        application_name="myapp",
        environment_name="myenv",
        max_records=10,
    )
    assert len(r) == 1


async def test_describe_events_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_events_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_events failed"):
        await describe_events()


# ---------------------------------------------------------------------------
# describe_instances_health
# ---------------------------------------------------------------------------


async def test_describe_instances_health_success(mc):
    mc.call.return_value = {"InstanceHealthList": [_IH]}
    r = await describe_instances_health("myenv")
    assert len(r) == 1


async def test_describe_instances_health_with_attrs(mc):
    mc.call.return_value = {"InstanceHealthList": [_IH]}
    r = await describe_instances_health(
        "myenv", attribute_names=["HealthStatus"]
    )
    assert len(r) == 1


async def test_describe_instances_health_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instances_health("myenv")


async def test_describe_instances_health_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="describe_instances_health failed"
    ):
        await describe_instances_health("myenv")


# ---------------------------------------------------------------------------
# wait_for_environment
# ---------------------------------------------------------------------------


async def test_wait_already_ready(monkeypatch):
    env = EnvironmentResult(
        environment_id="e-1",
        environment_name="myenv",
        application_name="myapp",
        status="Ready",
    )
    monkeypatch.setattr(
        mod,
        "describe_environments",
        AsyncMock(return_value=[env]),
    )
    r = await wait_for_environment("myenv")
    assert r.status == "Ready"


async def test_wait_not_found(monkeypatch):
    monkeypatch.setattr(
        mod,
        "describe_environments",
        AsyncMock(return_value=[]),
    )
    with pytest.raises(AwsServiceError, match="not found"):
        await wait_for_environment("myenv", timeout=1)


async def test_wait_terminated(monkeypatch):
    env = EnvironmentResult(
        environment_id="e-1",
        environment_name="myenv",
        application_name="myapp",
        status="Terminated",
    )
    monkeypatch.setattr(
        mod,
        "describe_environments",
        AsyncMock(return_value=[env]),
    )
    with pytest.raises(AwsServiceError, match="was terminated"):
        await wait_for_environment("myenv", timeout=1)


async def test_wait_timeout(monkeypatch):
    env = EnvironmentResult(
        environment_id="e-1",
        environment_name="myenv",
        application_name="myapp",
        status="Launching",
    )
    monkeypatch.setattr(
        mod,
        "describe_environments",
        AsyncMock(return_value=[env]),
    )
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.asyncio.sleep", AsyncMock()
    )
    counter = {"val": 0.0}

    def fake_monotonic():
        counter["val"] += 1000.0
        return counter["val"]

    monkeypatch.setattr(time, "monotonic", fake_monotonic)
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_environment(
            "myenv", timeout=1.0, poll_interval=0.001
        )


async def test_wait_polls_then_ready(monkeypatch):
    launching = EnvironmentResult(
        environment_id="e-1",
        environment_name="myenv",
        application_name="myapp",
        status="Launching",
    )
    ready = EnvironmentResult(
        environment_id="e-1",
        environment_name="myenv",
        application_name="myapp",
        status="Ready",
    )
    monkeypatch.setattr(
        mod,
        "describe_environments",
        AsyncMock(side_effect=[[launching], [ready]]),
    )
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.asyncio.sleep", AsyncMock()
    )
    r = await wait_for_environment(
        "myenv", timeout=9999.0, poll_interval=0.001
    )
    assert r.status == "Ready"


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_abort_environment_update(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await abort_environment_update()
    mock_client.call.assert_called_once()


async def test_abort_environment_update_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await abort_environment_update()


async def test_apply_environment_managed_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_environment_managed_action("test-action_id", )
    mock_client.call.assert_called_once()


async def test_apply_environment_managed_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_environment_managed_action("test-action_id", )


async def test_associate_environment_operations_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_environment_operations_role("test-environment_name", "test-operations_role", )
    mock_client.call.assert_called_once()


async def test_associate_environment_operations_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_environment_operations_role("test-environment_name", "test-operations_role", )


async def test_check_dns_availability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await check_dns_availability("test-cname_prefix", )
    mock_client.call.assert_called_once()


async def test_check_dns_availability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_dns_availability("test-cname_prefix", )


async def test_compose_environments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await compose_environments()
    mock_client.call.assert_called_once()


async def test_compose_environments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await compose_environments()


async def test_create_configuration_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_configuration_template("test-application_name", "test-template_name", )
    mock_client.call.assert_called_once()


async def test_create_configuration_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_template("test-application_name", "test-template_name", )


async def test_create_platform_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_platform_version("test-platform_name", "test-platform_version", {}, )
    mock_client.call.assert_called_once()


async def test_create_platform_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_platform_version("test-platform_name", "test-platform_version", {}, )


async def test_create_storage_location(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_storage_location()
    mock_client.call.assert_called_once()


async def test_create_storage_location_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_storage_location()


async def test_delete_configuration_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_configuration_template("test-application_name", "test-template_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_template("test-application_name", "test-template_name", )


async def test_delete_environment_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_environment_configuration("test-application_name", "test-environment_name", )
    mock_client.call.assert_called_once()


async def test_delete_environment_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_environment_configuration("test-application_name", "test-environment_name", )


async def test_delete_platform_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_platform_version()
    mock_client.call.assert_called_once()


async def test_delete_platform_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_platform_version()


async def test_describe_account_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_attributes()
    mock_client.call.assert_called_once()


async def test_describe_account_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_attributes()


async def test_describe_configuration_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_configuration_options()
    mock_client.call.assert_called_once()


async def test_describe_configuration_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_options()


async def test_describe_configuration_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_configuration_settings("test-application_name", )
    mock_client.call.assert_called_once()


async def test_describe_configuration_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_settings("test-application_name", )


async def test_describe_environment_health(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_environment_health()
    mock_client.call.assert_called_once()


async def test_describe_environment_health_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_environment_health()


async def test_describe_environment_managed_action_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_environment_managed_action_history()
    mock_client.call.assert_called_once()


async def test_describe_environment_managed_action_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_environment_managed_action_history()


async def test_describe_environment_managed_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_environment_managed_actions()
    mock_client.call.assert_called_once()


async def test_describe_environment_managed_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_environment_managed_actions()


async def test_describe_environment_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_environment_resources()
    mock_client.call.assert_called_once()


async def test_describe_environment_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_environment_resources()


async def test_describe_platform_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_platform_version()
    mock_client.call.assert_called_once()


async def test_describe_platform_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_platform_version()


async def test_disassociate_environment_operations_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_environment_operations_role("test-environment_name", )
    mock_client.call.assert_called_once()


async def test_disassociate_environment_operations_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_environment_operations_role("test-environment_name", )


async def test_list_available_solution_stacks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_available_solution_stacks()
    mock_client.call.assert_called_once()


async def test_list_available_solution_stacks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_available_solution_stacks()


async def test_list_platform_branches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_platform_branches()
    mock_client.call.assert_called_once()


async def test_list_platform_branches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_platform_branches()


async def test_list_platform_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_platform_versions()
    mock_client.call.assert_called_once()


async def test_list_platform_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_platform_versions()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_rebuild_environment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await rebuild_environment()
    mock_client.call.assert_called_once()


async def test_rebuild_environment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rebuild_environment()


async def test_request_environment_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await request_environment_info("test-info_type", )
    mock_client.call.assert_called_once()


async def test_request_environment_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await request_environment_info("test-info_type", )


async def test_restart_app_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await restart_app_server()
    mock_client.call.assert_called_once()


async def test_restart_app_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restart_app_server()


async def test_retrieve_environment_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await retrieve_environment_info("test-info_type", )
    mock_client.call.assert_called_once()


async def test_retrieve_environment_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retrieve_environment_info("test-info_type", )


async def test_swap_environment_cnames(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await swap_environment_cnames()
    mock_client.call.assert_called_once()


async def test_swap_environment_cnames_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await swap_environment_cnames()


async def test_update_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application("test-application_name", )
    mock_client.call.assert_called_once()


async def test_update_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application("test-application_name", )


async def test_update_application_resource_lifecycle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application_resource_lifecycle("test-application_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_application_resource_lifecycle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application_resource_lifecycle("test-application_name", {}, )


async def test_update_application_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application_version("test-application_name", "test-version_label", )
    mock_client.call.assert_called_once()


async def test_update_application_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application_version("test-application_name", "test-version_label", )


async def test_update_configuration_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration_template("test-application_name", "test-template_name", )
    mock_client.call.assert_called_once()


async def test_update_configuration_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_template("test-application_name", "test-template_name", )


async def test_update_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_update_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_tags_for_resource("test-resource_arn", )


async def test_validate_configuration_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_configuration_settings("test-application_name", [], )
    mock_client.call.assert_called_once()


async def test_validate_configuration_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elastic_beanstalk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_configuration_settings("test-application_name", [], )


@pytest.mark.asyncio
async def test_describe_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_applications(application_names="test-application_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_environment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import create_environment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await create_environment("test-application_name", "test-environment_name", solution_stack_name="test-solution_stack_name", version_label="test-version_label", option_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_environments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_environments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_environments(application_name="test-application_name", environment_names="test-environment_names", environment_ids="test-environment_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_environment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import update_environment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await update_environment("test-environment_name", version_label="test-version_label", option_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_application_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_application_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_application_versions("test-application_name", version_labels="test-version_labels", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_events(application_name="test-application_name", environment_name="test-environment_name", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instances_health_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_instances_health
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_instances_health("test-environment_name", attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_abort_environment_update_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import abort_environment_update
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await abort_environment_update(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_apply_environment_managed_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import apply_environment_managed_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await apply_environment_managed_action("test-action_id", environment_name="test-environment_name", environment_id="test-environment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_compose_environments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import compose_environments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await compose_environments(application_name="test-application_name", group_name="test-group_name", version_labels="test-version_labels", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_configuration_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import create_configuration_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await create_configuration_template("test-application_name", "test-template_name", solution_stack_name="test-solution_stack_name", platform_arn="test-platform_arn", source_configuration={}, environment_id="test-environment_id", description="test-description", option_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_platform_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import create_platform_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await create_platform_version("test-platform_name", "test-platform_version", {}, environment_name="test-environment_name", option_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_platform_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import delete_platform_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await delete_platform_version(platform_arn="test-platform_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_configuration_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_configuration_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_configuration_options(application_name="test-application_name", template_name="test-template_name", environment_name="test-environment_name", solution_stack_name="test-solution_stack_name", platform_arn="test-platform_arn", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_configuration_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_configuration_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_configuration_settings("test-application_name", template_name="test-template_name", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_environment_health_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_environment_health
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_environment_health(environment_name="test-environment_name", environment_id="test-environment_id", attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_environment_managed_action_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_environment_managed_action_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_environment_managed_action_history(environment_id="test-environment_id", environment_name="test-environment_name", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_environment_managed_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_environment_managed_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_environment_managed_actions(environment_name="test-environment_name", environment_id="test-environment_id", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_environment_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_environment_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_environment_resources(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_platform_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import describe_platform_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await describe_platform_version(platform_arn="test-platform_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_platform_branches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import list_platform_branches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await list_platform_branches(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_platform_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import list_platform_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await list_platform_versions(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_rebuild_environment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import rebuild_environment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await rebuild_environment(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_request_environment_info_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import request_environment_info
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await request_environment_info("test-info_type", environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restart_app_server_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import restart_app_server
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await restart_app_server(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_environment_info_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import retrieve_environment_info
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await retrieve_environment_info("test-info_type", environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_swap_environment_cnames_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import swap_environment_cnames
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await swap_environment_cnames(source_environment_id="test-source_environment_id", source_environment_name="test-source_environment_name", destination_environment_id="test-destination_environment_id", destination_environment_name="test-destination_environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import update_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await update_application("test-application_name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_application_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import update_application_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await update_application_version("test-application_name", "test-version_label", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_configuration_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import update_configuration_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await update_configuration_template("test-application_name", "test-template_name", description="test-description", option_settings={}, options_to_remove={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import update_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await update_tags_for_resource("test-resource_arn", tags_to_add=[{"Key": "k", "Value": "v"}], tags_to_remove=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_configuration_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elastic_beanstalk import validate_configuration_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elastic_beanstalk.async_client", lambda *a, **kw: mock_client)
    await validate_configuration_settings("test-application_name", {}, template_name="test-template_name", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
