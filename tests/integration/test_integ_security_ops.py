"""Integration tests for aws_util.security_ops against LocalStack."""
from __future__ import annotations

import json
import time

import boto3
import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import LOCALSTACK_URL, REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. audit_public_s3_buckets
# ---------------------------------------------------------------------------


class TestAuditPublicS3Buckets:
    def test_detects_public_bucket(self, s3_bucket, sns_topic):
        from aws_util.security_ops import audit_public_s3_buckets

        result = audit_public_s3_buckets(
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert result.total_scanned >= 1
        assert isinstance(result.public_buckets, list)

    def test_no_buckets(self):
        from aws_util.security_ops import audit_public_s3_buckets

        result = audit_public_s3_buckets(region_name=REGION)
        assert isinstance(result.total_scanned, int)
        assert isinstance(result.public_buckets, list)


# ---------------------------------------------------------------------------
# 2. rotate_iam_access_key
# ---------------------------------------------------------------------------


class TestRotateIamAccessKey:
    def test_rotate_and_store(self):
        from aws_util.security_ops import rotate_iam_access_key

        iam = ls_client("iam")
        sm = ls_client("secretsmanager")

        username = "test-rotate-user"
        try:
            iam.create_user(UserName=username)
        except ClientError:
            pass
        iam.create_access_key(UserName=username)

        result = rotate_iam_access_key(
            username=username,
            secret_name="test-rotated-key",
            region_name=REGION,
        )
        assert result.username == username
        assert result.new_access_key_id
        assert result.secret_name == "test-rotated-key"
        assert result.old_key_deactivated is True

        # Verify secret was stored
        secret = sm.get_secret_value(SecretId="test-rotated-key")
        stored = json.loads(secret["SecretString"])
        assert stored["access_key_id"] == result.new_access_key_id

        # Cleanup
        keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]
        for key in keys:
            iam.delete_access_key(UserName=username, AccessKeyId=key["AccessKeyId"])
        iam.delete_user(UserName=username)


# ---------------------------------------------------------------------------
# 3. kms_encrypt_to_secret
# ---------------------------------------------------------------------------


class TestKmsEncryptToSecret:
    def test_encrypt_and_store(self, kms_key):
        from aws_util.security_ops import kms_encrypt_to_secret

        # kms_encrypt_to_secret returns a str (the secret ARN)
        result = kms_encrypt_to_secret(
            plaintext="my-secret-data",
            kms_key_id=kms_key,
            secret_name="test-kms-secret",
            region_name=REGION,
        )
        assert isinstance(result, str)
        # Verify secret was stored
        sm = ls_client("secretsmanager")
        secret = sm.get_secret_value(SecretId="test-kms-secret")
        stored = json.loads(secret["SecretString"])
        assert "ciphertext" in stored
        assert stored["kms_key_id"] == kms_key


# ---------------------------------------------------------------------------
# 4. enforce_bucket_versioning
# ---------------------------------------------------------------------------


class TestEnforceBucketVersioning:
    def test_enables_versioning(self, s3_bucket):
        from aws_util.security_ops import enforce_bucket_versioning

        # Returns list[str] of bucket names where versioning was enabled
        result = enforce_bucket_versioning(
            bucket_names=[s3_bucket],
            region_name=REGION,
        )
        assert isinstance(result, list)
        assert len(result) >= 1
        assert s3_bucket in result

        # Verify versioning was enabled
        s3 = ls_client("s3")
        resp = s3.get_bucket_versioning(Bucket=s3_bucket)
        assert resp.get("Status") == "Enabled"


# ---------------------------------------------------------------------------
# 5. sync_secret_to_ssm
# ---------------------------------------------------------------------------


