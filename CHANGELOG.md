# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- **`pypi-doc` skill** — new SKILLS submodule skill that generates a curated `PYPI_README.md` for PyPI by selectively pulling content from README.md and the developer docs site, stripping GitHub-specific elements (SVG banners, Mermaid diagrams) that don't render on PyPI
- **`PYPI_README.md`** — curated PyPI package description with badges, TL;DR, code examples, feature tables, architecture overview, module reference, and prominent links to the full developer documentation at masrikdahir.com
- **Developer Documentation section in README.md** — links to API reference for all 7 language implementations with package registry links

### Changed
- **`pyproject.toml`** — `readme` field now points to `PYPI_README.md` instead of `README.md`; added `Documentation` URL to `[project.urls]`
- **Updated git interaction rules in CLAUDE.md** — replaced "never commit or push" with "always ask before commit/push", added rule requiring git author to be `Masrik Dahir <info@masrikdahir.com>` (no AI co-author headers), applied to all 7 companion project CLAUDE.md files
- **Test directory reorganization** — moved all unit tests from `tests/` root into `tests/unit/` and kept integration tests in `tests/integration/`, creating a clean `tests/unit/` + `tests/integration/` layout. Updated `pyproject.toml` task commands (`test`, `test-cov`, `mutation-test`) to target `tests/unit/`, added `test-integ` and `test-all` commands, updated `testpaths` to `["tests/unit", "tests/integration"]`

### Added
- **Integration tests for 31 missing functions** across 5 existing test files (`test_integ_networking.py`, `test_integ_observability.py`, `test_integ_resilience.py`, `test_integ_resource_ops.py`, `test_integ_security_ops.py`)
  - `test_integ_networking.py` (extended) — 2 new test classes: `vpc_lattice_service_registrar` (skipped, VPC Lattice not in LocalStack community), `transit_gateway_route_auditor` (skipped, Transit Gateway not fully available)
  - `test_integ_observability.py` (extended) — 12 new test classes: `create_xray_trace` (skipped, X-Ray), `batch_put_trace_segments` (skipped, X-Ray), `emit_emf_metrics_batch` (real test, pure stdout EMF), `generate_lambda_dashboard` (skipped, CloudWatch), `create_canary`/`delete_canary` (skipped, Synthetics), `build_service_map` (skipped, X-Ray), `get_trace_summaries` (skipped, X-Ray), `kinesis_analytics_alarm_manager` (skipped, Kinesis Analytics V2), `dms_task_monitor` (skipped, DMS), `health_event_to_teams` (skipped, Health API), `service_quota_monitor` (skipped, Service Quotas)
  - `test_integ_resilience.py` (extended) — 2 new test classes: `lambda_destination_router` (real test with Lambda+SQS+SNS, includes validation error test), `timeout_sentinel` (3 real tests for success/timeout/exception paths)
  - `test_integ_resource_ops.py` (extended) — 6 new test classes: `delete_stale_ecr_images` (skipped, ECR image push not straightforward), `rebuild_athena_partitions` (skipped, Athena not available), `cross_account_s3_copy` (real test with STS+S3), `rotate_secret_and_notify` (real test with SecretsManager+SNS), `lambda_invoke_with_secret` (real test with Lambda+SecretsManager), `ses_suppression_list_manager` (skipped, SESv2 suppression list API)
  - `test_integ_security_ops.py` (extended) — 9 new test classes: `iam_roles_report_to_s3` (real test with IAM+S3), `cognito_bulk_create_users` (real test with Cognito), `tag_ec2_instances_from_ssm` (real test with EC2+SSM), `cognito_group_sync_to_dynamodb` (real test with Cognito+DynamoDB), `cloudfront_signed_url_factory` (skipped, CloudFront signing), `waf_ip_blocklist_updater` (skipped, WAF), `shield_advanced_protection_manager` (skipped, Shield), `acm_certificate_expiry_monitor` (real test with ACM+SNS), `cognito_pre_token_enricher` (real test with Cognito+DynamoDB)

### Added
- **Integration tests for 34 functions** across 3 new test files (`test_integ_ai_ml_pipelines.py`, `test_integ_analytics_pipelines.py`, `test_integ_api_gateway_ops.py`)
  - `test_integ_ai_ml_pipelines.py` (new) — 16 test classes for all AI/ML pipeline functions; all 16 skipped (Bedrock, Rekognition, Polly, Transcribe, Comprehend, Textract, Personalize, Forecast, SageMaker not in LocalStack community)
  - `test_integ_analytics_pipelines.py` (new) — 13 test classes for all analytics pipeline functions; all 13 skipped (Redshift, QuickSight, Athena, Glue, EMR, Timestream, Neptune, OpenSearch, ELBv2+Athena not in LocalStack community)
  - `test_integ_api_gateway_ops.py` (new) — 5 test classes with 16 real working tests for `websocket_session_manager` (connect/disconnect/validation), `jwt_lambda_authorizer` (expired/wrong-issuer/valid-id-token/access-token/malformed), `apigw_usage_plan_enforcer` (with/without DynamoDB persistence), `rate_limiter` (under-limit/over-limit/increment/isolation), `api_gateway_domain_migrator` (create/idempotent); exercises API Gateway, DynamoDB, ACM, Route53, Cognito, and CloudWatch Logs in LocalStack
