"""Tests for aws_util.dynamodb module."""
from __future__ import annotations

import boto3
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest
from boto3.dynamodb.conditions import Attr, Key

from aws_util.dynamodb import (
    Attr as AwsUtilAttr,
    DynamoKey,
    Key as AwsUtilKey,
    atomic_increment,
    batch_get,
    batch_write,
    delete_item,
    get_item,
    put_if_not_exists,
    put_item,
    query,
    scan,
    transact_get,
    transact_write,
    update_item,
    update_item_raw,
    batch_execute_statement,
    batch_get_item,
    batch_write_item,
    create_backup,
    create_global_table,
    create_table,
    delete_backup,
    delete_resource_policy,
    delete_table,
    describe_backup,
    describe_continuous_backups,
    describe_contributor_insights,
    describe_endpoints,
    describe_export,
    describe_global_table,
    describe_global_table_settings,
    describe_import,
    describe_kinesis_streaming_destination,
    describe_limits,
    describe_table,
    describe_table_replica_auto_scaling,
    describe_time_to_live,
    disable_kinesis_streaming_destination,
    enable_kinesis_streaming_destination,
    execute_statement,
    execute_transaction,
    export_table_to_point_in_time,
    get_resource_policy,
    import_table,
    list_backups,
    list_contributor_insights,
    list_exports,
    list_global_tables,
    list_imports,
    list_tables,
    list_tags_of_resource,
    put_resource_policy,
    restore_table_from_backup,
    restore_table_to_point_in_time,
    tag_resource,
    transact_get_items,
    transact_write_items,
    untag_resource,
    update_continuous_backups,
    update_contributor_insights,
    update_global_table,
    update_global_table_settings,
    update_kinesis_streaming_destination,
    update_table,
    update_table_replica_auto_scaling,
    update_time_to_live,
)

REGION = "us-east-1"
TABLE = "test-table"


@pytest.fixture
def table(dynamodb_client):
    """Return a populated DynamoDB resource table."""
    resource = boto3.resource("dynamodb", region_name=REGION)
    return resource.Table(TABLE)


# ---------------------------------------------------------------------------
# DynamoKey
# ---------------------------------------------------------------------------


def test_dynamo_key_as_dict_partition_only():
    key = DynamoKey(partition_key="pk", partition_value="abc")
    assert key.as_dict() == {"pk": "abc"}


def test_dynamo_key_as_dict_with_sort():
    key = DynamoKey(
        partition_key="pk", partition_value="abc", sort_key="sk", sort_value="123"
    )
    assert key.as_dict() == {"pk": "abc", "sk": "123"}


# ---------------------------------------------------------------------------
# get_item
# ---------------------------------------------------------------------------


def test_get_item_returns_item(dynamodb_client):
    table_res = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
    table_res.put_item(Item={"pk": "user#1", "name": "Alice"})

    result = get_item(TABLE, {"pk": "user#1"}, region_name=REGION)
    assert result is not None
    assert result["name"] == "Alice"


def test_get_item_with_dynamo_key(dynamodb_client):
    table_res = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)
    table_res.put_item(Item={"pk": "user#2", "name": "Bob"})

    key = DynamoKey(partition_key="pk", partition_value="user#2")
    result = get_item(TABLE, key, region_name=REGION)
    assert result["name"] == "Bob"


def test_get_item_returns_none_for_missing(dynamodb_client):
    result = get_item(TABLE, {"pk": "nonexistent"}, region_name=REGION)
    assert result is None


def test_get_item_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def get_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "GetItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="get_item failed"):
        get_item("no-table", {"pk": "x"}, region_name=REGION)


# ---------------------------------------------------------------------------
# put_item
# ---------------------------------------------------------------------------


def test_put_item_creates_item(dynamodb_client):
    put_item(TABLE, {"pk": "item#1", "val": "test"}, region_name=REGION)
    result = get_item(TABLE, {"pk": "item#1"}, region_name=REGION)
    assert result["val"] == "test"


def test_put_item_with_condition(dynamodb_client):
    put_item(TABLE, {"pk": "cond#1", "val": "v"}, region_name=REGION)
    # Condition: item must not exist (will fail since it exists)
    with pytest.raises(RuntimeError, match="put_item failed"):
        put_item(
            TABLE,
            {"pk": "cond#1", "val": "new"},
            condition=Attr("pk").not_exists(),
            region_name=REGION,
        )


def test_put_item_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def put_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ProvisionedThroughputExceededException", "Message": "throttled"}},
                    "PutItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="put_item failed"):
        put_item("no-table", {"pk": "x"}, region_name=REGION)


# ---------------------------------------------------------------------------
# update_item
# ---------------------------------------------------------------------------


def test_update_item_modifies_attributes(dynamodb_client):
    put_item(TABLE, {"pk": "upd#1", "status": "old"}, region_name=REGION)
    result = update_item(TABLE, {"pk": "upd#1"}, {"status": "new"}, region_name=REGION)
    assert result["status"] == "new"


def test_update_item_with_dynamo_key(dynamodb_client):
    put_item(TABLE, {"pk": "upd#2", "count": 0}, region_name=REGION)
    key = DynamoKey(partition_key="pk", partition_value="upd#2")
    result = update_item(TABLE, key, {"count": 5}, region_name=REGION)
    assert result["count"] == 5


