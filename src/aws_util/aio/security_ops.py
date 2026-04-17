"""Native async security ops using :mod:`aws_util.aio._engine`.

Combines IAM, KMS, Secrets Manager, S3, CloudWatch, SNS, Cognito, SSM,
EC2, and CloudFormation for common async security automation workflows.
"""

from __future__ import annotations

import base64
import contextlib
import json
from datetime import UTC
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.security_ops import (
    AlarmProvisionResult,
    CertExpiryResult,
    CognitoUserResult,
    GroupSyncResult,
    IAMKeyRotationResult,
    PublicBucketAuditResult,
    ShieldProtectionResult,
    SignedUrlResult,
    TemplateValidationResult,
    TokenEnrichResult,
    WAFBlocklistResult,
)

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
# 1. Public S3 bucket audit
# ---------------------------------------------------------------------------


async def audit_public_s3_buckets(
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> PublicBucketAuditResult:
    """Scan all S3 buckets and flag those with public access enabled.

    Args:
        sns_topic_arn: Optional SNS topic ARN to notify if public buckets found.
        region_name: AWS region override.

    Returns:
        A :class:`PublicBucketAuditResult` with the list of public bucket names.

    Raises:
        RuntimeError: If the bucket listing call fails.
    """
    s3 = async_client("s3", region_name)
    try:
        resp = await s3.call("ListBuckets")
        buckets = [b["Name"] for b in resp.get("Buckets", [])]
    except Exception as exc:
        raise wrap_aws_error(exc, "audit_public_s3_buckets list_buckets failed") from exc

    public: list[str] = []
    for bucket in buckets:
        try:
            resp = await s3.call(
                "GetPublicAccessBlock",
                Bucket=bucket,
            )
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
        except RuntimeError:
            # No public-access-block -> treated as public
            public.append(bucket)

    notification_sent = False
    if public and sns_topic_arn:
        sns = async_client("sns", region_name)
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="Public S3 Buckets Detected",
                Message=(f"Found {len(public)} public bucket(s):\n" + "\n".join(public)),
            )
            notification_sent = True
        except Exception:
            pass

    return PublicBucketAuditResult(
        public_buckets=public,
        total_scanned=len(buckets),
        notification_sent=notification_sent,
    )


# ---------------------------------------------------------------------------
# 2. IAM access-key rotation -> Secrets Manager
# ---------------------------------------------------------------------------


async def rotate_iam_access_key(
    username: str,
    secret_name: str,
    region_name: str | None = None,
) -> IAMKeyRotationResult:
    """Rotate an IAM user's access key and store the new one in Secrets Manager.

    Args:
        username: IAM username.
        secret_name: Secrets Manager secret name for the new credentials.
        region_name: AWS region override.

    Returns:
        An :class:`IAMKeyRotationResult` with the new key ID.

    Raises:
        RuntimeError: If creation, storage, or deactivation fails.
    """
    iam = async_client("iam", region_name)
    sm = async_client("secretsmanager", region_name)

    try:
        resp = await iam.call(
            "CreateAccessKey",
            UserName=username,
        )
        new_key = resp["AccessKey"]
    except Exception as exc:
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
            await sm.call(
                "PutSecretValue",
                SecretId=secret_name,
                SecretString=secret_value,
            )
        except RuntimeError as exc:
            if "ResourceNotFoundException" in str(exc):
                await sm.call(
                    "CreateSecret",
                    Name=secret_name,
                    SecretString=secret_value,
                )
            else:
                raise
    except Exception as exc:
        raise wrap_aws_error(exc, "rotate_iam_access_key secret store failed") from exc

    old_key_deactivated = False
    try:
        keys_resp = await iam.call(
            "ListAccessKeys",
            UserName=username,
        )
        keys = keys_resp.get("AccessKeyMetadata", [])
        old_keys = [k for k in keys if k["AccessKeyId"] != new_key["AccessKeyId"]]
        if old_keys:
            oldest = sorted(
                old_keys,
                key=lambda k: k["CreateDate"],
            )[0]
            await iam.call(
                "UpdateAccessKey",
                UserName=username,
                AccessKeyId=oldest["AccessKeyId"],
                Status="Inactive",
            )
            old_key_deactivated = True
    except Exception as exc:
        raise wrap_aws_error(exc, "rotate_iam_access_key deactivate failed") from exc

    return IAMKeyRotationResult(
        username=username,
        new_access_key_id=new_key["AccessKeyId"],
        secret_name=secret_name,
        old_key_deactivated=old_key_deactivated,
    )


