# aws-util

[![PyPI version](https://badge.fury.io/py/aws-util.svg)](https://badge.fury.io/py/aws-util)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue?logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Masrik-Dahir/aws-util-python/blob/master/LICENSE)
[![CI](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/ci.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Masrik-Dahir/aws-util-python/branch/master/graph/badge.svg)](https://codecov.io/gh/Masrik-Dahir/aws-util-python)

> Production-grade Python wrappers for 100+ AWS services with typed Pydantic results, native async, and multi-service orchestration in a single call.

**[Full Documentation](https://www.masrikdahir.com/library/awsutil/python.html)** |
**[API Reference (all languages)](https://www.masrikdahir.com/library/awsutil.html)** |
**[GitHub](https://github.com/Masrik-Dahir/aws-util-python)** |
**[Changelog](https://github.com/Masrik-Dahir/aws-util-python/blob/master/CHANGELOG.md)**

---

## TL;DR

- **What:** A Python library that wraps every major AWS API surface (149 modules, 7,800+ methods) with typed Pydantic v2 return values and structured error handling.
- **Who:** Backend and DevOps engineers who use boto3 daily and want to stop writing the same try/except/parse boilerplate across projects.
- **Why:** Unlike raw boto3, every call returns a frozen Pydantic model instead of a raw dict -- no silent key typos, full IDE autocomplete, and multi-service orchestrations that combine 2-5 AWS calls into one function.
- **Start:** `pip install aws-util` then `from aws_util.s3 import upload_file` -- credentials come from your existing AWS config; no setup beyond that.
- **Know:** Requires Python 3.10+ and Pydantic v2; the async engine (`aws_util.aio.*`) mirrors every sync function but needs `aiohttp>=3.9`.

---

## Quick Start

### Install

```bash
pip install aws-util
```

### Single-service usage

```python
from aws_util.s3 import upload_file, download_bytes
from aws_util.sqs import send_message, receive_messages
from aws_util.dynamodb import get_item, put_item

# Upload a file to S3
result = upload_file("my-bucket", "data/report.csv", "/tmp/report.csv")
print(result.etag)

# Receive messages from SQS
msgs = receive_messages("https://sqs.us-east-1.amazonaws.com/123/my-queue", max_messages=5)
for msg in msgs:
    print(msg.body)
```

### Multi-service orchestration

```python
from aws_util.ci_cd_ops import codebuild_triggered_deploy
from aws_util.storage_ops import efs_to_s3_sync

# Trigger a CodeBuild build, wait for success, then deploy via CodeDeploy
result = codebuild_triggered_deploy(
    project_name="my-build-project",
    source_bucket="my-artifacts",
    source_key="builds/app.zip",
    application_name="my-app",
    deployment_group_name="prod-group",
)
print(result.build_status, result.deployment_status)
# CIDeployResult(build_id='...', build_status='SUCCEEDED', deployment_id='d-XXXX', deployment_status='Succeeded')
```

### Load application config

```python
from aws_util.config_loader import load_app_config

config = load_app_config(
    ssm_path="/myapp/prod/",
    secret_ids=["myapp/prod/db-credentials"],
    region_name="us-east-1",
)
# config.parameters: dict[str, str]   -- SSM values
# config.secrets: dict[str, Any]      -- Secrets Manager values
```

### Lambda middleware

```python
from aws_util.lambda_middleware import idempotent_handler

@idempotent_handler(table_name="idempotency-table")
def handler(event, context):
    # This function body runs at most once per unique event
    return process(event)
```

---

## Features

### Core Services

Individual wrappers for every major AWS service -- typed, tested, and ready to drop in:

| Category | Modules |
|---|---|
| Compute | `ec2`, `lambda_`, `ecs`, `eks`, `batch`, `elastic_beanstalk`, `app_runner`, `autoscaling` |
| Storage | `s3`, `efs`, `fsx`, `storage_gateway`, `lightsail`, `transfer`, `datasync` |
| Databases | `dynamodb`, `rds`, `rds_data`, `redshift`, `redshift_data`, `redshift_serverless`, `documentdb`, `neptune`, `neptune_graph`, `memorydb`, `elasticache`, `keyspaces`, `timestream_write`, `timestream_query` |
| Messaging | `sqs`, `sns`, `eventbridge`, `kinesis`, `firehose`, `msk`, `ivs` |
| AI / ML | `bedrock`, `bedrock_agent`, `rekognition`, `textract`, `comprehend`, `translate`, `polly`, `transcribe`, `forecast`, `personalize`, `sagemaker_runtime`, `lex_models`, `lex_runtime` |
| Security | `iam`, `kms`, `secrets_manager`, `cognito`, `acm`, `inspector`, `macie`, `detective`, `security_hub`, `sso_admin`, `access_analyzer` |
| Networking | `route53`, `cloudfront`, `elbv2`, `vpc_lattice`, `api_gateway`, `api_gateway_ops` |
| Developer Tools | `codebuild`, `codedeploy`, `codepipeline`, `codecommit`, `codeartifact` |
| Observability | `cloudwatch`, `cloudtrail`, `health`, `observability`, `config_service` |
| Governance | `organizations`, `service_quotas`, `cost_governance`, `cost_optimization` |
| Data & Analytics | `glue`, `athena`, `databrew`, `emr`, `emr_serverless`, `kinesis_analytics`, `quicksight`, `dms` |
| IoT | `iot`, `iot_data`, `iot_greengrass` |
| Serverless | `stepfunctions`, `parameter_store`, `config_loader`, `ses`, `ses_v2`, `connect`, `mediaconvert` |

### Multi-Service Orchestration Modules

Higher-order modules that combine multiple AWS services into end-to-end workflows:

| Module | What it does |
|---|---|
| `api_gateway_ops` | WebSocket sessions, JWT Lambda authorizers, usage plan enforcement, rate limiting, domain migration |
| `ci_cd_ops` | CodeBuild-triggered deploy, CodePipeline approval notifier, PR-to-CodeBuild, CodeArtifact package promotion |
| `storage_ops` | EFS-to-S3 DataSync, FSx backup archival, Transfer Family event processing, Storage Gateway monitoring |
| `security_ops` | Cognito group sync, CloudFront signed URLs, WAF IP blocklist, Shield protection, ACM certificate monitoring |
| `ai_ml_pipelines` | Rekognition face/video, Polly audio, Transcribe, Comprehend PII, Textract forms, Bedrock knowledge base |
| `deployment` | Lambda canary deploys, CloudFront invalidation, EKS node scaling, Step Functions tracking |
| `analytics_pipelines` | Redshift queries, QuickSight refresh, Athena-to-DynamoDB, Glue crawlers, EMR Serverless |
| `data_flow_etl` | MSK-to-S3 archival, Neptune graph backup, Keyspaces TTL enforcement |
| `cost_optimization` | Trusted Advisor reports, Cost & Usage analysis, idle EC2/RDS cleanup, Lambda dead code detection |
| `resilience` | Distributed lock manager (DynamoDB-based), Lambda destination routing |
| `iot_pipelines` | IoT telemetry to Timestream, device shadow sync, fleet command broadcast |

---

## Architecture

```
Caller
  -> aws_util.*  (sync)   -> get_client()    -> boto3 -> AWS
  -> aws_util.aio.* (async) -> async_client() -> boto3 -> AWS
                                                          |
                                           Response validated & packed
                                           into frozen Pydantic model
                                                          |
                                           ClientError caught & re-raised
                                           via wrap_aws_error()
```

Every public function follows this pattern:
1. Caller invokes a function from `aws_util.*` or `aws_util.aio.*`
2. The sync path calls `get_client(service, region)` which returns a boto3 client
3. The async path calls `async_client(service, region)` for non-blocking I/O
4. AWS response is validated and packed into a frozen Pydantic model
5. `ClientError` is caught and re-raised via `wrap_aws_error()` for consistent error handling

---

## Module Reference

### `ci_cd_ops` -- CI/CD Orchestration

```python
from aws_util.ci_cd_ops import (
    codebuild_triggered_deploy,
    codepipeline_approval_notifier,
    codecommit_pr_to_codebuild,
    codeartifact_package_promoter,
)
```

| Function | Services | Description |
|---|---|---|
| `codebuild_triggered_deploy` | CodeBuild, CodeDeploy | Start a build from S3, poll to completion, then create a deployment |
| `codepipeline_approval_notifier` | CodePipeline, SES v2, DynamoDB | Find pending approval actions, email approvers, persist tokens |
| `codecommit_pr_to_codebuild` | CodeCommit, CodeBuild | Trigger a build for a PR's source ref, post build status as a PR comment |
| `codeartifact_package_promoter` | CodeArtifact, SSM | Copy a package version between repositories, update an SSM version manifest |

### `storage_ops` -- Storage Orchestration

```python
from aws_util.storage_ops import (
    efs_to_s3_sync,
    fsx_backup_to_s3,
    transfer_family_event_processor,
    storage_gateway_cache_monitor,
    lightsail_snapshot_to_s3,
)
```

| Function | Services | Description |
|---|---|---|
| `efs_to_s3_sync` | DataSync, S3, DynamoDB | Create DataSync task to sync EFS to S3, log execution to DynamoDB |
| `fsx_backup_to_s3` | FSx, S3 | Initiate FSx backup, poll to AVAILABLE, write JSON metadata to S3 |
| `transfer_family_event_processor` | Transfer Family, SNS | Process new uploads: validate, version-copy, delete source, notify |
| `storage_gateway_cache_monitor` | Storage Gateway, CloudWatch | Measure cache utilisation; create CloudWatch alarm if above threshold |
| `lightsail_snapshot_to_s3` | Lightsail, S3 | Create Lightsail snapshot, wait for availability, export, archive metadata |

### Error Handling

All functions raise `aws_util.exceptions.AwsUtilError` (a subclass of `Exception`) on failure:

```python
from aws_util.exceptions import AwsUtilError
from aws_util.s3 import download_bytes

try:
    data = download_bytes("my-bucket", "missing-key.txt")
except AwsUtilError as exc:
    print(exc.service, exc.operation, exc.message)
```

---

## Async Usage

Every public sync function has an async counterpart in `aws_util.aio.*`:

```python
import asyncio
from aws_util.aio.ci_cd_ops import codebuild_triggered_deploy
from aws_util.aio.storage_ops import efs_to_s3_sync

async def main():
    # Run CI/CD deploy and EFS sync concurrently
    deploy_result, sync_result = await asyncio.gather(
        codebuild_triggered_deploy(
            project_name="my-build",
            source_bucket="artifacts",
            source_key="builds/app.zip",
            application_name="my-app",
            deployment_group_name="prod",
        ),
        efs_to_s3_sync(
            efs_filesystem_id="fs-abc123",
            source_subnet_arn="arn:aws:ec2:us-east-1:123:subnet/subnet-abc",
            source_security_group_arns=["arn:aws:ec2:us-east-1:123:security-group/sg-abc"],
            bucket="backups",
            key_prefix="efs",
            table_name="sync-log",
        ),
    )
    print(deploy_result.deployment_status)
    print(sync_result.task_arn)

asyncio.run(main())
```

---

## Configuration

`aws-util` uses boto3 under the hood and respects all standard AWS credential providers:

| Provider | How to configure |
|---|---|
| Environment variables | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` |
| AWS config file | `~/.aws/credentials` and `~/.aws/config` |
| IAM role (EC2/ECS/Lambda) | Automatic -- no configuration needed |
| STS assume role | Pass a pre-configured session to `get_client()` |

Every function accepts an optional `region_name` parameter:

```python
from aws_util.s3 import list_buckets

buckets = list_buckets(region_name="eu-west-1")
```

---

## Prerequisites

| Requirement | Minimum version | Notes |
|---|---|---|
| Python | 3.10 | 3.12 recommended |
| boto3 | latest | Pulled automatically |
| Pydantic | >= 2.0 | v2 required, v1 not supported |
| AWS credentials | -- | Any credential source boto3 supports |

---

## Documentation

| Resource | Link |
|----------|------|
| Full Documentation | [masrikdahir.com/.../python](https://www.masrikdahir.com/library/awsutil/python.html) |
| API Reference (all languages) | [masrikdahir.com/.../awsutil](https://www.masrikdahir.com/library/awsutil.html) |
| GitHub Repository | [github.com/Masrik-Dahir/aws-util-python](https://github.com/Masrik-Dahir/aws-util-python) |
| Changelog | [CHANGELOG.md](https://github.com/Masrik-Dahir/aws-util-python/blob/master/CHANGELOG.md) |

---

## Testing

```bash
pip install aws-util[dev]

# Run unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/unit/ -v --cov=src/aws_util --cov-report=term-missing

# Run integration tests (requires LocalStack)
pytest tests/integration/ -v -m integration
```

---

## License

[MIT](https://github.com/Masrik-Dahir/aws-util-python/blob/master/LICENSE) -- 2024 [Masrik Dahir](https://www.masrikdahir.com)