def test_update_item_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def update_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "UpdateItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="update_item failed"):
        update_item("no-table", {"pk": "x"}, {"a": 1}, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_item
# ---------------------------------------------------------------------------


def test_delete_item_removes(dynamodb_client):
    put_item(TABLE, {"pk": "del#1"}, region_name=REGION)
    delete_item(TABLE, {"pk": "del#1"}, region_name=REGION)
    assert get_item(TABLE, {"pk": "del#1"}, region_name=REGION) is None


def test_delete_item_with_dynamo_key(dynamodb_client):
    put_item(TABLE, {"pk": "del#2"}, region_name=REGION)
    key = DynamoKey(partition_key="pk", partition_value="del#2")
    delete_item(TABLE, key, region_name=REGION)
    assert get_item(TABLE, {"pk": "del#2"}, region_name=REGION) is None


def test_delete_item_with_condition(dynamodb_client):
    put_item(TABLE, {"pk": "del#3", "locked": True}, region_name=REGION)
    with pytest.raises(RuntimeError, match="delete_item failed"):
        delete_item(
            TABLE,
            {"pk": "del#3"},
            condition=Attr("locked").eq(False),
            region_name=REGION,
        )


def test_delete_item_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def delete_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "DeleteItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="delete_item failed"):
        delete_item("no-table", {"pk": "x"}, region_name=REGION)


# ---------------------------------------------------------------------------
# query
# ---------------------------------------------------------------------------


def test_query_returns_items(dynamodb_client):
    put_item(TABLE, {"pk": "q#1", "val": "a"}, region_name=REGION)
    put_item(TABLE, {"pk": "q#2", "val": "b"}, region_name=REGION)
    result = query(TABLE, Key("pk").eq("q#1"), region_name=REGION)
    assert len(result) == 1
    assert result[0]["val"] == "a"


def test_query_with_filter(dynamodb_client):
    put_item(TABLE, {"pk": "qf#1", "active": True}, region_name=REGION)
    put_item(TABLE, {"pk": "qf#1b", "active": False}, region_name=REGION)
    result = query(
        TABLE,
        Key("pk").eq("qf#1"),
        filter_condition=Attr("active").eq(True),
        region_name=REGION,
    )
    assert len(result) == 1


def test_query_with_limit(dynamodb_client):
    for i in range(5):
        put_item(TABLE, {"pk": f"ql#{i}"}, region_name=REGION)
    result = query(TABLE, Key("pk").eq("ql#0"), limit=1, region_name=REGION)
    assert len(result) <= 1


def test_query_scan_index_forward_false(dynamodb_client):
    put_item(TABLE, {"pk": "qsf#1"}, region_name=REGION)
    result = query(
        TABLE,
        Key("pk").eq("qsf#1"),
        scan_index_forward=False,
        region_name=REGION,
    )
    assert isinstance(result, list)


def test_query_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def query(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "Query",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="query failed"):
        query("no-table", Key("pk").eq("x"), region_name=REGION)


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------


def test_scan_returns_all_items(dynamodb_client):
    put_item(TABLE, {"pk": "s#1", "val": "a"}, region_name=REGION)
    put_item(TABLE, {"pk": "s#2", "val": "b"}, region_name=REGION)
    result = scan(TABLE, region_name=REGION)
    assert len(result) >= 2


def test_scan_with_filter(dynamodb_client):
    put_item(TABLE, {"pk": "sf#1", "active": True}, region_name=REGION)
    put_item(TABLE, {"pk": "sf#2", "active": False}, region_name=REGION)
    result = scan(TABLE, filter_condition=Attr("active").eq(True), region_name=REGION)
    assert all(item.get("active") for item in result)


def test_scan_with_limit(dynamodb_client):
    for i in range(5):
        put_item(TABLE, {"pk": f"sl#{i}"}, region_name=REGION)
    result = scan(TABLE, limit=2, region_name=REGION)
    assert len(result) <= 2


def test_scan_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def scan(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "Scan",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="scan failed"):
        scan("no-table", region_name=REGION)


# ---------------------------------------------------------------------------
# batch_get
# ---------------------------------------------------------------------------


def test_batch_get_returns_items(dynamodb_client):
    put_item(TABLE, {"pk": "bg#1", "v": "a"}, region_name=REGION)
    put_item(TABLE, {"pk": "bg#2", "v": "b"}, region_name=REGION)
    result = batch_get(TABLE, [{"pk": "bg#1"}, {"pk": "bg#2"}], region_name=REGION)
    assert len(result) == 2


def test_batch_get_with_dynamo_keys(dynamodb_client):
    put_item(TABLE, {"pk": "bgk#1"}, region_name=REGION)
    key = DynamoKey(partition_key="pk", partition_value="bgk#1")
    result = batch_get(TABLE, [key], region_name=REGION)
    assert len(result) == 1


def test_batch_get_too_many_keys():
    with pytest.raises(ValueError, match="at most 100"):
        batch_get(TABLE, [{"pk": str(i)} for i in range(101)], region_name=REGION)


def test_batch_get_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import boto3 as _boto3


    def bad_resource(service, **kwargs):
        class BadResource:
            def batch_get_item(self, **kw):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "BatchGetItem",
                )
        return BadResource()

    monkeypatch.setattr(_boto3, "resource", bad_resource)
    with pytest.raises(RuntimeError, match="batch_get failed"):
        batch_get(TABLE, [{"pk": "x"}], region_name=REGION)


# ---------------------------------------------------------------------------
# batch_write
# ---------------------------------------------------------------------------


def test_batch_write_writes_items(dynamodb_client):
    items = [{"pk": f"bw#{i}", "val": i} for i in range(5)]
    batch_write(TABLE, items, region_name=REGION)
    for i in range(5):
        result = get_item(TABLE, {"pk": f"bw#{i}"}, region_name=REGION)
        assert result is not None


# ---------------------------------------------------------------------------
# transact_write
# ---------------------------------------------------------------------------


def test_transact_write_basic(dynamodb_client, monkeypatch):
    """transact_write forwards operations to TransactWriteItems via get_client."""
    from unittest.mock import MagicMock, patch

    mock_client = MagicMock()
    mock_client.transact_write_items.return_value = {}
    ops = [
        {
            "Put": {
                "TableName": TABLE,
                "Item": {"pk": {"S": "tw#1"}, "val": {"S": "hello"}},
            }
        }
    ]
    with patch("aws_util.dynamodb.get_client", return_value=mock_client):
        transact_write(ops, region_name=REGION)
    mock_client.transact_write_items.assert_called_once()


