"""aws_util.sagemaker_featurestore_runtime -- SageMaker Feature Store Runtime.

Helpers for reading and writing records to SageMaker Feature Store
feature groups via the ``sagemaker-featurestore-runtime`` service.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchGetRecordResult",
    "FeatureRecord",
    "batch_get_record",
    "delete_record",
    "get_record",
    "put_record",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FeatureRecord(BaseModel):
    """A single feature record from SageMaker Feature Store."""

    model_config = ConfigDict(frozen=True)

    feature_group_name: str = ""
    record_identifier_value: str = ""
    features: list[dict[str, str]] = []


class BatchGetRecordResult(BaseModel):
    """Result of a batch-get-record call."""

    model_config = ConfigDict(frozen=True)

    records: list[FeatureRecord] = []
    errors: list[dict[str, Any]] = []
    unprocessed_identifiers: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def put_record(
    feature_group_name: str,
    record: list[dict[str, str]],
    target_stores: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Write a record to a SageMaker Feature Store feature group.

    Args:
        feature_group_name: Name of the feature group.
        record: List of feature name/value dicts, e.g.
            ``[{"FeatureName": "id", "ValueAsString": "123"}]``.
        target_stores: Target stores (e.g. ``["OnlineStore"]``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the put fails.
    """
    client = get_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "Record": record,
    }
    if target_stores is not None:
        kwargs["TargetStores"] = target_stores
    try:
        client.put_record(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "put_record failed") from exc


def get_record(
    feature_group_name: str,
    record_identifier_value: str,
    feature_names: list[str] | None = None,
    region_name: str | None = None,
) -> FeatureRecord:
    """Read a record from a SageMaker Feature Store feature group.

    Args:
        feature_group_name: Name of the feature group.
        record_identifier_value: The record identifier value.
        feature_names: Optional list of feature names to retrieve.
        region_name: AWS region override.

    Returns:
        A :class:`FeatureRecord` with the retrieved features.

    Raises:
        RuntimeError: If the get fails.
    """
    client = get_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "RecordIdentifierValueAsString": record_identifier_value,
    }
    if feature_names is not None:
        kwargs["FeatureNames"] = feature_names
    try:
        resp = client.get_record(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_record failed") from exc
    return FeatureRecord(
        feature_group_name=feature_group_name,
        record_identifier_value=record_identifier_value,
        features=resp.get("Record", []),
    )


def delete_record(
    feature_group_name: str,
    record_identifier_value: str,
    event_time: str,
    target_stores: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Delete a record from a SageMaker Feature Store feature group.

    Args:
        feature_group_name: Name of the feature group.
        record_identifier_value: The record identifier value.
        event_time: The event time of the record (ISO 8601).
        target_stores: Target stores to delete from.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the delete fails.
    """
    client = get_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "RecordIdentifierValueAsString": record_identifier_value,
        "EventTime": event_time,
    }
    if target_stores is not None:
        kwargs["TargetStores"] = target_stores
    try:
        client.delete_record(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_record failed") from exc


def batch_get_record(
    identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetRecordResult:
    """Batch-retrieve records from one or more feature groups.

    Args:
        identifiers: List of identifier dicts, each with
            ``FeatureGroupName``, ``RecordIdentifiersValueAsString``,
            and optionally ``FeatureNames``.
        region_name: AWS region override.

    Returns:
        A :class:`BatchGetRecordResult` with records, errors, and
        unprocessed identifiers.

    Raises:
        RuntimeError: If the batch-get fails.
    """
    client = get_client("sagemaker-featurestore-runtime", region_name)
    try:
        resp = client.batch_get_record(Identifiers=identifiers)
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_get_record failed") from exc
    records = [
        FeatureRecord(
            feature_group_name=r.get("FeatureGroupName", ""),
            record_identifier_value=r.get("RecordIdentifierValueAsString", ""),
            features=r.get("Record", []),
        )
        for r in resp.get("Records", [])
    ]
    return BatchGetRecordResult(
        records=records,
        errors=resp.get("Errors", []),
        unprocessed_identifiers=resp.get("UnprocessedIdentifiers", []),
    )
