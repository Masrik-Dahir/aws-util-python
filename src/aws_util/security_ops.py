"""security_ops — Multi-service security and compliance utilities.

Combines IAM, KMS, Secrets Manager, S3, CloudWatch, SNS, Cognito, SSM,
EC2, and CloudFormation for common security automation workflows.
"""

from __future__ import annotations

import contextlib
import json
from datetime import UTC, datetime, timedelta
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AlarmProvisionResult",
    "CertExpiryResult",
    "CognitoUserResult",
    "GroupSyncResult",
    "IAMKeyRotationResult",
    "PublicBucketAuditResult",
    "ShieldProtectionResult",
    "SignedUrlResult",
    "TemplateValidationResult",
    "TokenEnrichResult",
    "WAFBlocklistResult",
    "acm_certificate_expiry_monitor",
    "audit_public_s3_buckets",
    "cloudfront_signed_url_factory",
    "cognito_bulk_create_users",
    "cognito_group_sync_to_dynamodb",
    "cognito_pre_token_enricher",
    "create_cloudwatch_alarm_with_sns",
    "enforce_bucket_versioning",
    "iam_roles_report_to_s3",
    "kms_encrypt_to_secret",
    "rotate_iam_access_key",
    "shield_advanced_protection_manager",
    "sync_secret_to_ssm",
    "tag_ec2_instances_from_ssm",
    "validate_and_store_cfn_template",
    "waf_ip_blocklist_updater",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class PublicBucketAuditResult(BaseModel):
    """Result of auditing S3 buckets for public access."""

    model_config = ConfigDict(frozen=True)

    public_buckets: list[str]
    total_scanned: int
    notification_sent: bool = False


class IAMKeyRotationResult(BaseModel):
    """Result of an IAM access-key rotation."""

    model_config = ConfigDict(frozen=True)

    username: str
    new_access_key_id: str
    secret_name: str
    old_key_deactivated: bool


class AlarmProvisionResult(BaseModel):
    """Result of provisioning a CloudWatch alarm wired to SNS."""

    model_config = ConfigDict(frozen=True)

    alarm_name: str
    topic_arn: str
    created: bool = True


class CognitoUserResult(BaseModel):
    """Result of creating a single Cognito user."""

    model_config = ConfigDict(frozen=True)

    username: str
    user_status: str
    email_sent: bool = False


class TemplateValidationResult(BaseModel):
    """Result of uploading and validating a CloudFormation template."""

    model_config = ConfigDict(frozen=True)

    s3_key: str
    valid: bool
    parameters: list[str] = []
    capabilities: list[str] = []


# ---------------------------------------------------------------------------
# 1. Public S3 bucket audit
# ---------------------------------------------------------------------------


def audit_public_s3_buckets(
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> PublicBucketAuditResult:
    """Scan all S3 buckets and flag those with public access enabled.

    A bucket is considered public when any of its four public-access-block
    settings is disabled or when no block configuration exists at all.

    Args:
        sns_topic_arn: Optional SNS topic ARN to notify if public buckets found.
        region_name: AWS region override.

    Returns:
        A :class:`PublicBucketAuditResult` with the list of public bucket names.

    Raises:
        RuntimeError: If the bucket listing call fails.
    """
    s3 = get_client("s3", region_name)
    try:
        buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    except ClientError as exc:
        raise wrap_aws_error(exc, "audit_public_s3_buckets list_buckets failed") from exc

    public: list[str] = []
    for bucket in buckets:
        try:
            resp = s3.get_public_access_block(Bucket=bucket)
            cfg = resp["PublicAccessBlockConfiguration"]
            if not all(
                [
                    cfg.get("BlockPublicAcls", False),
                    cfg.get("IgnorePublicAcls", False),
                    cfg.get("BlockPublicPolicy", False),
                    cfg.get("RestrictPublicBuckets", False),
                ]
            ):
                public.append(bucket)
        except ClientError:
            # No public-access-block → treated as public
            public.append(bucket)

    notification_sent = False
    if public and sns_topic_arn:
        sns = get_client("sns", region_name)
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="Public S3 Buckets Detected",
                Message=(f"Found {len(public)} public bucket(s):\n" + "\n".join(public)),
            )
            notification_sent = True
        except ClientError:
            pass

    return PublicBucketAuditResult(
        public_buckets=public,
        total_scanned=len(buckets),
        notification_sent=notification_sent,
    )