def test_transact_write_too_many_operations():
    with pytest.raises(ValueError, match="at most 100"):
        transact_write([{"Put": {}} for _ in range(101)], region_name=REGION)


# ---------------------------------------------------------------------------
# transact_get
# ---------------------------------------------------------------------------


def test_transact_get_basic(dynamodb_client):
    put_item(TABLE, {"pk": "tg#1", "data": "hello"}, region_name=REGION)
    items = [{"Get": {"TableName": TABLE, "Key": {"pk": {"S": "tg#1"}}}}]
    result = transact_get(items, region_name=REGION)
    assert result[0] is not None
    assert result[0]["data"] == "hello"


def test_transact_get_missing_returns_none(dynamodb_client):
    items = [{"Get": {"TableName": TABLE, "Key": {"pk": {"S": "nonexistent"}}}}]
    result = transact_get(items, region_name=REGION)
    assert result[0] is None


def test_transact_get_too_many_items():
    with pytest.raises(ValueError, match="at most 100"):
        transact_get([{"Get": {}} for _ in range(101)], region_name=REGION)


def test_transact_get_shorthand_wrapped(dynamodb_client):
    """Plain {TableName, Key} dicts should be wrapped in {"Get": ...}."""
    put_item(TABLE, {"pk": "tgw#1"}, region_name=REGION)
    items = [{"TableName": TABLE, "Key": {"pk": {"S": "tgw#1"}}}]
    result = transact_get(items, region_name=REGION)
    assert result[0] is not None


# ---------------------------------------------------------------------------
# atomic_increment
# ---------------------------------------------------------------------------


def test_atomic_increment_creates_attribute(dynamodb_client):
    put_item(TABLE, {"pk": "ai#1"}, region_name=REGION)
    new_val = atomic_increment(TABLE, {"pk": "ai#1"}, "count", region_name=REGION)
    assert new_val == 1


def test_atomic_increment_by_custom_amount(dynamodb_client):
    put_item(TABLE, {"pk": "ai#2"}, region_name=REGION)
    atomic_increment(TABLE, {"pk": "ai#2"}, "count", amount=5, region_name=REGION)
    new_val = atomic_increment(TABLE, {"pk": "ai#2"}, "count", amount=3, region_name=REGION)
    assert new_val == 8


def test_atomic_increment_with_dynamo_key(dynamodb_client):
    put_item(TABLE, {"pk": "ai#3"}, region_name=REGION)
    key = DynamoKey(partition_key="pk", partition_value="ai#3")
    new_val = atomic_increment(TABLE, key, "visits", region_name=REGION)
    assert new_val == 1


def test_atomic_increment_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def update_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "UpdateItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="atomic_increment failed"):
        atomic_increment("no-table", {"pk": "x"}, "count", region_name=REGION)


# ---------------------------------------------------------------------------
# put_if_not_exists
# ---------------------------------------------------------------------------


def test_put_if_not_exists_creates(dynamodb_client):
    result = put_if_not_exists(TABLE, {"pk": "pine#1", "val": "new"}, "pk", region_name=REGION)
    assert result is True
    item = get_item(TABLE, {"pk": "pine#1"}, region_name=REGION)
    assert item["val"] == "new"


def test_put_if_not_exists_returns_false_when_exists(dynamodb_client):
    put_item(TABLE, {"pk": "pine#2", "val": "existing"}, region_name=REGION)
    result = put_if_not_exists(TABLE, {"pk": "pine#2", "val": "new"}, "pk", region_name=REGION)
    assert result is False
    # Original value should be unchanged
    item = get_item(TABLE, {"pk": "pine#2"}, region_name=REGION)
    assert item["val"] == "existing"


def test_put_if_not_exists_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def put_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ProvisionedThroughputExceededException", "Message": "throttled"}},
                    "PutItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="put_if_not_exists failed"):
        put_if_not_exists("no-table", {"pk": "x"}, "pk", region_name=REGION)


# ---------------------------------------------------------------------------
# query with index_name and pagination (lines 221, 233)
# ---------------------------------------------------------------------------


def test_query_with_index_name(monkeypatch):
    """Covers index_name branch in query (line 221)."""
    import aws_util.dynamodb as ddb

    class FakeTable:
        def query(self, **kwargs):
            assert kwargs.get("IndexName") == "my-index"
            return {"Items": [{"pk": "x"}], "LastEvaluatedKey": None}

    monkeypatch.setattr(ddb, "_table_resource", lambda *a, **kw: FakeTable())
    result = query(TABLE, Key("pk").eq("x"), index_name="my-index", region_name=REGION)
    assert len(result) == 1