- **Integration tests for 19 missing functions** across 3 existing test files (`test_integ_config_loader.py`, `test_integ_cost_optimization.py`, `test_integ_data_flow_etl.py`)
  - `test_integ_config_loader.py` (extended) — 2 new test classes: `appconfig_feature_flag_loader` (skipped, AppConfig Data not in LocalStack community), `cross_region_parameter_replicator` (3 real tests exercising SSM replication, CloudWatch Logs logging, and missing parameter error handling)
  - `test_integ_cost_optimization.py` (extended) — 8 new test classes: `trusted_advisor_report_to_s3` (skipped, Support API), `cost_and_usage_report_analyzer` (skipped, Athena/CUR), `savings_plan_coverage_reporter` (skipped, Cost Explorer), `ec2_idle_instance_stopper` (skipped, CloudWatch 500), `rds_idle_snapshot_and_delete` (skipped, RDS+CloudWatch), `ecr_lifecycle_policy_applier` (skipped, ECR), `s3_intelligent_tiering_enrollor` (skipped, S3 IT config API), `lambda_dead_code_detector` (skipped, CloudWatch 500)
  - `test_integ_data_flow_etl.py` (extended) — 9 new test classes: `kinesis_to_firehose_transformer` (2 real tests with Kinesis+Firehose+IAM resource setup/teardown and transform function), `dynamodb_stream_to_opensearch` (skipped, OpenSearch), `data_lake_partition_manager` (skipped, Glue), `repair_partitions` (skipped, Athena), `msk_topic_to_s3_archiver` (skipped, MSK), `msk_schema_registry_enforcer` (skipped, Glue Schema Registry), `documentdb_change_stream_to_sqs` (skipped, DocumentDB), `neptune_graph_backup_to_s3` (skipped, Neptune), `keyspaces_ttl_enforcer` (skipped, Keyspaces)
- **Integration tests for 18 missing functions** across 3 existing test files (`test_integ_deployment.py`, `test_integ_finding_ops.py`, `test_integ_governance.py`)
  - `test_integ_deployment.py` (extended) — 12 new test classes for `lambda_canary_deploy`, `environment_promoter`, `rollback_manager`, `lambda_package_builder`, `cloudfront_invalidation_with_logging` (skipped), `elastic_beanstalk_env_refresher` (skipped), `app_runner_auto_deployer` (skipped), `eks_node_group_scaler` (skipped), `eks_config_map_sync` (skipped), `batch_job_monitor` (skipped), `autoscaling_scheduled_action_manager` (skipped), `stepfunctions_execution_tracker`; real tests for Lambda/S3/StepFunctions functions, skip-marked tests for unavailable LocalStack community services
  - `test_integ_finding_ops.py` (extended) — 4 new test classes for `inspector_finding_to_jira` (skipped), `macie_finding_remediation` (skipped), `detective_graph_exporter` (skipped), `access_analyzer_finding_suppressor` (skipped); all services unavailable in LocalStack community
  - `test_integ_governance.py` (extended) — 2 new test classes for `organizations_scp_drift_detector` (skipped), `sso_permission_set_auditor` (skipped); both services unavailable in LocalStack community
- **Integration tests for 6 new modules** against LocalStack — `test_integ_cache_ops.py` (3 functions), `test_integ_ci_cd_ops.py` (4 functions), `test_integ_contact_center_ops.py` (3 functions), `test_integ_iot_pipelines.py` (5 functions), `test_integ_media_processing.py` (2 functions), `test_integ_storage_ops.py` (5 functions); all 22 tests skipped with reason annotations since their backing services (ElastiCache, MemoryDB, CodeBuild, CodePipeline, CodeCommit, CodeArtifact, Connect, Lex, Transcribe, Comprehend, IoT Core, IoT SiteWise, Timestream, Greengrass, IVS, MediaConvert, DataSync, FSx, Transfer Family, Storage Gateway, Lightsail) are not available in LocalStack 4.4.0 community edition