# ---------------------------------------------------------------------------
# 2. IAM access-key rotation → Secrets Manager
# ---------------------------------------------------------------------------


def rotate_iam_access_key(
    username: str,
    secret_name: str,
    region_name: str | None = None,
) -> IAMKeyRotationResult:
    """Rotate an IAM user's access key and store the new one in Secrets Manager.

    Creates a new key pair, stores it (creates the secret if needed), then
    deactivates the oldest existing key.

    Args:
        username: IAM username.
        secret_name: Secrets Manager secret name for the new credentials.
        region_name: AWS region override.

    Returns:
        An :class:`IAMKeyRotationResult` with the new key ID.

    Raises:
        RuntimeError: If creation, storage, or deactivation fails.
    """
    iam = get_client("iam", region_name)
    sm = get_client("secretsmanager", region_name)

    try:
        new_key = iam.create_access_key(UserName=username)["AccessKey"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"rotate_iam_access_key create failed for {username!r}") from exc

    secret_value = json.dumps(
        {
            "access_key_id": new_key["AccessKeyId"],
            "secret_access_key": new_key["SecretAccessKey"],
            "username": username,
        }
    )
    try:
        try:
            sm.put_secret_value(SecretId=secret_name, SecretString=secret_value)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                sm.create_secret(Name=secret_name, SecretString=secret_value)
            else:
                raise
    except ClientError as exc:
        raise wrap_aws_error(exc, "rotate_iam_access_key secret store failed") from exc

    old_key_deactivated = False
    try:
        keys = iam.list_access_keys(UserName=username).get("AccessKeyMetadata", [])
        old_keys = [k for k in keys if k["AccessKeyId"] != new_key["AccessKeyId"]]
        if old_keys:
            oldest = sorted(old_keys, key=lambda k: k["CreateDate"])[0]
            iam.update_access_key(
                UserName=username,
                AccessKeyId=oldest["AccessKeyId"],
                Status="Inactive",
            )
            old_key_deactivated = True
    except ClientError as exc:
        raise wrap_aws_error(exc, "rotate_iam_access_key deactivate failed") from exc

    return IAMKeyRotationResult(
        username=username,
        new_access_key_id=new_key["AccessKeyId"],
        secret_name=secret_name,
        old_key_deactivated=old_key_deactivated,
    )


# ---------------------------------------------------------------------------
# 3. KMS encrypt → Secrets Manager store
# ---------------------------------------------------------------------------


def kms_encrypt_to_secret(
    plaintext: str,
    secret_name: str,
    kms_key_id: str,
    region_name: str | None = None,
) -> str:
    """KMS-encrypt a value and store the ciphertext in Secrets Manager.

    The stored secret is a JSON object containing the base64-encoded
    ciphertext and the KMS key ID for future decryption.

    Args:
        plaintext: Value to encrypt.
        secret_name: Secrets Manager secret name.
        kms_key_id: KMS key ID or ARN.
        region_name: AWS region override.

    Returns:
        The ARN of the created or updated secret.

    Raises:
        RuntimeError: If encryption or storage fails.
    """
    import base64

    kms = get_client("kms", region_name)
    sm = get_client("secretsmanager", region_name)

    try:
        resp = kms.encrypt(KeyId=kms_key_id, Plaintext=plaintext.encode())
        ciphertext_b64 = base64.b64encode(resp["CiphertextBlob"]).decode()
    except ClientError as exc:
        raise wrap_aws_error(exc, "kms_encrypt_to_secret encryption failed") from exc

    payload = json.dumps({"ciphertext": ciphertext_b64, "kms_key_id": kms_key_id})
    try:
        try:
            resp = sm.put_secret_value(  # type: ignore[assignment]
                SecretId=secret_name, SecretString=payload
            )
            return resp.get("ARN", secret_name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceNotFoundException":
                resp = sm.create_secret(  # type: ignore[assignment]
                    Name=secret_name,
                    SecretString=payload,
                    KmsKeyId=kms_key_id,
                )
                return resp["ARN"]
            raise
    except ClientError as exc:
        raise wrap_aws_error(exc, "kms_encrypt_to_secret secret store failed") from exc


# ---------------------------------------------------------------------------
# 4. IAM roles report → S3
# ---------------------------------------------------------------------------


def iam_roles_report_to_s3(
    s3_bucket: str,
    s3_key: str,
    region_name: str | None = None,
) -> str:
    """Export all IAM roles with last-used metadata to S3 as JSON.

    Args:
        s3_bucket: Destination S3 bucket.
        s3_key: Destination S3 object key.
        region_name: AWS region override.

    Returns:
        The S3 key of the written report.

    Raises:
        RuntimeError: If IAM listing or S3 upload fails.
    """
    iam = get_client("iam", region_name)
    s3 = get_client("s3", region_name)

    try:
        paginator = iam.get_paginator("list_roles")
        roles: list[dict[str, Any]] = []
        for page in paginator.paginate():
            for role in page.get("Roles", []):
                last_used = role.get("RoleLastUsed", {})
                last_used_date = last_used.get("LastUsedDate")
                roles.append(
                    {
                        "role_name": role["RoleName"],
                        "role_arn": role["Arn"],
                        "created": role["CreateDate"].isoformat(),
                        "last_used_date": last_used_date.isoformat()
                        if hasattr(last_used_date, "isoformat")
                        else str(last_used_date or "Never"),
                        "last_used_region": last_used.get("Region", ""),
                    }
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "iam_roles_report_to_s3 list failed") from exc

    report = json.dumps({"roles": roles, "count": len(roles)}, indent=2)
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=report.encode())
    except ClientError as exc:
        raise wrap_aws_error(exc, "iam_roles_report_to_s3 upload failed") from exc

    return s3_key