def test_query_pagination(monkeypatch):
    """Covers ExclusiveStartKey in query (line 233)."""
    import aws_util.dynamodb as ddb

    call_count = {"n": 0}

    class PaginatedTable:
        def query(self, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {"Items": [{"pk": "p#1"}], "LastEvaluatedKey": {"pk": "p#1"}}
            return {"Items": [{"pk": "p#2"}]}

    monkeypatch.setattr(ddb, "_table_resource", lambda *a, **kw: PaginatedTable())
    result = query(TABLE, Key("pk").eq("x"), region_name=REGION)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# scan with index_name and pagination (lines 269, 281)
# ---------------------------------------------------------------------------


def test_scan_with_index_name(monkeypatch):
    """Covers index_name branch in scan (line 269)."""
    import aws_util.dynamodb as ddb

    class FakeTable:
        def scan(self, **kwargs):
            assert kwargs.get("IndexName") == "my-gsi"
            return {"Items": [{"pk": "y"}]}

    monkeypatch.setattr(ddb, "_table_resource", lambda *a, **kw: FakeTable())
    result = scan(TABLE, index_name="my-gsi", region_name=REGION)
    assert len(result) == 1


def test_scan_pagination(monkeypatch):
    """Covers ExclusiveStartKey in scan (line 281)."""
    import aws_util.dynamodb as ddb

    call_count = {"n": 0}

    class PaginatedTable:
        def scan(self, **kwargs):
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {"Items": [{"pk": "s#1"}], "LastEvaluatedKey": {"pk": "s#1"}}
            return {"Items": [{"pk": "s#2"}]}

    monkeypatch.setattr(ddb, "_table_resource", lambda *a, **kw: PaginatedTable())
    result = scan(TABLE, region_name=REGION)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# batch_write ClientError (lines 355-356)
# ---------------------------------------------------------------------------


def test_batch_write_runtime_error(monkeypatch):
    """Covers ClientError in batch_write (lines 355-356)."""
    from unittest.mock import MagicMock, patch
    from botocore.exceptions import ClientError

    mock_batch = MagicMock()
    mock_batch.__enter__ = MagicMock(return_value=mock_batch)
    mock_batch.__exit__ = MagicMock(return_value=False)
    mock_batch.put_item.side_effect = ClientError(
        {"Error": {"Code": "ProvisionedThroughputExceededException", "Message": "throttled"}},
        "BatchWriteItem",
    )
    mock_table = MagicMock()
    mock_table.batch_writer.return_value = mock_batch
    mock_resource = MagicMock()
    mock_resource.Table.return_value = mock_table

    with patch("boto3.resource", return_value=mock_resource):
        with pytest.raises(RuntimeError, match="batch_write failed"):
            batch_write(TABLE, [{"pk": "x"}], region_name=REGION)


# ---------------------------------------------------------------------------
# transact_write ClientError (lines 394-395)
# ---------------------------------------------------------------------------


def test_transact_write_runtime_error(monkeypatch):
    """Covers ClientError in transact_write."""
    from unittest.mock import MagicMock, patch
    from botocore.exceptions import ClientError

    mock_client = MagicMock()
    mock_client.transact_write_items.side_effect = ClientError(
        {"Error": {"Code": "TransactionCanceledException", "Message": "cancelled"}},
        "TransactWriteItems",
    )
    ops = [{"Put": {"TableName": TABLE, "Item": {"pk": {"S": "x"}}}}]
    with patch("aws_util.dynamodb.get_client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="transact_write failed"):
            transact_write(ops, region_name=REGION)


# ---------------------------------------------------------------------------
# transact_get ClientError (lines 432-433)
# ---------------------------------------------------------------------------


def test_transact_get_runtime_error(monkeypatch):
    """Covers ClientError in transact_get."""
    from unittest.mock import patch, MagicMock
    from botocore.exceptions import ClientError

    mock_client = MagicMock()
    mock_client.transact_get_items.side_effect = ClientError(
        {"Error": {"Code": "TransactionCanceledException", "Message": "cancelled"}},
        "TransactGetItems",
    )

    with patch("aws_util.dynamodb.get_client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="transact_get failed"):
            transact_get([{"Get": {"TableName": TABLE, "Key": {"pk": {"S": "x"}}}}], region_name=REGION)


# ---------------------------------------------------------------------------
# update_item_raw
# ---------------------------------------------------------------------------


def test_update_item_raw_simple_set(dynamodb_client):
    """update_item_raw with a simple SET expression."""
    put_item(TABLE, {"pk": "uir#1", "status": "pending"}, region_name=REGION)
    result = update_item_raw(
        TABLE,
        {"pk": "uir#1"},
        update_expression="SET #s = :val",
        expression_attribute_names={"#s": "status"},
        expression_attribute_values={":val": "complete"},
        region_name=REGION,
    )
    assert result["status"] == "complete"


def test_update_item_raw_if_not_exists(dynamodb_client):
    """update_item_raw with if_not_exists pattern."""
    put_item(TABLE, {"pk": "uir#2"}, region_name=REGION)
    result = update_item_raw(
        TABLE,
        {"pk": "uir#2"},
        update_expression="SET #c = if_not_exists(#c, :zero) + :inc",
        expression_attribute_names={"#c": "counter"},
        expression_attribute_values={":zero": 0, ":inc": 5},
        region_name=REGION,
    )
    assert result["counter"] == 5

    # Call again — should increment from 5 to 8
    result = update_item_raw(
        TABLE,
        {"pk": "uir#2"},
        update_expression="SET #c = if_not_exists(#c, :zero) + :inc",
        expression_attribute_names={"#c": "counter"},
        expression_attribute_values={":zero": 0, ":inc": 3},
        region_name=REGION,
    )
    assert result["counter"] == 8


def test_update_item_raw_with_dynamo_key(dynamodb_client):
    """update_item_raw accepts a DynamoKey instead of a dict."""
    put_item(TABLE, {"pk": "uir#3", "val": "old"}, region_name=REGION)
    key = DynamoKey(partition_key="pk", partition_value="uir#3")
    result = update_item_raw(
        TABLE,
        key,
        update_expression="SET #v = :new_val",
        expression_attribute_names={"#v": "val"},
        expression_attribute_values={":new_val": "new"},
        region_name=REGION,
    )
    assert result["val"] == "new"


def test_update_item_raw_condition_expression_failure(dynamodb_client):
    """update_item_raw raises RuntimeError when condition_expression fails."""
    put_item(TABLE, {"pk": "uir#4", "version": 1}, region_name=REGION)
    with pytest.raises(RuntimeError, match="update_item_raw failed"):
        update_item_raw(
            TABLE,
            {"pk": "uir#4"},
            update_expression="SET #v = :new_ver",
            expression_attribute_names={"#v": "version"},
            expression_attribute_values={":new_ver": 2, ":expected": 99},
            condition_expression=Attr("version").eq(99),
            region_name=REGION,
        )


def test_update_item_raw_no_names_or_values(dynamodb_client):
    """update_item_raw with no expression_attribute_names or values."""
    put_item(TABLE, {"pk": "uir#5", "qty": 42}, region_name=REGION)
    result = update_item_raw(
        TABLE,
        {"pk": "uir#5"},
        update_expression="REMOVE qty",
        region_name=REGION,
    )
    assert "qty" not in result


def test_update_item_raw_runtime_error(monkeypatch):
    """update_item_raw wraps ClientError in RuntimeError."""
    from botocore.exceptions import ClientError
    import aws_util.dynamodb as ddb

    def bad_table_resource(table_name, region_name=None):
        class BadTable:
            def update_item(self, **kwargs):
                raise ClientError(
                    {"Error": {"Code": "ResourceNotFoundException", "Message": "no table"}},
                    "UpdateItem",
                )
        return BadTable()

    monkeypatch.setattr(ddb, "_table_resource", bad_table_resource)
    with pytest.raises(RuntimeError, match="update_item_raw failed"):
        update_item_raw(
            "no-table",
            {"pk": "x"},
            update_expression="SET #a = :v",
            expression_attribute_names={"#a": "attr"},
            expression_attribute_values={":v": 1},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Key / Attr re-exports
# ---------------------------------------------------------------------------


def test_key_and_attr_importable_from_aws_util_dynamodb():
    """Key and Attr re-exported from aws_util.dynamodb match boto3 originals."""
    assert AwsUtilKey is Key
    assert AwsUtilAttr is Attr


def test_batch_execute_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_execute_statement.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_execute_statement([], region_name=REGION)
    mock_client.batch_execute_statement.assert_called_once()


def test_batch_execute_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_execute_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_execute_statement",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch execute statement"):
        batch_execute_statement([], region_name=REGION)


def test_batch_get_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_item.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_get_item({}, region_name=REGION)
    mock_client.batch_get_item.assert_called_once()


def test_batch_get_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_item",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get item"):
        batch_get_item({}, region_name=REGION)


def test_batch_write_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_write_item.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_write_item({}, region_name=REGION)
    mock_client.batch_write_item.assert_called_once()


def test_batch_write_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_write_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_write_item",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch write item"):
        batch_write_item({}, region_name=REGION)


def test_create_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_backup.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    create_backup("test-table_name", "test-backup_name", region_name=REGION)
    mock_client.create_backup.assert_called_once()


def test_create_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_backup",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create backup"):
        create_backup("test-table_name", "test-backup_name", region_name=REGION)


