"""IoT Pipeline utilities for multi-service orchestration.

Provides helpers for chaining IoT services with other AWS services:

- **IoT telemetry to Timestream** — Create/ensure an IoT topic rule that
  routes device telemetry to Timestream; creates database/table if absent.
- **IoT device shadow sync** — Read device shadow, diff desired vs reported
  state, and store the reconciled state in DynamoDB for fleet management.
- **IoT fleet command broadcaster** — Create an IoT Job targeting a thing
  group, store the job document in S3, and track metadata in DynamoDB.
- **IoT alert to SNS** — Query SiteWise asset property values, evaluate
  threshold breaches, and publish structured alerts to SNS.
- **Greengrass component deployer** — Upload a Lambda ZIP to S3, register
  a Greengrass v2 component version, and trigger a deployment.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "DeviceShadowSyncResult",
    "FleetCommandResult",
    "GreengrassDeployResult",
    "IoTAlertResult",
    "IoTTimestreamRuleResult",
    "iot_alert_to_sns",
    "iot_device_shadow_sync",
    "iot_fleet_command_broadcaster",
    "iot_greengrass_component_deployer",
    "iot_telemetry_to_timestream",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class IoTTimestreamRuleResult(BaseModel):
    """Result of the IoT-to-Timestream pipeline setup."""

    model_config = ConfigDict(frozen=True)

    rule_name: str
    rule_arn: str
    database_name: str
    table_name: str
    created_database: bool
    created_table: bool


class DeviceShadowSyncResult(BaseModel):
    """Result of a device shadow sync operation."""

    model_config = ConfigDict(frozen=True)

    thing_name: str
    reported_state: dict[str, Any]
    desired_state: dict[str, Any]
    delta_keys: list[str]
    synced_to_dynamodb: bool


class FleetCommandResult(BaseModel):
    """Result of broadcasting a command to a device fleet via IoT Job."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    job_arn: str
    targets_count: int
    document_key: str


class IoTAlertResult(BaseModel):
    """Result of an IoT SiteWise threshold-alert evaluation."""

    model_config = ConfigDict(frozen=True)

    asset_id: str
    property_id: str
    current_value: float
    threshold_breached: bool
    message_id: str | None = None


class GreengrassDeployResult(BaseModel):
    """Result of a Greengrass v2 component deployment."""

    model_config = ConfigDict(frozen=True)

    component_arn: str
    deployment_id: str
    artifact_key: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_COMPARISON_OPS: dict[str, Any] = {
    "GT": lambda v, t: v > t,
    "LT": lambda v, t: v < t,
    "GTE": lambda v, t: v >= t,
    "LTE": lambda v, t: v <= t,
}


# ---------------------------------------------------------------------------
# 1. IoT Telemetry to Timestream
# ---------------------------------------------------------------------------


