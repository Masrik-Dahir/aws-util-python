# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.2.7] - 2026-04-09

### Changed
- Scoped CI workflows (`test.yml`, `coverage.yml`, `mutation.yml`) to run against the `s3` module only instead of the entire test suite
- Added `scripts/` to `.gitignore`

## [2.2.6] - 2026-04-08

### Added
- **6,189 new boto3 method wrappers** achieving 100% coverage of all boto3 client methods across all 103 service modules (7,303 total methods). Each method includes typed parameters, Pydantic result models, error handling via `wrap_aws_error`, and both sync/async implementations:
  - `bedrock.py` — 93 new Bedrock management API wrappers (guardrails, models, evaluation jobs, inference profiles, provisioned throughput, marketplace endpoints, automated reasoning policies)
  - `api_gateway.py` — 124 new API Gateway REST API management wrappers (REST APIs, stages, deployments, authorizers, models, usage plans, VPC links, documentation, gateway responses, SDK generation)
  - 5,972 additional wrappers across all remaining service modules
- Full async parity for all new methods in corresponding `aio/` modules
- Pydantic result models for every new method
- **7,682 new tests** for optional parameter branch coverage, bringing all modules to 100% line coverage
- Automated code generator (`scripts/inject_all.py`) for maintaining full API parity with boto3

### Fixed
- Renamed `schema` field to `model_schema` in 6 Pydantic result models (api_gateway, glue, forecast, cloudformation, iot, personalize) to avoid shadowing `BaseModel.schema`
- Added missing `state` field to `StaticIpResult` in lightsail
- Resolved mypy type errors in async deployment and config_state modules
- Duplicate `@patch` decorators in 8 test files (connect, detective, inspector, iot_data, iot_greengrass, macie, timestream_query, transfer)
- Hardcoded `__all__` assertion tests replaced with dynamic checks to accommodate API expansion
- Fixed EC2 generated test assertions (Pydantic model returns vs raw dicts, required positional args)

## [2.2.5] - 2026-04-07

### Added
- **71 new single-service AWS modules** (sync + async), each with Pydantic models, automatic pagination, `wait_for_*` polling helpers, and 100% test coverage:
  - **Compute & Containers:** `app_runner`, `autoscaling`, `batch`, `elastic_beanstalk`, `eks`, `emr`, `emr_containers`, `emr_serverless`, `lightsail`
  - **Database & Storage:** `documentdb`, `elasticache`, `memorydb`, `neptune`, `neptune_graph`, `rds_data`, `redshift`, `redshift_data`, `redshift_serverless`, `efs`, `fsx`, `storage_gateway`, `keyspaces`, `timestream_write`, `timestream_query`
  - **Networking & Content Delivery:** `cloudfront`, `elbv2`, `vpc_lattice`
  - **Security & Identity:** `access_analyzer`, `cognito_identity`, `detective`, `inspector`, `macie`, `security_hub`, `sso_admin`
  - **Management & Governance:** `cloudtrail`, `config_service`, `health`, `organizations`, `service_quotas`
  - **Developer Tools:** `codebuild`, `codecommit`, `codedeploy`, `codepipeline`, `codeartifact`, `codestar_connections`
  - **AI/ML:** `bedrock_agent`, `bedrock_agent_runtime`, `personalize`, `personalize_runtime`, `polly`, `sagemaker_featurestore_runtime`, `sagemaker_runtime`, `transcribe`, `forecast`, `forecast_query`
  - **Analytics:** `kinesis_analytics`, `quicksight`, `databrew`, `msk`
  - **IoT:** `iot`, `iot_data`, `iot_greengrass`, `iot_sitewise`
  - **Media & Communication:** `connect`, `ivs`, `mediaconvert`, `lex_models`, `lex_runtime`
  - **Migration & Transfer:** `dms`, `transfer`
  - **Messaging:** `ses_v2`
- Total module count: **135 modules** covering **100+ AWS services**.

### Fixed
- `deployment.lambda_package_builder` now uses `sys.executable -m pip` instead of bare `pip` for portable pip invocation across platforms.

## [2.0.0] - 2026-03-31

### Added
- **Structured exception hierarchy** (`aws_util.exceptions`) — `AwsUtilError`, `AwsServiceError`, `AwsThrottlingError`, `AwsNotFoundError`, `AwsPermissionError`, `AwsConflictError`, `AwsValidationError`, `AwsTimeoutError`. All extend `RuntimeError` for backward compatibility.
- `wrap_aws_error()` and `classify_aws_error()` for automatic error classification from botocore `ClientError` codes.
- **Native async engine** (`aws_util.aio._engine`) — true non-blocking I/O via aiohttp with connection pooling, circuit breaking, and adaptive retry.
- **64 modules** covering 32+ AWS services with async counterparts in `aws_util.aio`.
- Multi-service orchestration modules: `blue_green`, `cross_account`, `data_lake`, `event_patterns`, `database_migration`, `credential_rotation`, `disaster_recovery`, `cost_governance`, `security_automation`, `container_ops`, `ml_pipeline`, `networking`.
- PEP 561 `py.typed` marker for type checker support.
- TTL-aware client cache (15-minute default) replacing unbounded `lru_cache` — fixes credential rotation in long-running processes.
- `__all__` exports on all sync service modules.

### Changed
- All AWS API errors now raise specific `AwsUtilError` subclasses instead of generic `RuntimeError`. Callers using `except RuntimeError` are unaffected (backward compatible).
- Client factory (`get_client`) now uses a bounded TTL cache (64 entries, 15-minute TTL) instead of unbounded `lru_cache`.
- Expanded ruff lint rules: added `B` (bugbear), `UP` (pyupgrade), `SIM` (simplify), `RUF` (ruff-specific).

### Removed
- `_async_wrap.py` — the thread-pool-based async wrapper is superseded by the native async engine.

### Fixed
- `invoke_with_retry` now correctly skips retry on function-level errors (matching its documented behavior).
- `drain_queue` now logs handler exceptions instead of silently swallowing them.
- `publish_fan_out` caps thread pool size and reports per-topic failures.
- `create_topic_if_not_exists` enforces `FifoTopic: "true"` when `fifo=True` regardless of caller-provided attributes.
- `replay_dlq` now forwards message attributes when replaying messages.
- Race condition in async engine global transport/credential initialization.
- `sync_folder` ETag comparison handles multipart-uploaded objects.
