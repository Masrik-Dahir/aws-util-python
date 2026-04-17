

"""Unit tests for aws_util.aio.dms."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import aws_util.aio.dms as _aio_dms
from aws_util.aio.dms import (
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
aio_dms_test_connection = _aio_dms.test_connection
from aws_util.exceptions import AwsTimeoutError


REGION = "us-east-1"
def _mock_client() -> MagicMock:
    client = MagicMock()
    client.call = AsyncMock()
    return client


# ---------------------------------------------------------------------------
# Replication instances
# ---------------------------------------------------------------------------


@patch("aws_util.aio.dms.async_client")
class TestCreateReplicationInstance:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
                "ReplicationInstanceClass": "dms.t3.medium",
                "ReplicationInstanceStatus": "creating",
            }
        }
        result = await create_replication_instance(
            "ri-1", "dms.t3.medium"
        )
        assert result.replication_instance_identifier == "ri-1"

    async def test_with_options(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-2",
                "ReplicationInstanceArn": "arn:ri-2",
            }
        }
        result = await create_replication_instance(
            "ri-2",
            "dms.r5.large",
            allocated_storage=100,
            availability_zone="us-east-1a",
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert result.replication_instance_arn == "arn:ri-2"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await create_replication_instance(
                "ri-1", "dms.t3.medium"
            )


@patch("aws_util.aio.dms.async_client")
class TestDescribeReplicationInstances:
    async def test_empty(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstances": []
        }
        result = await describe_replication_instances()
        assert result == []

    async def test_with_pagination(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = [
            {
                "ReplicationInstances": [
                    {
                        "ReplicationInstanceIdentifier": "ri-1",
                        "ReplicationInstanceArn": "arn:ri-1",
                    }
                ],
                "Marker": "tok1",
            },
            {
                "ReplicationInstances": [
                    {
                        "ReplicationInstanceIdentifier": "ri-2",
                        "ReplicationInstanceArn": "arn:ri-2",
                    }
                ],
            },
        ]
        result = await describe_replication_instances()
        assert len(result) == 2

    async def test_with_filters(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstances": []
        }
        await describe_replication_instances(
            filters=[{"Name": "status", "Values": ["available"]}]
        )
        client.call.assert_called_once()

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await describe_replication_instances()


@patch("aws_util.aio.dms.async_client")
class TestModifyReplicationInstance:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
            }
        }
        result = await modify_replication_instance(
            "arn:ri-1",
            replication_instance_class="dms.r5.large",
            allocated_storage=200,
            multi_az=True,
        )
        assert isinstance(result, ReplicationInstanceResult)

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await modify_replication_instance("arn:ri-missing")


@patch("aws_util.aio.dms.async_client")
class TestDeleteReplicationInstance:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationInstance": {
                "ReplicationInstanceIdentifier": "ri-1",
                "ReplicationInstanceArn": "arn:ri-1",
                "ReplicationInstanceStatus": "deleting",
            }
        }
        result = await delete_replication_instance("arn:ri-1")
        assert (
            result.replication_instance_status == "deleting"
        )

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await delete_replication_instance("arn:ri-missing")


@patch("aws_util.aio.dms.describe_replication_instances")
class TestWaitForReplicationInstance:
    async def test_immediate(
        self, mock_desc: MagicMock
    ) -> None:
        mock_desc.return_value = [
            ReplicationInstanceResult(
                replication_instance_identifier="ri-1",
                replication_instance_arn="arn:ri-1",
                replication_instance_status="available",
            )
        ]
        # Make mock awaitable
        mock_desc.side_effect = None
        mock_desc.return_value = [
            ReplicationInstanceResult(
                replication_instance_identifier="ri-1",
                replication_instance_arn="arn:ri-1",
                replication_instance_status="available",
            )
        ]
        mock_desc.__class__ = AsyncMock
        result = await wait_for_replication_instance(
            "arn:ri-1"
        )
        assert result.replication_instance_status == "available"

    @patch("aws_util.aio.dms._time")
    @patch("aws_util.aio.dms.asyncio.sleep", new_callable=AsyncMock)
    async def test_timeout(
        self,
        mock_sleep: AsyncMock,
        mock_time: MagicMock,
        mock_desc: MagicMock,
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_desc.return_value = [
            ReplicationInstanceResult(
                replication_instance_identifier="ri-1",
                replication_instance_arn="arn:ri-1",
                replication_instance_status="creating",
            )
        ]
        mock_desc.__class__ = AsyncMock
        with pytest.raises(AwsTimeoutError):
            await wait_for_replication_instance(
                "arn:ri-1", timeout=5
            )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@patch("aws_util.aio.dms.async_client")
class TestCreateEndpoint:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
                "EndpointType": "source",
                "EngineName": "mysql",
            }
        }
        result = await create_endpoint(
            "ep-1", "source", "mysql"
        )
        assert result.endpoint_identifier == "ep-1"

    async def test_with_options(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-2",
                "EndpointArn": "arn:ep-2",
            }
        }
        result = await create_endpoint(
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

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await create_endpoint("ep-1", "source", "mysql")


@patch("aws_util.aio.dms.async_client")
class TestDescribeEndpoints:
    async def test_empty(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {"Endpoints": []}
        result = await describe_endpoints()
        assert result == []

    async def test_with_pagination(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = [
            {
                "Endpoints": [
                    {
                        "EndpointIdentifier": "ep-1",
                        "EndpointArn": "arn:ep-1",
                    }
                ],
                "Marker": "tok1",
            },
            {
                "Endpoints": [
                    {
                        "EndpointIdentifier": "ep-2",
                        "EndpointArn": "arn:ep-2",
                    }
                ],
            },
        ]
        result = await describe_endpoints()
        assert len(result) == 2

    async def test_with_filters(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {"Endpoints": []}
        await describe_endpoints(
            filters=[{"Name": "type", "Values": ["source"]}]
        )
        client.call.assert_called_once()

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await describe_endpoints()


@patch("aws_util.aio.dms.async_client")
class TestModifyEndpoint:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
            }
        }
        result = await modify_endpoint(
            "arn:ep-1",
            endpoint_identifier="ep-new",
            engine_name="postgres",
            server_name="new.db",
            port=5433,
            database_name="newdb",
            username="u",
            password="p",
            ssl_mode="require",
        )
        assert isinstance(result, EndpointResult)

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await modify_endpoint("arn:ep-missing")


@patch("aws_util.aio.dms.async_client")
class TestDeleteEndpoint:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "Endpoint": {
                "EndpointIdentifier": "ep-1",
                "EndpointArn": "arn:ep-1",
                "Status": "deleting",
            }
        }
        result = await delete_endpoint("arn:ep-1")
        assert result.status == "deleting"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await delete_endpoint("arn:ep-missing")


@patch("aws_util.aio.dms.async_client")
class TestTestConnection:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "Connection": {
                "ReplicationInstanceArn": "arn:ri-1",
                "EndpointArn": "arn:ep-1",
                "Status": "testing",
            }
        }
        result = await aio_dms_test_connection(
            "arn:ri-1", "arn:ep-1"
        )
        assert result.status == "testing"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await aio_dms_test_connection("arn:ri-1", "arn:ep-1")


@patch("aws_util.aio.dms.async_client")
class TestDescribeConnections:
    async def test_empty(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {"Connections": []}
        result = await describe_connections()
        assert result == []

    async def test_with_pagination(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = [
            {
                "Connections": [
                    {
                        "ReplicationInstanceArn": "arn:ri-1",
                        "EndpointArn": "arn:ep-1",
                        "Status": "successful",
                    }
                ],
                "Marker": "tok1",
            },
            {"Connections": []},
        ]
        result = await describe_connections()
        assert len(result) == 1

    async def test_with_filters(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {"Connections": []}
        await describe_connections(
            filters=[{"Name": "status", "Values": ["successful"]}]
        )
        client.call.assert_called_once()

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await describe_connections()


# ---------------------------------------------------------------------------
# Replication tasks
# ---------------------------------------------------------------------------


@patch("aws_util.aio.dms.async_client")
class TestCreateReplicationTask:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "creating",
            }
        }
        result = await create_replication_task(
            "task-1",
            "arn:src",
            "arn:tgt",
            "arn:ri-1",
            "full-load",
            '{"rules": []}',
        )
        assert result.replication_task_identifier == "task-1"

    async def test_with_tags(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-2",
                "ReplicationTaskArn": "arn:task-2",
            }
        }
        result = await create_replication_task(
            "task-2",
            "arn:src",
            "arn:tgt",
            "arn:ri-1",
            "cdc",
            '{"rules": []}',
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert result.replication_task_arn == "arn:task-2"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await create_replication_task(
                "task-1",
                "arn:src",
                "arn:tgt",
                "arn:ri-1",
                "full-load",
                '{"rules": []}',
            )


@patch("aws_util.aio.dms.async_client")
class TestDescribeReplicationTasks:
    async def test_empty(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTasks": []
        }
        result = await describe_replication_tasks()
        assert result == []

    async def test_with_pagination(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = [
            {
                "ReplicationTasks": [
                    {
                        "ReplicationTaskIdentifier": "task-1",
                        "ReplicationTaskArn": "arn:task-1",
                    }
                ],
                "Marker": "tok1",
            },
            {"ReplicationTasks": []},
        ]
        result = await describe_replication_tasks()
        assert len(result) == 1

    async def test_with_filters(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTasks": []
        }
        await describe_replication_tasks(
            filters=[{"Name": "status", "Values": ["running"]}]
        )
        client.call.assert_called_once()

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await describe_replication_tasks()


@patch("aws_util.aio.dms.async_client")
class TestStartReplicationTask:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "starting",
            }
        }
        result = await start_replication_task("arn:task-1")
        assert result.status == "starting"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await start_replication_task("arn:task-missing")


@patch("aws_util.aio.dms.async_client")
class TestStopReplicationTask:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "stopping",
            }
        }
        result = await stop_replication_task("arn:task-1")
        assert result.status == "stopping"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await stop_replication_task("arn:task-missing")


@patch("aws_util.aio.dms.async_client")
class TestDeleteReplicationTask:
    async def test_success(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationTask": {
                "ReplicationTaskIdentifier": "task-1",
                "ReplicationTaskArn": "arn:task-1",
                "Status": "deleting",
            }
        }
        result = await delete_replication_task("arn:task-1")
        assert result.status == "deleting"

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await delete_replication_task("arn:task-missing")


@patch("aws_util.aio.dms.describe_replication_tasks")
class TestWaitForReplicationTask:
    async def test_immediate(
        self, mock_desc: MagicMock
    ) -> None:
        mock_desc.return_value = [
            ReplicationTaskResult(
                replication_task_identifier="task-1",
                replication_task_arn="arn:task-1",
                status="running",
            )
        ]
        mock_desc.__class__ = AsyncMock
        result = await wait_for_replication_task(
            "arn:task-1"
        )
        assert result.status == "running"

    @patch("aws_util.aio.dms._time")
    @patch("aws_util.aio.dms.asyncio.sleep", new_callable=AsyncMock)
    async def test_timeout(
        self,
        mock_sleep: AsyncMock,
        mock_time: MagicMock,
        mock_desc: MagicMock,
    ) -> None:
        mock_time.monotonic.side_effect = [0, 0, 1000]
        mock_desc.return_value = [
            ReplicationTaskResult(
                replication_task_identifier="task-1",
                replication_task_arn="arn:task-1",
                status="starting",
            )
        ]
        mock_desc.__class__ = AsyncMock
        with pytest.raises(AwsTimeoutError):
            await wait_for_replication_task(
                "arn:task-1", timeout=5
            )


@patch("aws_util.aio.dms.async_client")
class TestDescribeTableStatistics:
    async def test_empty(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "TableStatistics": []
        }
        result = await describe_table_statistics(
            "arn:task-1"
        )
        assert result == []

    async def test_with_items(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "TableStatistics": [
                {
                    "SchemaName": "public",
                    "TableName": "users",
                    "Inserts": 100,
                    "Deletes": 5,
                    "Updates": 50,
                    "FullLoadRows": 1000,
                    "TableState": "completed",
                }
            ]
        }
        result = await describe_table_statistics(
            "arn:task-1"
        )
        assert len(result) == 1
        assert result[0].inserts == 100

    async def test_with_pagination(
        self, gc: MagicMock
    ) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = [
            {
                "TableStatistics": [
                    {
                        "SchemaName": "public",
                        "TableName": "t1",
                    }
                ],
                "Marker": "tok1",
            },
            {"TableStatistics": []},
        ]
        result = await describe_table_statistics(
            "arn:task-1"
        )
        assert len(result) == 1

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await describe_table_statistics("arn:task-1")


# ---------------------------------------------------------------------------
# Subnet groups
# ---------------------------------------------------------------------------


@patch("aws_util.aio.dms.async_client")
class TestCreateReplicationSubnetGroup:
    async def test_basic(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationSubnetGroup": {
                "ReplicationSubnetGroupIdentifier": "sg-1",
                "ReplicationSubnetGroupDescription": "test",
                "VpcId": "vpc-123",
                "SubnetGroupStatus": "Complete",
            }
        }
        result = await create_replication_subnet_group(
            "sg-1", "test", ["subnet-1"]
        )
        assert (
            result.replication_subnet_group_identifier
            == "sg-1"
        )

    async def test_with_tags(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.return_value = {
            "ReplicationSubnetGroup": {
                "ReplicationSubnetGroupIdentifier": "sg-2",
            }
        }
        result = await create_replication_subnet_group(
            "sg-2",
            "prod",
            ["subnet-1"],
            tags=[{"Key": "env", "Value": "prod"}],
        )
        assert isinstance(result, ReplicationSubnetGroupResult)

    async def test_error(self, gc: MagicMock) -> None:
        client = _mock_client()
        gc.return_value = client
        client.call.side_effect = RuntimeError("fail")
        with pytest.raises(Exception):
            await create_replication_subnet_group(
                "sg-1", "test", ["subnet-1"]
            )


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_arn", [], )


async def test_apply_pending_maintenance_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_pending_maintenance_action("test-replication_instance_arn", "test-apply_action", "test-opt_in_type", )
    mock_client.call.assert_called_once()


async def test_apply_pending_maintenance_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_pending_maintenance_action("test-replication_instance_arn", "test-apply_action", "test-opt_in_type", )


async def test_batch_start_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_start_recommendations()
    mock_client.call.assert_called_once()


async def test_batch_start_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_start_recommendations()


async def test_cancel_metadata_model_conversion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_metadata_model_conversion("test-migration_project_identifier", "test-request_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_metadata_model_conversion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_metadata_model_conversion("test-migration_project_identifier", "test-request_identifier", )


async def test_cancel_metadata_model_creation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_metadata_model_creation("test-migration_project_identifier", "test-request_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_metadata_model_creation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_metadata_model_creation("test-migration_project_identifier", "test-request_identifier", )


async def test_cancel_replication_task_assessment_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_replication_task_assessment_run("test-replication_task_assessment_run_arn", )
    mock_client.call.assert_called_once()


async def test_cancel_replication_task_assessment_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_replication_task_assessment_run("test-replication_task_assessment_run_arn", )


async def test_create_data_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_data_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", )


async def test_create_data_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_data_provider("test-engine", {}, )
    mock_client.call.assert_called_once()


async def test_create_data_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_provider("test-engine", {}, )


async def test_create_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )


async def test_create_fleet_advisor_collector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", )
    mock_client.call.assert_called_once()


async def test_create_fleet_advisor_collector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", )


async def test_create_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_profile()
    mock_client.call.assert_called_once()


async def test_create_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_profile()


async def test_create_migration_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_migration_project([], [], "test-instance_profile_identifier", )
    mock_client.call.assert_called_once()


async def test_create_migration_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_migration_project([], [], "test-instance_profile_identifier", )


async def test_create_replication_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_replication_config("test-replication_config_identifier", "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", "test-table_mappings", )
    mock_client.call.assert_called_once()


async def test_create_replication_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_replication_config("test-replication_config_identifier", "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", "test-table_mappings", )


async def test_delete_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_certificate("test-certificate_arn", )
    mock_client.call.assert_called_once()


async def test_delete_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_certificate("test-certificate_arn", )


async def test_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connection("test-endpoint_arn", "test-replication_instance_arn", )
    mock_client.call.assert_called_once()


async def test_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection("test-endpoint_arn", "test-replication_instance_arn", )


async def test_delete_data_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_migration("test-data_migration_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_data_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_migration("test-data_migration_identifier", )


async def test_delete_data_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_provider("test-data_provider_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_data_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_provider("test-data_provider_identifier", )


async def test_delete_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_delete_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_subscription("test-subscription_name", )


async def test_delete_fleet_advisor_collector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fleet_advisor_collector("test-collector_referenced_id", )
    mock_client.call.assert_called_once()


async def test_delete_fleet_advisor_collector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fleet_advisor_collector("test-collector_referenced_id", )


async def test_delete_fleet_advisor_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fleet_advisor_databases([], )
    mock_client.call.assert_called_once()


async def test_delete_fleet_advisor_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fleet_advisor_databases([], )


async def test_delete_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_instance_profile("test-instance_profile_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_instance_profile("test-instance_profile_identifier", )


async def test_delete_migration_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_migration_project("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_migration_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_migration_project("test-migration_project_identifier", )


async def test_delete_replication_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_replication_config("test-replication_config_arn", )
    mock_client.call.assert_called_once()


async def test_delete_replication_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replication_config("test-replication_config_arn", )


async def test_delete_replication_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_replication_subnet_group("test-replication_subnet_group_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_replication_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replication_subnet_group("test-replication_subnet_group_identifier", )


async def test_delete_replication_task_assessment_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_replication_task_assessment_run("test-replication_task_assessment_run_arn", )
    mock_client.call.assert_called_once()


async def test_delete_replication_task_assessment_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replication_task_assessment_run("test-replication_task_assessment_run_arn", )


async def test_describe_account_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_attributes()
    mock_client.call.assert_called_once()


async def test_describe_account_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_attributes()


async def test_describe_applicable_individual_assessments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_applicable_individual_assessments()
    mock_client.call.assert_called_once()


async def test_describe_applicable_individual_assessments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_applicable_individual_assessments()


async def test_describe_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificates()
    mock_client.call.assert_called_once()


async def test_describe_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificates()


async def test_describe_conversion_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_conversion_configuration("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_conversion_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_conversion_configuration("test-migration_project_identifier", )


async def test_describe_data_migrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_migrations()
    mock_client.call.assert_called_once()


async def test_describe_data_migrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_migrations()


async def test_describe_data_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_providers()
    mock_client.call.assert_called_once()


async def test_describe_data_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_providers()


async def test_describe_endpoint_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint_settings("test-engine_name", )
    mock_client.call.assert_called_once()


async def test_describe_endpoint_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint_settings("test-engine_name", )


async def test_describe_endpoint_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint_types()
    mock_client.call.assert_called_once()


async def test_describe_endpoint_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint_types()


async def test_describe_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_versions()


async def test_describe_event_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_categories()
    mock_client.call.assert_called_once()


async def test_describe_event_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_categories()


async def test_describe_event_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_subscriptions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_extension_pack_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_extension_pack_associations("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_extension_pack_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_extension_pack_associations("test-migration_project_identifier", )


async def test_describe_fleet_advisor_collectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_advisor_collectors()
    mock_client.call.assert_called_once()


async def test_describe_fleet_advisor_collectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_advisor_collectors()


async def test_describe_fleet_advisor_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_advisor_databases()
    mock_client.call.assert_called_once()


async def test_describe_fleet_advisor_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_advisor_databases()


async def test_describe_fleet_advisor_lsa_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_advisor_lsa_analysis()
    mock_client.call.assert_called_once()


async def test_describe_fleet_advisor_lsa_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_advisor_lsa_analysis()


async def test_describe_fleet_advisor_schema_object_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_advisor_schema_object_summary()
    mock_client.call.assert_called_once()


async def test_describe_fleet_advisor_schema_object_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_advisor_schema_object_summary()


async def test_describe_fleet_advisor_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_advisor_schemas()
    mock_client.call.assert_called_once()


async def test_describe_fleet_advisor_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_advisor_schemas()


async def test_describe_instance_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_profiles()
    mock_client.call.assert_called_once()


async def test_describe_instance_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_profiles()


async def test_describe_metadata_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model("test-selection_rules", "test-migration_project_identifier", "test-origin", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model("test-selection_rules", "test-migration_project_identifier", "test-origin", )


async def test_describe_metadata_model_assessments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_assessments("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_assessments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_assessments("test-migration_project_identifier", )


async def test_describe_metadata_model_children(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_children_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", )


async def test_describe_metadata_model_conversions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_conversions("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_conversions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_conversions("test-migration_project_identifier", )


async def test_describe_metadata_model_creations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_creations("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_creations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_creations("test-migration_project_identifier", )


async def test_describe_metadata_model_exports_as_script(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_exports_as_script("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_exports_as_script_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_exports_as_script("test-migration_project_identifier", )


async def test_describe_metadata_model_exports_to_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_exports_to_target("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_exports_to_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_exports_to_target("test-migration_project_identifier", )


async def test_describe_metadata_model_imports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metadata_model_imports("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_metadata_model_imports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metadata_model_imports("test-migration_project_identifier", )


async def test_describe_migration_projects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_migration_projects()
    mock_client.call.assert_called_once()


async def test_describe_migration_projects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_migration_projects()


async def test_describe_orderable_replication_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_orderable_replication_instances()
    mock_client.call.assert_called_once()


async def test_describe_orderable_replication_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_orderable_replication_instances()


async def test_describe_pending_maintenance_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pending_maintenance_actions()
    mock_client.call.assert_called_once()


async def test_describe_pending_maintenance_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pending_maintenance_actions()


async def test_describe_recommendation_limitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_recommendation_limitations()
    mock_client.call.assert_called_once()


async def test_describe_recommendation_limitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_recommendation_limitations()


async def test_describe_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_recommendations()
    mock_client.call.assert_called_once()


async def test_describe_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_recommendations()


async def test_describe_refresh_schemas_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_refresh_schemas_status("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_describe_refresh_schemas_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_refresh_schemas_status("test-endpoint_arn", )


async def test_describe_replication_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_configs()
    mock_client.call.assert_called_once()


async def test_describe_replication_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_configs()


async def test_describe_replication_instance_task_logs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_instance_task_logs("test-replication_instance_arn", )
    mock_client.call.assert_called_once()


async def test_describe_replication_instance_task_logs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_instance_task_logs("test-replication_instance_arn", )


async def test_describe_replication_subnet_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_subnet_groups()
    mock_client.call.assert_called_once()


async def test_describe_replication_subnet_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_subnet_groups()


async def test_describe_replication_table_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_table_statistics("test-replication_config_arn", )
    mock_client.call.assert_called_once()


async def test_describe_replication_table_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_table_statistics("test-replication_config_arn", )


async def test_describe_replication_task_assessment_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_task_assessment_results()
    mock_client.call.assert_called_once()


async def test_describe_replication_task_assessment_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_task_assessment_results()


async def test_describe_replication_task_assessment_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_task_assessment_runs()
    mock_client.call.assert_called_once()


async def test_describe_replication_task_assessment_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_task_assessment_runs()


async def test_describe_replication_task_individual_assessments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_task_individual_assessments()
    mock_client.call.assert_called_once()


async def test_describe_replication_task_individual_assessments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_task_individual_assessments()


async def test_describe_replications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replications()
    mock_client.call.assert_called_once()


async def test_describe_replications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replications()


async def test_describe_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_schemas("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_describe_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_schemas("test-endpoint_arn", )


async def test_export_metadata_model_assessment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", )
    mock_client.call.assert_called_once()


async def test_export_metadata_model_assessment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", )


async def test_get_target_selection_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_target_selection_rules("test-migration_project_identifier", "test-selection_rules", )
    mock_client.call.assert_called_once()


async def test_get_target_selection_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_target_selection_rules("test-migration_project_identifier", "test-selection_rules", )


async def test_import_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_certificate("test-certificate_identifier", )
    mock_client.call.assert_called_once()


async def test_import_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_certificate("test-certificate_identifier", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource()
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource()


async def test_modify_conversion_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_conversion_configuration("test-migration_project_identifier", "test-conversion_configuration", )
    mock_client.call.assert_called_once()


async def test_modify_conversion_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_conversion_configuration("test-migration_project_identifier", "test-conversion_configuration", )


async def test_modify_data_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_data_migration("test-data_migration_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_data_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_data_migration("test-data_migration_identifier", )


async def test_modify_data_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_data_provider("test-data_provider_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_data_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_data_provider("test-data_provider_identifier", )


async def test_modify_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_modify_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_event_subscription("test-subscription_name", )


async def test_modify_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_profile("test-instance_profile_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_profile("test-instance_profile_identifier", )


async def test_modify_migration_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_migration_project("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_migration_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_migration_project("test-migration_project_identifier", )


async def test_modify_replication_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_replication_config("test-replication_config_arn", )
    mock_client.call.assert_called_once()


async def test_modify_replication_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_replication_config("test-replication_config_arn", )


async def test_modify_replication_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_replication_subnet_group("test-replication_subnet_group_identifier", [], )
    mock_client.call.assert_called_once()


async def test_modify_replication_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_replication_subnet_group("test-replication_subnet_group_identifier", [], )


async def test_modify_replication_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_replication_task("test-replication_task_arn", )
    mock_client.call.assert_called_once()


async def test_modify_replication_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_replication_task("test-replication_task_arn", )


async def test_move_replication_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await move_replication_task("test-replication_task_arn", "test-target_replication_instance_arn", )
    mock_client.call.assert_called_once()


async def test_move_replication_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await move_replication_task("test-replication_task_arn", "test-target_replication_instance_arn", )


async def test_reboot_replication_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_replication_instance("test-replication_instance_arn", )
    mock_client.call.assert_called_once()


async def test_reboot_replication_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_replication_instance("test-replication_instance_arn", )


async def test_refresh_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await refresh_schemas("test-endpoint_arn", "test-replication_instance_arn", )
    mock_client.call.assert_called_once()


async def test_refresh_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await refresh_schemas("test-endpoint_arn", "test-replication_instance_arn", )


async def test_reload_replication_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await reload_replication_tables("test-replication_config_arn", [], )
    mock_client.call.assert_called_once()


async def test_reload_replication_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reload_replication_tables("test-replication_config_arn", [], )


async def test_reload_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await reload_tables("test-replication_task_arn", [], )
    mock_client.call.assert_called_once()


async def test_reload_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reload_tables("test-replication_task_arn", [], )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_arn", [], )


async def test_run_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_connection("test-replication_instance_arn", "test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_run_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_connection("test-replication_instance_arn", "test-endpoint_arn", )


async def test_run_fleet_advisor_lsa_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_fleet_advisor_lsa_analysis()
    mock_client.call.assert_called_once()


async def test_run_fleet_advisor_lsa_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_fleet_advisor_lsa_analysis()


async def test_start_data_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_data_migration("test-data_migration_identifier", "test-start_type", )
    mock_client.call.assert_called_once()


async def test_start_data_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_data_migration("test-data_migration_identifier", "test-start_type", )


async def test_start_extension_pack_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_extension_pack_association("test-migration_project_identifier", )
    mock_client.call.assert_called_once()


async def test_start_extension_pack_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_extension_pack_association("test-migration_project_identifier", )


async def test_start_metadata_model_assessment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_assessment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", )


async def test_start_metadata_model_conversion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_conversion("test-migration_project_identifier", "test-selection_rules", )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_conversion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_conversion("test-migration_project_identifier", "test-selection_rules", )


async def test_start_metadata_model_creation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_creation("test-migration_project_identifier", "test-selection_rules", "test-metadata_model_name", {}, )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_creation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_creation("test-migration_project_identifier", "test-selection_rules", "test-metadata_model_name", {}, )


async def test_start_metadata_model_export_as_script(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_export_as_script_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", )


async def test_start_metadata_model_export_to_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_export_to_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", )


async def test_start_metadata_model_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", )
    mock_client.call.assert_called_once()


async def test_start_metadata_model_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", )


async def test_start_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_recommendations("test-database_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_recommendations("test-database_id", {}, )


async def test_start_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_replication("test-replication_config_arn", "test-start_replication_type", )
    mock_client.call.assert_called_once()


async def test_start_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_replication("test-replication_config_arn", "test-start_replication_type", )


async def test_start_replication_task_assessment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_replication_task_assessment("test-replication_task_arn", )
    mock_client.call.assert_called_once()


async def test_start_replication_task_assessment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_replication_task_assessment("test-replication_task_arn", )


async def test_start_replication_task_assessment_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", )
    mock_client.call.assert_called_once()


async def test_start_replication_task_assessment_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", )


async def test_stop_data_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_data_migration("test-data_migration_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_data_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_data_migration("test-data_migration_identifier", )


async def test_stop_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_replication("test-replication_config_arn", )
    mock_client.call.assert_called_once()


async def test_stop_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_replication("test-replication_config_arn", )


async def test_update_subscriptions_to_event_bridge(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_subscriptions_to_event_bridge()
    mock_client.call.assert_called_once()


async def test_update_subscriptions_to_event_bridge_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_subscriptions_to_event_bridge()


@pytest.mark.asyncio
async def test_batch_start_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import batch_start_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await batch_start_recommendations(data="test-data", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_migration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_data_migration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_data_migration("test-migration_project_identifier", "test-data_migration_type", "test-service_access_role_arn", data_migration_name="test-data_migration_name", enable_cloudwatch_logs=True, source_data_settings={}, target_data_settings={}, number_of_jobs="test-number_of_jobs", tags=[{"Key": "k", "Value": "v"}], selection_rules="test-selection_rules", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_data_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_data_provider("test-engine", {}, data_provider_name="test-data_provider_name", description="test-description", virtual="test-virtual", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_fleet_advisor_collector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_fleet_advisor_collector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_fleet_advisor_collector("test-collector_name", "test-service_access_role_arn", "test-s3_bucket_name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instance_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_instance_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_instance_profile(availability_zone="test-availability_zone", kms_key_arn="test-kms_key_arn", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], network_type="test-network_type", instance_profile_name="test-instance_profile_name", description="test-description", subnet_group_identifier="test-subnet_group_identifier", vpc_security_groups="test-vpc_security_groups", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_migration_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_migration_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_migration_project("test-source_data_provider_descriptors", "test-target_data_provider_descriptors", "test-instance_profile_identifier", migration_project_name="test-migration_project_name", transformation_rules="test-transformation_rules", description="test-description", tags=[{"Key": "k", "Value": "v"}], schema_conversion_application_attributes="test-schema_conversion_application_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_replication_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import create_replication_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await create_replication_config({}, "test-source_endpoint_arn", "test-target_endpoint_arn", {}, "test-replication_type", {}, replication_settings={}, supplemental_settings={}, resource_identifier="test-resource_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_applicable_individual_assessments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_applicable_individual_assessments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_applicable_individual_assessments(replication_task_arn="test-replication_task_arn", replication_instance_arn="test-replication_instance_arn", replication_config_arn={}, source_engine_name="test-source_engine_name", target_engine_name="test-target_engine_name", migration_type="test-migration_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_certificates(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_data_migrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_data_migrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_data_migrations(filters=[{}], max_records=1, marker="test-marker", without_settings={}, without_statistics="test-without_statistics", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_data_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_data_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_data_providers(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_endpoint_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint_settings("test-engine_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_endpoint_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint_types(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_engine_versions(max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_event_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_event_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_extension_pack_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_extension_pack_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_extension_pack_associations("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_advisor_collectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_fleet_advisor_collectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_advisor_collectors(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_advisor_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_fleet_advisor_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_advisor_databases(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_advisor_lsa_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_fleet_advisor_lsa_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_advisor_lsa_analysis(max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_advisor_schema_object_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_fleet_advisor_schema_object_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_advisor_schema_object_summary(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_advisor_schemas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_fleet_advisor_schemas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_advisor_schemas(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_instance_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_instance_profiles(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_assessments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_assessments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_assessments("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_children_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_children
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_children("test-selection_rules", "test-migration_project_identifier", "test-origin", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_conversions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_conversions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_conversions("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_creations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_creations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_creations("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_exports_as_script_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_exports_as_script
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_exports_as_script("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_exports_to_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_exports_to_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_exports_to_target("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_metadata_model_imports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_metadata_model_imports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_metadata_model_imports("test-migration_project_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_migration_projects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_migration_projects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_migration_projects(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_orderable_replication_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_orderable_replication_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_orderable_replication_instances(max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_pending_maintenance_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_pending_maintenance_actions(replication_instance_arn="test-replication_instance_arn", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_recommendation_limitations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_recommendation_limitations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_recommendation_limitations(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_recommendations(filters=[{}], max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_configs(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_instance_task_logs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_instance_task_logs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_instance_task_logs("test-replication_instance_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_subnet_groups(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_table_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_table_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_table_statistics({}, max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_task_assessment_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_task_assessment_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_task_assessment_results(replication_task_arn="test-replication_task_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_task_assessment_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_task_assessment_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_task_assessment_runs(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_task_individual_assessments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replication_task_individual_assessments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replication_task_individual_assessments(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_replications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_replications(filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_schemas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import describe_schemas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await describe_schemas("test-endpoint_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_export_metadata_model_assessment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import export_metadata_model_assessment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await export_metadata_model_assessment("test-migration_project_identifier", "test-selection_rules", file_name="test-file_name", assessment_report_types=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import import_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await import_certificate("test-certificate_identifier", certificate_pem="test-certificate_pem", certificate_wallet="test-certificate_wallet", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource(resource_arn="test-resource_arn", resource_arn_list="test-resource_arn_list", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_data_migration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_data_migration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_data_migration("test-data_migration_identifier", data_migration_name="test-data_migration_name", enable_cloudwatch_logs=True, service_access_role_arn="test-service_access_role_arn", data_migration_type="test-data_migration_type", source_data_settings={}, target_data_settings={}, number_of_jobs="test-number_of_jobs", selection_rules="test-selection_rules", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_data_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_data_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_data_provider("test-data_provider_identifier", data_provider_name="test-data_provider_name", description="test-description", engine="test-engine", virtual="test-virtual", exact_settings={}, settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_instance_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_instance_profile("test-instance_profile_identifier", availability_zone="test-availability_zone", kms_key_arn="test-kms_key_arn", publicly_accessible="test-publicly_accessible", network_type="test-network_type", instance_profile_name="test-instance_profile_name", description="test-description", subnet_group_identifier="test-subnet_group_identifier", vpc_security_groups="test-vpc_security_groups", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_migration_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_migration_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_migration_project("test-migration_project_identifier", migration_project_name="test-migration_project_name", source_data_provider_descriptors="test-source_data_provider_descriptors", target_data_provider_descriptors="test-target_data_provider_descriptors", instance_profile_identifier="test-instance_profile_identifier", transformation_rules="test-transformation_rules", description="test-description", schema_conversion_application_attributes="test-schema_conversion_application_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_replication_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_replication_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_replication_config({}, replication_config_identifier={}, replication_type="test-replication_type", table_mappings={}, replication_settings={}, supplemental_settings={}, compute_config={}, source_endpoint_arn="test-source_endpoint_arn", target_endpoint_arn="test-target_endpoint_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_replication_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_replication_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_replication_subnet_group("test-replication_subnet_group_identifier", "test-subnet_ids", replication_subnet_group_description="test-replication_subnet_group_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_replication_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import modify_replication_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await modify_replication_task("test-replication_task_arn", replication_task_identifier="test-replication_task_identifier", migration_type="test-migration_type", table_mappings={}, replication_task_settings={}, cdc_start_time="test-cdc_start_time", cdc_start_position="test-cdc_start_position", cdc_stop_position="test-cdc_stop_position", task_data="test-task_data", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reboot_replication_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import reboot_replication_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await reboot_replication_instance("test-replication_instance_arn", force_failover=True, force_planned_failover=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reload_replication_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import reload_replication_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await reload_replication_tables({}, "test-tables_to_reload", reload_option="test-reload_option", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reload_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import reload_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await reload_tables("test-replication_task_arn", "test-tables_to_reload", reload_option="test-reload_option", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_metadata_model_export_as_script_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import start_metadata_model_export_as_script
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await start_metadata_model_export_as_script("test-migration_project_identifier", "test-selection_rules", "test-origin", file_name="test-file_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_metadata_model_export_to_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import start_metadata_model_export_to_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await start_metadata_model_export_to_target("test-migration_project_identifier", "test-selection_rules", overwrite_extension_pack="test-overwrite_extension_pack", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_metadata_model_import_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import start_metadata_model_import
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await start_metadata_model_import("test-migration_project_identifier", "test-selection_rules", "test-origin", refresh="test-refresh", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_replication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import start_replication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await start_replication({}, "test-start_replication_type", premigration_assessment_settings={}, cdc_start_time="test-cdc_start_time", cdc_start_position="test-cdc_start_position", cdc_stop_position="test-cdc_stop_position", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_replication_task_assessment_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import start_replication_task_assessment_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await start_replication_task_assessment_run("test-replication_task_arn", "test-service_access_role_arn", "test-result_location_bucket", "test-assessment_run_name", result_location_folder="test-result_location_folder", result_encryption_mode="test-result_encryption_mode", result_kms_key_arn="test-result_kms_key_arn", include_only=True, exclude="test-exclude", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_subscriptions_to_event_bridge_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dms import update_subscriptions_to_event_bridge
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dms.async_client", lambda *a, **kw: mock_client)
    await update_subscriptions_to_event_bridge(force_move=True, region_name="us-east-1")
    mock_client.call.assert_called_once()