# ---------------------------------------------------------------------------
# 5. S3 bucket versioning enforcement
# ---------------------------------------------------------------------------


def enforce_bucket_versioning(
    bucket_names: list[str],
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> list[str]:
    """Enable versioning on S3 buckets that do not already have it.

    Args:
        bucket_names: Bucket names to enforce versioning on.
        sns_topic_arn: Optional SNS topic to notify about newly enabled buckets.
        region_name: AWS region override.

    Returns:
        List of bucket names where versioning was newly enabled.

    Raises:
        RuntimeError: If enabling versioning fails for any bucket.
    """
    s3 = get_client("s3", region_name)
    updated: list[str] = []

    for bucket in bucket_names:
        try:
            resp = s3.get_bucket_versioning(Bucket=bucket)
            status = resp.get("Status", "")
            if status != "Enabled":
                s3.put_bucket_versioning(
                    Bucket=bucket,
                    VersioningConfiguration={"Status": "Enabled"},
                )
                updated.append(bucket)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"enforce_bucket_versioning failed for {bucket!r}") from exc

    if updated and sns_topic_arn:
        sns = get_client("sns", region_name)
        with contextlib.suppress(ClientError):
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="S3 Versioning Enabled",
                Message=(f"Versioning enabled on {len(updated)} bucket(s):\n" + "\n".join(updated)),
            )

    return updated


# ---------------------------------------------------------------------------
# 6. Cognito bulk user creation + SES invite
# ---------------------------------------------------------------------------


def cognito_bulk_create_users(
    user_pool_id: str,
    users: list[dict[str, str]],
    from_email: str | None = None,
    region_name: str | None = None,
) -> list[CognitoUserResult]:
    """Create Cognito users in bulk and optionally send SES invitation emails.

    Each dict in *users* must contain ``username`` and ``email`` keys.

    Args:
        user_pool_id: Cognito User Pool ID.
        users: List of ``{"username": "…", "email": "…"}`` dicts.
        from_email: Verified SES sender for invitation emails (optional).
        region_name: AWS region override.

    Returns:
        List of :class:`CognitoUserResult` for each user created.

    Raises:
        RuntimeError: If Cognito user creation fails.
    """
    cognito = get_client("cognito-idp", region_name)
    results: list[CognitoUserResult] = []

    for user in users:
        username = user["username"]
        email = user["email"]
        try:
            resp = cognito.admin_create_user(
                UserPoolId=user_pool_id,
                Username=username,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                ],
                MessageAction="SUPPRESS",
            )
            status = resp["User"]["UserStatus"]
        except ClientError as exc:
            raise wrap_aws_error(exc, f"cognito_bulk_create_users failed for {username!r}") from exc

        email_sent = False
        if from_email:
            ses = get_client("ses", region_name)
            try:
                ses.send_email(
                    Source=from_email,
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {"Data": "Your account has been created"},
                        "Body": {"Text": {"Data": (f"Hello {username}, your account is ready.")}},
                    },
                )
                email_sent = True
            except ClientError:
                pass  # email failure is non-fatal

        results.append(
            CognitoUserResult(
                username=username,
                user_status=status,
                email_sent=email_sent,
            )
        )

    return results


