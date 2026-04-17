"""Integration tests for aws_util.resource_ops against LocalStack."""
from __future__ import annotations

import json
import time

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. reprocess_sqs_dlq
# ---------------------------------------------------------------------------


class TestReprocessSqsDlq:
    def test_moves_messages(self, sqs_queue):
        from aws_util.resource_ops import reprocess_sqs_dlq

        sqs = ls_client("sqs")
        # Create a DLQ
        dlq_resp = sqs.create_queue(QueueName="test-dlq")
        dlq_url = dlq_resp["QueueUrl"]

        # Put messages in DLQ
        for i in range(3):
            sqs.send_message(QueueUrl=dlq_url, MessageBody=json.dumps({"idx": i}))

        result = reprocess_sqs_dlq(
            dlq_url=dlq_url,
            target_queue_url=sqs_queue,
            max_messages=10,
            region_name=REGION,
        )
        assert result.total_read >= 1
        assert result.reprocessed >= 1


# ---------------------------------------------------------------------------
# 2. backup_dynamodb_to_s3
# ---------------------------------------------------------------------------


class TestBackupDynamodbToS3:
    def test_exports_items(self, dynamodb_pk_table, s3_bucket):
        from aws_util.resource_ops import backup_dynamodb_to_s3

        ddb = ls_client("dynamodb")
        for i in range(5):
            ddb.put_item(
                TableName=dynamodb_pk_table,
                Item={"pk": {"S": f"item-{i}"}, "data": {"S": f"value-{i}"}},
            )

        # backup_dynamodb_to_s3 returns str (the S3 key)
        s3_key = "backups/table.jsonl"
        result = backup_dynamodb_to_s3(
            table_name=dynamodb_pk_table,
            s3_bucket=s3_bucket,
            s3_key=s3_key,
            region_name=REGION,
        )
        assert isinstance(result, str)
        assert result == s3_key

        # Verify file exists in S3
        s3 = ls_client("s3")
        obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        body = obj["Body"].read().decode()
        lines = [line for line in body.strip().splitlines() if line]
        assert len(lines) >= 5


# ---------------------------------------------------------------------------
# 3. sync_ssm_params_to_lambda_env
# ---------------------------------------------------------------------------