def iot_telemetry_to_timestream(
    rule_name: str,
    topic_filter: str,
    database_name: str,
    table_name: str,
    role_arn: str,
    dimensions: list[dict[str, str]],
    region_name: str | None = None,
) -> IoTTimestreamRuleResult:
    """Create/ensure an IoT topic rule that routes telemetry to Timestream.

    Creates the Timestream database and table when they don't already exist,
    then creates (or replaces) an IoT topic rule with a Timestream action that
    forwards every message matching *topic_filter* to the specified table.

    Args:
        rule_name: Name of the IoT topic rule to create or replace.
        topic_filter: MQTT topic filter expression for the SQL query
            (e.g. ``"factory/+/telemetry"``).
        database_name: Timestream database name to route data into.
        table_name: Timestream table name within *database_name*.
        role_arn: IAM role ARN that IoT Core assumes to write to Timestream.
        dimensions: List of dicts with ``"name"`` and ``"value"`` keys
            specifying Timestream dimension mappings, e.g.
            ``[{"name": "device_id", "value": "${clientId()}"}]``.
        region_name: AWS region override.

    Returns:
        An :class:`IoTTimestreamRuleResult` containing the rule ARN,
        database/table names, and flags indicating whether the database
        and table were created by this call.

    Raises:
        RuntimeError: If any AWS service call fails.
    """
    iot = get_client("iot", region_name=region_name)
    ts_write = get_client("timestream-write", region_name=region_name)

    # --- Ensure Timestream database exists ---
    created_database = False
    try:
        ts_write.create_database(DatabaseName=database_name)
        created_database = True
        logger.info("Created Timestream database %s", database_name)
    except ClientError as exc:
        code = exc.response["Error"].get("Code", "")
        if code not in (
            "ConflictException",
            "ResourceAlreadyExistsException",
        ):
            raise wrap_aws_error(
                exc, f"Failed to create Timestream database {database_name}"
            ) from exc
        logger.debug("Timestream database %s already exists", database_name)

    # --- Ensure Timestream table exists ---
    created_table = False
    try:
        ts_write.create_table(
            DatabaseName=database_name,
            TableName=table_name,
            RetentionProperties={
                "MemoryStoreRetentionPeriodInHours": 24,
                "MagneticStoreRetentionPeriodInDays": 365,
            },
        )
        created_table = True
        logger.info("Created Timestream table %s.%s", database_name, table_name)
    except ClientError as exc:
        code = exc.response["Error"].get("Code", "")
        if code not in (
            "ConflictException",
            "ResourceAlreadyExistsException",
        ):
            raise wrap_aws_error(
                exc,
                f"Failed to create Timestream table {database_name}.{table_name}",
            ) from exc
        logger.debug("Timestream table %s.%s already exists", database_name, table_name)

    # --- Build and upsert the IoT topic rule ---
    rule_payload: dict[str, Any] = {
        "sql": f"SELECT * FROM '{topic_filter}'",
        "description": (
            f"Routes {topic_filter} telemetry to Timestream {database_name}.{table_name}"
        ),
        "actions": [
            {
                "timestream": {
                    "roleArn": role_arn,
                    "databaseName": database_name,
                    "tableName": table_name,
                    "dimensions": dimensions,
                }
            }
        ],
        "ruleDisabled": False,
        "awsIotSqlVersion": "2016-03-23",
    }

    try:
        iot.create_topic_rule(ruleName=rule_name, topicRulePayload=rule_payload)
        logger.info("Created IoT topic rule %s", rule_name)
    except ClientError as exc:
        code = exc.response["Error"].get("Code", "")
        if code in (
            "ResourceAlreadyExistsException",
            "ConflictException",
        ):
            try:
                iot.replace_topic_rule(ruleName=rule_name, topicRulePayload=rule_payload)
                logger.info("Replaced existing IoT topic rule %s", rule_name)
            except ClientError as inner_exc:
                raise wrap_aws_error(
                    inner_exc, f"Failed to replace topic rule {rule_name}"
                ) from inner_exc
        else:
            raise wrap_aws_error(exc, f"Failed to create topic rule {rule_name}") from exc

    # --- Retrieve rule ARN ---
    try:
        rule_resp = iot.get_topic_rule(ruleName=rule_name)
        rule_arn: str = rule_resp.get("ruleArn", "")
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to retrieve ARN for topic rule {rule_name}") from exc

    return IoTTimestreamRuleResult(
        rule_name=rule_name,
        rule_arn=rule_arn,
        database_name=database_name,
        table_name=table_name,
        created_database=created_database,
        created_table=created_table,
    )


# ---------------------------------------------------------------------------
# 2. IoT Device Shadow Sync
# ---------------------------------------------------------------------------


