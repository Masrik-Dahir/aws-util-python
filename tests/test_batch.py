"""Tests for aws_util.batch module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

import aws_util.batch as batch_mod
from aws_util.batch import (
    ComputeEnvironmentResult,
    JobDefinitionResult,
    JobQueueResult,
    JobResult,
    create_compute_environment,
    create_job_queue,
    delete_compute_environment,
    delete_job_queue,
    deregister_job_definition,
    describe_compute_environments,
    describe_job_definitions,
    describe_job_queues,
    describe_jobs,
    list_jobs,
    register_job_definition,
    submit_and_wait,
    submit_job,
    terminate_job,
    cancel_job,
    update_compute_environment,
    update_job_queue,
    wait_for_job,
    _parse_compute_env,
    _parse_job,
    _parse_job_definition,
    _parse_job_queue,
    create_consumable_resource,
    create_scheduling_policy,
    create_service_environment,
    delete_consumable_resource,
    delete_scheduling_policy,
    delete_service_environment,
    describe_consumable_resource,
    describe_scheduling_policies,
    describe_service_environments,
    describe_service_job,
    get_job_queue_snapshot,
    list_consumable_resources,
    list_jobs_by_consumable_resource,
    list_scheduling_policies,
    list_service_jobs,
    list_tags_for_resource,
    submit_service_job,
    tag_resource,
    terminate_service_job,
    untag_resource,
    update_consumable_resource,
    update_scheduling_policy,
    update_service_environment,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError

REGION = "us-east-1"
CE_NAME = "test-ce"
CE_ARN = "arn:aws:batch:us-east-1:123456789012:compute-environment/test-ce"
JQ_NAME = "test-jq"
JQ_ARN = "arn:aws:batch:us-east-1:123456789012:job-queue/test-jq"
JD_NAME = "test-jd"
JD_ARN = "arn:aws:batch:us-east-1:123456789012:job-definition/test-jd:1"
JOB_ID = "job-12345"
JOB_NAME = "test-job"


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _make_ce_dict(**kwargs) -> dict:
    defaults = {
        "computeEnvironmentName": CE_NAME,
        "computeEnvironmentArn": CE_ARN,
        "type": "MANAGED",
        "state": "ENABLED",
        "status": "VALID",
        "computeResources": {"type": "EC2", "minvCpus": 0},
        "serviceRole": "arn:aws:iam::123456789012:role/BatchRole",
    }
    defaults.update(kwargs)
    return defaults


def _make_jq_dict(**kwargs) -> dict:
    defaults = {
        "jobQueueName": JQ_NAME,
        "jobQueueArn": JQ_ARN,
        "state": "ENABLED",
        "status": "VALID",
        "priority": 1,
        "computeEnvironmentOrder": [
            {"computeEnvironment": CE_ARN, "order": 1}
        ],
    }
    defaults.update(kwargs)
    return defaults


def _make_jd_dict(**kwargs) -> dict:
    defaults = {
        "jobDefinitionName": JD_NAME,
        "jobDefinitionArn": JD_ARN,
        "revision": 1,
        "type": "container",
        "status": "ACTIVE",
        "containerProperties": {"image": "busybox", "vcpus": 1, "memory": 512},
    }
    defaults.update(kwargs)
    return defaults


def _make_job_dict(**kwargs) -> dict:
    defaults = {
        "jobId": JOB_ID,
        "jobName": JOB_NAME,
        "jobQueue": JQ_ARN,
        "status": "SUBMITTED",
        "createdAt": 1609459200,
    }
    defaults.update(kwargs)
    return defaults


def _client_error(code: str = "ClientException", msg: str = "error", op: str = "Op"):
    return ClientError({"Error": {"Code": code, "Message": msg}}, op)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_compute_environment_model(self):
        ce = ComputeEnvironmentResult(
            name=CE_NAME, arn=CE_ARN, type="MANAGED",
            state="ENABLED", status="VALID",
        )
        assert ce.name == CE_NAME
        assert ce.compute_resources is None
        assert ce.service_role is None
        assert ce.extra == {}

    def test_job_queue_model(self):
        jq = JobQueueResult(
            name=JQ_NAME, arn=JQ_ARN, state="ENABLED",
            status="VALID", priority=1, compute_environments=[],
        )
        assert jq.priority == 1

    def test_job_definition_model(self):
        jd = JobDefinitionResult(
            name=JD_NAME, arn=JD_ARN, revision=1,
            type="container", status="ACTIVE",
        )
        assert jd.revision == 1
        assert jd.container_properties is None

    def test_job_result_model(self):
        job = JobResult(
            job_id=JOB_ID, job_name=JOB_NAME,
            job_queue=JQ_ARN, status="SUBMITTED",
        )
        assert job.status_reason is None
        assert job.created_at is None
        assert job.container is None

    def test_job_result_model_full(self):
        job = JobResult(
            job_id=JOB_ID, job_name=JOB_NAME,
            job_queue=JQ_ARN, status="RUNNING",
            status_reason="Started", created_at=100,
            started_at=200, stopped_at=300,
            container={"image": "busybox"},
            extra={"foo": "bar"},
        )
        assert job.started_at == 200
        assert job.extra == {"foo": "bar"}


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_compute_env(self):
        result = _parse_compute_env(_make_ce_dict())
        assert result.name == CE_NAME
        assert result.compute_resources is not None

    def test_parse_compute_env_extra_fields(self):
        data = _make_ce_dict(tags={"env": "test"})
        result = _parse_compute_env(data)
        assert "tags" in result.extra

    def test_parse_job_queue(self):
        result = _parse_job_queue(_make_jq_dict())
        assert result.name == JQ_NAME
        assert len(result.compute_environments) == 1

    def test_parse_job_queue_extra_fields(self):
        data = _make_jq_dict(tags={"env": "test"})
        result = _parse_job_queue(data)
        assert "tags" in result.extra

    def test_parse_job_definition(self):
        result = _parse_job_definition(_make_jd_dict())
        assert result.name == JD_NAME
        assert result.container_properties is not None

    def test_parse_job_definition_extra_fields(self):
        data = _make_jd_dict(tags={"env": "test"})
        result = _parse_job_definition(data)
        assert "tags" in result.extra

    def test_parse_job(self):
        result = _parse_job(_make_job_dict())
        assert result.job_id == JOB_ID

    def test_parse_job_extra_fields(self):
        data = _make_job_dict(attempts=[{"container": {}}])
        result = _parse_job(data)
        assert "attempts" in result.extra

    def test_parse_job_all_optional_fields(self):
        data = _make_job_dict(
            statusReason="reason",
            startedAt=100,
            stoppedAt=200,
            container={"image": "busybox"},
        )
        result = _parse_job(data)
        assert result.status_reason == "reason"
        assert result.started_at == 100
        assert result.stopped_at == 200
        assert result.container is not None


# ---------------------------------------------------------------------------
# create_compute_environment
# ---------------------------------------------------------------------------


class TestCreateComputeEnvironment:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_compute_environment.return_value = {
            "computeEnvironmentArn": CE_ARN,
            "computeEnvironmentName": CE_NAME,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_compute_environment(CE_NAME, region_name=REGION)
        assert isinstance(result, ComputeEnvironmentResult)
        assert result.arn == CE_ARN

    def test_with_compute_resources_and_role(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_compute_environment.return_value = {
            "computeEnvironmentArn": CE_ARN,
            "computeEnvironmentName": CE_NAME,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        resources = {"type": "EC2", "minvCpus": 0}
        role = "arn:aws:iam::123:role/Batch"
        result = create_compute_environment(
            CE_NAME, compute_resources=resources, service_role=role,
            region_name=REGION,
        )
        assert result.compute_resources == resources
        assert result.service_role == role

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_compute_environment.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_compute_environment failed"):
            create_compute_environment(CE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_compute_environments
# ---------------------------------------------------------------------------


class TestDescribeComputeEnvironments:
    def test_success_with_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_compute_environments.return_value = {
            "computeEnvironments": [_make_ce_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_compute_environments(names=[CE_NAME], region_name=REGION)
        assert len(result) == 1
        assert result[0].name == CE_NAME

    def test_success_without_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_compute_environments.return_value = {
            "computeEnvironments": []
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_compute_environments(region_name=REGION)
        assert result == []

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_compute_environments.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_compute_environments failed"):
            describe_compute_environments(region_name=REGION)


# ---------------------------------------------------------------------------
# update_compute_environment
# ---------------------------------------------------------------------------


class TestUpdateComputeEnvironment:
    def test_success_with_describe(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_compute_environment.return_value = {
            "computeEnvironmentArn": CE_ARN,
            "computeEnvironmentName": CE_NAME,
        }
        mock_client.describe_compute_environments.return_value = {
            "computeEnvironments": [_make_ce_dict(state="DISABLED")]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_compute_environment(
            CE_NAME, state="DISABLED", region_name=REGION,
        )
        assert result.state == "DISABLED"

    def test_success_with_compute_resources(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_compute_environment.return_value = {
            "computeEnvironmentArn": CE_ARN,
        }
        mock_client.describe_compute_environments.return_value = {
            "computeEnvironments": [_make_ce_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_compute_environment(
            CE_NAME, compute_resources={"maxvCpus": 10}, region_name=REGION,
        )
        assert isinstance(result, ComputeEnvironmentResult)

    def test_fallback_when_describe_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_compute_environment.return_value = {
            "computeEnvironmentArn": CE_ARN,
        }
        mock_client.describe_compute_environments.return_value = {
            "computeEnvironments": []
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_compute_environment(CE_NAME, region_name=REGION)
        assert result.name == CE_NAME

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_compute_environment.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_compute_environment failed"):
            update_compute_environment(CE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_compute_environment
# ---------------------------------------------------------------------------


class TestDeleteComputeEnvironment:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_compute_environment.return_value = {}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        delete_compute_environment(CE_NAME, region_name=REGION)
        mock_client.delete_compute_environment.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_compute_environment.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_compute_environment failed"):
            delete_compute_environment(CE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# create_job_queue
# ---------------------------------------------------------------------------


class TestCreateJobQueue:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_job_queue.return_value = {
            "jobQueueArn": JQ_ARN,
            "jobQueueName": JQ_NAME,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        ce_order = [{"computeEnvironment": CE_ARN, "order": 1}]
        result = create_job_queue(
            JQ_NAME, compute_environments=ce_order, region_name=REGION,
        )
        assert isinstance(result, JobQueueResult)
        assert result.arn == JQ_ARN

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_job_queue.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_job_queue failed"):
            create_job_queue(JQ_NAME, compute_environments=[], region_name=REGION)


# ---------------------------------------------------------------------------
# describe_job_queues
# ---------------------------------------------------------------------------


class TestDescribeJobQueues:
    def test_success_with_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_queues.return_value = {
            "jobQueues": [_make_jq_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_job_queues(names=[JQ_NAME], region_name=REGION)
        assert len(result) == 1

    def test_success_without_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_queues.return_value = {"jobQueues": []}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_job_queues(region_name=REGION)
        assert result == []

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_queues.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_job_queues failed"):
            describe_job_queues(region_name=REGION)


# ---------------------------------------------------------------------------
# update_job_queue
# ---------------------------------------------------------------------------


class TestUpdateJobQueue:
    def test_success_with_describe(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_job_queue.return_value = {
            "jobQueueArn": JQ_ARN,
            "jobQueueName": JQ_NAME,
        }
        mock_client.describe_job_queues.return_value = {
            "jobQueues": [_make_jq_dict(state="DISABLED")]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_job_queue(JQ_NAME, state="DISABLED", region_name=REGION)
        assert result.state == "DISABLED"

    def test_with_priority_and_ce(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_job_queue.return_value = {"jobQueueArn": JQ_ARN}
        mock_client.describe_job_queues.return_value = {
            "jobQueues": [_make_jq_dict(priority=5)]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_job_queue(
            JQ_NAME, priority=5,
            compute_environments=[{"computeEnvironment": CE_ARN, "order": 1}],
            region_name=REGION,
        )
        assert result.priority == 5

    def test_fallback_when_describe_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_job_queue.return_value = {"jobQueueArn": JQ_ARN}
        mock_client.describe_job_queues.return_value = {"jobQueues": []}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_job_queue(JQ_NAME, region_name=REGION)
        assert result.name == JQ_NAME

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_job_queue.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_job_queue failed"):
            update_job_queue(JQ_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_job_queue
# ---------------------------------------------------------------------------


class TestDeleteJobQueue:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_job_queue.return_value = {}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        delete_job_queue(JQ_NAME, region_name=REGION)
        mock_client.delete_job_queue.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_job_queue.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_job_queue failed"):
            delete_job_queue(JQ_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# register_job_definition
# ---------------------------------------------------------------------------


class TestRegisterJobDefinition:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.register_job_definition.return_value = {
            "jobDefinitionArn": JD_ARN,
            "jobDefinitionName": JD_NAME,
            "revision": 1,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = register_job_definition(JD_NAME, region_name=REGION)
        assert isinstance(result, JobDefinitionResult)
        assert result.arn == JD_ARN

    def test_with_container_properties(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.register_job_definition.return_value = {
            "jobDefinitionArn": JD_ARN,
            "jobDefinitionName": JD_NAME,
            "revision": 1,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        props = {"image": "busybox", "vcpus": 1, "memory": 512}
        result = register_job_definition(
            JD_NAME, container_properties=props, region_name=REGION,
        )
        assert result.container_properties == props

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.register_job_definition.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="register_job_definition failed"):
            register_job_definition(JD_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_job_definitions
# ---------------------------------------------------------------------------


class TestDescribeJobDefinitions:
    def test_success_with_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_definitions.return_value = {
            "jobDefinitions": [_make_jd_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_job_definitions(names=[JD_NAME], region_name=REGION)
        assert len(result) == 1

    def test_success_without_names(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_definitions.return_value = {"jobDefinitions": []}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_job_definitions(region_name=REGION)
        assert result == []

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_job_definitions.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_job_definitions failed"):
            describe_job_definitions(region_name=REGION)


# ---------------------------------------------------------------------------
# deregister_job_definition
# ---------------------------------------------------------------------------


class TestDeregisterJobDefinition:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.deregister_job_definition.return_value = {}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        deregister_job_definition(JD_ARN, region_name=REGION)
        mock_client.deregister_job_definition.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.deregister_job_definition.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="deregister_job_definition failed"):
            deregister_job_definition(JD_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# submit_job
# ---------------------------------------------------------------------------


class TestSubmitJob:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.submit_job.return_value = {
            "jobId": JOB_ID,
            "jobName": JOB_NAME,
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = submit_job(
            JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
            region_name=REGION,
        )
        assert result == JOB_ID

    def test_with_parameters_and_overrides(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.submit_job.return_value = {"jobId": JOB_ID, "jobName": JOB_NAME}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = submit_job(
            JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
            parameters={"key": "value"},
            container_overrides={"vcpus": 2},
            region_name=REGION,
        )
        assert result == JOB_ID
        call_kwargs = mock_client.submit_job.call_args[1]
        assert call_kwargs["parameters"] == {"key": "value"}
        assert call_kwargs["containerOverrides"] == {"vcpus": 2}

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.submit_job.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="submit_job failed"):
            submit_job(JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
                       region_name=REGION)


# ---------------------------------------------------------------------------
# describe_jobs
# ---------------------------------------------------------------------------


class TestDescribeJobs:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_jobs.return_value = {
            "jobs": [_make_job_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_jobs([JOB_ID], region_name=REGION)
        assert len(result) == 1
        assert result[0].job_id == JOB_ID

    def test_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_jobs.return_value = {"jobs": []}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_jobs(["nonexistent"], region_name=REGION)
        assert result == []

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_jobs.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_jobs failed"):
            describe_jobs([JOB_ID], region_name=REGION)


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------


class TestListJobs:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_jobs.return_value = {
            "jobSummaryList": [_make_job_dict()]
        }
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_jobs(JQ_NAME, region_name=REGION)
        assert len(result) == 1

    def test_with_status_filter(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_jobs.return_value = {"jobSummaryList": []}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_jobs(JQ_NAME, job_status="RUNNING", region_name=REGION)
        assert result == []
        call_kwargs = mock_client.list_jobs.call_args[1]
        assert call_kwargs["jobStatus"] == "RUNNING"

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_jobs.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_jobs failed"):
            list_jobs(JQ_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# cancel_job
# ---------------------------------------------------------------------------


class TestCancelJob:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.cancel_job.return_value = {}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        cancel_job(JOB_ID, reason="Testing", region_name=REGION)
        mock_client.cancel_job.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.cancel_job.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="cancel_job failed"):
            cancel_job(JOB_ID, reason="Testing", region_name=REGION)


# ---------------------------------------------------------------------------
# terminate_job
# ---------------------------------------------------------------------------


class TestTerminateJob:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.terminate_job.return_value = {}
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        terminate_job(JOB_ID, reason="Testing", region_name=REGION)
        mock_client.terminate_job.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.terminate_job.side_effect = _client_error()
        monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="terminate_job failed"):
            terminate_job(JOB_ID, reason="Testing", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_job
# ---------------------------------------------------------------------------


class TestWaitForJob:
    def test_already_succeeded(self, monkeypatch):
        monkeypatch.setattr(
            batch_mod, "describe_jobs",
            lambda *a, **kw: [JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="SUCCEEDED",
            )],
        )
        result = wait_for_job(JOB_ID, timeout=5.0, poll_interval=0.01,
                              region_name=REGION)
        assert result.status == "SUCCEEDED"

    def test_job_not_found(self, monkeypatch):
        monkeypatch.setattr(batch_mod, "describe_jobs", lambda *a, **kw: [])
        with pytest.raises(RuntimeError, match="not found"):
            wait_for_job(JOB_ID, timeout=1.0, region_name=REGION)

    def test_job_failure_status(self, monkeypatch):
        monkeypatch.setattr(
            batch_mod, "describe_jobs",
            lambda *a, **kw: [JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="FAILED",
                status_reason="OutOfMemory",
            )],
        )
        with pytest.raises(RuntimeError, match="failure status"):
            wait_for_job(JOB_ID, timeout=5.0, region_name=REGION)

    def test_job_failure_no_reason(self, monkeypatch):
        monkeypatch.setattr(
            batch_mod, "describe_jobs",
            lambda *a, **kw: [JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="FAILED",
            )],
        )
        with pytest.raises(RuntimeError, match="no reason"):
            wait_for_job(JOB_ID, timeout=5.0, region_name=REGION)

    def test_timeout(self, monkeypatch):
        monkeypatch.setattr(
            batch_mod, "describe_jobs",
            lambda *a, **kw: [JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="RUNNING",
            )],
        )
        with pytest.raises((TimeoutError, AwsTimeoutError)):
            wait_for_job(JOB_ID, timeout=0.0, poll_interval=0.0,
                         region_name=REGION)

    def test_poll_then_success(self, monkeypatch):
        import time as _t
        monkeypatch.setattr(_t, "sleep", lambda s: None)

        call_count = {"n": 0}

        def fake_describe(job_ids, region_name=None):
            call_count["n"] += 1
            if call_count["n"] < 2:
                return [JobResult(
                    job_id=JOB_ID, job_name=JOB_NAME,
                    job_queue=JQ_ARN, status="RUNNING",
                )]
            return [JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="SUCCEEDED",
            )]

        monkeypatch.setattr(batch_mod, "describe_jobs", fake_describe)
        result = wait_for_job(
            JOB_ID, timeout=10.0, poll_interval=0.001,
            region_name=REGION,
        )
        assert result.status == "SUCCEEDED"


# ---------------------------------------------------------------------------
# submit_and_wait
# ---------------------------------------------------------------------------


class TestSubmitAndWait:
    def test_success(self, monkeypatch):
        monkeypatch.setattr(
            batch_mod, "submit_job", lambda *a, **kw: JOB_ID,
        )
        monkeypatch.setattr(
            batch_mod, "wait_for_job",
            lambda *a, **kw: JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="SUCCEEDED",
            ),
        )
        result = submit_and_wait(
            JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
            region_name=REGION,
        )
        assert result.status == "SUCCEEDED"

    def test_with_params_and_overrides(self, monkeypatch):
        monkeypatch.setattr(batch_mod, "submit_job", lambda *a, **kw: JOB_ID)
        monkeypatch.setattr(
            batch_mod, "wait_for_job",
            lambda *a, **kw: JobResult(
                job_id=JOB_ID, job_name=JOB_NAME,
                job_queue=JQ_ARN, status="SUCCEEDED",
            ),
        )
        result = submit_and_wait(
            JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
            parameters={"key": "val"},
            container_overrides={"vcpus": 2},
            timeout=30, poll_interval=1,
            region_name=REGION,
        )
        assert result.status == "SUCCEEDED"


def test_create_consumable_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_consumable_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    create_consumable_resource("test-consumable_resource_name", region_name=REGION)
    mock_client.create_consumable_resource.assert_called_once()


def test_create_consumable_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_consumable_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_consumable_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create consumable resource"):
        create_consumable_resource("test-consumable_resource_name", region_name=REGION)


def test_create_scheduling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduling_policy.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    create_scheduling_policy("test-name", region_name=REGION)
    mock_client.create_scheduling_policy.assert_called_once()


def test_create_scheduling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_scheduling_policy",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create scheduling policy"):
        create_scheduling_policy("test-name", region_name=REGION)


def test_create_service_environment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_environment.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    create_service_environment("test-service_environment_name", "test-service_environment_type", [], region_name=REGION)
    mock_client.create_service_environment.assert_called_once()


def test_create_service_environment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_environment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_environment",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service environment"):
        create_service_environment("test-service_environment_name", "test-service_environment_type", [], region_name=REGION)


def test_delete_consumable_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_consumable_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    delete_consumable_resource("test-consumable_resource", region_name=REGION)
    mock_client.delete_consumable_resource.assert_called_once()


def test_delete_consumable_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_consumable_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_consumable_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete consumable resource"):
        delete_consumable_resource("test-consumable_resource", region_name=REGION)


def test_delete_scheduling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduling_policy.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    delete_scheduling_policy("test-arn", region_name=REGION)
    mock_client.delete_scheduling_policy.assert_called_once()


def test_delete_scheduling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_scheduling_policy",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete scheduling policy"):
        delete_scheduling_policy("test-arn", region_name=REGION)


def test_delete_service_environment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_environment.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    delete_service_environment("test-service_environment", region_name=REGION)
    mock_client.delete_service_environment.assert_called_once()


def test_delete_service_environment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_environment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_environment",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service environment"):
        delete_service_environment("test-service_environment", region_name=REGION)


def test_describe_consumable_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_consumable_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    describe_consumable_resource("test-consumable_resource", region_name=REGION)
    mock_client.describe_consumable_resource.assert_called_once()


def test_describe_consumable_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_consumable_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_consumable_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe consumable resource"):
        describe_consumable_resource("test-consumable_resource", region_name=REGION)


def test_describe_scheduling_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduling_policies.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    describe_scheduling_policies([], region_name=REGION)
    mock_client.describe_scheduling_policies.assert_called_once()


def test_describe_scheduling_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduling_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduling_policies",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scheduling policies"):
        describe_scheduling_policies([], region_name=REGION)


def test_describe_service_environments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_environments.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    describe_service_environments(region_name=REGION)
    mock_client.describe_service_environments.assert_called_once()


def test_describe_service_environments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_environments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_environments",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service environments"):
        describe_service_environments(region_name=REGION)


def test_describe_service_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_job.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    describe_service_job("test-job_id", region_name=REGION)
    mock_client.describe_service_job.assert_called_once()


def test_describe_service_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_job",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service job"):
        describe_service_job("test-job_id", region_name=REGION)


def test_get_job_queue_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_queue_snapshot.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    get_job_queue_snapshot("test-job_queue", region_name=REGION)
    mock_client.get_job_queue_snapshot.assert_called_once()


def test_get_job_queue_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_queue_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_job_queue_snapshot",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get job queue snapshot"):
        get_job_queue_snapshot("test-job_queue", region_name=REGION)


def test_list_consumable_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_consumable_resources.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    list_consumable_resources(region_name=REGION)
    mock_client.list_consumable_resources.assert_called_once()


def test_list_consumable_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_consumable_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_consumable_resources",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list consumable resources"):
        list_consumable_resources(region_name=REGION)


def test_list_jobs_by_consumable_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_jobs_by_consumable_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    list_jobs_by_consumable_resource("test-consumable_resource", region_name=REGION)
    mock_client.list_jobs_by_consumable_resource.assert_called_once()


def test_list_jobs_by_consumable_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_jobs_by_consumable_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_jobs_by_consumable_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list jobs by consumable resource"):
        list_jobs_by_consumable_resource("test-consumable_resource", region_name=REGION)


def test_list_scheduling_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scheduling_policies.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    list_scheduling_policies(region_name=REGION)
    mock_client.list_scheduling_policies.assert_called_once()


def test_list_scheduling_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scheduling_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_scheduling_policies",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list scheduling policies"):
        list_scheduling_policies(region_name=REGION)


def test_list_service_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_jobs.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    list_service_jobs(region_name=REGION)
    mock_client.list_service_jobs.assert_called_once()


def test_list_service_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_jobs",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service jobs"):
        list_service_jobs(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_submit_service_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_service_job.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", region_name=REGION)
    mock_client.submit_service_job.assert_called_once()


def test_submit_service_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_service_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "submit_service_job",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to submit service job"):
        submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_terminate_service_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_service_job.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    terminate_service_job("test-job_id", "test-reason", region_name=REGION)
    mock_client.terminate_service_job.assert_called_once()


def test_terminate_service_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_service_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "terminate_service_job",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate service job"):
        terminate_service_job("test-job_id", "test-reason", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_consumable_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_consumable_resource.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    update_consumable_resource("test-consumable_resource", region_name=REGION)
    mock_client.update_consumable_resource.assert_called_once()


def test_update_consumable_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_consumable_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_consumable_resource",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update consumable resource"):
        update_consumable_resource("test-consumable_resource", region_name=REGION)


def test_update_scheduling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_scheduling_policy.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    update_scheduling_policy("test-arn", region_name=REGION)
    mock_client.update_scheduling_policy.assert_called_once()


def test_update_scheduling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_scheduling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_scheduling_policy",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update scheduling policy"):
        update_scheduling_policy("test-arn", region_name=REGION)


def test_update_service_environment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_environment.return_value = {}
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    update_service_environment("test-service_environment", region_name=REGION)
    mock_client.update_service_environment.assert_called_once()


def test_update_service_environment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_environment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_service_environment",
    )
    monkeypatch.setattr(batch_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update service environment"):
        update_service_environment("test-service_environment", region_name=REGION)


def test_describe_compute_environments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import describe_compute_environments
    mock_client = MagicMock()
    mock_client.describe_compute_environments.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    describe_compute_environments(names="test-names", region_name="us-east-1")
    mock_client.describe_compute_environments.assert_called_once()

def test_update_compute_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import update_compute_environment
    mock_client = MagicMock()
    mock_client.update_compute_environment.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    update_compute_environment("test-name", state="test-state", compute_resources="test-compute_resources", region_name="us-east-1")
    mock_client.update_compute_environment.assert_called_once()

def test_describe_job_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import describe_job_queues
    mock_client = MagicMock()
    mock_client.describe_job_queues.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    describe_job_queues(names="test-names", region_name="us-east-1")
    mock_client.describe_job_queues.assert_called_once()

def test_describe_job_definitions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import describe_job_definitions
    mock_client = MagicMock()
    mock_client.describe_job_definitions.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    describe_job_definitions(names="test-names", region_name="us-east-1")
    mock_client.describe_job_definitions.assert_called_once()

def test_list_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import list_jobs
    mock_client = MagicMock()
    mock_client.list_jobs.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    list_jobs("test-job_queue", job_status="test-job_status", region_name="us-east-1")
    mock_client.list_jobs.assert_called_once()

def test_create_consumable_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import create_consumable_resource
    mock_client = MagicMock()
    mock_client.create_consumable_resource.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    create_consumable_resource("test-consumable_resource_name", total_quantity="test-total_quantity", resource_type="test-resource_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_consumable_resource.assert_called_once()

def test_create_scheduling_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import create_scheduling_policy
    mock_client = MagicMock()
    mock_client.create_scheduling_policy.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    create_scheduling_policy("test-name", fairshare_policy="{}", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_scheduling_policy.assert_called_once()

def test_create_service_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import create_service_environment
    mock_client = MagicMock()
    mock_client.create_service_environment.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    create_service_environment("test-service_environment_name", "test-service_environment_type", 1, state="test-state", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_service_environment.assert_called_once()

def test_describe_service_environments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import describe_service_environments
    mock_client = MagicMock()
    mock_client.describe_service_environments.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    describe_service_environments(service_environments="test-service_environments", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_service_environments.assert_called_once()

def test_list_consumable_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import list_consumable_resources
    mock_client = MagicMock()
    mock_client.list_consumable_resources.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    list_consumable_resources(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_consumable_resources.assert_called_once()

def test_list_jobs_by_consumable_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import list_jobs_by_consumable_resource
    mock_client = MagicMock()
    mock_client.list_jobs_by_consumable_resource.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    list_jobs_by_consumable_resource("test-consumable_resource", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_jobs_by_consumable_resource.assert_called_once()

def test_list_scheduling_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import list_scheduling_policies
    mock_client = MagicMock()
    mock_client.list_scheduling_policies.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    list_scheduling_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_scheduling_policies.assert_called_once()

def test_list_service_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import list_service_jobs
    mock_client = MagicMock()
    mock_client.list_service_jobs.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    list_service_jobs(job_queue="test-job_queue", job_status="test-job_status", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.list_service_jobs.assert_called_once()

def test_submit_service_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import submit_service_job
    mock_client = MagicMock()
    mock_client.submit_service_job.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", retry_strategy="test-retry_strategy", scheduling_priority="test-scheduling_priority", share_identifier="test-share_identifier", timeout_config=1, tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.submit_service_job.assert_called_once()

def test_update_consumable_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import update_consumable_resource
    mock_client = MagicMock()
    mock_client.update_consumable_resource.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    update_consumable_resource("test-consumable_resource", operation="test-operation", quantity="test-quantity", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_consumable_resource.assert_called_once()

def test_update_scheduling_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import update_scheduling_policy
    mock_client = MagicMock()
    mock_client.update_scheduling_policy.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    update_scheduling_policy("test-arn", fairshare_policy="{}", region_name="us-east-1")
    mock_client.update_scheduling_policy.assert_called_once()

def test_update_service_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.batch import update_service_environment
    mock_client = MagicMock()
    mock_client.update_service_environment.return_value = {}
    monkeypatch.setattr("aws_util.batch.get_client", lambda *a, **kw: mock_client)
    update_service_environment("test-service_environment", state="test-state", capacity_limits=1, region_name="us-east-1")
    mock_client.update_service_environment.assert_called_once()