# ---------------------------------------------------------------------------
# 3. KMS encrypt -> Secrets Manager store
# ---------------------------------------------------------------------------


async def kms_encrypt_to_secret(
    plaintext: str,
    secret_name: str,
    kms_key_id: str,
    region_name: str | None = None,
) -> str:
    """KMS-encrypt a value and store the ciphertext in Secrets Manager.

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
    kms = async_client("kms", region_name)
    sm = async_client("secretsmanager", region_name)

    try:
        resp = await kms.call(
            "Encrypt",
            KeyId=kms_key_id,
            Plaintext=plaintext.encode(),
        )
        ciphertext_b64 = base64.b64encode(resp["CiphertextBlob"]).decode()
    except Exception as exc:
        raise wrap_aws_error(exc, "kms_encrypt_to_secret encryption failed") from exc

    payload = json.dumps(
        {
            "ciphertext": ciphertext_b64,
            "kms_key_id": kms_key_id,
        }
    )
    try:
        try:
            resp = await sm.call(
                "PutSecretValue",
                SecretId=secret_name,
                SecretString=payload,
            )
            return resp.get("ARN", secret_name)
        except RuntimeError as exc:
            if "ResourceNotFoundException" in str(exc):
                resp = await sm.call(
                    "CreateSecret",
                    Name=secret_name,
                    SecretString=payload,
                    KmsKeyId=kms_key_id,
                )
                return resp["ARN"]
            raise
    except Exception as exc:
        raise wrap_aws_error(exc, "kms_encrypt_to_secret secret store failed") from exc


# ---------------------------------------------------------------------------
# 4. IAM roles report -> S3
# ---------------------------------------------------------------------------


async def iam_roles_report_to_s3(
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
    iam = async_client("iam", region_name)
    s3 = async_client("s3", region_name)

    try:
        raw_roles = await iam.paginate(
            "ListRoles",
            "Roles",
            token_input="Marker",
            token_output="Marker",
        )
        roles: list[dict[str, Any]] = []
        for role in raw_roles:
            last_used = role.get("RoleLastUsed", {})
            last_used_date = last_used.get("LastUsedDate")
            roles.append(
                {
                    "role_name": role["RoleName"],
                    "role_arn": role["Arn"],
                    "created": (
                        role["CreateDate"].isoformat()
                        if hasattr(role["CreateDate"], "isoformat")
                        else str(role["CreateDate"])
                    ),
                    "last_used_date": (
                        last_used_date.isoformat()
                        if hasattr(last_used_date, "isoformat")
                        else str(last_used_date or "Never")
                    ),
                    "last_used_region": last_used.get("Region", ""),
                }
            )
    except Exception as exc:
        raise wrap_aws_error(exc, "iam_roles_report_to_s3 list failed") from exc

    report = json.dumps(
        {"roles": roles, "count": len(roles)},
        indent=2,
    )
    try:
        await s3.call(
            "PutObject",
            Bucket=s3_bucket,
            Key=s3_key,
            Body=report.encode(),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "iam_roles_report_to_s3 upload failed") from exc

    return s3_key


# ---------------------------------------------------------------------------
# 5. S3 bucket versioning enforcement
# ---------------------------------------------------------------------------


async def enforce_bucket_versioning(
    bucket_names: list[str],
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> list[str]:
    """Enable versioning on S3 buckets that do not already have it.

    Args:
        bucket_names: Bucket names to enforce versioning on.
        sns_topic_arn: Optional SNS topic to notify.
        region_name: AWS region override.

    Returns:
        List of bucket names where versioning was newly enabled.

    Raises:
        RuntimeError: If enabling versioning fails for any bucket.
    """
    s3 = async_client("s3", region_name)
    updated: list[str] = []

    for bucket in bucket_names:
        try:
            resp = await s3.call(
                "GetBucketVersioning",
                Bucket=bucket,
            )
            status = resp.get("Status", "")
            if status != "Enabled":
                await s3.call(
                    "PutBucketVersioning",
                    Bucket=bucket,
                    VersioningConfiguration={"Status": "Enabled"},
                )
                updated.append(bucket)
        except Exception as exc:
            raise wrap_aws_error(exc, f"enforce_bucket_versioning failed for {bucket!r}") from exc

    if updated and sns_topic_arn:
        sns = async_client("sns", region_name)
        with contextlib.suppress(Exception):
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="S3 Versioning Enabled",
                Message=(f"Versioning enabled on {len(updated)} bucket(s):\n" + "\n".join(updated)),
            )

    return updated


# ---------------------------------------------------------------------------
# 6. Cognito bulk user creation + SES invite
# ---------------------------------------------------------------------------


async def cognito_bulk_create_users(
    user_pool_id: str,
    users: list[dict[str, str]],
    from_email: str | None = None,
    region_name: str | None = None,
) -> list[CognitoUserResult]:
    """Create Cognito users in bulk and optionally send SES invitation emails.

    Args:
        user_pool_id: Cognito User Pool ID.
        users: List of ``{"username": "...", "email": "..."}`` dicts.
        from_email: Verified SES sender for invitation emails.
        region_name: AWS region override.

    Returns:
        List of :class:`CognitoUserResult` for each user created.

    Raises:
        RuntimeError: If Cognito user creation fails.
    """
    cognito = async_client("cognito-idp", region_name)
    results: list[CognitoUserResult] = []

    for user in users:
        username = user["username"]
        email = user["email"]
        try:
            resp = await cognito.call(
                "AdminCreateUser",
                UserPoolId=user_pool_id,
                Username=username,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                ],
                MessageAction="SUPPRESS",
            )
            status = resp["User"]["UserStatus"]
        except Exception as exc:
            raise wrap_aws_error(exc, f"cognito_bulk_create_users failed for {username!r}") from exc

        email_sent = False
        if from_email:
            ses = async_client("ses", region_name)
            try:
                await ses.call(
                    "SendEmail",
                    Source=from_email,
                    Destination={"ToAddresses": [email]},
                    Message={
                        "Subject": {
                            "Data": "Your account has been created",
                        },
                        "Body": {
                            "Text": {
                                "Data": (f"Hello {username}, your account is ready."),
                            },
                        },
                    },
                )
                email_sent = True
            except Exception:
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
# 7. Secrets Manager -> SSM Parameter Store sync
# ---------------------------------------------------------------------------


async def sync_secret_to_ssm(
    secret_id: str,
    ssm_path: str,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> dict[str, str]:
    """Read a JSON secret and propagate each key as an SSM SecureString parameter.

    Args:
        secret_id: Secrets Manager secret name or ARN.
        ssm_path: SSM parameter path prefix (no trailing slash).
        kms_key_id: Optional KMS key for the SSM SecureString parameters.
        region_name: AWS region override.

    Returns:
        Mapping of secret key -> SSM parameter name.

    Raises:
        RuntimeError: If secret retrieval or SSM write fails.
        ValueError: If the secret is not valid JSON.
    """
    sm = async_client("secretsmanager", region_name)
    ssm = async_client("ssm", region_name)

    try:
        resp = await sm.call(
            "GetSecretValue",
            SecretId=secret_id,
        )
        raw = resp.get("SecretString", "{}")
    except Exception as exc:
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
            await ssm.call("PutParameter", **kwargs)
            written[key] = param_name
        except Exception as exc:
            raise wrap_aws_error(
                exc, f"sync_secret_to_ssm put_parameter failed for {param_name!r}"
            ) from exc

    return written


# ---------------------------------------------------------------------------
# 8. CloudWatch alarm + SNS topic provisioning
# ---------------------------------------------------------------------------


async def create_cloudwatch_alarm_with_sns(
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

    Args:
        alarm_name: Unique alarm name.
        namespace: CloudWatch metric namespace.
        metric_name: Metric name.
        threshold: Alarm threshold.
        topic_name: SNS topic name.
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
    sns = async_client("sns", region_name)
    cw = async_client("cloudwatch", region_name)

    try:
        topic_resp = await sns.call(
            "CreateTopic",
            Name=topic_name,
        )
        topic_arn = topic_resp["TopicArn"]
    except Exception as exc:
        raise wrap_aws_error(exc, "create_cloudwatch_alarm_with_sns topic failed") from exc

    try:
        await cw.call(
            "PutMetricAlarm",
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
    except Exception as exc:
        raise wrap_aws_error(exc, "create_cloudwatch_alarm_with_sns alarm failed") from exc

    return AlarmProvisionResult(
        alarm_name=alarm_name,
        topic_arn=topic_arn,
    )


# ---------------------------------------------------------------------------
# 9. Tag EC2 instances from SSM config
# ---------------------------------------------------------------------------


async def tag_ec2_instances_from_ssm(
    instance_ids: list[str],
    ssm_param_name: str,
    region_name: str | None = None,
) -> dict[str, list[str]]:
    """Read a JSON tag map from SSM and apply it to EC2 instances.

    Args:
        instance_ids: EC2 instance IDs to tag.
        ssm_param_name: SSM parameter name holding the JSON tag map.
        region_name: AWS region override.

    Returns:
        Mapping of instance ID -> list of tag keys that were applied.

    Raises:
        RuntimeError: If SSM retrieval or EC2 tagging fails.
        ValueError: If the SSM parameter is not valid JSON.
    """
    ssm = async_client("ssm", region_name)
    ec2 = async_client("ec2", region_name)

    try:
        resp = await ssm.call(
            "GetParameter",
            Name=ssm_param_name,
            WithDecryption=True,
        )
        raw = resp["Parameter"]["Value"]
    except Exception as exc:
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
            await ec2.call(
                "CreateTags",
                Resources=[iid],
                Tags=tags,
            )
            result[iid] = list(tag_map.keys())
        except Exception as exc:
            raise wrap_aws_error(
                exc, f"tag_ec2_instances_from_ssm tagging failed for {iid!r}"
            ) from exc

    return result


# ---------------------------------------------------------------------------
# 10. CloudFormation template upload + validation
# ---------------------------------------------------------------------------


async def validate_and_store_cfn_template(
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
    s3 = async_client("s3", region_name)
    cfn = async_client("cloudformation", region_name)

    template_body = json.dumps(template)

    # Upload and validate can be done in parallel
    try:
        await s3.call(
            "PutObject",
            Bucket=s3_bucket,
            Key=s3_key,
            Body=template_body.encode(),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "validate_and_store_cfn_template upload failed") from exc

    try:
        resp = await cfn.call(
            "ValidateTemplate",
            TemplateBody=template_body,
        )
        parameters = [p["ParameterKey"] for p in resp.get("Parameters", [])]
        capabilities = resp.get("Capabilities", [])
    except Exception as exc:
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


async def cognito_group_sync_to_dynamodb(
    user_pool_id: str,
    table_name: str,
    region_name: str | None = None,
) -> GroupSyncResult:
    """Sync Cognito User Pool group memberships to DynamoDB for fast lookups.

    Args:
        user_pool_id: Cognito User Pool ID.
        table_name: DynamoDB table name to write membership records.
        region_name: AWS region override.

    Returns:
        A :class:`GroupSyncResult` with counts of groups, users, and items written.

    Raises:
        RuntimeError: If Cognito listing or DynamoDB batch write fails.
    """
    cognito = async_client("cognito-idp", region_name)
    ddb = async_client("dynamodb", region_name)

    try:
        groups_resp = await cognito.call("ListGroups", UserPoolId=user_pool_id)
        groups = [g["GroupName"] for g in groups_resp.get("Groups", [])]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "cognito_group_sync_to_dynamodb list_groups failed") from exc

    items: list[dict[str, Any]] = []
    users_seen: set[str] = set()

    for group_name in groups:
        try:
            users_resp = await cognito.call(
                "ListUsersInGroup", UserPoolId=user_pool_id, GroupName=group_name
            )
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
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"cognito_group_sync_to_dynamodb list_users_in_group failed for {group_name!r}"
            ) from exc

    written = 0
    for i in range(0, len(items), 25):
        chunk = items[i : i + 25]
        try:
            await ddb.call("BatchWriteItem", RequestItems={table_name: chunk})
            written += len(chunk)
        except RuntimeError as exc:
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


async def cloudfront_signed_url_factory(
    distribution_domain: str,
    object_path: str,
    key_pair_id: str,
    secret_name: str,
    expiry_seconds: int = 3600,
    region_name: str | None = None,
) -> SignedUrlResult:
    """Generate a CloudFront signed URL using a private key stored in Secrets Manager.

    Args:
        distribution_domain: CloudFront distribution domain.
        object_path: Object path including leading slash.
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

    sm = async_client("secretsmanager", region_name)
    try:
        resp = await sm.call("GetSecretValue", SecretId=secret_name)
        raw = resp.get("SecretString", "")
    except RuntimeError as exc:
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

    params = urlencode({"Expires": expires_at, "Signature": sig_b64, "Key-Pair-Id": key_pair_id})
    signed_url = f"{url}?{params}"
    return SignedUrlResult(signed_url=signed_url, expires_at=expires_at, key_pair_id=key_pair_id)


