"""Tests for aws_util.aio.emr_containers -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.emr_containers import (
    JobRunResult,
    VirtualClusterResult,
    cancel_job_run,
    create_virtual_cluster,
    delete_virtual_cluster,
    describe_job_run,
    describe_virtual_cluster,
    list_job_runs,
    list_virtual_clusters,
    start_job_run,
    create_job_template,
    create_managed_endpoint,
    create_security_configuration,
    delete_job_template,
    delete_managed_endpoint,
    describe_job_template,
    describe_managed_endpoint,
    describe_security_configuration,
    get_managed_endpoint_session_credentials,
    list_job_templates,
    list_managed_endpoints,
    list_security_configurations,
    list_tags_for_resource,
    tag_resource,
    untag_resource,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# Re-exported models
# ---------------------------------------------------------------------------


def test_models_re_exported():
    assert VirtualClusterResult is not None
    assert JobRunResult is not None


# ---------------------------------------------------------------------------
# Virtual cluster operations
# ---------------------------------------------------------------------------


class TestCreateVirtualCluster:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"id": "vc-1", "name": "test", "arn": "arn:vc"})
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await create_virtual_cluster(
            "test", container_provider={"type": "EKS"}
        )
        assert result.id == "vc-1"

    @pytest.mark.asyncio
    async def test_with_tags(self, monkeypatch):
        mc = _mc({"id": "vc-1", "name": "test", "arn": "arn:vc"})
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await create_virtual_cluster(
            "test",
            container_provider={"type": "EKS"},
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.id == "vc-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await create_virtual_cluster(
                "test", container_provider={"type": "EKS"}
            )


class TestDescribeVirtualCluster:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "virtualCluster": {
                "id": "vc-1", "name": "test", "state": "RUNNING"
            }
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await describe_virtual_cluster("vc-1")
        assert result.id == "vc-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await describe_virtual_cluster("vc-1")


class TestListVirtualClusters:
    @pytest.mark.asyncio
    async def test_success_single_page(self, monkeypatch):
        mc = _mc({
            "virtualClusters": [
                {"id": "vc-1", "name": "a"},
                {"id": "vc-2", "name": "b"},
            ]
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await list_virtual_clusters()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"virtualClusters": [{"id": "vc-1", "name": "a"}], "nextToken": "tok"},
            {"virtualClusters": [{"id": "vc-2", "name": "b"}]},
        ]
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await list_virtual_clusters()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await list_virtual_clusters()


class TestDeleteVirtualCluster:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await delete_virtual_cluster("vc-1")
        assert result == {"id": "vc-1"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await delete_virtual_cluster("vc-1")


# ---------------------------------------------------------------------------
# Job run operations
# ---------------------------------------------------------------------------


class TestStartJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "id": "jr-1", "name": "job",
            "virtualClusterId": "vc-1", "arn": "arn:jr"
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await start_job_run(
            "vc-1",
            name="job",
            execution_role_arn="arn:role",
            release_label="emr-6.9.0",
            job_driver={"sparkSubmitJobDriver": {}},
        )
        assert result.id == "jr-1"

    @pytest.mark.asyncio
    async def test_with_optionals(self, monkeypatch):
        mc = _mc({
            "id": "jr-1", "name": "job",
            "virtualClusterId": "vc-1", "arn": "arn:jr"
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await start_job_run(
            "vc-1",
            name="job",
            execution_role_arn="arn:role",
            release_label="emr-6.9.0",
            job_driver={},
            configuration_overrides={"monitoring": {}},
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.id == "jr-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await start_job_run(
                "vc-1",
                name="job",
                execution_role_arn="arn:role",
                release_label="emr-6.9.0",
                job_driver={},
            )


class TestDescribeJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "jobRun": {"id": "jr-1", "name": "job", "virtualClusterId": "vc-1"}
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await describe_job_run("vc-1", "jr-1")
        assert result.id == "jr-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await describe_job_run("vc-1", "jr-1")


class TestListJobRuns:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"jobRuns": [{"id": "jr-1"}], "nextToken": "tok"},
            {"jobRuns": [{"id": "jr-2"}]},
        ]
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await list_job_runs("vc-1")
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await list_job_runs("vc-1")


class TestCancelJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        result = await cancel_job_run("vc-1", "jr-1")
        assert result == {"virtual_cluster_id": "vc-1", "id": "jr-1"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_containers.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await cancel_job_run("vc-1", "jr-1")


async def test_create_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_job_template("test-name", "test-client_token", {}, )
    mock_client.call.assert_called_once()


async def test_create_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_job_template("test-name", "test-client_token", {}, )


async def test_create_managed_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_managed_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", )


async def test_create_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_security_configuration("test-client_token", "test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_security_configuration("test-client_token", "test-name", {}, )


async def test_delete_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job_template("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job_template("test-id", )


async def test_delete_managed_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_managed_endpoint("test-id", "test-virtual_cluster_id", )
    mock_client.call.assert_called_once()


async def test_delete_managed_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_managed_endpoint("test-id", "test-virtual_cluster_id", )


async def test_describe_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_job_template("test-id", )
    mock_client.call.assert_called_once()


async def test_describe_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_job_template("test-id", )


async def test_describe_managed_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_managed_endpoint("test-id", "test-virtual_cluster_id", )
    mock_client.call.assert_called_once()


async def test_describe_managed_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_managed_endpoint("test-id", "test-virtual_cluster_id", )


async def test_describe_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_configuration("test-id", )
    mock_client.call.assert_called_once()


async def test_describe_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_configuration("test-id", )


async def test_get_managed_endpoint_session_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", )
    mock_client.call.assert_called_once()


async def test_get_managed_endpoint_session_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", )


async def test_list_job_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_job_templates()
    mock_client.call.assert_called_once()


async def test_list_job_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_job_templates()


async def test_list_managed_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_managed_endpoints("test-virtual_cluster_id", )
    mock_client.call.assert_called_once()


async def test_list_managed_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_managed_endpoints("test-virtual_cluster_id", )


async def test_list_security_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_configurations()
    mock_client.call.assert_called_once()


async def test_list_security_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_configurations()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_containers.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import create_job_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await create_job_template("test-name", "test-client_token", "test-job_template_data", tags=[{"Key": "k", "Value": "v"}], kms_key_arn="test-kms_key_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_managed_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import create_managed_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", certificate_arn="test-certificate_arn", configuration_overrides={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_security_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import create_security_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await create_security_configuration("test-client_token", "test-name", {}, container_provider="test-container_provider", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_managed_endpoint_session_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import get_managed_endpoint_session_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", duration_in_seconds=1, log_context={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import list_job_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await list_job_templates(created_after="test-created_after", created_before="test-created_before", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_managed_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import list_managed_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await list_managed_endpoints("test-virtual_cluster_id", created_before="test-created_before", created_after="test-created_after", types="test-types", states="test-states", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_containers import list_security_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_containers.async_client", lambda *a, **kw: mock_client)
    await list_security_configurations(created_after="test-created_after", created_before="test-created_before", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
