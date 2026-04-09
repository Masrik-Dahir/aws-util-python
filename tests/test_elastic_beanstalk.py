"""Tests for aws_util.elastic_beanstalk -- 100% line coverage."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.elastic_beanstalk as mod
from aws_util.elastic_beanstalk import (
    ApplicationResult,
    ApplicationVersionResult,
    EnvironmentResult,
    EventResult,
    InstanceHealthResult,
    _parse_application,
    _parse_application_version,
    _parse_environment,
    _parse_event,
    _parse_instance_health,
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


def _ce(code: str = "ServiceException", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


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
# Parser tests
# ---------------------------------------------------------------------------


class TestParseApplication:
    def test_full(self):
        r = _parse_application(_APP)
        assert r.application_name == "myapp"
        assert r.description == "desc"
        assert r.date_created == "2025-01-01"
        assert r.date_updated == "2025-01-02"
        assert r.versions == ["v1"]
        assert r.extra == {"ExtraKey": "x"}

    def test_no_dates(self):
        r = _parse_application({"ApplicationName": "a"})
        assert r.date_created is None
        assert r.date_updated is None

    def test_none_dates(self):
        data = {**_APP, "DateCreated": None, "DateUpdated": None}
        r = _parse_application(data)
        assert r.date_created is None
        assert r.date_updated is None


class TestParseEnvironment:
    def test_full(self):
        r = _parse_environment(_ENV)
        assert r.environment_id == "e-123"
        assert r.environment_name == "myenv"
        assert r.status == "Ready"
        assert r.cname == "myenv.elasticbeanstalk.com"
        assert r.extra == {"ExtraEnv": "y"}

    def test_minimal(self):
        r = _parse_environment({"EnvironmentId": "e", "Status": "Ready"})
        assert r.environment_name == ""


class TestParseApplicationVersion:
    def test_full(self):
        r = _parse_application_version(_AV)
        assert r.version_label == "v1"
        assert r.status == "PROCESSED"
        assert r.extra == {"ExtraAv": "z"}

    def test_no_date(self):
        r = _parse_application_version(
            {"ApplicationName": "a", "VersionLabel": "v"}
        )
        assert r.date_created is None

    def test_none_date(self):
        data = {**_AV, "DateCreated": None}
        r = _parse_application_version(data)
        assert r.date_created is None


class TestParseEvent:
    def test_full(self):
        r = _parse_event(_EVT)
        assert r.message == "event msg"
        assert r.severity == "INFO"
        assert r.extra == {"ExtraEvt": "w"}

    def test_no_date(self):
        r = _parse_event({"Message": "m"})
        assert r.event_date is None

    def test_none_date(self):
        data = {**_EVT, "EventDate": None}
        r = _parse_event(data)
        assert r.event_date is None


class TestParseInstanceHealth:
    def test_full(self):
        r = _parse_instance_health(_IH)
        assert r.instance_id == "i-123"
        assert r.causes == ["cause1"]
        assert r.extra == {"ExtraIh": "q"}

    def test_minimal(self):
        r = _parse_instance_health({"InstanceId": "i"})
        assert r.health_status == ""


# ---------------------------------------------------------------------------
# Application operations
# ---------------------------------------------------------------------------


class TestCreateApplication:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application.return_value = {"Application": _APP}
        r = create_application("myapp", description="desc")
        assert r.application_name == "myapp"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_no_description(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application.return_value = {"Application": _APP}
        r = create_application("myapp")
        assert isinstance(r, ApplicationResult)

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application.side_effect = _ce()
        with pytest.raises(RuntimeError, match="create_application failed"):
            create_application("myapp")


class TestDescribeApplications:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_applications.return_value = {
            "Applications": [_APP],
        }
        r = describe_applications()
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_with_names(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_applications.return_value = {
            "Applications": [_APP],
        }
        r = describe_applications(application_names=["myapp"])
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_applications.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="describe_applications failed"
        ):
            describe_applications()


class TestDeleteApplication:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_application("myapp")
        client.delete_application.assert_called_once()

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_force(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_application("myapp", terminate_env_by_force=True)
        kw = client.delete_application.call_args[1]
        assert kw["TerminateEnvByForce"] is True

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_application.side_effect = _ce()
        with pytest.raises(RuntimeError, match="delete_application failed"):
            delete_application("myapp")


# ---------------------------------------------------------------------------
# Environment operations
# ---------------------------------------------------------------------------


class TestCreateEnvironment:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_environment.return_value = _ENV
        r = create_environment("myapp", "myenv")
        assert r.environment_name == "myenv"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_environment.return_value = _ENV
        r = create_environment(
            "myapp",
            "myenv",
            solution_stack_name="stack",
            version_label="v1",
            option_settings=[
                {"Namespace": "ns", "OptionName": "on", "Value": "v"}
            ],
        )
        assert r.environment_name == "myenv"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_environment.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="create_environment failed"
        ):
            create_environment("myapp", "myenv")


class TestDescribeEnvironments:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_environments.return_value = {
            "Environments": [_ENV],
        }
        r = describe_environments()
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_all_filters(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_environments.return_value = {
            "Environments": [_ENV],
        }
        r = describe_environments(
            application_name="myapp",
            environment_names=["myenv"],
            environment_ids=["e-123"],
        )
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_environments.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="describe_environments failed"
        ):
            describe_environments()


class TestUpdateEnvironment:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_environment.return_value = _ENV
        r = update_environment("myenv")
        assert r.environment_name == "myenv"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_environment.return_value = _ENV
        r = update_environment(
            "myenv",
            version_label="v2",
            option_settings=[
                {"Namespace": "ns", "OptionName": "on", "Value": "v"}
            ],
        )
        assert r.environment_name == "myenv"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_environment.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="update_environment failed"
        ):
            update_environment("myenv")


class TestTerminateEnvironment:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.terminate_environment.return_value = _ENV
        r = terminate_environment("myenv")
        assert isinstance(r, EnvironmentResult)

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_force(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.terminate_environment.return_value = _ENV
        terminate_environment("myenv", force_terminate=True)
        kw = client.terminate_environment.call_args[1]
        assert kw["ForceTerminate"] is True

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.terminate_environment.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="terminate_environment failed"
        ):
            terminate_environment("myenv")


# ---------------------------------------------------------------------------
# Application version operations
# ---------------------------------------------------------------------------


class TestCreateApplicationVersion:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application_version.return_value = {
            "ApplicationVersion": _AV,
        }
        r = create_application_version("myapp", "v1", description="d")
        assert r.version_label == "v1"

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_with_source(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application_version.return_value = {
            "ApplicationVersion": _AV,
        }
        r = create_application_version(
            "myapp",
            "v1",
            source_bundle={"S3Bucket": "b", "S3Key": "k"},
        )
        assert isinstance(r, ApplicationVersionResult)

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_no_desc(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application_version.return_value = {
            "ApplicationVersion": _AV,
        }
        r = create_application_version("myapp", "v1")
        assert isinstance(r, ApplicationVersionResult)

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_application_version.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="create_application_version failed"
        ):
            create_application_version("myapp", "v1")


class TestDescribeApplicationVersions:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_application_versions.return_value = {
            "ApplicationVersions": [_AV],
        }
        r = describe_application_versions("myapp")
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_with_labels(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_application_versions.return_value = {
            "ApplicationVersions": [_AV],
        }
        r = describe_application_versions(
            "myapp", version_labels=["v1"]
        )
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_application_versions.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="describe_application_versions failed"
        ):
            describe_application_versions("myapp")


class TestDeleteApplicationVersion:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_application_version("myapp", "v1")
        client.delete_application_version.assert_called_once()

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_delete_source(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_application_version(
            "myapp", "v1", delete_source_bundle=True
        )
        kw = client.delete_application_version.call_args[1]
        assert kw["DeleteSourceBundle"] is True

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_application_version.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="delete_application_version failed"
        ):
            delete_application_version("myapp", "v1")


# ---------------------------------------------------------------------------
# Events and health
# ---------------------------------------------------------------------------


class TestDescribeEvents:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_events.return_value = {"Events": [_EVT]}
        r = describe_events()
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_events.return_value = {"Events": [_EVT]}
        r = describe_events(
            application_name="myapp",
            environment_name="myenv",
            max_records=10,
        )
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_events.side_effect = _ce()
        with pytest.raises(RuntimeError, match="describe_events failed"):
            describe_events()


class TestDescribeInstancesHealth:
    @patch("aws_util.elastic_beanstalk.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_instances_health.return_value = {
            "InstanceHealthList": [_IH],
        }
        r = describe_instances_health("myenv")
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_with_attrs(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_instances_health.return_value = {
            "InstanceHealthList": [_IH],
        }
        r = describe_instances_health(
            "myenv", attribute_names=["HealthStatus"]
        )
        assert len(r) == 1

    @patch("aws_util.elastic_beanstalk.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_instances_health.side_effect = _ce()
        with pytest.raises(
            RuntimeError, match="describe_instances_health failed"
        ):
            describe_instances_health("myenv")


# ---------------------------------------------------------------------------
# wait_for_environment
# ---------------------------------------------------------------------------


class TestWaitForEnvironment:
    def test_already_ready(self, monkeypatch):
        env = EnvironmentResult(
            environment_id="e-1",
            environment_name="myenv",
            application_name="myapp",
            status="Ready",
        )
        monkeypatch.setattr(
            mod, "describe_environments", lambda **kw: [env]
        )
        r = wait_for_environment(
            "myenv", timeout=5, poll_interval=0.01
        )
        assert r.status == "Ready"

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(
            mod, "describe_environments", lambda **kw: []
        )
        with pytest.raises(AwsServiceError, match="not found"):
            wait_for_environment(
                "myenv", timeout=1, poll_interval=0.01
            )

    def test_terminated(self, monkeypatch):
        env = EnvironmentResult(
            environment_id="e-1",
            environment_name="myenv",
            application_name="myapp",
            status="Terminated",
        )
        monkeypatch.setattr(
            mod, "describe_environments", lambda **kw: [env]
        )
        with pytest.raises(AwsServiceError, match="was terminated"):
            wait_for_environment(
                "myenv", timeout=1, poll_interval=0.01
            )

    def test_timeout(self, monkeypatch):
        env = EnvironmentResult(
            environment_id="e-1",
            environment_name="myenv",
            application_name="myapp",
            status="Launching",
        )
        monkeypatch.setattr(
            mod, "describe_environments", lambda **kw: [env]
        )
        monkeypatch.setattr(time, "sleep", lambda s: None)
        with pytest.raises(AwsTimeoutError, match="did not reach"):
            wait_for_environment(
                "myenv", timeout=0.0, poll_interval=0.0
            )

    def test_polls_then_ready(self, monkeypatch):
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
        call_count = {"n": 0}

        def fake_desc(**kw):
            call_count["n"] += 1
            return [launching] if call_count["n"] < 2 else [ready]

        monkeypatch.setattr(mod, "describe_environments", fake_desc)
        monkeypatch.setattr(time, "sleep", lambda s: None)
        r = wait_for_environment(
            "myenv", timeout=10.0, poll_interval=0.001
        )
        assert r.status == "Ready"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_application_result_model():
    r = ApplicationResult(application_name="a")
    assert r.application_name == "a"


def test_environment_result_model():
    r = EnvironmentResult(
        environment_id="e-1",
        environment_name="e",
        application_name="a",
        status="Ready",
    )
    assert r.status == "Ready"


def test_application_version_result_model():
    r = ApplicationVersionResult(
        application_name="a", version_label="v"
    )
    assert r.version_label == "v"


def test_event_result_model():
    r = EventResult()
    assert r.message == ""


def test_instance_health_result_model():
    r = InstanceHealthResult(instance_id="i")
    assert r.instance_id == "i"


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


@patch("aws_util.elastic_beanstalk.get_client")
def test_abort_environment_update(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.abort_environment_update.return_value = {}
    abort_environment_update(region_name=REGION)
    mock_client.abort_environment_update.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_abort_environment_update_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.abort_environment_update.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "abort_environment_update",
    )
    with pytest.raises(RuntimeError, match="Failed to abort environment update"):
        abort_environment_update(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_apply_environment_managed_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_environment_managed_action.return_value = {}
    apply_environment_managed_action("test-action_id", region_name=REGION)
    mock_client.apply_environment_managed_action.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_apply_environment_managed_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_environment_managed_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_environment_managed_action",
    )
    with pytest.raises(RuntimeError, match="Failed to apply environment managed action"):
        apply_environment_managed_action("test-action_id", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_associate_environment_operations_role(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_environment_operations_role.return_value = {}
    associate_environment_operations_role("test-environment_name", "test-operations_role", region_name=REGION)
    mock_client.associate_environment_operations_role.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_associate_environment_operations_role_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_environment_operations_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_environment_operations_role",
    )
    with pytest.raises(RuntimeError, match="Failed to associate environment operations role"):
        associate_environment_operations_role("test-environment_name", "test-operations_role", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_check_dns_availability(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.check_dns_availability.return_value = {}
    check_dns_availability("test-cname_prefix", region_name=REGION)
    mock_client.check_dns_availability.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_check_dns_availability_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.check_dns_availability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "check_dns_availability",
    )
    with pytest.raises(RuntimeError, match="Failed to check dns availability"):
        check_dns_availability("test-cname_prefix", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_compose_environments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.compose_environments.return_value = {}
    compose_environments(region_name=REGION)
    mock_client.compose_environments.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_compose_environments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.compose_environments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "compose_environments",
    )
    with pytest.raises(RuntimeError, match="Failed to compose environments"):
        compose_environments(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_configuration_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_configuration_template.return_value = {}
    create_configuration_template("test-application_name", "test-template_name", region_name=REGION)
    mock_client.create_configuration_template.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_configuration_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_configuration_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_template",
    )
    with pytest.raises(RuntimeError, match="Failed to create configuration template"):
        create_configuration_template("test-application_name", "test-template_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_platform_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_platform_version.return_value = {}
    create_platform_version("test-platform_name", "test-platform_version", {}, region_name=REGION)
    mock_client.create_platform_version.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_platform_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_platform_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_platform_version",
    )
    with pytest.raises(RuntimeError, match="Failed to create platform version"):
        create_platform_version("test-platform_name", "test-platform_version", {}, region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_storage_location(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_storage_location.return_value = {}
    create_storage_location(region_name=REGION)
    mock_client.create_storage_location.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_create_storage_location_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_storage_location.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_storage_location",
    )
    with pytest.raises(RuntimeError, match="Failed to create storage location"):
        create_storage_location(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_configuration_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_configuration_template.return_value = {}
    delete_configuration_template("test-application_name", "test-template_name", region_name=REGION)
    mock_client.delete_configuration_template.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_configuration_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_configuration_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_template",
    )
    with pytest.raises(RuntimeError, match="Failed to delete configuration template"):
        delete_configuration_template("test-application_name", "test-template_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_environment_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_environment_configuration.return_value = {}
    delete_environment_configuration("test-application_name", "test-environment_name", region_name=REGION)
    mock_client.delete_environment_configuration.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_environment_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_environment_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_environment_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete environment configuration"):
        delete_environment_configuration("test-application_name", "test-environment_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_platform_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_platform_version.return_value = {}
    delete_platform_version(region_name=REGION)
    mock_client.delete_platform_version.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_delete_platform_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_platform_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_platform_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete platform version"):
        delete_platform_version(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_account_attributes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_attributes.return_value = {}
    describe_account_attributes(region_name=REGION)
    mock_client.describe_account_attributes.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_account_attributes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_attributes",
    )
    with pytest.raises(RuntimeError, match="Failed to describe account attributes"):
        describe_account_attributes(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_configuration_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_configuration_options.return_value = {}
    describe_configuration_options(region_name=REGION)
    mock_client.describe_configuration_options.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_configuration_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_configuration_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_options",
    )
    with pytest.raises(RuntimeError, match="Failed to describe configuration options"):
        describe_configuration_options(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_configuration_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_configuration_settings.return_value = {}
    describe_configuration_settings("test-application_name", region_name=REGION)
    mock_client.describe_configuration_settings.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_configuration_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_configuration_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to describe configuration settings"):
        describe_configuration_settings("test-application_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_health(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_health.return_value = {}
    describe_environment_health(region_name=REGION)
    mock_client.describe_environment_health.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_health_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_health.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_environment_health",
    )
    with pytest.raises(RuntimeError, match="Failed to describe environment health"):
        describe_environment_health(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_managed_action_history(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_managed_action_history.return_value = {}
    describe_environment_managed_action_history(region_name=REGION)
    mock_client.describe_environment_managed_action_history.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_managed_action_history_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_managed_action_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_environment_managed_action_history",
    )
    with pytest.raises(RuntimeError, match="Failed to describe environment managed action history"):
        describe_environment_managed_action_history(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_managed_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_managed_actions.return_value = {}
    describe_environment_managed_actions(region_name=REGION)
    mock_client.describe_environment_managed_actions.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_managed_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_managed_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_environment_managed_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe environment managed actions"):
        describe_environment_managed_actions(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_resources(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_resources.return_value = {}
    describe_environment_resources(region_name=REGION)
    mock_client.describe_environment_resources.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_environment_resources_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_environment_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_environment_resources",
    )
    with pytest.raises(RuntimeError, match="Failed to describe environment resources"):
        describe_environment_resources(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_platform_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_platform_version.return_value = {}
    describe_platform_version(region_name=REGION)
    mock_client.describe_platform_version.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_describe_platform_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_platform_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_platform_version",
    )
    with pytest.raises(RuntimeError, match="Failed to describe platform version"):
        describe_platform_version(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_disassociate_environment_operations_role(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_environment_operations_role.return_value = {}
    disassociate_environment_operations_role("test-environment_name", region_name=REGION)
    mock_client.disassociate_environment_operations_role.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_disassociate_environment_operations_role_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_environment_operations_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_environment_operations_role",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate environment operations role"):
        disassociate_environment_operations_role("test-environment_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_available_solution_stacks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_available_solution_stacks.return_value = {}
    list_available_solution_stacks(region_name=REGION)
    mock_client.list_available_solution_stacks.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_available_solution_stacks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_available_solution_stacks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_available_solution_stacks",
    )
    with pytest.raises(RuntimeError, match="Failed to list available solution stacks"):
        list_available_solution_stacks(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_platform_branches(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_platform_branches.return_value = {}
    list_platform_branches(region_name=REGION)
    mock_client.list_platform_branches.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_platform_branches_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_platform_branches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_platform_branches",
    )
    with pytest.raises(RuntimeError, match="Failed to list platform branches"):
        list_platform_branches(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_platform_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_platform_versions.return_value = {}
    list_platform_versions(region_name=REGION)
    mock_client.list_platform_versions.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_platform_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_platform_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_platform_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list platform versions"):
        list_platform_versions(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_rebuild_environment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.rebuild_environment.return_value = {}
    rebuild_environment(region_name=REGION)
    mock_client.rebuild_environment.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_rebuild_environment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.rebuild_environment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rebuild_environment",
    )
    with pytest.raises(RuntimeError, match="Failed to rebuild environment"):
        rebuild_environment(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_request_environment_info(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.request_environment_info.return_value = {}
    request_environment_info("test-info_type", region_name=REGION)
    mock_client.request_environment_info.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_request_environment_info_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.request_environment_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "request_environment_info",
    )
    with pytest.raises(RuntimeError, match="Failed to request environment info"):
        request_environment_info("test-info_type", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_restart_app_server(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restart_app_server.return_value = {}
    restart_app_server(region_name=REGION)
    mock_client.restart_app_server.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_restart_app_server_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restart_app_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restart_app_server",
    )
    with pytest.raises(RuntimeError, match="Failed to restart app server"):
        restart_app_server(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_retrieve_environment_info(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.retrieve_environment_info.return_value = {}
    retrieve_environment_info("test-info_type", region_name=REGION)
    mock_client.retrieve_environment_info.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_retrieve_environment_info_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.retrieve_environment_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retrieve_environment_info",
    )
    with pytest.raises(RuntimeError, match="Failed to retrieve environment info"):
        retrieve_environment_info("test-info_type", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_swap_environment_cnames(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.swap_environment_cnames.return_value = {}
    swap_environment_cnames(region_name=REGION)
    mock_client.swap_environment_cnames.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_swap_environment_cnames_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.swap_environment_cnames.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "swap_environment_cnames",
    )
    with pytest.raises(RuntimeError, match="Failed to swap environment cnames"):
        swap_environment_cnames(region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application.return_value = {}
    update_application("test-application_name", region_name=REGION)
    mock_client.update_application.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application",
    )
    with pytest.raises(RuntimeError, match="Failed to update application"):
        update_application("test-application_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application_resource_lifecycle(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application_resource_lifecycle.return_value = {}
    update_application_resource_lifecycle("test-application_name", {}, region_name=REGION)
    mock_client.update_application_resource_lifecycle.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application_resource_lifecycle_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application_resource_lifecycle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application_resource_lifecycle",
    )
    with pytest.raises(RuntimeError, match="Failed to update application resource lifecycle"):
        update_application_resource_lifecycle("test-application_name", {}, region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application_version.return_value = {}
    update_application_version("test-application_name", "test-version_label", region_name=REGION)
    mock_client.update_application_version.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_application_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_application_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application_version",
    )
    with pytest.raises(RuntimeError, match="Failed to update application version"):
        update_application_version("test-application_name", "test-version_label", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_configuration_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_configuration_template.return_value = {}
    update_configuration_template("test-application_name", "test-template_name", region_name=REGION)
    mock_client.update_configuration_template.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_configuration_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_configuration_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_template",
    )
    with pytest.raises(RuntimeError, match="Failed to update configuration template"):
        update_configuration_template("test-application_name", "test-template_name", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_tags_for_resource.return_value = {}
    update_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.update_tags_for_resource.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_update_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to update tags for resource"):
        update_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.elastic_beanstalk.get_client")
def test_validate_configuration_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.validate_configuration_settings.return_value = {}
    validate_configuration_settings("test-application_name", [], region_name=REGION)
    mock_client.validate_configuration_settings.assert_called_once()


@patch("aws_util.elastic_beanstalk.get_client")
def test_validate_configuration_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.validate_configuration_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_configuration_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to validate configuration settings"):
        validate_configuration_settings("test-application_name", [], region_name=REGION)


def test_describe_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_applications
    mock_client = MagicMock()
    mock_client.describe_applications.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_applications(application_names="test-application_names", region_name="us-east-1")
    mock_client.describe_applications.assert_called_once()

def test_create_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import create_environment
    mock_client = MagicMock()
    mock_client.create_environment.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    create_environment("test-application_name", "test-environment_name", solution_stack_name="test-solution_stack_name", version_label="test-version_label", option_settings={}, region_name="us-east-1")
    mock_client.create_environment.assert_called_once()

def test_describe_environments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_environments
    mock_client = MagicMock()
    mock_client.describe_environments.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_environments(application_name="test-application_name", environment_names="test-environment_names", environment_ids="test-environment_ids", region_name="us-east-1")
    mock_client.describe_environments.assert_called_once()

def test_update_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import update_environment
    mock_client = MagicMock()
    mock_client.update_environment.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    update_environment("test-environment_name", version_label="test-version_label", option_settings={}, region_name="us-east-1")
    mock_client.update_environment.assert_called_once()

def test_describe_application_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_application_versions
    mock_client = MagicMock()
    mock_client.describe_application_versions.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_application_versions("test-application_name", version_labels="test-version_labels", region_name="us-east-1")
    mock_client.describe_application_versions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_events(application_name="test-application_name", environment_name="test-environment_name", max_records=1, region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_instances_health_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_instances_health
    mock_client = MagicMock()
    mock_client.describe_instances_health.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_instances_health("test-environment_name", attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.describe_instances_health.assert_called_once()

def test_abort_environment_update_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import abort_environment_update
    mock_client = MagicMock()
    mock_client.abort_environment_update.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    abort_environment_update(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.abort_environment_update.assert_called_once()

def test_apply_environment_managed_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import apply_environment_managed_action
    mock_client = MagicMock()
    mock_client.apply_environment_managed_action.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    apply_environment_managed_action("test-action_id", environment_name="test-environment_name", environment_id="test-environment_id", region_name="us-east-1")
    mock_client.apply_environment_managed_action.assert_called_once()

def test_compose_environments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import compose_environments
    mock_client = MagicMock()
    mock_client.compose_environments.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    compose_environments(application_name="test-application_name", group_name="test-group_name", version_labels="test-version_labels", region_name="us-east-1")
    mock_client.compose_environments.assert_called_once()

def test_create_configuration_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import create_configuration_template
    mock_client = MagicMock()
    mock_client.create_configuration_template.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    create_configuration_template("test-application_name", "test-template_name", solution_stack_name="test-solution_stack_name", platform_arn="test-platform_arn", source_configuration={}, environment_id="test-environment_id", description="test-description", option_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_configuration_template.assert_called_once()

def test_create_platform_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import create_platform_version
    mock_client = MagicMock()
    mock_client.create_platform_version.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    create_platform_version("test-platform_name", "test-platform_version", {}, environment_name="test-environment_name", option_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_platform_version.assert_called_once()

def test_delete_platform_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import delete_platform_version
    mock_client = MagicMock()
    mock_client.delete_platform_version.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    delete_platform_version(platform_arn="test-platform_arn", region_name="us-east-1")
    mock_client.delete_platform_version.assert_called_once()

def test_describe_configuration_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_configuration_options
    mock_client = MagicMock()
    mock_client.describe_configuration_options.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_configuration_options(application_name="test-application_name", template_name="test-template_name", environment_name="test-environment_name", solution_stack_name="test-solution_stack_name", platform_arn="test-platform_arn", options={}, region_name="us-east-1")
    mock_client.describe_configuration_options.assert_called_once()

def test_describe_configuration_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_configuration_settings
    mock_client = MagicMock()
    mock_client.describe_configuration_settings.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_configuration_settings("test-application_name", template_name="test-template_name", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.describe_configuration_settings.assert_called_once()

def test_describe_environment_health_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_environment_health
    mock_client = MagicMock()
    mock_client.describe_environment_health.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_environment_health(environment_name="test-environment_name", environment_id="test-environment_id", attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.describe_environment_health.assert_called_once()

def test_describe_environment_managed_action_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_environment_managed_action_history
    mock_client = MagicMock()
    mock_client.describe_environment_managed_action_history.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_environment_managed_action_history(environment_id="test-environment_id", environment_name="test-environment_name", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.describe_environment_managed_action_history.assert_called_once()

def test_describe_environment_managed_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_environment_managed_actions
    mock_client = MagicMock()
    mock_client.describe_environment_managed_actions.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_environment_managed_actions(environment_name="test-environment_name", environment_id="test-environment_id", status="test-status", region_name="us-east-1")
    mock_client.describe_environment_managed_actions.assert_called_once()

def test_describe_environment_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_environment_resources
    mock_client = MagicMock()
    mock_client.describe_environment_resources.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_environment_resources(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.describe_environment_resources.assert_called_once()

def test_describe_platform_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import describe_platform_version
    mock_client = MagicMock()
    mock_client.describe_platform_version.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    describe_platform_version(platform_arn="test-platform_arn", region_name="us-east-1")
    mock_client.describe_platform_version.assert_called_once()

def test_list_platform_branches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import list_platform_branches
    mock_client = MagicMock()
    mock_client.list_platform_branches.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    list_platform_branches(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_platform_branches.assert_called_once()

def test_list_platform_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import list_platform_versions
    mock_client = MagicMock()
    mock_client.list_platform_versions.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    list_platform_versions(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_platform_versions.assert_called_once()

def test_rebuild_environment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import rebuild_environment
    mock_client = MagicMock()
    mock_client.rebuild_environment.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    rebuild_environment(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.rebuild_environment.assert_called_once()

def test_request_environment_info_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import request_environment_info
    mock_client = MagicMock()
    mock_client.request_environment_info.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    request_environment_info("test-info_type", environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.request_environment_info.assert_called_once()

def test_restart_app_server_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import restart_app_server
    mock_client = MagicMock()
    mock_client.restart_app_server.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    restart_app_server(environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.restart_app_server.assert_called_once()

def test_retrieve_environment_info_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import retrieve_environment_info
    mock_client = MagicMock()
    mock_client.retrieve_environment_info.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    retrieve_environment_info("test-info_type", environment_id="test-environment_id", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.retrieve_environment_info.assert_called_once()

def test_swap_environment_cnames_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import swap_environment_cnames
    mock_client = MagicMock()
    mock_client.swap_environment_cnames.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    swap_environment_cnames(source_environment_id="test-source_environment_id", source_environment_name="test-source_environment_name", destination_environment_id="test-destination_environment_id", destination_environment_name="test-destination_environment_name", region_name="us-east-1")
    mock_client.swap_environment_cnames.assert_called_once()

def test_update_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import update_application
    mock_client = MagicMock()
    mock_client.update_application.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    update_application("test-application_name", description="test-description", region_name="us-east-1")
    mock_client.update_application.assert_called_once()

def test_update_application_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import update_application_version
    mock_client = MagicMock()
    mock_client.update_application_version.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    update_application_version("test-application_name", "test-version_label", description="test-description", region_name="us-east-1")
    mock_client.update_application_version.assert_called_once()

def test_update_configuration_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import update_configuration_template
    mock_client = MagicMock()
    mock_client.update_configuration_template.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    update_configuration_template("test-application_name", "test-template_name", description="test-description", option_settings={}, options_to_remove={}, region_name="us-east-1")
    mock_client.update_configuration_template.assert_called_once()

def test_update_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import update_tags_for_resource
    mock_client = MagicMock()
    mock_client.update_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    update_tags_for_resource("test-resource_arn", tags_to_add=[{"Key": "k", "Value": "v"}], tags_to_remove=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.update_tags_for_resource.assert_called_once()

def test_validate_configuration_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elastic_beanstalk import validate_configuration_settings
    mock_client = MagicMock()
    mock_client.validate_configuration_settings.return_value = {}
    monkeypatch.setattr("aws_util.elastic_beanstalk.get_client", lambda *a, **kw: mock_client)
    validate_configuration_settings("test-application_name", {}, template_name="test-template_name", environment_name="test-environment_name", region_name="us-east-1")
    mock_client.validate_configuration_settings.assert_called_once()
