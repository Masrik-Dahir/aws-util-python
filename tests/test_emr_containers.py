"""Tests for aws_util.emr_containers -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.emr_containers import (
    JobRunResult,
    VirtualClusterResult,
    _parse_job_run,
    _parse_virtual_cluster,
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
# Model tests
# ---------------------------------------------------------------------------


class TestVirtualClusterResult:
    def test_minimal(self):
        vc = VirtualClusterResult(id="vc-1", name="test")
        assert vc.id == "vc-1"
        assert vc.name == "test"
        assert vc.arn == ""
        assert vc.state == ""
        assert vc.container_provider == {}
        assert vc.created_at is None
        assert vc.tags == {}
        assert vc.extra == {}

    def test_full(self):
        vc = VirtualClusterResult(
            id="vc-1",
            name="test",
            arn="arn:aws:emr-containers:us-east-1:123:vc/vc-1",
            state="RUNNING",
            container_provider={"type": "EKS", "id": "cluster-1"},
            created_at="2024-01-01T00:00:00Z",
            tags={"env": "dev"},
            extra={"foo": "bar"},
        )
        assert vc.state == "RUNNING"
        assert vc.tags == {"env": "dev"}


class TestJobRunResult:
    def test_minimal(self):
        jr = JobRunResult(id="jr-1")
        assert jr.id == "jr-1"
        assert jr.name == ""
        assert jr.virtual_cluster_id == ""
        assert jr.state_details is None
        assert jr.execution_role_arn is None
        assert jr.release_label is None
        assert jr.created_at is None
        assert jr.finished_at is None

    def test_full(self):
        jr = JobRunResult(
            id="jr-1",
            name="job",
            virtual_cluster_id="vc-1",
            arn="arn:jr",
            state="COMPLETED",
            state_details="done",
            execution_role_arn="arn:role",
            release_label="emr-6.9.0",
            created_at="2024-01-01",
            finished_at="2024-01-02",
            extra={"k": "v"},
        )
        assert jr.finished_at == "2024-01-02"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_virtual_cluster_full(self):
        data = {
            "id": "vc-1",
            "name": "test",
            "arn": "arn:vc",
            "state": "RUNNING",
            "containerProvider": {"type": "EKS"},
            "createdAt": "2024-01-01",
            "tags": {"env": "dev"},
            "extraField": "value",
        }
        vc = _parse_virtual_cluster(data)
        assert vc.id == "vc-1"
        assert vc.created_at == "2024-01-01"
        assert vc.extra == {"extraField": "value"}

    def test_parse_virtual_cluster_none_created(self):
        data = {"id": "vc-1", "name": "test"}
        vc = _parse_virtual_cluster(data)
        assert vc.created_at is None

    def test_parse_job_run_full(self):
        data = {
            "id": "jr-1",
            "name": "job",
            "virtualClusterId": "vc-1",
            "arn": "arn:jr",
            "state": "COMPLETED",
            "stateDetails": "done",
            "executionRoleArn": "arn:role",
            "releaseLabel": "emr-6.9.0",
            "createdAt": "2024-01-01",
            "finishedAt": "2024-01-02",
            "extra_key": "extra_val",
        }
        jr = _parse_job_run(data)
        assert jr.created_at == "2024-01-01"
        assert jr.finished_at == "2024-01-02"
        assert jr.extra == {"extra_key": "extra_val"}

    def test_parse_job_run_none_times(self):
        data = {"id": "jr-1"}
        jr = _parse_job_run(data)
        assert jr.created_at is None
        assert jr.finished_at is None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ERR = ClientError(
    {"Error": {"Code": "ValidationException", "Message": "bad"}},
    "op",
)


def _mock_client(return_value=None, side_effect=None):
    client = MagicMock()
    if side_effect:
        for method_name, se in side_effect.items():
            getattr(client, method_name).side_effect = se
    if return_value:
        for method_name, rv in return_value.items():
            getattr(client, method_name).return_value = rv
    return client


# ---------------------------------------------------------------------------
# Virtual cluster function tests
# ---------------------------------------------------------------------------


class TestCreateVirtualCluster:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_virtual_cluster.return_value = {
            "id": "vc-1", "name": "test", "arn": "arn:vc"
        }
        mock_gc.return_value = client
        result = create_virtual_cluster(
            "test",
            container_provider={"type": "EKS"},
        )
        assert result.id == "vc-1"
        assert result.name == "test"

    @patch("aws_util.emr_containers.get_client")
    def test_with_tags(self, mock_gc):
        client = MagicMock()
        client.create_virtual_cluster.return_value = {
            "id": "vc-1", "name": "test", "arn": "arn:vc"
        }
        mock_gc.return_value = client
        result = create_virtual_cluster(
            "test",
            container_provider={"type": "EKS"},
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.id == "vc-1"
        call_kw = client.create_virtual_cluster.call_args[1]
        assert call_kw["tags"] == {"env": "dev"}

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_virtual_cluster.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            create_virtual_cluster(
                "test", container_provider={"type": "EKS"}
            )


class TestDescribeVirtualCluster:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_virtual_cluster.return_value = {
            "virtualCluster": {
                "id": "vc-1", "name": "test", "arn": "arn:vc",
                "state": "RUNNING",
            }
        }
        mock_gc.return_value = client
        result = describe_virtual_cluster("vc-1")
        assert result.id == "vc-1"
        assert result.state == "RUNNING"

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_virtual_cluster.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_virtual_cluster("vc-1")


class TestListVirtualClusters:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"virtualClusters": [{"id": "vc-1", "name": "a"}]},
            {"virtualClusters": [{"id": "vc-2", "name": "b"}]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_virtual_clusters()
        assert len(result) == 2
        assert result[0].id == "vc-1"

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_virtual_clusters()


class TestDeleteVirtualCluster:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        result = delete_virtual_cluster("vc-1")
        assert result == {"id": "vc-1"}

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_virtual_cluster.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            delete_virtual_cluster("vc-1")


# ---------------------------------------------------------------------------
# Job run function tests
# ---------------------------------------------------------------------------


class TestStartJobRun:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.start_job_run.return_value = {
            "id": "jr-1", "name": "job",
            "virtualClusterId": "vc-1", "arn": "arn:jr"
        }
        mock_gc.return_value = client
        result = start_job_run(
            "vc-1",
            name="job",
            execution_role_arn="arn:role",
            release_label="emr-6.9.0",
            job_driver={"sparkSubmitJobDriver": {}},
        )
        assert result.id == "jr-1"

    @patch("aws_util.emr_containers.get_client")
    def test_with_optionals(self, mock_gc):
        client = MagicMock()
        client.start_job_run.return_value = {
            "id": "jr-1", "name": "job",
            "virtualClusterId": "vc-1", "arn": "arn:jr"
        }
        mock_gc.return_value = client
        result = start_job_run(
            "vc-1",
            name="job",
            execution_role_arn="arn:role",
            release_label="emr-6.9.0",
            job_driver={"sparkSubmitJobDriver": {}},
            configuration_overrides={"monitoring": {}},
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.id == "jr-1"
        call_kw = client.start_job_run.call_args[1]
        assert "configurationOverrides" in call_kw
        assert "tags" in call_kw

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.start_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            start_job_run(
                "vc-1",
                name="job",
                execution_role_arn="arn:role",
                release_label="emr-6.9.0",
                job_driver={},
            )


class TestDescribeJobRun:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_job_run.return_value = {
            "jobRun": {
                "id": "jr-1", "name": "job",
                "virtualClusterId": "vc-1",
            }
        }
        mock_gc.return_value = client
        result = describe_job_run("vc-1", "jr-1")
        assert result.id == "jr-1"

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_job_run("vc-1", "jr-1")


class TestListJobRuns:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"jobRuns": [{"id": "jr-1"}]},
            {"jobRuns": [{"id": "jr-2"}]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_job_runs("vc-1")
        assert len(result) == 2

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_job_runs("vc-1")


class TestCancelJobRun:
    @patch("aws_util.emr_containers.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        result = cancel_job_run("vc-1", "jr-1")
        assert result == {"virtual_cluster_id": "vc-1", "id": "jr-1"}

    @patch("aws_util.emr_containers.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.cancel_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            cancel_job_run("vc-1", "jr-1")


REGION = "us-east-1"


@patch("aws_util.emr_containers.get_client")
def test_create_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_job_template.return_value = {}
    create_job_template("test-name", "test-client_token", {}, region_name=REGION)
    mock_client.create_job_template.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_create_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to create job template"):
        create_job_template("test-name", "test-client_token", {}, region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_create_managed_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_managed_endpoint.return_value = {}
    create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", region_name=REGION)
    mock_client.create_managed_endpoint.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_create_managed_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_managed_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_managed_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to create managed endpoint"):
        create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_create_security_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_security_configuration.return_value = {}
    create_security_configuration("test-client_token", "test-name", {}, region_name=REGION)
    mock_client.create_security_configuration.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_create_security_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_security_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to create security configuration"):
        create_security_configuration("test-client_token", "test-name", {}, region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_delete_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_template.return_value = {}
    delete_job_template("test-id", region_name=REGION)
    mock_client.delete_job_template.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_delete_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to delete job template"):
        delete_job_template("test-id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_delete_managed_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_managed_endpoint.return_value = {}
    delete_managed_endpoint("test-id", "test-virtual_cluster_id", region_name=REGION)
    mock_client.delete_managed_endpoint.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_delete_managed_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_managed_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_managed_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to delete managed endpoint"):
        delete_managed_endpoint("test-id", "test-virtual_cluster_id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_describe_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_template.return_value = {}
    describe_job_template("test-id", region_name=REGION)
    mock_client.describe_job_template.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_describe_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to describe job template"):
        describe_job_template("test-id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_describe_managed_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_managed_endpoint.return_value = {}
    describe_managed_endpoint("test-id", "test-virtual_cluster_id", region_name=REGION)
    mock_client.describe_managed_endpoint.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_describe_managed_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_managed_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_managed_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to describe managed endpoint"):
        describe_managed_endpoint("test-id", "test-virtual_cluster_id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_describe_security_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_security_configuration.return_value = {}
    describe_security_configuration("test-id", region_name=REGION)
    mock_client.describe_security_configuration.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_describe_security_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe security configuration"):
        describe_security_configuration("test-id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_get_managed_endpoint_session_credentials(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_managed_endpoint_session_credentials.return_value = {}
    get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", region_name=REGION)
    mock_client.get_managed_endpoint_session_credentials.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_get_managed_endpoint_session_credentials_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_managed_endpoint_session_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_managed_endpoint_session_credentials",
    )
    with pytest.raises(RuntimeError, match="Failed to get managed endpoint session credentials"):
        get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_list_job_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_templates.return_value = {}
    list_job_templates(region_name=REGION)
    mock_client.list_job_templates.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_list_job_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_job_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list job templates"):
        list_job_templates(region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_list_managed_endpoints(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_endpoints.return_value = {}
    list_managed_endpoints("test-virtual_cluster_id", region_name=REGION)
    mock_client.list_managed_endpoints.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_list_managed_endpoints_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_managed_endpoints",
    )
    with pytest.raises(RuntimeError, match="Failed to list managed endpoints"):
        list_managed_endpoints("test-virtual_cluster_id", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_list_security_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_configurations.return_value = {}
    list_security_configurations(region_name=REGION)
    mock_client.list_security_configurations.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_list_security_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to list security configurations"):
        list_security_configurations(region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.emr_containers.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.emr_containers.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import create_job_template
    mock_client = MagicMock()
    mock_client.create_job_template.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    create_job_template("test-name", "test-client_token", "test-job_template_data", tags=[{"Key": "k", "Value": "v"}], kms_key_arn="test-kms_key_arn", region_name="us-east-1")
    mock_client.create_job_template.assert_called_once()

def test_create_managed_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import create_managed_endpoint
    mock_client = MagicMock()
    mock_client.create_managed_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    create_managed_endpoint("test-name", "test-virtual_cluster_id", "test-type_value", "test-release_label", "test-execution_role_arn", "test-client_token", certificate_arn="test-certificate_arn", configuration_overrides={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_managed_endpoint.assert_called_once()

def test_create_security_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import create_security_configuration
    mock_client = MagicMock()
    mock_client.create_security_configuration.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    create_security_configuration("test-client_token", "test-name", {}, container_provider="test-container_provider", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_security_configuration.assert_called_once()

def test_get_managed_endpoint_session_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import get_managed_endpoint_session_credentials
    mock_client = MagicMock()
    mock_client.get_managed_endpoint_session_credentials.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    get_managed_endpoint_session_credentials("test-endpoint_identifier", "test-virtual_cluster_identifier", "test-execution_role_arn", "test-credential_type", duration_in_seconds=1, log_context={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.get_managed_endpoint_session_credentials.assert_called_once()

def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import list_job_templates
    mock_client = MagicMock()
    mock_client.list_job_templates.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    list_job_templates(created_after="test-created_after", created_before="test-created_before", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_job_templates.assert_called_once()

def test_list_managed_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import list_managed_endpoints
    mock_client = MagicMock()
    mock_client.list_managed_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    list_managed_endpoints("test-virtual_cluster_id", created_before="test-created_before", created_after="test-created_after", types="test-types", states="test-states", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_managed_endpoints.assert_called_once()

def test_list_security_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_containers import list_security_configurations
    mock_client = MagicMock()
    mock_client.list_security_configurations.return_value = {}
    monkeypatch.setattr("aws_util.emr_containers.get_client", lambda *a, **kw: mock_client)
    list_security_configurations(created_after="test-created_after", created_before="test-created_before", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_security_configurations.assert_called_once()
