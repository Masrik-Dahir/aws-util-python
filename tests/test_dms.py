"""Unit tests for aws_util.dms."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.dms as _dms
from aws_util.dms import (
    ConnectionResult,
    EndpointResult,
    ReplicationInstanceResult,
    ReplicationSubnetGroupResult,
    ReplicationTaskResult,
    TableStatistic,
    create_endpoint,
    create_replication_instance,
    create_replication_subnet_group,
    create_replication_task,
    delete_endpoint,
    delete_replication_instance,
    delete_replication_task,
    describe_connections,
    describe_endpoints,
    describe_replication_instances,
    describe_replication_tasks,
    describe_table_statistics,
    modify_endpoint,
    modify_replication_instance,
    start_replication_task,
    stop_replication_task,
    wait_for_replication_instance,
    wait_for_replication_task,
    add_tags_to_resource,
    apply_pending_maintenance_action,
    batch_start_recommendations,
    cancel_metadata_model_conversion,
    cancel_metadata_model_creation,
    cancel_replication_task_assessment_run,
    create_data_migration,
    create_data_provider,
    create_event_subscription,
    create_fleet_advisor_collector,
    create_instance_profile,
    create_migration_project,
    create_replication_config,
    delete_certificate,
    delete_connection,
    delete_data_migration,
    delete_data_provider,
    delete_event_subscription,
    delete_fleet_advisor_collector,
    delete_fleet_advisor_databases,
    delete_instance_profile,
    delete_migration_project,
    delete_replication_config,
    delete_replication_subnet_group,
    delete_replication_task_assessment_run,
    describe_account_attributes,
    describe_applicable_individual_assessments,
    describe_certificates,
    describe_conversion_configuration,
    describe_data_migrations,
    describe_data_providers,
    describe_endpoint_settings,
    describe_endpoint_types,
    describe_engine_versions,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_extension_pack_associations,
    describe_fleet_advisor_collectors,
    describe_fleet_advisor_databases,
    describe_fleet_advisor_lsa_analysis,
    describe_fleet_advisor_schema_object_summary,
    describe_fleet_advisor_schemas,
    describe_instance_profiles,
    describe_metadata_model,
    describe_metadata_model_assessments,
    describe_metadata_model_children,
    describe_metadata_model_conversions,
    describe_metadata_model_creations,
    describe_metadata_model_exports_as_script,
    describe_metadata_model_exports_to_target,
    describe_metadata_model_imports,
    describe_migration_projects,
    describe_orderable_replication_instances,
    describe_pending_maintenance_actions,
    describe_recommendation_limitations,
    describe_recommendations,
    describe_refresh_schemas_status,
    describe_replication_configs,
    describe_replication_instance_task_logs,
    describe_replication_subnet_groups,
    describe_replication_table_statistics,
    describe_replication_task_assessment_results,
    describe_replication_task_assessment_runs,
    describe_replication_task_individual_assessments,
    describe_replications,
    describe_schemas,
    export_metadata_model_assessment,
    get_target_selection_rules,
    import_certificate,
    list_tags_for_resource,
    modify_conversion_configuration,
    modify_data_migration,
    modify_data_provider,
    modify_event_subscription,
    modify_instance_profile,
    modify_migration_project,
    modify_replication_config,
    modify_replication_subnet_group,
    modify_replication_task,
    move_replication_task,
    reboot_replication_instance,
    refresh_schemas,
    reload_replication_tables,
    reload_tables,
    remove_tags_from_resource,
    run_connection,
    run_fleet_advisor_lsa_analysis,
    start_data_migration,
    start_extension_pack_association,
    start_metadata_model_assessment,
    start_metadata_model_conversion,
    start_metadata_model_creation,
    start_metadata_model_export_as_script,
    start_metadata_model_export_to_target,
    start_metadata_model_import,
    start_recommendations,
    start_replication,
    start_replication_task_assessment,
    start_replication_task_assessment_run,
    stop_data_migration,
    stop_replication,
    update_subscriptions_to_event_bridge,
)

# Alias to avoid pytest collecting it as a test function
dms_test_connection = _dms.test_connection
from aws_util.exceptions import AwsTimeoutError


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "op"
    )


# ---------------------------------------------------------------------------
# Replication instances
# ---------------------------------------------------------------------------


@patch("aws_util.dms.get_client")
class TestCreateReplicationInstance:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_instance.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
                "ReplicationInstanceClass": "dms.t3.medium",
                "ReplicationInstanceStatus": "creating",
            }
        }
        result = create_replication_instance(
            "ri-1", "dms.t3.medium"
        )
        assert result.replication_instance_identifier == "ri-1"
        assert result.replication_instance_status == "creating"

    def test_with_options(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_instance.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-2",
                "ReplicationInstanceArn": "arn:ri-2",
                "AllocatedStorage": 100,
                "MultiAZ": True,
            }
        }
        result = create_replication_instance(
            "ri-2",
            "dms.r5.large",
            allocated_storage=100,
            availability_zone="us-east-1a",
            multi_az=True,
            publicly_accessible=True,
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert result.replication_instance_arn == "arn:ri-2"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_instance.side_effect = (
            _client_error("AccessDeniedException")
        )
        with pytest.raises(Exception):
            create_replication_instance("ri-1", "dms.t3.medium")


@patch("aws_util.dms.get_client")
class TestDescribeReplicationInstances:
    def test_empty(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {"ReplicationInstances": []}
        ]
        assert describe_replication_instances() == []

    def test_with_items(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {
                "ReplicationInstances": [
                    {
                        "ReplicationInstanceIdentifier": "ri-1",
                        "ReplicationInstanceArn": "arn:ri-1",
                        "ReplicationInstanceStatus": "available",
                    }
                ]
            }
        ]
        result = describe_replication_instances()
        assert len(result) == 1
        assert result[0].replication_instance_status == "available"

    def test_with_filters(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {"ReplicationInstances": []}
        ]
        describe_replication_instances(
            filters=[{"Name": "status", "Values": ["available"]}]
        )
        pag.paginate.assert_called_once()

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.side_effect = _client_error("InternalError")
        with pytest.raises(Exception):
            describe_replication_instances()


@patch("aws_util.dms.get_client")
class TestModifyReplicationInstance:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.modify_replication_instance.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
                "ReplicationInstanceClass": "dms.r5.large",
            }
        }
        result = modify_replication_instance(
            "arn:ri-1",
            replication_instance_class="dms.r5.large",
            allocated_storage=200,
            multi_az=True,
        )
        assert isinstance(result, ReplicationInstanceResult)

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.modify_replication_instance.side_effect = (
            _client_error("ResourceNotFoundFault")
        )
        with pytest.raises(Exception):
            modify_replication_instance("arn:ri-missing")


@patch("aws_util.dms.get_client")
class TestDeleteReplicationInstance:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_replication_instance.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
                "ReplicationInstanceStatus": "deleting",
            }
        }
        result = delete_replication_instance("arn:ri-1")
        assert result.replication_instance_status == "deleting"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_replication_instance.side_effect = (
            _client_error("ResourceNotFoundFault")
        )
        with pytest.raises(Exception):
            delete_replication_instance("arn:ri-missing")


@patch("aws_util.dms.describe_replication_instances")
class TestWaitForReplicationInstance:
    def test_immediate(self, mock_desc: MagicMock) -> None:
        mock_desc.return_value = [
            ReplicationInstanceResult(
                replication_instance_identifier="ri-1",
                replication_instance_arn="arn:ri-1",
                replication_instance_status="available",
            )
        ]
        result = wait_for_replication_instance("arn:ri-1")
        assert result.replication_instance_status == "available"

    @patch("aws_util.dms._time")
    def test_timeout(
        self, mock_time: MagicMock, mock_desc: MagicMock
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_time.sleep = MagicMock()
        mock_desc.return_value = [
            ReplicationInstanceResult(
                replication_instance_identifier="ri-1",
                replication_instance_arn="arn:ri-1",
                replication_instance_status="creating",
            )
        ]
        with pytest.raises(AwsTimeoutError):
            wait_for_replication_instance(
                "arn:ri-1", timeout=5
            )

    @patch("aws_util.dms._time")
    def test_not_found(
        self, mock_time: MagicMock, mock_desc: MagicMock
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_time.sleep = MagicMock()
        mock_desc.return_value = []
        with pytest.raises(AwsTimeoutError):
            wait_for_replication_instance(
                "arn:ri-missing", timeout=5
            )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@patch("aws_util.dms.get_client")
class TestCreateEndpoint:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_endpoint.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
                "EndpointType": "source",
                "EngineName": "mysql",
            }
        }
        result = create_endpoint(
            "ep-1", "source", "mysql"
        )
        assert result.endpoint_identifier == "ep-1"

    def test_with_options(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_endpoint.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-2",
                "EndpointArn": "arn:ep-2",
                "EndpointType": "target",
                "EngineName": "postgres",
                "ServerName": "db.example.com",
                "Port": 5432,
            }
        }
        result = create_endpoint(
            "ep-2",
            "target",
            "postgres",
            server_name="db.example.com",
            port=5432,
            database_name="mydb",
            username="admin",
            password="secret",
            ssl_mode="require",
            tags=[{"Key": "env", "Value": "prod"}],
            extra_connection_attributes="key=value",
        )
        assert result.endpoint_arn == "arn:ep-2"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_endpoint.side_effect = _client_error(
            "AccessDeniedException"
        )
        with pytest.raises(Exception):
            create_endpoint("ep-1", "source", "mysql")


@patch("aws_util.dms.get_client")
class TestDescribeEndpoints:
    def test_empty(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [{"Endpoints": []}]
        assert describe_endpoints() == []

    def test_with_items(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {
                "Endpoints": [
                    {
                        "EndpointIdentifier": "ep-1",
                        "EndpointArn": "arn:ep-1",
                        "Status": "active",
                    }
                ]
            }
        ]
        result = describe_endpoints()
        assert len(result) == 1

    def test_with_filters(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [{"Endpoints": []}]
        describe_endpoints(
            filters=[{"Name": "type", "Values": ["source"]}]
        )
        pag.paginate.assert_called_once()

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.side_effect = _client_error("InternalError")
        with pytest.raises(Exception):
            describe_endpoints()


@patch("aws_util.dms.get_client")
class TestModifyEndpoint:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.modify_endpoint.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
            }
        }
        result = modify_endpoint(
            "arn:ep-1",
            endpoint_identifier="ep-1-new",
            engine_name="postgres",
            server_name="new-db.example.com",
            port=5433,
            database_name="newdb",
            username="newuser",
            password="newpass",
            ssl_mode="verify-full",
        )
        assert isinstance(result, EndpointResult)

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.modify_endpoint.side_effect = _client_error(
            "ResourceNotFoundFault"
        )
        with pytest.raises(Exception):
            modify_endpoint("arn:ep-missing")


@patch("aws_util.dms.get_client")
class TestDeleteEndpoint:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_endpoint.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
                "Status": "deleting",
            }
        }
        result = delete_endpoint("arn:ep-1")
        assert result.status == "deleting"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_endpoint.side_effect = _client_error(
            "ResourceNotFoundFault"
        )
        with pytest.raises(Exception):
            delete_endpoint("arn:ep-missing")


@patch("aws_util.dms.get_client")
class TestTestConnection:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.test_connection.return_value = {
            "Connection": {
                "ReplicationInstanceArn": "arn:ri-1",
                "EndpointArn": "arn:ep-1",
                "Status": "testing",
            }
        }
        result = dms_test_connection("arn:ri-1", "arn:ep-1")
        assert result.status == "testing"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.test_connection.side_effect = _client_error(
            "ResourceNotFoundFault"
        )
        with pytest.raises(Exception):
            dms_test_connection("arn:ri-1", "arn:ep-1")


@patch("aws_util.dms.get_client")
class TestDescribeConnections:
    def test_empty(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [{"Connections": []}]
        assert describe_connections() == []

    def test_with_items(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {
                "Connections": [
                    {
                        "ReplicationInstanceArn": "arn:ri-1",
                        "EndpointArn": "arn:ep-1",
                        "Status": "successful",
                    }
                ]
            }
        ]
        result = describe_connections()
        assert len(result) == 1
        assert result[0].status == "successful"

    def test_with_filters(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [{"Connections": []}]
        describe_connections(
            filters=[{"Name": "status", "Values": ["successful"]}]
        )
        pag.paginate.assert_called_once()

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.side_effect = _client_error("InternalError")
        with pytest.raises(Exception):
            describe_connections()


# ---------------------------------------------------------------------------
# Replication tasks
# ---------------------------------------------------------------------------


@patch("aws_util.dms.get_client")
class TestCreateReplicationTask:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_task.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "creating",
            }
        }
        result = create_replication_task(
            "task-1",
            "arn:src",
            "arn:tgt",
            "arn:ri-1",
            "full-load",
            '{"rules": []}',
        )
        assert result.replication_task_identifier == "task-1"

    def test_with_tags(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_task.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-2",
                "ReplicationTaskArn": "arn:task-2",
            }
        }
        result = create_replication_task(
            "task-2",
            "arn:src",
            "arn:tgt",
            "arn:ri-1",
            "cdc",
            '{"rules": []}',
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert result.replication_task_arn == "arn:task-2"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_task.side_effect = (
            _client_error("AccessDeniedException")
        )
        with pytest.raises(Exception):
            create_replication_task(
                "task-1",
                "arn:src",
                "arn:tgt",
                "arn:ri-1",
                "full-load",
                '{"rules": []}',
            )


@patch("aws_util.dms.get_client")
class TestDescribeReplicationTasks:
    def test_empty(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {"ReplicationTasks": []}
        ]
        assert describe_replication_tasks() == []

    def test_with_items(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {
                "ReplicationTasks": [
                    {
                        "ReplicationTaskIdentifier": "task-1",
                        "ReplicationTaskArn": "arn:task-1",
                        "Status": "running",
                        "ReplicationTaskStartDate": "2024-01-01",
                    }
                ]
            }
        ]
        result = describe_replication_tasks()
        assert len(result) == 1
        assert result[0].status == "running"

    def test_with_filters(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {"ReplicationTasks": []}
        ]
        describe_replication_tasks(
            filters=[{"Name": "status", "Values": ["running"]}]
        )
        pag.paginate.assert_called_once()

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.side_effect = _client_error("InternalError")
        with pytest.raises(Exception):
            describe_replication_tasks()


@patch("aws_util.dms.get_client")
class TestStartReplicationTask:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.start_replication_task.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "starting",
            }
        }
        result = start_replication_task("arn:task-1")
        assert result.status == "starting"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.start_replication_task.side_effect = (
            _client_error("ResourceNotFoundFault")
        )
        with pytest.raises(Exception):
            start_replication_task("arn:task-missing")


@patch("aws_util.dms.get_client")
class TestStopReplicationTask:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.stop_replication_task.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "stopping",
            }
        }
        result = stop_replication_task("arn:task-1")
        assert result.status == "stopping"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.stop_replication_task.side_effect = (
            _client_error("ResourceNotFoundFault")
        )
        with pytest.raises(Exception):
            stop_replication_task("arn:task-missing")


@patch("aws_util.dms.get_client")
class TestDeleteReplicationTask:
    def test_success(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_replication_task.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "deleting",
            }
        }
        result = delete_replication_task("arn:task-1")
        assert result.status == "deleting"

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.delete_replication_task.side_effect = (
            _client_error("ResourceNotFoundFault")
        )
        with pytest.raises(Exception):
            delete_replication_task("arn:task-missing")


@patch("aws_util.dms.describe_replication_tasks")
class TestWaitForReplicationTask:
    def test_immediate(self, mock_desc: MagicMock) -> None:
        mock_desc.return_value = [
            ReplicationTaskResult(
                replication_task_identifier="task-1",
                replication_task_arn="arn:task-1",
                status="running",
            )
        ]
        result = wait_for_replication_task("arn:task-1")
        assert result.status == "running"

    @patch("aws_util.dms._time")
    def test_timeout(
        self, mock_time: MagicMock, mock_desc: MagicMock
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_time.sleep = MagicMock()
        mock_desc.return_value = [
            ReplicationTaskResult(
                replication_task_identifier="task-1",
                replication_task_arn="arn:task-1",
                status="starting",
            )
        ]
        with pytest.raises(AwsTimeoutError):
            wait_for_replication_task(
                "arn:task-1", timeout=5
            )

    @patch("aws_util.dms._time")
    def test_not_found(
        self, mock_time: MagicMock, mock_desc: MagicMock
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_time.sleep = MagicMock()
        mock_desc.return_value = []
        with pytest.raises(AwsTimeoutError):
            wait_for_replication_task(
                "arn:task-missing", timeout=5
            )


@patch("aws_util.dms.get_client")
class TestDescribeTableStatistics:
    def test_empty(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {"TableStatistics": []}
        ]
        assert describe_table_statistics("arn:task-1") == []

    def test_with_items(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.return_value = [
            {
                "TableStatistics": [
                    {
                        "SchemaName": "public",
                        "TableName": "users",
                        "Inserts": 100,
                        "Deletes": 5,
                        "Updates": 50,
                        "FullLoadRows": 1000,
                        "TableState": "Table completed",
                    }
                ]
            }
        ]
        result = describe_table_statistics("arn:task-1")
        assert len(result) == 1
        assert result[0].table_name == "users"
        assert result[0].inserts == 100

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        pag = MagicMock()
        client.get_paginator.return_value = pag
        pag.paginate.side_effect = _client_error(
            "ResourceNotFoundFault"
        )
        with pytest.raises(Exception):
            describe_table_statistics("arn:task-missing")


# ---------------------------------------------------------------------------
# Subnet groups
# ---------------------------------------------------------------------------


@patch("aws_util.dms.get_client")
class TestCreateReplicationSubnetGroup:
    def test_basic(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_subnet_group.return_value = {
            "ReplicationSubnetGroup": {
                "ReplicationSubnetGroupIdentifier": "sg-1",
                "ReplicationSubnetGroupDescription": "test",
                "VpcId": "vpc-123",
                "SubnetGroupStatus": "Complete",
            }
        }
        result = create_replication_subnet_group(
            "sg-1", "test", ["subnet-1", "subnet-2"]
        )
        assert result.replication_subnet_group_identifier == "sg-1"
        assert result.vpc_id == "vpc-123"

    def test_with_tags(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_subnet_group.return_value = {
            "ReplicationSubnetGroup": {
                "ReplicationSubnetGroupIdentifier": "sg-2",
                "ReplicationSubnetGroupDescription": "prod",
            }
        }
        result = create_replication_subnet_group(
            "sg-2",
            "prod",
            ["subnet-1"],
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert isinstance(result, ReplicationSubnetGroupResult)

    def test_error(self, gc: MagicMock) -> None:
        client = MagicMock()
        gc.return_value = client
        client.create_replication_subnet_group.side_effect = (
            _client_error("AccessDeniedException")
        )
        with pytest.raises(Exception):
            create_replication_subnet_group(
                "sg-1", "test", ["subnet-1"]
            )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_replication_instance_result(self) -> None:
        r = ReplicationInstanceResult(
            replication_instance_identifier="ri-1",
            replication_instance_arn="arn:ri-1",
        )
        assert r.replication_instance_identifier == "ri-1"
        assert r.replication_instance_status is None

    def test_endpoint_result(self) -> None:
        r = EndpointResult(
            endpoint_identifier="ep-1",
            endpoint_arn="arn:ep-1",
        )
        assert r.endpoint_identifier == "ep-1"
        assert r.status is None

    def test_replication_task_result(self) -> None:
        r = ReplicationTaskResult(
            replication_task_identifier="task-1",
            replication_task_arn="arn:task-1",
        )
        assert r.replication_task_identifier == "task-1"
        assert r.status is None

    def test_connection_result(self) -> None:
        r = ConnectionResult(
            replication_instance_arn="arn:ri-1",
            endpoint_arn="arn:ep-1",
        )
        assert r.status is None

    def test_table_statistic(self) -> None:
        r = TableStatistic()
        assert r.inserts == 0
        assert r.schema_name is None

    def test_subnet_group_result(self) -> None:
        r = ReplicationSubnetGroupResult(
            replication_subnet_group_identifier="sg-1",
        )
        assert r.vpc_id is None


REGION = "us-east-1"


@patch("aws_util.dms.get_client")
def test_add_tags_to_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.return_value = {}
    add_tags_to_resource("test-resource_arn", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


@patch("aws_util.dms.get_client")
def test_add_tags_to_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_apply_pending_maintenance_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.return_value = {}
    apply_pending_maintenance_action("test-replication_instance_arn", "test-apply_action", "test-opt_in_type", region_name=REGION)
    mock_client.apply_pending_maintenance_action.assert_called_once()


@patch("aws_util.dms.get_client")
def test_apply_pending_maintenance_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_pending_maintenance_action",
    )
    with pytest.raises(RuntimeError, match="Failed to apply pending maintenance action"):
        apply_pending_maintenance_action("test-replication_instance_arn", "test-apply_action", "test-opt_in_type", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_batch_start_recommendations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_start_recommendations.return_value = {}
    batch_start_recommendations(region_name=REGION)
    mock_client.batch_start_recommendations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_batch_start_recommendations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_start_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_start_recommendations",
    )
    with pytest.raises(RuntimeError, match="Failed to batch start recommendations"):
        batch_start_recommendations(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_cancel_metadata_model_conversion(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_metadata_model_conversion.return_value = {}
    cancel_metadata_model_conversion("test-migration_project_identifier", "test-request_identifier", region_name=REGION)
    mock_client.cancel_metadata_model_conversion.assert_called_once()


@patch("aws_util.dms.get_client")
def test_cancel_metadata_model_conversion_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_metadata_model_conversion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_metadata_model_conversion",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel metadata model conversion"):
        cancel_metadata_model_conversion("test-migration_project_identifier", "test-request_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_cancel_metadata_model_creation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_metadata_model_creation.return_value = {}
    cancel_metadata_model_creation("test-migration_project_identifier", "test-request_identifier", region_name=REGION)
    mock_client.cancel_metadata_model_creation.assert_called_once()


@patch("aws_util.dms.get_client")
def test_cancel_metadata_model_creation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_metadata_model_creation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_metadata_model_creation",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel metadata model creation"):
        cancel_metadata_model_creation("test-migration_project_identifier", "test-request_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_cancel_replication_task_assessment_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_replication_task_assessment_run.return_value = {}
    cancel_replication_task_assessment_run("test-replication_task_assessment_run_arn", region_name=REGION)
    mock_client.cancel_replication_task_assessment_run.assert_called_once()


@patch("aws_util.dms.get_client")
def test_cancel_replication_task_assessment_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_replication_task_assessment_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_replication_task_assessment_run",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel replication task assessment run"):
        cancel_replication_task_assessment_run("test-replication_task_assessment_run_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_data_migration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_data_migration.return_value = {}
    create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", region_name=REGION)
    mock_client.create_data_migration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_data_migration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_data_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_migration",
    )
    with pytest.raises(RuntimeError, match="Failed to create data migration"):
        create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_data_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_data_provider.return_value = {}
    create_data_provider("test-engine", {}, region_name=REGION)
    mock_client.create_data_provider.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_data_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_data_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to create data provider"):
        create_data_provider("test-engine", {}, region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.return_value = {}
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)
    mock_client.create_event_subscription.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to create event subscription"):
        create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_fleet_advisor_collector(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet_advisor_collector.return_value = {}
    create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", region_name=REGION)
    mock_client.create_fleet_advisor_collector.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_fleet_advisor_collector_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet_advisor_collector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_fleet_advisor_collector",
    )
    with pytest.raises(RuntimeError, match="Failed to create fleet advisor collector"):
        create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_instance_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_instance_profile.return_value = {}
    create_instance_profile(region_name=REGION)
    mock_client.create_instance_profile.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_instance_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to create instance profile"):
        create_instance_profile(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_migration_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_migration_project.return_value = {}
    create_migration_project([], [], "test-instance_profile_identifier", region_name=REGION)
    mock_client.create_migration_project.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_migration_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_migration_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_migration_project",
    )
    with pytest.raises(RuntimeError, match="Failed to create migration project"):
        create_migration_project([], [], "test-instance_profile_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_create_replication_config(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_replication_config.return_value = {}
    create_replication_config("test-replication_config_identifier", "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", "test-table_mappings", region_name=REGION)
    mock_client.create_replication_config.assert_called_once()


@patch("aws_util.dms.get_client")
def test_create_replication_config_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_replication_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_replication_config",
    )
    with pytest.raises(RuntimeError, match="Failed to create replication config"):
        create_replication_config("test-replication_config_identifier", "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", "test-table_mappings", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.return_value = {}
    delete_certificate("test-certificate_arn", region_name=REGION)
    mock_client.delete_certificate.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to delete certificate"):
        delete_certificate("test-certificate_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_connection(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_connection.return_value = {}
    delete_connection("test-endpoint_arn", "test-replication_instance_arn", region_name=REGION)
    mock_client.delete_connection.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_connection_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection",
    )
    with pytest.raises(RuntimeError, match="Failed to delete connection"):
        delete_connection("test-endpoint_arn", "test-replication_instance_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_data_migration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_data_migration.return_value = {}
    delete_data_migration("test-data_migration_identifier", region_name=REGION)
    mock_client.delete_data_migration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_data_migration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_data_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_migration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete data migration"):
        delete_data_migration("test-data_migration_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_data_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_data_provider.return_value = {}
    delete_data_provider("test-data_provider_identifier", region_name=REGION)
    mock_client.delete_data_provider.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_data_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_data_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to delete data provider"):
        delete_data_provider("test-data_provider_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.return_value = {}
    delete_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.delete_event_subscription.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to delete event subscription"):
        delete_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_fleet_advisor_collector(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_advisor_collector.return_value = {}
    delete_fleet_advisor_collector("test-collector_referenced_id", region_name=REGION)
    mock_client.delete_fleet_advisor_collector.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_fleet_advisor_collector_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_advisor_collector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fleet_advisor_collector",
    )
    with pytest.raises(RuntimeError, match="Failed to delete fleet advisor collector"):
        delete_fleet_advisor_collector("test-collector_referenced_id", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_fleet_advisor_databases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_advisor_databases.return_value = {}
    delete_fleet_advisor_databases([], region_name=REGION)
    mock_client.delete_fleet_advisor_databases.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_fleet_advisor_databases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_advisor_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fleet_advisor_databases",
    )
    with pytest.raises(RuntimeError, match="Failed to delete fleet advisor databases"):
        delete_fleet_advisor_databases([], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_instance_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_instance_profile.return_value = {}
    delete_instance_profile("test-instance_profile_identifier", region_name=REGION)
    mock_client.delete_instance_profile.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_instance_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_instance_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to delete instance profile"):
        delete_instance_profile("test-instance_profile_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_migration_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_migration_project.return_value = {}
    delete_migration_project("test-migration_project_identifier", region_name=REGION)
    mock_client.delete_migration_project.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_migration_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_migration_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_migration_project",
    )
    with pytest.raises(RuntimeError, match="Failed to delete migration project"):
        delete_migration_project("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_replication_config(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_config.return_value = {}
    delete_replication_config("test-replication_config_arn", region_name=REGION)
    mock_client.delete_replication_config.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_replication_config_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_replication_config",
    )
    with pytest.raises(RuntimeError, match="Failed to delete replication config"):
        delete_replication_config("test-replication_config_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_replication_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_subnet_group.return_value = {}
    delete_replication_subnet_group("test-replication_subnet_group_identifier", region_name=REGION)
    mock_client.delete_replication_subnet_group.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_replication_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_replication_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete replication subnet group"):
        delete_replication_subnet_group("test-replication_subnet_group_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_delete_replication_task_assessment_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_task_assessment_run.return_value = {}
    delete_replication_task_assessment_run("test-replication_task_assessment_run_arn", region_name=REGION)
    mock_client.delete_replication_task_assessment_run.assert_called_once()


@patch("aws_util.dms.get_client")
def test_delete_replication_task_assessment_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_replication_task_assessment_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_replication_task_assessment_run",
    )
    with pytest.raises(RuntimeError, match="Failed to delete replication task assessment run"):
        delete_replication_task_assessment_run("test-replication_task_assessment_run_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_account_attributes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_attributes.return_value = {}
    describe_account_attributes(region_name=REGION)
    mock_client.describe_account_attributes.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_account_attributes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_attributes",
    )
    with pytest.raises(RuntimeError, match="Failed to describe account attributes"):
        describe_account_attributes(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_applicable_individual_assessments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_applicable_individual_assessments.return_value = {}
    describe_applicable_individual_assessments(region_name=REGION)
    mock_client.describe_applicable_individual_assessments.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_applicable_individual_assessments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_applicable_individual_assessments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_applicable_individual_assessments",
    )
    with pytest.raises(RuntimeError, match="Failed to describe applicable individual assessments"):
        describe_applicable_individual_assessments(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificates.return_value = {}
    describe_certificates(region_name=REGION)
    mock_client.describe_certificates.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to describe certificates"):
        describe_certificates(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_conversion_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_conversion_configuration.return_value = {}
    describe_conversion_configuration("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_conversion_configuration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_conversion_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_conversion_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_conversion_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe conversion configuration"):
        describe_conversion_configuration("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_data_migrations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_data_migrations.return_value = {}
    describe_data_migrations(region_name=REGION)
    mock_client.describe_data_migrations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_data_migrations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_data_migrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_migrations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe data migrations"):
        describe_data_migrations(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_data_providers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_data_providers.return_value = {}
    describe_data_providers(region_name=REGION)
    mock_client.describe_data_providers.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_data_providers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_data_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_providers",
    )
    with pytest.raises(RuntimeError, match="Failed to describe data providers"):
        describe_data_providers(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_endpoint_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint_settings.return_value = {}
    describe_endpoint_settings("test-engine_name", region_name=REGION)
    mock_client.describe_endpoint_settings.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_endpoint_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to describe endpoint settings"):
        describe_endpoint_settings("test-engine_name", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_endpoint_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint_types.return_value = {}
    describe_endpoint_types(region_name=REGION)
    mock_client.describe_endpoint_types.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_endpoint_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint_types",
    )
    with pytest.raises(RuntimeError, match="Failed to describe endpoint types"):
        describe_endpoint_types(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_engine_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_versions.return_value = {}
    describe_engine_versions(region_name=REGION)
    mock_client.describe_engine_versions.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_engine_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe engine versions"):
        describe_engine_versions(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_event_categories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.return_value = {}
    describe_event_categories(region_name=REGION)
    mock_client.describe_event_categories.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_event_categories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_categories",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event categories"):
        describe_event_categories(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_event_subscriptions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.return_value = {}
    describe_event_subscriptions(region_name=REGION)
    mock_client.describe_event_subscriptions.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_event_subscriptions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_subscriptions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event subscriptions"):
        describe_event_subscriptions(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.return_value = {}
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_extension_pack_associations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_extension_pack_associations.return_value = {}
    describe_extension_pack_associations("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_extension_pack_associations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_extension_pack_associations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_extension_pack_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_extension_pack_associations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe extension pack associations"):
        describe_extension_pack_associations("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_collectors(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_collectors.return_value = {}
    describe_fleet_advisor_collectors(region_name=REGION)
    mock_client.describe_fleet_advisor_collectors.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_collectors_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_collectors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_advisor_collectors",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet advisor collectors"):
        describe_fleet_advisor_collectors(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_databases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_databases.return_value = {}
    describe_fleet_advisor_databases(region_name=REGION)
    mock_client.describe_fleet_advisor_databases.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_databases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_advisor_databases",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet advisor databases"):
        describe_fleet_advisor_databases(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_lsa_analysis(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_lsa_analysis.return_value = {}
    describe_fleet_advisor_lsa_analysis(region_name=REGION)
    mock_client.describe_fleet_advisor_lsa_analysis.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_lsa_analysis_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_lsa_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_advisor_lsa_analysis",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet advisor lsa analysis"):
        describe_fleet_advisor_lsa_analysis(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_schema_object_summary(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_schema_object_summary.return_value = {}
    describe_fleet_advisor_schema_object_summary(region_name=REGION)
    mock_client.describe_fleet_advisor_schema_object_summary.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_schema_object_summary_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_schema_object_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_advisor_schema_object_summary",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet advisor schema object summary"):
        describe_fleet_advisor_schema_object_summary(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_schemas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_schemas.return_value = {}
    describe_fleet_advisor_schemas(region_name=REGION)
    mock_client.describe_fleet_advisor_schemas.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_fleet_advisor_schemas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_advisor_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_advisor_schemas",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet advisor schemas"):
        describe_fleet_advisor_schemas(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_instance_profiles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_instance_profiles.return_value = {}
    describe_instance_profiles(region_name=REGION)
    mock_client.describe_instance_profiles.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_instance_profiles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_instance_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_profiles",
    )
    with pytest.raises(RuntimeError, match="Failed to describe instance profiles"):
        describe_instance_profiles(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model.return_value = {}
    describe_metadata_model("test-selection_rules", "test-migration_project_identifier", "test-origin", region_name=REGION)
    mock_client.describe_metadata_model.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model"):
        describe_metadata_model("test-selection_rules", "test-migration_project_identifier", "test-origin", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_assessments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_assessments.return_value = {}
    describe_metadata_model_assessments("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_assessments.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_assessments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_assessments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_assessments",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model assessments"):
        describe_metadata_model_assessments("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_children(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_children.return_value = {}
    describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", region_name=REGION)
    mock_client.describe_metadata_model_children.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_children_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_children.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_children",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model children"):
        describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_conversions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_conversions.return_value = {}
    describe_metadata_model_conversions("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_conversions.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_conversions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_conversions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_conversions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model conversions"):
        describe_metadata_model_conversions("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_creations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_creations.return_value = {}
    describe_metadata_model_creations("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_creations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_creations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_creations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_creations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model creations"):
        describe_metadata_model_creations("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_exports_as_script(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_exports_as_script.return_value = {}
    describe_metadata_model_exports_as_script("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_exports_as_script.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_exports_as_script_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_exports_as_script.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_exports_as_script",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model exports as script"):
        describe_metadata_model_exports_as_script("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_exports_to_target(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_exports_to_target.return_value = {}
    describe_metadata_model_exports_to_target("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_exports_to_target.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_exports_to_target_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_exports_to_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_exports_to_target",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model exports to target"):
        describe_metadata_model_exports_to_target("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_imports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_imports.return_value = {}
    describe_metadata_model_imports("test-migration_project_identifier", region_name=REGION)
    mock_client.describe_metadata_model_imports.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_metadata_model_imports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_metadata_model_imports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metadata_model_imports",
    )
    with pytest.raises(RuntimeError, match="Failed to describe metadata model imports"):
        describe_metadata_model_imports("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_migration_projects(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_migration_projects.return_value = {}
    describe_migration_projects(region_name=REGION)
    mock_client.describe_migration_projects.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_migration_projects_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_migration_projects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_migration_projects",
    )
    with pytest.raises(RuntimeError, match="Failed to describe migration projects"):
        describe_migration_projects(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_orderable_replication_instances(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_replication_instances.return_value = {}
    describe_orderable_replication_instances(region_name=REGION)
    mock_client.describe_orderable_replication_instances.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_orderable_replication_instances_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_replication_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_orderable_replication_instances",
    )
    with pytest.raises(RuntimeError, match="Failed to describe orderable replication instances"):
        describe_orderable_replication_instances(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_pending_maintenance_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.return_value = {}
    describe_pending_maintenance_actions(region_name=REGION)
    mock_client.describe_pending_maintenance_actions.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_pending_maintenance_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pending_maintenance_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe pending maintenance actions"):
        describe_pending_maintenance_actions(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_recommendation_limitations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recommendation_limitations.return_value = {}
    describe_recommendation_limitations(region_name=REGION)
    mock_client.describe_recommendation_limitations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_recommendation_limitations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recommendation_limitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_recommendation_limitations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe recommendation limitations"):
        describe_recommendation_limitations(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_recommendations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recommendations.return_value = {}
    describe_recommendations(region_name=REGION)
    mock_client.describe_recommendations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_recommendations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_recommendations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe recommendations"):
        describe_recommendations(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_refresh_schemas_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_refresh_schemas_status.return_value = {}
    describe_refresh_schemas_status("test-endpoint_arn", region_name=REGION)
    mock_client.describe_refresh_schemas_status.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_refresh_schemas_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_refresh_schemas_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_refresh_schemas_status",
    )
    with pytest.raises(RuntimeError, match="Failed to describe refresh schemas status"):
        describe_refresh_schemas_status("test-endpoint_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_configs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_configs.return_value = {}
    describe_replication_configs(region_name=REGION)
    mock_client.describe_replication_configs.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_configs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_configs",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication configs"):
        describe_replication_configs(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_instance_task_logs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_instance_task_logs.return_value = {}
    describe_replication_instance_task_logs("test-replication_instance_arn", region_name=REGION)
    mock_client.describe_replication_instance_task_logs.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_instance_task_logs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_instance_task_logs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_instance_task_logs",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication instance task logs"):
        describe_replication_instance_task_logs("test-replication_instance_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_subnet_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_subnet_groups.return_value = {}
    describe_replication_subnet_groups(region_name=REGION)
    mock_client.describe_replication_subnet_groups.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_subnet_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_subnet_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_subnet_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication subnet groups"):
        describe_replication_subnet_groups(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_table_statistics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_table_statistics.return_value = {}
    describe_replication_table_statistics("test-replication_config_arn", region_name=REGION)
    mock_client.describe_replication_table_statistics.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_table_statistics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_table_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_table_statistics",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication table statistics"):
        describe_replication_table_statistics("test-replication_config_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_task_assessment_results(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_assessment_results.return_value = {}
    describe_replication_task_assessment_results(region_name=REGION)
    mock_client.describe_replication_task_assessment_results.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_task_assessment_results_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_assessment_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_task_assessment_results",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication task assessment results"):
        describe_replication_task_assessment_results(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_task_assessment_runs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_assessment_runs.return_value = {}
    describe_replication_task_assessment_runs(region_name=REGION)
    mock_client.describe_replication_task_assessment_runs.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_task_assessment_runs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_assessment_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_task_assessment_runs",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication task assessment runs"):
        describe_replication_task_assessment_runs(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replication_task_individual_assessments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_individual_assessments.return_value = {}
    describe_replication_task_individual_assessments(region_name=REGION)
    mock_client.describe_replication_task_individual_assessments.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replication_task_individual_assessments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replication_task_individual_assessments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_task_individual_assessments",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replication task individual assessments"):
        describe_replication_task_individual_assessments(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_replications(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replications.return_value = {}
    describe_replications(region_name=REGION)
    mock_client.describe_replications.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_replications_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_replications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replications",
    )
    with pytest.raises(RuntimeError, match="Failed to describe replications"):
        describe_replications(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_describe_schemas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_schemas.return_value = {}
    describe_schemas("test-endpoint_arn", region_name=REGION)
    mock_client.describe_schemas.assert_called_once()


@patch("aws_util.dms.get_client")
def test_describe_schemas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_schemas",
    )
    with pytest.raises(RuntimeError, match="Failed to describe schemas"):
        describe_schemas("test-endpoint_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_export_metadata_model_assessment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.export_metadata_model_assessment.return_value = {}
    export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", region_name=REGION)
    mock_client.export_metadata_model_assessment.assert_called_once()


@patch("aws_util.dms.get_client")
def test_export_metadata_model_assessment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.export_metadata_model_assessment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_metadata_model_assessment",
    )
    with pytest.raises(RuntimeError, match="Failed to export metadata model assessment"):
        export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_get_target_selection_rules(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_target_selection_rules.return_value = {}
    get_target_selection_rules("test-migration_project_identifier", "test-selection_rules", region_name=REGION)
    mock_client.get_target_selection_rules.assert_called_once()


@patch("aws_util.dms.get_client")
def test_get_target_selection_rules_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_target_selection_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_target_selection_rules",
    )
    with pytest.raises(RuntimeError, match="Failed to get target selection rules"):
        get_target_selection_rules("test-migration_project_identifier", "test-selection_rules", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_import_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_certificate.return_value = {}
    import_certificate("test-certificate_identifier", region_name=REGION)
    mock_client.import_certificate.assert_called_once()


@patch("aws_util.dms.get_client")
def test_import_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to import certificate"):
        import_certificate("test-certificate_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource(region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.dms.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_conversion_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_conversion_configuration.return_value = {}
    modify_conversion_configuration("test-migration_project_identifier", "test-conversion_configuration", region_name=REGION)
    mock_client.modify_conversion_configuration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_conversion_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_conversion_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_conversion_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to modify conversion configuration"):
        modify_conversion_configuration("test-migration_project_identifier", "test-conversion_configuration", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_data_migration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_data_migration.return_value = {}
    modify_data_migration("test-data_migration_identifier", region_name=REGION)
    mock_client.modify_data_migration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_data_migration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_data_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_data_migration",
    )
    with pytest.raises(RuntimeError, match="Failed to modify data migration"):
        modify_data_migration("test-data_migration_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_data_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_data_provider.return_value = {}
    modify_data_provider("test-data_provider_identifier", region_name=REGION)
    mock_client.modify_data_provider.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_data_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_data_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_data_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to modify data provider"):
        modify_data_provider("test-data_provider_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.return_value = {}
    modify_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.modify_event_subscription.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to modify event subscription"):
        modify_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_instance_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_instance_profile.return_value = {}
    modify_instance_profile("test-instance_profile_identifier", region_name=REGION)
    mock_client.modify_instance_profile.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_instance_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to modify instance profile"):
        modify_instance_profile("test-instance_profile_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_migration_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_migration_project.return_value = {}
    modify_migration_project("test-migration_project_identifier", region_name=REGION)
    mock_client.modify_migration_project.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_migration_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_migration_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_migration_project",
    )
    with pytest.raises(RuntimeError, match="Failed to modify migration project"):
        modify_migration_project("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_replication_config(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_config.return_value = {}
    modify_replication_config("test-replication_config_arn", region_name=REGION)
    mock_client.modify_replication_config.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_replication_config_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_replication_config",
    )
    with pytest.raises(RuntimeError, match="Failed to modify replication config"):
        modify_replication_config("test-replication_config_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_replication_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_subnet_group.return_value = {}
    modify_replication_subnet_group("test-replication_subnet_group_identifier", [], region_name=REGION)
    mock_client.modify_replication_subnet_group.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_replication_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_replication_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify replication subnet group"):
        modify_replication_subnet_group("test-replication_subnet_group_identifier", [], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_modify_replication_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_task.return_value = {}
    modify_replication_task("test-replication_task_arn", region_name=REGION)
    mock_client.modify_replication_task.assert_called_once()


@patch("aws_util.dms.get_client")
def test_modify_replication_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_replication_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_replication_task",
    )
    with pytest.raises(RuntimeError, match="Failed to modify replication task"):
        modify_replication_task("test-replication_task_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_move_replication_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.move_replication_task.return_value = {}
    move_replication_task("test-replication_task_arn", "test-target_replication_instance_arn", region_name=REGION)
    mock_client.move_replication_task.assert_called_once()


@patch("aws_util.dms.get_client")
def test_move_replication_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.move_replication_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "move_replication_task",
    )
    with pytest.raises(RuntimeError, match="Failed to move replication task"):
        move_replication_task("test-replication_task_arn", "test-target_replication_instance_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_reboot_replication_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_replication_instance.return_value = {}
    reboot_replication_instance("test-replication_instance_arn", region_name=REGION)
    mock_client.reboot_replication_instance.assert_called_once()


@patch("aws_util.dms.get_client")
def test_reboot_replication_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_replication_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_replication_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to reboot replication instance"):
        reboot_replication_instance("test-replication_instance_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_refresh_schemas(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.refresh_schemas.return_value = {}
    refresh_schemas("test-endpoint_arn", "test-replication_instance_arn", region_name=REGION)
    mock_client.refresh_schemas.assert_called_once()


@patch("aws_util.dms.get_client")
def test_refresh_schemas_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.refresh_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "refresh_schemas",
    )
    with pytest.raises(RuntimeError, match="Failed to refresh schemas"):
        refresh_schemas("test-endpoint_arn", "test-replication_instance_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_reload_replication_tables(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reload_replication_tables.return_value = {}
    reload_replication_tables("test-replication_config_arn", [], region_name=REGION)
    mock_client.reload_replication_tables.assert_called_once()


@patch("aws_util.dms.get_client")
def test_reload_replication_tables_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reload_replication_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reload_replication_tables",
    )
    with pytest.raises(RuntimeError, match="Failed to reload replication tables"):
        reload_replication_tables("test-replication_config_arn", [], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_reload_tables(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reload_tables.return_value = {}
    reload_tables("test-replication_task_arn", [], region_name=REGION)
    mock_client.reload_tables.assert_called_once()


@patch("aws_util.dms.get_client")
def test_reload_tables_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reload_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reload_tables",
    )
    with pytest.raises(RuntimeError, match="Failed to reload tables"):
        reload_tables("test-replication_task_arn", [], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_remove_tags_from_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.return_value = {}
    remove_tags_from_resource("test-resource_arn", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


@patch("aws_util.dms.get_client")
def test_remove_tags_from_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.dms.get_client")
def test_run_connection(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_connection.return_value = {}
    run_connection("test-replication_instance_arn", "test-endpoint_arn", region_name=REGION)
    mock_client.test_connection.assert_called_once()


@patch("aws_util.dms.get_client")
def test_run_connection_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_connection",
    )
    with pytest.raises(RuntimeError, match="Failed to run connection"):
        run_connection("test-replication_instance_arn", "test-endpoint_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_run_fleet_advisor_lsa_analysis(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.run_fleet_advisor_lsa_analysis.return_value = {}
    run_fleet_advisor_lsa_analysis(region_name=REGION)
    mock_client.run_fleet_advisor_lsa_analysis.assert_called_once()


@patch("aws_util.dms.get_client")
def test_run_fleet_advisor_lsa_analysis_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.run_fleet_advisor_lsa_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_fleet_advisor_lsa_analysis",
    )
    with pytest.raises(RuntimeError, match="Failed to run fleet advisor lsa analysis"):
        run_fleet_advisor_lsa_analysis(region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_data_migration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_data_migration.return_value = {}
    start_data_migration("test-data_migration_identifier", "test-start_type", region_name=REGION)
    mock_client.start_data_migration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_data_migration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_data_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_data_migration",
    )
    with pytest.raises(RuntimeError, match="Failed to start data migration"):
        start_data_migration("test-data_migration_identifier", "test-start_type", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_extension_pack_association(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_extension_pack_association.return_value = {}
    start_extension_pack_association("test-migration_project_identifier", region_name=REGION)
    mock_client.start_extension_pack_association.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_extension_pack_association_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_extension_pack_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_extension_pack_association",
    )
    with pytest.raises(RuntimeError, match="Failed to start extension pack association"):
        start_extension_pack_association("test-migration_project_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_assessment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_assessment.return_value = {}
    start_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", region_name=REGION)
    mock_client.start_metadata_model_assessment.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_assessment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_assessment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_assessment",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model assessment"):
        start_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_conversion(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_conversion.return_value = {}
    start_metadata_model_conversion("test-migration_project_identifier", "test-selection_rules", region_name=REGION)
    mock_client.start_metadata_model_conversion.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_conversion_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_conversion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_conversion",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model conversion"):
        start_metadata_model_conversion("test-migration_project_identifier", "test-selection_rules", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_creation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_creation.return_value = {}
    start_metadata_model_creation("test-migration_project_identifier", "test-selection_rules", "test-metadata_model_name", {}, region_name=REGION)
    mock_client.start_metadata_model_creation.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_creation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_creation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_creation",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model creation"):
        start_metadata_model_creation("test-migration_project_identifier", "test-selection_rules", "test-metadata_model_name", {}, region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_export_as_script(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_export_as_script.return_value = {}
    start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", region_name=REGION)
    mock_client.start_metadata_model_export_as_script.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_export_as_script_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_export_as_script.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_export_as_script",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model export as script"):
        start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_export_to_target(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_export_to_target.return_value = {}
    start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", region_name=REGION)
    mock_client.start_metadata_model_export_to_target.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_export_to_target_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_export_to_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_export_to_target",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model export to target"):
        start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_metadata_model_import(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_import.return_value = {}
    start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", region_name=REGION)
    mock_client.start_metadata_model_import.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_metadata_model_import_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_metadata_model_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_metadata_model_import",
    )
    with pytest.raises(RuntimeError, match="Failed to start metadata model import"):
        start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_recommendations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_recommendations.return_value = {}
    start_recommendations("test-database_id", {}, region_name=REGION)
    mock_client.start_recommendations.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_recommendations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_recommendations",
    )
    with pytest.raises(RuntimeError, match="Failed to start recommendations"):
        start_recommendations("test-database_id", {}, region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_replication(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication.return_value = {}
    start_replication("test-replication_config_arn", "test-start_replication_type", region_name=REGION)
    mock_client.start_replication.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_replication_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_replication",
    )
    with pytest.raises(RuntimeError, match="Failed to start replication"):
        start_replication("test-replication_config_arn", "test-start_replication_type", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_replication_task_assessment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication_task_assessment.return_value = {}
    start_replication_task_assessment("test-replication_task_arn", region_name=REGION)
    mock_client.start_replication_task_assessment.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_replication_task_assessment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication_task_assessment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_replication_task_assessment",
    )
    with pytest.raises(RuntimeError, match="Failed to start replication task assessment"):
        start_replication_task_assessment("test-replication_task_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_start_replication_task_assessment_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication_task_assessment_run.return_value = {}
    start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", region_name=REGION)
    mock_client.start_replication_task_assessment_run.assert_called_once()


@patch("aws_util.dms.get_client")
def test_start_replication_task_assessment_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_replication_task_assessment_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_replication_task_assessment_run",
    )
    with pytest.raises(RuntimeError, match="Failed to start replication task assessment run"):
        start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_stop_data_migration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_data_migration.return_value = {}
    stop_data_migration("test-data_migration_identifier", region_name=REGION)
    mock_client.stop_data_migration.assert_called_once()


@patch("aws_util.dms.get_client")
def test_stop_data_migration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_data_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_data_migration",
    )
    with pytest.raises(RuntimeError, match="Failed to stop data migration"):
        stop_data_migration("test-data_migration_identifier", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_stop_replication(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_replication.return_value = {}
    stop_replication("test-replication_config_arn", region_name=REGION)
    mock_client.stop_replication.assert_called_once()


@patch("aws_util.dms.get_client")
def test_stop_replication_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_replication",
    )
    with pytest.raises(RuntimeError, match="Failed to stop replication"):
        stop_replication("test-replication_config_arn", region_name=REGION)


@patch("aws_util.dms.get_client")
def test_update_subscriptions_to_event_bridge(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_subscriptions_to_event_bridge.return_value = {}
    update_subscriptions_to_event_bridge(region_name=REGION)
    mock_client.update_subscriptions_to_event_bridge.assert_called_once()


@patch("aws_util.dms.get_client")
def test_update_subscriptions_to_event_bridge_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_subscriptions_to_event_bridge.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_subscriptions_to_event_bridge",
    )
    with pytest.raises(RuntimeError, match="Failed to update subscriptions to event bridge"):
        update_subscriptions_to_event_bridge(region_name=REGION)


def test_batch_start_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import batch_start_recommendations
    mock_client = MagicMock()
    mock_client.batch_start_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    batch_start_recommendations(data="test-data", region_name="us-east-1")
    mock_client.batch_start_recommendations.assert_called_once()

def test_create_data_migration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_data_migration
    mock_client = MagicMock()
    mock_client.create_data_migration.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", data_migration_name="test-data_migration_name", enable_cloudwatch_logs=True, source_data_settings={}, target_data_settings={}, number_of_jobs="test-number_of_jobs", tags=[{"Key": "k", "Value": "v"}], selection_rules="test-selection_rules", region_name="us-east-1")
    mock_client.create_data_migration.assert_called_once()

def test_create_data_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_data_provider
    mock_client = MagicMock()
    mock_client.create_data_provider.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_data_provider("test-engine", {}, data_provider_name="test-data_provider_name", description="test-description", virtual="test-virtual", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_data_provider.assert_called_once()

def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_event_subscription
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_subscription.assert_called_once()

def test_create_fleet_advisor_collector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_fleet_advisor_collector
    mock_client = MagicMock()
    mock_client.create_fleet_advisor_collector.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", description="test-description", region_name="us-east-1")
    mock_client.create_fleet_advisor_collector.assert_called_once()

def test_create_instance_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_instance_profile
    mock_client = MagicMock()
    mock_client.create_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_instance_profile(availability_zone="test-availability_zone", kms_key_arn="test-kms_key_arn", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], network_type="test-network_type", instance_profile_name="test-instance_profile_name", description="test-description", subnet_group_identifier="test-subnet_group_identifier", vpc_security_groups="test-vpc_security_groups", region_name="us-east-1")
    mock_client.create_instance_profile.assert_called_once()

def test_create_migration_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_migration_project
    mock_client = MagicMock()
    mock_client.create_migration_project.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_migration_project("test-source_data_provider_descriptors", "test-target_data_provider_descriptors", "test-instance_profile_identifier", migration_project_name="test-migration_project_name", transformation_rules="test-transformation_rules", description="test-description", tags=[{"Key": "k", "Value": "v"}], schema_conversion_application_attributes="test-schema_conversion_application_attributes", region_name="us-east-1")
    mock_client.create_migration_project.assert_called_once()

def test_create_replication_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import create_replication_config
    mock_client = MagicMock()
    mock_client.create_replication_config.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    create_replication_config({}, "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", {}, replication_settings={}, supplemental_settings={}, resource_identifier="test-resource_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_replication_config.assert_called_once()

def test_describe_applicable_individual_assessments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_applicable_individual_assessments
    mock_client = MagicMock()
    mock_client.describe_applicable_individual_assessments.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_applicable_individual_assessments(replication_task_arn="test-replication_task_arn", replication_instance_arn="test-replication_instance_arn", replication_config_arn={}, source_engine_name="test-source_engine_name", target_engine_name="test-target_engine_name", migration_type="test-migration_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_applicable_individual_assessments.assert_called_once()

def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_certificates
    mock_client = MagicMock()
    mock_client.describe_certificates.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_certificates(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_certificates.assert_called_once()

def test_describe_data_migrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_data_migrations
    mock_client = MagicMock()
    mock_client.describe_data_migrations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_data_migrations(filters=[{}], max_records=1, marker="test-marker", without_settings={}, without_statistics="test-without_statistics", region_name="us-east-1")
    mock_client.describe_data_migrations.assert_called_once()

def test_describe_data_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_data_providers
    mock_client = MagicMock()
    mock_client.describe_data_providers.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_data_providers(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_data_providers.assert_called_once()

def test_describe_endpoint_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_endpoint_settings
    mock_client = MagicMock()
    mock_client.describe_endpoint_settings.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_settings("test-engine_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_endpoint_settings.assert_called_once()

def test_describe_endpoint_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_endpoint_types
    mock_client = MagicMock()
    mock_client.describe_endpoint_types.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_types(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_endpoint_types.assert_called_once()

def test_describe_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_engine_versions
    mock_client = MagicMock()
    mock_client.describe_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_engine_versions(max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_versions.assert_called_once()

def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_event_categories
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.describe_event_categories.assert_called_once()

def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_event_subscriptions
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_event_subscriptions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_extension_pack_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_extension_pack_associations
    mock_client = MagicMock()
    mock_client.describe_extension_pack_associations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_extension_pack_associations("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_extension_pack_associations.assert_called_once()

def test_describe_fleet_advisor_collectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_fleet_advisor_collectors
    mock_client = MagicMock()
    mock_client.describe_fleet_advisor_collectors.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_fleet_advisor_collectors(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_advisor_collectors.assert_called_once()

def test_describe_fleet_advisor_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_fleet_advisor_databases
    mock_client = MagicMock()
    mock_client.describe_fleet_advisor_databases.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_fleet_advisor_databases(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_advisor_databases.assert_called_once()

def test_describe_fleet_advisor_lsa_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_fleet_advisor_lsa_analysis
    mock_client = MagicMock()
    mock_client.describe_fleet_advisor_lsa_analysis.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_fleet_advisor_lsa_analysis(max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_advisor_lsa_analysis.assert_called_once()

def test_describe_fleet_advisor_schema_object_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_fleet_advisor_schema_object_summary
    mock_client = MagicMock()
    mock_client.describe_fleet_advisor_schema_object_summary.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_fleet_advisor_schema_object_summary(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_advisor_schema_object_summary.assert_called_once()

def test_describe_fleet_advisor_schemas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_fleet_advisor_schemas
    mock_client = MagicMock()
    mock_client.describe_fleet_advisor_schemas.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_fleet_advisor_schemas(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_advisor_schemas.assert_called_once()

def test_describe_instance_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_instance_profiles
    mock_client = MagicMock()
    mock_client.describe_instance_profiles.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_instance_profiles(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_instance_profiles.assert_called_once()

def test_describe_metadata_model_assessments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_assessments
    mock_client = MagicMock()
    mock_client.describe_metadata_model_assessments.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_assessments("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_assessments.assert_called_once()

def test_describe_metadata_model_children_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_children
    mock_client = MagicMock()
    mock_client.describe_metadata_model_children.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_children.assert_called_once()

def test_describe_metadata_model_conversions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_conversions
    mock_client = MagicMock()
    mock_client.describe_metadata_model_conversions.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_conversions("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_conversions.assert_called_once()

def test_describe_metadata_model_creations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_creations
    mock_client = MagicMock()
    mock_client.describe_metadata_model_creations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_creations("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_creations.assert_called_once()

def test_describe_metadata_model_exports_as_script_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_exports_as_script
    mock_client = MagicMock()
    mock_client.describe_metadata_model_exports_as_script.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_exports_as_script("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_exports_as_script.assert_called_once()

def test_describe_metadata_model_exports_to_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_exports_to_target
    mock_client = MagicMock()
    mock_client.describe_metadata_model_exports_to_target.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_exports_to_target("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_exports_to_target.assert_called_once()

def test_describe_metadata_model_imports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_metadata_model_imports
    mock_client = MagicMock()
    mock_client.describe_metadata_model_imports.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_metadata_model_imports("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_metadata_model_imports.assert_called_once()

def test_describe_migration_projects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_migration_projects
    mock_client = MagicMock()
    mock_client.describe_migration_projects.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_migration_projects(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_migration_projects.assert_called_once()

def test_describe_orderable_replication_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_orderable_replication_instances
    mock_client = MagicMock()
    mock_client.describe_orderable_replication_instances.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_orderable_replication_instances(max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_orderable_replication_instances.assert_called_once()

def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_pending_maintenance_actions
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_pending_maintenance_actions(replication_instance_arn="test-replication_instance_arn", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_pending_maintenance_actions.assert_called_once()

def test_describe_recommendation_limitations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_recommendation_limitations
    mock_client = MagicMock()
    mock_client.describe_recommendation_limitations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_recommendation_limitations(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_recommendation_limitations.assert_called_once()

def test_describe_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_recommendations
    mock_client = MagicMock()
    mock_client.describe_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_recommendations(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_recommendations.assert_called_once()

def test_describe_replication_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_configs
    mock_client = MagicMock()
    mock_client.describe_replication_configs.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_configs(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_configs.assert_called_once()

def test_describe_replication_instance_task_logs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_instance_task_logs
    mock_client = MagicMock()
    mock_client.describe_replication_instance_task_logs.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_instance_task_logs("test-replication_instance_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_instance_task_logs.assert_called_once()

def test_describe_replication_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_replication_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_subnet_groups(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_subnet_groups.assert_called_once()

def test_describe_replication_table_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_table_statistics
    mock_client = MagicMock()
    mock_client.describe_replication_table_statistics.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_table_statistics({}, max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.describe_replication_table_statistics.assert_called_once()

def test_describe_replication_task_assessment_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_task_assessment_results
    mock_client = MagicMock()
    mock_client.describe_replication_task_assessment_results.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_task_assessment_results(replication_task_arn="test-replication_task_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_task_assessment_results.assert_called_once()

def test_describe_replication_task_assessment_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_task_assessment_runs
    mock_client = MagicMock()
    mock_client.describe_replication_task_assessment_runs.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_task_assessment_runs(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_task_assessment_runs.assert_called_once()

def test_describe_replication_task_individual_assessments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replication_task_individual_assessments
    mock_client = MagicMock()
    mock_client.describe_replication_task_individual_assessments.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replication_task_individual_assessments(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replication_task_individual_assessments.assert_called_once()

def test_describe_replications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_replications
    mock_client = MagicMock()
    mock_client.describe_replications.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_replications(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_replications.assert_called_once()

def test_describe_schemas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import describe_schemas
    mock_client = MagicMock()
    mock_client.describe_schemas.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    describe_schemas("test-endpoint_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_schemas.assert_called_once()

def test_export_metadata_model_assessment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import export_metadata_model_assessment
    mock_client = MagicMock()
    mock_client.export_metadata_model_assessment.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", file_name="test-file_name", assessment_report_types=1, region_name="us-east-1")
    mock_client.export_metadata_model_assessment.assert_called_once()

def test_import_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import import_certificate
    mock_client = MagicMock()
    mock_client.import_certificate.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    import_certificate("test-certificate_identifier", certificate_pem="test-certificate_pem", certificate_wallet="test-certificate_wallet", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_certificate.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource(resource_arn="test-resource_arn", resource_arn_list="test-resource_arn_list", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_modify_data_migration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_data_migration
    mock_client = MagicMock()
    mock_client.modify_data_migration.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_data_migration("test-data_migration_identifier", data_migration_name="test-data_migration_name", enable_cloudwatch_logs=True, service_access_role_arn="test-service_access_role_arn", data_migration_type="test-data_migration_type", source_data_settings={}, target_data_settings={}, number_of_jobs="test-number_of_jobs", selection_rules="test-selection_rules", region_name="us-east-1")
    mock_client.modify_data_migration.assert_called_once()

def test_modify_data_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_data_provider
    mock_client = MagicMock()
    mock_client.modify_data_provider.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_data_provider("test-data_provider_identifier", data_provider_name="test-data_provider_name", description="test-description", engine="test-engine", virtual="test-virtual", exact_settings={}, settings={}, region_name="us-east-1")
    mock_client.modify_data_provider.assert_called_once()

def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_event_subscription
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.modify_event_subscription.assert_called_once()

def test_modify_instance_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_instance_profile
    mock_client = MagicMock()
    mock_client.modify_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_instance_profile("test-instance_profile_identifier", availability_zone="test-availability_zone", kms_key_arn="test-kms_key_arn", publicly_accessible="test-publicly_accessible", network_type="test-network_type", instance_profile_name="test-instance_profile_name", description="test-description", subnet_group_identifier="test-subnet_group_identifier", vpc_security_groups="test-vpc_security_groups", region_name="us-east-1")
    mock_client.modify_instance_profile.assert_called_once()

def test_modify_migration_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_migration_project
    mock_client = MagicMock()
    mock_client.modify_migration_project.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_migration_project("test-migration_project_identifier", migration_project_name="test-migration_project_name", source_data_provider_descriptors="test-source_data_provider_descriptors", target_data_provider_descriptors="test-target_data_provider_descriptors", instance_profile_identifier="test-instance_profile_identifier", transformation_rules="test-transformation_rules", description="test-description", schema_conversion_application_attributes="test-schema_conversion_application_attributes", region_name="us-east-1")
    mock_client.modify_migration_project.assert_called_once()

def test_modify_replication_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_replication_config
    mock_client = MagicMock()
    mock_client.modify_replication_config.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_replication_config({}, replication_config_identifier={}, replication_type="test-replication_type", table_mappings={}, replication_settings={}, supplemental_settings={}, compute_config={}, source_endpoint_arn="test-source_endpoint_arn", target_endpoint_arn="test-target_endpoint_arn", region_name="us-east-1")
    mock_client.modify_replication_config.assert_called_once()

def test_modify_replication_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_replication_subnet_group
    mock_client = MagicMock()
    mock_client.modify_replication_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_replication_subnet_group("test-replication_subnet_group_identifier", "test-subnet_ids", replication_subnet_group_description="test-replication_subnet_group_description", region_name="us-east-1")
    mock_client.modify_replication_subnet_group.assert_called_once()

def test_modify_replication_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import modify_replication_task
    mock_client = MagicMock()
    mock_client.modify_replication_task.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    modify_replication_task("test-replication_task_arn", replication_task_identifier="test-replication_task_identifier", migration_type="test-migration_type", table_mappings={}, replication_task_settings={}, cdc_start_time="test-cdc_start_time", cdc_start_position="test-cdc_start_position", cdc_stop_position="test-cdc_stop_position", task_data="test-task_data", region_name="us-east-1")
    mock_client.modify_replication_task.assert_called_once()

def test_reboot_replication_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import reboot_replication_instance
    mock_client = MagicMock()
    mock_client.reboot_replication_instance.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    reboot_replication_instance("test-replication_instance_arn", force_failover=True, force_planned_failover=True, region_name="us-east-1")
    mock_client.reboot_replication_instance.assert_called_once()

def test_reload_replication_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import reload_replication_tables
    mock_client = MagicMock()
    mock_client.reload_replication_tables.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    reload_replication_tables({}, "test-tables_to_reload", reload_option="test-reload_option", region_name="us-east-1")
    mock_client.reload_replication_tables.assert_called_once()

def test_reload_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import reload_tables
    mock_client = MagicMock()
    mock_client.reload_tables.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    reload_tables("test-replication_task_arn", "test-tables_to_reload", reload_option="test-reload_option", region_name="us-east-1")
    mock_client.reload_tables.assert_called_once()

def test_start_metadata_model_export_as_script_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import start_metadata_model_export_as_script
    mock_client = MagicMock()
    mock_client.start_metadata_model_export_as_script.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", file_name="test-file_name", region_name="us-east-1")
    mock_client.start_metadata_model_export_as_script.assert_called_once()

def test_start_metadata_model_export_to_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import start_metadata_model_export_to_target
    mock_client = MagicMock()
    mock_client.start_metadata_model_export_to_target.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", overwrite_extension_pack="test-overwrite_extension_pack", region_name="us-east-1")
    mock_client.start_metadata_model_export_to_target.assert_called_once()

def test_start_metadata_model_import_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import start_metadata_model_import
    mock_client = MagicMock()
    mock_client.start_metadata_model_import.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", refresh="test-refresh", region_name="us-east-1")
    mock_client.start_metadata_model_import.assert_called_once()

def test_start_replication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import start_replication
    mock_client = MagicMock()
    mock_client.start_replication.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    start_replication({}, "test-start_replication_type", premigration_assessment_settings={}, cdc_start_time="test-cdc_start_time", cdc_start_position="test-cdc_start_position", cdc_stop_position="test-cdc_stop_position", region_name="us-east-1")
    mock_client.start_replication.assert_called_once()

def test_start_replication_task_assessment_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import start_replication_task_assessment_run
    mock_client = MagicMock()
    mock_client.start_replication_task_assessment_run.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", result_location_folder="test-result_location_folder", result_encryption_mode="test-result_encryption_mode", result_kms_key_arn="test-result_kms_key_arn", include_only=True, exclude="test-exclude", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_replication_task_assessment_run.assert_called_once()

def test_update_subscriptions_to_event_bridge_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dms import update_subscriptions_to_event_bridge
    mock_client = MagicMock()
    mock_client.update_subscriptions_to_event_bridge.return_value = {}
    monkeypatch.setattr("aws_util.dms.get_client", lambda *a, **kw: mock_client)
    update_subscriptions_to_event_bridge(force_move=True, region_name="us-east-1")
    mock_client.update_subscriptions_to_event_bridge.assert_called_once()