class TestSyncSecretToSsm:
    def test_sync(self):
        from aws_util.security_ops import sync_secret_to_ssm

        sm = ls_client("secretsmanager")
        # Handle ResourceExistsException — create or update the secret
        try:
            sm.create_secret(
                Name="test-sync-secret",
                SecretString=json.dumps({"db_host": "localhost", "db_port": "5432"}),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId="test-sync-secret",
                    SecretString=json.dumps({"db_host": "localhost", "db_port": "5432"}),
                )
            else:
                raise

        # sync_secret_to_ssm returns dict[str, str] mapping secret key -> SSM param name
        result = sync_secret_to_ssm(
            secret_id="test-sync-secret",
            ssm_path="/test/sync",
            region_name=REGION,
        )
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "db_host" in result
        assert "db_port" in result

        # Verify SSM parameters
        ssm = ls_client("ssm")
        param = ssm.get_parameter(Name="/test/sync/db_host", WithDecryption=True)
        assert param["Parameter"]["Value"] == "localhost"


# ---------------------------------------------------------------------------
# 6. create_cloudwatch_alarm_with_sns
# ---------------------------------------------------------------------------


class TestCreateCloudwatchAlarmWithSns:
    @pytest.mark.skip(reason="CloudWatch PutMetricAlarm returns 500 on LocalStack community")
    def test_create_alarm(self):
        from aws_util.security_ops import create_cloudwatch_alarm_with_sns

        # The function takes topic_name (str), not sns_topic_arn
        result = create_cloudwatch_alarm_with_sns(
            alarm_name="test-alarm",
            metric_name="CPUUtilization",
            namespace="AWS/EC2",
            threshold=80.0,
            comparison_operator="GreaterThanThreshold",
            period=300,
            evaluation_periods=1,
            topic_name="test-alarm-topic",
            region_name=REGION,
        )
        assert result.alarm_name == "test-alarm"
        assert result.topic_arn  # Should be a non-empty ARN string
        assert result.created is True


# ---------------------------------------------------------------------------
# 7. validate_and_store_cfn_template
# ---------------------------------------------------------------------------


class TestValidateAndStoreCfnTemplate:
    def test_upload_and_validate(self, s3_bucket):
        from aws_util.security_ops import validate_and_store_cfn_template

        # The function takes template (dict), s3_bucket (str), s3_key (str)
        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Test template",
            "Resources": {
                "MyBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {"BucketName": "test-cfn-bucket"},
                }
            },
        }

        result = validate_and_store_cfn_template(
            template=template,
            s3_bucket=s3_bucket,
            s3_key="templates/test.json",
            region_name=REGION,
        )
        assert result.valid is True
        assert result.s3_key == "templates/test.json"


# ---------------------------------------------------------------------------
# 8. iam_roles_report_to_s3
# ---------------------------------------------------------------------------


class TestIamRolesReportToS3:
    def test_generates_report(self, s3_bucket):
        from aws_util.security_ops import iam_roles_report_to_s3

        # Ensure at least one IAM role exists
        iam = ls_client("iam")
        role_name = f"test-report-role-{int(time.time())}"
        try:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}],
                }),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "EntityAlreadyExists":
                pass
            else:
                raise

        result = iam_roles_report_to_s3(
            s3_bucket=s3_bucket,
            s3_key="reports/iam-roles.json",
            region_name=REGION,
        )
        assert result == "reports/iam-roles.json"

        # Verify report was written to S3
        s3 = ls_client("s3")
        obj = s3.get_object(Bucket=s3_bucket, Key="reports/iam-roles.json")
        body = json.loads(obj["Body"].read().decode())
        assert "roles" in body
        assert "count" in body
        assert body["count"] >= 1


# ---------------------------------------------------------------------------
# 9. cognito_bulk_create_users
# ---------------------------------------------------------------------------


