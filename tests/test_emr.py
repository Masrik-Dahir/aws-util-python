"""Tests for aws_util.emr module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.emr as emr_mod
from aws_util.emr import (
    BootstrapActionResult,
    ClusterResult,
    InstanceGroupResult,
    SecurityConfigurationResult,
    StepResult,
    _READY_STATES,
    _TERMINAL_STATES,
    _parse_bootstrap_action,
    _parse_cluster,
    _parse_instance_group,
    _parse_security_configuration,
    _parse_step,
    add_instance_groups,
    add_job_flow_steps,
    create_security_configuration,
    describe_cluster,
    describe_step,
    list_bootstrap_actions,
    list_clusters,
    list_instance_groups,
    list_security_configurations,
    list_steps,
    modify_instance_groups,
    put_auto_scaling_policy,
    run_and_wait,
    run_job_flow,
    set_termination_protection,
    terminate_job_flows,
    wait_for_cluster,
    add_instance_fleet,
    add_tags,
    cancel_steps,
    create_persistent_app_ui,
    create_studio,
    create_studio_session_mapping,
    delete_security_configuration,
    delete_studio,
    delete_studio_session_mapping,
    describe_job_flows,
    describe_notebook_execution,
    describe_persistent_app_ui,
    describe_release_label,
    describe_security_configuration,
    describe_studio,
    get_auto_termination_policy,
    get_block_public_access_configuration,
    get_cluster_session_credentials,
    get_managed_scaling_policy,
    get_on_cluster_app_ui_presigned_url,
    get_persistent_app_ui_presigned_url,
    get_studio_session_mapping,
    list_instance_fleets,
    list_instances,
    list_notebook_executions,
    list_release_labels,
    list_studio_session_mappings,
    list_studios,
    list_supported_instance_types,
    modify_cluster,
    modify_instance_fleet,
    put_auto_termination_policy,
    put_block_public_access_configuration,
    put_managed_scaling_policy,
    remove_auto_scaling_policy,
    remove_auto_termination_policy,
    remove_managed_scaling_policy,
    remove_tags,
    set_keep_job_flow_alive_when_no_steps,
    set_unhealthy_node_replacement,
    set_visible_to_all_users,
    start_notebook_execution,
    stop_notebook_execution,
    update_studio,
    update_studio_session_mapping,
)

REGION = "us-east-1"
CLUSTER_ID = "j-ABCDEF12345"
CLUSTER_NAME = "test-emr-cluster"
STEP_ID = "s-STEP12345"
IG_ID = "ig-INSTANCE12345"

# ---------------------------------------------------------------------------
# Helpers — raw dicts matching AWS API shape
# ---------------------------------------------------------------------------


def _cluster_dict(**overrides: object) -> dict:
    d: dict = {
        "Id": CLUSTER_ID,
        "Name": CLUSTER_NAME,
        "Status": {"State": "WAITING", "StateChangeReason": {}},
        "NormalizedInstanceHours": 100,
        "LogUri": "s3://my-logs/emr/",
        "ReleaseLabel": "emr-6.15.0",
        "AutoTerminate": False,
        "TerminationProtected": True,
        "Tags": [{"Key": "env", "Value": "test"}],
    }
    d.update(overrides)
    return d


def _cluster_list_dict(**overrides: object) -> dict:
    """Cluster summary dict as returned by ListClusters."""
    d: dict = {
        "Id": CLUSTER_ID,
        "Name": CLUSTER_NAME,
        "Status": {"State": "WAITING", "StateChangeReason": {}},
        "NormalizedInstanceHours": 100,
    }
    d.update(overrides)
    return d


def _step_dict(**overrides: object) -> dict:
    d: dict = {
        "Id": STEP_ID,
        "Name": "MyStep",
        "Status": {"State": "COMPLETED"},
        "ActionOnFailure": "CONTINUE",
    }
    d.update(overrides)
    return d


def _instance_group_dict(**overrides: object) -> dict:
    d: dict = {
        "Id": IG_ID,
        "Name": "Core",
        "Market": "ON_DEMAND",
        "InstanceGroupType": "CORE",
        "InstanceType": "m5.xlarge",
        "RequestedInstanceCount": 2,
        "RunningInstanceCount": 2,
        "Status": {"State": "RUNNING"},
    }
    d.update(overrides)
    return d


def _security_config_dict(**overrides: object) -> dict:
    d: dict = {
        "Name": "my-sec-config",
        "CreationDateTime": "2024-01-01T00:00:00Z",
    }
    d.update(overrides)
    return d


def _bootstrap_action_dict(**overrides: object) -> dict:
    d: dict = {
        "Name": "MyBootstrap",
        "ScriptBootstrapAction": {
            "Path": "s3://my-bucket/bootstrap.sh",
            "Args": ["--opt1", "val1"],
        },
    }
    d.update(overrides)
    return d


def _client_error(code: str = "ValidationException", msg: str = "err") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "Operation"
    )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_cluster_result_model(self):
        c = ClusterResult(
            cluster_id="j-1", name="c1", status="WAITING"
        )
        assert c.cluster_id == "j-1"
        assert c.log_uri is None
        assert c.tags == []

    def test_step_result_model(self):
        s = StepResult(step_id="s-1", name="step", status="COMPLETED")
        assert s.action_on_failure is None
        assert s.extra == {}

    def test_instance_group_result_model(self):
        ig = InstanceGroupResult(
            instance_group_id="ig-1", name="Core",
            market="ON_DEMAND", instance_role="CORE",
            instance_type="m5.xlarge", status="RUNNING",
        )
        assert ig.requested_instance_count == 0
        assert ig.running_instance_count == 0

    def test_security_configuration_result_model(self):
        sc = SecurityConfigurationResult(name="sc1")
        assert sc.creation_date_time is None
        assert sc.extra == {}

    def test_bootstrap_action_result_model(self):
        ba = BootstrapActionResult(name="ba", script_path="s3://x")
        assert ba.args == []
        assert ba.extra == {}

    def test_models_are_frozen(self):
        c = ClusterResult(
            cluster_id="j-1", name="c1", status="WAITING"
        )
        with pytest.raises(Exception):
            c.name = "new"  # type: ignore[misc]

    def test_ready_and_terminal_states(self):
        assert "WAITING" in _READY_STATES
        assert "RUNNING" in _READY_STATES
        assert "TERMINATED" in _TERMINAL_STATES
        assert "TERMINATED_WITH_ERRORS" in _TERMINAL_STATES


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_cluster_full(self):
        result = _parse_cluster(_cluster_dict())
        assert result.cluster_id == CLUSTER_ID
        assert result.name == CLUSTER_NAME
        assert result.status == "WAITING"
        assert result.log_uri == "s3://my-logs/emr/"
        assert result.release_label == "emr-6.15.0"
        assert result.termination_protected is True
        assert result.normalized_instance_hours == 100
        assert result.tags == [{"Key": "env", "Value": "test"}]

    def test_parse_cluster_minimal(self):
        result = _parse_cluster({
            "Id": "j-min",
            "Name": "min",
            "Status": {"State": "STARTING"},
        })
        assert result.cluster_id == "j-min"
        assert result.log_uri is None
        assert result.release_label is None
        assert result.auto_terminate is False

    def test_parse_cluster_with_cluster_id_key(self):
        result = _parse_cluster({
            "ClusterId": "j-alt",
            "Name": "alt",
            "Status": {"State": "RUNNING"},
        })
        assert result.cluster_id == "j-alt"

    def test_parse_cluster_extra_fields(self):
        data = _cluster_dict()
        data["Ec2InstanceAttributes"] = {"AvailabilityZone": "us-east-1a"}
        result = _parse_cluster(data)
        assert result.extra["Ec2InstanceAttributes"] == {
            "AvailabilityZone": "us-east-1a"
        }

    def test_parse_step_full(self):
        result = _parse_step(_step_dict())
        assert result.step_id == STEP_ID
        assert result.name == "MyStep"
        assert result.status == "COMPLETED"
        assert result.action_on_failure == "CONTINUE"

    def test_parse_step_extra_fields(self):
        data = _step_dict()
        data["Config"] = {"Jar": "s3://my-jar.jar"}
        result = _parse_step(data)
        assert result.extra["Config"] == {"Jar": "s3://my-jar.jar"}

    def test_parse_instance_group_full(self):
        result = _parse_instance_group(_instance_group_dict())
        assert result.instance_group_id == IG_ID
        assert result.name == "Core"
        assert result.market == "ON_DEMAND"
        assert result.instance_role == "CORE"
        assert result.instance_type == "m5.xlarge"
        assert result.requested_instance_count == 2
        assert result.running_instance_count == 2
        assert result.status == "RUNNING"

    def test_parse_instance_group_extra_fields(self):
        data = _instance_group_dict()
        data["EbsBlockDevices"] = []
        result = _parse_instance_group(data)
        assert result.extra["EbsBlockDevices"] == []

    def test_parse_security_configuration_full(self):
        result = _parse_security_configuration(_security_config_dict())
        assert result.name == "my-sec-config"
        assert result.creation_date_time == "2024-01-01T00:00:00Z"

    def test_parse_security_configuration_no_date(self):
        result = _parse_security_configuration({"Name": "sc"})
        assert result.creation_date_time is None

    def test_parse_security_configuration_extra_fields(self):
        data = _security_config_dict()
        data["SecurityConfiguration"] = "{}"
        result = _parse_security_configuration(data)
        assert result.extra["SecurityConfiguration"] == "{}"

    def test_parse_bootstrap_action_full(self):
        result = _parse_bootstrap_action(_bootstrap_action_dict())
        assert result.name == "MyBootstrap"
        assert result.script_path == "s3://my-bucket/bootstrap.sh"
        assert result.args == ["--opt1", "val1"]

    def test_parse_bootstrap_action_minimal(self):
        result = _parse_bootstrap_action({"Name": "ba"})
        assert result.script_path == ""
        assert result.args == []

    def test_parse_bootstrap_action_extra_fields(self):
        data = _bootstrap_action_dict()
        data["ExtraField"] = "extra"
        result = _parse_bootstrap_action(data)
        assert result.extra["ExtraField"] == "extra"


# ---------------------------------------------------------------------------
# run_job_flow
# ---------------------------------------------------------------------------


class TestRunJobFlow:
    def test_run_job_flow_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.run_job_flow.return_value = {"JobFlowId": CLUSTER_ID}
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = run_job_flow("my-cluster", region_name=REGION)
        assert result == CLUSTER_ID

    def test_run_job_flow_all_options(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.run_job_flow.return_value = {"JobFlowId": CLUSTER_ID}
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = run_job_flow(
            "my-cluster",
            log_uri="s3://logs/",
            release_label="emr-6.15.0",
            instances={"KeepJobFlowAliveWhenNoSteps": True},
            steps=[{"Name": "step1"}],
            applications=[{"Name": "Spark"}],
            configurations=[{"Classification": "spark-defaults"}],
            service_role="EMR_DefaultRole",
            job_flow_role="EMR_EC2_DefaultRole",
            tags=[{"Key": "env", "Value": "test"}],
            visible_to_all_users=False,
            region_name=REGION,
        )
        assert result == CLUSTER_ID
        call_kwargs = mock_client.run_job_flow.call_args[1]
        assert call_kwargs["LogUri"] == "s3://logs/"
        assert call_kwargs["ReleaseLabel"] == "emr-6.15.0"
        assert call_kwargs["Applications"] == [{"Name": "Spark"}]
        assert call_kwargs["VisibleToAllUsers"] is False

    def test_run_job_flow_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.run_job_flow.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="run_job_flow failed"):
            run_job_flow("bad-cluster", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_cluster
# ---------------------------------------------------------------------------


class TestDescribeCluster:
    def test_describe_cluster_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict()
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_cluster(CLUSTER_ID, region_name=REGION)
        assert isinstance(result, ClusterResult)
        assert result.cluster_id == CLUSTER_ID

    def test_describe_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_cluster failed"):
            describe_cluster("missing", region_name=REGION)


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------


class TestListClusters:
    def test_list_clusters_no_filter(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Clusters": [_cluster_list_dict(), _cluster_list_dict(Id="j-2", Name="c2")]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_clusters(region_name=REGION)
        assert len(result) == 2

    def test_list_clusters_with_states(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Clusters": [_cluster_list_dict()]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_clusters(
            cluster_states=["WAITING"], region_name=REGION
        )
        assert len(result) == 1

    def test_list_clusters_empty(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"Clusters": []}]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_clusters(region_name=REGION)
        assert result == []

    def test_list_clusters_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_clusters failed"):
            list_clusters(region_name=REGION)


# ---------------------------------------------------------------------------
# terminate_job_flows
# ---------------------------------------------------------------------------


class TestTerminateJobFlows:
    def test_terminate_job_flows_success(self, monkeypatch):
        mock_client = MagicMock()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        terminate_job_flows([CLUSTER_ID], region_name=REGION)
        mock_client.terminate_job_flows.assert_called_once_with(
            JobFlowIds=[CLUSTER_ID]
        )

    def test_terminate_job_flows_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.terminate_job_flows.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="terminate_job_flows failed"):
            terminate_job_flows([CLUSTER_ID], region_name=REGION)


# ---------------------------------------------------------------------------
# add_job_flow_steps
# ---------------------------------------------------------------------------


class TestAddJobFlowSteps:
    def test_add_job_flow_steps_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_job_flow_steps.return_value = {
            "StepIds": ["s-1", "s-2"]
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = add_job_flow_steps(
            CLUSTER_ID,
            [{"Name": "step1"}, {"Name": "step2"}],
            region_name=REGION,
        )
        assert result == ["s-1", "s-2"]

    def test_add_job_flow_steps_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_job_flow_steps.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="add_job_flow_steps failed"):
            add_job_flow_steps(CLUSTER_ID, [{"Name": "s"}], region_name=REGION)


# ---------------------------------------------------------------------------
# list_steps
# ---------------------------------------------------------------------------


class TestListSteps:
    def test_list_steps_no_filter(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Steps": [_step_dict(), _step_dict(Id="s-2", Name="Step2")]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_steps(CLUSTER_ID, region_name=REGION)
        assert len(result) == 2

    def test_list_steps_with_states(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Steps": [_step_dict()]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_steps(
            CLUSTER_ID, step_states=["COMPLETED"], region_name=REGION
        )
        assert len(result) == 1

    def test_list_steps_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_steps failed"):
            list_steps(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_step
# ---------------------------------------------------------------------------


class TestDescribeStep:
    def test_describe_step_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_step.return_value = {"Step": _step_dict()}
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_step(CLUSTER_ID, STEP_ID, region_name=REGION)
        assert result.step_id == STEP_ID
        assert result.name == "MyStep"

    def test_describe_step_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_step.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_step failed"):
            describe_step(CLUSTER_ID, "missing", region_name=REGION)


# ---------------------------------------------------------------------------
# add_instance_groups
# ---------------------------------------------------------------------------


class TestAddInstanceGroups:
    def test_add_instance_groups_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_instance_groups.return_value = {
            "InstanceGroupIds": [IG_ID]
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = add_instance_groups(
            CLUSTER_ID,
            [{"InstanceGroupType": "TASK", "InstanceType": "m5.xlarge", "InstanceCount": 1}],
            region_name=REGION,
        )
        assert result == [IG_ID]

    def test_add_instance_groups_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_instance_groups.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="add_instance_groups failed"):
            add_instance_groups(CLUSTER_ID, [], region_name=REGION)


# ---------------------------------------------------------------------------
# list_instance_groups
# ---------------------------------------------------------------------------


class TestListInstanceGroups:
    def test_list_instance_groups_success(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"InstanceGroups": [_instance_group_dict()]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_instance_groups(CLUSTER_ID, region_name=REGION)
        assert len(result) == 1
        assert result[0].instance_group_id == IG_ID

    def test_list_instance_groups_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_instance_groups failed"):
            list_instance_groups(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# modify_instance_groups
# ---------------------------------------------------------------------------


class TestModifyInstanceGroups:
    def test_modify_instance_groups_success(self, monkeypatch):
        mock_client = MagicMock()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        modify_instance_groups(
            [{"InstanceGroupId": IG_ID, "InstanceCount": 4}],
            region_name=REGION,
        )
        mock_client.modify_instance_groups.assert_called_once()

    def test_modify_instance_groups_with_cluster_id(self, monkeypatch):
        mock_client = MagicMock()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        modify_instance_groups(
            [{"InstanceGroupId": IG_ID, "InstanceCount": 4}],
            cluster_id=CLUSTER_ID,
            region_name=REGION,
        )
        call_kwargs = mock_client.modify_instance_groups.call_args[1]
        assert call_kwargs["ClusterId"] == CLUSTER_ID

    def test_modify_instance_groups_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_instance_groups.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="modify_instance_groups failed"):
            modify_instance_groups([], region_name=REGION)


# ---------------------------------------------------------------------------
# create_security_configuration
# ---------------------------------------------------------------------------


class TestCreateSecurityConfiguration:
    def test_create_security_configuration_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_security_configuration.return_value = (
            _security_config_dict()
        )
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_security_configuration(
            "my-sec-config", '{"Encryption": {}}', region_name=REGION
        )
        assert isinstance(result, SecurityConfigurationResult)
        assert result.name == "my-sec-config"

    def test_create_security_configuration_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_security_configuration.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="create_security_configuration failed"
        ):
            create_security_configuration(
                "bad", "{}", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_security_configurations
# ---------------------------------------------------------------------------


class TestListSecurityConfigurations:
    def test_list_security_configurations_success(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"SecurityConfigurations": [_security_config_dict()]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_security_configurations(region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "my-sec-config"

    def test_list_security_configurations_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="list_security_configurations failed"
        ):
            list_security_configurations(region_name=REGION)


# ---------------------------------------------------------------------------
# set_termination_protection
# ---------------------------------------------------------------------------


class TestSetTerminationProtection:
    def test_set_termination_protection_success(self, monkeypatch):
        mock_client = MagicMock()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        set_termination_protection(
            [CLUSTER_ID], True, region_name=REGION
        )
        mock_client.set_termination_protection.assert_called_once_with(
            JobFlowIds=[CLUSTER_ID],
            TerminationProtected=True,
        )

    def test_set_termination_protection_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.set_termination_protection.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="set_termination_protection failed"
        ):
            set_termination_protection(
                [CLUSTER_ID], True, region_name=REGION
            )


# ---------------------------------------------------------------------------
# put_auto_scaling_policy
# ---------------------------------------------------------------------------


class TestPutAutoScalingPolicy:
    def test_put_auto_scaling_policy_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.put_auto_scaling_policy.return_value = {
            "ClusterId": CLUSTER_ID,
            "InstanceGroupId": IG_ID,
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = put_auto_scaling_policy(
            CLUSTER_ID,
            IG_ID,
            {"Constraints": {"MinCapacity": 1, "MaxCapacity": 10}},
            region_name=REGION,
        )
        assert result["ClusterId"] == CLUSTER_ID

    def test_put_auto_scaling_policy_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.put_auto_scaling_policy.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="put_auto_scaling_policy failed"
        ):
            put_auto_scaling_policy(
                CLUSTER_ID, IG_ID, {}, region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_bootstrap_actions
# ---------------------------------------------------------------------------


class TestListBootstrapActions:
    def test_list_bootstrap_actions_success(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"BootstrapActions": [_bootstrap_action_dict()]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_bootstrap_actions(CLUSTER_ID, region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "MyBootstrap"

    def test_list_bootstrap_actions_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="list_bootstrap_actions failed"
        ):
            list_bootstrap_actions(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


class TestWaitForCluster:
    def test_wait_for_cluster_immediate_waiting(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict()
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = wait_for_cluster(CLUSTER_ID, region_name=REGION)
        assert result.status == "WAITING"

    def test_wait_for_cluster_immediate_running(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict(
                Status={"State": "RUNNING", "StateChangeReason": {}}
            )
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = wait_for_cluster(CLUSTER_ID, region_name=REGION)
        assert result.status == "RUNNING"

    def test_wait_for_cluster_terminal_state(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict(
                Status={"State": "TERMINATED", "StateChangeReason": {}}
            )
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="terminal state"):
            wait_for_cluster(CLUSTER_ID, region_name=REGION)

    def test_wait_for_cluster_terminal_with_errors(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict(
                Status={
                    "State": "TERMINATED_WITH_ERRORS",
                    "StateChangeReason": {},
                }
            )
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="terminal state"):
            wait_for_cluster(CLUSTER_ID, region_name=REGION)

    def test_wait_for_cluster_timeout(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict(
                Status={"State": "STARTING", "StateChangeReason": {}}
            )
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        monkeypatch.setattr(emr_mod.time, "sleep", lambda _: None)
        with pytest.raises(TimeoutError, match="did not become ready"):
            wait_for_cluster(
                CLUSTER_ID,
                timeout=0.01,
                poll_interval=0.001,
                region_name=REGION,
            )

    def test_wait_for_cluster_transitions(self, monkeypatch):
        """Cluster transitions from STARTING -> BOOTSTRAPPING -> WAITING."""
        responses = [
            {"Cluster": _cluster_dict(
                Status={"State": "STARTING", "StateChangeReason": {}}
            )},
            {"Cluster": _cluster_dict(
                Status={"State": "BOOTSTRAPPING", "StateChangeReason": {}}
            )},
            {"Cluster": _cluster_dict(
                Status={"State": "WAITING", "StateChangeReason": {}}
            )},
        ]
        mock_client = MagicMock()
        mock_client.describe_cluster.side_effect = responses
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        monkeypatch.setattr(emr_mod.time, "sleep", lambda _: None)
        result = wait_for_cluster(
            CLUSTER_ID, timeout=60, poll_interval=0.001, region_name=REGION
        )
        assert result.status == "WAITING"


# ---------------------------------------------------------------------------
# run_and_wait
# ---------------------------------------------------------------------------


class TestRunAndWait:
    def test_run_and_wait_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.run_job_flow.return_value = {"JobFlowId": CLUSTER_ID}
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict()
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        result = run_and_wait(
            "my-cluster",
            log_uri="s3://logs/",
            release_label="emr-6.15.0",
            instances={"KeepJobFlowAliveWhenNoSteps": True},
            steps=[{"Name": "step1"}],
            applications=[{"Name": "Spark"}],
            configurations=[{"Classification": "spark-defaults"}],
            service_role="EMR_DefaultRole",
            job_flow_role="EMR_EC2_DefaultRole",
            tags=[{"Key": "env", "Value": "test"}],
            visible_to_all_users=True,
            timeout=60,
            poll_interval=1,
            region_name=REGION,
        )
        assert isinstance(result, ClusterResult)
        assert result.status == "WAITING"

    def test_run_and_wait_terminal_failure(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.run_job_flow.return_value = {"JobFlowId": CLUSTER_ID}
        mock_client.describe_cluster.return_value = {
            "Cluster": _cluster_dict(
                Status={"State": "TERMINATED_WITH_ERRORS", "StateChangeReason": {}}
            )
        }
        monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="terminal state"):
            run_and_wait("fail-cluster", region_name=REGION)


def test_add_instance_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_instance_fleet.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    add_instance_fleet("test-cluster_id", {}, region_name=REGION)
    mock_client.add_instance_fleet.assert_called_once()


def test_add_instance_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_instance_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_instance_fleet",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add instance fleet"):
        add_instance_fleet("test-cluster_id", {}, region_name=REGION)


def test_add_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    add_tags("test-resource_id", [], region_name=REGION)
    mock_client.add_tags.assert_called_once()


def test_add_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags"):
        add_tags("test-resource_id", [], region_name=REGION)


def test_cancel_steps(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_steps.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_steps("test-cluster_id", [], region_name=REGION)
    mock_client.cancel_steps.assert_called_once()


def test_cancel_steps_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_steps.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_steps",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel steps"):
        cancel_steps("test-cluster_id", [], region_name=REGION)


def test_create_persistent_app_ui(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_persistent_app_ui.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    create_persistent_app_ui("test-target_resource_arn", region_name=REGION)
    mock_client.create_persistent_app_ui.assert_called_once()


def test_create_persistent_app_ui_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_persistent_app_ui.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_persistent_app_ui",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create persistent app ui"):
        create_persistent_app_ui("test-target_resource_arn", region_name=REGION)


def test_create_studio(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_studio.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    create_studio("test-name", "test-auth_mode", "test-vpc_id", [], "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", region_name=REGION)
    mock_client.create_studio.assert_called_once()


def test_create_studio_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_studio.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_studio",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create studio"):
        create_studio("test-name", "test-auth_mode", "test-vpc_id", [], "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", region_name=REGION)


def test_create_studio_session_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_studio_session_mapping.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", region_name=REGION)
    mock_client.create_studio_session_mapping.assert_called_once()


def test_create_studio_session_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_studio_session_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_studio_session_mapping",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create studio session mapping"):
        create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", region_name=REGION)


def test_delete_security_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_configuration.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_security_configuration("test-name", region_name=REGION)
    mock_client.delete_security_configuration.assert_called_once()


def test_delete_security_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_security_configuration",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete security configuration"):
        delete_security_configuration("test-name", region_name=REGION)


def test_delete_studio(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_studio.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_studio("test-studio_id", region_name=REGION)
    mock_client.delete_studio.assert_called_once()


def test_delete_studio_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_studio.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_studio",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete studio"):
        delete_studio("test-studio_id", region_name=REGION)


def test_delete_studio_session_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_studio_session_mapping.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_studio_session_mapping("test-studio_id", "test-identity_type", region_name=REGION)
    mock_client.delete_studio_session_mapping.assert_called_once()


def test_delete_studio_session_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_studio_session_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_studio_session_mapping",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete studio session mapping"):
        delete_studio_session_mapping("test-studio_id", "test-identity_type", region_name=REGION)


def test_describe_job_flows(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_job_flows.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_job_flows(region_name=REGION)
    mock_client.describe_job_flows.assert_called_once()


def test_describe_job_flows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_job_flows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_job_flows",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe job flows"):
        describe_job_flows(region_name=REGION)


def test_describe_notebook_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_notebook_execution.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_notebook_execution("test-notebook_execution_id", region_name=REGION)
    mock_client.describe_notebook_execution.assert_called_once()


def test_describe_notebook_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_notebook_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_notebook_execution",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe notebook execution"):
        describe_notebook_execution("test-notebook_execution_id", region_name=REGION)


def test_describe_persistent_app_ui(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_persistent_app_ui.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_persistent_app_ui("test-persistent_app_ui_id", region_name=REGION)
    mock_client.describe_persistent_app_ui.assert_called_once()


def test_describe_persistent_app_ui_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_persistent_app_ui.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_persistent_app_ui",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe persistent app ui"):
        describe_persistent_app_ui("test-persistent_app_ui_id", region_name=REGION)


def test_describe_release_label(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_release_label.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_release_label(region_name=REGION)
    mock_client.describe_release_label.assert_called_once()


def test_describe_release_label_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_release_label.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_release_label",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe release label"):
        describe_release_label(region_name=REGION)


def test_describe_security_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_configuration.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_security_configuration("test-name", region_name=REGION)
    mock_client.describe_security_configuration.assert_called_once()


def test_describe_security_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_configuration",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security configuration"):
        describe_security_configuration("test-name", region_name=REGION)


def test_describe_studio(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_studio.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_studio("test-studio_id", region_name=REGION)
    mock_client.describe_studio.assert_called_once()


def test_describe_studio_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_studio.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_studio",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe studio"):
        describe_studio("test-studio_id", region_name=REGION)


def test_get_auto_termination_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auto_termination_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_auto_termination_policy("test-cluster_id", region_name=REGION)
    mock_client.get_auto_termination_policy.assert_called_once()


def test_get_auto_termination_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auto_termination_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_auto_termination_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get auto termination policy"):
        get_auto_termination_policy("test-cluster_id", region_name=REGION)


def test_get_block_public_access_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_block_public_access_configuration.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_block_public_access_configuration(region_name=REGION)
    mock_client.get_block_public_access_configuration.assert_called_once()


def test_get_block_public_access_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_block_public_access_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_block_public_access_configuration",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get block public access configuration"):
        get_block_public_access_configuration(region_name=REGION)


def test_get_cluster_session_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_session_credentials.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_cluster_session_credentials("test-cluster_id", region_name=REGION)
    mock_client.get_cluster_session_credentials.assert_called_once()


def test_get_cluster_session_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_session_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cluster_session_credentials",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cluster session credentials"):
        get_cluster_session_credentials("test-cluster_id", region_name=REGION)


def test_get_managed_scaling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_scaling_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_managed_scaling_policy("test-cluster_id", region_name=REGION)
    mock_client.get_managed_scaling_policy.assert_called_once()


def test_get_managed_scaling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_scaling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_managed_scaling_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get managed scaling policy"):
        get_managed_scaling_policy("test-cluster_id", region_name=REGION)


def test_get_on_cluster_app_ui_presigned_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_on_cluster_app_ui_presigned_url.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_on_cluster_app_ui_presigned_url("test-cluster_id", region_name=REGION)
    mock_client.get_on_cluster_app_ui_presigned_url.assert_called_once()


def test_get_on_cluster_app_ui_presigned_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_on_cluster_app_ui_presigned_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_on_cluster_app_ui_presigned_url",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get on cluster app ui presigned url"):
        get_on_cluster_app_ui_presigned_url("test-cluster_id", region_name=REGION)


def test_get_persistent_app_ui_presigned_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_persistent_app_ui_presigned_url.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", region_name=REGION)
    mock_client.get_persistent_app_ui_presigned_url.assert_called_once()


def test_get_persistent_app_ui_presigned_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_persistent_app_ui_presigned_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_persistent_app_ui_presigned_url",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get persistent app ui presigned url"):
        get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", region_name=REGION)


def test_get_studio_session_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_studio_session_mapping.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    get_studio_session_mapping("test-studio_id", "test-identity_type", region_name=REGION)
    mock_client.get_studio_session_mapping.assert_called_once()


def test_get_studio_session_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_studio_session_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_studio_session_mapping",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get studio session mapping"):
        get_studio_session_mapping("test-studio_id", "test-identity_type", region_name=REGION)


def test_list_instance_fleets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_fleets.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_instance_fleets("test-cluster_id", region_name=REGION)
    mock_client.list_instance_fleets.assert_called_once()


def test_list_instance_fleets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_fleets",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance fleets"):
        list_instance_fleets("test-cluster_id", region_name=REGION)


def test_list_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instances.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_instances("test-cluster_id", region_name=REGION)
    mock_client.list_instances.assert_called_once()


def test_list_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instances",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instances"):
        list_instances("test-cluster_id", region_name=REGION)


def test_list_notebook_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_executions.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_notebook_executions(region_name=REGION)
    mock_client.list_notebook_executions.assert_called_once()


def test_list_notebook_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_notebook_executions",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list notebook executions"):
        list_notebook_executions(region_name=REGION)


def test_list_release_labels(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_release_labels.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_release_labels(region_name=REGION)
    mock_client.list_release_labels.assert_called_once()


def test_list_release_labels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_release_labels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_release_labels",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list release labels"):
        list_release_labels(region_name=REGION)


def test_list_studio_session_mappings(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_studio_session_mappings.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_studio_session_mappings(region_name=REGION)
    mock_client.list_studio_session_mappings.assert_called_once()


def test_list_studio_session_mappings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_studio_session_mappings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_studio_session_mappings",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list studio session mappings"):
        list_studio_session_mappings(region_name=REGION)


def test_list_studios(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_studios.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_studios(region_name=REGION)
    mock_client.list_studios.assert_called_once()


def test_list_studios_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_studios.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_studios",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list studios"):
        list_studios(region_name=REGION)


def test_list_supported_instance_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_supported_instance_types.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    list_supported_instance_types("test-release_label", region_name=REGION)
    mock_client.list_supported_instance_types.assert_called_once()


def test_list_supported_instance_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_supported_instance_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_supported_instance_types",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list supported instance types"):
        list_supported_instance_types("test-release_label", region_name=REGION)


def test_modify_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    modify_cluster("test-cluster_id", region_name=REGION)
    mock_client.modify_cluster.assert_called_once()


def test_modify_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster"):
        modify_cluster("test-cluster_id", region_name=REGION)


def test_modify_instance_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_fleet.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    modify_instance_fleet("test-cluster_id", {}, region_name=REGION)
    mock_client.modify_instance_fleet.assert_called_once()


def test_modify_instance_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_fleet",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance fleet"):
        modify_instance_fleet("test-cluster_id", {}, region_name=REGION)


def test_put_auto_termination_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_auto_termination_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    put_auto_termination_policy("test-cluster_id", region_name=REGION)
    mock_client.put_auto_termination_policy.assert_called_once()


def test_put_auto_termination_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_auto_termination_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_auto_termination_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put auto termination policy"):
        put_auto_termination_policy("test-cluster_id", region_name=REGION)


def test_put_block_public_access_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_block_public_access_configuration.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    put_block_public_access_configuration({}, region_name=REGION)
    mock_client.put_block_public_access_configuration.assert_called_once()


def test_put_block_public_access_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_block_public_access_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_block_public_access_configuration",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put block public access configuration"):
        put_block_public_access_configuration({}, region_name=REGION)


def test_put_managed_scaling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_managed_scaling_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    put_managed_scaling_policy("test-cluster_id", {}, region_name=REGION)
    mock_client.put_managed_scaling_policy.assert_called_once()


def test_put_managed_scaling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_managed_scaling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_managed_scaling_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put managed scaling policy"):
        put_managed_scaling_policy("test-cluster_id", {}, region_name=REGION)


def test_remove_auto_scaling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_auto_scaling_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    remove_auto_scaling_policy("test-cluster_id", "test-instance_group_id", region_name=REGION)
    mock_client.remove_auto_scaling_policy.assert_called_once()


def test_remove_auto_scaling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_auto_scaling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_auto_scaling_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove auto scaling policy"):
        remove_auto_scaling_policy("test-cluster_id", "test-instance_group_id", region_name=REGION)


def test_remove_auto_termination_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_auto_termination_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    remove_auto_termination_policy("test-cluster_id", region_name=REGION)
    mock_client.remove_auto_termination_policy.assert_called_once()


def test_remove_auto_termination_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_auto_termination_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_auto_termination_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove auto termination policy"):
        remove_auto_termination_policy("test-cluster_id", region_name=REGION)


def test_remove_managed_scaling_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_managed_scaling_policy.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    remove_managed_scaling_policy("test-cluster_id", region_name=REGION)
    mock_client.remove_managed_scaling_policy.assert_called_once()


def test_remove_managed_scaling_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_managed_scaling_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_managed_scaling_policy",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove managed scaling policy"):
        remove_managed_scaling_policy("test-cluster_id", region_name=REGION)


def test_remove_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    remove_tags("test-resource_id", [], region_name=REGION)
    mock_client.remove_tags.assert_called_once()


def test_remove_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags"):
        remove_tags("test-resource_id", [], region_name=REGION)


def test_set_keep_job_flow_alive_when_no_steps(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_keep_job_flow_alive_when_no_steps.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    set_keep_job_flow_alive_when_no_steps([], True, region_name=REGION)
    mock_client.set_keep_job_flow_alive_when_no_steps.assert_called_once()


def test_set_keep_job_flow_alive_when_no_steps_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_keep_job_flow_alive_when_no_steps.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_keep_job_flow_alive_when_no_steps",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set keep job flow alive when no steps"):
        set_keep_job_flow_alive_when_no_steps([], True, region_name=REGION)


def test_set_unhealthy_node_replacement(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_unhealthy_node_replacement.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    set_unhealthy_node_replacement([], True, region_name=REGION)
    mock_client.set_unhealthy_node_replacement.assert_called_once()


def test_set_unhealthy_node_replacement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_unhealthy_node_replacement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_unhealthy_node_replacement",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set unhealthy node replacement"):
        set_unhealthy_node_replacement([], True, region_name=REGION)


def test_set_visible_to_all_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_visible_to_all_users.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    set_visible_to_all_users([], True, region_name=REGION)
    mock_client.set_visible_to_all_users.assert_called_once()


def test_set_visible_to_all_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_visible_to_all_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_visible_to_all_users",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set visible to all users"):
        set_visible_to_all_users([], True, region_name=REGION)


def test_start_notebook_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_notebook_execution.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    start_notebook_execution({}, "test-service_role", region_name=REGION)
    mock_client.start_notebook_execution.assert_called_once()


def test_start_notebook_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_notebook_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_notebook_execution",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start notebook execution"):
        start_notebook_execution({}, "test-service_role", region_name=REGION)


def test_stop_notebook_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_notebook_execution.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    stop_notebook_execution("test-notebook_execution_id", region_name=REGION)
    mock_client.stop_notebook_execution.assert_called_once()


def test_stop_notebook_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_notebook_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_notebook_execution",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop notebook execution"):
        stop_notebook_execution("test-notebook_execution_id", region_name=REGION)


def test_update_studio(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_studio.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    update_studio("test-studio_id", region_name=REGION)
    mock_client.update_studio.assert_called_once()


def test_update_studio_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_studio.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_studio",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update studio"):
        update_studio("test-studio_id", region_name=REGION)


def test_update_studio_session_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_studio_session_mapping.return_value = {}
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", region_name=REGION)
    mock_client.update_studio_session_mapping.assert_called_once()


def test_update_studio_session_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_studio_session_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_studio_session_mapping",
    )
    monkeypatch.setattr(emr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update studio session mapping"):
        update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", region_name=REGION)


def test_modify_instance_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import modify_instance_groups
    mock_client = MagicMock()
    mock_client.modify_instance_groups.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    modify_instance_groups("test-instance_groups", cluster_id="test-cluster_id", region_name="us-east-1")
    mock_client.modify_instance_groups.assert_called_once()

def test_cancel_steps_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import cancel_steps
    mock_client = MagicMock()
    mock_client.cancel_steps.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    cancel_steps("test-cluster_id", "test-step_ids", step_cancellation_option="test-step_cancellation_option", region_name="us-east-1")
    mock_client.cancel_steps.assert_called_once()

def test_create_persistent_app_ui_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import create_persistent_app_ui
    mock_client = MagicMock()
    mock_client.create_persistent_app_ui.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    create_persistent_app_ui("test-target_resource_arn", emr_containers_config={}, tags=[{"Key": "k", "Value": "v"}], x_referer="test-x_referer", profiler_type="test-profiler_type", region_name="us-east-1")
    mock_client.create_persistent_app_ui.assert_called_once()

def test_create_studio_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import create_studio
    mock_client = MagicMock()
    mock_client.create_studio.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    create_studio("test-name", "test-auth_mode", "test-vpc_id", "test-subnet_ids", "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", description="test-description", user_role="test-user_role", idp_auth_url="test-idp_auth_url", idp_relay_state_parameter_name="test-idp_relay_state_parameter_name", tags=[{"Key": "k", "Value": "v"}], trusted_identity_propagation_enabled="test-trusted_identity_propagation_enabled", idc_user_assignment="test-idc_user_assignment", idc_instance_arn="test-idc_instance_arn", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.create_studio.assert_called_once()

def test_create_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import create_studio_session_mapping
    mock_client = MagicMock()
    mock_client.create_studio_session_mapping.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.create_studio_session_mapping.assert_called_once()

def test_delete_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import delete_studio_session_mapping
    mock_client = MagicMock()
    mock_client.delete_studio_session_mapping.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    delete_studio_session_mapping("test-studio_id", "test-identity_type", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.delete_studio_session_mapping.assert_called_once()

def test_describe_job_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import describe_job_flows
    mock_client = MagicMock()
    mock_client.describe_job_flows.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    describe_job_flows(created_after="test-created_after", created_before="test-created_before", job_flow_ids="test-job_flow_ids", job_flow_states="test-job_flow_states", region_name="us-east-1")
    mock_client.describe_job_flows.assert_called_once()

def test_describe_release_label_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import describe_release_label
    mock_client = MagicMock()
    mock_client.describe_release_label.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    describe_release_label(release_label="test-release_label", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_release_label.assert_called_once()

def test_get_cluster_session_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import get_cluster_session_credentials
    mock_client = MagicMock()
    mock_client.get_cluster_session_credentials.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    get_cluster_session_credentials("test-cluster_id", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.get_cluster_session_credentials.assert_called_once()

def test_get_on_cluster_app_ui_presigned_url_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import get_on_cluster_app_ui_presigned_url
    mock_client = MagicMock()
    mock_client.get_on_cluster_app_ui_presigned_url.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    get_on_cluster_app_ui_presigned_url("test-cluster_id", on_cluster_app_ui_type="test-on_cluster_app_ui_type", application_id="test-application_id", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.get_on_cluster_app_ui_presigned_url.assert_called_once()

def test_get_persistent_app_ui_presigned_url_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import get_persistent_app_ui_presigned_url
    mock_client = MagicMock()
    mock_client.get_persistent_app_ui_presigned_url.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", persistent_app_ui_type="test-persistent_app_ui_type", application_id="test-application_id", auth_proxy_call="test-auth_proxy_call", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.get_persistent_app_ui_presigned_url.assert_called_once()

def test_get_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import get_studio_session_mapping
    mock_client = MagicMock()
    mock_client.get_studio_session_mapping.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    get_studio_session_mapping("test-studio_id", "test-identity_type", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.get_studio_session_mapping.assert_called_once()

def test_list_instance_fleets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_instance_fleets
    mock_client = MagicMock()
    mock_client.list_instance_fleets.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_instance_fleets("test-cluster_id", marker="test-marker", region_name="us-east-1")
    mock_client.list_instance_fleets.assert_called_once()

def test_list_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_instances
    mock_client = MagicMock()
    mock_client.list_instances.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_instances("test-cluster_id", instance_group_id="test-instance_group_id", instance_group_types="test-instance_group_types", instance_fleet_id="test-instance_fleet_id", instance_fleet_type="test-instance_fleet_type", instance_states="test-instance_states", marker="test-marker", region_name="us-east-1")
    mock_client.list_instances.assert_called_once()

def test_list_notebook_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_notebook_executions
    mock_client = MagicMock()
    mock_client.list_notebook_executions.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_notebook_executions(editor_id="test-editor_id", status="test-status", from_value="test-from_value", to="test-to", marker="test-marker", execution_engine_id="test-execution_engine_id", region_name="us-east-1")
    mock_client.list_notebook_executions.assert_called_once()

def test_list_release_labels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_release_labels
    mock_client = MagicMock()
    mock_client.list_release_labels.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_release_labels(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_release_labels.assert_called_once()

def test_list_studio_session_mappings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_studio_session_mappings
    mock_client = MagicMock()
    mock_client.list_studio_session_mappings.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_studio_session_mappings(studio_id="test-studio_id", identity_type="test-identity_type", marker="test-marker", region_name="us-east-1")
    mock_client.list_studio_session_mappings.assert_called_once()

def test_list_studios_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_studios
    mock_client = MagicMock()
    mock_client.list_studios.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_studios(marker="test-marker", region_name="us-east-1")
    mock_client.list_studios.assert_called_once()

def test_list_supported_instance_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import list_supported_instance_types
    mock_client = MagicMock()
    mock_client.list_supported_instance_types.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    list_supported_instance_types("test-release_label", marker="test-marker", region_name="us-east-1")
    mock_client.list_supported_instance_types.assert_called_once()

def test_modify_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import modify_cluster
    mock_client = MagicMock()
    mock_client.modify_cluster.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    modify_cluster("test-cluster_id", step_concurrency_level="test-step_concurrency_level", extended_support=1, region_name="us-east-1")
    mock_client.modify_cluster.assert_called_once()

def test_put_auto_termination_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import put_auto_termination_policy
    mock_client = MagicMock()
    mock_client.put_auto_termination_policy.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    put_auto_termination_policy("test-cluster_id", auto_termination_policy=True, region_name="us-east-1")
    mock_client.put_auto_termination_policy.assert_called_once()

def test_start_notebook_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import start_notebook_execution
    mock_client = MagicMock()
    mock_client.start_notebook_execution.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    start_notebook_execution("test-execution_engine", "test-service_role", editor_id="test-editor_id", relative_path="test-relative_path", notebook_execution_name="test-notebook_execution_name", notebook_params="test-notebook_params", notebook_instance_security_group_id="test-notebook_instance_security_group_id", tags=[{"Key": "k", "Value": "v"}], notebook_s3_location="test-notebook_s3_location", output_notebook_s3_location="test-output_notebook_s3_location", output_notebook_format="test-output_notebook_format", environment_variables="test-environment_variables", region_name="us-east-1")
    mock_client.start_notebook_execution.assert_called_once()

def test_update_studio_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import update_studio
    mock_client = MagicMock()
    mock_client.update_studio.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    update_studio("test-studio_id", name="test-name", description="test-description", subnet_ids="test-subnet_ids", default_s3_location="test-default_s3_location", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.update_studio.assert_called_once()

def test_update_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr import update_studio_session_mapping
    mock_client = MagicMock()
    mock_client.update_studio_session_mapping.return_value = {}
    monkeypatch.setattr("aws_util.emr.get_client", lambda *a, **kw: mock_client)
    update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.update_studio_session_mapping.assert_called_once()