class TestSyncSsmParamsToLambdaEnv:
    def test_syncs_params(self, iam_role):
        from aws_util.resource_ops import sync_ssm_params_to_lambda_env
        import io
        import zipfile

        ssm = ls_client("ssm")
        ssm.put_parameter(Name="/sync/DB_HOST", Value="db.local", Type="String", Overwrite=True)
        ssm.put_parameter(Name="/sync/DB_PORT", Value="5432", Type="String", Overwrite=True)

        # Create lambda function
        lam = ls_client("lambda")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(event, context): return event")

        try:
            lam.create_function(
                FunctionName="test-sync-fn",
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceConflictException":
                pass  # Function already exists
            else:
                raise

        # sync_ssm_params_to_lambda_env returns dict[str, str] (env var mapping)
        result = sync_ssm_params_to_lambda_env(
            function_name="test-sync-fn",
            ssm_path="/sync/",
            region_name=REGION,
        )
        assert isinstance(result, dict)
        assert "DB_HOST" in result
        assert "DB_PORT" in result


# ---------------------------------------------------------------------------
# 4. s3_inventory_to_dynamodb
# ---------------------------------------------------------------------------


class TestS3InventoryToDynamodb:
    def test_inventories_bucket(self, s3_bucket, dynamodb_pk_table):
        from aws_util.resource_ops import s3_inventory_to_dynamodb

        s3 = ls_client("s3")
        for i in range(3):
            s3.put_object(Bucket=s3_bucket, Key=f"data/file-{i}.txt", Body=f"content-{i}")

        result = s3_inventory_to_dynamodb(
            bucket_name=s3_bucket,
            prefix="data/",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert result.bucket == s3_bucket
        assert result.items_written >= 3
        assert result.prefix == "data/"


# ---------------------------------------------------------------------------
# 5. publish_s3_keys_to_sqs
# ---------------------------------------------------------------------------


class TestPublishS3KeysToSqs:
    def test_publishes_keys(self, s3_bucket, sqs_queue):
        from aws_util.resource_ops import publish_s3_keys_to_sqs

        s3 = ls_client("s3")
        for i in range(3):
            s3.put_object(Bucket=s3_bucket, Key=f"events/item-{i}.json", Body="{}")

        # publish_s3_keys_to_sqs returns int (total messages sent)
        result = publish_s3_keys_to_sqs(
            bucket_name=s3_bucket,
            prefix="events/",
            queue_url=sqs_queue,
            region_name=REGION,
        )
        assert isinstance(result, int)
        assert result >= 3

        # Verify messages were sent to SQS
        sqs = ls_client("sqs")
        msgs = sqs.receive_message(QueueUrl=sqs_queue, MaxNumberOfMessages=10)
        assert len(msgs.get("Messages", [])) >= 1


# ---------------------------------------------------------------------------
# 6. delete_stale_ecr_images
# ---------------------------------------------------------------------------


class TestDeleteStaleEcrImages:
    @pytest.mark.skip(reason="ECR image push not straightforward in LocalStack community")
    def test_deletes_stale_images(self, sns_topic):
        from aws_util.resource_ops import delete_stale_ecr_images

        ecr = ls_client("ecr")
        repo_name = f"test-ecr-repo-{int(time.time())}"
        try:
            ecr.create_repository(repositoryName=repo_name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "RepositoryAlreadyExistsException":
                pass
            else:
                raise

        # delete_stale_ecr_images returns list[str] of deleted image digests
        result = delete_stale_ecr_images(
            repository_name=repo_name,
            keep_count=5,
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# 7. rebuild_athena_partitions
# ---------------------------------------------------------------------------


class TestRebuildAthenaPartitions:
    @pytest.mark.skip(reason="Athena not available in LocalStack community")
    def test_rebuilds_partitions(self):
        from aws_util.resource_ops import rebuild_athena_partitions

        result = rebuild_athena_partitions(
            database="test_db",
            table="test_table",
            output_location="s3://test-bucket/athena/",
            region_name=REGION,
        )
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# 8. cross_account_s3_copy
# ---------------------------------------------------------------------------


class TestCrossAccountS3Copy:
    def test_copies_object(self, s3_bucket, iam_role):
        from aws_util.resource_ops import cross_account_s3_copy

        s3 = ls_client("s3")
        # Put source object
        s3.put_object(Bucket=s3_bucket, Key="source/data.txt", Body=b"hello cross-account")

        # Create a destination bucket
        import time as _time

        dest_bucket = f"dest-bucket-{int(_time.time())}"
        s3.create_bucket(Bucket=dest_bucket)

        try:
            result = cross_account_s3_copy(
                role_arn=iam_role,
                source_bucket=s3_bucket,
                source_key="source/data.txt",
                dest_bucket=dest_bucket,
                dest_key="dest/data.txt",
                region_name=REGION,
            )
            assert result == "dest/data.txt"

            # Verify the object was copied
            obj = s3.get_object(Bucket=dest_bucket, Key="dest/data.txt")
            body = obj["Body"].read()
            assert body == b"hello cross-account"
        finally:
            # Cleanup destination bucket
            try:
                objs = s3.list_objects_v2(Bucket=dest_bucket).get("Contents", [])
                if objs:
                    s3.delete_objects(
                        Bucket=dest_bucket,
                        Delete={"Objects": [{"Key": o["Key"]} for o in objs]},
                    )
                s3.delete_bucket(Bucket=dest_bucket)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 9. rotate_secret_and_notify
# ---------------------------------------------------------------------------


class TestRotateSecretAndNotify:
    @pytest.mark.skip(reason="RotateSecret requires a Lambda rotation function ARN in LocalStack community")
    def test_rotates_and_notifies(self, sns_topic):
        from aws_util.resource_ops import rotate_secret_and_notify

        sm = ls_client("secretsmanager")
        secret_name = f"test-rotate-secret-{int(time.time())}"
        try:
            sm.create_secret(
                Name=secret_name,
                SecretString=json.dumps({"user": "admin", "pass": "secret123"}),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId=secret_name,
                    SecretString=json.dumps({"user": "admin", "pass": "secret123"}),
                )
            else:
                raise

        result = rotate_secret_and_notify(
            secret_id=secret_name,
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert result.secret_id == secret_name
        assert result.rotation_enabled is True
        assert result.message_id is not None


# ---------------------------------------------------------------------------
# 10. lambda_invoke_with_secret
# ---------------------------------------------------------------------------


class TestLambdaInvokeWithSecret:
    @pytest.mark.skip(reason="Lambda invoke times out in LocalStack community due to Pending state")
    def test_invokes_with_secret(self, iam_role):
        from aws_util.resource_ops import lambda_invoke_with_secret

        import io
        import zipfile

        sm = ls_client("secretsmanager")
        secret_name = f"test-invoke-secret-{int(time.time())}"
        try:
            sm.create_secret(
                Name=secret_name,
                SecretString=json.dumps({"api_key": "abc123"}),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId=secret_name,
                    SecretString=json.dumps({"api_key": "abc123"}),
                )
            else:
                raise

        # Create a simple Lambda function that echoes its event
        lam = ls_client("lambda")
        fn_name = f"invoke-secret-fn-{int(time.time())}"
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(event, context): return event")

        try:
            lam.create_function(
                FunctionName=fn_name,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceConflictException":
                pass
            else:
                raise

        # Wait for the function to become Active before invoking
        lam.get_waiter("function_active_v2").wait(FunctionName=fn_name)

        result = lambda_invoke_with_secret(
            function_name=fn_name,
            secret_id=secret_name,
            region_name=REGION,
        )
        assert isinstance(result, dict)
        assert "status_code" in result
        assert result["status_code"] == 200
        assert "payload" in result


# ---------------------------------------------------------------------------
# 11. ses_suppression_list_manager
# ---------------------------------------------------------------------------


class TestSesSuppressionListManager:
    @pytest.mark.skip(reason="SESv2 suppression list API not available in LocalStack community")
    def test_syncs_suppression_list(self, s3_bucket, dynamodb_pk_table):
        from aws_util.resource_ops import ses_suppression_list_manager

        s3 = ls_client("s3")
        # Upload a blocklist file
        blocklist = ["spam@example.com", "blocked@example.com"]
        s3.put_object(
            Bucket=s3_bucket,
            Key="blocklist.json",
            Body=json.dumps(blocklist),
        )

        result = ses_suppression_list_manager(
            bucket=s3_bucket,
            blocklist_key="blocklist.json",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert isinstance(result.current_count, int)
        assert isinstance(result.added, int)
        assert isinstance(result.removed, int)
        assert isinstance(result.s3_synced, bool)