class TestCognitoBulkCreateUsers:
    @pytest.mark.skip(reason="Cognito IDP not available in LocalStack community")
    def test_creates_users(self):
        from aws_util.security_ops import cognito_bulk_create_users

        cognito = ls_client("cognito-idp")
        pool_resp = cognito.create_user_pool(PoolName=f"test-pool-{int(time.time())}")
        pool_id = pool_resp["UserPool"]["Id"]

        users = [
            {"username": "alice", "email": "alice@example.com"},
            {"username": "bob", "email": "bob@example.com"},
        ]

        try:
            results = cognito_bulk_create_users(
                user_pool_id=pool_id,
                users=users,
                region_name=REGION,
            )
            assert len(results) == 2
            assert results[0].username == "alice"
            assert results[1].username == "bob"
            for r in results:
                assert r.user_status  # Should have a status like FORCE_CHANGE_PASSWORD
        finally:
            # Cleanup
            try:
                cognito.delete_user_pool(UserPoolId=pool_id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 10. tag_ec2_instances_from_ssm
# ---------------------------------------------------------------------------


class TestTagEc2InstancesFromSsm:
    def test_tags_instances(self):
        from aws_util.security_ops import tag_ec2_instances_from_ssm

        ssm = ls_client("ssm")
        ec2 = ls_client("ec2")

        # Create SSM parameter with tag map
        tag_map = {"Environment": "test", "Project": "integ-test"}
        ssm.put_parameter(
            Name="/tags/ec2-tags",
            Value=json.dumps(tag_map),
            Type="String",
            Overwrite=True,
        )

        # Launch a micro instance
        run_resp = ec2.run_instances(
            ImageId="ami-00000000",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
        )
        instance_id = run_resp["Instances"][0]["InstanceId"]

        try:
            result = tag_ec2_instances_from_ssm(
                instance_ids=[instance_id],
                ssm_param_name="/tags/ec2-tags",
                region_name=REGION,
            )
            assert instance_id in result
            assert "Environment" in result[instance_id]
            assert "Project" in result[instance_id]

            # Verify tags were applied
            desc = ec2.describe_instances(InstanceIds=[instance_id])
            tags = desc["Reservations"][0]["Instances"][0].get("Tags", [])
            tag_keys = [t["Key"] for t in tags]
            assert "Environment" in tag_keys
            assert "Project" in tag_keys
        finally:
            try:
                ec2.terminate_instances(InstanceIds=[instance_id])
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 11. cognito_group_sync_to_dynamodb
# ---------------------------------------------------------------------------


class TestCognitoGroupSyncToDynamodb:
    @pytest.mark.skip(reason="Cognito IDP not available in LocalStack community")
    def test_syncs_groups(self, dynamodb_table):
        from aws_util.security_ops import cognito_group_sync_to_dynamodb

        cognito = ls_client("cognito-idp")
        pool_resp = cognito.create_user_pool(PoolName=f"test-sync-pool-{int(time.time())}")
        pool_id = pool_resp["UserPool"]["Id"]

        try:
            # Create a group
            cognito.create_group(GroupName="admins", UserPoolId=pool_id)

            # Create a user and add to group
            cognito.admin_create_user(
                UserPoolId=pool_id,
                Username="syncuser1",
                UserAttributes=[{"Name": "email", "Value": "syncuser1@example.com"}],
                MessageAction="SUPPRESS",
            )
            cognito.admin_add_user_to_group(
                UserPoolId=pool_id,
                Username="syncuser1",
                GroupName="admins",
            )

            result = cognito_group_sync_to_dynamodb(
                user_pool_id=pool_id,
                table_name=dynamodb_table,
                region_name=REGION,
            )
            assert result.groups_synced >= 1
            assert result.users_synced >= 1
            assert result.items_written >= 1
        finally:
            try:
                cognito.delete_user_pool(UserPoolId=pool_id)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 12. cloudfront_signed_url_factory
# ---------------------------------------------------------------------------


class TestCloudfrontSignedUrlFactory:
    @pytest.mark.skip(reason="CloudFront signing requires cryptography + not available in LocalStack community")
    def test_generates_signed_url(self):
        from aws_util.security_ops import cloudfront_signed_url_factory

        result = cloudfront_signed_url_factory(
            distribution_domain="d1234.cloudfront.net",
            object_path="/videos/clip.mp4",
            key_pair_id="KPID123",
            secret_name="cf-private-key",
            expiry_seconds=3600,
            region_name=REGION,
        )
        assert result.signed_url
        assert result.expires_at > 0
        assert result.key_pair_id == "KPID123"


# ---------------------------------------------------------------------------
# 13. waf_ip_blocklist_updater
# ---------------------------------------------------------------------------


class TestWafIpBlocklistUpdater:
    @pytest.mark.skip(reason="WAF not available in LocalStack community")
    def test_updates_blocklist(self, s3_bucket, dynamodb_table):
        from aws_util.security_ops import waf_ip_blocklist_updater

        result = waf_ip_blocklist_updater(
            ip_set_name="test-ip-set",
            ip_set_id="ipset-123",
            scope="REGIONAL",
            bucket=s3_bucket,
            feed_key="feeds/threat-ips.txt",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert isinstance(result.ips_added, int)
        assert isinstance(result.ips_removed, int)
        assert isinstance(result.total_ips, int)


# ---------------------------------------------------------------------------
# 14. shield_advanced_protection_manager
# ---------------------------------------------------------------------------


class TestShieldAdvancedProtectionManager:
    @pytest.mark.skip(reason="Shield not available in LocalStack community")
    def test_protects_resources(self):
        from aws_util.security_ops import shield_advanced_protection_manager

        result = shield_advanced_protection_manager(
            resource_arns=[
                "arn:aws:ec2:us-east-1:000000000000:eip-allocation/eipalloc-123",
            ],
            emergency_contact_email="security@example.com",
            region_name=REGION,
        )
        assert isinstance(result.protections_created, int)
        assert isinstance(result.already_protected, int)
        assert isinstance(result.emergency_contact_set, bool)


# ---------------------------------------------------------------------------
# 15. acm_certificate_expiry_monitor
# ---------------------------------------------------------------------------


class TestAcmCertificateExpiryMonitor:
    def test_monitors_certificates(self, sns_topic):
        from aws_util.security_ops import acm_certificate_expiry_monitor

        # ACM is available in LocalStack; there may be zero certs, that's fine.
        result = acm_certificate_expiry_monitor(
            sns_topic_arn=sns_topic,
            days_threshold=30,
            region_name=REGION,
        )
        assert isinstance(result.total_certs, int)
        assert isinstance(result.expiring_count, int)
        assert isinstance(result.expiring_domains, list)
        assert isinstance(result.alert_sent, bool)
        # With no certs, no alert should be sent
        if result.total_certs == 0:
            assert result.expiring_count == 0
            assert result.alert_sent is False


# ---------------------------------------------------------------------------
# 16. cognito_pre_token_enricher
# ---------------------------------------------------------------------------


class TestCognitoPreTokenEnricher:
    @pytest.mark.skip(reason="Cognito IDP not available in LocalStack community")
    def test_enriches_token(self, dynamodb_pk_table):
        from aws_util.security_ops import cognito_pre_token_enricher

        cognito = ls_client("cognito-idp")
        pool_resp = cognito.create_user_pool(PoolName=f"test-enrich-pool-{int(time.time())}")
        pool_id = pool_resp["UserPool"]["Id"]

        try:
            # Create a user
            cognito.admin_create_user(
                UserPoolId=pool_id,
                Username="enrichuser",
                UserAttributes=[
                    {"Name": "email", "Value": "enrichuser@example.com"},
                ],
                MessageAction="SUPPRESS",
            )

            # Put custom attributes in DynamoDB
            ddb = ls_client("dynamodb")
            ddb.put_item(
                TableName=dynamodb_pk_table,
                Item={
                    "pk": {"S": "enrichuser"},
                    "role": {"S": "admin"},
                    "tenant_id": {"S": "tenant-42"},
                },
            )

            result = cognito_pre_token_enricher(
                user_pool_id=pool_id,
                username="enrichuser",
                table_name=dynamodb_pk_table,
                claim_attributes=["role", "tenant_id"],
                region_name=REGION,
            )
            assert result.username == "enrichuser"
            assert result.claims_added >= 1
            assert isinstance(result.claims, dict)
            # Should include DynamoDB custom attrs
            assert result.claims.get("role") == "admin"
            assert result.claims.get("tenant_id") == "tenant-42"
        finally:
            try:
                cognito.delete_user_pool(UserPoolId=pool_id)
            except Exception:
                pass