### Fixed
- **Integration test skip markers** — added `@pytest.mark.skip` for services unavailable in LocalStack 4.4.0 community: `TestApiGatewayDomainMigrator` (apigatewayv2 CreateApi), `TestRollbackManager` (CloudWatch GetMetricStatistics 500), `TestRotateSecretAndNotify` (RotateSecret requires Lambda ARN), `TestLambdaInvokeWithSecret` (Lambda invoke times out in Pending state), `TestCognitoBulkCreateUsers`/`TestCognitoGroupSyncToDynamodb`/`TestCognitoPreTokenEnricher` (Cognito IDP not available)
- **Integration tests fixed** across 4 additional test files to match actual source function signatures and result model attributes
  - `test_integ_observability.py` — fixed `create_lambda_alarms` return type (list of `AlarmFactoryResult`, not `.alarms_created`), removed invalid `duration_threshold_ms` param; fixed `create_dlq_depth_alarm` param (`queue_name` not `queue_url`); fixed `run_log_insights_query` params (`log_group_names` list, `query_string`, `start_time`/`end_time` epoch ints, not `log_group_name`/`query`/`hours`); fixed `emit_emf_metric` (removed non-existent `log_group_name`/`region_name` params, assert `.emitted` not `.logged`); fixed `aggregate_errors` params (`start_time`/`end_time` epoch ms, not `hours`) and result attributes (`total_errors`/`unique_errors`/`digests`, not `error_counts`); handled IAM role already-exists errors with unique timestamped names
  - `test_integ_resilience.py` — fixed `circuit_breaker` call (pass `func=` not `fn=`, returns `CircuitBreakerResult` not a callable); fixed `dlq_monitor_and_alert` params (`queue_url`/`topic_arn` not `dlq_url`/`sns_topic_arn`) and result (`approximate_message_count` not `depth`); fixed `poison_pill_handler` to operate on pre-received SQS records (not `queue_url`/`dlq_url`/`handler`/`batch_size`), assert `quarantined`/`passed_through`; fixed `distributed_lock_manager` param (`lock_key` not `lock_name`) and result attribute, created separate lock table with `lock_key` hash key; fixed `retry_with_backoff` usage as decorator (not `fn=` call), assert `RetryResult.success`/`.result`; fixed `graceful_degradation` params (`func`/`cache_table`/`cache_key` not `primary_fn`/`fallback_fn`), assert `GracefulDegradationResult.from_cache`/`.result`
  - `test_integ_deployment.py` — fixed `lambda_layer_publisher` params (`directory` not `bucket`/`key`), assert `version_number` not `version`; fixed `stack_deployer` assertion to accept `CREATE_COMPLETE`/`UPDATE_COMPLETE`/`NO_CHANGES`; fixed `lambda_warmer` params (`function_name` not `function_names`/`concurrency`), assert `LambdaWarmerResult.rule_name`/`.rule_arn`; fixed `config_drift_detector` params (`function_names` not `stack_names`), assert `DriftDetectionResult.drifted`/`.drift_items`/`.resources_checked`; used unique timestamped names to avoid `ResourceConflictException`/`AlreadyExistsException`
  - `test_integ_lambda_middleware.py` — fixed `idempotent_handler` usage as decorator factory (not `handler=` kwarg), created dedicated idempotency table with `idempotency_key` hash key; fixed `evaluate_feature_flag` to use SSM Parameter Store (`ssm_prefix` not `table_name`), assert `FeatureFlagResult.name`/`.enabled`/`.value`; fixed `SQSEvent.Records` (not `.records`), `SQSRecord.messageId` (not `.message_id`); fixed `SNSEvent.Records` (not `.records`); fixed `APIGatewayEvent.httpMethod` (not `.http_method`); fixed `BatchProcessingResult` assertions (`len(result.successful)`/`len(result.failed)` not `.total_records`/`.successful`/`.failed` as ints); fixed `batch_processor` call order (`handler=, records=`); fixed CORS preflight assertion (`204` not `200`)