# ---------------------------------------------------------------------------
# 7. Secrets Manager → SSM Parameter Store sync
# ---------------------------------------------------------------------------


def sync_secret_to_ssm(
    secret_id: str,
    ssm_path: str,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> dict[str, str]:
    """Read a JSON secret and propagate each key as an SSM SecureString parameter.

    Each top-level key becomes ``{ssm_path}/{key}``.

    Args:
        secret_id: Secrets Manager secret name or ARN.
        ssm_path: SSM parameter path prefix (no trailing slash).
        kms_key_id: Optional KMS key for the SSM SecureString parameters.
        region_name: AWS region override.

    Returns:
        Mapping of secret key → SSM parameter name.

    Raises:
        RuntimeError: If secret retrieval or SSM write fails.
        ValueError: If the secret is not valid JSON.
    """
    sm = get_client("secretsmanager", region_name)
    ssm = get_client("ssm", region_name)

    try:
        raw = sm.get_secret_value(SecretId=secret_id).get("SecretString", "{}")
    except ClientError as exc:
        raise wrap_aws_error(exc, "sync_secret_to_ssm get_secret failed") from exc

    try:
        data: dict[str, str] = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"sync_secret_to_ssm: secret {secret_id!r} is not valid JSON") from exc

    path = ssm_path.rstrip("/")
    written: dict[str, str] = {}
    for key, value in data.items():
        param_name = f"{path}/{key}"
        kwargs: dict[str, Any] = {
            "Name": param_name,
            "Value": str(value),
            "Type": "SecureString",
            "Overwrite": True,
        }
        if kms_key_id:
            kwargs["KeyId"] = kms_key_id
        try:
            ssm.put_parameter(**kwargs)
            written[key] = param_name
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"sync_secret_to_ssm put_parameter failed for {param_name!r}"
            ) from exc

    return written


# ---------------------------------------------------------------------------
# 8. CloudWatch alarm + SNS topic provisioning
# ---------------------------------------------------------------------------


def create_cloudwatch_alarm_with_sns(
    alarm_name: str,
    namespace: str,
    metric_name: str,
    threshold: float,
    topic_name: str,
    comparison_operator: str = "GreaterThanOrEqualToThreshold",
    period: int = 300,
    evaluation_periods: int = 1,
    statistic: str = "Sum",
    region_name: str | None = None,
) -> AlarmProvisionResult:
    """Create a CloudWatch alarm wired to a new or existing SNS topic.

    The topic is created (idempotently) before the alarm so the ARN can be
    attached as an alarm action.

    Args:
        alarm_name: Unique alarm name.
        namespace: CloudWatch metric namespace.
        metric_name: Metric name.
        threshold: Alarm threshold.
        topic_name: SNS topic name (created if it does not exist).
        comparison_operator: Alarm comparison operator.
        period: Evaluation period in seconds.
        evaluation_periods: Consecutive periods before alarm state change.
        statistic: Metric statistic.
        region_name: AWS region override.

    Returns:
        An :class:`AlarmProvisionResult` with alarm name and topic ARN.

    Raises:
        RuntimeError: If topic creation or alarm creation fails.
    """
    sns = get_client("sns", region_name)
    cw = get_client("cloudwatch", region_name)

    try:
        topic_resp = sns.create_topic(Name=topic_name)
        topic_arn = topic_resp["TopicArn"]
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_cloudwatch_alarm_with_sns topic failed") from exc

    try:
        cw.put_metric_alarm(
            AlarmName=alarm_name,
            Namespace=namespace,
            MetricName=metric_name,
            Threshold=threshold,
            ComparisonOperator=comparison_operator,
            Period=period,
            EvaluationPeriods=evaluation_periods,
            Statistic=statistic,
            AlarmActions=[topic_arn],
            OKActions=[topic_arn],
            TreatMissingData="notBreaching",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_cloudwatch_alarm_with_sns alarm failed") from exc

    return AlarmProvisionResult(alarm_name=alarm_name, topic_arn=topic_arn)


# ---------------------------------------------------------------------------
# 9. Tag EC2 instances from SSM config
# ---------------------------------------------------------------------------


def tag_ec2_instances_from_ssm(
    instance_ids: list[str],
    ssm_param_name: str,
    region_name: str | None = None,
) -> dict[str, list[str]]:
    """Read a JSON tag map from SSM and apply it to EC2 instances.

    The SSM parameter value must be a JSON object of ``{tag_key: tag_value}``.

    Args:
        instance_ids: EC2 instance IDs to tag.
        ssm_param_name: SSM parameter name holding the JSON tag map.
        region_name: AWS region override.

    Returns:
        Mapping of instance ID → list of tag keys that were applied.

    Raises:
        RuntimeError: If SSM retrieval or EC2 tagging fails.
        ValueError: If the SSM parameter is not valid JSON.
    """
    ssm = get_client("ssm", region_name)
    ec2 = get_client("ec2", region_name)

    try:
        raw = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)["Parameter"]["Value"]
    except ClientError as exc:
        raise wrap_aws_error(exc, "tag_ec2_instances_from_ssm SSM fetch failed") from exc

    try:
        tag_map: dict[str, str] = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"tag_ec2_instances_from_ssm: {ssm_param_name!r} is not valid JSON"
        ) from exc

    tags = [{"Key": k, "Value": v} for k, v in tag_map.items()]
    result: dict[str, list[str]] = {}
    for iid in instance_ids:
        try:
            ec2.create_tags(Resources=[iid], Tags=tags)
            result[iid] = list(tag_map.keys())
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"tag_ec2_instances_from_ssm tagging failed for {iid!r}"
            ) from exc

    return result


