"""Shared fixtures for LocalStack integration tests.

These tests run against a real LocalStack instance (docker-compose.yml).
Start LocalStack before running:
    docker-compose up -d
    pytest tests/integration/ -v -m integration
"""
from __future__ import annotations

import os
import time

import boto3
import pytest
import requests

from aws_util._client import clear_client_cache

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LOCALSTACK_URL = os.environ.get("LOCALSTACK_URL", "http://localhost:4566")
REGION = "us-east-1"

# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------

def pytest_configure(config):
    config.addinivalue_line("markers", "integration: mark test as integration test (requires LocalStack)")


# ---------------------------------------------------------------------------
# Skip if LocalStack is not running
# ---------------------------------------------------------------------------

def _localstack_is_running() -> bool:
    try:
        resp = requests.get(f"{LOCALSTACK_URL}/_localstack/health", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


@pytest.fixture(autouse=True, scope="session")
def _require_localstack():
    if not _localstack_is_running():
        pytest.skip("LocalStack is not running — start with: docker-compose up -d")


# ---------------------------------------------------------------------------
# AWS environment pointing at LocalStack
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _aws_env(monkeypatch):
    """Point all AWS SDK calls at LocalStack."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", REGION)
    monkeypatch.setenv("AWS_ENDPOINT_URL", LOCALSTACK_URL)
    clear_client_cache()
    yield
    clear_client_cache()


# ---------------------------------------------------------------------------
# Client factory pointing at LocalStack
# ---------------------------------------------------------------------------

def ls_client(service: str, region: str = REGION):
    """Create a boto3 client pointing at LocalStack."""
    return boto3.client(
        service,
        region_name=region,
        endpoint_url=LOCALSTACK_URL,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


# ---------------------------------------------------------------------------
# Resource helpers — create and tear down AWS resources
# ---------------------------------------------------------------------------

@pytest.fixture
def s3_bucket():
    """Create a temporary S3 bucket in LocalStack."""
    client = ls_client("s3")
    name = f"test-bucket-{int(time.time())}"
    client.create_bucket(Bucket=name)
    yield name
    # cleanup
    try:
        objs = client.list_objects_v2(Bucket=name).get("Contents", [])
        if objs:
            client.delete_objects(
                Bucket=name,
                Delete={"Objects": [{"Key": o["Key"]} for o in objs]},
            )
        client.delete_bucket(Bucket=name)
    except Exception:
        pass


@pytest.fixture
def dynamodb_table():
    """Create a temporary DynamoDB table with pk/sk in LocalStack."""
    client = ls_client("dynamodb")
    name = f"test-table-{int(time.time())}"
    client.create_table(
        TableName=name,
        KeySchema=[
            {"AttributeName": "pk", "KeyType": "HASH"},
            {"AttributeName": "sk", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "pk", "AttributeType": "S"},
            {"AttributeName": "sk", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    client.get_waiter("table_exists").wait(TableName=name)
    yield name
    try:
        client.delete_table(TableName=name)
    except Exception:
        pass


@pytest.fixture
def dynamodb_pk_table():
    """Create a DynamoDB table with only pk (no sort key)."""
    client = ls_client("dynamodb")
    name = f"test-pk-table-{int(time.time())}"
    client.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    client.get_waiter("table_exists").wait(TableName=name)
    yield name
    try:
        client.delete_table(TableName=name)
    except Exception:
        pass


@pytest.fixture
def sns_topic():
    """Create a temporary SNS topic in LocalStack."""
    client = ls_client("sns")
    name = f"test-topic-{int(time.time())}"
    resp = client.create_topic(Name=name)
    arn = resp["TopicArn"]
    yield arn
    try:
        client.delete_topic(TopicArn=arn)
    except Exception:
        pass


@pytest.fixture
def sqs_queue():
    """Create a temporary SQS queue in LocalStack."""
    client = ls_client("sqs")
    name = f"test-queue-{int(time.time())}"
    resp = client.create_queue(QueueName=name)
    url = resp["QueueUrl"]
    yield url
    try:
        client.delete_queue(QueueUrl=url)
    except Exception:
        pass


@pytest.fixture
def ssm_client():
    """Return an SSM client pointing at LocalStack."""
    return ls_client("ssm")


@pytest.fixture
def secrets_client():
    """Return a Secrets Manager client pointing at LocalStack."""
    return ls_client("secretsmanager")


@pytest.fixture
def logs_group():
    """Create a CloudWatch Logs group in LocalStack."""
    client = ls_client("logs")
    name = f"/test/integration/{int(time.time())}"
    client.create_log_group(logGroupName=name)
    yield name
    try:
        client.delete_log_group(logGroupName=name)
    except Exception:
        pass


@pytest.fixture
def kms_key():
    """Create a KMS key in LocalStack."""
    client = ls_client("kms")
    resp = client.create_key(Description="integration-test")
    key_id = resp["KeyMetadata"]["KeyId"]
    yield key_id


@pytest.fixture
def iam_role():
    """Create a minimal IAM role in LocalStack."""
    import json
    client = ls_client("iam")
    name = f"test-role-{int(time.time())}"
    policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}],
    })
    resp = client.create_role(RoleName=name, AssumeRolePolicyDocument=policy)
    arn = resp["Role"]["Arn"]
    yield arn
    try:
        client.delete_role(RoleName=name)
    except Exception:
        pass
