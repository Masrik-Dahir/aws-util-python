"""finding_ops — Security finding operations and routing utilities.

Provides multi-service finding management helpers for AWS environments:

- **inspector_finding_to_jira** — Get Inspector findings, deduplicate by CVE
  in DynamoDB, send notification emails via SES for new findings.
- **macie_finding_remediation** — Get Macie findings, block public access on
  affected S3 buckets, log remediation in DynamoDB.
- **detective_graph_exporter** — List Detective graph members, export to S3
  as JSON, register in Glue Data Catalog.
- **security_hub_finding_router** — Get Security Hub findings, classify by
  severity, route to different SQS queues.
- **cloudtrail_anomaly_detector** — Query CloudTrail events, detect anomalous
  patterns, publish alerts via SNS.
- **access_analyzer_finding_suppressor** — Get Access Analyzer findings, check
  against approved patterns in DynamoDB, archive matches, log to CloudWatch.
"""

from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "AnomalyDetectionResult",
    "DetectiveExportResult",
    "FindingRouterResult",
    "FindingSuppressorResult",
    "InspectorFindingResult",
    "MacieRemediationResult",
    "access_analyzer_finding_suppressor",
    "cloudtrail_anomaly_detector",
    "detective_graph_exporter",
    "inspector_finding_to_jira",
    "macie_finding_remediation",
    "security_hub_finding_router",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class InspectorFindingResult(BaseModel):
    """Result of the Inspector finding deduplication and notification."""

    model_config = ConfigDict(frozen=True)

    findings_count: int
    new_findings: int
    emails_sent: int


class MacieRemediationResult(BaseModel):
    """Result of the Macie finding remediation."""

    model_config = ConfigDict(frozen=True)

    findings_count: int
    remediated_count: int
    buckets_affected: list[str]


class DetectiveExportResult(BaseModel):
    """Result of the Detective graph export."""

    model_config = ConfigDict(frozen=True)

    members_count: int
    s3_key: str
    glue_table_name: str


class FindingRouterResult(BaseModel):
    """Result of the Security Hub finding router."""

    model_config = ConfigDict(frozen=True)

    total_findings: int
    critical_count: int
    high_count: int
    default_count: int


class AnomalyDetectionResult(BaseModel):
    """Result of the CloudTrail anomaly detector."""

    model_config = ConfigDict(frozen=True)

    events_analyzed: int
    anomalies_found: int
    anomaly_details: list[dict[str, Any]] = []
    alert_sent: bool


class FindingSuppressorResult(BaseModel):
    """Result of the Access Analyzer finding suppressor."""

    model_config = ConfigDict(frozen=True)

    findings_count: int
    suppressed_count: int
    unresolved_count: int


# ---------------------------------------------------------------------------
# 1. Inspector Finding to Jira (DynamoDB dedup + SES v2 notification)
# ---------------------------------------------------------------------------