# ---------------------------------------------------------------------------
# 13. WAF IP blocklist updater
# ---------------------------------------------------------------------------


async def waf_ip_blocklist_updater(
    ip_set_name: str,
    ip_set_id: str,
    scope: str,
    bucket: str,
    feed_key: str,
    table_name: str,
    region_name: str | None = None,
) -> WAFBlocklistResult:
    """Read IP CIDRs from S3 threat feed and update a WAFv2 IP set.

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

    s3 = async_client("s3", region_name)
    wafv2 = async_client("wafv2", region_name)
    ddb = async_client("dynamodb", region_name)

    try:
        obj = await s3.call("GetObject", Bucket=bucket, Key=feed_key)
        body = obj["Body"]
        content = body.read() if hasattr(body, "read") else body
        feed_cidrs = {c.strip() for c in content.decode().splitlines() if c.strip()}
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater s3 get_object failed") from exc

    try:
        ip_set_resp = await wafv2.call("GetIPSet", Name=ip_set_name, Scope=scope, Id=ip_set_id)
        current_addresses = set(ip_set_resp["IPSet"]["Addresses"])
        lock_token = ip_set_resp["LockToken"]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater get_ip_set failed") from exc

    added = len(feed_cidrs - current_addresses)
    removed = len(current_addresses - feed_cidrs)
    new_addresses = list(feed_cidrs)

    try:
        await wafv2.call(
            "UpdateIPSet",
            Name=ip_set_name,
            Scope=scope,
            Id=ip_set_id,
            Addresses=new_addresses,
            LockToken=lock_token,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater update_ip_set failed") from exc

    try:
        await ddb.call(
            "PutItem",
            TableName=table_name,
            Item={
                "pk": {"S": ip_set_id},
                "sk": {"S": str(int(time.time()))},
                "ips_added": {"N": str(added)},
                "ips_removed": {"N": str(removed)},
                "total_ips": {"N": str(len(new_addresses))},
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "waf_ip_blocklist_updater ddb put_item failed") from exc

    return WAFBlocklistResult(ips_added=added, ips_removed=removed, total_ips=len(new_addresses))


# ---------------------------------------------------------------------------
# 14. Shield Advanced protection manager
# ---------------------------------------------------------------------------


async def shield_advanced_protection_manager(
    resource_arns: list[str],
    emergency_contact_email: str | None = None,
    region_name: str | None = None,
) -> ShieldProtectionResult:
    """Attach Shield Advanced protections to specified resource ARNs.

    Args:
        resource_arns: List of resource ARNs to protect.
        emergency_contact_email: Optional email for DDoS Response Team contacts.
        region_name: AWS region override.

    Returns:
        A :class:`ShieldProtectionResult` with creation counts.

    Raises:
        RuntimeError: If Shield API calls fail unexpectedly.
    """
    shield = async_client("shield", region_name or "us-east-1")

    created = 0
    already = 0

    for arn in resource_arns:
        try:
            await shield.call("CreateProtection", Name=arn.split(":")[-1][:128], ResourceArn=arn)
            created += 1
        except RuntimeError as exc:
            err_str = str(exc)
            if "ResourceAlreadyExistsException" in err_str or "AlreadyExistsException" in err_str:
                already += 1
            else:
                raise wrap_aws_error(
                    exc, f"shield_advanced_protection_manager failed for {arn!r}"
                ) from exc

    emergency_contact_set = False
    if emergency_contact_email:
        try:
            await shield.call(
                "UpdateEmergencyContactSettings",
                EmergencyContactList=[{"EmailAddress": emergency_contact_email}],
            )
            emergency_contact_set = True
        except RuntimeError as exc:
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


async def acm_certificate_expiry_monitor(
    sns_topic_arn: str,
    days_threshold: int = 30,
    region_name: str | None = None,
) -> CertExpiryResult:
    """List ACM certificates expiring within N days and publish alerts to SNS.

    Args:
        sns_topic_arn: SNS topic ARN for alerts.
        days_threshold: Days before expiry to flag a certificate (default 30).
        region_name: AWS region override.

    Returns:
        A :class:`CertExpiryResult` with expiry counts and domains.

    Raises:
        RuntimeError: If ACM listing or SNS publish fails.
    """

    acm = async_client("acm", region_name)
    sns = async_client("sns", region_name)

    try:
        certs_resp = await acm.call("ListCertificates", CertificateStatuses=["ISSUED"])
        cert_list = certs_resp.get("CertificateSummaryList", [])
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, "acm_certificate_expiry_monitor list_certificates failed"
        ) from exc

    from datetime import datetime as _dt
    from datetime import timedelta as _td

    threshold_dt = _dt.now(tz=UTC) + _td(days=days_threshold)
    expiring_domains: list[str] = []

    for cert_summary in cert_list:
        arn = cert_summary["CertificateArn"]
        try:
            detail_resp = await acm.call("DescribeCertificate", CertificateArn=arn)
            detail = detail_resp.get("Certificate", {})
            not_after = detail.get("NotAfter")
            if not_after and not_after < threshold_dt:
                domain = detail.get("DomainName", arn)
                expiring_domains.append(domain)
        except RuntimeError:
            continue

    alert_sent = False
    if expiring_domains:
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject=f"ACM Certificates Expiring Within {days_threshold} Days",
                Message=(
                    f"Found {len(expiring_domains)} certificate(s) expiring soon:\n"
                    + "\n".join(expiring_domains)
                ),
            )
            alert_sent = True
        except RuntimeError as exc:
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


async def cognito_pre_token_enricher(
    user_pool_id: str,
    username: str,
    table_name: str,
    claim_attributes: list[str],
    region_name: str | None = None,
) -> TokenEnrichResult:
    """Read user attributes from DynamoDB and format as Cognito custom claims.

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
    cognito = async_client("cognito-idp", region_name)
    ddb = async_client("dynamodb", region_name)

    try:
        user_resp = await cognito.call("AdminGetUser", UserPoolId=user_pool_id, Username=username)
        base_attrs = {a["Name"]: a["Value"] for a in user_resp.get("UserAttributes", [])}
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"cognito_pre_token_enricher admin_get_user failed for {username!r}"
        ) from exc

    custom_attrs: dict[str, str] = {}
    try:
        item_resp = await ddb.call("GetItem", TableName=table_name, Key={"pk": {"S": username}})
        item = item_resp.get("Item", {})
        for attr in claim_attributes:
            val = item.get(attr, {})
            if val:
                custom_attrs[attr] = next(iter(val.values()))
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "cognito_pre_token_enricher ddb get_item failed") from exc

    claims = {**base_attrs, **custom_attrs}
    filtered_claims = {k: v for k, v in claims.items() if k in claim_attributes or k in base_attrs}

    return TokenEnrichResult(
        username=username,
        claims_added=len(custom_attrs),
        claims=filtered_claims,
    )
