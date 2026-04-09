"""Tests for aws_util.timestream_query module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.timestream_query as tsq_mod
from aws_util.timestream_query import (
    ColumnInfo,
    EndpointInfo,
    QueryResult,
    Row,
    ScheduledQueryDescription,
    _parse_column_info,
    _parse_query_result,
    _parse_row,
    _parse_scheduled_query,
    cancel_query,
    create_scheduled_query,
    delete_scheduled_query,
    describe_endpoints,
    execute_scheduled_query,
    list_scheduled_queries,
    query,
    run_query,
    describe_account_settings,
    describe_scheduled_query,
    list_tags_for_resource,
    prepare_query,
    tag_resource,
    untag_resource,
    update_account_settings,
    update_scheduled_query,
)

REGION = "us-east-1"
QUERY_ID = "qid-12345"
SQ_ARN = "arn:aws:timestream:us-east-1:123:scheduled-query/my-sq"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_column_info(monkeypatch):
    ci = _parse_column_info({"Name": "host", "Type": {"ScalarType": "VARCHAR"}})
    assert ci.name == "host"
    assert ci.type_name == "VARCHAR"


def test_parse_column_info_no_type():
    ci = _parse_column_info({"Name": "x"})
    assert ci.type_name is None


def test_parse_column_info_empty_type():
    ci = _parse_column_info({"Name": "x", "Type": {}})
    assert ci.type_name is None


def test_parse_row():
    r = _parse_row({"Data": [{"ScalarValue": "1"}]})
    assert r.data == [{"ScalarValue": "1"}]


def test_parse_row_empty():
    r = _parse_row({})
    assert r.data == []


def test_parse_query_result():
    resp = {
        "QueryId": QUERY_ID,
        "Rows": [{"Data": [{"ScalarValue": "v"}]}],
        "ColumnInfo": [{"Name": "col1", "Type": {"ScalarType": "VARCHAR"}}],
        "NextToken": "tok123",
    }
    qr = _parse_query_result(resp)
    assert qr.query_id == QUERY_ID
    assert len(qr.rows) == 1
    assert len(qr.column_info) == 1
    assert qr.next_token == "tok123"


def test_parse_scheduled_query():
    raw = {
        "Arn": SQ_ARN,
        "Name": "my-sq",
        "State": "ENABLED",
        "QueryString": "SELECT 1",
        "ScheduleConfiguration": {"ScheduleExpression": "rate(1 hour)"},
        "TargetConfiguration": {
            "TimestreamConfiguration": {
                "DatabaseName": "db1",
                "TableName": "t1",
            },
        },
        "CreationTime": "2024-01-01T00:00:00Z",
    }
    sq = _parse_scheduled_query(raw)
    assert sq.arn == SQ_ARN
    assert sq.name == "my-sq"
    assert sq.target_database == "db1"
    assert sq.target_table == "t1"


def test_parse_scheduled_query_alt_key():
    raw = {"ScheduledQueryArn": SQ_ARN, "ScheduledQueryName": "alt"}
    sq = _parse_scheduled_query(raw)
    assert sq.arn == SQ_ARN
    assert sq.name == "alt"


# ---------------------------------------------------------------------------
# query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_query_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query.return_value = {
        "QueryId": QUERY_ID,
        "Rows": [{"Data": []}],
        "ColumnInfo": [],
    }
    result = query("SELECT 1", region_name=REGION)
    assert result.query_id == QUERY_ID


@patch("aws_util.timestream_query.get_client")
def test_query_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query.side_effect = _client_error("ValidationException")
    with pytest.raises(RuntimeError):
        query("BAD SQL", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_endpoints
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_describe_endpoints_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.return_value = {
        "Endpoints": [
            {"Address": "endpoint.example.com", "CachePeriodInMinutes": 10},
        ],
    }
    result = describe_endpoints(region_name=REGION)
    assert len(result) == 1
    assert result[0].address == "endpoint.example.com"
    assert result[0].cache_period_in_minutes == 10


@patch("aws_util.timestream_query.get_client")
def test_describe_endpoints_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.side_effect = _client_error("InternalServerError")
    with pytest.raises(RuntimeError):
        describe_endpoints(region_name=REGION)


# ---------------------------------------------------------------------------
# cancel_query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_cancel_query_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_query.return_value = {}
    result = cancel_query(QUERY_ID, region_name=REGION)
    assert result is True


@patch("aws_util.timestream_query.get_client")
def test_cancel_query_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_query.side_effect = _client_error("InvalidEndpointException")
    with pytest.raises(RuntimeError):
        cancel_query(QUERY_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_run_query_single_page(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query.return_value = {
        "QueryId": QUERY_ID,
        "Rows": [{"Data": [{"ScalarValue": "1"}]}],
        "ColumnInfo": [{"Name": "c", "Type": {"ScalarType": "BIGINT"}}],
    }
    result = run_query("SELECT 1", region_name=REGION)
    assert result.query_id == QUERY_ID
    assert len(result.rows) == 1


@patch("aws_util.timestream_query.get_client")
def test_run_query_multi_page(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query.side_effect = [
        {
            "QueryId": QUERY_ID,
            "Rows": [{"Data": [{"ScalarValue": "1"}]}],
            "ColumnInfo": [{"Name": "c", "Type": {"ScalarType": "BIGINT"}}],
            "NextToken": "page2",
        },
        {
            "QueryId": QUERY_ID,
            "Rows": [{"Data": [{"ScalarValue": "2"}]}],
            "ColumnInfo": [],
        },
    ]
    result = run_query("SELECT *", max_rows=1, region_name=REGION)
    assert len(result.rows) == 2


# ---------------------------------------------------------------------------
# create_scheduled_query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_create_scheduled_query_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_scheduled_query.return_value = {
        "ScheduledQuery": {
            "Arn": SQ_ARN,
            "Name": "sq1",
            "State": "ENABLED",
        },
    }
    result = create_scheduled_query(
        "sq1", "SELECT 1", "rate(1 hour)", region_name=REGION,
    )
    assert result.arn == SQ_ARN


@patch("aws_util.timestream_query.get_client")
def test_create_scheduled_query_all_options(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_scheduled_query.return_value = {
        "ScheduledQuery": {"Arn": SQ_ARN, "Name": "sq2"},
    }
    result = create_scheduled_query(
        "sq2",
        "SELECT 1",
        "rate(1 hour)",
        target_database="db",
        target_table="tbl",
        notification_sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
        scheduled_query_execution_role_arn="arn:aws:iam::123:role/r",
        tags=[{"Key": "env", "Value": "test"}],
        region_name=REGION,
    )
    assert result.arn == SQ_ARN


@patch("aws_util.timestream_query.get_client")
def test_create_scheduled_query_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_scheduled_query.side_effect = _client_error("ConflictException")
    with pytest.raises(RuntimeError):
        create_scheduled_query("sq", "SELECT 1", "rate(1 hour)", region_name=REGION)


# ---------------------------------------------------------------------------
# list_scheduled_queries
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_list_scheduled_queries_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_scheduled_queries.return_value = {
        "ScheduledQueries": [{"Arn": SQ_ARN, "Name": "sq1"}],
        "NextToken": "tok",
    }
    queries, token = list_scheduled_queries(max_results=10, region_name=REGION)
    assert len(queries) == 1
    assert token == "tok"


@patch("aws_util.timestream_query.get_client")
def test_list_scheduled_queries_with_token(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_scheduled_queries.return_value = {
        "ScheduledQueries": [],
    }
    queries, token = list_scheduled_queries(
        next_token="prev", region_name=REGION,
    )
    assert queries == []
    assert token is None


@patch("aws_util.timestream_query.get_client")
def test_list_scheduled_queries_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_scheduled_queries.side_effect = _client_error("AccessDeniedException")
    with pytest.raises(RuntimeError):
        list_scheduled_queries(region_name=REGION)


# ---------------------------------------------------------------------------
# execute_scheduled_query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_execute_scheduled_query_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.execute_scheduled_query.return_value = {}
    result = execute_scheduled_query(
        SQ_ARN, "2024-01-01T00:00:00Z", region_name=REGION,
    )
    assert result is True


@patch("aws_util.timestream_query.get_client")
def test_execute_scheduled_query_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.execute_scheduled_query.side_effect = _client_error(
        "ResourceNotFoundException",
    )
    with pytest.raises(RuntimeError):
        execute_scheduled_query(SQ_ARN, "2024-01-01T00:00:00Z", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_scheduled_query
# ---------------------------------------------------------------------------


@patch("aws_util.timestream_query.get_client")
def test_delete_scheduled_query_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_scheduled_query.return_value = {}
    result = delete_scheduled_query(SQ_ARN, region_name=REGION)
    assert result is True


@patch("aws_util.timestream_query.get_client")
def test_delete_scheduled_query_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_scheduled_query.side_effect = _client_error(
        "ResourceNotFoundException",
    )
    with pytest.raises(RuntimeError):
        delete_scheduled_query(SQ_ARN, region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_describe_account_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_settings.return_value = {}
    describe_account_settings(region_name=REGION)
    mock_client.describe_account_settings.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_describe_account_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to describe account settings"):
        describe_account_settings(region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_describe_scheduled_query(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_scheduled_query.return_value = {}
    describe_scheduled_query("test-scheduled_query_arn", region_name=REGION)
    mock_client.describe_scheduled_query.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_describe_scheduled_query_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_scheduled_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_query",
    )
    with pytest.raises(RuntimeError, match="Failed to describe scheduled query"):
        describe_scheduled_query("test-scheduled_query_arn", region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_prepare_query(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.prepare_query.return_value = {}
    prepare_query("test-query_string", region_name=REGION)
    mock_client.prepare_query.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_prepare_query_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.prepare_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "prepare_query",
    )
    with pytest.raises(RuntimeError, match="Failed to prepare query"):
        prepare_query("test-query_string", region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_update_account_settings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_account_settings.return_value = {}
    update_account_settings(region_name=REGION)
    mock_client.update_account_settings.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_update_account_settings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_settings",
    )
    with pytest.raises(RuntimeError, match="Failed to update account settings"):
        update_account_settings(region_name=REGION)


@patch("aws_util.timestream_query.get_client")
def test_update_scheduled_query(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_scheduled_query.return_value = {}
    update_scheduled_query("test-scheduled_query_arn", "test-state", region_name=REGION)
    mock_client.update_scheduled_query.assert_called_once()


@patch("aws_util.timestream_query.get_client")
def test_update_scheduled_query_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_scheduled_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_scheduled_query",
    )
    with pytest.raises(RuntimeError, match="Failed to update scheduled query"):
        update_scheduled_query("test-scheduled_query_arn", "test-state", region_name=REGION)


def test_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import query
    mock_client = MagicMock()
    mock_client.query.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    query("test-query_string", max_rows=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.query.assert_called_once()

def test_create_scheduled_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import create_scheduled_query
    mock_client = MagicMock()
    mock_client.create_scheduled_query.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    create_scheduled_query("test-name", "test-query_string", "test-schedule_expression", notification_sns_topic_arn="test-notification_sns_topic_arn", scheduled_query_execution_role_arn="test-scheduled_query_execution_role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_scheduled_query.assert_called_once()

def test_list_scheduled_queries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import list_scheduled_queries
    mock_client = MagicMock()
    mock_client.list_scheduled_queries.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    list_scheduled_queries(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_scheduled_queries.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_prepare_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import prepare_query
    mock_client = MagicMock()
    mock_client.prepare_query.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    prepare_query("test-query_string", validate_only="test-validate_only", region_name="us-east-1")
    mock_client.prepare_query.assert_called_once()

def test_update_account_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.timestream_query import update_account_settings
    mock_client = MagicMock()
    mock_client.update_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.timestream_query.get_client", lambda *a, **kw: mock_client)
    update_account_settings(max_query_tcu=1, query_pricing_model="test-query_pricing_model", query_compute="test-query_compute", region_name="us-east-1")
    mock_client.update_account_settings.assert_called_once()
