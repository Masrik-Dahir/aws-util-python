"""Native async governance — cloud governance and compliance utilities.

Native async implementation using :mod:`aws_util.aio._engine` for true
non-blocking I/O.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.governance import (
    KMSRotationAuditResult,
    RemediationResult,
    SCPDriftResult,
    SSOAuditResult,
)

logger = logging.getLogger(__name__)

__all__ = [
    "KMSRotationAuditResult",
    "RemediationResult",
    "SCPDriftResult",
    "SSOAuditResult",
    "config_rule_remediation_executor",
    "kms_key_rotation_auditor",
    "organizations_scp_drift_detector",
    "sso_permission_set_auditor",
]


# ---------------------------------------------------------------------------
# 1. Config Rule Remediation Executor
# ---------------------------------------------------------------------------


async def config_rule_remediation_executor(
    config_rule_name: str,
    remediation_lambda_arn: str,
    table_name: str,
    max_items: int = 25,
    region_name: str | None = None,
) -> RemediationResult:
    """Get non-compliant AWS Config rule evaluations and invoke a remediation Lambda.

    Queries AWS Config for resources that are non-compliant with
    *config_rule_name*, invokes *remediation_lambda_arn* once per resource
    with the resource info as the payload, and records each remediation
    outcome (success/failure) in DynamoDB table *table_name*.

    Args:
        config_rule_name: Name of the AWS Config rule to check for
            non-compliant resources.
        remediation_lambda_arn: ARN of the Lambda function to invoke for
            each non-compliant resource.
        table_name: DynamoDB table name for storing remediation history
            records.
        max_items: Maximum number of non-compliant resources to process
            (default 25).
        region_name: AWS region override.

    Returns:
        A :class:`RemediationResult` with non_compliant_count,
        remediated_count, failed_count, and resource_ids.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    config = async_client("config", region_name=region_name)
    lambda_client = async_client("lambda", region_name=region_name)
    ddb = async_client("dynamodb", region_name=region_name)

    # ------------------------------------------------------------------
    # Get non-compliant resources (paginated)
    # ------------------------------------------------------------------
    non_compliant: list[dict[str, Any]] = []
    next_token: str | None = None

    while len(non_compliant) < max_items:
        params: dict[str, Any] = {
            "ConfigRuleName": config_rule_name,
            "ComplianceTypes": ["NON_COMPLIANT"],
        }
        if next_token:
            params["NextToken"] = next_token

        try:
            page = await config.call("GetComplianceDetailsByConfigRule", **params)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"config_rule_remediation_executor: GetComplianceDetailsByConfigRule failed for "
                f"{config_rule_name!r}",
            ) from exc

        for item in page.get("EvaluationResults", []):
            if len(non_compliant) >= max_items:
                break
            qualifier = item.get("EvaluationResultIdentifier", {}).get(
                "EvaluationResultQualifier", {}
            )
            result_time = item.get("ResultRecordedTime", datetime.now(tz=UTC))
            non_compliant.append(
                {
                    "resource_id": qualifier.get("ResourceId", ""),
                    "resource_type": qualifier.get("ResourceType", ""),
                    "annotation": item.get("Annotation", ""),
                    "result_recorded_time": result_time.isoformat()
                    if hasattr(result_time, "isoformat")
                    else str(result_time),
                }
            )

        next_token = page.get("NextToken")
        if not next_token:
            break

    non_compliant_count = len(non_compliant)
    remediated_count = 0
    failed_count = 0
    resource_ids: list[str] = []

    # ------------------------------------------------------------------
    # Invoke Lambda + record result in DynamoDB for each resource
    # ------------------------------------------------------------------
    for resource in non_compliant:
        resource_id = resource["resource_id"]
        resource_ids.append(resource_id)
        payload = json.dumps(
            {
                "config_rule_name": config_rule_name,
                "resource_id": resource_id,
                "resource_type": resource["resource_type"],
                "annotation": resource["annotation"],
            }
        )

        success = False
        error_message = ""
        try:
            resp = await lambda_client.call(
                "Invoke",
                FunctionName=remediation_lambda_arn,
                InvocationType="RequestResponse",
                Payload=payload.encode(),
            )
            if resp.get("FunctionError"):
                error_message = f"Lambda FunctionError: {resp['FunctionError']}"
                failed_count += 1
            else:
                remediated_count += 1
                success = True
        except RuntimeError as exc:
            error_message = str(exc)
            failed_count += 1

        # Record remediation history in DynamoDB
        try:
            await ddb.call(
                "PutItem",
                TableName=table_name,
                Item={
                    "config_rule_name": {"S": config_rule_name},
                    "resource_id": {"S": resource_id},
                    "resource_type": {"S": resource["resource_type"]},
                    "remediation_lambda_arn": {"S": remediation_lambda_arn},
                    "success": {"BOOL": success},
                    "error_message": {"S": error_message},
                    "remediated_at": {"S": datetime.now(tz=UTC).isoformat()},
                },
            )
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"config_rule_remediation_executor: DynamoDB PutItem failed for {resource_id!r}",
            ) from exc

    logger.info(
        "config_rule_remediation_executor: rule=%r non_compliant=%d remediated=%d failed=%d",
        config_rule_name,
        non_compliant_count,
        remediated_count,
        failed_count,
    )
    return RemediationResult(
        non_compliant_count=non_compliant_count,
        remediated_count=remediated_count,
        failed_count=failed_count,
        resource_ids=resource_ids,
    )