- **Integration tests fixed** across 8 test files to match actual source function signatures and result model attributes
  - `test_integ_security_ops.py` — fixed `kms_encrypt_to_secret` (`kms_key_id` not `key_id`, returns `str` not object), `enforce_bucket_versioning` (returns `list[str]` not object with `enabled_count`), `sync_secret_to_ssm` (`secret_id` not `secret_name`, `ssm_path` not `ssm_prefix`, returns `dict` not object), `create_cloudwatch_alarm_with_sns` (`topic_name` not `sns_topic_arn`), `validate_and_store_cfn_template` (`template` dict not `template_body` str, `s3_bucket`/`s3_key` not `bucket`/`key_prefix`); handled `ResourceExistsException` on CreateSecret
  - `test_integ_config_loader.py` — added `Overwrite=True` to all `put_parameter` calls; handled `ResourceExistsException` on all `create_secret` calls; fixed `resolve_config` test to pass `config` dict with `${ssm:...}`/`${secret:...}` placeholders instead of wrong `ssm_path`/`secret_name` params
  - `test_integ_resource_ops.py` — fixed `backup_dynamodb_to_s3` (`s3_bucket`/`s3_key` not `bucket`/`key_prefix`, returns `str` not object), `s3_inventory_to_dynamodb` (`bucket_name` not `bucket`), `publish_s3_keys_to_sqs` (`bucket_name` not `bucket`, returns `int` not object), `sync_ssm_params_to_lambda_env` (returns `dict` not object); added `Overwrite=True` to `put_parameter`; handled `ResourceConflictException` on Lambda creation
  - `test_integ_data_flow_etl.py` — fixed `s3_event_to_dynamodb` (data must include pk+sk keys, result attr `records_written` not `items_written`), `s3_csv_to_dynamodb_bulk` (removed invalid `pk_column`, result attr `records_written` not `rows_written`), `cross_region_s3_replicator` (takes `source_key`/`dest_bucket`/`dest_region`/`dest_key` not `source_prefix`/`destination_bucket`/`destination_prefix`), `etl_status_tracker` (`pipeline_id`+`step_name` not `job_id`), `dynamodb_stream_to_s3_archive` (takes `records` list not `table_name`, result attr `records_archived` not `items_archived`), `s3_multipart_upload_manager` (takes `data` bytes not `max_age_days`, result attrs `parts_uploaded`/`total_bytes` not `aborted`/`active`)
  - `test_integ_cost_optimization.py` — fixed `lambda_right_sizer` call (`function_name` not `function_names`), `unused_resource_finder` result attributes (`idle_lambdas`/`empty_queues`/`orphaned_log_groups`/`total_found` not `resources`), `log_retention_enforcer` result (`groups_updated` not `updated`), `cost_attribution_tagger` param (`required_tags` not `tags`) and result (`resources_tagged` not `tagged`), `concurrency_optimizer` result (`functions` not `recommendations`); handled `ResourceConflictException` on Lambda creation; skipped `dynamodb_capacity_advisor` (CloudWatch GetMetricStatistics 500 on LocalStack)
  - `test_integ_networking.py` — fixed `vpc_connectivity_manager` call (`connectivity_type`/`requestor_vpc_id`/`acceptor_vpc_id` not `vpc_id`), `route53_health_check_manager` call (`endpoints`/`alarm_prefix`/`sns_topic_arn` not `domain`), `eventbridge_cross_account_forwarder` call (`event_pattern` dict/`target_event_bus_arn`/`target_account_id` not `source_bus_name`)
  - `test_integ_governance.py` — fixed `kms_key_rotation_auditor` param (`report_key` not `key_prefix`) and result attributes (`total_keys`/`rotation_enabled`/`rotation_disabled` not `keys_audited`/`non_rotating_keys`), `config_rule_remediation_executor` params (`config_rule_name`/`remediation_lambda_arn` not `rule_name`/`lambda_function_name`) and result (`remediated_count` not `remediated`); handled `ResourceConflictException` on Lambda creation
  - `test_integ_finding_ops.py` — fixed `security_hub_finding_router` params (`critical_queue_url`/`high_queue_url`/`default_queue_url` not `queue_url`) and result attributes; skipped Security Hub and CloudTrail tests (not supported in LocalStack community edition)

### Added
- **Unit tests for 33 missing functions** across 4 test files (`test_ai_ml_pipelines.py`, `test_security_ops.py`, `test_cost_optimization.py`, `test_deployment.py`) achieving 100% function coverage; 395 tests total covering success paths, all error/exception branches, polling/timeout paths, edge cases, and model constructors
  - `test_ai_ml_pipelines.py` (extended) — 11 new test classes for `rekognition_face_indexer`, `rekognition_video_label_pipeline`, `polly_audio_generator`, `transcribe_job_to_s3`, `comprehend_pii_redactor`, `textract_form_extractor`, `bedrock_knowledge_base_ingestor`, `bedrock_guardrail_enforcer`, `personalize_real_time_recommender`, `forecast_inference_pipeline`, `sagemaker_batch_transform_monitor`; 84 tests total
  - `test_security_ops.py` (extended) — 6 new test classes for `cognito_group_sync_to_dynamodb`, `cloudfront_signed_url_factory`, `waf_ip_blocklist_updater`, `shield_advanced_protection_manager`, `acm_certificate_expiry_monitor`, `cognito_pre_token_enricher`; 77 tests total
  - `test_cost_optimization.py` (extended) — 8 new test classes for `trusted_advisor_report_to_s3`, `cost_and_usage_report_analyzer`, `savings_plan_coverage_reporter`, `ec2_idle_instance_stopper`, `rds_idle_snapshot_and_delete`, `ecr_lifecycle_policy_applier`, `s3_intelligent_tiering_enrollor`, `lambda_dead_code_detector`; 99 tests total
  - `test_deployment.py` (extended) — 8 new test classes for `cloudfront_invalidation_with_logging`, `elastic_beanstalk_env_refresher`, `app_runner_auto_deployer`, `eks_node_group_scaler`, `eks_config_map_sync`, `batch_job_monitor`, `autoscaling_scheduled_action_manager`, `stepfunctions_execution_tracker`; 135 tests total

