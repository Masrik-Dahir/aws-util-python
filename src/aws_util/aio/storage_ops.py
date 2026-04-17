"""Native async storage_ops utilities using :mod:`aws_util.aio._engine`.

Provides async counterparts for every function in :mod:`aws_util.storage_ops`.
Models are re-exported from the sync module — there is no duplication.

- **efs_to_s3_sync** — async DataSync EFS → S3 pipeline with DynamoDB tracking.
- **fsx_backup_to_s3** — async FSx backup with polling and S3 metadata write.
- **transfer_family_event_processor** — async file validation, move, and SNS notify.
- **storage_gateway_cache_monitor** — async cache check with CloudWatch alarm.
- **lightsail_snapshot_to_s3** — async snapshot export and S3 metadata write.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.storage_ops import (
    CacheMonitorResult,
    EfsS3SyncResult,
    FsxBackupResult,
    LightsailExportResult,
    TransferEventResult,
)

logger = logging.getLogger(__name__)

__all__ = [
    "CacheMonitorResult",
    "EfsS3SyncResult",
    "FsxBackupResult",
    "LightsailExportResult",
    "TransferEventResult",
    "efs_to_s3_sync",
    "fsx_backup_to_s3",
    "lightsail_snapshot_to_s3",
    "storage_gateway_cache_monitor",
    "transfer_family_event_processor",
]


async def efs_to_s3_sync(
    efs_filesystem_id: str,
    source_subnet_arn: str,
    source_security_group_arns: list[str],
    bucket: str,
    key_prefix: str,
    table_name: str,
    region_name: str | None = None,
) -> EfsS3SyncResult:
    """Describe EFS access points, create a DataSync task from EFS to S3, start the task execution, and track sync state in DynamoDB.

    Async counterpart of :func:`aws_util.storage_ops.efs_to_s3_sync`.

    Args:
        efs_filesystem_id: EFS file system ID.
        source_subnet_arn: ARN of the subnet for the EFS mount target.
        source_security_group_arns: Security group ARNs for the DataSync agent.
        bucket: Destination S3 bucket name.
        key_prefix: Key prefix within the S3 bucket.
        table_name: DynamoDB table name for recording sync metadata.
        region_name: AWS region override.

    Returns:
        An :class:`EfsS3SyncResult` with task_arn, execution_arn, and status.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    datasync = async_client("datasync", region_name)
    ddb = async_client("dynamodb", region_name)

    # ------------------------------------------------------------------
    # 1. Create DataSync EFS source location
    # ------------------------------------------------------------------
    logger.info("Creating DataSync EFS source location for %r", efs_filesystem_id)
    region = region_name or "us-east-1"
    try:
        src_resp = await datasync.call(
            "CreateLocationEfs",
            EfsFilesystemArn=(
                f"arn:aws:elasticfilesystem:{region}:*:file-system/{efs_filesystem_id}"
            ),
            Ec2Config={
                "SubnetArn": source_subnet_arn,
                "SecurityGroupArns": source_security_group_arns,
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create DataSync EFS source location for {efs_filesystem_id!r}",
        ) from exc

    source_location_arn: str = src_resp["LocationArn"]
    logger.info("EFS source location created: %s", source_location_arn)

    # ------------------------------------------------------------------
    # 2. Create DataSync S3 destination location
    # ------------------------------------------------------------------
    logger.info("Creating DataSync S3 destination location for s3://%s/%s", bucket, key_prefix)
    try:
        dst_resp = await datasync.call(
            "CreateLocationS3",
            S3BucketArn=f"arn:aws:s3:::{bucket}",
            Subdirectory=key_prefix,
            S3Config={
                "BucketAccessRoleArn": "arn:aws:iam::*:role/DataSyncS3BucketAccessRole",
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to create DataSync S3 destination location for {bucket!r}"
        ) from exc

    dest_location_arn: str = dst_resp["LocationArn"]
    logger.info("S3 destination location created: %s", dest_location_arn)

    # ------------------------------------------------------------------
    # 3. Create DataSync task
    # ------------------------------------------------------------------
    task_name = f"efs-{efs_filesystem_id}-to-{bucket}"
    logger.info("Creating DataSync task %r", task_name)
    try:
        task_resp = await datasync.call(
            "CreateTask",
            SourceLocationArn=source_location_arn,
            DestinationLocationArn=dest_location_arn,
            Name=task_name,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to create DataSync task") from exc

    task_arn: str = task_resp["TaskArn"]
    logger.info("DataSync task created: %s", task_arn)

    # ------------------------------------------------------------------
    # 4. Start task execution
    # ------------------------------------------------------------------
    try:
        exec_resp = await datasync.call("StartTaskExecution", TaskArn=task_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to start DataSync task {task_arn!r}") from exc

    execution_arn: str = exec_resp["TaskExecutionArn"]
    logger.info("DataSync task execution started: %s", execution_arn)

    # ------------------------------------------------------------------
    # 5. Record sync metadata in DynamoDB
    # ------------------------------------------------------------------
    record: dict[str, Any] = {
        "task_arn": {"S": task_arn},
        "execution_arn": {"S": execution_arn},
        "efs_filesystem_id": {"S": efs_filesystem_id},
        "s3_bucket": {"S": bucket},
        "s3_prefix": {"S": key_prefix},
        "status": {"S": "LAUNCHED"},
        "started_at": {"S": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
    }
    try:
        await ddb.call("PutItem", TableName=table_name, Item=record)
        logger.info("Sync metadata recorded in DynamoDB table %r", table_name)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to record sync metadata in DynamoDB table {table_name!r}"
        ) from exc

    return EfsS3SyncResult(
        task_arn=task_arn,
        execution_arn=execution_arn,
        status="LAUNCHED",
    )


async def fsx_backup_to_s3(
    file_system_id: str,
    backup_name: str,
    bucket: str,
    key_prefix: str,
    region_name: str | None = None,
) -> FsxBackupResult:
    """Create an FSx backup, poll until available, and record backup metadata in S3.

    Async counterpart of :func:`aws_util.storage_ops.fsx_backup_to_s3`.

    Args:
        file_system_id: FSx file system ID.
        backup_name: Tag value used to name/identify the backup.
        bucket: S3 bucket for storing backup metadata.
        key_prefix: S3 key prefix for the metadata object.
        region_name: AWS region override.

    Returns:
        A :class:`FsxBackupResult` with backup_id, status, and s3_metadata_key.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    import asyncio

    fsx = async_client("fsx", region_name)
    s3 = async_client("s3", region_name)

    # ------------------------------------------------------------------
    # 1. Create FSx backup with name tag
    # ------------------------------------------------------------------
    logger.info("Creating FSx backup for file system %r (name=%r)", file_system_id, backup_name)
    try:
        backup_resp = await fsx.call(
            "CreateBackup",
            FileSystemId=file_system_id,
            Tags=[{"Key": "Name", "Value": backup_name}],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to create FSx backup for file system {file_system_id!r}"
        ) from exc

    backup = backup_resp["Backup"]
    backup_id: str = backup["BackupId"]
    backup_status: str = backup.get("Lifecycle", "CREATING")
    logger.info("FSx backup %r created, polling for completion", backup_id)

    # ------------------------------------------------------------------
    # 2. Poll describe_backups until AVAILABLE (max 60 iters, 15s sleep)
    # ------------------------------------------------------------------
    terminal_statuses = {"AVAILABLE", "FAILED", "DELETED"}
    max_iterations = 60
    iteration = 0

    while backup_status not in terminal_statuses and iteration < max_iterations:
        await asyncio.sleep(15)
        iteration += 1
        try:
            desc_resp = await fsx.call("DescribeBackups", BackupIds=[backup_id])
        except RuntimeError as exc:
            raise wrap_aws_error(exc, f"Failed to describe FSx backup {backup_id!r}") from exc
        backups = desc_resp.get("Backups", [])
        if backups:
            backup_status = backups[0].get("Lifecycle", backup_status)
        logger.debug(
            "FSx backup %s status: %s (iter %d/%d)",
            backup_id,
            backup_status,
            iteration,
            max_iterations,
        )

    logger.info("FSx backup %s reached status: %s", backup_id, backup_status)

    # ------------------------------------------------------------------
    # 3. Write JSON metadata to S3
    # ------------------------------------------------------------------
    metadata = {
        "backup_id": backup_id,
        "file_system_id": file_system_id,
        "backup_name": backup_name,
        "status": backup_status,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    s3_key = f"{key_prefix.rstrip('/')}/{backup_id}.json"
    logger.info("Writing backup metadata to s3://%s/%s", bucket, s3_key)
    try:
        await s3.call(
            "PutObject",
            Bucket=bucket,
            Key=s3_key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to write FSx backup metadata to s3://{bucket}/{s3_key}"
        ) from exc

    return FsxBackupResult(
        backup_id=backup_id,
        status=backup_status,
        s3_metadata_key=s3_key,
    )


async def transfer_family_event_processor(
    server_id: str,
    bucket: str,
    destination_prefix: str,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> TransferEventResult:
    """List recent Transfer Family server sessions, validate uploaded files exist in S3, move to versioned prefix, and notify via SNS.

    Async counterpart of
    :func:`aws_util.storage_ops.transfer_family_event_processor`.

    Args:
        server_id: Transfer Family server ID.
        bucket: S3 bucket used by the Transfer Family server.
        destination_prefix: S3 key prefix for moved (versioned) files.
        sns_topic_arn: Optional SNS topic ARN for per-file notifications.
        region_name: AWS region override.

    Returns:
        A :class:`TransferEventResult` with files_processed count,
        files_moved list, and notifications_sent count.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    transfer = async_client("transfer", region_name)
    s3 = async_client("s3", region_name)

    files_moved: list[str] = []
    notifications_sent = 0

    # ------------------------------------------------------------------
    # 1. List workflow executions for the server
    # ------------------------------------------------------------------
    logger.info("Listing executions for Transfer Family server %r", server_id)
    try:
        exec_resp = await transfer.call("ListExecutions", WorkflowId=server_id)
        executions: list[dict[str, Any]] = exec_resp.get("Executions", [])
    except RuntimeError as exc:
        logger.warning(
            "ListExecutions failed for server %r — proceeding with empty list: %s",
            server_id,
            exc,
        )
        executions = []

    logger.info("Found %d executions", len(executions))

    # ------------------------------------------------------------------
    # 2. For each completed execution, validate S3 object, copy, delete, notify
    # ------------------------------------------------------------------
    for execution in executions:
        exec_status: str = execution.get("Status", "")
        if exec_status != "COMPLETED":
            continue

        initial_file: dict[str, Any] = execution.get("InitialFile", {})
        source_key: str = initial_file.get("Path", "")
        if not source_key:
            continue

        # Validate the file exists in S3
        try:
            await s3.call("HeadObject", Bucket=bucket, Key=source_key)
        except RuntimeError as exc:
            error_msg = str(exc)
            if "404" in error_msg or "NoSuchKey" in error_msg:
                logger.warning("File s3://%s/%s not found — skipping", bucket, source_key)
                continue
            raise wrap_aws_error(
                exc, f"Failed to check existence of s3://{bucket}/{source_key}"
            ) from exc

        # Build the versioned destination key
        filename = source_key.split("/")[-1]
        timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        dest_key = f"{destination_prefix.rstrip('/')}/{timestamp}/{filename}"

        # Copy to destination_prefix
        try:
            await s3.call(
                "CopyObject",
                Bucket=bucket,
                CopySource={"Bucket": bucket, "Key": source_key},
                Key=dest_key,
            )
            logger.debug("Copied s3://%s/%s -> %s", bucket, source_key, dest_key)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"Failed to copy s3://{bucket}/{source_key} to {dest_key}",
            ) from exc

        # Delete the original
        try:
            await s3.call("DeleteObject", Bucket=bucket, Key=source_key)
            logger.debug("Deleted original: s3://%s/%s", bucket, source_key)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"Failed to delete original s3://{bucket}/{source_key}"
            ) from exc

        files_moved.append(dest_key)

        # Publish SNS notification
        if sns_topic_arn:
            sns = async_client("sns", region_name)
            message = json.dumps(
                {
                    "server_id": server_id,
                    "source_key": source_key,
                    "dest_key": dest_key,
                    "bucket": bucket,
                    "moved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                }
            )
            try:
                await sns.call(
                    "Publish",
                    TopicArn=sns_topic_arn,
                    Subject=f"Transfer Family file moved: {filename}",
                    Message=message,
                )
                notifications_sent += 1
                logger.debug("SNS notification sent for %r", dest_key)
            except RuntimeError as exc:
                raise wrap_aws_error(
                    exc,
                    f"Failed to publish SNS notification to {sns_topic_arn!r}",
                ) from exc

    logger.info(
        "Transfer event processing complete: %d files moved, %d notifications sent",
        len(files_moved),
        notifications_sent,
    )
    return TransferEventResult(
        files_processed=len(files_moved),
        files_moved=files_moved,
        notifications_sent=notifications_sent,
    )


async def storage_gateway_cache_monitor(
    gateway_arn: str,
    alarm_threshold_percent: float = 80.0,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> CacheMonitorResult:
    """Describe Storage Gateway cache info, check utilization against threshold, and publish a CloudWatch alarm if needed.

    Async counterpart of
    :func:`aws_util.storage_ops.storage_gateway_cache_monitor`.

    Args:
        gateway_arn: Full ARN of the Storage Gateway.
        alarm_threshold_percent: Cache usage percentage threshold that
            triggers alarm creation (default ``80.0``).
        sns_topic_arn: Optional SNS topic ARN used as the alarm action.
        region_name: AWS region override.

    Returns:
        A :class:`CacheMonitorResult` with gateway_id, cache_used_percent,
        cache_allocated_bytes, and alarm_created flag.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    sgw = async_client("storagegateway", region_name)
    cw = async_client("cloudwatch", region_name)

    # ------------------------------------------------------------------
    # 1. describe_cache to get utilization
    # ------------------------------------------------------------------
    logger.info("Describing cache for Storage Gateway %r", gateway_arn)
    try:
        cache_resp = await sgw.call("DescribeCache", GatewayARN=gateway_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to describe cache for gateway {gateway_arn!r}") from exc

    gateway_id: str = cache_resp.get("GatewayARN", gateway_arn).split("/")[-1]
    cache_allocated: int = cache_resp.get("CacheAllocatedInBytes", 0)
    cache_used_pct: float = cache_resp.get("CacheUsedPercentage", 0.0)

    logger.info(
        "Gateway %s: cache %d bytes allocated, %.1f%% used",
        gateway_id,
        cache_allocated,
        cache_used_pct,
    )

    # ------------------------------------------------------------------
    # 2. If above threshold, put_metric_alarm on CloudWatch
    # ------------------------------------------------------------------
    alarm_created = False

    if cache_used_pct >= alarm_threshold_percent:
        alarm_name = f"StorageGateway-CacheUsage-{gateway_id}"
        alarm_actions: list[str] = [sns_topic_arn] if sns_topic_arn else []

        logger.info(
            "Cache utilization %.1f%% >= threshold %.1f%%, creating alarm %r",
            cache_used_pct,
            alarm_threshold_percent,
            alarm_name,
        )
        try:
            await cw.call(
                "PutMetricAlarm",
                AlarmName=alarm_name,
                AlarmDescription=(
                    f"Storage Gateway cache utilization exceeds "
                    f"{alarm_threshold_percent:.0f}% for gateway {gateway_id}"
                ),
                Namespace="AWS/StorageGateway",
                MetricName="CacheUsed",
                Dimensions=[{"Name": "GatewayId", "Value": gateway_id}],
                Statistic="Average",
                Period=300,
                EvaluationPeriods=2,
                Threshold=alarm_threshold_percent,
                ComparisonOperator="GreaterThanOrEqualToThreshold",
                TreatMissingData="notBreaching",
                AlarmActions=alarm_actions,
                OKActions=alarm_actions,
            )
            alarm_created = True
            logger.info("CloudWatch alarm %r created", alarm_name)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"Failed to create CloudWatch alarm for gateway {gateway_id!r}"
            ) from exc

    return CacheMonitorResult(
        gateway_id=gateway_id,
        cache_used_percent=cache_used_pct,
        cache_allocated_bytes=cache_allocated,
        alarm_created=alarm_created,
    )


async def lightsail_snapshot_to_s3(
    instance_name: str,
    snapshot_name: str,
    bucket: str,
    key_prefix: str,
    region_name: str | None = None,
) -> LightsailExportResult:
    """Create a Lightsail instance snapshot, export to EC2, and record export metadata in S3.

    Async counterpart of :func:`aws_util.storage_ops.lightsail_snapshot_to_s3`.

    Args:
        instance_name: Lightsail instance name to snapshot.
        snapshot_name: Name for the new Lightsail snapshot.
        bucket: S3 bucket for storing export metadata.
        key_prefix: S3 key prefix for the metadata object.
        region_name: AWS region override.

    Returns:
        A :class:`LightsailExportResult` with snapshot_name, export_arn,
        and s3_metadata_key.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    import asyncio

    ls = async_client("lightsail", region_name)
    s3 = async_client("s3", region_name)

    # ------------------------------------------------------------------
    # 1. Create Lightsail instance snapshot
    # ------------------------------------------------------------------
    logger.info("Creating Lightsail snapshot %r for instance %r", snapshot_name, instance_name)
    try:
        await ls.call(
            "CreateInstanceSnapshot",
            instanceSnapshotName=snapshot_name,
            instanceName=instance_name,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create Lightsail snapshot {snapshot_name!r} for instance {instance_name!r}",
        ) from exc

    logger.info("Snapshot creation initiated — polling for availability")

    # ------------------------------------------------------------------
    # 2. Poll get_instance_snapshot until state == "available"
    # ------------------------------------------------------------------
    snapshot_state = "pending"
    max_iterations = 60
    iteration = 0

    while snapshot_state != "available" and iteration < max_iterations:
        await asyncio.sleep(15)
        iteration += 1
        try:
            snap_resp = await ls.call("GetInstanceSnapshot", instanceSnapshotName=snapshot_name)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"Failed to get Lightsail snapshot {snapshot_name!r}"
            ) from exc
        snapshot_state = snap_resp.get("instanceSnapshot", {}).get("state", snapshot_state)
        logger.debug(
            "Snapshot %s state: %s (iter %d/%d)",
            snapshot_name,
            snapshot_state,
            iteration,
            max_iterations,
        )

    logger.info("Snapshot %r reached state: %s", snapshot_name, snapshot_state)

    # ------------------------------------------------------------------
    # 3. Export snapshot to EC2
    # ------------------------------------------------------------------
    export_arn: str | None = None

    if snapshot_state == "available":
        logger.info("Exporting Lightsail snapshot %r to EC2", snapshot_name)
        try:
            export_resp = await ls.call("ExportSnapshot", sourceSnapshotName=snapshot_name)
            operations: list[dict[str, Any]] = export_resp.get("operations", [])
            if operations:
                export_arn = operations[0].get("resourceArn") or operations[0].get("id")
            logger.info("Export initiated: export_arn=%s", export_arn)
        except RuntimeError as exc:
            logger.warning(
                "Lightsail snapshot export failed (snapshot may still be creating): %s",
                exc,
            )
    else:
        logger.warning(
            "Snapshot %r not available after %d iterations — skipping export",
            snapshot_name,
            max_iterations,
        )

    # ------------------------------------------------------------------
    # 4. Write metadata JSON to S3
    # ------------------------------------------------------------------
    metadata = {
        "snapshot_name": snapshot_name,
        "instance_name": instance_name,
        "snapshot_state": snapshot_state,
        "export_arn": export_arn,
        "exported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    s3_key = f"{key_prefix.rstrip('/')}/{snapshot_name}.json"
    logger.info("Writing export metadata to s3://%s/%s", bucket, s3_key)
    try:
        await s3.call(
            "PutObject",
            Bucket=bucket,
            Key=s3_key,
            Body=json.dumps(metadata, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to write Lightsail export metadata to s3://{bucket}/{s3_key}",
        ) from exc

    return LightsailExportResult(
        snapshot_name=snapshot_name,
        export_arn=export_arn,
        s3_metadata_key=s3_key,
    )
