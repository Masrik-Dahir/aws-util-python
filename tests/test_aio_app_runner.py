"""Tests for aws_util.aio.app_runner — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.app_runner import (
    AppRunnerAutoScalingConfig,
    AppRunnerConnection,
    AppRunnerObservabilityConfig,
    AppRunnerOperation,
    AppRunnerService,
    AppRunnerServiceSummary,
    _TERMINAL_STATUSES,
    create_auto_scaling_configuration,
    create_connection,
    create_observability_configuration,
    create_service,
    delete_service,
    describe_service,
    list_auto_scaling_configurations,
    list_connections,
    list_operations,
    list_services,
    pause_service,
    resume_service,
    start_deployment,
    update_service,
    wait_for_service,
    associate_custom_domain,
    create_vpc_connector,
    create_vpc_ingress_connection,
    delete_auto_scaling_configuration,
    delete_connection,
    delete_observability_configuration,
    delete_vpc_connector,
    delete_vpc_ingress_connection,
    describe_auto_scaling_configuration,
    describe_custom_domains,
    describe_observability_configuration,
    describe_vpc_connector,
    describe_vpc_ingress_connection,
    disassociate_custom_domain,
    list_observability_configurations,
    list_services_for_auto_scaling_configuration,
    list_tags_for_resource,
    list_vpc_connectors,
    list_vpc_ingress_connections,
    tag_resource,
    untag_resource,
    update_default_auto_scaling_configuration,
    update_vpc_ingress_connection,
)



REGION = "us-east-1"

SVC_ARN = "arn:aws:apprunner:us-east-1:123:service/my-svc/abc"
SOURCE_CFG: dict = {
    "ImageRepository": {
        "ImageIdentifier": "public.ecr.aws/...",
        "ImageRepositoryType": "ECR_PUBLIC",
    }
}


def _mock_factory(mock_client):  # noqa: ANN001
    return lambda *a, **kw: mock_client


def _service_dict(**overrides):  # noqa: ANN003
    d = {
        "ServiceId": "svc-123",
        "ServiceName": "my-svc",
        "ServiceArn": SVC_ARN,
        "ServiceUrl": "abc.us-east-1.awsapprunner.com",
        "Status": "RUNNING",
        "CreatedAt": "2024-01-01T00:00:00Z",
    }
    d.update(overrides)
    return d


def _svc_summary_dict(**overrides):  # noqa: ANN003
    d = {
        "ServiceName": "my-svc",
        "ServiceArn": SVC_ARN,
        "ServiceId": "svc-123",
        "Status": "RUNNING",
        "ServiceUrl": "abc.us-east-1.awsapprunner.com",
        "CreatedAt": "2024-01-01T00:00:00Z",
    }
    d.update(overrides)
    return d


def _auto_scaling_dict(**overrides):  # noqa: ANN003
    d = {
        "AutoScalingConfigurationArn": (
            "arn:aws:apprunner:us-east-1:123:autoscalingconfiguration/asc/1"
        ),
        "AutoScalingConfigurationName": "asc-1",
        "AutoScalingConfigurationRevision": 1,
        "MaxConcurrency": 100,
        "MaxSize": 25,
        "MinSize": 1,
        "Status": "ACTIVE",
    }
    d.update(overrides)
    return d


def _connection_dict(**overrides):  # noqa: ANN003
    d = {
        "ConnectionArn": "arn:aws:apprunner:us-east-1:123:connection/conn-1/id",
        "ConnectionName": "conn-1",
        "ProviderType": "GITHUB",
        "Status": "AVAILABLE",
        "CreatedAt": "2024-01-01T00:00:00Z",
    }
    d.update(overrides)
    return d


def _observability_dict(**overrides):  # noqa: ANN003
    d = {
        "ObservabilityConfigurationArn": (
            "arn:aws:apprunner:us-east-1:123:observabilityconfiguration/obs-1/1"
        ),
        "ObservabilityConfigurationName": "obs-1",
        "ObservabilityConfigurationRevision": 1,
        "TraceConfiguration": {"Vendor": "AWSXRAY"},
        "Status": "ACTIVE",
    }
    d.update(overrides)
    return d


def _operation_dict(**overrides):  # noqa: ANN003
    d = {
        "Id": "op-1",
        "Type": "CREATE_SERVICE",
        "Status": "SUCCEEDED",
        "TargetArn": SVC_ARN,
        "StartedAt": "2024-01-01T00:00:00Z",
        "EndedAt": "2024-01-01T00:01:00Z",
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Service operations
# ---------------------------------------------------------------------------


async def test_create_service_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_service("my-svc", SOURCE_CFG, region_name=REGION)
    assert isinstance(result, AppRunnerService)
    assert result.service_name == "my-svc"


async def test_create_service_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_service(
        "my-svc",
        SOURCE_CFG,
        instance_configuration={"Cpu": "1024", "Memory": "2048"},
        tags=[{"Key": "env", "Value": "test"}],
        auto_scaling_configuration_arn="arn:...",
        health_check_configuration={"Protocol": "TCP"},
        region_name=REGION,
    )
    assert result.service_name == "my-svc"


async def test_create_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_service("svc", SOURCE_CFG, region_name=REGION)


async def test_describe_service_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await describe_service(SVC_ARN, region_name=REGION)
    assert result.service_arn == SVC_ARN


async def test_describe_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_service(SVC_ARN, region_name=REGION)


async def test_list_services_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_svc_summary_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_services(region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerServiceSummary)


async def test_list_services_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_services(region_name=REGION)


async def test_delete_service_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Service": _service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await delete_service(SVC_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


async def test_delete_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_service(SVC_ARN, region_name=REGION)


async def test_update_service_all_params(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await update_service(
        SVC_ARN,
        source_configuration=SOURCE_CFG,
        instance_configuration={"Cpu": "2048"},
        auto_scaling_configuration_arn="arn:...",
        health_check_configuration={"Protocol": "HTTP"},
        region_name=REGION,
    )
    assert result.service_name == "my-svc"


async def test_update_service_minimal(monkeypatch):
    """Covers the None branches for optional kwargs."""
    client = AsyncMock()
    client.call.return_value = {"Service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await update_service(SVC_ARN, region_name=REGION)
    assert isinstance(result, AppRunnerService)


async def test_update_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await update_service(SVC_ARN, region_name=REGION)


async def test_pause_service_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Service": _service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await pause_service(SVC_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


async def test_pause_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await pause_service(SVC_ARN, region_name=REGION)


async def test_resume_service_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Service": _service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await resume_service(SVC_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


async def test_resume_service_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await resume_service(SVC_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Auto-scaling configurations
# ---------------------------------------------------------------------------


async def test_create_auto_scaling_config_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "AutoScalingConfiguration": _auto_scaling_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_auto_scaling_configuration(
        "asc-1",
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerAutoScalingConfig)
    assert result.auto_scaling_configuration_name == "asc-1"
    assert result.max_concurrency == 100


async def test_create_auto_scaling_config_no_tags(monkeypatch):
    """Covers the tags=None branch."""
    client = AsyncMock()
    client.call.return_value = {
        "AutoScalingConfiguration": _auto_scaling_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_auto_scaling_configuration(
        "asc-1",
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerAutoScalingConfig)


async def test_create_auto_scaling_config_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_auto_scaling_configuration("asc", region_name=REGION)


async def test_list_auto_scaling_configs_with_name(monkeypatch):
    """Covers the name-filter branch."""
    client = AsyncMock()
    client.paginate.return_value = [_auto_scaling_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_auto_scaling_configurations(
        auto_scaling_configuration_name="asc-1",
        region_name=REGION,
    )
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerAutoScalingConfig)


async def test_list_auto_scaling_configs_no_name(monkeypatch):
    """Covers the no-filter branch."""
    client = AsyncMock()
    client.paginate.return_value = [_auto_scaling_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_auto_scaling_configurations(region_name=REGION)
    assert len(result) == 1


async def test_list_auto_scaling_configs_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_auto_scaling_configurations(region_name=REGION)


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------


async def test_create_connection_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Connection": _connection_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_connection(
        "conn-1",
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerConnection)
    assert result.connection_name == "conn-1"


async def test_create_connection_no_tags(monkeypatch):
    """Covers the tags=None branch."""
    client = AsyncMock()
    client.call.return_value = {
        "Connection": _connection_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_connection("conn-1", region_name=REGION)
    assert result.provider_type == "GITHUB"


async def test_create_connection_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_connection("conn", region_name=REGION)


async def test_list_connections_with_name(monkeypatch):
    """Covers the connection_name filter branch."""
    client = AsyncMock()
    client.paginate.return_value = [_connection_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_connections(
        connection_name="conn-1",
        region_name=REGION,
    )
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerConnection)


async def test_list_connections_no_name(monkeypatch):
    """Covers the no-filter branch."""
    client = AsyncMock()
    client.paginate.return_value = [_connection_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_connections(region_name=REGION)
    assert len(result) == 1


async def test_list_connections_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_connections(region_name=REGION)


# ---------------------------------------------------------------------------
# Observability
# ---------------------------------------------------------------------------


async def test_create_observability_config_all_params(monkeypatch):
    """Covers both trace_configuration and tags branches."""
    client = AsyncMock()
    client.call.return_value = {
        "ObservabilityConfiguration": _observability_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_observability_configuration(
        "obs-1",
        trace_configuration={"Vendor": "AWSXRAY"},
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerObservabilityConfig)
    assert result.observability_configuration_name == "obs-1"


async def test_create_observability_config_minimal(monkeypatch):
    """Covers the None branches for trace_configuration and tags."""
    client = AsyncMock()
    client.call.return_value = {
        "ObservabilityConfiguration": _observability_dict(),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await create_observability_configuration(
        "obs-1",
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerObservabilityConfig)


async def test_create_observability_config_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_observability_configuration("obs", region_name=REGION)


# ---------------------------------------------------------------------------
# Deployments & operations
# ---------------------------------------------------------------------------


async def test_start_deployment_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"OperationId": "op-123"}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await start_deployment(SVC_ARN, region_name=REGION)
    assert result == "op-123"


async def test_start_deployment_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await start_deployment(SVC_ARN, region_name=REGION)


async def test_list_operations_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_operation_dict()]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await list_operations(SVC_ARN, region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerOperation)


async def test_list_operations_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_operations(SVC_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_service
# ---------------------------------------------------------------------------


async def test_wait_for_service_immediate(monkeypatch):
    """Service already in terminal status -- no polling needed."""
    client = AsyncMock()
    client.call.return_value = {
        "Service": _service_dict(Status="RUNNING"),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    result = await wait_for_service(
        SVC_ARN, timeout=5, region_name=REGION,
    )
    assert result.status == "RUNNING"


async def test_wait_for_service_polls_then_succeeds(monkeypatch):
    """Service transitions from non-terminal to terminal after one poll."""
    client = AsyncMock()
    client.call.side_effect = [
        {"Service": _service_dict(Status="OPERATION_IN_PROGRESS")},
        {"Service": _service_dict(Status="RUNNING")},
    ]
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    monkeypatch.setattr(
        "aws_util.aio.app_runner.asyncio.sleep",
        AsyncMock(),
    )
    result = await wait_for_service(
        SVC_ARN, timeout=600, poll_interval=1, region_name=REGION,
    )
    assert result.status == "RUNNING"


async def test_wait_for_service_timeout(monkeypatch):
    """Service never reaches terminal status -- times out."""
    client = AsyncMock()
    client.call.return_value = {
        "Service": _service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        _mock_factory(client),
    )
    monkeypatch.setattr(
        "aws_util.aio.app_runner.asyncio.sleep",
        AsyncMock(),
    )
    import aws_util.aio.app_runner as _ar_mod


    call_count = 0

    def _monotonic():
        nonlocal call_count
        call_count += 1
        # First call sets deadline (0.0 + 0.0 = 0.0).
        # Second call returns 1.0, exceeding the deadline.
        return 0.0 if call_count <= 1 else 1.0

    monkeypatch.setattr(_ar_mod._time, "monotonic", _monotonic)

    with pytest.raises(
        TimeoutError, match="did not reach a terminal status"
    ):
        await wait_for_service(
            SVC_ARN,
            timeout=0.0,
            poll_interval=0.1,
            region_name=REGION,
        )


async def test_associate_custom_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_custom_domain("test-service_arn", "test-domain_name", )
    mock_client.call.assert_called_once()


async def test_associate_custom_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_custom_domain("test-service_arn", "test-domain_name", )


async def test_create_vpc_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_connector("test-vpc_connector_name", [], )
    mock_client.call.assert_called_once()


async def test_create_vpc_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_connector("test-vpc_connector_name", [], )


async def test_create_vpc_ingress_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_vpc_ingress_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, )


async def test_delete_auto_scaling_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_auto_scaling_configuration("test-auto_scaling_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_auto_scaling_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_auto_scaling_configuration("test-auto_scaling_configuration_arn", )


async def test_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connection("test-connection_arn", )
    mock_client.call.assert_called_once()


async def test_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection("test-connection_arn", )


async def test_delete_observability_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_observability_configuration("test-observability_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_observability_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_observability_configuration("test-observability_configuration_arn", )


async def test_delete_vpc_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_connector("test-vpc_connector_arn", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_connector("test-vpc_connector_arn", )


async def test_delete_vpc_ingress_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_ingress_connection("test-vpc_ingress_connection_arn", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_ingress_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_ingress_connection("test-vpc_ingress_connection_arn", )


async def test_describe_auto_scaling_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_auto_scaling_configuration("test-auto_scaling_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_describe_auto_scaling_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_auto_scaling_configuration("test-auto_scaling_configuration_arn", )


async def test_describe_custom_domains(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_domains("test-service_arn", )
    mock_client.call.assert_called_once()


async def test_describe_custom_domains_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_domains("test-service_arn", )


async def test_describe_observability_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_observability_configuration("test-observability_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_describe_observability_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_observability_configuration("test-observability_configuration_arn", )


async def test_describe_vpc_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_connector("test-vpc_connector_arn", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_connector("test-vpc_connector_arn", )


async def test_describe_vpc_ingress_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_ingress_connection("test-vpc_ingress_connection_arn", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_ingress_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_ingress_connection("test-vpc_ingress_connection_arn", )


async def test_disassociate_custom_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_custom_domain("test-service_arn", "test-domain_name", )
    mock_client.call.assert_called_once()


async def test_disassociate_custom_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_custom_domain("test-service_arn", "test-domain_name", )


async def test_list_observability_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_observability_configurations()
    mock_client.call.assert_called_once()


async def test_list_observability_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_observability_configurations()


async def test_list_services_for_auto_scaling_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_services_for_auto_scaling_configuration("test-auto_scaling_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_list_services_for_auto_scaling_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_services_for_auto_scaling_configuration("test-auto_scaling_configuration_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_vpc_connectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vpc_connectors()
    mock_client.call.assert_called_once()


async def test_list_vpc_connectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_connectors()


async def test_list_vpc_ingress_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vpc_ingress_connections()
    mock_client.call.assert_called_once()


async def test_list_vpc_ingress_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_ingress_connections()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_default_auto_scaling_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_default_auto_scaling_configuration("test-auto_scaling_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_update_default_auto_scaling_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_default_auto_scaling_configuration("test-auto_scaling_configuration_arn", )


async def test_update_vpc_ingress_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_vpc_ingress_connection("test-vpc_ingress_connection_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_vpc_ingress_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.app_runner.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_vpc_ingress_connection("test-vpc_ingress_connection_arn", {}, )


@pytest.mark.asyncio
async def test_associate_custom_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import associate_custom_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await associate_custom_domain("test-service_arn", "test-domain_name", enable_www_subdomain=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_connector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import create_vpc_connector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await create_vpc_connector("test-vpc_connector_name", "test-subnets", security_groups="test-security_groups", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_ingress_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import create_vpc_ingress_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_auto_scaling_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import delete_auto_scaling_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await delete_auto_scaling_configuration(True, delete_all_revisions=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_custom_domains_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import describe_custom_domains
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await describe_custom_domains("test-service_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_observability_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import list_observability_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await list_observability_configurations(observability_configuration_name={}, latest_only="test-latest_only", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_services_for_auto_scaling_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import list_services_for_auto_scaling_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await list_services_for_auto_scaling_configuration(True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_connectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import list_vpc_connectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await list_vpc_connectors(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_ingress_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.app_runner import list_vpc_ingress_connections



    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.app_runner.async_client", lambda *a, **kw: mock_client)
    await list_vpc_ingress_connections(filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
