"""Tests for aws_util.timestream_write module."""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.timestream_write as tw_mod
from aws_util.timestream_write import (
    DatabaseDescription,
    MagneticStoreWriteProperties,
    Record,
    RetentionProperties,
    TableDescription,
    WriteRecordsResult,
    create_database,
    create_table,
    delete_database,
    delete_table,
    describe_database,
    describe_table,
    list_databases,
    list_tables,
    update_database,
    update_table,
    write_records,
    _build_record,
    _parse_database,
    _parse_table,
    create_batch_load_task,
    describe_batch_load_task,
    describe_endpoints,
    list_batch_load_tasks,
    list_tags_for_resource,
    resume_batch_load_task,
    tag_resource,
    untag_resource,
)

REGION = "us-east-1"
DB_NAME = "mydb"
TABLE_NAME = "mytable"
KMS_KEY = "arn:aws:kms:us-east-1:123:key/abc"
SQ_ARN = "arn:aws:timestream:us-east-1:123:scheduled-query/sq1"


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _client_error(
    code: str = "ClientException",
    msg: str = "error",
    op: str = "Op",
) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, op
    )


def _db_dict(**kwargs: object) -> dict:
    defaults: dict = {
        "DatabaseName": DB_NAME,
        "Arn": "arn:aws:timestream:us-east-1:123:database/mydb",
        "TableCount": 3,
        "KmsKeyId": KMS_KEY,
        "CreationTime": "2024-01-01T00:00:00Z",
        "LastUpdatedTime": "2024-06-01T00:00:00Z",
    }
    defaults.update(kwargs)
    return defaults