# ---------------------------------------------------------------------------
# 10. CloudFormation template upload + validation
# ---------------------------------------------------------------------------


def validate_and_store_cfn_template(
    template: dict[str, Any],
    s3_bucket: str,
    s3_key: str,
    region_name: str | None = None,
) -> TemplateValidationResult:
    """Upload a CloudFormation template to S3 and validate it.

    Args:
        template: CloudFormation template as a Python dict.
        s3_bucket: S3 bucket for the template.
        s3_key: S3 object key.
        region_name: AWS region override.

    Returns:
        A :class:`TemplateValidationResult` with parameter and capability info.

    Raises:
        RuntimeError: If the upload or validation fails.
    """
    s3 = get_client("s3", region_name)
    cfn = get_client("cloudformation", region_name)

    template_body = json.dumps(template)
    try:
        s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=template_body.encode())
    except ClientError as exc:
        raise wrap_aws_error(exc, "validate_and_store_cfn_template upload failed") from exc

    try:
        resp = cfn.validate_template(TemplateBody=template_body)
        parameters = [p["ParameterKey"] for p in resp.get("Parameters", [])]
        capabilities = resp.get("Capabilities", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, "validate_and_store_cfn_template validation failed") from exc

    return TemplateValidationResult(
        s3_key=s3_key,
        valid=True,
        parameters=parameters,
        capabilities=capabilities,
    )


# ---------------------------------------------------------------------------
# 11. Cognito group sync to DynamoDB
# ---------------------------------------------------------------------------


class GroupSyncResult(BaseModel):
    """Result of syncing Cognito group memberships to DynamoDB."""

    model_config = ConfigDict(frozen=True)

    groups_synced: int
    users_synced: int
    items_written: int


def cognito_group_sync_to_dynamodb(
    user_pool_id: str,
    table_name: str,
    region_name: str | None = None,
) -> GroupSyncResult:
    """Sync Cognito User Pool group memberships to DynamoDB for fast lookups.

    Lists all groups in the pool, enumerates users in each group, and
    batch-writes items with pk=user_id / sk=group_name to DynamoDB.

    Args:
        user_pool_id: Cognito User Pool ID.
        table_name: DynamoDB table name to write membership records.
        region_name: AWS region override.

    Returns:
        A :class:`GroupSyncResult` with counts of groups, users, and items written.

    Raises:
        RuntimeError: If Cognito listing or DynamoDB batch write fails.
    """
    cognito = get_client("cognito-idp", region_name)
    ddb = get_client("dynamodb", region_name)

    try:
        groups_resp = cognito.list_groups(UserPoolId=user_pool_id)
        groups = [g["GroupName"] for g in groups_resp.get("Groups", [])]
    except ClientError as exc:
        raise wrap_aws_error(exc, "cognito_group_sync_to_dynamodb list_groups failed") from exc

    items: list[dict[str, Any]] = []
    users_seen: set[str] = set()

    for group_name in groups:
        try:
            users_resp = cognito.list_users_in_group(UserPoolId=user_pool_id, GroupName=group_name)
            for user in users_resp.get("Users", []):
                uid = user["Username"]
                users_seen.add(uid)
                items.append(
                    {
                        "PutRequest": {
                            "Item": {
                                "pk": {"S": uid},
                                "sk": {"S": group_name},
                                "group": {"S": group_name},
                                "user_id": {"S": uid},
                            }
                        }
                    }
                )
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"cognito_group_sync_to_dynamodb list_users_in_group failed for {group_name!r}"
            ) from exc

    # Batch write in chunks of 25 (DDB limit)
    written = 0
    for i in range(0, len(items), 25):
        chunk = items[i : i + 25]
        try:
            ddb.batch_write_item(RequestItems={table_name: chunk})
            written += len(chunk)
        except ClientError as exc:
            raise wrap_aws_error(
                exc, "cognito_group_sync_to_dynamodb batch_write_item failed"
            ) from exc

    return GroupSyncResult(
        groups_synced=len(groups),
        users_synced=len(users_seen),
        items_written=written,
    )