def test_create_global_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    create_global_table("test-global_table_name", [], region_name=REGION)
    mock_client.create_global_table.assert_called_once()


def test_create_global_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_global_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create global table"):
        create_global_table("test-global_table_name", [], region_name=REGION)


def test_create_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    create_table([], "test-table_name", [], region_name=REGION)
    mock_client.create_table.assert_called_once()


def test_create_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create table"):
        create_table([], "test-table_name", [], region_name=REGION)


def test_delete_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_backup.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    delete_backup("test-backup_arn", region_name=REGION)
    mock_client.delete_backup.assert_called_once()


def test_delete_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_backup",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete backup"):
        delete_backup("test-backup_arn", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    delete_table("test-table_name", region_name=REGION)
    mock_client.delete_table.assert_called_once()


def test_delete_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete table"):
        delete_table("test-table_name", region_name=REGION)


def test_describe_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_backup.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_backup("test-backup_arn", region_name=REGION)
    mock_client.describe_backup.assert_called_once()


def test_describe_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_backup",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe backup"):
        describe_backup("test-backup_arn", region_name=REGION)


def test_describe_continuous_backups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_continuous_backups.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_continuous_backups("test-table_name", region_name=REGION)
    mock_client.describe_continuous_backups.assert_called_once()


def test_describe_continuous_backups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_continuous_backups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_continuous_backups",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe continuous backups"):
        describe_continuous_backups("test-table_name", region_name=REGION)


def test_describe_contributor_insights(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_contributor_insights("test-table_name", region_name=REGION)
    mock_client.describe_contributor_insights.assert_called_once()


def test_describe_contributor_insights_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contributor_insights.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_contributor_insights",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe contributor insights"):
        describe_contributor_insights("test-table_name", region_name=REGION)


def test_describe_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_endpoints(region_name=REGION)
    mock_client.describe_endpoints.assert_called_once()


def test_describe_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoints",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoints"):
        describe_endpoints(region_name=REGION)


def test_describe_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_export("test-export_arn", region_name=REGION)
    mock_client.describe_export.assert_called_once()


def test_describe_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_export",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe export"):
        describe_export("test-export_arn", region_name=REGION)


def test_describe_global_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_global_table("test-global_table_name", region_name=REGION)
    mock_client.describe_global_table.assert_called_once()


def test_describe_global_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe global table"):
        describe_global_table("test-global_table_name", region_name=REGION)


def test_describe_global_table_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_table_settings.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_global_table_settings("test-global_table_name", region_name=REGION)
    mock_client.describe_global_table_settings.assert_called_once()


def test_describe_global_table_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_table_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_table_settings",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe global table settings"):
        describe_global_table_settings("test-global_table_name", region_name=REGION)


def test_describe_import(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_import("test-import_arn", region_name=REGION)
    mock_client.describe_import.assert_called_once()


def test_describe_import_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_import",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe import"):
        describe_import("test-import_arn", region_name=REGION)


def test_describe_kinesis_streaming_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_kinesis_streaming_destination("test-table_name", region_name=REGION)
    mock_client.describe_kinesis_streaming_destination.assert_called_once()


def test_describe_kinesis_streaming_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_kinesis_streaming_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_kinesis_streaming_destination",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe kinesis streaming destination"):
        describe_kinesis_streaming_destination("test-table_name", region_name=REGION)


def test_describe_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_limits.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_limits(region_name=REGION)
    mock_client.describe_limits.assert_called_once()


def test_describe_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_limits",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe limits"):
        describe_limits(region_name=REGION)


def test_describe_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_table("test-table_name", region_name=REGION)
    mock_client.describe_table.assert_called_once()