def _table_dict(**kwargs: object) -> dict:
    defaults: dict = {
        "DatabaseName": DB_NAME,
        "TableName": TABLE_NAME,
        "Arn": "arn:aws:timestream:us-east-1:123:database/mydb/table/mytable",
        "TableStatus": "ACTIVE",
        "RetentionProperties": {
            "MemoryStoreRetentionPeriodInHours": 48,
            "MagneticStoreRetentionPeriodInDays": 365,
        },
        "MagneticStoreWriteProperties": {
            "EnableMagneticStoreWrites": True,
        },
        "CreationTime": "2024-01-01T00:00:00Z",
        "LastUpdatedTime": "2024-06-01T00:00:00Z",
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_retention_properties_defaults(self) -> None:
        rp = RetentionProperties()
        assert rp.memory_store_retention_period_in_hours == 24
        assert rp.magnetic_store_retention_period_in_days == 73000

    def test_magnetic_store_write_properties_defaults(self) -> None:
        mp = MagneticStoreWriteProperties()
        assert mp.enable_magnetic_store_writes is False

    def test_database_description_defaults(self) -> None:
        db = DatabaseDescription(database_name=DB_NAME)
        assert db.database_name == DB_NAME
        assert db.arn is None
        assert db.table_count == 0
        assert db.kms_key_id is None
        assert db.creation_time is None
        assert db.last_updated_time is None

    def test_database_description_full(self) -> None:
        db = DatabaseDescription(
            database_name=DB_NAME,
            arn="arn:db",
            table_count=5,
            kms_key_id=KMS_KEY,
            creation_time="2024-01-01",
            last_updated_time="2024-06-01",
        )
        assert db.table_count == 5
        assert db.kms_key_id == KMS_KEY

    def test_table_description_defaults(self) -> None:
        td = TableDescription(
            database_name=DB_NAME, table_name=TABLE_NAME
        )
        assert td.arn is None
        assert td.table_status is None
        assert td.retention_properties is None
        assert td.magnetic_store_write_properties is None

    def test_table_description_full(self) -> None:
        td = TableDescription(
            database_name=DB_NAME,
            table_name=TABLE_NAME,
            arn="arn:table",
            table_status="ACTIVE",
            retention_properties=RetentionProperties(
                memory_store_retention_period_in_hours=48,
            ),
            magnetic_store_write_properties=MagneticStoreWriteProperties(
                enable_magnetic_store_writes=True,
            ),
            creation_time="2024-01-01",
            last_updated_time="2024-06-01",
        )
        assert td.table_status == "ACTIVE"
        assert td.retention_properties is not None
        assert td.retention_properties.memory_store_retention_period_in_hours == 48

    def test_record_defaults(self) -> None:
        rec = Record()
        assert rec.dimensions == []
        assert rec.measure_name is None
        assert rec.measure_value is None
        assert rec.measure_value_type is None
        assert rec.time is None
        assert rec.time_unit is None
        assert rec.measure_values is None
        assert rec.version is None

    def test_record_full(self) -> None:
        rec = Record(
            dimensions=[{"Name": "host", "Value": "web1"}],
            measure_name="cpu",
            measure_value="80.5",
            measure_value_type="DOUBLE",
            time="1234567890",
            time_unit="SECONDS",
            measure_values=[{"Name": "m", "Value": "1", "Type": "DOUBLE"}],
            version=1,
        )
        assert rec.measure_name == "cpu"
        assert rec.version == 1

    def test_write_records_result_defaults(self) -> None:
        wr = WriteRecordsResult()
        assert wr.records_ingested_total == 0
        assert wr.records_ingested_memory_store == 0
        assert wr.records_ingested_magnetic_store == 0


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_database(self) -> None:
        result = _parse_database(_db_dict())
        assert result.database_name == DB_NAME
        assert result.table_count == 3
        assert result.kms_key_id == KMS_KEY
        assert result.creation_time is not None
        assert result.last_updated_time is not None

    def test_parse_database_minimal(self) -> None:
        result = _parse_database({"DatabaseName": DB_NAME})
        assert result.database_name == DB_NAME
        assert result.arn is None
        assert result.table_count == 0
        assert result.creation_time is None

    def test_parse_database_empty(self) -> None:
        result = _parse_database({})
        assert result.database_name == ""

    def test_parse_table(self) -> None:
        result = _parse_table(_table_dict())
        assert result.table_name == TABLE_NAME
        assert result.table_status == "ACTIVE"
        assert result.retention_properties is not None
        assert (
            result.retention_properties.memory_store_retention_period_in_hours
            == 48
        )
        assert result.magnetic_store_write_properties is not None
        assert (
            result.magnetic_store_write_properties.enable_magnetic_store_writes
            is True
        )

    def test_parse_table_minimal(self) -> None:
        result = _parse_table(
            {"DatabaseName": DB_NAME, "TableName": TABLE_NAME}
        )
        assert result.retention_properties is None
        assert result.magnetic_store_write_properties is None
        assert result.creation_time is None

    def test_parse_table_empty(self) -> None:
        result = _parse_table({})
        assert result.database_name == ""
        assert result.table_name == ""

    def test_build_record_from_dict(self) -> None:
        raw = {"MeasureName": "cpu", "MeasureValue": "50"}
        assert _build_record(raw) is raw

    def test_build_record_from_model(self) -> None:
        rec = Record(
            dimensions=[{"Name": "host", "Value": "web1"}],
            measure_name="cpu",
            measure_value="80.5",
            measure_value_type="DOUBLE",
            time="123",
            time_unit="SECONDS",
            measure_values=[{"Name": "m", "Value": "1"}],
            version=2,
        )
        built = _build_record(rec)
        assert built["MeasureName"] == "cpu"
        assert built["MeasureValue"] == "80.5"
        assert built["MeasureValueType"] == "DOUBLE"
        assert built["Time"] == "123"
        assert built["TimeUnit"] == "SECONDS"
        assert built["MeasureValues"] == [{"Name": "m", "Value": "1"}]
        assert built["Version"] == 2
        assert len(built["Dimensions"]) == 1

    def test_build_record_empty_model(self) -> None:
        rec = Record()
        built = _build_record(rec)
        # No keys set because all fields are None / empty
        assert "MeasureName" not in built
        assert "Dimensions" not in built


# ---------------------------------------------------------------------------
# create_database
# ---------------------------------------------------------------------------


class TestCreateDatabase:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_database.return_value = {
            "Database": _db_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_database(DB_NAME, region_name=REGION)
        assert isinstance(result, DatabaseDescription)
        assert result.database_name == DB_NAME

    def test_with_kms_and_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_database.return_value = {
            "Database": _db_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        tags = [{"Key": "env", "Value": "prod"}]
        create_database(
            DB_NAME,
            kms_key_id=KMS_KEY,
            tags=tags,
            region_name=REGION,
        )
        call_kwargs = mock_client.create_database.call_args[1]
        assert call_kwargs["KmsKeyId"] == KMS_KEY
        assert call_kwargs["Tags"] == tags

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_database.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="create_database failed"):
            create_database(DB_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_database
# ---------------------------------------------------------------------------


class TestDescribeDatabase:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_database.return_value = {
            "Database": _db_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = describe_database(DB_NAME, region_name=REGION)
        assert result.database_name == DB_NAME

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_database.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="describe_database failed"
        ):
            describe_database(DB_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# list_databases
# ---------------------------------------------------------------------------


class TestListDatabases:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_databases.return_value = {
            "Databases": [_db_dict()],
            "NextToken": "tok2",
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        dbs, token = list_databases(region_name=REGION)
        assert len(dbs) == 1
        assert token == "tok2"

    def test_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_databases.return_value = {"Databases": []}
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        dbs, token = list_databases(
            max_results=10,
            next_token="tok",
            region_name=REGION,
        )
        assert dbs == []
        assert token is None
        call_kwargs = mock_client.list_databases.call_args[1]
        assert call_kwargs["MaxResults"] == 10
        assert call_kwargs["NextToken"] == "tok"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_databases.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="list_databases failed"):
            list_databases(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_database
# ---------------------------------------------------------------------------


class TestDeleteDatabase:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.delete_database.return_value = {}
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        assert delete_database(DB_NAME, region_name=REGION) is True

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.delete_database.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="delete_database failed"
        ):
            delete_database(DB_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# update_database
# ---------------------------------------------------------------------------


class TestUpdateDatabase:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.update_database.return_value = {
            "Database": _db_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = update_database(
            DB_NAME, kms_key_id=KMS_KEY, region_name=REGION
        )
        assert result.database_name == DB_NAME

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.update_database.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="update_database failed"
        ):
            update_database(
                DB_NAME, kms_key_id=KMS_KEY, region_name=REGION
            )


# ---------------------------------------------------------------------------
# create_table
# ---------------------------------------------------------------------------


class TestCreateTable:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_table.return_value = {
            "Table": _table_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_table(
            DB_NAME, TABLE_NAME, region_name=REGION
        )
        assert isinstance(result, TableDescription)
        assert result.table_name == TABLE_NAME

    def test_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_table.return_value = {
            "Table": _table_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        ret_props = {"MemoryStoreRetentionPeriodInHours": 48}
        mag_props = {"EnableMagneticStoreWrites": True}
        tags = [{"Key": "env", "Value": "prod"}]
        create_table(
            DB_NAME,
            TABLE_NAME,
            retention_properties=ret_props,
            magnetic_store_write_properties=mag_props,
            tags=tags,
            region_name=REGION,
        )
        call_kwargs = mock_client.create_table.call_args[1]
        assert call_kwargs["RetentionProperties"] == ret_props
        assert call_kwargs["MagneticStoreWriteProperties"] == mag_props
        assert call_kwargs["Tags"] == tags

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.create_table.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="create_table failed"):
            create_table(
                DB_NAME, TABLE_NAME, region_name=REGION
            )


# ---------------------------------------------------------------------------
# describe_table
# ---------------------------------------------------------------------------


class TestDescribeTable:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_table.return_value = {
            "Table": _table_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = describe_table(
            DB_NAME, TABLE_NAME, region_name=REGION
        )
        assert result.table_name == TABLE_NAME

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_table.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="describe_table failed"
        ):
            describe_table(
                DB_NAME, TABLE_NAME, region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_tables
# ---------------------------------------------------------------------------


class TestListTables:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_tables.return_value = {
            "Tables": [_table_dict()],
            "NextToken": "tok2",
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        tables, token = list_tables(region_name=REGION)
        assert len(tables) == 1
        assert token == "tok2"

    def test_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_tables.return_value = {"Tables": []}
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        tables, token = list_tables(
            database_name=DB_NAME,
            max_results=5,
            next_token="tok",
            region_name=REGION,
        )
        assert tables == []
        assert token is None
        call_kwargs = mock_client.list_tables.call_args[1]
        assert call_kwargs["DatabaseName"] == DB_NAME
        assert call_kwargs["MaxResults"] == 5
        assert call_kwargs["NextToken"] == "tok"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_tables.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="list_tables failed"):
            list_tables(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_table
# ---------------------------------------------------------------------------


class TestDeleteTable:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.delete_table.return_value = {}
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        assert delete_table(
            DB_NAME, TABLE_NAME, region_name=REGION
        ) is True

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.delete_table.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="delete_table failed"
        ):
            delete_table(
                DB_NAME, TABLE_NAME, region_name=REGION
            )


# ---------------------------------------------------------------------------
# update_table
# ---------------------------------------------------------------------------


class TestUpdateTable:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.update_table.return_value = {
            "Table": _table_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = update_table(
            DB_NAME, TABLE_NAME, region_name=REGION
        )
        assert result.table_name == TABLE_NAME

    def test_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.update_table.return_value = {
            "Table": _table_dict()
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        ret_props = {"MemoryStoreRetentionPeriodInHours": 96}
        mag_props = {"EnableMagneticStoreWrites": False}
        update_table(
            DB_NAME,
            TABLE_NAME,
            retention_properties=ret_props,
            magnetic_store_write_properties=mag_props,
            region_name=REGION,
        )
        call_kwargs = mock_client.update_table.call_args[1]
        assert call_kwargs["RetentionProperties"] == ret_props
        assert call_kwargs["MagneticStoreWriteProperties"] == mag_props

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.update_table.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="update_table failed"
        ):
            update_table(
                DB_NAME, TABLE_NAME, region_name=REGION
            )


# ---------------------------------------------------------------------------
# write_records
# ---------------------------------------------------------------------------


class TestWriteRecords:
    def test_success_with_dict_records(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.write_records.return_value = {
            "RecordsIngested": {
                "Total": 5,
                "MemoryStore": 3,
                "MagneticStore": 2,
            },
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        records: list[dict[str, Any]] = [
            {"MeasureName": "cpu", "MeasureValue": "80"}
        ]
        result = write_records(
            DB_NAME, TABLE_NAME, records, region_name=REGION
        )
        assert isinstance(result, WriteRecordsResult)
        assert result.records_ingested_total == 5
        assert result.records_ingested_memory_store == 3
        assert result.records_ingested_magnetic_store == 2

    def test_success_with_model_records(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.write_records.return_value = {
            "RecordsIngested": {"Total": 1},
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        records = [
            Record(
                measure_name="cpu",
                measure_value="50",
                measure_value_type="DOUBLE",
            )
        ]
        result = write_records(
            DB_NAME, TABLE_NAME, records, region_name=REGION
        )
        assert result.records_ingested_total == 1

    def test_with_common_attributes(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.write_records.return_value = {
            "RecordsIngested": {"Total": 1},
        }
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        common = Record(
            dimensions=[{"Name": "region", "Value": "us-east-1"}],
        )
        records: list[dict[str, Any]] = [{"MeasureName": "cpu"}]
        write_records(
            DB_NAME,
            TABLE_NAME,
            records,
            common_attributes=common,
            region_name=REGION,
        )
        call_kwargs = mock_client.write_records.call_args[1]
        assert "CommonAttributes" in call_kwargs

    def test_empty_ingested_response(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.write_records.return_value = {}
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = write_records(
            DB_NAME,
            TABLE_NAME,
            [{"MeasureName": "cpu"}],
            region_name=REGION,
        )
        assert result.records_ingested_total == 0

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.write_records.side_effect = _client_error()
        monkeypatch.setattr(
            tw_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="write_records failed"):
            write_records(
                DB_NAME,
                TABLE_NAME,
                [{"MeasureName": "cpu"}],
                region_name=REGION,
            )


def test_create_batch_load_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_load_task.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    create_batch_load_task({}, {}, "test-target_database_name", "test-target_table_name", region_name=REGION)
    mock_client.create_batch_load_task.assert_called_once()


def test_create_batch_load_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_batch_load_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_batch_load_task",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create batch load task"):
        create_batch_load_task({}, {}, "test-target_database_name", "test-target_table_name", region_name=REGION)


def test_describe_batch_load_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_load_task.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    describe_batch_load_task("test-task_id", region_name=REGION)
    mock_client.describe_batch_load_task.assert_called_once()


def test_describe_batch_load_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_batch_load_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_batch_load_task",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe batch load task"):
        describe_batch_load_task("test-task_id", region_name=REGION)


def test_describe_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    describe_endpoints(region_name=REGION)
    mock_client.describe_endpoints.assert_called_once()


def test_describe_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoints",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoints"):
        describe_endpoints(region_name=REGION)


def test_list_batch_load_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_load_tasks.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    list_batch_load_tasks(region_name=REGION)
    mock_client.list_batch_load_tasks.assert_called_once()


def test_list_batch_load_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_batch_load_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_batch_load_tasks",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list batch load tasks"):
        list_batch_load_tasks(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_resume_batch_load_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_batch_load_task.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    resume_batch_load_task("test-task_id", region_name=REGION)
    mock_client.resume_batch_load_task.assert_called_once()


def test_resume_batch_load_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_batch_load_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_batch_load_task",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume batch load task"):
        resume_batch_load_task("test-task_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_create_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import create_database
    mock_client = MagicMock()
    mock_client.create_database.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    create_database("test-database_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_database.assert_called_once()

def test_list_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import list_databases
    mock_client = MagicMock()
    mock_client.list_databases.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    list_databases(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_databases.assert_called_once()

def test_create_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import create_table
    mock_client = MagicMock()
    mock_client.create_table.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    create_table("test-database_name", "test-table_name", retention_properties={}, magnetic_store_write_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_table.assert_called_once()

def test_list_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import list_tables
    mock_client = MagicMock()
    mock_client.list_tables.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    list_tables(database_name="test-database_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tables.assert_called_once()

def test_update_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import update_table
    mock_client = MagicMock()
    mock_client.update_table.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    update_table("test-database_name", "test-table_name", retention_properties={}, magnetic_store_write_properties={}, region_name="us-east-1")
    mock_client.update_table.assert_called_once()

def test_create_batch_load_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import create_batch_load_task
    mock_client = MagicMock()
    mock_client.create_batch_load_task.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    create_batch_load_task({}, 1, "test-target_database_name", "test-target_table_name", client_token="test-client_token", data_model_configuration={}, record_version="test-record_version", region_name="us-east-1")
    mock_client.create_batch_load_task.assert_called_once()

def test_list_batch_load_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_write import list_batch_load_tasks
    mock_client = MagicMock()
    mock_client.list_batch_load_tasks.return_value = {}
    monkeypatch.setattr("aws_util.timestream_write.get_client", lambda *a, **kw: mock_client)
    list_batch_load_tasks(next_token="test-next_token", max_results=1, task_status="test-task_status", region_name="us-east-1")
    mock_client.list_batch_load_tasks.assert_called_once()