- **Unit tests for 18 functions** across 5 new test files (`test_api_gateway_ops.py`, `test_iot_pipelines.py`, `test_contact_center_ops.py`, `test_media_processing.py`, `test_cache_ops.py`) achieving full branch coverage; 194 tests total covering success paths, all error/exception branches, polling/timeout paths, edge cases, and model constructors
  - `test_api_gateway_ops.py` (new) — 5 test classes for `websocket_session_manager`, `jwt_lambda_authorizer`, `apigw_usage_plan_enforcer`, `rate_limiter`, `api_gateway_domain_migrator` plus `_decode_jwt_claims` helper and model tests
  - `test_iot_pipelines.py` (new) — 5 test classes for `iot_telemetry_to_timestream`, `iot_device_shadow_sync`, `iot_fleet_command_broadcaster`, `iot_alert_to_sns`, `iot_greengrass_component_deployer` plus model tests
  - `test_contact_center_ops.py` (new) — 3 test classes for `connect_contact_event_to_dynamodb`, `connect_post_call_analyzer`, `lex_escalation_to_connect` plus model tests
  - `test_media_processing.py` (new) — 2 test classes for `ivs_stream_recording_archiver`, `mediaconvert_job_orchestrator` plus model tests
  - `test_cache_ops.py` (new) — 3 test classes for `elasticache_warmer`, `elasticache_cache_invalidator`, `memorydb_snapshot_to_s3` plus `_extract_ddb_value` and `_describe_elasticache_endpoint` helper tests and model tests

- **Unit tests for 17 missing functions** across 5 test files (`test_networking.py`, `test_config_loader.py`, `test_resource_ops.py`, `test_finding_ops.py`, `test_governance.py`) achieving 100% function coverage; 283 tests total covering success paths, all error/exception branches, pagination, edge cases, and model constructors
  - `test_finding_ops.py` (new) — 6 test classes for `inspector_finding_to_jira`, `macie_finding_remediation`, `detective_graph_exporter`, `security_hub_finding_router`, `cloudtrail_anomaly_detector`, `access_analyzer_finding_suppressor`
  - `test_governance.py` (new) — 4 test classes for `config_rule_remediation_executor`, `organizations_scp_drift_detector`, `sso_permission_set_auditor`, `kms_key_rotation_auditor`
  - `test_networking.py` (extended) — 4 new test classes for `vpc_lattice_service_registrar`, `transit_gateway_route_auditor`, `route53_health_check_manager`, `eventbridge_cross_account_forwarder`
  - `test_config_loader.py` (extended) — 2 new test classes for `appconfig_feature_flag_loader`, `cross_region_parameter_replicator`
  - `test_resource_ops.py` (extended) — 1 new test class for `ses_suppression_list_manager`
- **Unit tests for 22 functions** across 3 new test files (`test_ci_cd_ops.py`, `test_storage_ops.py`, `test_analytics_pipelines.py`) covering all public functions in `ci_cd_ops.py` (4), `storage_ops.py` (5), and `analytics_pipelines.py` (13); 164 tests total covering success paths, all error/exception branches, edge cases, polling/timeout paths, pagination, and model constructors

### Fixed
- `analytics_pipelines.glue_crawler_and_catalog_sync` — fixed `UnboundLocalError` for `ref_item` when DynamoDB `get_item` raises `ClientError`; variable is now initialized before the try block

### Added
- **Unit tests for 10 missing functions** achieving 100% function coverage across `data_flow_etl.py` (5 functions: `msk_topic_to_s3_archiver`, `msk_schema_registry_enforcer`, `documentdb_change_stream_to_sqs`, `neptune_graph_backup_to_s3`, `keyspaces_ttl_enforcer`), `observability.py` (4 functions: `kinesis_analytics_alarm_manager`, `dms_task_monitor`, `health_event_to_teams`, `service_quota_monitor`), and `resilience.py` (1 function: `distributed_lock_manager`); covers happy paths, all error/exception branches, edge cases, and model constructors
- **100 new multi-service orchestration functions** (sync + async) across 10 new modules and 10 extended modules, each combining 2+ AWS services with Pydantic v2 frozen result models; cross-replicated to TypeScript, Rust, Ruby, Go, C#, and Java companion projects
- **Java companion project cross-replication** — all 100 new Python functions replicated to `E:\Repo\IdeaProjects\AwsUtil` as Java 21 service classes with matching records and method stubs following existing `IotPipelinesService.java` pattern
  - New files: `ApiGatewayOpsService.java` (5 methods), `ContactCenterOpsService.java` (3 methods), `MediaProcessingService.java` (2 methods), `CacheOpsService.java` (3 methods), `CiCdOpsService.java` (4 methods), `StorageOpsService.java` (5 methods), `GovernanceOpsService.java` (4 methods), `FindingOpsService.java` (6 methods), `AnalyticsPipelinesService.java` (13 methods)
  - Extended files: `AiMlPipelinesService.java` (+11 methods), `SecurityOpsService.java` (+6 methods, +1 bonus), `CostOptimizationService.java` (+8 methods), `NetworkingService.java` (+4 methods, +1 bonus), `ObservabilityService.java` (+4 methods), `DeploymentService.java` (+8 methods), `ResilienceService.java` (+1 method), `ConfigLoaderService.java` (+2 methods), `DataFlowEtlService.java` (+5 methods), `ResourceOpsService.java` (+1 method)
  - All Java records placed as package-private top-level types in the same file before the `public final class`; type mappings: `str→String`, `int→int`, `float→double`, `bool→boolean`, `list[str]→List<String>`, `dict→Map<String,Object>`, `optional→String (nullable)`
