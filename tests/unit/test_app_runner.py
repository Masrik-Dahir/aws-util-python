"""Tests for aws_util.app_runner module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.app_runner as ar_mod
from aws_util.app_runner import (
    AppRunnerAutoScalingConfig,
    AppRunnerConnection,
    AppRunnerObservabilityConfig,
    AppRunnerOperation,
    AppRunnerService,
    AppRunnerServiceSummary,
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
SERVICE_ARN = "arn:aws:apprunner:us-east-1:123456789012:service/my-svc/id123"
SERVICE_NAME = "my-svc"
SERVICE_ID = "id123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service_dict(**kwargs) -> dict:
    defaults = {
        "ServiceArn": SERVICE_ARN,
        "ServiceName": SERVICE_NAME,
        "ServiceId": SERVICE_ID,
        "ServiceUrl": "abc123.us-east-1.awsapprunner.com",
        "Status": "RUNNING",
        "CreatedAt": "2024-01-01T00:00:00Z",
        "UpdatedAt": "2024-01-01T00:00:00Z",
    }
    defaults.update(kwargs)
    return defaults


def _make_service_summary_dict(**kwargs) -> dict:
    defaults = {
        "ServiceArn": SERVICE_ARN,
        "ServiceName": SERVICE_NAME,
        "ServiceId": SERVICE_ID,
        "Status": "RUNNING",
        "ServiceUrl": "abc123.us-east-1.awsapprunner.com",
        "CreatedAt": "2024-01-01T00:00:00Z",
        "UpdatedAt": "2024-01-01T00:00:00Z",
    }
    defaults.update(kwargs)
    return defaults


def _make_auto_scaling_dict(**kwargs) -> dict:
    defaults = {
        "AutoScalingConfigurationArn": (
            "arn:aws:apprunner:us-east-1:123:autoscalingconfiguration/asc/1"
        ),
        "AutoScalingConfigurationName": "default-asc",
        "AutoScalingConfigurationRevision": 1,
        "MaxConcurrency": 100,
        "MaxSize": 25,
        "MinSize": 1,
        "Status": "ACTIVE",
    }
    defaults.update(kwargs)
    return defaults


def _make_connection_dict(**kwargs) -> dict:
    defaults = {
        "ConnectionArn": "arn:aws:apprunner:us-east-1:123:connection/my-conn/id",
        "ConnectionName": "my-conn",
        "ProviderType": "GITHUB",
        "Status": "AVAILABLE",
        "CreatedAt": "2024-01-01T00:00:00Z",
    }
    defaults.update(kwargs)
    return defaults


def _make_observability_dict(**kwargs) -> dict:
    defaults = {
        "ObservabilityConfigurationArn": (
            "arn:aws:apprunner:us-east-1:123:observabilityconfiguration/oc/1"
        ),
        "ObservabilityConfigurationName": "my-oc",
        "ObservabilityConfigurationRevision": 1,
        "TraceConfiguration": {"Vendor": "AWSXRAY"},
        "Status": "ACTIVE",
    }
    defaults.update(kwargs)
    return defaults


def _make_operation_dict(**kwargs) -> dict:
    defaults = {
        "Id": "op-123",
        "Type": "CREATE_SERVICE",
        "Status": "SUCCEEDED",
        "TargetArn": SERVICE_ARN,
        "StartedAt": "2024-01-01T00:00:00Z",
        "EndedAt": "2024-01-01T00:01:00Z",
    }
    defaults.update(kwargs)
    return defaults


def _client_error(code: str = "InvalidRequestException", msg: str = "error") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "Op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_app_runner_service_model():
    svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="RUNNING",
    )
    assert svc.service_arn == SERVICE_ARN
    assert svc.service_url is None


def test_app_runner_service_summary_model():
    summary = AppRunnerServiceSummary(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="RUNNING",
    )
    assert summary.status == "RUNNING"


def test_app_runner_auto_scaling_model():
    cfg = AppRunnerAutoScalingConfig(
        auto_scaling_configuration_arn="arn:...",
        auto_scaling_configuration_name="test",
        auto_scaling_configuration_revision=1,
    )
    assert cfg.max_concurrency is None


def test_app_runner_connection_model():
    conn = AppRunnerConnection(
        connection_arn="arn:...",
        connection_name="test",
        provider_type="GITHUB",
        status="AVAILABLE",
    )
    assert conn.created_at is None


def test_app_runner_observability_model():
    oc = AppRunnerObservabilityConfig(
        observability_configuration_arn="arn:...",
        observability_configuration_name="test",
        observability_configuration_revision=1,
    )
    assert oc.trace_configuration is None


def test_app_runner_operation_model():
    op = AppRunnerOperation()
    assert op.id is None
    assert op.type is None


# ---------------------------------------------------------------------------
# create_service
# ---------------------------------------------------------------------------


def test_create_service_minimal(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service.return_value = {
        "Service": _make_service_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_service(
        SERVICE_NAME,
        source_configuration={"ImageRepository": {"ImageIdentifier": "img"}},
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerService)
    assert result.service_name == SERVICE_NAME


def test_create_service_all_params(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service.return_value = {
        "Service": _make_service_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_service(
        SERVICE_NAME,
        source_configuration={"ImageRepository": {"ImageIdentifier": "img"}},
        instance_configuration={"Cpu": "1024", "Memory": "2048"},
        tags=[{"Key": "env", "Value": "dev"}],
        auto_scaling_configuration_arn="arn:asc",
        health_check_configuration={"Protocol": "HTTP"},
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerService)
    call_kwargs = mock_client.create_service.call_args[1]
    assert "InstanceConfiguration" in call_kwargs
    assert "Tags" in call_kwargs
    assert "AutoScalingConfigurationArn" in call_kwargs
    assert "HealthCheckConfiguration" in call_kwargs


def test_create_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_service failed"):
        create_service(SERVICE_NAME, source_configuration={}, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_service
# ---------------------------------------------------------------------------


def test_describe_service_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service.return_value = {
        "Service": _make_service_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_service(SERVICE_ARN, region_name=REGION)
    assert result.service_arn == SERVICE_ARN


def test_describe_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service.side_effect = _client_error("ResourceNotFoundException")
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_service failed"):
        describe_service(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# list_services
# ---------------------------------------------------------------------------


def test_list_services_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services.return_value = {
        "ServiceSummaryList": [_make_service_summary_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_services(region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerServiceSummary)


def test_list_services_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services.side_effect = [
        {
            "ServiceSummaryList": [_make_service_summary_dict()],
            "NextToken": "tok1",
        },
        {
            "ServiceSummaryList": [_make_service_summary_dict(ServiceName="svc2")],
        },
    ]
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_services(region_name=REGION)
    assert len(result) == 2


def test_list_services_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_services failed"):
        list_services(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_service
# ---------------------------------------------------------------------------


def test_delete_service_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service.return_value = {
        "Service": _make_service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = delete_service(SERVICE_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


def test_delete_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_service failed"):
        delete_service(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# update_service
# ---------------------------------------------------------------------------


def test_update_service_minimal(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.return_value = {
        "Service": _make_service_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = update_service(SERVICE_ARN, region_name=REGION)
    assert isinstance(result, AppRunnerService)
    call_kwargs = mock_client.update_service.call_args[1]
    assert "SourceConfiguration" not in call_kwargs
    assert "InstanceConfiguration" not in call_kwargs
    assert "AutoScalingConfigurationArn" not in call_kwargs
    assert "HealthCheckConfiguration" not in call_kwargs


def test_update_service_all_params(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.return_value = {
        "Service": _make_service_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = update_service(
        SERVICE_ARN,
        source_configuration={"ImageRepository": {"ImageIdentifier": "img2"}},
        instance_configuration={"Cpu": "2048"},
        auto_scaling_configuration_arn="arn:asc2",
        health_check_configuration={"Protocol": "TCP"},
        region_name=REGION,
    )
    assert isinstance(result, AppRunnerService)
    call_kwargs = mock_client.update_service.call_args[1]
    assert "SourceConfiguration" in call_kwargs
    assert "InstanceConfiguration" in call_kwargs
    assert "AutoScalingConfigurationArn" in call_kwargs
    assert "HealthCheckConfiguration" in call_kwargs


def test_update_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="update_service failed"):
        update_service(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# pause_service
# ---------------------------------------------------------------------------


def test_pause_service_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_service.return_value = {
        "Service": _make_service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = pause_service(SERVICE_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


def test_pause_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_service.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="pause_service failed"):
        pause_service(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# resume_service
# ---------------------------------------------------------------------------


def test_resume_service_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_service.return_value = {
        "Service": _make_service_dict(Status="OPERATION_IN_PROGRESS"),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = resume_service(SERVICE_ARN, region_name=REGION)
    assert result.status == "OPERATION_IN_PROGRESS"


def test_resume_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_service.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="resume_service failed"):
        resume_service(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# create_auto_scaling_configuration
# ---------------------------------------------------------------------------


def test_create_auto_scaling_configuration_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_auto_scaling_configuration.return_value = {
        "AutoScalingConfiguration": _make_auto_scaling_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_auto_scaling_configuration(
        "default-asc", region_name=REGION
    )
    assert isinstance(result, AppRunnerAutoScalingConfig)
    assert result.max_concurrency == 100


def test_create_auto_scaling_configuration_with_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_auto_scaling_configuration.return_value = {
        "AutoScalingConfiguration": _make_auto_scaling_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_auto_scaling_configuration(
        "default-asc",
        tags=[{"Key": "env", "Value": "prod"}],
        region_name=REGION,
    )
    call_kwargs = mock_client.create_auto_scaling_configuration.call_args[1]
    assert "Tags" in call_kwargs


def test_create_auto_scaling_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_auto_scaling_configuration.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_auto_scaling_configuration failed"):
        create_auto_scaling_configuration("test", region_name=REGION)


# ---------------------------------------------------------------------------
# list_auto_scaling_configurations
# ---------------------------------------------------------------------------


def test_list_auto_scaling_configurations_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_auto_scaling_configurations.return_value = {
        "AutoScalingConfigurationSummaryList": [_make_auto_scaling_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_auto_scaling_configurations(region_name=REGION)
    assert len(result) == 1


def test_list_auto_scaling_configurations_with_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_auto_scaling_configurations.return_value = {
        "AutoScalingConfigurationSummaryList": [_make_auto_scaling_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_auto_scaling_configurations(
        auto_scaling_configuration_name="default-asc", region_name=REGION
    )
    assert len(result) == 1


def test_list_auto_scaling_configurations_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_auto_scaling_configurations.side_effect = [
        {
            "AutoScalingConfigurationSummaryList": [_make_auto_scaling_dict()],
            "NextToken": "tok1",
        },
        {
            "AutoScalingConfigurationSummaryList": [_make_auto_scaling_dict()],
        },
    ]
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_auto_scaling_configurations(region_name=REGION)
    assert len(result) == 2


def test_list_auto_scaling_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_auto_scaling_configurations.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_auto_scaling_configurations failed"):
        list_auto_scaling_configurations(region_name=REGION)


# ---------------------------------------------------------------------------
# create_connection
# ---------------------------------------------------------------------------


def test_create_connection_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {
        "Connection": _make_connection_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_connection("my-conn", region_name=REGION)
    assert isinstance(result, AppRunnerConnection)
    assert result.provider_type == "GITHUB"


def test_create_connection_with_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {
        "Connection": _make_connection_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    create_connection(
        "my-conn",
        provider_type="BITBUCKET",
        tags=[{"Key": "env", "Value": "prod"}],
        region_name=REGION,
    )
    call_kwargs = mock_client.create_connection.call_args[1]
    assert "Tags" in call_kwargs
    assert call_kwargs["ProviderType"] == "BITBUCKET"


def test_create_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_connection failed"):
        create_connection("test", region_name=REGION)


# ---------------------------------------------------------------------------
# list_connections
# ---------------------------------------------------------------------------


def test_list_connections_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {
        "ConnectionSummaryList": [_make_connection_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_connections(region_name=REGION)
    assert len(result) == 1


def test_list_connections_with_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {
        "ConnectionSummaryList": [_make_connection_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_connections(connection_name="my-conn", region_name=REGION)
    assert len(result) == 1


def test_list_connections_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.side_effect = [
        {
            "ConnectionSummaryList": [_make_connection_dict()],
            "NextToken": "tok1",
        },
        {
            "ConnectionSummaryList": [_make_connection_dict()],
        },
    ]
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_connections(region_name=REGION)
    assert len(result) == 2


def test_list_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_connections failed"):
        list_connections(region_name=REGION)


# ---------------------------------------------------------------------------
# create_observability_configuration
# ---------------------------------------------------------------------------


def test_create_observability_configuration_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_observability_configuration.return_value = {
        "ObservabilityConfiguration": _make_observability_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_observability_configuration("my-oc", region_name=REGION)
    assert isinstance(result, AppRunnerObservabilityConfig)


def test_create_observability_configuration_all_params(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_observability_configuration.return_value = {
        "ObservabilityConfiguration": _make_observability_dict(),
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    create_observability_configuration(
        "my-oc",
        trace_configuration={"Vendor": "AWSXRAY"},
        tags=[{"Key": "env", "Value": "prod"}],
        region_name=REGION,
    )
    call_kwargs = mock_client.create_observability_configuration.call_args[1]
    assert "TraceConfiguration" in call_kwargs
    assert "Tags" in call_kwargs


def test_create_observability_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_observability_configuration.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_observability_configuration failed"):
        create_observability_configuration("test", region_name=REGION)


# ---------------------------------------------------------------------------
# start_deployment
# ---------------------------------------------------------------------------


def test_start_deployment_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_deployment.return_value = {"OperationId": "op-456"}
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_deployment(SERVICE_ARN, region_name=REGION)
    assert result == "op-456"


def test_start_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_deployment.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="start_deployment failed"):
        start_deployment(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# list_operations
# ---------------------------------------------------------------------------


def test_list_operations_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_operations.return_value = {
        "OperationSummaryList": [_make_operation_dict()],
    }
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_operations(SERVICE_ARN, region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], AppRunnerOperation)
    assert result[0].id == "op-123"


def test_list_operations_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_operations.side_effect = [
        {
            "OperationSummaryList": [_make_operation_dict()],
            "NextToken": "tok1",
        },
        {
            "OperationSummaryList": [_make_operation_dict(Id="op-456")],
        },
    ]
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_operations(SERVICE_ARN, region_name=REGION)
    assert len(result) == 2


def test_list_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_operations.side_effect = _client_error()
    monkeypatch.setattr(ar_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_operations failed"):
        list_operations(SERVICE_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_service
# ---------------------------------------------------------------------------


def test_wait_for_service_already_running(monkeypatch):
    running_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="RUNNING",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: running_svc)
    result = wait_for_service(SERVICE_ARN, timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.status == "RUNNING"


def test_wait_for_service_create_failed(monkeypatch):
    failed_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="CREATE_FAILED",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: failed_svc)
    result = wait_for_service(SERVICE_ARN, timeout=5.0, region_name=REGION)
    assert result.status == "CREATE_FAILED"


def test_wait_for_service_delete_failed(monkeypatch):
    failed_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="DELETE_FAILED",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: failed_svc)
    result = wait_for_service(SERVICE_ARN, timeout=5.0, region_name=REGION)
    assert result.status == "DELETE_FAILED"


def test_wait_for_service_deleted(monkeypatch):
    deleted_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="DELETED",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: deleted_svc)
    result = wait_for_service(SERVICE_ARN, timeout=5.0, region_name=REGION)
    assert result.status == "DELETED"


def test_wait_for_service_paused(monkeypatch):
    paused_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="PAUSED",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: paused_svc)
    result = wait_for_service(SERVICE_ARN, timeout=5.0, region_name=REGION)
    assert result.status == "PAUSED"


def test_wait_for_service_timeout(monkeypatch):
    pending_svc = AppRunnerService(
        service_arn=SERVICE_ARN,
        service_name=SERVICE_NAME,
        service_id=SERVICE_ID,
        status="OPERATION_IN_PROGRESS",
    )
    monkeypatch.setattr(ar_mod, "describe_service", lambda *a, **kw: pending_svc)
    with pytest.raises(TimeoutError, match="did not reach a terminal status"):
        wait_for_service(
            SERVICE_ARN, timeout=0.0, poll_interval=0.0, region_name=REGION
        )


def test_wait_for_service_polls_then_succeeds(monkeypatch):
    import time as _t
    monkeypatch.setattr(_t, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_describe(service_arn, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return AppRunnerService(
                service_arn=SERVICE_ARN,
                service_name=SERVICE_NAME,
                service_id=SERVICE_ID,
                status="OPERATION_IN_PROGRESS",
            )
        return AppRunnerService(
            service_arn=SERVICE_ARN,
            service_name=SERVICE_NAME,
            service_id=SERVICE_ID,
            status="RUNNING",
        )

    monkeypatch.setattr(ar_mod, "describe_service", fake_describe)
    result = wait_for_service(
        SERVICE_ARN, timeout=10.0, poll_interval=0.001, region_name=REGION
    )
    assert result.status == "RUNNING"


# ---------------------------------------------------------------------------
# Internal parser edge-cases
# ---------------------------------------------------------------------------


def test_parse_service_no_optional_fields():
    """Parse a service dict with no optional keys."""
    data = {
        "ServiceArn": SERVICE_ARN,
        "ServiceName": SERVICE_NAME,
        "ServiceId": SERVICE_ID,
        "Status": "RUNNING",
    }
    result = ar_mod._parse_service(data)
    assert result.service_url is None
    assert result.auto_scaling_configuration_arn is None
    assert result.source_type is None
    assert result.created_at is None
    assert result.updated_at is None


def test_parse_service_summary_no_optional_fields():
    """Parse a service summary with no optional keys."""
    data = {
        "ServiceArn": SERVICE_ARN,
        "ServiceName": SERVICE_NAME,
        "ServiceId": SERVICE_ID,
        "Status": "RUNNING",
    }
    result = ar_mod._parse_service_summary(data)
    assert result.service_url is None
    assert result.created_at is None


def test_parse_auto_scaling_no_optional_fields():
    """Parse auto-scaling dict with no optional keys."""
    data = {
        "AutoScalingConfigurationArn": "arn:...",
        "AutoScalingConfigurationName": "test",
        "AutoScalingConfigurationRevision": 1,
    }
    result = ar_mod._parse_auto_scaling(data)
    assert result.max_concurrency is None
    assert result.status is None


def test_parse_connection_no_optional_fields():
    """Parse connection dict with no optional keys."""
    data = {
        "ConnectionArn": "arn:...",
        "ConnectionName": "test",
        "ProviderType": "GITHUB",
        "Status": "AVAILABLE",
    }
    result = ar_mod._parse_connection(data)
    assert result.created_at is None


def test_parse_observability_no_optional_fields():
    """Parse observability dict with no optional keys."""
    data = {
        "ObservabilityConfigurationArn": "arn:...",
        "ObservabilityConfigurationName": "test",
        "ObservabilityConfigurationRevision": 1,
    }
    result = ar_mod._parse_observability(data)
    assert result.trace_configuration is None
    assert result.status is None


def test_parse_operation_no_optional_fields():
    """Parse operation dict with no optional keys."""
    data: dict = {}
    result = ar_mod._parse_operation(data)
    assert result.id is None
    assert result.type is None
    assert result.started_at is None
    assert result.ended_at is None


def test_associate_custom_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_custom_domain.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    associate_custom_domain("test-service_arn", "test-domain_name", region_name=REGION)
    mock_client.associate_custom_domain.assert_called_once()


def test_associate_custom_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_custom_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_custom_domain",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate custom domain"):
        associate_custom_domain("test-service_arn", "test-domain_name", region_name=REGION)


def test_create_vpc_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connector.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    create_vpc_connector("test-vpc_connector_name", [], region_name=REGION)
    mock_client.create_vpc_connector.assert_called_once()


def test_create_vpc_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_connector",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc connector"):
        create_vpc_connector("test-vpc_connector_name", [], region_name=REGION)


def test_create_vpc_ingress_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_ingress_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, region_name=REGION)
    mock_client.create_vpc_ingress_connection.assert_called_once()


def test_create_vpc_ingress_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_ingress_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_ingress_connection",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc ingress connection"):
        create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, region_name=REGION)


def test_delete_auto_scaling_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)
    mock_client.delete_auto_scaling_configuration.assert_called_once()


def test_delete_auto_scaling_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_auto_scaling_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_auto_scaling_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete auto scaling configuration"):
        delete_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)


def test_delete_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_connection("test-connection_arn", region_name=REGION)
    mock_client.delete_connection.assert_called_once()


def test_delete_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connection"):
        delete_connection("test-connection_arn", region_name=REGION)


def test_delete_observability_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_observability_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_observability_configuration("test-observability_configuration_arn", region_name=REGION)
    mock_client.delete_observability_configuration.assert_called_once()


def test_delete_observability_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_observability_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_observability_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete observability configuration"):
        delete_observability_configuration("test-observability_configuration_arn", region_name=REGION)


def test_delete_vpc_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connector.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_vpc_connector("test-vpc_connector_arn", region_name=REGION)
    mock_client.delete_vpc_connector.assert_called_once()


def test_delete_vpc_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_connector",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc connector"):
        delete_vpc_connector("test-vpc_connector_arn", region_name=REGION)


def test_delete_vpc_ingress_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_ingress_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_vpc_ingress_connection("test-vpc_ingress_connection_arn", region_name=REGION)
    mock_client.delete_vpc_ingress_connection.assert_called_once()


def test_delete_vpc_ingress_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_ingress_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_ingress_connection",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc ingress connection"):
        delete_vpc_ingress_connection("test-vpc_ingress_connection_arn", region_name=REGION)


def test_describe_auto_scaling_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)
    mock_client.describe_auto_scaling_configuration.assert_called_once()


def test_describe_auto_scaling_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_scaling_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_auto_scaling_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe auto scaling configuration"):
        describe_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)


def test_describe_custom_domains(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_domains.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_custom_domains("test-service_arn", region_name=REGION)
    mock_client.describe_custom_domains.assert_called_once()


def test_describe_custom_domains_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_domains.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_domains",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe custom domains"):
        describe_custom_domains("test-service_arn", region_name=REGION)


def test_describe_observability_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_observability_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_observability_configuration("test-observability_configuration_arn", region_name=REGION)
    mock_client.describe_observability_configuration.assert_called_once()


def test_describe_observability_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_observability_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_observability_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe observability configuration"):
        describe_observability_configuration("test-observability_configuration_arn", region_name=REGION)


def test_describe_vpc_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connector.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_vpc_connector("test-vpc_connector_arn", region_name=REGION)
    mock_client.describe_vpc_connector.assert_called_once()


def test_describe_vpc_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_connector",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc connector"):
        describe_vpc_connector("test-vpc_connector_arn", region_name=REGION)


def test_describe_vpc_ingress_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_ingress_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_vpc_ingress_connection("test-vpc_ingress_connection_arn", region_name=REGION)
    mock_client.describe_vpc_ingress_connection.assert_called_once()


def test_describe_vpc_ingress_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_ingress_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_ingress_connection",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc ingress connection"):
        describe_vpc_ingress_connection("test-vpc_ingress_connection_arn", region_name=REGION)


def test_disassociate_custom_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_custom_domain.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    disassociate_custom_domain("test-service_arn", "test-domain_name", region_name=REGION)
    mock_client.disassociate_custom_domain.assert_called_once()


def test_disassociate_custom_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_custom_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_custom_domain",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate custom domain"):
        disassociate_custom_domain("test-service_arn", "test-domain_name", region_name=REGION)


def test_list_observability_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_observability_configurations.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_observability_configurations(region_name=REGION)
    mock_client.list_observability_configurations.assert_called_once()


def test_list_observability_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_observability_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_observability_configurations",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list observability configurations"):
        list_observability_configurations(region_name=REGION)


def test_list_services_for_auto_scaling_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services_for_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_services_for_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)
    mock_client.list_services_for_auto_scaling_configuration.assert_called_once()


def test_list_services_for_auto_scaling_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services_for_auto_scaling_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_services_for_auto_scaling_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list services for auto scaling configuration"):
        list_services_for_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_vpc_connectors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connectors.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_vpc_connectors(region_name=REGION)
    mock_client.list_vpc_connectors.assert_called_once()


def test_list_vpc_connectors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connectors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_connectors",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc connectors"):
        list_vpc_connectors(region_name=REGION)


def test_list_vpc_ingress_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_ingress_connections.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_vpc_ingress_connections(region_name=REGION)
    mock_client.list_vpc_ingress_connections.assert_called_once()


def test_list_vpc_ingress_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_ingress_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_ingress_connections",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc ingress connections"):
        list_vpc_ingress_connections(region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_default_auto_scaling_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_default_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    update_default_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)
    mock_client.update_default_auto_scaling_configuration.assert_called_once()


def test_update_default_auto_scaling_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_default_auto_scaling_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_default_auto_scaling_configuration",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update default auto scaling configuration"):
        update_default_auto_scaling_configuration("test-auto_scaling_configuration_arn", region_name=REGION)


def test_update_vpc_ingress_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_ingress_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    update_vpc_ingress_connection("test-vpc_ingress_connection_arn", {}, region_name=REGION)
    mock_client.update_vpc_ingress_connection.assert_called_once()


def test_update_vpc_ingress_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_ingress_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vpc_ingress_connection",
    )
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vpc ingress connection"):
        update_vpc_ingress_connection("test-vpc_ingress_connection_arn", {}, region_name=REGION)


def test_list_auto_scaling_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_auto_scaling_configurations
    mock_client = MagicMock()
    mock_client.list_auto_scaling_configurations.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_auto_scaling_configurations(auto_scaling_configuration_name=True, region_name="us-east-1")
    mock_client.list_auto_scaling_configurations.assert_called_once()

def test_list_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_connections
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_connections(connection_name="test-connection_name", region_name="us-east-1")
    mock_client.list_connections.assert_called_once()

def test_associate_custom_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import associate_custom_domain
    mock_client = MagicMock()
    mock_client.associate_custom_domain.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    associate_custom_domain("test-service_arn", "test-domain_name", enable_www_subdomain=True, region_name="us-east-1")
    mock_client.associate_custom_domain.assert_called_once()

def test_create_vpc_connector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import create_vpc_connector
    mock_client = MagicMock()
    mock_client.create_vpc_connector.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    create_vpc_connector("test-vpc_connector_name", "test-subnets", security_groups="test-security_groups", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vpc_connector.assert_called_once()

def test_create_vpc_ingress_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import create_vpc_ingress_connection
    mock_client = MagicMock()
    mock_client.create_vpc_ingress_connection.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    create_vpc_ingress_connection("test-service_arn", "test-vpc_ingress_connection_name", {}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vpc_ingress_connection.assert_called_once()

def test_delete_auto_scaling_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import delete_auto_scaling_configuration
    mock_client = MagicMock()
    mock_client.delete_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    delete_auto_scaling_configuration(True, delete_all_revisions=True, region_name="us-east-1")
    mock_client.delete_auto_scaling_configuration.assert_called_once()

def test_describe_custom_domains_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import describe_custom_domains
    mock_client = MagicMock()
    mock_client.describe_custom_domains.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    describe_custom_domains("test-service_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_custom_domains.assert_called_once()

def test_list_observability_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_observability_configurations
    mock_client = MagicMock()
    mock_client.list_observability_configurations.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_observability_configurations(observability_configuration_name={}, latest_only="test-latest_only", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_observability_configurations.assert_called_once()

def test_list_services_for_auto_scaling_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_services_for_auto_scaling_configuration
    mock_client = MagicMock()
    mock_client.list_services_for_auto_scaling_configuration.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_services_for_auto_scaling_configuration(True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_services_for_auto_scaling_configuration.assert_called_once()

def test_list_vpc_connectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_vpc_connectors
    mock_client = MagicMock()
    mock_client.list_vpc_connectors.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_vpc_connectors(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_vpc_connectors.assert_called_once()

def test_list_vpc_ingress_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.app_runner import list_vpc_ingress_connections
    mock_client = MagicMock()
    mock_client.list_vpc_ingress_connections.return_value = {}
    monkeypatch.setattr("aws_util.app_runner.get_client", lambda *a, **kw: mock_client)
    list_vpc_ingress_connections(filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_vpc_ingress_connections.assert_called_once()