def iot_device_shadow_sync(
    thing_name: str,
    table_name: str,
    shadow_name: str | None = None,
    region_name: str | None = None,
) -> DeviceShadowSyncResult:
    """Read IoT Device Shadow, diff reported vs desired, write to DynamoDB.

    Retrieves the classic (unnamed) or named shadow for *thing_name*, computes
    a delta between the ``desired`` and ``reported`` states, then persists the
    full reconciled record (including the delta key list) to DynamoDB for use
    by fleet management dashboards.

    Args:
        thing_name: IoT thing name whose shadow to read.
        table_name: DynamoDB table name for storing the sync record.
        shadow_name: Named shadow identifier; ``None`` targets the classic
            (unnamed) shadow.
        region_name: AWS region override.

    Returns:
        A :class:`DeviceShadowSyncResult` with the reported and desired
        states, a list of keys where they diverge, and whether the record
        was successfully written to DynamoDB.

    Raises:
        RuntimeError: If shadow retrieval or DynamoDB write fails.
    """
    iot_data = get_client("iot-data", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # --- Read device shadow ---
    get_kwargs: dict[str, Any] = {"thingName": thing_name}
    if shadow_name:
        get_kwargs["shadowName"] = shadow_name

    try:
        shadow_resp = iot_data.get_thing_shadow(**get_kwargs)
        raw = shadow_resp["payload"]
        shadow_payload: dict[str, Any] = json.loads(raw.read() if hasattr(raw, "read") else raw)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to read shadow for thing {thing_name}") from exc

    state: dict[str, Any] = shadow_payload.get("state", {})
    reported_state: dict[str, Any] = state.get("reported", {})
    desired_state: dict[str, Any] = state.get("desired", {})

    # --- Compute delta: keys in desired that are absent or differ in reported ---
    delta_keys: list[str] = [
        key
        for key, desired_val in desired_state.items()
        if key not in reported_state or reported_state[key] != desired_val
    ]
    # Also capture keys in reported absent from desired (reverse delta)
    for key in reported_state:
        if key not in desired_state and key not in delta_keys:
            delta_keys.append(key)

    shadow_version: int = shadow_payload.get("version", 0)
    ts = int(time.time())
    shadow_key = shadow_name or "classic"

    logger.info(
        "Shadow sync for %s (%s): %d delta key(s): %s",
        thing_name,
        shadow_key,
        len(delta_keys),
        delta_keys,
    )

    # --- Persist reconciled state to DynamoDB ---
    synced_to_dynamodb = False
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"shadow#{thing_name}#{shadow_key}"},
                "sk": {"S": str(ts)},
                "thing_name": {"S": thing_name},
                "shadow_name": {"S": shadow_key},
                "shadow_version": {"N": str(shadow_version)},
                "reported_state": {"S": json.dumps(reported_state, default=str)},
                "desired_state": {"S": json.dumps(desired_state, default=str)},
                "delta_keys": {"S": json.dumps(delta_keys)},
                "timestamp": {"N": str(ts)},
            },
        )
        synced_to_dynamodb = True
        logger.info(
            "Wrote shadow sync record for %s (%s) to DynamoDB table %s",
            thing_name,
            shadow_key,
            table_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to store shadow sync record for {thing_name} in {table_name}",
        ) from exc

    return DeviceShadowSyncResult(
        thing_name=thing_name,
        reported_state=reported_state,
        desired_state=desired_state,
        delta_keys=delta_keys,
        synced_to_dynamodb=synced_to_dynamodb,
    )


# ---------------------------------------------------------------------------
# 3. IoT Fleet Command Broadcaster
# ---------------------------------------------------------------------------