def test_describe_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe table"):
        describe_table("test-table_name", region_name=REGION)


def test_describe_table_replica_auto_scaling(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table_replica_auto_scaling.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_table_replica_auto_scaling("test-table_name", region_name=REGION)
    mock_client.describe_table_replica_auto_scaling.assert_called_once()


def test_describe_table_replica_auto_scaling_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table_replica_auto_scaling.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_table_replica_auto_scaling",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe table replica auto scaling"):
        describe_table_replica_auto_scaling("test-table_name", region_name=REGION)


def test_describe_time_to_live(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_time_to_live.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_time_to_live("test-table_name", region_name=REGION)
    mock_client.describe_time_to_live.assert_called_once()


def test_describe_time_to_live_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_time_to_live.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_time_to_live",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe time to live"):
        describe_time_to_live("test-table_name", region_name=REGION)


def test_disable_kinesis_streaming_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)
    mock_client.disable_kinesis_streaming_destination.assert_called_once()


def test_disable_kinesis_streaming_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_kinesis_streaming_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_kinesis_streaming_destination",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable kinesis streaming destination"):
        disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)


def test_enable_kinesis_streaming_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)
    mock_client.enable_kinesis_streaming_destination.assert_called_once()


def test_enable_kinesis_streaming_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_kinesis_streaming_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_kinesis_streaming_destination",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable kinesis streaming destination"):
        enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)


def test_execute_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_statement.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    execute_statement("test-statement", region_name=REGION)
    mock_client.execute_statement.assert_called_once()


def test_execute_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_statement",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute statement"):
        execute_statement("test-statement", region_name=REGION)


def test_execute_transaction(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_transaction.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    execute_transaction([], region_name=REGION)
    mock_client.execute_transaction.assert_called_once()


def test_execute_transaction_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_transaction.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_transaction",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute transaction"):
        execute_transaction([], region_name=REGION)


def test_export_table_to_point_in_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_table_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    export_table_to_point_in_time("test-table_arn", "test-s3_bucket", region_name=REGION)
    mock_client.export_table_to_point_in_time.assert_called_once()


def test_export_table_to_point_in_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_table_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_table_to_point_in_time",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export table to point in time"):
        export_table_to_point_in_time("test-table_arn", "test-s3_bucket", region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_import_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    import_table({}, "test-input_format", {}, region_name=REGION)
    mock_client.import_table.assert_called_once()


def test_import_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import table"):
        import_table({}, "test-input_format", {}, region_name=REGION)


def test_list_backups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_backups.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_backups(region_name=REGION)
    mock_client.list_backups.assert_called_once()


def test_list_backups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_backups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_backups",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list backups"):
        list_backups(region_name=REGION)


def test_list_contributor_insights(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_contributor_insights(region_name=REGION)
    mock_client.list_contributor_insights.assert_called_once()


def test_list_contributor_insights_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contributor_insights.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_contributor_insights",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list contributor insights"):
        list_contributor_insights(region_name=REGION)


def test_list_exports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_exports.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_exports(region_name=REGION)
    mock_client.list_exports.assert_called_once()


def test_list_exports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_exports",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list exports"):
        list_exports(region_name=REGION)


def test_list_global_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_global_tables.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_global_tables(region_name=REGION)
    mock_client.list_global_tables.assert_called_once()


def test_list_global_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_global_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_global_tables",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list global tables"):
        list_global_tables(region_name=REGION)


def test_list_imports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_imports(region_name=REGION)
    mock_client.list_imports.assert_called_once()


def test_list_imports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_imports",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list imports"):
        list_imports(region_name=REGION)


def test_list_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tables.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_tables(region_name=REGION)
    mock_client.list_tables.assert_called_once()


def test_list_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tables",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tables"):
        list_tables(region_name=REGION)


def test_list_tags_of_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_of_resource.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_tags_of_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_of_resource.assert_called_once()


def test_list_tags_of_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_of_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_of_resource",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags of resource"):
        list_tags_of_resource("test-resource_arn", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


def test_restore_table_from_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_backup.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    restore_table_from_backup("test-target_table_name", "test-backup_arn", region_name=REGION)
    mock_client.restore_table_from_backup.assert_called_once()


def test_restore_table_from_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_table_from_backup",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore table from backup"):
        restore_table_from_backup("test-target_table_name", "test-backup_arn", region_name=REGION)


def test_restore_table_to_point_in_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    restore_table_to_point_in_time("test-target_table_name", region_name=REGION)
    mock_client.restore_table_to_point_in_time.assert_called_once()


def test_restore_table_to_point_in_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_table_to_point_in_time",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore table to point in time"):
        restore_table_to_point_in_time("test-target_table_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_transact_get_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.transact_get_items.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    transact_get_items([], region_name=REGION)
    mock_client.transact_get_items.assert_called_once()


def test_transact_get_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.transact_get_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "transact_get_items",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to transact get items"):
        transact_get_items([], region_name=REGION)


def test_transact_write_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.transact_write_items.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    transact_write_items([], region_name=REGION)
    mock_client.transact_write_items.assert_called_once()


def test_transact_write_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.transact_write_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "transact_write_items",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to transact write items"):
        transact_write_items([], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_continuous_backups(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_continuous_backups.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_continuous_backups("test-table_name", {}, region_name=REGION)
    mock_client.update_continuous_backups.assert_called_once()


def test_update_continuous_backups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_continuous_backups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_continuous_backups",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update continuous backups"):
        update_continuous_backups("test-table_name", {}, region_name=REGION)


def test_update_contributor_insights(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_contributor_insights("test-table_name", "test-contributor_insights_action", region_name=REGION)
    mock_client.update_contributor_insights.assert_called_once()


def test_update_contributor_insights_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contributor_insights.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contributor_insights",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contributor insights"):
        update_contributor_insights("test-table_name", "test-contributor_insights_action", region_name=REGION)


def test_update_global_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_global_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_global_table("test-global_table_name", [], region_name=REGION)
    mock_client.update_global_table.assert_called_once()


def test_update_global_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_global_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_global_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update global table"):
        update_global_table("test-global_table_name", [], region_name=REGION)


def test_update_global_table_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_global_table_settings.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_global_table_settings("test-global_table_name", region_name=REGION)
    mock_client.update_global_table_settings.assert_called_once()


def test_update_global_table_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_global_table_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_global_table_settings",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update global table settings"):
        update_global_table_settings("test-global_table_name", region_name=REGION)


def test_update_kinesis_streaming_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)
    mock_client.update_kinesis_streaming_destination.assert_called_once()