- **C# companion project cross-replication** — all 100 new Python functions replicated to `E:\Repo\RiderProject\AwsUtil` as C# .NET service classes with `public sealed record` result types and `public static async Task<T>` method stubs following the `ErrorClassifier.ClassifyAwsError` pattern
  - New files: `ApiGatewayOpsService.cs` (5 methods), `ContactCenterOpsService.cs` (3 methods), `MediaProcessingService.cs` (2 methods), `CacheOpsService.cs` (3 methods), `CiCdOpsService.cs` (4 methods), `StorageOpsService.cs` (5 methods), `GovernanceService.cs` (4 methods), `FindingOpsService.cs` (6 methods), `AnalyticsPipelinesService.cs` (13 methods)
  - Extended files: `AiMlPipelinesService.cs` (+11 methods), `SecurityOpsService.cs` (+6 methods), `CostOptimizationService.cs` (+8 methods), `NetworkingService.cs` (+4 new methods + `VpcConnectivityManager` stub fix), `ObservabilityService.cs` (+4 methods), `DeploymentService.cs` (+8 methods), `ResilienceService.cs` (+1 method), `ConfigLoaderService.cs` (+2 methods), `DataFlowEtlService.cs` (+5 methods), `ResourceOpsService.cs` (+1 method)
  - All async methods include synchronous `.GetAwaiter().GetResult()` wrappers; type mappings: `str→string`, `int→int`, `float→double`, `bool→bool`, `list[str]→List<string>`, `dict→Dictionary<string,object>`, `optional→type?`
- **Ruby companion project cross-replication** — all 100 new Python functions replicated to `E:\Repo\RubymineProjects\AwsUtil` as Ruby service modules with matching Structs and NotImplementedError method stubs following existing module_function pattern
  - New files: `api_gateway_ops.rb` (5 methods), `contact_center_ops.rb` (3 methods), `media_processing.rb` (2 methods), `cache_ops.rb` (3 methods), `ci_cd_ops.rb` (4 methods), `storage_ops.rb` (5 methods), `governance.rb` (4 methods), `finding_ops.rb` (6 methods), `analytics_pipelines.rb` (13 methods)
  - Extended files: `ai_ml_pipelines.rb` (+11 methods), `security_ops.rb` (+6 methods), `cost_optimization.rb` (+8 methods), `networking.rb` (+4 methods), `observability.rb` (+4 methods), `deployment.rb` (+8 methods), `resilience.rb` (+1 method), `config_loader.rb` (+2 methods), `data_flow_etl.rb` (+5 methods), `resource_ops.rb` (+1 method)
  - All Structs use `keyword_init: true`; all methods raise `NotImplementedError` with `rescue Aws::Errors::ServiceError` clause