def iot_fleet_command_broadcaster(
    job_id: str,
    thing_group_arn: str,
    command_document: dict[str, Any],
    bucket: str,
    table_name: str,
    target_selection: str = "SNAPSHOT",
    region_name: str | None = None,
) -> FleetCommandResult:
    """Create an IoT Job to broadcast a command to a thing group.

    Uploads the JSON *command_document* to S3 as the IoT Job document
    source, then creates an IoT Job targeting *thing_group_arn* that
    devices can fetch and execute.  Metadata about the job is stored in
    DynamoDB for dashboard visibility.

    Args:
        job_id: Globally unique IoT Job identifier (must be unique per
            account/region, e.g. ``"fw-update-2026-04-15"``).
        thing_group_arn: ARN of the thing group to target.
        command_document: Dict representing the job document payload
            (will be JSON-serialised and stored in S3).
        bucket: S3 bucket where the job document will be stored.
        table_name: DynamoDB table name for job tracking metadata.
        target_selection: ``"SNAPSHOT"`` (target current group members)
            or ``"CONTINUOUS"`` (include future members).
        region_name: AWS region override.

    Returns:
        A :class:`FleetCommandResult` with the job ARN, estimated target
        count, and S3 document key.

    Raises:
        RuntimeError: If any AWS service call fails.
        ValueError: If *target_selection* is not a valid value.
    """
    if target_selection not in ("SNAPSHOT", "CONTINUOUS"):
        raise ValueError(
            f"target_selection must be 'SNAPSHOT' or 'CONTINUOUS', got {target_selection!r}"
        )

    iot = get_client("iot", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # --- Upload job document to S3 ---
    document_key = f"iot-jobs/{job_id}/document.json"
    document_body = json.dumps(command_document, indent=2).encode("utf-8")
    try:
        s3.put_object(
            Bucket=bucket,
            Key=document_key,
            Body=document_body,
            ContentType="application/json",
        )
        logger.info("Uploaded job document to s3://%s/%s", bucket, document_key)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to upload job document to s3://{bucket}/{document_key}",
        ) from exc

    document_source = f"https://s3.amazonaws.com/{bucket}/{document_key}"

    # --- Determine targets count by describing the thing group ---
    targets_count = 0
    try:
        group_name = thing_group_arn.split(":")[-1].split("/")[-1]
        search_resp = iot.search_index(
            queryString=f"thingGroupNames:{group_name}",
        )
        targets_count = len(search_resp.get("things", []))
    except ClientError:
        # Index may not be enabled — fall back gracefully
        logger.debug("Could not determine targets count via Fleet Indexing; defaulting to 0")

    # --- Create the IoT Job ---
    try:
        job_resp = iot.create_job(
            jobId=job_id,
            targets=[thing_group_arn],
            documentSource=document_source,
            targetSelection=target_selection,
            description=f"Fleet command broadcast — {job_id}",
            jobExecutionsRolloutConfig={"maximumPerMinute": 50},
            abortConfig={
                "criteriaList": [
                    {
                        "failureType": "FAILED",
                        "action": "CANCEL",
                        "thresholdPercentage": 20.0,
                        "minNumberOfExecutedThings": 10,
                    }
                ]
            },
            timeoutConfig={"inProgressTimeoutInMinutes": 60},
        )
        job_arn: str = job_resp.get("jobArn", "")
        logger.info(
            "Created IoT job %s targeting %s (selection=%s)",
            job_id,
            thing_group_arn,
            target_selection,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create IoT job {job_id}") from exc

    ts = int(time.time())

    # --- Track job metadata in DynamoDB ---
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"job#{job_id}"},
                "sk": {"S": str(ts)},
                "job_id": {"S": job_id},
                "job_arn": {"S": job_arn},
                "thing_group_arn": {"S": thing_group_arn},
                "targets_count": {"N": str(targets_count)},
                "document_key": {"S": document_key},
                "target_selection": {"S": target_selection},
                "created_at": {"N": str(ts)},
            },
        )
        logger.info("Stored job metadata for %s in DynamoDB table %s", job_id, table_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to store job metadata for {job_id}") from exc

    return FleetCommandResult(
        job_id=job_id,
        job_arn=job_arn,
        targets_count=targets_count,
        document_key=document_key,
    )


# ---------------------------------------------------------------------------
# 4. IoT Alert to SNS
# ---------------------------------------------------------------------------


def iot_alert_to_sns(
    asset_id: str,
    property_id: str,
    threshold_value: float,
    comparison: str,
    sns_topic_arn: str,
    region_name: str | None = None,
) -> IoTAlertResult:
    """Read a SiteWise property value, evaluate threshold, publish SNS alert.

    Retrieves the latest value for *property_id* on *asset_id* from IoT
    SiteWise, compares it against *threshold_value* using *comparison*, and
    publishes a structured JSON alert to *sns_topic_arn* when the condition
    is met.

    Args:
        asset_id: IoT SiteWise asset identifier.
        property_id: Property identifier within the asset.
        threshold_value: Numeric threshold for breach detection.
        comparison: Comparison operator — one of ``"GT"``, ``"LT"``,
            ``"GTE"``, or ``"LTE"``.
        sns_topic_arn: SNS topic ARN to publish breach alerts to.
        region_name: AWS region override.

    Returns:
        An :class:`IoTAlertResult` with the current property value, breach
        flag, and SNS MessageId when published.

    Raises:
        RuntimeError: If SiteWise or SNS API calls fail.
        ValueError: If *comparison* is not one of the accepted operators.
    """
    comparison_upper = comparison.upper()
    if comparison_upper not in _COMPARISON_OPS:
        raise ValueError(f"comparison must be one of {sorted(_COMPARISON_OPS)}, got {comparison!r}")

    sitewise = get_client("iotsitewise", region_name=region_name)
    sns_client = get_client("sns", region_name=region_name)

    # --- Fetch latest property value from SiteWise ---
    try:
        prop_resp = sitewise.get_asset_property_value(
            assetId=asset_id,
            propertyId=property_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to get SiteWise property {property_id} on asset {asset_id}",
        ) from exc

    value_entry: dict[str, Any] = prop_resp.get("propertyValue", {}).get("value", {})
    # SiteWise returns a typed value union; extract the numeric variant
    raw_value: Any = (
        value_entry.get("doubleValue")
        or value_entry.get("integerValue")
        or value_entry.get("stringValue")
        or 0.0
    )
    try:
        current_value = float(raw_value)
    except (TypeError, ValueError):
        current_value = 0.0

    threshold_breached = _COMPARISON_OPS[comparison_upper](current_value, threshold_value)
    logger.info(
        "SiteWise %s/%s = %s %s %s → breached=%s",
        asset_id,
        property_id,
        current_value,
        comparison_upper,
        threshold_value,
        threshold_breached,
    )

    # --- Publish alert to SNS if threshold is breached ---
    message_id: str | None = None
    if threshold_breached:
        alert_payload = {
            "source": "aws-util/iot_pipelines",
            "asset_id": asset_id,
            "property_id": property_id,
            "current_value": current_value,
            "threshold_value": threshold_value,
            "comparison": comparison_upper,
            "threshold_breached": True,
            "evaluated_at": int(time.time()),
        }
        try:
            pub_resp = sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject=f"IoT SiteWise Threshold Alert — asset {asset_id}",
                Message=json.dumps(alert_payload, indent=2),
                MessageAttributes={
                    "asset_id": {"DataType": "String", "StringValue": asset_id},
                    "property_id": {"DataType": "String", "StringValue": property_id},
                    "comparison": {"DataType": "String", "StringValue": comparison_upper},
                },
            )
            message_id = pub_resp.get("MessageId")
            logger.info(
                "Published IoT alert to SNS topic %s; MessageId=%s",
                sns_topic_arn,
                message_id,
            )
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"Failed to publish alert to SNS topic {sns_topic_arn}"
            ) from exc

    return IoTAlertResult(
        asset_id=asset_id,
        property_id=property_id,
        current_value=current_value,
        threshold_breached=threshold_breached,
        message_id=message_id,
    )