def inspector_finding_to_jira(
    table_name: str,
    from_email: str,
    to_emails: list[str],
    max_findings: int = 50,
    region_name: str | None = None,
) -> InspectorFindingResult:
    """Get Inspector findings, deduplicate by CVE in DynamoDB, notify via SES.

    Lists active Inspector v2 findings (up to *max_findings*), checks each
    CVE/finding ID against DynamoDB for deduplication, stores new findings,
    and sends a notification email via SES v2 for every new unique finding.

    Args:
        table_name: DynamoDB table name for CVE deduplication records.
        from_email: Verified SES sender email address.
        to_emails: List of recipient email addresses for finding
            notifications.
        max_findings: Maximum number of findings to process (default 50).
        region_name: AWS region override.

    Returns:
        An :class:`InspectorFindingResult` with findings_count, new_findings,
        and emails_sent.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    inspector = get_client("inspector2", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)
    ses = get_client("sesv2", region_name=region_name)

    # ------------------------------------------------------------------
    # List Inspector findings (paginated up to max_findings)
    # ------------------------------------------------------------------
    filter_criteria: dict[str, Any] = {
        "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
    }
    findings: list[dict[str, Any]] = []
    next_token: str | None = None

    while len(findings) < max_findings:
        params: dict[str, Any] = {
            "filterCriteria": filter_criteria,
            "maxResults": min(100, max_findings - len(findings)),
        }
        if next_token:
            params["nextToken"] = next_token
        try:
            page = inspector.list_findings(**params)
        except ClientError as exc:
            raise wrap_aws_error(exc, "inspector_finding_to_jira: list_findings failed") from exc

        findings.extend(page.get("findings", []))
        next_token = page.get("nextToken")
        if not next_token:
            break

    findings_count = len(findings)
    new_findings = 0
    emails_sent = 0

    # ------------------------------------------------------------------
    # Deduplicate by CVE ID; send SES email for each new finding
    # ------------------------------------------------------------------
    for finding in findings:
        vuln = finding.get("packageVulnerabilityDetails", {})
        cve_id = vuln.get("vulnerabilityId", "") or finding.get("findingArn", "")
        if not cve_id:
            continue

        # Check DynamoDB for existing record
        try:
            existing = ddb.get_item(
                TableName=table_name,
                Key={"cve_id": {"S": cve_id}},
            )
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"inspector_finding_to_jira: DynamoDB get_item failed for {cve_id!r}",
            ) from exc

        if existing.get("Item"):
            continue  # Duplicate — skip

        severity = finding.get("severity", "UNKNOWN")
        title = finding.get("title", "")
        description = finding.get("description", "")
        resources = finding.get("resources", [])
        resource_arns = [r.get("id", "") for r in resources]

        # Store new finding in DynamoDB
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "cve_id": {"S": cve_id},
                    "severity": {"S": severity},
                    "title": {"S": title},
                    "description": {"S": description[:1000]},
                    "resource_arns": {"SS": resource_arns or ["N/A"]},
                    "finding_arn": {"S": finding.get("findingArn", "")},
                    "detected_at": {"S": datetime.now(tz=UTC).isoformat()},
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"inspector_finding_to_jira: DynamoDB put_item failed for {cve_id!r}",
            ) from exc

        new_findings += 1

        # Send email via SES v2
        email_body = (
            f"New Inspector Finding Detected\n\n"
            f"CVE/ID: {cve_id}\n"
            f"Severity: {severity}\n"
            f"Title: {title}\n"
            f"Description: {description[:500]}\n\n"
            f"Affected resources:\n" + "\n".join(f"  - {arn}" for arn in resource_arns[:10])
        )
        try:
            ses.send_email(
                FromEmailAddress=from_email,
                Destination={"ToAddresses": to_emails},
                Content={
                    "Simple": {
                        "Subject": {"Data": f"[Inspector] {severity} — {cve_id}: {title[:60]}"},
                        "Body": {"Text": {"Data": email_body}},
                    }
                },
            )
            emails_sent += 1
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"inspector_finding_to_jira: SES send_email failed for {cve_id!r}",
            ) from exc

    logger.info(
        "inspector_finding_to_jira: count=%d new=%d emails=%d",
        findings_count,
        new_findings,
        emails_sent,
    )
    return InspectorFindingResult(
        findings_count=findings_count,
        new_findings=new_findings,
        emails_sent=emails_sent,
    )


# ---------------------------------------------------------------------------
# 2. Macie Finding Remediation
# ---------------------------------------------------------------------------


def macie_finding_remediation(
    table_name: str,
    max_findings: int = 25,
    region_name: str | None = None,
) -> MacieRemediationResult:
    """Get Macie sensitive data findings and apply S3 block-public-access.

    Lists active Macie sensitive-data findings (up to *max_findings*),
    applies ``put_public_access_block`` on each affected S3 bucket if not
    already blocked, and records the remediation outcome in DynamoDB.

    Args:
        table_name: DynamoDB table name for remediation log records.
        max_findings: Maximum number of findings to process (default 25).
        region_name: AWS region override.

    Returns:
        A :class:`MacieRemediationResult` with findings_count,
        remediated_count, and buckets_affected.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    macie = get_client("macie2", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # ------------------------------------------------------------------
    # List Macie sensitive-data findings (paginated)
    # ------------------------------------------------------------------
    findings: list[dict[str, Any]] = []
    next_token: str | None = None

    while len(findings) < max_findings:
        params: dict[str, Any] = {
            "findingCriteria": {"criterion": {"category": {"eq": ["SENSITIVE_DATA"]}}},
            "maxResults": min(50, max_findings - len(findings)),
        }
        if next_token:
            params["nextToken"] = next_token
        try:
            page = macie.list_findings(**params)
        except ClientError as exc:
            raise wrap_aws_error(exc, "macie_finding_remediation: list_findings failed") from exc

        finding_ids = page.get("findingIds", [])
        if not finding_ids:
            break

        # Fetch full finding details
        try:
            details_resp = macie.get_findings(findingIds=finding_ids)
            findings.extend(details_resp.get("findings", []))
        except ClientError as exc:
            raise wrap_aws_error(exc, "macie_finding_remediation: get_findings failed") from exc

        next_token = page.get("nextToken")
        if not next_token:
            break

    findings_count = len(findings)
    remediated_buckets: set[str] = set()

    # ------------------------------------------------------------------
    # Remediate each finding: block public access, log in DynamoDB
    # ------------------------------------------------------------------
    for finding in findings:
        resources_affected = finding.get("resourcesAffected", {})
        s3_bucket = resources_affected.get("s3Bucket", {})
        s3_object = resources_affected.get("s3Object", {})

        bucket_name = s3_bucket.get("name", "")
        object_key = s3_object.get("key", "")
        finding_id = finding.get("id", "")
        severity = finding.get("severity", {}).get("description", "UNKNOWN")

        if not bucket_name:
            continue

        bucket_remediated = False

        # Apply block-public-access on bucket if not already done
        if bucket_name not in remediated_buckets:
            try:
                s3.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        "BlockPublicAcls": True,
                        "IgnorePublicAcls": True,
                        "BlockPublicPolicy": True,
                        "RestrictPublicBuckets": True,
                    },
                )
                remediated_buckets.add(bucket_name)
                bucket_remediated = True
            except ClientError as exc:
                error_code = exc.response.get("Error", {}).get("Code", "")
                if error_code == "AccessDenied":
                    logger.warning(
                        "macie_finding_remediation: access denied for bucket %r",
                        bucket_name,
                    )
                else:
                    raise wrap_aws_error(
                        exc,
                        f"macie_finding_remediation: put_public_access_block failed for "
                        f"{bucket_name!r}",
                    ) from exc
        else:
            bucket_remediated = True  # Already remediated this session

        # Record in DynamoDB
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "finding_id": {"S": finding_id},
                    "bucket_name": {"S": bucket_name},
                    "object_key": {"S": object_key or ""},
                    "severity": {"S": severity},
                    "bucket_remediated": {"BOOL": bucket_remediated},
                    "remediated_at": {"S": datetime.now(tz=UTC).isoformat()},
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"macie_finding_remediation: DynamoDB put_item failed for finding {finding_id!r}",
            ) from exc

    logger.info(
        "macie_finding_remediation: findings=%d remediated=%d buckets=%s",
        findings_count,
        len(remediated_buckets),
        list(remediated_buckets),
    )
    return MacieRemediationResult(
        findings_count=findings_count,
        remediated_count=len(remediated_buckets),
        buckets_affected=sorted(remediated_buckets),
    )


