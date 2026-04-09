"""Native async sagemaker_featurestore_runtime utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.sagemaker_featurestore_runtime import (
    BatchGetRecordResult,
    FeatureRecord,
)

__all__ = [
    "BatchGetRecordResult",
    "FeatureRecord",
    "batch_get_record",
    "delete_record",
    "get_record",
    "put_record",
]


async def put_record(
    feature_group_name: str,
    record: list[dict[str, str]],
    target_stores: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Write a record to a SageMaker Feature Store feature group.

    Args:
        feature_group_name: Name of the feature group.
        record: List of feature name/value dicts.
        target_stores: Target stores (e.g. ``["OnlineStore"]``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the put fails.
    """
    client = async_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "Record": record,
    }
    if target_stores is not None:
        kwargs["TargetStores"] = target_stores
    try:
        await client.call("PutRecord", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "put_record failed") from exc


async def get_record(
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
    client = async_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "RecordIdentifierValueAsString": record_identifier_value,
    }
    if feature_names is not None:
        kwargs["FeatureNames"] = feature_names
    try:
        resp = await client.call("GetRecord", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "get_record failed") from exc
    return FeatureRecord(
        feature_group_name=feature_group_name,
        record_identifier_value=record_identifier_value,
        features=resp.get("Record", []),
    )


async def delete_record(
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
    client = async_client("sagemaker-featurestore-runtime", region_name)
    kwargs: dict[str, Any] = {
        "FeatureGroupName": feature_group_name,
        "RecordIdentifierValueAsString": record_identifier_value,
        "EventTime": event_time,
    }
    if target_stores is not None:
        kwargs["TargetStores"] = target_stores
    try:
        await client.call("DeleteRecord", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_record failed") from exc


async def batch_get_record(
    identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetRecordResult:
    """Batch-retrieve records from one or more feature groups.

    Args:
        identifiers: List of identifier dicts.
        region_name: AWS region override.

    Returns:
        A :class:`BatchGetRecordResult`.

    Raises:
        RuntimeError: If the batch-get fails.
    """
    client = async_client("sagemaker-featurestore-runtime", region_name)
    try:
        resp = await client.call(
            "BatchGetRecord",
            Identifiers=identifiers,
        )
    except RuntimeError:
        raise
    except Exception as exc:
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