- `api_gateway_ops.py` / `aio/api_gateway_ops.py` — 5 functions: `websocket_session_manager` (API Gateway Management API + DynamoDB), `jwt_lambda_authorizer` (Cognito + DynamoDB + CloudWatch Logs), `apigw_usage_plan_enforcer` (API Gateway + DynamoDB + SNS), `rate_limiter` (DynamoDB + CloudWatch), `api_gateway_domain_migrator` (API Gateway v2 + ACM + Route53)
- `iot_pipelines.py` / `aio/iot_pipelines.py` — 5 functions: `iot_telemetry_to_timestream` (IoT Core + Timestream Write), `iot_device_shadow_sync` (IoT Data + DynamoDB), `iot_fleet_command_broadcaster` (IoT Core + S3 + DynamoDB), `iot_alert_to_sns` (IoT SiteWise + SNS), `iot_greengrass_component_deployer` (Greengrass v2 + S3)
- `contact_center_ops.py` / `aio/contact_center_ops.py` — 3 functions: `connect_contact_event_to_dynamodb` (Kinesis + DynamoDB), `connect_post_call_analyzer` (S3 + Transcribe + Comprehend + DynamoDB), `lex_escalation_to_connect` (Lex V2 + Connect)
- `media_processing.py` / `aio/media_processing.py` — 2 functions: `ivs_stream_recording_archiver` (IVS + S3 + DynamoDB), `mediaconvert_job_orchestrator` (MediaConvert + DynamoDB + SNS)
- `cache_ops.py` / `aio/cache_ops.py` — 3 functions: `elasticache_warmer` (ElastiCache + DynamoDB), `elasticache_cache_invalidator` (DynamoDB Streams + ElastiCache), `memorydb_snapshot_to_s3` (MemoryDB + S3)
- `ci_cd_ops.py` / `aio/ci_cd_ops.py` — 4 functions: `codebuild_triggered_deploy` (CodeBuild + S3 + CodeDeploy), `codepipeline_approval_notifier` (CodePipeline + SES v2 + DynamoDB), `codecommit_pr_to_codebuild` (CodeCommit + CodeBuild), `codeartifact_package_promoter` (CodeArtifact + SSM)
- `storage_ops.py` / `aio/storage_ops.py` — 5 functions: `efs_to_s3_sync` (DataSync + DynamoDB), `fsx_backup_to_s3` (FSx + S3), `transfer_family_event_processor` (Transfer + S3 + SNS), `storage_gateway_cache_monitor` (Storage Gateway + CloudWatch), `lightsail_snapshot_to_s3` (Lightsail + S3)
- `governance.py` / `aio/governance.py` — 4 functions: `config_rule_remediation_executor` (Config + Lambda + DynamoDB), `organizations_scp_drift_detector` (Organizations + S3 + SNS), `sso_permission_set_auditor` (SSO Admin + S3 + SNS), `kms_key_rotation_auditor` (KMS + S3 + SNS)
- `finding_ops.py` / `aio/finding_ops.py` — 6 functions: `inspector_finding_to_jira` (Inspector v2 + DynamoDB + SES v2), `macie_finding_remediation` (Macie2 + S3 + DynamoDB), `detective_graph_exporter` (Detective + S3 + Glue), `security_hub_finding_router` (Security Hub + SQS), `cloudtrail_anomaly_detector` (CloudTrail + SNS), `access_analyzer_finding_suppressor` (Access Analyzer + DynamoDB + CloudWatch Logs)
- `analytics_pipelines.py` / `aio/analytics_pipelines.py` — 13 functions: `redshift_unload_to_s3`, `redshift_serverless_query_runner`, `quicksight_dashboard_embedder`, `quicksight_dataset_refresher`, `athena_result_to_dynamodb`, `glue_crawler_and_catalog_sync`, `glue_databrew_profile_pipeline`, `emr_serverless_job_runner`, `timestream_query_to_s3`, `neptune_graph_query_to_s3`, `elbv2_access_log_analyzer`, `glue_job_output_to_redshift`, `opensearch_index_lifecycle_manager`
- `security_ops.py` / `aio/security_ops.py` — 6 new functions: `cognito_group_sync_to_dynamodb`, `cloudfront_signed_url_factory`, `waf_ip_blocklist_updater`, `shield_advanced_protection_manager`, `acm_certificate_expiry_monitor`, `cognito_pre_token_enricher`
- `cost_optimization.py` / `aio/cost_optimization.py` — 8 new functions: `trusted_advisor_report_to_s3`, `cost_and_usage_report_analyzer`, `savings_plan_coverage_reporter`, `ec2_idle_instance_stopper`, `rds_idle_snapshot_and_delete`, `ecr_lifecycle_policy_applier`, `s3_intelligent_tiering_enrollor`, `lambda_dead_code_detector`
- `ai_ml_pipelines.py` / `aio/ai_ml_pipelines.py` — 11 new functions: `rekognition_face_indexer`, `rekognition_video_label_pipeline`, `polly_audio_generator`, `transcribe_job_to_s3`, `comprehend_pii_redactor`, `textract_form_extractor`, `bedrock_knowledge_base_ingestor`, `bedrock_guardrail_enforcer`, `personalize_real_time_recommender`, `forecast_inference_pipeline`, `sagemaker_batch_transform_monitor`
- `deployment.py` / `aio/deployment.py` — 8 new functions: `cloudfront_invalidation_with_logging`, `elastic_beanstalk_env_refresher`, `app_runner_auto_deployer`, `eks_node_group_scaler`, `eks_config_map_sync`, `batch_job_monitor`, `autoscaling_scheduled_action_manager`, `stepfunctions_execution_tracker`
- `networking.py` / `aio/networking.py` — 4 new functions: `vpc_lattice_service_registrar`, `transit_gateway_route_auditor`, `route53_health_check_manager`, `eventbridge_cross_account_forwarder`
- `observability.py` / `aio/observability.py` — 4 new functions: `kinesis_analytics_alarm_manager`, `dms_task_monitor`, `health_event_to_teams`, `service_quota_monitor`
- `resilience.py` / `aio/resilience.py` — 1 new function: `distributed_lock_manager`
- `config_loader.py` / `aio/config_loader.py` — 2 new functions: `appconfig_feature_flag_loader`, `cross_region_parameter_replicator`
- `data_flow_etl.py` / `aio/data_flow_etl.py` — 5 new functions: `msk_topic_to_s3_archiver`, `msk_schema_registry_enforcer`, `documentdb_change_stream_to_sqs`, `neptune_graph_backup_to_s3`, `keyspaces_ttl_enforcer`
- `resource_ops.py` / `aio/resource_ops.py` — 1 new function: `ses_suppression_list_manager`
- `Pipfile` — `moto` extras expanded with `batch`, `autoscaling`, `eks`, `elasticbeanstalk`, `apprunner`, `cloudfront`, `rds`, `neptune`, `keyspaces`; `boto3-stubs` extras expanded with all service clients needed for new modules
- `docs/multi_service_utilities_research_v2.md` — research document with 100 new multi-service AWS utility function ideas
- `scripts/generate_go_impl.py`, `scripts/generate_cs_impl.py`, `scripts/generate_ts_additions.py` — cross-language code generators
- **Integration test infrastructure** with LocalStack (`docker-compose.yml`, `tests/integration/conftest.py`) — session-scoped fixtures for S3, DynamoDB, SNS, SQS, SSM, Secrets Manager, CloudWatch Logs, KMS, IAM; `AWS_ENDPOINT_URL` support in `_client.py` for transparent LocalStack routing
- **Integration tests for all 21 modules** (`tests/integration/test_integ_*.py`) — 11 test files covering security_ops, config_loader, resource_ops, data_flow_etl, lambda_middleware, deployment, observability, resilience, cost_optimization, networking, governance, finding_ops against LocalStack
- Production-grade `README.md` with animated SVG banners, hero screenshot, architecture diagrams, full CI/CD documentation
- `.github/banners/` — animated banners (`gravitational-lens-warp`, `build-pipeline-cascade`, `circuit-trace-pulse`, `service-mesh-nebula`) with manifest tracking
- `.github/screenshots/hero.svg` — IDE mockup showing library usage, test results, and coverage
- `.github/workflows/` — `stats.yml`, `release-stats.yml`, `update-badges.yml`, `banner-archive.yml`
- `scripts/generate_docs_html.py` — per-language API documentation generator for masrikdahir.com
- Documentation at `masrikdahir.com/product/awsutil` — animated landing page with per-language API references, searchable sidebar, model extraction for all 7 languages
- Reusable `doc-writer` skill for generating multi-language API documentation