# ---------------------------------------------------------------------------
# 12. CloudFront signed URL factory
# ---------------------------------------------------------------------------


class SignedUrlResult(BaseModel):
    """Result of generating a CloudFront signed URL."""

    model_config = ConfigDict(frozen=True)

    signed_url: str
    expires_at: int
    key_pair_id: str


def cloudfront_signed_url_factory(
    distribution_domain: str,
    object_path: str,
    key_pair_id: str,
    secret_name: str,
    expiry_seconds: int = 3600,
    region_name: str | None = None,
) -> SignedUrlResult:
    """Generate a CloudFront signed URL using a private key stored in Secrets Manager.

    Retrieves the RSA private key from Secrets Manager, builds a canned
    CloudFront signed URL policy, signs it with the private key, and
    returns the complete signed URL.

    Args:
        distribution_domain: CloudFront distribution domain (e.g. ``d1234.cloudfront.net``).
        object_path: Object path including leading slash (e.g. ``/videos/clip.mp4``).
        key_pair_id: CloudFront key pair ID.
        secret_name: Secrets Manager secret containing the PEM private key.
        expiry_seconds: URL validity window in seconds (default 3600).
        region_name: AWS region override.

    Returns:
        A :class:`SignedUrlResult` with the signed URL and expiry timestamp.

    Raises:
        RuntimeError: If the secret retrieval or signing fails.
    """
    import base64
    import time
    from urllib.parse import urlencode

    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    sm = get_client("secretsmanager", region_name)
    try:
        raw = sm.get_secret_value(SecretId=secret_name).get("SecretString", "")
    except ClientError as exc:
        raise wrap_aws_error(exc, "cloudfront_signed_url_factory get_secret failed") from exc

    expires_at = int(time.time()) + expiry_seconds
    url = f"https://{distribution_domain}{object_path}"
    policy = (
        '{"Statement":[{"Resource":"'
        + url
        + '","Condition":{"DateLessThan":{"AWS:EpochTime":'
        + str(expires_at)
        + "}}}]}"
    )

    try:
        private_key = serialization.load_pem_private_key(raw.encode(), password=None)
        signature = private_key.sign(policy.encode(), padding.PKCS1v15(), hashes.SHA1())
        sig_b64 = (
            base64.b64encode(signature)
            .decode()
            .replace("+", "-")
            .replace("=", "_")
            .replace("/", "~")
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "cloudfront_signed_url_factory signing failed") from exc

    params = urlencode(
        {
            "Expires": expires_at,
            "Signature": sig_b64,
            "Key-Pair-Id": key_pair_id,
        }
    )
    signed_url = f"{url}?{params}"
    return SignedUrlResult(signed_url=signed_url, expires_at=expires_at, key_pair_id=key_pair_id)


# ---------------------------------------------------------------------------
# 13. WAF IP blocklist updater
# ---------------------------------------------------------------------------


class WAFBlocklistResult(BaseModel):
    """Result of updating a WAFv2 IP set from a threat feed."""

    model_config = ConfigDict(frozen=True)

    ips_added: int
    ips_removed: int
    total_ips: int


