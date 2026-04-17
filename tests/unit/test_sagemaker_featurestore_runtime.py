"""Tests for aws_util.sagemaker_featurestore_runtime — 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.sagemaker_featurestore_runtime import (
    BatchGetRecordResult,
    FeatureRecord,
    batch_get_record,
    delete_record,
    get_record,
    put_record,
)

FG = "my-feature-group"
RID = "rec-123"
RECORD = [{"FeatureName": "id", "ValueAsString": "123"}]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_feature_record_defaults(self):
        r = FeatureRecord()
        assert r.feature_group_name == ""
        assert r.record_identifier_value == ""
        assert r.features == []

    def test_feature_record_full(self):
        r = FeatureRecord(
            feature_group_name=FG,
            record_identifier_value=RID,
            features=RECORD,
        )
        assert r.feature_group_name == FG
        assert r.features == RECORD

    def test_batch_get_record_result_defaults(self):
        r = BatchGetRecordResult()
        assert r.records == []
        assert r.errors == []
        assert r.unprocessed_identifiers == []


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------


class TestPutRecord:
    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        put_record(FG, RECORD)
        client.put_record.assert_called_once()

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_with_target_stores(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        put_record(FG, RECORD, target_stores=["OnlineStore"])
        args = client.put_record.call_args[1]
        assert args["TargetStores"] == ["OnlineStore"]

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_with_region(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        put_record(FG, RECORD, region_name="eu-west-1")
        mock_gc.assert_called_once_with("sagemaker-featurestore-runtime", "eu-west-1")

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.put_record.side_effect = ClientError(
            {"Error": {"Code": "ValidationException", "Message": "fail"}}, "PutRecord"
        )
        with pytest.raises(Exception):
            put_record(FG, RECORD)


# ---------------------------------------------------------------------------
# get_record
# ---------------------------------------------------------------------------


class TestGetRecord:
    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_record.return_value = {"Record": RECORD}
        result = get_record(FG, RID)
        assert isinstance(result, FeatureRecord)
        assert result.feature_group_name == FG
        assert result.features == RECORD

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_with_feature_names(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_record.return_value = {"Record": RECORD}
        get_record(FG, RID, feature_names=["id"])
        args = client.get_record.call_args[1]
        assert args["FeatureNames"] == ["id"]

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_record.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFound", "Message": "fail"}}, "GetRecord"
        )
        with pytest.raises(Exception):
            get_record(FG, RID)


# ---------------------------------------------------------------------------
# delete_record
# ---------------------------------------------------------------------------


class TestDeleteRecord:
    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_record(FG, RID, "2024-01-01T00:00:00Z")
        client.delete_record.assert_called_once()

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_with_target_stores(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        delete_record(FG, RID, "2024-01-01T00:00:00Z", target_stores=["OnlineStore"])
        args = client.delete_record.call_args[1]
        assert args["TargetStores"] == ["OnlineStore"]

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_record.side_effect = ClientError(
            {"Error": {"Code": "ValidationException", "Message": "fail"}}, "DeleteRecord"
        )
        with pytest.raises(Exception):
            delete_record(FG, RID, "2024-01-01T00:00:00Z")


# ---------------------------------------------------------------------------
# batch_get_record
# ---------------------------------------------------------------------------


class TestBatchGetRecord:
    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.batch_get_record.return_value = {
            "Records": [
                {
                    "FeatureGroupName": FG,
                    "RecordIdentifierValueAsString": RID,
                    "Record": RECORD,
                }
            ],
            "Errors": [],
            "UnprocessedIdentifiers": [],
        }
        result = batch_get_record([{"FeatureGroupName": FG, "RecordIdentifiersValueAsString": [RID]}])
        assert isinstance(result, BatchGetRecordResult)
        assert len(result.records) == 1
        assert result.records[0].feature_group_name == FG

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_empty_response(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.batch_get_record.return_value = {}
        result = batch_get_record([])
        assert result.records == []
        assert result.errors == []

    @patch("aws_util.sagemaker_featurestore_runtime.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.batch_get_record.side_effect = ClientError(
            {"Error": {"Code": "ValidationException", "Message": "fail"}}, "BatchGetRecord"
        )
        with pytest.raises(Exception):
            batch_get_record([])
