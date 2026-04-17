"""Tests for aws_util.keyspaces -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.keyspaces import (
    KeyspaceResult,
    TableResult,
    _parse_keyspace,
    _parse_table,
    create_keyspace,
    create_table,
    delete_keyspace,
    delete_table,
    get_keyspace,
    get_table,
    list_keyspaces,
    list_tables,
    list_tags_for_resource,
    restore_table,
    tag_resource,
    update_table,
    create_type,
    delete_type,
    get_table_auto_scaling_settings,
    get_type,
    list_types,
    untag_resource,
    update_keyspace,
)

_ERR = ClientError(
    {"Error": {"Code": "ValidationException", "Message": "bad"}}, "op"
)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_keyspace_result_minimal(self):
        ks = KeyspaceResult(keyspace_name="ks", resource_arn="arn:ks")
        assert ks.keyspace_name == "ks"
        assert ks.replication_strategy is None
        assert ks.extra == {}

    def test_keyspace_result_full(self):
        ks = KeyspaceResult(
            keyspace_name="ks",
            resource_arn="arn:ks",
            replication_strategy="SINGLE_REGION",
            extra={"k": "v"},
        )
        assert ks.replication_strategy == "SINGLE_REGION"

    def test_table_result_minimal(self):
        t = TableResult(
            keyspace_name="ks", table_name="tbl",
            resource_arn="arn:tbl",
        )
        assert t.status is None
        assert t.extra == {}

    def test_table_result_full(self):
        t = TableResult(
            keyspace_name="ks", table_name="tbl",
            resource_arn="arn:tbl", status="ACTIVE",
            extra={"k": "v"},
        )
        assert t.status == "ACTIVE"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_keyspace(self):
        data = {
            "keyspaceName": "ks",
            "resourceArn": "arn:ks",
            "replicationStrategy": "SINGLE_REGION",
            "extra_key": "val",
        }
        ks = _parse_keyspace(data)
        assert ks.keyspace_name == "ks"
        assert ks.extra == {"extra_key": "val"}

    def test_parse_table(self):
        data = {
            "keyspaceName": "ks",
            "tableName": "tbl",
            "resourceArn": "arn:tbl",
            "status": "ACTIVE",
            "extra_key": "val",
        }
        t = _parse_table(data)
        assert t.table_name == "tbl"
        assert t.extra == {"extra_key": "val"}


# ---------------------------------------------------------------------------
# Keyspace operations
# ---------------------------------------------------------------------------


class TestCreateKeyspace:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_keyspace.return_value = {"resourceArn": "arn:ks"}
        mock_gc.return_value = client
        result = create_keyspace("ks")
        assert result.keyspace_name == "ks"
        assert result.resource_arn == "arn:ks"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_keyspace.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            create_keyspace("ks")


class TestGetKeyspace:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_keyspace.return_value = {
            "keyspaceName": "ks", "resourceArn": "arn:ks"
        }
        mock_gc.return_value = client
        result = get_keyspace("ks")
        assert result.keyspace_name == "ks"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_keyspace.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            get_keyspace("ks")


class TestListKeyspaces:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"keyspaces": [{"keyspaceName": "ks", "resourceArn": "arn:ks"}]}
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_keyspaces()
        assert len(result) == 1

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_keyspaces()


class TestDeleteKeyspace:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_keyspace("ks")

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_keyspace.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            delete_keyspace("ks")


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


class TestCreateTable:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_table.return_value = {"resourceArn": "arn:tbl"}
        mock_gc.return_value = client
        result = create_table("ks", "tbl", {"columns": []})
        assert result.table_name == "tbl"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_table.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            create_table("ks", "tbl", {"columns": []})


class TestGetTable:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_table.return_value = {
            "keyspaceName": "ks", "tableName": "tbl",
            "resourceArn": "arn:tbl", "status": "ACTIVE",
        }
        mock_gc.return_value = client
        result = get_table("ks", "tbl")
        assert result.status == "ACTIVE"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_table.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            get_table("ks", "tbl")


class TestListTables:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"tables": [
                {"keyspaceName": "ks", "tableName": "tbl", "resourceArn": "arn:tbl"}
            ]}
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_tables("ks")
        assert len(result) == 1

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_tables("ks")


class TestDeleteTable:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_table("ks", "tbl")

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_table.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            delete_table("ks", "tbl")


class TestUpdateTable:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.update_table.return_value = {"resourceArn": "arn:tbl"}
        mock_gc.return_value = client
        result = update_table("ks", "tbl")
        assert result == "arn:tbl"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.update_table.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            update_table("ks", "tbl")


class TestRestoreTable:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.restore_table.return_value = {
            "restoredTableARN": "arn:restored"
        }
        mock_gc.return_value = client
        result = restore_table("ks1", "tbl1", "ks2", "tbl2")
        assert result == "arn:restored"

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.restore_table.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            restore_table("ks1", "tbl1", "ks2", "tbl2")


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


class TestTagResource:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        tag_resource("arn:ks", [{"key": "env", "value": "dev"}])

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.tag_resource.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            tag_resource("arn:ks", [{"key": "env", "value": "dev"}])


class TestListTagsForResource:
    @patch("aws_util.keyspaces.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.list_tags_for_resource.return_value = {
            "tags": [{"key": "env", "value": "dev"}]
        }
        mock_gc.return_value = client
        result = list_tags_for_resource("arn:ks")
        assert len(result) == 1

    @patch("aws_util.keyspaces.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.list_tags_for_resource.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_tags_for_resource("arn:ks")


REGION = "us-east-1"


@patch("aws_util.keyspaces.get_client")
def test_create_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_type.return_value = {}
    create_type("test-keyspace_name", "test-type_name", [], region_name=REGION)
    mock_client.create_type.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_create_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_type",
    )
    with pytest.raises(RuntimeError, match="Failed to create type"):
        create_type("test-keyspace_name", "test-type_name", [], region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_delete_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_type.return_value = {}
    delete_type("test-keyspace_name", "test-type_name", region_name=REGION)
    mock_client.delete_type.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_delete_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_type",
    )
    with pytest.raises(RuntimeError, match="Failed to delete type"):
        delete_type("test-keyspace_name", "test-type_name", region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_get_table_auto_scaling_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_table_auto_scaling_settings.return_value = {}
    get_table_auto_scaling_settings("test-keyspace_name", "test-table_name", region_name=REGION)
    mock_client.get_table_auto_scaling_settings.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_get_table_auto_scaling_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_table_auto_scaling_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_auto_scaling_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to get table auto scaling settings"):
        get_table_auto_scaling_settings("test-keyspace_name", "test-table_name", region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_get_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_type.return_value = {}
    get_type("test-keyspace_name", "test-type_name", region_name=REGION)
    mock_client.get_type.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_get_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_type",
    )
    with pytest.raises(RuntimeError, match="Failed to get type"):
        get_type("test-keyspace_name", "test-type_name", region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_list_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_types.return_value = {}
    list_types("test-keyspace_name", region_name=REGION)
    mock_client.list_types.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_list_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_types",
    )
    with pytest.raises(RuntimeError, match="Failed to list types"):
        list_types("test-keyspace_name", region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.keyspaces.get_client")
def test_update_keyspace(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_keyspace.return_value = {}
    update_keyspace("test-keyspace_name", {}, region_name=REGION)
    mock_client.update_keyspace.assert_called_once()


@patch("aws_util.keyspaces.get_client")
def test_update_keyspace_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_keyspace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_keyspace",
    )
    with pytest.raises(RuntimeError, match="Failed to update keyspace"):
        update_keyspace("test-keyspace_name", {}, region_name=REGION)


def test_list_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.keyspaces import list_types
    mock_client = MagicMock()
    mock_client.list_types.return_value = {}
    monkeypatch.setattr("aws_util.keyspaces.get_client", lambda *a, **kw: mock_client)
    list_types("test-keyspace_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_types.assert_called_once()

def test_update_keyspace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.keyspaces import update_keyspace
    mock_client = MagicMock()
    mock_client.update_keyspace.return_value = {}
    monkeypatch.setattr("aws_util.keyspaces.get_client", lambda *a, **kw: mock_client)
    update_keyspace("test-keyspace_name", {}, client_side_timestamps="test-client_side_timestamps", region_name="us-east-1")
    mock_client.update_keyspace.assert_called_once()