def waf_ip_blocklist_updater(
    ip_set_name: str,
    ip_set_id: str,
    scope: str,
    bucket: str,
    feed_key: str,
    table_name: str,
    region_name: str | None = None,
) -> WAFBlocklistResult:
    """Read IP CIDRs from S3 threat feed and update a WAFv2 IP set.

    Fetches a newline-delimited CIDR list from S3, computes the diff
    against the current IP set state, applies the update, and records
    the change history in DynamoDB.

    Args:
        ip_set_name: WAFv2 IP set name.
        ip_set_id: WAFv2 IP set ID.
        scope: ``"REGIONAL"`` or ``"CLOUDFRONT"``.
        bucket: S3 bucket containing the feed file.
        feed_key: S3 object key of the CIDR feed.
        table_name: DynamoDB table for change history.
        region_name: AWS region override.

    Returns:
        A :class:`WAFBlocklistResult` with counts of added/removed/total IPs.

    Raises:
        RuntimeError: If S3 fetch, WAF read/update, or DynamoDB write fails.
    """
    import time

    s3 = get_client("s3", region_name)
    wafv2 = get_client("wafv2", region_name)
    ddb = get_client("dynamodb", region_name)

    try:
        obj = s3.get_object(Bucket=bucket, Key=feed_key)
        feed_cidrs = set(obj["Body"].read().decode().splitlines())
        feed_cidrs = {c.strip() for c in feed_cidrs if c.strip()}
    except ClientError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater s3 get_object failed") from exc

    try:
        ip_set_resp = wafv2.get_ip_set(Name=ip_set_name, Scope=scope, Id=ip_set_id)
        current_addresses = set(ip_set_resp["IPSet"]["Addresses"])
        lock_token = ip_set_resp["LockToken"]
    except ClientError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater get_ip_set failed") from exc

    added = len(feed_cidrs - current_addresses)
    removed = len(current_addresses - feed_cidrs)
    new_addresses = list(feed_cidrs)

    try:
        wafv2.update_ip_set(
            Name=ip_set_name,
            Scope=scope,
            Id=ip_set_id,
            Addresses=new_addresses,
            LockToken=lock_token,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater update_ip_set failed") from exc

    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": ip_set_id},
                "sk": {"S": str(int(time.time()))},
                "ips_added": {"N": str(added)},
                "ips_removed": {"N": str(removed)},
                "total_ips": {"N": str(len(new_addresses))},
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater ddb put_item failed") from exc

    return WAFBlocklistResult(ips_added=added, ips_removed=removed, total_ips=len(new_addresses))


# ---------------------------------------------------------------------------
# 14. Shield Advanced protection manager
# ---------------------------------------------------------------------------


class ShieldProtectionResult(BaseModel):
    """Result of attaching Shield Advanced protections to resources."""

    model_config = ConfigDict(frozen=True)

    protections_created: int
    already_protected: int
    emergency_contact_set: bool


def shield_advanced_protection_manager(
    resource_arns: list[str],
    emergency_contact_email: str | None = None,
    region_name: str | None = None,
) -> ShieldProtectionResult:
    """Attach Shield Advanced protections to specified resource ARNs.

    Creates a Shield protection for each ARN (skips if already protected),
    then optionally sets an emergency contact for the DDoS Response Team.

    Args:
        resource_arns: List of resource ARNs to protect.
        emergency_contact_email: Optional email for DDoS Response Team contacts.
        region_name: AWS region override.

    Returns:
        A :class:`ShieldProtectionResult` with creation counts.

    Raises:
        RuntimeError: If Shield API calls fail unexpectedly.
    """
    shield = get_client("shield", region_name or "us-east-1")

    created = 0
    already = 0

    for arn in resource_arns:
        try:
            shield.create_protection(
                Name=arn.split(":")[-1][:128],
                ResourceArn=arn,
            )
            created += 1
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code in ("ResourceAlreadyExistsException", "AlreadyExistsException"):
                already += 1
            else:
                raise wrap_aws_error(
                    exc, f"shield_advanced_protection_manager failed for {arn!r}"
                ) from exc

    emergency_contact_set = False
    if emergency_contact_email:
        try:
            shield.update_emergency_contact_settings(
                EmergencyContactList=[{"EmailAddress": emergency_contact_email}]
            )
            emergency_contact_set = True
        except ClientError as exc:
            raise wrap_aws_error(
                exc, "shield_advanced_protection_manager emergency contact failed"
            ) from exc

    return ShieldProtectionResult(
        protections_created=created,
        already_protected=already,
        emergency_contact_set=emergency_contact_set,
    )


# ---------------------------------------------------------------------------
# 15. ACM certificate expiry monitor
# ---------------------------------------------------------------------------


class CertExpiryResult(BaseModel):
    """Result of ACM certificate expiry monitoring."""

    model_config = ConfigDict(frozen=True)

    total_certs: int
    expiring_count: int
    expiring_domains: list[str]
    alert_sent: bool


def acm_certificate_expiry_monitor(
    sns_topic_arn: str,
    days_threshold: int = 30,
    region_name: str | None = None,
) -> CertExpiryResult:
    """List ACM certificates expiring within N days and publish alerts to SNS.

    Paginates through all certificates, describes each one, checks the
    ``NotAfter`` date, and publishes an SNS notification when any are
    found expiring within the threshold.

    Args:
        sns_topic_arn: SNS topic ARN for alerts.
        days_threshold: Days before expiry to flag a certificate (default 30).
        region_name: AWS region override.

    Returns:
        A :class:`CertExpiryResult` with expiry counts and domains.

    Raises:
        RuntimeError: If ACM listing or SNS publish fails.
    """

    acm = get_client("acm", region_name)
    sns = get_client("sns", region_name)

    try:
        certs_resp = acm.list_certificates(CertificateStatuses=["ISSUED"])
        cert_list = certs_resp.get("CertificateSummaryList", [])
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "acm_certificate_expiry_monitor list_certificates failed"
        ) from exc

    threshold_dt = datetime.now(tz=UTC) + timedelta(days=days_threshold)
    expiring_domains: list[str] = []

    for cert_summary in cert_list:
        arn = cert_summary["CertificateArn"]
        try:
            detail = acm.describe_certificate(CertificateArn=arn)["Certificate"]
            not_after = detail.get("NotAfter")
            if not_after and not_after < threshold_dt:
                domain = detail.get("DomainName", arn)
                expiring_domains.append(domain)
        except ClientError:
            continue

    alert_sent = False
    if expiring_domains:
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=f"ACM Certificates Expiring Within {days_threshold} Days",
                Message=(
                    f"Found {len(expiring_domains)} certificate(s) expiring soon:\n"
                    + "\n".join(expiring_domains)
                ),
            )
            alert_sent = True
        except ClientError as exc:
            raise wrap_aws_error(exc, "acm_certificate_expiry_monitor SNS publish failed") from exc

    return CertExpiryResult(
        total_certs=len(cert_list),
        expiring_count=len(expiring_domains),
        expiring_domains=expiring_domains,
        alert_sent=alert_sent,
    )