# ---------------------------------------------------------------------------
# 5. Greengrass Component Deployer
# ---------------------------------------------------------------------------


def iot_greengrass_component_deployer(
    component_name: str,
    component_version: str,
    artifact_path: str,
    bucket: str,
    target_arn: str,
    region_name: str | None = None,
) -> GreengrassDeployResult:
    """Upload a Lambda ZIP to S3, register a Greengrass v2 component, deploy.

    Reads the ZIP file at *artifact_path*, uploads it to *bucket* under a
    deterministic key, creates a Greengrass v2 component version with a
    recipe pointing to that artifact, then triggers a deployment of the
    component to *target_arn*.

    Args:
        component_name: Fully qualified Greengrass v2 component name
            (e.g. ``"com.example.SensorProcessor"``).
        component_version: Semantic version string for the component version
            (e.g. ``"1.2.0"``).
        artifact_path: Local filesystem path to the Lambda function ZIP
            archive to upload.
        bucket: S3 bucket that Greengrass devices can download artifacts from.
        target_arn: ARN of the Greengrass core device or thing group to
            deploy the component to.
        region_name: AWS region override.

    Returns:
        A :class:`GreengrassDeployResult` with the component ARN,
        deployment identifier, and S3 artifact key.

    Raises:
        RuntimeError: If any S3 or Greengrass API call fails.
        FileNotFoundError: If *artifact_path* does not exist.
    """
    artifact_file = Path(artifact_path)
    if not artifact_file.exists():
        raise FileNotFoundError(f"Artifact not found at path: {artifact_path}")

    s3 = get_client("s3", region_name=region_name)
    gg = get_client("greengrassv2", region_name=region_name)

    # --- Upload artifact ZIP to S3 ---
    artifact_key = (
        f"greengrass/components/{component_name}/{component_version}/{artifact_file.name}"
    )
    try:
        artifact_bytes = artifact_file.read_bytes()
        s3.put_object(
            Bucket=bucket,
            Key=artifact_key,
            Body=artifact_bytes,
            ContentType="application/zip",
        )
        logger.info(
            "Uploaded Greengrass artifact (%d bytes) to s3://%s/%s",
            len(artifact_bytes),
            bucket,
            artifact_key,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to upload artifact to s3://{bucket}/{artifact_key}",
        ) from exc

    artifact_uri = f"s3://{bucket}/{artifact_key}"

    # --- Build Greengrass v2 inline component recipe ---
    recipe: dict[str, Any] = {
        "RecipeFormatVersion": "2020-01-25",
        "ComponentName": component_name,
        "ComponentVersion": component_version,
        "ComponentDescription": (
            f"Greengrass v2 component {component_name} v{component_version} "
            f"— artifact uploaded by aws-util"
        ),
        "ComponentPublisher": "aws-util",
        "Manifests": [
            {
                "Platform": {"os": "linux"},
                "Artifacts": [
                    {
                        "URI": artifact_uri,
                        "Unarchive": "ZIP",
                        "Permission": {"Read": "OWNER"},
                    }
                ],
                "Lifecycle": {
                    "Install": {
                        "Script": (
                            "pip3 install --quiet -r "
                            "{artifacts:decompressedPath}/"
                            f"{artifact_file.stem}/requirements.txt "
                            "2>/dev/null || true"
                        )
                    },
                    "Run": {
                        "Script": (
                            "python3 {artifacts:decompressedPath}/"
                            f"{artifact_file.stem}/lambda_function.py"
                        )
                    },
                },
            }
        ],
    }

    # --- Register Greengrass v2 component version ---
    try:
        comp_resp = gg.create_component_version(
            inlineRecipe=json.dumps(recipe).encode("utf-8"),
        )
        component_arn: str = comp_resp.get("arn", "")
        logger.info(
            "Created Greengrass component version %s@%s → %s",
            component_name,
            component_version,
            component_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create Greengrass component {component_name}@{component_version}",
        ) from exc

    # --- Trigger deployment to target ---
    deployment_name = f"{component_name}-v{component_version}-{int(time.time())}"
    try:
        deploy_resp = gg.create_deployment(
            targetArn=target_arn,
            deploymentName=deployment_name,
            components={
                component_name: {
                    "componentVersion": component_version,
                    "configurationUpdate": {"merge": "{}"},
                }
            },
            deploymentPolicies={
                "failureHandlingPolicy": "ROLLBACK",
                "componentUpdatePolicy": {
                    "timeoutInSeconds": 60,
                    "action": "NOTIFY_COMPONENTS",
                },
            },
        )
        deployment_id: str = deploy_resp.get("deploymentId", "")
        logger.info(
            "Triggered Greengrass deployment %s (%s) to target %s",
            deployment_id,
            deployment_name,
            target_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to deploy Greengrass component {component_name} to {target_arn}",
        ) from exc

    return GreengrassDeployResult(
        component_arn=component_arn,
        deployment_id=deployment_id,
        artifact_key=artifact_key,
    )