# ---------------------------------------------------------------------------
# 3. Detective Graph Exporter
# ---------------------------------------------------------------------------


def detective_graph_exporter(
    graph_arn: str,
    bucket: str,
    key_prefix: str,
    database_name: str,
    table_name_prefix: str,
    region_name: str | None = None,
) -> DetectiveExportResult:
    """List Detective graph members, export to S3, register in Glue Data Catalog.

    Lists all members of the Detective behavior graph, compiles membership
    and graph metadata to JSON, uploads it to S3 under *key_prefix*, then
    creates a Glue Data Catalog table pointing at that S3 location so the
    data is queryable via Athena.

    Args:
        graph_arn: Amazon Detective behavior graph ARN.
        bucket: S3 bucket for the export.
        key_prefix: S3 key prefix (directory) under which the JSON export
            is stored.  The final key is ``{key_prefix}/graph_members.json``.
        database_name: Glue Data Catalog database name for the new table.
        table_name_prefix: Prefix for the Glue table name; the full name
            is ``{table_name_prefix}_graph_members``.
        region_name: AWS region override.

    Returns:
        A :class:`DetectiveExportResult` with members_count, s3_key, and
        glue_table_name.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    detective = get_client("detective", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)
    glue = get_client("glue", region_name=region_name)

    # ------------------------------------------------------------------
    # List graph members (paginated)
    # ------------------------------------------------------------------
    members: list[dict[str, Any]] = []
    next_token: str | None = None

    while True:
        params: dict[str, Any] = {"GraphArn": graph_arn}
        if next_token:
            params["NextToken"] = next_token
        try:
            page = detective.list_members(**params)
        except ClientError as exc:
            raise wrap_aws_error(exc, "detective_graph_exporter: list_members failed") from exc

        for member in page.get("MemberDetails", []):
            invited_time = member.get("InvitedTime", datetime.now(tz=UTC))
            updated_time = member.get("UpdatedTime", datetime.now(tz=UTC))
            members.append(
                {
                    "account_id": member.get("AccountId", ""),
                    "email_address": member.get("EmailAddress", ""),
                    "graph_arn": member.get("GraphArn", ""),
                    "status": member.get("Status", ""),
                    "disabled_reason": member.get("DisabledReason", ""),
                    "invited_time": invited_time.isoformat()
                    if hasattr(invited_time, "isoformat")
                    else str(invited_time),
                    "updated_time": updated_time.isoformat()
                    if hasattr(updated_time, "isoformat")
                    else str(updated_time),
                }
            )

        next_token = page.get("NextToken")
        if not next_token:
            break

    # ------------------------------------------------------------------
    # Compile export document and upload to S3
    # ------------------------------------------------------------------
    export_key = f"{key_prefix.rstrip('/')}/graph_members.json"
    export_doc = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "graph_arn": graph_arn,
        "members_count": len(members),
        "members": members,
    }

    try:
        s3.put_object(
            Bucket=bucket,
            Key=export_key,
            Body=json.dumps(export_doc, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "detective_graph_exporter: S3 put_object failed") from exc

    s3_location = f"s3://{bucket}/{key_prefix.rstrip('/')}/"

    # ------------------------------------------------------------------
    # Register table in Glue Data Catalog
    # ------------------------------------------------------------------
    glue_table_name = f"{table_name_prefix}_graph_members"

    # Ensure the Glue database exists (create if absent)
    try:
        glue.create_database(
            DatabaseInput={
                "Name": database_name,
                "Description": "Detective graph export database",
            }
        )
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "AlreadyExistsException":
            raise wrap_aws_error(
                exc, "detective_graph_exporter: Glue create_database failed"
            ) from exc

    try:
        glue.create_table(
            DatabaseName=database_name,
            TableInput={
                "Name": glue_table_name,
                "Description": "Amazon Detective graph members export",
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "account_id", "Type": "string"},
                        {"Name": "email_address", "Type": "string"},
                        {"Name": "graph_arn", "Type": "string"},
                        {"Name": "status", "Type": "string"},
                        {"Name": "invited_time", "Type": "string"},
                        {"Name": "updated_time", "Type": "string"},
                    ],
                    "Location": s3_location,
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {"SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"},
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "AlreadyExistsException":
            # Table already exists — update it
            try:
                glue.update_table(
                    DatabaseName=database_name,
                    TableInput={
                        "Name": glue_table_name,
                        "StorageDescriptor": {
                            "Columns": [
                                {"Name": "account_id", "Type": "string"},
                                {"Name": "email_address", "Type": "string"},
                                {"Name": "graph_arn", "Type": "string"},
                                {"Name": "status", "Type": "string"},
                                {"Name": "invited_time", "Type": "string"},
                                {"Name": "updated_time", "Type": "string"},
                            ],
                            "Location": s3_location,
                            "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                            "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                            "SerdeInfo": {
                                "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                            },
                        },
                        "TableType": "EXTERNAL_TABLE",
                    },
                )
            except ClientError as update_exc:
                raise wrap_aws_error(
                    update_exc,
                    "detective_graph_exporter: Glue update_table failed",
                ) from update_exc
        else:
            raise wrap_aws_error(exc, "detective_graph_exporter: Glue create_table failed") from exc

    logger.info(
        "detective_graph_exporter: members=%d s3_key=%s glue_table=%s",
        len(members),
        export_key,
        glue_table_name,
    )
    return DetectiveExportResult(
        members_count=len(members),
        s3_key=export_key,
        glue_table_name=glue_table_name,
    )


# ---------------------------------------------------------------------------
# 4. Security Hub Finding Router
# ---------------------------------------------------------------------------


def security_hub_finding_router(
    critical_queue_url: str,
    high_queue_url: str,
    default_queue_url: str,
    max_findings: int = 100,
    filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> FindingRouterResult:
    """Get Security Hub findings, classify by severity, route to SQS queues.

    Lists active Security Hub findings (with optional *filters*), classifies
    each by SeverityLabel (CRITICAL, HIGH, or default), and sends messages
    to the corresponding SQS queue in batches of 10.

    Args:
        critical_queue_url: SQS queue URL for CRITICAL severity findings.
        high_queue_url: SQS queue URL for HIGH severity findings.
        default_queue_url: SQS queue URL for all other severities (MEDIUM,
            LOW, INFORMATIONAL, UNKNOWN).
        max_findings: Maximum number of findings to process (default 100).
        filters: Optional Security Hub filter criteria dict to pass directly
            to ``get_findings(Filters=...)``.
        region_name: AWS region override.

    Returns:
        A :class:`FindingRouterResult` with total_findings, critical_count,
        high_count, and default_count.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    hub = get_client("securityhub", region_name=region_name)
    sqs = get_client("sqs", region_name=region_name)

    # ------------------------------------------------------------------
    # Retrieve Security Hub findings (paginated)
    # ------------------------------------------------------------------
    base_filters: dict[str, Any] = filters or {
        "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}],
        "WorkflowStatus": [{"Value": "NEW", "Comparison": "EQUALS"}],
    }

    findings: list[dict[str, Any]] = []
    next_token: str | None = None

    while len(findings) < max_findings:
        params: dict[str, Any] = {
            "Filters": base_filters,
            "MaxResults": min(100, max_findings - len(findings)),
        }
        if next_token:
            params["NextToken"] = next_token
        try:
            page = hub.get_findings(**params)
        except ClientError as exc:
            raise wrap_aws_error(exc, "security_hub_finding_router: get_findings failed") from exc

        page_findings = page.get("Findings", [])
        findings.extend(page_findings)
        next_token = page.get("NextToken")
        if not next_token or not page_findings:
            break

    # ------------------------------------------------------------------
    # Classify by severity and route to SQS
    # ------------------------------------------------------------------
    critical_count = 0
    high_count = 0
    default_count = 0

    batch_by_queue: dict[str, list[dict[str, Any]]] = {
        critical_queue_url: [],
        high_queue_url: [],
        default_queue_url: [],
    }

    for finding in findings:
        sev_label = finding.get("Severity", {}).get("Label", "").upper()
        if sev_label == "CRITICAL":
            critical_count += 1
            batch_by_queue[critical_queue_url].append(finding)
        elif sev_label == "HIGH":
            high_count += 1
            batch_by_queue[high_queue_url].append(finding)
        else:
            default_count += 1
            batch_by_queue[default_queue_url].append(finding)

    for queue_url, queue_findings in batch_by_queue.items():
        if not queue_findings:
            continue
        for i in range(0, len(queue_findings), 10):
            batch = queue_findings[i : i + 10]
            entries = [
                {
                    "Id": str(i + j),
                    "MessageBody": json.dumps(
                        {
                            "finding_id": f.get("Id", ""),
                            "severity": f.get("Severity", {}).get("Label", ""),
                            "title": f.get("Title", ""),
                            "description": f.get("Description", "")[:500],
                            "aws_account_id": f.get("AwsAccountId", ""),
                            "region": f.get("Region", ""),
                            "resources": [r.get("Id", "") for r in f.get("Resources", [])[:5]],
                        }
                    ),
                }
                for j, f in enumerate(batch)
            ]
            try:
                sqs.send_message_batch(QueueUrl=queue_url, Entries=entries)
            except ClientError as exc:
                raise wrap_aws_error(
                    exc,
                    f"security_hub_finding_router: SQS send_message_batch failed for {queue_url!r}",
                ) from exc

    logger.info(
        "security_hub_finding_router: total=%d critical=%d high=%d default=%d",
        len(findings),
        critical_count,
        high_count,
        default_count,
    )
    return FindingRouterResult(
        total_findings=len(findings),
        critical_count=critical_count,
        high_count=high_count,
        default_count=default_count,
    )