# ---------------------------------------------------------------------------
# 16. Cognito pre-token enricher
# ---------------------------------------------------------------------------


class TokenEnrichResult(BaseModel):
    """Result of enriching Cognito pre-token-generation claims from DynamoDB."""

    model_config = ConfigDict(frozen=True)

    username: str
    claims_added: int
    claims: dict[str, str]


def cognito_pre_token_enricher(
    user_pool_id: str,
    username: str,
    table_name: str,
    claim_attributes: list[str],
    region_name: str | None = None,
) -> TokenEnrichResult:
    """Read user attributes from DynamoDB and format as Cognito custom claims.

    Fetches base user attributes from Cognito via ``admin_get_user``, then
    reads additional custom data from DynamoDB. Merges both into a claims
    dict keyed by the requested attribute names.

    Args:
        user_pool_id: Cognito User Pool ID.
        username: Username to enrich.
        table_name: DynamoDB table holding custom user data (pk=username).
        claim_attributes: DynamoDB attribute names to include as claims.
        region_name: AWS region override.

    Returns:
        A :class:`TokenEnrichResult` with the merged claims dict.

    Raises:
        RuntimeError: If Cognito or DynamoDB calls fail.
    """
    cognito = get_client("cognito-idp", region_name)
    ddb = get_client("dynamodb", region_name)

    try:
        user_resp = cognito.admin_get_user(UserPoolId=user_pool_id, Username=username)
        base_attrs = {a["Name"]: a["Value"] for a in user_resp.get("UserAttributes", [])}
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"cognito_pre_token_enricher admin_get_user failed for {username!r}"
        ) from exc

    custom_attrs: dict[str, str] = {}
    try:
        item_resp = ddb.get_item(
            TableName=table_name,
            Key={"pk": {"S": username}},
        )
        item = item_resp.get("Item", {})
        for attr in claim_attributes:
            val = item.get(attr, {})
            if val:
                custom_attrs[attr] = next(iter(val.values()))
    except ClientError as exc:
        raise wrap_aws_error(exc, "cognito_pre_token_enricher ddb get_item failed") from exc

    claims = {**base_attrs, **custom_attrs}
    filtered_claims = {k: v for k, v in claims.items() if k in claim_attributes or k in base_attrs}

    return TokenEnrichResult(
        username=username,
        claims_added=len(custom_attrs),
        claims=filtered_claims,
    )
