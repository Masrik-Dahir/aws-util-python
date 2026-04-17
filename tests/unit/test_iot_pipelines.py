"""Tests for aws_util.iot_pipelines module."""
from __future__ import annotations

import io
import json
import time
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.iot_pipelines as mod
from aws_util.iot_pipelines import (
    DeviceShadowSyncResult,
    FleetCommandResult,
    GreengrassDeployResult,
    IoTAlertResult,
    IoTTimestreamRuleResult,
    iot_alert_to_sns,
    iot_device_shadow_sync,
    iot_fleet_command_broadcaster,
    iot_greengrass_component_deployer,
    iot_telemetry_to_timestream,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_iot_timestream_rule_result(self) -> None:
        r = IoTTimestreamRuleResult(
            rule_name="r1", rule_arn="arn:r1",
            database_name="db", table_name="tbl",
            created_database=True, created_table=True,
        )
        assert r.rule_name == "r1"
        assert r.created_database is True

    def test_device_shadow_sync_result(self) -> None:
        r = DeviceShadowSyncResult(
            thing_name="thing1", reported_state={"a": 1},
            desired_state={"a": 2}, delta_keys=["a"],
            synced_to_dynamodb=True,
        )
        assert r.delta_keys == ["a"]

    def test_fleet_command_result(self) -> None:
        r = FleetCommandResult(
            job_id="j1", job_arn="arn:j1",
            targets_count=5, document_key="key",
        )
        assert r.targets_count == 5

    def test_iot_alert_result(self) -> None:
        r = IoTAlertResult(
            asset_id="a1", property_id="p1",
            current_value=75.0, threshold_breached=True,
            message_id="msg-1",
        )
        assert r.threshold_breached is True

    def test_greengrass_deploy_result(self) -> None:
        r = GreengrassDeployResult(
            component_arn="arn:gg", deployment_id="d1",
            artifact_key="s3/key",
        )
        assert r.deployment_id == "d1"


# ==================================================================
# iot_telemetry_to_timestream
# ==================================================================


class TestIotTelemetryToTimestream:
    def _build_clients(
        self,
        iot: MagicMock | None = None,
        ts_write: MagicMock | None = None,
    ) -> Any:
        _iot = iot or _mock()
        _ts = ts_write or _mock()

        def factory(service, **kw):
            if service == "iot":
                return _iot
            if service == "timestream-write":
                return _ts
            return _mock()
        return factory, _iot, _ts

    def test_success_creates_all(self, monkeypatch) -> None:
        iot = _mock()
        iot.get_topic_rule.return_value = {"ruleArn": "arn:aws:iot:rule/test"}
        ts = _mock()
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_telemetry_to_timestream(
            rule_name="test-rule",
            topic_filter="factory/+/telemetry",
            database_name="test-db",
            table_name="test-table",
            role_arn="arn:aws:iam::123:role/test",
            dimensions=[{"name": "device_id", "value": "${clientId()}"}],
            region_name=REGION,
        )
        assert result.rule_name == "test-rule"
        assert result.rule_arn == "arn:aws:iot:rule/test"
        assert result.created_database is True
        assert result.created_table is True
        ts.create_database.assert_called_once()
        ts.create_table.assert_called_once()
        iot.create_topic_rule.assert_called_once()

    def test_database_already_exists(self, monkeypatch) -> None:
        iot = _mock()
        iot.get_topic_rule.return_value = {"ruleArn": "arn:rule"}
        ts = _mock()
        ts.create_database.side_effect = _client_error("ConflictException")
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_telemetry_to_timestream(
            rule_name="r", topic_filter="t", database_name="db",
            table_name="tbl", role_arn="arn:role",
            dimensions=[],
            region_name=REGION,
        )
        assert result.created_database is False

    def test_database_resource_already_exists(self, monkeypatch) -> None:
        iot = _mock()
        iot.get_topic_rule.return_value = {"ruleArn": "arn:rule"}
        ts = _mock()
        ts.create_database.side_effect = _client_error("ResourceAlreadyExistsException")
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_telemetry_to_timestream(
            rule_name="r", topic_filter="t", database_name="db",
            table_name="tbl", role_arn="arn:role", dimensions=[],
            region_name=REGION,
        )
        assert result.created_database is False

    def test_database_create_error(self, monkeypatch) -> None:
        ts = _mock()
        ts.create_database.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_telemetry_to_timestream(
                rule_name="r", topic_filter="t", database_name="db",
                table_name="tbl", role_arn="arn:role", dimensions=[],
                region_name=REGION,
            )

    def test_table_already_exists(self, monkeypatch) -> None:
        iot = _mock()
        iot.get_topic_rule.return_value = {"ruleArn": "arn:rule"}
        ts = _mock()
        ts.create_table.side_effect = _client_error("ConflictException")
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_telemetry_to_timestream(
            rule_name="r", topic_filter="t", database_name="db",
            table_name="tbl", role_arn="arn:role", dimensions=[],
            region_name=REGION,
        )
        assert result.created_table is False

    def test_table_create_error(self, monkeypatch) -> None:
        ts = _mock()
        ts.create_table.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_telemetry_to_timestream(
                rule_name="r", topic_filter="t", database_name="db",
                table_name="tbl", role_arn="arn:role", dimensions=[],
                region_name=REGION,
            )

    def test_rule_already_exists_replaced(self, monkeypatch) -> None:
        iot = _mock()
        iot.create_topic_rule.side_effect = _client_error("ResourceAlreadyExistsException")
        iot.get_topic_rule.return_value = {"ruleArn": "arn:rule"}
        ts = _mock()
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_telemetry_to_timestream(
            rule_name="r", topic_filter="t", database_name="db",
            table_name="tbl", role_arn="arn:role", dimensions=[],
            region_name=REGION,
        )
        iot.replace_topic_rule.assert_called_once()
        assert result.rule_arn == "arn:rule"

    def test_rule_conflict_replace_fails(self, monkeypatch) -> None:
        iot = _mock()
        iot.create_topic_rule.side_effect = _client_error("ConflictException")
        iot.replace_topic_rule.side_effect = _client_error("InternalServerError")
        ts = _mock()
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_telemetry_to_timestream(
                rule_name="r", topic_filter="t", database_name="db",
                table_name="tbl", role_arn="arn:role", dimensions=[],
                region_name=REGION,
            )

    def test_rule_create_other_error(self, monkeypatch) -> None:
        iot = _mock()
        iot.create_topic_rule.side_effect = _client_error("InternalServerError")
        ts = _mock()
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_telemetry_to_timestream(
                rule_name="r", topic_filter="t", database_name="db",
                table_name="tbl", role_arn="arn:role", dimensions=[],
                region_name=REGION,
            )

    def test_get_topic_rule_error(self, monkeypatch) -> None:
        iot = _mock()
        iot.get_topic_rule.side_effect = _client_error("ResourceNotFoundException")
        ts = _mock()
        factory, _, _ = self._build_clients(iot=iot, ts_write=ts)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_telemetry_to_timestream(
                rule_name="r", topic_filter="t", database_name="db",
                table_name="tbl", role_arn="arn:role", dimensions=[],
                region_name=REGION,
            )


# ==================================================================
# iot_device_shadow_sync
# ==================================================================


class TestIotDeviceShadowSync:
    def _build_clients(
        self,
        iot_data: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _iot_data = iot_data or _mock()
        _ddb = ddb or _mock()

        def factory(service, **kw):
            if service == "iot-data":
                return _iot_data
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _iot_data, _ddb

    def _shadow_response(self, reported: dict, desired: dict, version: int = 1) -> dict:
        payload = json.dumps({
            "state": {"reported": reported, "desired": desired},
            "version": version,
        }).encode()
        return {"payload": io.BytesIO(payload)}

    def test_success_with_delta(self, monkeypatch) -> None:
        iot_data = _mock()
        iot_data.get_thing_shadow.return_value = self._shadow_response(
            reported={"temp": 20, "mode": "auto"},
            desired={"temp": 25},
        )
        ddb = _mock()
        factory, _, _ = self._build_clients(iot_data=iot_data, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_device_shadow_sync(
            thing_name="sensor-1",
            table_name="shadow-table",
            region_name=REGION,
        )
        assert result.thing_name == "sensor-1"
        assert result.reported_state == {"temp": 20, "mode": "auto"}
        assert result.desired_state == {"temp": 25}
        assert "temp" in result.delta_keys
        assert "mode" in result.delta_keys  # in reported but not desired
        assert result.synced_to_dynamodb is True
        ddb.put_item.assert_called_once()

    def test_success_no_delta(self, monkeypatch) -> None:
        iot_data = _mock()
        iot_data.get_thing_shadow.return_value = self._shadow_response(
            reported={"temp": 25}, desired={"temp": 25},
        )
        factory, _, ddb = self._build_clients(iot_data=iot_data)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_device_shadow_sync(
            thing_name="sensor-1", table_name="t", region_name=REGION,
        )
        assert result.delta_keys == []

    def test_named_shadow(self, monkeypatch) -> None:
        iot_data = _mock()
        iot_data.get_thing_shadow.return_value = self._shadow_response(
            reported={}, desired={"a": 1},
        )
        factory, _, ddb = self._build_clients(iot_data=iot_data)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_device_shadow_sync(
            thing_name="thing-1", table_name="t",
            shadow_name="config", region_name=REGION,
        )
        assert result.delta_keys == ["a"]
        # Verify shadowName was passed
        call_kwargs = iot_data.get_thing_shadow.call_args[1]
        assert call_kwargs.get("shadowName") == "config"

    def test_shadow_read_error(self, monkeypatch) -> None:
        iot_data = _mock()
        iot_data.get_thing_shadow.side_effect = _client_error("ResourceNotFoundException")
        factory, _, _ = self._build_clients(iot_data=iot_data)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_device_shadow_sync(
                thing_name="thing-1", table_name="t", region_name=REGION,
            )

    def test_ddb_write_error(self, monkeypatch) -> None:
        iot_data = _mock()
        iot_data.get_thing_shadow.return_value = self._shadow_response(
            reported={}, desired={},
        )
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(iot_data=iot_data, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_device_shadow_sync(
                thing_name="thing-1", table_name="t", region_name=REGION,
            )

    def test_shadow_payload_as_bytes(self, monkeypatch) -> None:
        """Test that raw bytes payload (no .read() method) is handled."""
        iot_data = _mock()
        payload_bytes = json.dumps({
            "state": {"reported": {"a": 1}, "desired": {"a": 2}},
            "version": 5,
        }).encode()
        iot_data.get_thing_shadow.return_value = {"payload": payload_bytes}
        factory, _, ddb = self._build_clients(iot_data=iot_data)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_device_shadow_sync(
            thing_name="t1", table_name="tbl", region_name=REGION,
        )
        assert result.delta_keys == ["a"]


# ==================================================================
# iot_fleet_command_broadcaster
# ==================================================================


class TestIotFleetCommandBroadcaster:
    def _build_clients(
        self,
        iot: MagicMock | None = None,
        s3: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _iot = iot or _mock()
        _s3 = s3 or _mock()
        _ddb = ddb or _mock()

        def factory(service, **kw):
            if service == "iot":
                return _iot
            if service == "s3":
                return _s3
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _iot, _s3, _ddb

    def test_success(self, monkeypatch) -> None:
        iot = _mock()
        iot.search_index.return_value = {"things": [{"thingName": "t1"}, {"thingName": "t2"}]}
        iot.create_job.return_value = {"jobArn": "arn:aws:iot:job/j1"}
        factory, _, s3, ddb = self._build_clients(iot=iot)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_fleet_command_broadcaster(
            job_id="j1",
            thing_group_arn="arn:aws:iot:us-east-1:123:thinggroup/fleet",
            command_document={"action": "update"},
            bucket="cmd-bucket",
            table_name="job-table",
            region_name=REGION,
        )
        assert result.job_id == "j1"
        assert result.job_arn == "arn:aws:iot:job/j1"
        assert result.targets_count == 2
        assert "iot-jobs/j1/document.json" in result.document_key
        s3.put_object.assert_called_once()
        ddb.put_item.assert_called_once()

    def test_invalid_target_selection(self) -> None:
        with pytest.raises(ValueError, match="target_selection"):
            iot_fleet_command_broadcaster(
                job_id="j1",
                thing_group_arn="arn:group",
                command_document={},
                bucket="b",
                table_name="t",
                target_selection="INVALID",
            )

    def test_continuous_target_selection(self, monkeypatch) -> None:
        iot = _mock()
        iot.search_index.return_value = {"things": []}
        iot.create_job.return_value = {"jobArn": "arn:job"}
        factory, _, _, _ = self._build_clients(iot=iot)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_fleet_command_broadcaster(
            job_id="j1",
            thing_group_arn="arn:aws:iot:us-east-1:123:thinggroup/fleet",
            command_document={},
            bucket="b",
            table_name="t",
            target_selection="CONTINUOUS",
            region_name=REGION,
        )
        assert result.targets_count == 0

    def test_s3_upload_error(self, monkeypatch) -> None:
        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        factory, _, _, _ = self._build_clients(s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_fleet_command_broadcaster(
                job_id="j1",
                thing_group_arn="arn:group",
                command_document={},
                bucket="b",
                table_name="t",
                region_name=REGION,
            )

    def test_search_index_error_falls_back(self, monkeypatch) -> None:
        iot = _mock()
        iot.search_index.side_effect = _client_error("ResourceNotFoundException")
        iot.create_job.return_value = {"jobArn": "arn:job"}
        factory, _, _, _ = self._build_clients(iot=iot)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_fleet_command_broadcaster(
            job_id="j1",
            thing_group_arn="arn:aws:iot:us-east-1:123:thinggroup/fleet",
            command_document={},
            bucket="b",
            table_name="t",
            region_name=REGION,
        )
        assert result.targets_count == 0

    def test_create_job_error(self, monkeypatch) -> None:
        iot = _mock()
        iot.search_index.return_value = {"things": []}
        iot.create_job.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(iot=iot)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_fleet_command_broadcaster(
                job_id="j1",
                thing_group_arn="arn:group",
                command_document={},
                bucket="b",
                table_name="t",
                region_name=REGION,
            )

    def test_ddb_metadata_error(self, monkeypatch) -> None:
        iot = _mock()
        iot.search_index.return_value = {"things": []}
        iot.create_job.return_value = {"jobArn": "arn:job"}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(iot=iot, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_fleet_command_broadcaster(
                job_id="j1",
                thing_group_arn="arn:group",
                command_document={},
                bucket="b",
                table_name="t",
                region_name=REGION,
            )


# ==================================================================
# iot_alert_to_sns
# ==================================================================


class TestIotAlertToSns:
    def _build_clients(
        self,
        sitewise: MagicMock | None = None,
        sns: MagicMock | None = None,
    ) -> Any:
        _sw = sitewise or _mock()
        _sns = sns or _mock()

        def factory(service, **kw):
            if service == "iotsitewise":
                return _sw
            if service == "sns":
                return _sns
            return _mock()
        return factory, _sw, _sns

    def _property_response(self, value: float) -> dict:
        return {
            "propertyValue": {
                "value": {"doubleValue": value},
                "timestamp": {"timeInSeconds": int(time.time())},
            }
        }

    def test_threshold_breached_gt(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(80.0)
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-1"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=70.0, comparison="GT",
            sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
            region_name=REGION,
        )
        assert result.threshold_breached is True
        assert result.current_value == 80.0
        assert result.message_id == "msg-1"
        sns.publish.assert_called_once()

    def test_threshold_not_breached_gt(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(50.0)
        sns = _mock()
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=70.0, comparison="GT",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.threshold_breached is False
        assert result.message_id is None
        sns.publish.assert_not_called()

    def test_threshold_lt(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(10.0)
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-2"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=20.0, comparison="LT",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.threshold_breached is True

    def test_threshold_gte(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(70.0)
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-3"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=70.0, comparison="GTE",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.threshold_breached is True

    def test_threshold_lte(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(70.0)
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-4"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=70.0, comparison="LTE",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.threshold_breached is True

    def test_invalid_comparison(self) -> None:
        with pytest.raises(ValueError, match="comparison must be one of"):
            iot_alert_to_sns(
                asset_id="a1", property_id="p1",
                threshold_value=70.0, comparison="EQ",
                sns_topic_arn="arn:topic",
            )

    def test_lowercase_comparison(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(80.0)
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-5"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=70.0, comparison="gt",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.threshold_breached is True

    def test_sitewise_error(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.side_effect = _client_error("ResourceNotFoundException")
        factory, _, _ = self._build_clients(sitewise=sw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_alert_to_sns(
                asset_id="a1", property_id="p1",
                threshold_value=70.0, comparison="GT",
                sns_topic_arn="arn:topic",
                region_name=REGION,
            )

    def test_sns_publish_error(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = self._property_response(80.0)
        sns = _mock()
        sns.publish.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_alert_to_sns(
                asset_id="a1", property_id="p1",
                threshold_value=70.0, comparison="GT",
                sns_topic_arn="arn:topic",
                region_name=REGION,
            )

    def test_integer_value_property(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = {
            "propertyValue": {"value": {"integerValue": 42}}
        }
        sns = _mock()
        sns.publish.return_value = {"MessageId": "msg-int"}
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=50.0, comparison="LT",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.current_value == 42.0
        assert result.threshold_breached is True

    def test_string_value_property(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = {
            "propertyValue": {"value": {"stringValue": "abc"}}
        }
        sns = _mock()
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        # 0.0 > 50.0 is False, so no SNS publish
        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=50.0, comparison="GT",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        # non-numeric string => 0.0
        assert result.current_value == 0.0
        assert result.threshold_breached is False

    def test_empty_value(self, monkeypatch) -> None:
        sw = _mock()
        sw.get_asset_property_value.return_value = {
            "propertyValue": {"value": {}}
        }
        sns = _mock()
        factory, _, _ = self._build_clients(sitewise=sw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        # 0.0 > 50.0 is False, so no SNS publish
        result = iot_alert_to_sns(
            asset_id="a1", property_id="p1",
            threshold_value=50.0, comparison="GT",
            sns_topic_arn="arn:topic",
            region_name=REGION,
        )
        assert result.current_value == 0.0
        assert result.threshold_breached is False


# ==================================================================
# iot_greengrass_component_deployer
# ==================================================================


class TestIotGreengrassComponentDeployer:
    def _build_clients(
        self,
        s3: MagicMock | None = None,
        gg: MagicMock | None = None,
    ) -> Any:
        _s3 = s3 or _mock()
        _gg = gg or _mock()

        def factory(service, **kw):
            if service == "s3":
                return _s3
            if service == "greengrassv2":
                return _gg
            return _mock()
        return factory, _s3, _gg

    def test_success(self, monkeypatch, tmp_path) -> None:
        artifact = tmp_path / "artifact.zip"
        artifact.write_bytes(b"PK\x03\x04fake-zip-content")

        gg = _mock()
        gg.create_component_version.return_value = {"arn": "arn:aws:greengrass:comp"}
        gg.create_deployment.return_value = {"deploymentId": "deploy-1"}
        factory, s3, _ = self._build_clients(gg=gg)
        monkeypatch.setattr(mod, "get_client", factory)

        result = iot_greengrass_component_deployer(
            component_name="com.example.Sensor",
            component_version="1.0.0",
            artifact_path=str(artifact),
            bucket="gg-bucket",
            target_arn="arn:aws:iot:thing/core-device",
            region_name=REGION,
        )
        assert result.component_arn == "arn:aws:greengrass:comp"
        assert result.deployment_id == "deploy-1"
        assert "artifact.zip" in result.artifact_key
        s3.put_object.assert_called_once()

    def test_artifact_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="Artifact not found"):
            iot_greengrass_component_deployer(
                component_name="comp",
                component_version="1.0.0",
                artifact_path="/nonexistent/artifact.zip",
                bucket="b",
                target_arn="arn:target",
            )

    def test_s3_upload_error(self, monkeypatch, tmp_path) -> None:
        artifact = tmp_path / "artifact.zip"
        artifact.write_bytes(b"content")

        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        factory, _, _ = self._build_clients(s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_greengrass_component_deployer(
                component_name="comp",
                component_version="1.0.0",
                artifact_path=str(artifact),
                bucket="b",
                target_arn="arn:target",
                region_name=REGION,
            )

    def test_create_component_error(self, monkeypatch, tmp_path) -> None:
        artifact = tmp_path / "artifact.zip"
        artifact.write_bytes(b"content")

        gg = _mock()
        gg.create_component_version.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(gg=gg)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_greengrass_component_deployer(
                component_name="comp",
                component_version="1.0.0",
                artifact_path=str(artifact),
                bucket="b",
                target_arn="arn:target",
                region_name=REGION,
            )

    def test_create_deployment_error(self, monkeypatch, tmp_path) -> None:
        artifact = tmp_path / "artifact.zip"
        artifact.write_bytes(b"content")

        gg = _mock()
        gg.create_component_version.return_value = {"arn": "arn:comp"}
        gg.create_deployment.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(gg=gg)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            iot_greengrass_component_deployer(
                component_name="comp",
                component_version="1.0.0",
                artifact_path=str(artifact),
                bucket="b",
                target_arn="arn:target",
                region_name=REGION,
            )