def test_update_kinesis_streaming_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_kinesis_streaming_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_kinesis_streaming_destination",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update kinesis streaming destination"):
        update_kinesis_streaming_destination("test-table_name", "test-stream_arn", region_name=REGION)


def test_update_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_table("test-table_name", region_name=REGION)
    mock_client.update_table.assert_called_once()


def test_update_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_table",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update table"):
        update_table("test-table_name", region_name=REGION)


def test_update_table_replica_auto_scaling(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table_replica_auto_scaling.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_table_replica_auto_scaling("test-table_name", region_name=REGION)
    mock_client.update_table_replica_auto_scaling.assert_called_once()


def test_update_table_replica_auto_scaling_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table_replica_auto_scaling.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_table_replica_auto_scaling",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update table replica auto scaling"):
        update_table_replica_auto_scaling("test-table_name", region_name=REGION)


def test_update_time_to_live(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_time_to_live.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_time_to_live("test-table_name", {}, region_name=REGION)
    mock_client.update_time_to_live.assert_called_once()


def test_update_time_to_live_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_time_to_live.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_time_to_live",
    )
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update time to live"):
        update_time_to_live("test-table_name", {}, region_name=REGION)


def test_batch_execute_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import batch_execute_statement
    mock_client = MagicMock()
    mock_client.batch_execute_statement.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_execute_statement("test-statements", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.batch_execute_statement.assert_called_once()

def test_batch_get_item_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import batch_get_item
    mock_client = MagicMock()
    mock_client.batch_get_item.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_get_item("test-request_items", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.batch_get_item.assert_called_once()

def test_batch_write_item_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import batch_write_item
    mock_client = MagicMock()
    mock_client.batch_write_item.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    batch_write_item("test-request_items", return_consumed_capacity="test-return_consumed_capacity", return_item_collection_metrics="test-return_item_collection_metrics", region_name="us-east-1")
    mock_client.batch_write_item.assert_called_once()

def test_create_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import create_table
    mock_client = MagicMock()
    mock_client.create_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    create_table({}, "test-table_name", "test-key_schema", local_secondary_indexes="test-local_secondary_indexes", global_secondary_indexes="test-global_secondary_indexes", billing_mode="test-billing_mode", provisioned_throughput="test-provisioned_throughput", stream_specification={}, sse_specification={}, tags=[{"Key": "k", "Value": "v"}], table_class="test-table_class", deletion_protection_enabled="test-deletion_protection_enabled", warm_throughput="test-warm_throughput", resource_policy="{}", on_demand_throughput="test-on_demand_throughput", region_name="us-east-1")
    mock_client.create_table.assert_called_once()

def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import delete_resource_policy
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.delete_resource_policy.assert_called_once()

def test_describe_contributor_insights_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import describe_contributor_insights
    mock_client = MagicMock()
    mock_client.describe_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    describe_contributor_insights("test-table_name", index_name="test-index_name", region_name="us-east-1")
    mock_client.describe_contributor_insights.assert_called_once()

def test_disable_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import disable_kinesis_streaming_destination
    mock_client = MagicMock()
    mock_client.disable_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", enable_kinesis_streaming_configuration=True, region_name="us-east-1")
    mock_client.disable_kinesis_streaming_destination.assert_called_once()

def test_enable_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import enable_kinesis_streaming_destination
    mock_client = MagicMock()
    mock_client.enable_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", enable_kinesis_streaming_configuration=True, region_name="us-east-1")
    mock_client.enable_kinesis_streaming_destination.assert_called_once()

def test_execute_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import execute_statement
    mock_client = MagicMock()
    mock_client.execute_statement.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    execute_statement("test-statement", parameters="test-parameters", consistent_read="test-consistent_read", next_token="test-next_token", return_consumed_capacity="test-return_consumed_capacity", limit=1, return_values_on_condition_check_failure="test-return_values_on_condition_check_failure", region_name="us-east-1")
    mock_client.execute_statement.assert_called_once()

def test_execute_transaction_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import execute_transaction
    mock_client = MagicMock()
    mock_client.execute_transaction.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    execute_transaction("test-transact_statements", client_request_token="test-client_request_token", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.execute_transaction.assert_called_once()

def test_export_table_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import export_table_to_point_in_time
    mock_client = MagicMock()
    mock_client.export_table_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    export_table_to_point_in_time("test-table_arn", "test-s3_bucket", export_time=1, client_token="test-client_token", s3_bucket_owner="test-s3_bucket_owner", s3_prefix="test-s3_prefix", s3_sse_algorithm="test-s3_sse_algorithm", s3_sse_kms_key_id="test-s3_sse_kms_key_id", export_format=1, export_type=1, incremental_export_specification=1, region_name="us-east-1")
    mock_client.export_table_to_point_in_time.assert_called_once()

def test_import_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import import_table
    mock_client = MagicMock()
    mock_client.import_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    import_table("test-s3_bucket_source", "test-input_format", "test-table_creation_parameters", client_token="test-client_token", input_format_options={}, input_compression_type="test-input_compression_type", region_name="us-east-1")
    mock_client.import_table.assert_called_once()

def test_list_backups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_backups
    mock_client = MagicMock()
    mock_client.list_backups.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_backups(table_name="test-table_name", limit=1, time_range_lower_bound="test-time_range_lower_bound", time_range_upper_bound="test-time_range_upper_bound", exclusive_start_backup_arn="test-exclusive_start_backup_arn", backup_type="test-backup_type", region_name="us-east-1")
    mock_client.list_backups.assert_called_once()

def test_list_contributor_insights_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_contributor_insights
    mock_client = MagicMock()
    mock_client.list_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_contributor_insights(table_name="test-table_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_contributor_insights.assert_called_once()

def test_list_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_exports
    mock_client = MagicMock()
    mock_client.list_exports.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_exports(table_arn="test-table_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_exports.assert_called_once()

def test_list_global_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_global_tables
    mock_client = MagicMock()
    mock_client.list_global_tables.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_global_tables(exclusive_start_global_table_name="test-exclusive_start_global_table_name", limit=1, target_region_name="test-target_region_name", region_name="us-east-1")
    mock_client.list_global_tables.assert_called_once()

def test_list_imports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_imports
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_imports(table_arn="test-table_arn", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_imports.assert_called_once()

def test_list_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_tables
    mock_client = MagicMock()
    mock_client.list_tables.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_tables(exclusive_start_table_name="test-exclusive_start_table_name", limit=1, region_name="us-east-1")
    mock_client.list_tables.assert_called_once()

def test_list_tags_of_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import list_tags_of_resource
    mock_client = MagicMock()
    mock_client.list_tags_of_resource.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    list_tags_of_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_of_resource.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "{}", expected_revision_id="test-expected_revision_id", confirm_remove_self_resource_access=True, region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_restore_table_from_backup_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import restore_table_from_backup
    mock_client = MagicMock()
    mock_client.restore_table_from_backup.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    restore_table_from_backup("test-target_table_name", "test-backup_arn", billing_mode_override="test-billing_mode_override", global_secondary_index_override="test-global_secondary_index_override", local_secondary_index_override="test-local_secondary_index_override", provisioned_throughput_override="test-provisioned_throughput_override", on_demand_throughput_override="test-on_demand_throughput_override", sse_specification_override={}, region_name="us-east-1")
    mock_client.restore_table_from_backup.assert_called_once()

def test_restore_table_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import restore_table_to_point_in_time
    mock_client = MagicMock()
    mock_client.restore_table_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    restore_table_to_point_in_time("test-target_table_name", source_table_arn="test-source_table_arn", source_table_name="test-source_table_name", use_latest_restorable_time=True, restore_date_time="test-restore_date_time", billing_mode_override="test-billing_mode_override", global_secondary_index_override="test-global_secondary_index_override", local_secondary_index_override="test-local_secondary_index_override", provisioned_throughput_override="test-provisioned_throughput_override", on_demand_throughput_override="test-on_demand_throughput_override", sse_specification_override={}, region_name="us-east-1")
    mock_client.restore_table_to_point_in_time.assert_called_once()

def test_transact_get_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import transact_get_items
    mock_client = MagicMock()
    mock_client.transact_get_items.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    transact_get_items("test-transact_items", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.transact_get_items.assert_called_once()

def test_transact_write_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import transact_write_items
    mock_client = MagicMock()
    mock_client.transact_write_items.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    transact_write_items("test-transact_items", return_consumed_capacity="test-return_consumed_capacity", return_item_collection_metrics="test-return_item_collection_metrics", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.transact_write_items.assert_called_once()

def test_update_contributor_insights_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import update_contributor_insights
    mock_client = MagicMock()
    mock_client.update_contributor_insights.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_contributor_insights("test-table_name", "test-contributor_insights_action", index_name="test-index_name", contributor_insights_mode="test-contributor_insights_mode", region_name="us-east-1")
    mock_client.update_contributor_insights.assert_called_once()

def test_update_global_table_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import update_global_table_settings
    mock_client = MagicMock()
    mock_client.update_global_table_settings.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_global_table_settings("test-global_table_name", global_table_billing_mode="test-global_table_billing_mode", global_table_provisioned_write_capacity_units="test-global_table_provisioned_write_capacity_units", global_table_provisioned_write_capacity_auto_scaling_settings_update={}, global_table_global_secondary_index_settings_update={}, replica_settings_update={}, region_name="us-east-1")
    mock_client.update_global_table_settings.assert_called_once()

def test_update_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import update_kinesis_streaming_destination
    mock_client = MagicMock()
    mock_client.update_kinesis_streaming_destination.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_kinesis_streaming_destination("test-table_name", "test-stream_arn", update_kinesis_streaming_configuration={}, region_name="us-east-1")
    mock_client.update_kinesis_streaming_destination.assert_called_once()

def test_update_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import update_table
    mock_client = MagicMock()
    mock_client.update_table.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_table("test-table_name", attribute_definitions={}, billing_mode="test-billing_mode", provisioned_throughput="test-provisioned_throughput", global_secondary_index_updates="test-global_secondary_index_updates", stream_specification={}, sse_specification={}, replica_updates="test-replica_updates", table_class="test-table_class", deletion_protection_enabled="test-deletion_protection_enabled", multi_region_consistency=True, global_table_witness_updates="test-global_table_witness_updates", on_demand_throughput="test-on_demand_throughput", warm_throughput="test-warm_throughput", region_name="us-east-1")
    mock_client.update_table.assert_called_once()

def test_update_table_replica_auto_scaling_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.dynamodb import update_table_replica_auto_scaling
    mock_client = MagicMock()
    mock_client.update_table_replica_auto_scaling.return_value = {}
    monkeypatch.setattr("aws_util.dynamodb.get_client", lambda *a, **kw: mock_client)
    update_table_replica_auto_scaling("test-table_name", global_secondary_index_updates="test-global_secondary_index_updates", provisioned_write_capacity_auto_scaling_update="test-provisioned_write_capacity_auto_scaling_update", replica_updates="test-replica_updates", region_name="us-east-1")
    mock_client.update_table_replica_auto_scaling.assert_called_once()