# ---------------------------------------------------------------------------
# 5. CloudTrail Anomaly Detector
# ---------------------------------------------------------------------------


def cloudtrail_anomaly_detector(
    trail_name: str | None = None,
    lookback_minutes: int = 60,
    error_rate_threshold: float = 0.3,
    sns_topic_arn: str = "",
    region_name: str | None = None,
) -> AnomalyDetectionResult:
    """Query CloudTrail events, detect anomalous patterns, alert via SNS.

    Looks up CloudTrail events over *lookback_minutes*, analyzes for:
    - High error rates exceeding *error_rate_threshold*
    - Unusual / high-privilege API calls (DeleteTrail, CreateUser, etc.)
    - Unusual regions (events outside the primary region of the trail)

    Publishes a consolidated alert to *sns_topic_arn* if anomalies are found.

    Args:
        trail_name: Optional CloudTrail trail name to scope the lookup.
            If ``None``, all trails in the region are considered.
        lookback_minutes: Minutes of CloudTrail history to analyze
            (default 60).
        error_rate_threshold: Fraction of events that must be errors before
            flagging a HIGH_ERROR_RATE anomaly (default 0.3).
        sns_topic_arn: SNS topic ARN to publish alerts to.
        region_name: AWS region override.

    Returns:
        An :class:`AnomalyDetectionResult` with events_analyzed,
        anomalies_found, anomaly_details, and alert_sent.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    ct = get_client("cloudtrail", region_name=region_name)

    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(minutes=lookback_minutes)

    # ------------------------------------------------------------------
    # Collect CloudTrail events (paginated)
    # ------------------------------------------------------------------
    lookup_params: dict[str, Any] = {
        "StartTime": start_time,
        "EndTime": end_time,
        "MaxResults": 50,
    }

    _high_privilege_apis = {
        "DeleteTrail",
        "StopLogging",
        "DeleteBucket",
        "PutBucketPolicy",
        "CreateUser",
        "AttachUserPolicy",
        "AttachRolePolicy",
        "PutUserPolicy",
        "CreateAccessKey",
        "ConsoleLogin",
        "AssumeRoleWithSAML",
        "AssumeRoleWithWebIdentity",
        "PutRolePolicy",
        "CreateRole",
        "UpdateAssumeRolePolicy",
    }

    events: list[dict[str, Any]] = []
    next_token: str | None = None

    while True:
        params: dict[str, Any] = dict(lookup_params)
        if next_token:
            params["NextToken"] = next_token
        try:
            page = ct.lookup_events(**params)
        except ClientError as exc:
            raise wrap_aws_error(exc, "cloudtrail_anomaly_detector: lookup_events failed") from exc

        events.extend(page.get("Events", []))
        next_token = page.get("NextToken")
        if not next_token:
            break

    events_analyzed = len(events)
    anomaly_details: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Analysis: error rate
    # ------------------------------------------------------------------
    error_events = [
        e for e in events if json.loads(e.get("CloudTrailEvent", "{}")).get("errorCode")
    ]
    error_rate = len(error_events) / events_analyzed if events_analyzed else 0.0
    if error_rate > error_rate_threshold:
        anomaly_details.append(
            {
                "anomaly_type": "HIGH_ERROR_RATE",
                "description": (
                    f"Error rate {error_rate:.1%} exceeds {error_rate_threshold:.0%} threshold"
                ),
                "error_count": len(error_events),
                "total_events": events_analyzed,
            }
        )

    # ------------------------------------------------------------------
    # Analysis: unusual/high-privilege API calls
    # ------------------------------------------------------------------
    seen_unusual: dict[str, int] = {}
    for event in events:
        event_name = event.get("EventName", "")
        if event_name in _high_privilege_apis:
            seen_unusual[event_name] = seen_unusual.get(event_name, 0) + 1

    if seen_unusual:
        anomaly_details.append(
            {
                "anomaly_type": "UNUSUAL_API_CALLS",
                "description": f"Detected {len(seen_unusual)} unusual/high-privilege API call type(s)",
                "api_calls": seen_unusual,
            }
        )

    # ------------------------------------------------------------------
    # Analysis: unusual regions (events from outside expected region)
    # ------------------------------------------------------------------
    region_counter: Counter[str] = Counter()
    for event in events:
        raw = json.loads(event.get("CloudTrailEvent", "{}"))
        aws_region = raw.get("awsRegion", "")
        if aws_region:
            region_counter[aws_region] += 1

    if len(region_counter) > 1:
        dominant_region, _dominant_count = region_counter.most_common(1)[0]
        unusual_regions = {r: c for r, c in region_counter.items() if r != dominant_region}
        if unusual_regions:
            anomaly_details.append(
                {
                    "anomaly_type": "UNUSUAL_REGIONS",
                    "description": (
                        f"Events detected from {len(unusual_regions)} region(s) "
                        f"other than the primary region {dominant_region!r}"
                    ),
                    "dominant_region": dominant_region,
                    "unusual_regions": unusual_regions,
                }
            )

    # ------------------------------------------------------------------
    # Alert via SNS if anomalies found
    # ------------------------------------------------------------------
    alert_sent = False
    if anomaly_details and sns_topic_arn:
        sns = get_client("sns", region_name=region_name)
        lines = [
            f"CloudTrail Anomaly Alert — {len(anomaly_details)} anomaly type(s) detected",
            f"Time window: last {lookback_minutes} minutes",
            f"Events analyzed: {events_analyzed}",
            "",
        ]
        for a in anomaly_details:
            lines.append(f"[{a['anomaly_type']}] {a['description']}")
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="CloudTrail Anomaly Alert",
                Message="\n".join(lines),
            )
            alert_sent = True
        except ClientError as exc:
            raise wrap_aws_error(exc, "cloudtrail_anomaly_detector: SNS publish failed") from exc

    logger.info(
        "cloudtrail_anomaly_detector: events=%d anomalies=%d alert_sent=%s",
        events_analyzed,
        len(anomaly_details),
        alert_sent,
    )
    return AnomalyDetectionResult(
        events_analyzed=events_analyzed,
        anomalies_found=len(anomaly_details),
        anomaly_details=anomaly_details,
        alert_sent=alert_sent,
    )


# ---------------------------------------------------------------------------
# 6. Access Analyzer Finding Suppressor
# ---------------------------------------------------------------------------


def access_analyzer_finding_suppressor(
    analyzer_arn: str,
    table_name: str,
    log_group_name: str,
    region_name: str | None = None,
) -> FindingSuppressorResult:
    """Archive Access Analyzer findings that match approved patterns in DynamoDB.

    Lists all ACTIVE Access Analyzer findings for *analyzer_arn*, checks each
    against approved suppression patterns stored in *table_name* (DynamoDB),
    archives findings whose resource ARN or principal matches an approved
    pattern via ``update_findings``, and logs each suppression to
    CloudWatch Logs under *log_group_name*.

    Args:
        analyzer_arn: Access Analyzer analyzer ARN.
        table_name: DynamoDB table holding approved suppression patterns.
            Each item must have a ``pattern`` (S) attribute whose value is
            a substring matched against the resource ARN and principal JSON.
        log_group_name: CloudWatch Logs log group name for audit logging.
        region_name: AWS region override.

    Returns:
        A :class:`FindingSuppressorResult` with findings_count,
        suppressed_count, and unresolved_count.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    aa = get_client("accessanalyzer", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)
    logs = get_client("logs", region_name=region_name)

    # ------------------------------------------------------------------
    # Ensure CloudWatch log group and stream exist
    # ------------------------------------------------------------------
    log_stream_name = f"access-analyzer-suppressor/{datetime.now(tz=UTC).strftime('%Y/%m/%d')}"
    try:
        logs.create_log_group(logGroupName=log_group_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
            raise wrap_aws_error(
                exc,
                "access_analyzer_finding_suppressor: create_log_group failed",
            ) from exc

    try:
        logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
            raise wrap_aws_error(
                exc,
                "access_analyzer_finding_suppressor: create_log_stream failed",
            ) from exc

    # ------------------------------------------------------------------
    # Load approved patterns from DynamoDB (full table scan)
    # ------------------------------------------------------------------
    approved_patterns: list[str] = []
    try:
        paginator = ddb.get_paginator("scan")
        for page in paginator.paginate(TableName=table_name):
            for item in page.get("Items", []):
                pattern = item.get("pattern", {}).get("S", "")
                if pattern:
                    approved_patterns.append(pattern)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "access_analyzer_finding_suppressor: DynamoDB scan failed",
        ) from exc

    # ------------------------------------------------------------------
    # List active Access Analyzer findings (paginated)
    # ------------------------------------------------------------------
    findings: list[dict[str, Any]] = []
    next_token: str | None = None

    while True:
        params: dict[str, Any] = {
            "analyzerArn": analyzer_arn,
            "filter": {"status": {"eq": ["ACTIVE"]}},
        }
        if next_token:
            params["nextToken"] = next_token
        try:
            page = aa.list_findings(**params)
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                "access_analyzer_finding_suppressor: list_findings failed",
            ) from exc
        findings.extend(page.get("findings", []))
        next_token = page.get("nextToken")
        if not next_token:
            break

    findings_count = len(findings)
    suppressed_count = 0
    log_events: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Check each finding against approved patterns; archive on match
    # ------------------------------------------------------------------
    for finding in findings:
        finding_id = finding.get("id", "")
        resource_arn = finding.get("resource", "")
        principal = json.dumps(finding.get("principal", {}))

        matched_pattern = None
        for pattern in approved_patterns:
            if pattern in resource_arn or pattern in principal:
                matched_pattern = pattern
                break

        if not matched_pattern:
            continue

        # Archive the finding
        try:
            aa.update_findings(
                analyzerArn=analyzer_arn,
                ids=[finding_id],
                status="ARCHIVED",
            )
            suppressed_count += 1
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"access_analyzer_finding_suppressor: update_findings failed for {finding_id!r}",
            ) from exc

        log_events.append(
            {
                "timestamp": int(datetime.now(tz=UTC).timestamp() * 1000),
                "message": json.dumps(
                    {
                        "action": "SUPPRESSED",
                        "finding_id": finding_id,
                        "resource": resource_arn,
                        "matched_pattern": matched_pattern,
                        "suppressed_at": datetime.now(tz=UTC).isoformat(),
                    }
                ),
            }
        )

    # ------------------------------------------------------------------
    # Write audit log events to CloudWatch Logs
    # ------------------------------------------------------------------
    if log_events:
        try:
            logs.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events,
            )
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                "access_analyzer_finding_suppressor: put_log_events failed",
            ) from exc

    unresolved_count = findings_count - suppressed_count
    logger.info(
        "access_analyzer_finding_suppressor: total=%d suppressed=%d unresolved=%d",
        findings_count,
        suppressed_count,
        unresolved_count,
    )
    return FindingSuppressorResult(
        findings_count=findings_count,
        suppressed_count=suppressed_count,
        unresolved_count=unresolved_count,
    )