# ---------------------------------------------------------------------------
# 2. Organizations SCP Drift Detector
# ---------------------------------------------------------------------------


async def organizations_scp_drift_detector(
    bucket: str,
    baseline_key: str,
    sns_topic_arn: str,
    region_name: str | None = None,
) -> SCPDriftResult:
    """List all SCPs, compare against an S3 baseline, report drifts via SNS.

    Downloads the baseline SCP document map from *bucket*/*baseline_key*
    (a JSON object mapping policy ID or name to policy document), lists all
    Service Control Policies from AWS Organizations, compares each policy's
    document to the baseline, and publishes a drift report to *sns_topic_arn*
    whenever drifts are found.

    Args:
        bucket: S3 bucket containing the baseline SCP JSON file.
        baseline_key: S3 object key for the baseline JSON.
        sns_topic_arn: SNS topic ARN to publish the drift report to.
        region_name: AWS region override.

    Returns:
        A :class:`SCPDriftResult` with total_policies, drifted_policies, and
        drift_details.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    orgs = async_client("organizations", region_name=region_name)
    s3 = async_client("s3", region_name=region_name)

    # ------------------------------------------------------------------
    # Download baseline from S3
    # ------------------------------------------------------------------
    try:
        obj = await s3.call("GetObject", Bucket=bucket, Key=baseline_key)
        body_bytes = obj.get("Body", b"")
        if hasattr(body_bytes, "read"):
            body_bytes = body_bytes.read()
        baseline: dict[str, Any] = json.loads(
            body_bytes.decode("utf-8") if isinstance(body_bytes, bytes) else body_bytes
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            "organizations_scp_drift_detector: failed to download baseline from S3",
        ) from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"organizations_scp_drift_detector: baseline at s3://{bucket}/{baseline_key} "
            "is not valid JSON"
        ) from exc

    # ------------------------------------------------------------------
    # List all SCPs from Organizations (paginated)
    # ------------------------------------------------------------------
    policies: list[dict[str, Any]] = []
    next_token: str | None = None

    while True:
        params: dict[str, Any] = {"Filter": "SERVICE_CONTROL_POLICY"}
        if next_token:
            params["NextToken"] = next_token
        try:
            page = await orgs.call("ListPolicies", **params)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, "organizations_scp_drift_detector: ListPolicies failed"
            ) from exc
        policies.extend(page.get("Policies", []))
        next_token = page.get("NextToken")
        if not next_token:
            break

    # ------------------------------------------------------------------
    # Describe each policy and compare to baseline
    # ------------------------------------------------------------------
    drift_details: list[dict[str, Any]] = []
    total_policies = len(policies)

    for policy in policies:
        policy_id = policy["Id"]
        policy_name = policy["Name"]

        try:
            detail = await orgs.call("DescribePolicy", PolicyId=policy_id)
            current_document = detail.get("Policy", {}).get("Content", "")
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"organizations_scp_drift_detector: DescribePolicy failed for {policy_id!r}",
            ) from exc

        try:
            current_doc_obj = json.loads(current_document) if current_document else {}
        except json.JSONDecodeError:
            current_doc_obj = {"_raw": current_document}

        baseline_doc_obj = baseline.get(policy_id, baseline.get(policy_name))

        if baseline_doc_obj is None:
            drift_details.append(
                {
                    "policy_id": policy_id,
                    "policy_name": policy_name,
                    "drift_type": "POLICY_NOT_IN_BASELINE",
                    "current_document": current_doc_obj,
                    "baseline_document": None,
                }
            )
        elif json.dumps(current_doc_obj, sort_keys=True) != json.dumps(
            baseline_doc_obj, sort_keys=True
        ):
            drift_details.append(
                {
                    "policy_id": policy_id,
                    "policy_name": policy_name,
                    "drift_type": "DOCUMENT_CHANGED",
                    "current_document": current_doc_obj,
                    "baseline_document": baseline_doc_obj,
                }
            )

    # Detect policies in baseline but missing from AWS
    current_ids = {p["Id"] for p in policies}
    current_names = {p["Name"] for p in policies}
    for baseline_ref, doc in baseline.items():
        if baseline_ref not in current_ids and baseline_ref not in current_names:
            drift_details.append(
                {
                    "policy_id": baseline_ref,
                    "policy_name": baseline_ref,
                    "drift_type": "POLICY_DELETED_FROM_AWS",
                    "current_document": None,
                    "baseline_document": doc,
                }
            )

    # ------------------------------------------------------------------
    # Publish drift report to SNS (when drifts found)
    # ------------------------------------------------------------------
    if drift_details:
        sns = async_client("sns", region_name=region_name)
        summary = (
            f"SCP Drift Detected — {len(drift_details)} drift(s) across "
            f"{total_policies} policies\n\n"
        )
        for d in drift_details:
            summary += f"  [{d['drift_type']}] {d['policy_name']} ({d['policy_id']})\n"
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="SCP Drift Alert",
                Message=summary,
            )
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, "organizations_scp_drift_detector: SNS Publish failed"
            ) from exc

    logger.info(
        "organizations_scp_drift_detector: total=%d drifted=%d",
        total_policies,
        len(drift_details),
    )
    return SCPDriftResult(
        total_policies=total_policies,
        drifted_policies=len(drift_details),
        drift_details=drift_details,
    )


# ---------------------------------------------------------------------------
# 3. SSO Permission Set Auditor
# ---------------------------------------------------------------------------


async def sso_permission_set_auditor(
    instance_arn: str,
    bucket: str,
    report_key: str,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> SSOAuditResult:
    """Enumerate SSO Admin permission sets and account assignments, write report.

    Lists all permission sets for *instance_arn*, retrieves details and
    account assignments for each, compiles a JSON compliance report, uploads
    it to S3 at *bucket*/*report_key*, and optionally notifies via SNS.

    Args:
        instance_arn: AWS SSO Admin instance ARN.
        bucket: S3 bucket for the audit report.
        report_key: S3 object key for the compliance report JSON.
        sns_topic_arn: Optional SNS topic ARN for completion notification.
        region_name: AWS region override.

    Returns:
        A :class:`SSOAuditResult` with permission_sets_count,
        total_assignments, and report_s3_key.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    sso = async_client("sso-admin", region_name=region_name)
    s3 = async_client("s3", region_name=region_name)

    # ------------------------------------------------------------------
    # List all permission sets (paginated)
    # ------------------------------------------------------------------
    permission_set_arns: list[str] = []
    next_token: str | None = None

    while True:
        params: dict[str, Any] = {"InstanceArn": instance_arn}
        if next_token:
            params["NextToken"] = next_token
        try:
            page = await sso.call("ListPermissionSets", **params)
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, "sso_permission_set_auditor: ListPermissionSets failed"
            ) from exc
        permission_set_arns.extend(page.get("PermissionSets", []))
        next_token = page.get("NextToken")
        if not next_token:
            break

    report_entries: list[dict[str, Any]] = []
    total_assignments = 0

    for ps_arn in permission_set_arns:
        # Describe permission set
        try:
            detail_resp = await sso.call(
                "DescribePermissionSet",
                InstanceArn=instance_arn,
                PermissionSetArn=ps_arn,
            )
            ps_detail = detail_resp.get("PermissionSet", {})
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"sso_permission_set_auditor: DescribePermissionSet failed for {ps_arn!r}",
            ) from exc

        # List account assignments (paginated)
        account_ids: list[str] = []
        assign_token: str | None = None
        while True:
            assign_params: dict[str, Any] = {
                "InstanceArn": instance_arn,
                "PermissionSetArn": ps_arn,
            }
            if assign_token:
                assign_params["NextToken"] = assign_token
            try:
                assign_page = await sso.call(
                    "ListAccountsForProvisionedPermissionSet", **assign_params
                )
            except RuntimeError as exc:
                raise wrap_aws_error(
                    exc,
                    f"sso_permission_set_auditor: ListAccountsForProvisionedPermissionSet "
                    f"failed for {ps_arn!r}",
                ) from exc
            account_ids.extend(assign_page.get("AccountIds", []))
            assign_token = assign_page.get("NextToken")
            if not assign_token:
                break

        total_assignments += len(account_ids)
        creation_date = ps_detail.get("CreatedDate", datetime.now(tz=UTC))
        report_entries.append(
            {
                "permission_set_arn": ps_arn,
                "name": ps_detail.get("Name", ""),
                "description": ps_detail.get("Description", ""),
                "session_duration": ps_detail.get("SessionDuration", ""),
                "created_date": creation_date.isoformat()
                if hasattr(creation_date, "isoformat")
                else str(creation_date),
                "account_ids": account_ids,
                "account_count": len(account_ids),
            }
        )

    # ------------------------------------------------------------------
    # Compile and upload report to S3
    # ------------------------------------------------------------------
    report = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "instance_arn": instance_arn,
        "permission_sets_count": len(permission_set_arns),
        "total_assignments": total_assignments,
        "permission_sets": report_entries,
    }

    try:
        await s3.call(
            "PutObject",
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "sso_permission_set_auditor: S3 PutObject failed") from exc

    # ------------------------------------------------------------------
    # Notify via SNS (optional)
    # ------------------------------------------------------------------
    if sns_topic_arn:
        sns = async_client("sns", region_name=region_name)
        message = (
            f"SSO Permission Set Audit Complete\n\n"
            f"Instance: {instance_arn}\n"
            f"Permission sets audited: {len(permission_set_arns)}\n"
            f"Total account assignments: {total_assignments}\n"
            f"Report: s3://{bucket}/{report_key}"
        )
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="SSO Audit Report",
                Message=message,
            )
        except RuntimeError as exc:
            raise wrap_aws_error(exc, "sso_permission_set_auditor: SNS Publish failed") from exc

    logger.info(
        "sso_permission_set_auditor: permission_sets=%d assignments=%d report_key=%s",
        len(permission_set_arns),
        total_assignments,
        report_key,
    )
    return SSOAuditResult(
        permission_sets_count=len(permission_set_arns),
        total_assignments=total_assignments,
        report_s3_key=report_key,
    )


# ---------------------------------------------------------------------------
# 4. KMS Key Rotation Auditor
# ---------------------------------------------------------------------------


async def kms_key_rotation_auditor(
    bucket: str,
    report_key: str,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> KMSRotationAuditResult:
    """List all KMS customer-managed keys, check rotation status, report to S3.

    Retrieves all KMS keys in the account, filters to customer-managed keys
    (KeyManager == CUSTOMER), checks automatic rotation status for each,
    compiles a compliance report, uploads it to S3, and optionally publishes
    an SNS alert when any keys have rotation disabled.

    Args:
        bucket: S3 bucket for the rotation audit report.
        report_key: S3 object key for the report JSON.
        sns_topic_arn: Optional SNS topic ARN to alert on non-compliant keys.
        region_name: AWS region override.

    Returns:
        A :class:`KMSRotationAuditResult` with total_keys, rotation_enabled,
        rotation_disabled, and report_s3_key.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    kms = async_client("kms", region_name=region_name)
    s3 = async_client("s3", region_name=region_name)

    # ------------------------------------------------------------------
    # List all KMS keys (paginated via Marker/Truncated pattern)
    # ------------------------------------------------------------------
    all_keys: list[dict[str, Any]] = []
    marker: str | None = None

    while True:
        params: dict[str, Any] = {}
        if marker:
            params["Marker"] = marker
        try:
            page = await kms.call("ListKeys", **params)
        except RuntimeError as exc:
            raise wrap_aws_error(exc, "kms_key_rotation_auditor: ListKeys failed") from exc
        all_keys.extend(page.get("Keys", []))
        if not page.get("Truncated", False):
            break
        marker = page.get("NextMarker")
        if not marker:
            break

    # ------------------------------------------------------------------
    # Filter to customer-managed keys and check rotation status
    # ------------------------------------------------------------------
    rotation_enabled_count = 0
    rotation_disabled_count = 0
    key_reports: list[dict[str, Any]] = []

    for key in all_keys:
        key_id = key["KeyId"]

        try:
            desc = await kms.call("DescribeKey", KeyId=key_id)
            meta = desc.get("KeyMetadata", {})
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc,
                f"kms_key_rotation_auditor: DescribeKey failed for {key_id!r}",
            ) from exc

        if meta.get("KeyManager", "") != "CUSTOMER":
            continue

        key_state = meta.get("KeyState", "")
        if key_state in ("PendingDeletion", "Unavailable"):
            continue

        rotation_enabled = False
        try:
            rotation_resp = await kms.call("GetKeyRotationStatus", KeyId=key_id)
            rotation_enabled = rotation_resp.get("KeyRotationEnabled", False)
        except RuntimeError:
            rotation_enabled = False

        if rotation_enabled:
            rotation_enabled_count += 1
        else:
            rotation_disabled_count += 1

        creation_date = meta.get("CreationDate", datetime.now(tz=UTC))
        key_reports.append(
            {
                "key_id": key_id,
                "key_arn": meta.get("Arn", ""),
                "description": meta.get("Description", ""),
                "key_state": key_state,
                "key_usage": meta.get("KeyUsage", ""),
                "rotation_enabled": rotation_enabled,
                "creation_date": creation_date.isoformat()
                if hasattr(creation_date, "isoformat")
                else str(creation_date),
                "compliant": rotation_enabled,
            }
        )

    total_keys = rotation_enabled_count + rotation_disabled_count

    # ------------------------------------------------------------------
    # Compile and upload report to S3
    # ------------------------------------------------------------------
    report = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "total_keys": total_keys,
        "rotation_enabled": rotation_enabled_count,
        "rotation_disabled": rotation_disabled_count,
        "compliance_rate_pct": round(
            (rotation_enabled_count / total_keys * 100) if total_keys else 100.0, 2
        ),
        "keys": key_reports,
    }

    try:
        await s3.call(
            "PutObject",
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "kms_key_rotation_auditor: S3 PutObject failed") from exc

    # ------------------------------------------------------------------
    # Alert via SNS if any keys have rotation disabled (optional)
    # ------------------------------------------------------------------
    if sns_topic_arn and rotation_disabled_count > 0:
        sns = async_client("sns", region_name=region_name)
        non_compliant_keys = [k for k in key_reports if not k["rotation_enabled"]]
        key_list = "\n".join(
            f"  {k['key_id']} — {k['description'] or 'no description'}"
            for k in non_compliant_keys[:20]
        )
        message = (
            f"KMS Key Rotation Audit Alert\n\n"
            f"Total customer-managed keys: {total_keys}\n"
            f"Rotation enabled: {rotation_enabled_count}\n"
            f"Rotation DISABLED: {rotation_disabled_count}\n\n"
            f"Non-compliant keys (first 20):\n{key_list}\n\n"
            f"Full report: s3://{bucket}/{report_key}"
        )
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="KMS Key Rotation Non-Compliance Alert",
                Message=message,
            )
        except RuntimeError as exc:
            raise wrap_aws_error(exc, "kms_key_rotation_auditor: SNS Publish failed") from exc

    logger.info(
        "kms_key_rotation_auditor: total=%d enabled=%d disabled=%d report_key=%s",
        total_keys,
        rotation_enabled_count,
        rotation_disabled_count,
        report_key,
    )
    return KMSRotationAuditResult(
        total_keys=total_keys,
        rotation_enabled=rotation_enabled_count,
        rotation_disabled=rotation_disabled_count,
        report_s3_key=report_key,
    )