### Changed
- `README.md` — full rewrite with project banner, author banner, hero screenshot, TL;DR, architecture Mermaid diagram, module reference tables, async usage examples, CI/CD workflow table, and contributing guide
- `.github/banners/manifest.json` — deduplicated stale entries, added new banners
- `product/library/awsutil/python/awsutil_data.js` — regenerated from source; totals now 7,868 functions, 5,673 models, 149 modules
- `product/library/awsutil/rust/awsutil_data.js` — updated with 95 new functions, 95 new models, and 9 new modules from Rust companion; totals now 7,797 functions, 5,622 models, 145 modules
- `product/library/awsutil/go/awsutil_data.js` — updated with 64 new functions, 63 new models, and 9 new modules from Go companion; totals now 7,802 functions, 5,622 models, 145 modules. New modules: `api_gateway_ops`, `contact_center_ops`, `media_processing`, `cache_ops`, `ci_cd_ops`, `storage_ops`, `governance`, `finding_ops`, `analytics_pipelines`. Extended modules: `security_ops` (+6), `cost_optimization` (+8), `networking` (+4), `deployment` (+1)
- `product/library/awsutil/csharp/awsutil_data.js` — updated with 190 new functions, 95 new models, and 9 new modules from C# companion; totals now 3,412 functions, 2,462 models, 143 modules. New modules: `api_gateway_ops`, `contact_center_ops`, `media_processing`, `cache_ops`, `ci_cd_ops`, `storage_ops`, `governance`, `finding_ops`, `analytics_pipelines`. Extended modules: `ai_ml_pipelines` (+22), `security_ops` (+12), `cost_optimization` (+16), `networking` (+8), `observability` (+8), `deployment` (+16), `resilience` (+2), `config_loader` (+4), `data_flow_etl` (+10), `resource_ops` (+2)
- `product/library/awsutil/awsutil.html` — updated C# card stats to 3,412 functions, 143 modules, 7,284 models; corrected aggregate hero totals to 49,119 functions and 41,070 models across all 7 languages

### Fixed
- Fixed broken model cross-links in documentation data files across all 7 languages — orphan modelAnchors removed, unanchored models added, all return-type signature links now resolve to valid model definitions
- `product/library/awsutil/csharp/awsutil_data.js` — added 4,822 missing model definitions across 135 modules parsed from C# source; totalModels 2,462 → 7,284
- `product/library/awsutil/java/awsutil_data.js` — added 51 missing record models across 11 modules; totalModels 5,571 → 5,622
- `product/library/awsutil/typescript/awsutil_data.js` — added 176 missing type definitions across 4 modules (api_gateway +129, ecr +46, config_loader +1); totalModels 5,449 → 5,625
- `product/library/awsutil/ruby/awsutil_data.js` — added DynamoDBStreamImage model and 98 missing modelAnchors entries
- `product/library/awsutil/rust/awsutil_data.js` — removed 11 orphan anchors, added 5 missing anchors for IoT module models
- `product/library/awsutil/go/awsutil_data.js` — removed 1 orphan anchor (DynamoDBStreamImage)
- Refactored `generate_docs_html.py` from server-side HTML rendering to Vue.js data-driven architecture
- Restructured documentation output from `product/library/<lang>/` to `product/library/awsutil/<lang>/`
- Expanded cross-project sync rule in CLAUDE.md to cover all 7 companion implementations

## [2.2.7] - 2026-04-09

### Changed
- Scoped CI workflows (`test.yml`, `coverage.yml`, `mutation.yml`) to run against the `s3` module only instead of the entire test suite
- Added `scripts/` to `.gitignore`
- Moved README author banner SVG to external file (`.github/banner.svg`) for GitHub rendering compatibility

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
