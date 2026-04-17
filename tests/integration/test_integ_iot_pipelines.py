"""Integration tests for aws_util.iot_pipelines against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. iot_telemetry_to_timestream
# ---------------------------------------------------------------------------


class TestIotTelemetryToTimestream:
    @pytest.mark.skip(
        reason="IoT Core/Timestream not available in LocalStack community"
    )
    def test_creates_timestream_resources_and_iot_rule(self, iam_role):
        from aws_util.iot_pipelines import iot_telemetry_to_timestream

        result = iot_telemetry_to_timestream(
            rule_name="test_telemetry_rule",
            topic_filter="factory/+/telemetry",
            database_name="test-iot-db",
            table_name="test-iot-table",
            role_arn=iam_role,
            dimensions=[{"name": "device_id", "value": "${clientId()}"}],
            region_name=REGION,
        )
        assert result.rule_name == "test_telemetry_rule"
        assert isinstance(result.rule_arn, str)
        assert result.database_name == "test-iot-db"
        assert result.table_name == "test-iot-table"
        assert isinstance(result.created_database, bool)
        assert isinstance(result.created_table, bool)


# ---------------------------------------------------------------------------
# 2. iot_device_shadow_sync
# ---------------------------------------------------------------------------


class TestIotDeviceShadowSync:
    @pytest.mark.skip(
        reason="IoT Data (device shadows) not available in LocalStack community"
    )
    def test_syncs_shadow_delta_to_dynamodb(self, dynamodb_table):
        from aws_util.iot_pipelines import iot_device_shadow_sync

        result = iot_device_shadow_sync(
            thing_name="test-sensor-001",
            table_name=dynamodb_table,
            shadow_name=None,
            region_name=REGION,
        )
        assert result.thing_name == "test-sensor-001"
        assert isinstance(result.reported_state, dict)
        assert isinstance(result.desired_state, dict)
        assert isinstance(result.delta_keys, list)
        assert isinstance(result.synced_to_dynamodb, bool)


# ---------------------------------------------------------------------------
# 3. iot_fleet_command_broadcaster
# ---------------------------------------------------------------------------


class TestIotFleetCommandBroadcaster:
    @pytest.mark.skip(reason="IoT Core not available in LocalStack community")
    def test_creates_job_and_stores_metadata(self, s3_bucket, dynamodb_table):
        from aws_util.iot_pipelines import iot_fleet_command_broadcaster

        result = iot_fleet_command_broadcaster(
            job_id="fw-update-test-001",
            thing_group_arn="arn:aws:iot:us-east-1:000000000000:thinggroup/test-group",
            command_document={"action": "update_firmware", "version": "2.0.0"},
            bucket=s3_bucket,
            table_name=dynamodb_table,
            target_selection="SNAPSHOT",
            region_name=REGION,
        )
        assert result.job_id == "fw-update-test-001"
        assert isinstance(result.job_arn, str)
        assert isinstance(result.targets_count, int)
        assert isinstance(result.document_key, str)


# ---------------------------------------------------------------------------
# 4. iot_alert_to_sns
# ---------------------------------------------------------------------------


class TestIotAlertToSns:
    @pytest.mark.skip(
        reason="IoT SiteWise not available in LocalStack community"
    )
    def test_evaluates_threshold_and_publishes_alert(self, sns_topic):
        from aws_util.iot_pipelines import iot_alert_to_sns

        result = iot_alert_to_sns(
            asset_id="test-asset-001",
            property_id="test-property-001",
            threshold_value=75.0,
            comparison="GT",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert result.asset_id == "test-asset-001"
        assert result.property_id == "test-property-001"
        assert isinstance(result.current_value, float)
        assert isinstance(result.threshold_breached, bool)
        assert result.message_id is None or isinstance(result.message_id, str)


# ---------------------------------------------------------------------------
# 5. iot_greengrass_component_deployer
# ---------------------------------------------------------------------------


class TestIotGreengrassComponentDeployer:
    @pytest.mark.skip(
        reason="Greengrass v2 not available in LocalStack community"
    )
    def test_uploads_artifact_and_deploys_component(self, s3_bucket, tmp_path):
        from aws_util.iot_pipelines import iot_greengrass_component_deployer

        # Create a dummy ZIP artifact
        artifact = tmp_path / "component.zip"
        artifact.write_bytes(b"PK\x03\x04" + b"\x00" * 100)

        result = iot_greengrass_component_deployer(
            component_name="com.example.TestSensor",
            component_version="1.0.0",
            artifact_path=str(artifact),
            bucket=s3_bucket,
            target_arn="arn:aws:iot:us-east-1:000000000000:thinggroup/test-group",
            region_name=REGION,
        )
        assert isinstance(result.component_arn, str)
        assert isinstance(result.deployment_id, str)
        assert isinstance(result.artifact_key, str)
