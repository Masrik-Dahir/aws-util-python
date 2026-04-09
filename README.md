# aws-util

**Author:** [Masrik Dahir](https://www.masrikdahir.com/) | [GitHub](https://github.com/Masrik-Dahir/aws-util-python) | [PyPI](https://pypi.org/project/aws-util/)

[![Build](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/build.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/build.yml)
[![Coverage](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/coverage.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/coverage.yml)
[![Lint](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/lint.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/lint.yml)
[![Test](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/test.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/test.yml)
[![Test](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/mutation.yml/badge.svg)](https://github.com/Masrik-Dahir/aws-util-python/actions/workflows/mutation.yml)


A comprehensive Python utility library for **100+ AWS services** with **136 modules** and **7,300+ typed API wrappers**. Every module provides clean, typed helper functions backed by Pydantic data models, TTL-aware cached boto3 clients, automatic pagination, built-in `wait_for_*` polling helpers, and **complex multi-step utilities** for real-world workflows. Covers every standard boto3 client method across all 103 service modules with both sync and async implementations. Includes dedicated multi-service orchestration modules for config loading, deployments, alerting, and data pipelines.

## Installation

```bash
pip install aws-util
```

## Requirements

- Python 3.10+
- `boto3`
- `pydantic >= 2.0`
- `cryptography >= 42.0` (for KMS envelope encryption)
- `aiohttp >= 3.9` (for native async `aws_util.aio` modules)
- AWS credentials configured (environment variables, IAM role, or `~/.aws/credentials`)

This package ships a PEP 561 `py.typed` marker — mypy and pyright will pick up all type annotations automatically.

---

## Service Coverage

| # | Module | AWS Service | Key Utilities |
|---|---|---|---|
| 1 | `placeholder` | SSM + Secrets Manager | `retrieve` — resolves `${ssm:...}` / `${secret:...}` placeholders |
| 2 | `parameter_store` | SSM Parameter Store | `get_parameter`, `put_parameter`, `delete_parameter`, **`get_parameters_by_path`**, **`get_parameters_batch`**, **`describe_parameters`**, **`delete_parameters`** |
| 3 | `secrets_manager` | Secrets Manager | `get_secret`, **`create_secret`**, **`update_secret`**, **`delete_secret`**, **`list_secrets`**, **`rotate_secret`**, **`batch_get_secret_value`**, **`cancel_rotate_secret`**, **`describe_secret`**, **`get_random_password`**, **`get_resource_policy`**, **`list_secret_version_ids`**, **`put_resource_policy`**, **`put_secret_value`**, **`remove_regions_from_replication`**, **`replicate_secret_to_regions`**, **`restore_secret`**, **`tag_resource`**, **`untag_resource`**, **`update_secret_version_stage`**, **`validate_resource_policy`** |
| 4 | `s3` | S3 | upload, download, list, copy, delete, presigned URL, **`delete_prefix`**, **`move_object`**, **`batch_copy`**, **`download_as_text`**, **`get_object_metadata`**, **`get_object`**, **`list_object_versions`**, **`upload_fileobj`** |
| 5 | `dynamodb` | DynamoDB | get, put, update, delete, query, scan, batch, **`update_item_raw`**, **`Key`**, **`Attr`** (re-exported), **`create_table`**, **`delete_table`**, **`describe_table`**, **`update_table`**, **`list_tables`**, **`create_backup`**, **`delete_backup`**, **`describe_backup`**, **`list_backups`**, **`describe_continuous_backups`**, **`update_continuous_backups`**, **`restore_table_from_backup`**, **`restore_table_to_point_in_time`**, **`create_global_table`**, **`describe_global_table`**, **`describe_global_table_settings`**, **`list_global_tables`**, **`update_global_table`**, **`update_global_table_settings`**, **`describe_time_to_live`**, **`update_time_to_live`**, **`list_tags_of_resource`**, **`tag_resource`**, **`untag_resource`**, **`describe_kinesis_streaming_destination`**, **`enable_kinesis_streaming_destination`**, **`disable_kinesis_streaming_destination`**, **`update_kinesis_streaming_destination`**, **`describe_contributor_insights`**, **`list_contributor_insights`**, **`update_contributor_insights`**, **`describe_endpoints`**, **`describe_limits`**, **`describe_table_replica_auto_scaling`**, **`update_table_replica_auto_scaling`**, **`get_resource_policy`**, **`put_resource_policy`**, **`delete_resource_policy`**, **`execute_statement`**, **`execute_transaction`**, **`batch_execute_statement`**, **`export_table_to_point_in_time`**, **`describe_export`**, **`list_exports`**, **`import_table`**, **`describe_import`**, **`list_imports`** |
| 6 | `sqs` | SQS | send, receive, delete, batch, purge, **`send_large_batch`**, **`wait_for_message`**, **`drain_queue`**, **`replay_dlq`** |
| 7 | `sns` | SNS | publish, publish_batch, **publish_fan_out**, **create_topic_if_not_exists** |
| 8 | `lambda_` | Lambda | invoke, invoke_async |
| 9 | `cloudwatch` | CloudWatch Metrics + Logs | put_metric, put_log_events, get_log_events |
| 10 | `sts` | STS | get_caller_identity, get_account_id, assume_role, **assume_role_session** |
| 11 | `eventbridge` | EventBridge | put_event, put_events, **put_events_chunked**, **list_rules** |
| 12 | `kms` | KMS | encrypt, decrypt, generate_data_key, **envelope_encrypt**, **envelope_decrypt**, **re_encrypt** |
| 13 | `ec2` | EC2 | describe, start, stop, reboot, terminate, create_image |
| 14 | `rds` | RDS | describe, start, stop, create/delete snapshots |
| 15 | `ecs` | ECS | run_task, stop_task, describe, list, update_service |
| 16 | `ecr` | ECR | get_auth_token, list_repositories, list_images, **ensure_repository**, **get_latest_image_tag** |
| 17 | `iam` | IAM | create/delete/list roles, attach/detach policies, list users, **create_role_with_policies**, **ensure_role** |
| 18 | `cognito` | Cognito User Pools | create/get/delete user, list users, set password, auth, **get_or_create_user**, **bulk_create_users**, **reset_user_password** |
| 19 | `route53` | Route 53 | list_hosted_zones, upsert_record, delete_record, **wait_for_change**, **bulk_upsert_records** |
| 20 | `acm` | ACM | list, describe, request, delete, import, export, renew certificates, add/remove/list tags, get/put account config, resend validation email, update certificate options, **wait_for_certificate**, **find_certificate_by_domain** |
| 21 | `stepfunctions` | Step Functions | start, describe, stop, list, wait_for_execution, **run_and_wait**, **get_execution_history** |
| 22 | `cloudformation` | CloudFormation | create, update, delete, describe, get_outputs, wait, **deploy_stack**, **get_export_value** |
| 23 | `kinesis` | Kinesis Data Streams | put_record, put_records, get_records, describe_stream, describe_stream_summary, create_stream, delete_stream, list_streams, list_shards, get_shard_iterator, add_tags_to_stream, remove_tags_from_stream, list_tags_for_stream, increase/decrease_stream_retention_period, merge_shards, split_shard, start/stop_stream_encryption, enable/disable_enhanced_monitoring, update_shard_count, update_stream_mode, register/deregister/describe_stream_consumer, list_stream_consumers, describe_limits, subscribe_to_shard, put/get/delete_resource_policy, **consume_stream** |
| 24 | `firehose` | Kinesis Firehose | put_record, put_record_batch, list_delivery_streams, **put_record_batch_with_retry** |
| 25 | `ses` | SES | send_email, send_templated_email, send_raw_email, **send_with_attachment**, **send_bulk** |
| 26 | `glue` | Glue | start_job_run, get_job_run, list_jobs, wait_for_job_run, **run_job_and_wait**, **stop_job_run** |
| 27 | `athena` | Athena | start_query, get_results, run_query, **get_table_schema**, **run_ddl** |
| 28 | `bedrock` | Bedrock | invoke_model, invoke_claude, invoke_titan_text, **chat**, **embed_text**, **stream_invoke_claude**, plus all 94 Bedrock management API methods (guardrails, models, evaluation jobs, inference profiles, provisioned throughput, etc.) |
| 29 | `rekognition` | Rekognition | detect_labels, detect_faces, detect_text, compare_faces, **create_collection**, **index_face**, **search_face_by_image**, delete_collection, **ensure_collection** |
| 30 | `textract` | Textract | detect_document_text, analyze_document, async jobs, **extract_text**, **extract_tables**, **extract_form_fields**, **extract_all** |
| 31 | `comprehend` | Comprehend | detect_sentiment, detect_entities, detect_key_phrases, detect_pii, **analyze_text**, **redact_pii**, **batch_detect_sentiment** |
| 32 | `translate` | Translate | translate_text, list_languages, **translate_batch** |
| 33 | `config_loader` | SSM + Secrets Manager *(multi-service)* | **`load_app_config`** (concurrent), **`resolve_config`** (placeholder expansion), **`get_db_credentials`**, **`get_ssm_parameter_map`** |
| 34 | `deployer` | Lambda + ECS + ECR + SSM *(multi-service)* | **`deploy_lambda_with_config`**, **`deploy_ecs_image`**, **`deploy_ecs_from_ecr`**, **`update_lambda_code_from_s3`**, **`update_lambda_alias`** |
| 35 | `notifier` | SNS + SES + SQS *(multi-service)* | **`send_alert`** (concurrent), **`notify_on_exception`** (decorator), **`broadcast`**, **`resolve_and_notify`** |
| 36 | `data_pipeline` | S3 + Glue + Athena + Kinesis + DynamoDB + SQS *(multi-service)* | **`run_glue_then_query`**, **`export_query_to_s3_json`**, **`s3_json_to_dynamodb`**, **`s3_jsonl_to_sqs`**, **`kinesis_to_s3_snapshot`**, **`parallel_export`** |
| 37 | `resource_ops` | SQS + DynamoDB + S3 + SSM + Lambda + ECR + SNS + Athena + STS *(multi-service)* | **`reprocess_sqs_dlq`**, **`backup_dynamodb_to_s3`**, **`sync_ssm_params_to_lambda_env`**, **`delete_stale_ecr_images`**, **`rebuild_athena_partitions`**, **`s3_inventory_to_dynamodb`**, **`cross_account_s3_copy`**, **`rotate_secret_and_notify`**, **`lambda_invoke_with_secret`**, **`publish_s3_keys_to_sqs`** |
| 38 | `security_ops` | S3 + IAM + KMS + Secrets Manager + SNS + Cognito + SES + SSM + CloudWatch + EC2 + CloudFormation *(multi-service)* | **`audit_public_s3_buckets`**, **`rotate_iam_access_key`**, **`kms_encrypt_to_secret`**, **`iam_roles_report_to_s3`**, **`enforce_bucket_versioning`**, **`cognito_bulk_create_users`**, **`sync_secret_to_ssm`**, **`create_cloudwatch_alarm_with_sns`**, **`tag_ec2_instances_from_ssm`**, **`validate_and_store_cfn_template`** |
| 39 | `lambda_middleware` | Lambda + DynamoDB + SQS + CloudWatch + SSM *(multi-service)* | **`idempotent_handler`**, **`batch_processor`**, **`middleware_chain`**, **`lambda_timeout_guard`**, **`cold_start_tracker`**, **`lambda_response`**, **`cors_preflight`**, **`parse_event`**, **`evaluate_feature_flag`**, **`evaluate_feature_flags`** |
| 40 | `api_gateway` | API Gateway + Lambda + DynamoDB + Cognito *(multi-service)* | **`jwt_authorizer`**, **`api_key_authorizer`**, **`request_validator`**, **`throttle_guard`**, **`websocket_connect`**, **`websocket_disconnect`**, **`websocket_list_connections`**, **`websocket_broadcast`**, plus all 124 API Gateway REST API management methods (REST APIs, stages, deployments, authorizers, models, usage plans, VPC links, etc.) |
| 41 | `event_orchestration` | EventBridge + Step Functions + Lambda + SQS + DynamoDB + Scheduler + Pipes *(multi-service)* | **`create_eventbridge_rule`**, **`put_eventbridge_targets`**, **`delete_eventbridge_rule`**, **`create_schedule`**, **`delete_schedule`**, **`run_workflow`**, **`saga_orchestrator`**, **`fan_out_fan_in`**, **`start_event_replay`**, **`describe_event_replay`**, **`create_pipe`**, **`delete_pipe`**, **`create_sqs_event_source_mapping`**, **`delete_event_source_mapping`** |
| 42 | `data_flow_etl` | S3 + DynamoDB + Kinesis + Firehose + OpenSearch + Glue + Athena + CloudWatch + SNS *(multi-service)* | **`s3_event_to_dynamodb`**, **`dynamodb_stream_to_opensearch`**, **`dynamodb_stream_to_s3_archive`**, **`s3_csv_to_dynamodb_bulk`**, **`kinesis_to_firehose_transformer`**, **`cross_region_s3_replicator`**, **`etl_status_tracker`**, **`s3_multipart_upload_manager`**, **`data_lake_partition_manager`**, **`repair_partitions`** |
| 43 | `resilience` | Lambda + DynamoDB + SQS + SNS + S3 *(multi-service)* | **`circuit_breaker`**, **`retry_with_backoff`**, **`dlq_monitor_and_alert`**, **`poison_pill_handler`**, **`lambda_destination_router`**, **`graceful_degradation`**, **`timeout_sentinel`** |
| 44 | `observability` | CloudWatch + X-Ray + Synthetics + CloudWatch Logs *(multi-service)* | **`StructuredLogger`**, **`create_xray_trace`**, **`emit_emf_metric`**, **`create_lambda_alarms`**, **`create_dlq_depth_alarm`**, **`run_log_insights_query`**, **`generate_lambda_dashboard`**, **`aggregate_errors`**, **`create_canary`**, **`build_service_map`** |
| 45 | `deployment` | Lambda + CloudFormation + EventBridge + CloudWatch + S3 *(multi-service)* | **`lambda_canary_deploy`**, **`lambda_layer_publisher`**, **`stack_deployer`**, **`environment_promoter`**, **`lambda_warmer`**, **`config_drift_detector`**, **`rollback_manager`**, **`lambda_package_builder`** |
| 46 | `security_compliance` | IAM + Lambda + Secrets Manager + SSM + SNS + EC2 + DynamoDB + SQS + S3 + KMS + WAF + Cognito *(multi-service)* | **`least_privilege_analyzer`**, **`secret_rotation_orchestrator`**, **`data_masking_processor`**, **`vpc_security_group_auditor`**, **`encryption_enforcer`**, **`api_gateway_waf_manager`**, **`compliance_snapshot`**, **`resource_policy_validator`**, **`cognito_auth_flow_manager`** |
| 47 | `cost_optimization` | Lambda + CloudWatch + SQS + CloudWatch Logs + DynamoDB + Resource Groups Tagging *(multi-service)* | **`lambda_right_sizer`**, **`unused_resource_finder`**, **`concurrency_optimizer`**, **`cost_attribution_tagger`**, **`dynamodb_capacity_advisor`**, **`log_retention_enforcer`** |
| 48 | `testing_dev` | Lambda + CloudFormation + DynamoDB + SQS + S3 + SNS *(multi-service)* | **`lambda_event_generator`**, **`local_dynamodb_seeder`**, **`integration_test_harness`**, **`mock_event_source`**, **`lambda_invoke_recorder`**, **`snapshot_tester`** |
| 49 | `config_state` | SSM + Secrets Manager + DynamoDB + STS + Lambda + AppConfig *(multi-service)* | **`config_resolver`**, **`distributed_lock`**, **`state_machine_checkpoint`**, **`cross_account_role_assumer`**, **`environment_variable_sync`**, **`appconfig_feature_loader`** |
| 50 | `blue_green` | ECS + ELBv2 + Route53 + CloudWatch + SNS + Lambda + Application Auto Scaling *(multi-service)* | **`ecs_blue_green_deployer`**, **`weighted_routing_manager`**, **`lambda_provisioned_concurrency_scaler`** |
| 51 | `data_lake` | Glue + Lake Formation + Athena + S3 + DynamoDB + CloudWatch + SNS *(multi-service)* | **`schema_evolution_manager`**, **`lake_formation_access_manager`**, **`data_quality_pipeline`** |
| 52 | `cross_account` | EventBridge + CloudWatch Logs + Kinesis Firehose + S3 + DynamoDB + SQS + STS + Resource Groups Tagging *(multi-service)* | **`cross_account_event_bus_federator`**, **`centralized_log_aggregator`**, **`multi_account_resource_inventory`** |
| 53 | `event_patterns` | DynamoDB + SNS + SQS + EventBridge + S3 *(multi-service)* | **`transactional_outbox_processor`**, **`dlq_escalation_chain`**, **`event_sourcing_store`** |
| 54 | `database_migration` | DynamoDB + S3 + RDS + Route53 + Secrets Manager *(multi-service)* | **`dynamodb_table_migrator`**, **`rds_blue_green_orchestrator`** |
| 55 | `credential_rotation` | Secrets Manager + RDS + SNS *(multi-service)* | **`database_credential_rotator`** |
| 56 | `disaster_recovery` | EC2 + RDS + S3 + Route53 + SNS + Backup *(multi-service)* | **`disaster_recovery_orchestrator`**, **`backup_compliance_manager`** |
| 57 | `cost_governance` | Cost Explorer + CloudWatch + SNS *(multi-service)* | **`cost_anomaly_detector`**, **`savings_plan_analyzer`** |
| 58 | `security_automation` | GuardDuty + EC2 + IAM + Config + SNS + Lambda + S3 *(multi-service)* | **`guardduty_auto_remediator`**, **`config_rules_auto_remediator`** |
| 59 | `container_ops` | ECS + Application Auto Scaling + CloudWatch *(multi-service)* | **`ecs_capacity_provider_optimizer`** |
| 60 | `ml_pipeline` | SageMaker + CloudWatch + S3 + STS *(multi-service)* | **`sagemaker_endpoint_manager`**, **`model_registry_promoter`** |
| 61 | `networking` | EC2 (VPC) + Route53 *(multi-service)* | **`vpc_connectivity_manager`** |
| 62 | `redshift_data` | Redshift Data API | **`execute_statement`**, **`batch_execute_statement`**, **`describe_statement`**, **`get_statement_result`**, **`list_statements`**, **`cancel_statement`**, **`run_query`** (composite: execute + poll + get results) |
| 63 | `redshift` | Amazon Redshift | **`create_cluster`**, **`describe_clusters`**, **`delete_cluster`**, **`modify_cluster`**, **`reboot_cluster`**, **`create_cluster_snapshot`**, **`describe_cluster_snapshots`**, **`delete_cluster_snapshot`**, **`restore_from_cluster_snapshot`**, **`create_cluster_parameter_group`**, **`create_cluster_subnet_group`**, **`describe_logging_status`**, **`enable_logging`**, **`disable_logging`**, **`wait_for_cluster`** |
| 64 | `security_hub` | Security Hub | **`enable_security_hub`**, **`disable_security_hub`**, **`describe_hub`**, **`get_findings`**, **`update_findings`**, **`get_insight_results`**, **`list_insights`**, **`create_insight`**, **`update_insight`**, **`delete_insight`**, **`enable_import_findings_for_product`**, **`disable_import_findings_for_product`**, **`list_enabled_products_for_import`**, **`get_enabled_standards`**, **`batch_enable_standards`**, **`batch_disable_standards`**, **`describe_standards`**, **`describe_standards_controls`**, **`update_standards_control`**, **`invite_members`**, **`list_members`**, **`get_members`**, **`create_members`**, **`delete_members`**, **`get_administrator_account`**, **`accept_administrator_invitation`** |
| 65 | `access_analyzer` | IAM Access Analyzer | **`create_analyzer`**, **`get_analyzer`**, **`list_analyzers`**, **`delete_analyzer`**, **`update_analyzer`**, **`get_finding`**, **`list_findings`**, **`update_findings`**, **`get_analyzed_resource`**, **`list_analyzed_resources`**, **`start_resource_scan`**, **`create_archive_rule`**, **`get_archive_rule`**, **`list_archive_rules`**, **`update_archive_rule`**, **`delete_archive_rule`**, **`apply_archive_rule`**, **`validate_policy`**, **`check_access_not_granted`**, **`check_no_new_access`**, **`generate_finding_recommendation`** |
| 66 | `codedeploy` | CodeDeploy | **`create_application`**, **`get_application`**, **`list_applications`**, **`delete_application`**, **`create_deployment_group`**, **`get_deployment_group`**, **`list_deployment_groups`**, **`delete_deployment_group`**, **`create_deployment`**, **`get_deployment`**, **`list_deployments`**, **`stop_deployment`**, **`continue_deployment`**, **`register_application_revision`**, **`get_application_revision`**, **`list_application_revisions`**, **`create_deployment_config`**, **`get_deployment_config`**, **`wait_for_deployment`**, **`deploy_and_wait`** |
| 67 | `codecommit` | CodeCommit | **`create_repository`**, **`get_repository`**, **`list_repositories`**, **`delete_repository`**, **`update_repository_name`**, **`update_repository_description`**, **`create_branch`**, **`get_branch`**, **`list_branches`**, **`delete_branch`**, **`merge_branches_by_fast_forward`**, **`merge_branches_by_squash`**, **`create_commit`**, **`get_commit`**, **`get_file`**, **`put_file`**, **`delete_file`**, **`get_differences`**, **`create_pull_request`**, **`get_pull_request`**, **`list_pull_requests`**, **`merge_pull_request_by_fast_forward`**, **`get_blob`** |
| 68 | `organizations` | AWS Organizations | **`create_organization`**, **`describe_organization`**, **`create_organizational_unit`**, **`describe_organizational_unit`**, **`list_organizational_units_for_parent`**, **`list_accounts`**, **`list_accounts_for_parent`**, **`describe_account`**, **`create_account`**, **`invite_account_to_organization`**, **`accept_handshake`**, **`move_account`**, **`remove_account_from_organization`**, **`list_roots`**, **`list_children`**, **`list_parents`**, **`list_policies`**, **`describe_policy`**, **`create_policy`**, **`update_policy`**, **`delete_policy`**, **`attach_policy`**, **`detach_policy`**, **`enable_policy_type`**, **`disable_policy_type`**, **`list_tags_for_resource`**, **`tag_resource`** |
| 69 | `cloudtrail` | CloudTrail | **`create_trail`**, **`describe_trails`**, **`get_trail`**, **`update_trail`**, **`delete_trail`**, **`start_logging`**, **`stop_logging`**, **`get_trail_status`**, **`lookup_events`**, **`list_trails`**, **`create_event_data_store`**, **`describe_event_data_store`**, **`list_event_data_stores`**, **`delete_event_data_store`**, **`start_query`**, **`get_query_results`**, **`list_queries`**, **`put_event_selectors`**, **`get_event_selectors`**, **`put_insight_selectors`**, **`get_insight_selectors`** |
| 70 | `kinesis_analytics` | Kinesis Analytics V2 | **`create_application`**, **`describe_application`**, **`list_applications`**, **`delete_application`**, **`start_application`**, **`stop_application`**, **`add_application_input`**, **`add_application_output`**, **`update_application`** |
| 71 | `elbv2` | Elastic Load Balancing v2 | `create_load_balancer`, `describe_load_balancers`, `delete_load_balancer`, `create_target_group`, `describe_target_groups`, `register_targets`, `deregister_targets`, `describe_target_health`, `create_listener`, `describe_listeners`, `delete_listener`, `create_rule`, `describe_rules`, `modify_rule`, `delete_rule`, `set_rule_priorities`, `modify_load_balancer_attributes`, `modify_target_group_attributes`, `add_tags`, `remove_tags`, `wait_for_load_balancer` + more |
| 72 | `elasticache` | ElastiCache | `create_cache_cluster`, `describe_cache_clusters`, `delete_cache_cluster`, `modify_cache_cluster`, `create_replication_group`, `describe_replication_groups`, `delete_replication_group`, `modify_replication_group`, `create_cache_subnet_group`, `describe_cache_subnet_groups`, `wait_for_cache_cluster`, `wait_for_replication_group` + more |
| 73 | `eks` | Elastic Kubernetes Service | `create_cluster`, `describe_cluster`, `list_clusters`, `delete_cluster`, `update_cluster_config`, `create_nodegroup`, `describe_nodegroup`, `list_nodegroups`, `delete_nodegroup`, `create_fargate_profile`, `list_fargate_profiles`, `describe_fargate_profile`, `delete_fargate_profile`, `wait_for_cluster`, `wait_for_nodegroup` + more |
| 74 | `cloudfront` | CloudFront | `create_distribution`, `get_distribution`, `list_distributions`, `update_distribution`, `delete_distribution`, `create_invalidation`, `get_invalidation`, `list_invalidations`, `wait_for_distribution`, `wait_for_invalidation` + more |
| 75 | `autoscaling` | EC2 Auto Scaling | `create_auto_scaling_group`, `describe_auto_scaling_groups`, `update_auto_scaling_group`, `delete_auto_scaling_group`, `create_launch_configuration`, `describe_launch_configurations`, `set_desired_capacity`, `attach_instances`, `detach_instances`, `put_scaling_policy`, `describe_policies`, `execute_policy`, `wait_for_group_stable` + more |
| 76 | `batch` | AWS Batch | `create_compute_environment`, `describe_compute_environments`, `update_compute_environment`, `delete_compute_environment`, `register_job_definition`, `describe_job_definitions`, `submit_job`, `describe_jobs`, `list_jobs`, `terminate_job`, `create_job_queue`, `describe_job_queues`, `update_job_queue`, `delete_job_queue`, `wait_for_job` + more |
| 77 | `codebuild` | CodeBuild | `create_project`, `batch_get_projects`, `list_projects`, `update_project`, `delete_project`, `start_build`, `batch_get_builds`, `stop_build`, `list_builds_for_project`, `create_report_group`, `list_report_groups`, `wait_for_build` + more |
| 78 | `codepipeline` | CodePipeline | `create_pipeline`, `get_pipeline`, `list_pipelines`, `update_pipeline`, `delete_pipeline`, `start_pipeline_execution`, `get_pipeline_execution`, `list_pipeline_executions`, `get_pipeline_state`, `enable_stage_transition`, `disable_stage_transition`, `put_approval_result`, `wait_for_pipeline_execution` + more |
| 79 | `efs` | Elastic File System | `create_file_system`, `describe_file_systems`, `delete_file_system`, `create_mount_target`, `describe_mount_targets`, `delete_mount_target`, `create_access_point`, `describe_access_points`, `delete_access_point`, `put_file_system_policy`, `describe_file_system_policy`, `put_lifecycle_configuration`, `describe_lifecycle_configuration`, `wait_for_file_system`, `wait_for_mount_target` + more |
| 80 | `config_service` | AWS Config | `put_config_rule`, `describe_config_rules`, `delete_config_rule`, `put_configuration_recorder`, `describe_configuration_recorders`, `start_configuration_recorder`, `stop_configuration_recorder`, `put_delivery_channel`, `describe_delivery_channels`, `get_compliance_details_by_config_rule`, `describe_compliance_by_config_rule`, `put_evaluations`, `start_config_rules_evaluation`, `get_resource_config_history` + more |
| 81 | `ses_v2` | SES v2 | `send_email`, `send_bulk_email`, `create_email_identity`, `get_email_identity`, `list_email_identities`, `delete_email_identity`, `create_email_template`, `get_email_template`, `list_email_templates`, `update_email_template`, `create_contact_list`, `list_contact_lists`, `create_contact`, `list_contacts`, `create_configuration_set`, `list_configuration_sets`, `create_import_job`, `get_message_insights` + more |
| 82 | `dms` | Database Migration Service | `create_replication_instance`, `describe_replication_instances`, `modify_replication_instance`, `delete_replication_instance`, `wait_for_replication_instance`, `create_endpoint`, `describe_endpoints`, `modify_endpoint`, `delete_endpoint`, `test_connection`, `create_replication_task`, `describe_replication_tasks`, `start_replication_task`, `stop_replication_task`, `wait_for_replication_task`, `describe_table_statistics`, `create_replication_subnet_group` + more |
| 83 | `msk` | Managed Streaming for Kafka | `create_cluster`, `describe_cluster`, `list_clusters`, `delete_cluster`, `update_broker_count`, `update_broker_storage`, `list_nodes`, `get_bootstrap_brokers`, `create_configuration`, `describe_configuration`, `list_configurations`, `wait_for_cluster` |
| 84 | `polly` | Amazon Polly | `synthesize_speech`, `describe_voices`, `list_lexicons`, `get_lexicon`, `put_lexicon`, `delete_lexicon`, `start_speech_synthesis_task`, `get_speech_synthesis_task` |
| 85 | `transcribe` | Amazon Transcribe | `start_transcription_job`, `get_transcription_job`, `list_transcription_jobs`, `delete_transcription_job`, `create_vocabulary`, `get_vocabulary`, `list_vocabularies`, `delete_vocabulary`, `wait_for_transcription_job`, `transcribe_and_wait` |
| 86 | `bedrock_agent_runtime` | Bedrock Agent Runtime | `invoke_agent`, `retrieve`, `retrieve_and_generate`, `invoke_flow` |
| 87 | `personalize` | Amazon Personalize | `create_dataset_group`, `describe_dataset_group`, `list_dataset_groups`, `create_dataset`, `describe_dataset`, `create_schema`, `describe_schema`, `create_dataset_import_job`, `describe_dataset_import_job`, `create_solution`, `describe_solution`, `create_solution_version`, `create_campaign`, `describe_campaign`, `list_campaigns` |
| 88 | `personalize_runtime` | Amazon Personalize Runtime | `get_recommendations`, `get_personalized_ranking` |
| 89 | `rds_data` | RDS Data API | `execute_statement`, `batch_execute_statement`, `begin_transaction`, `commit_transaction`, `rollback_transaction`, `execute_sql`, `run_query` |
| 90 | `emr` | Amazon EMR | `run_job_flow`, `describe_cluster`, `list_clusters`, `terminate_job_flows`, `add_job_flow_steps`, `describe_step`, `list_steps`, `set_termination_protection`, `set_visible_to_all_users`, `create_security_configuration`, `list_security_configurations`, `list_instance_groups`, `modify_instance_groups`, `wait_for_cluster`, `wait_for_step` + more |
| 91 | `quicksight` | Amazon QuickSight | `create_data_source`, `describe_data_source`, `list_data_sources`, `delete_data_source`, `update_data_source`, `create_dataset`, `describe_dataset`, `list_datasets`, `delete_dataset`, `create_dashboard`, `describe_dashboard`, `list_dashboards`, `delete_dashboard`, `describe_dashboard_permissions`, `update_dashboard_permissions` + more |
| 92 | `app_runner` | AWS App Runner | `create_service`, `describe_service`, `list_services`, `update_service`, `delete_service`, `pause_service`, `resume_service`, `create_auto_scaling_configuration`, `describe_auto_scaling_configuration`, `list_auto_scaling_configurations`, `delete_auto_scaling_configuration`, `create_connection`, `list_connections`, `delete_connection`, `wait_for_service` |
| 93 | `timestream_write` | Amazon Timestream Write | `create_database`, `describe_database`, `list_databases`, `delete_database`, `update_database`, `create_table`, `describe_table`, `list_tables`, `delete_table`, `update_table`, `write_records` |
| 94 | `timestream_query` | Amazon Timestream Query | `query`, `describe_endpoints` |
| 95 | `transfer` | AWS Transfer Family | `create_server`, `describe_server`, `list_servers`, `update_server`, `delete_server`, `start_server`, `stop_server`, `create_user`, `describe_user`, `list_users`, `update_user`, `delete_user`, `create_connector`, `describe_connector`, `list_connectors`, `delete_connector`, `import_ssh_public_key`, `create_workflow`, `describe_workflow`, `list_workflows`, `delete_workflow`, `wait_for_server` + more |
| 96 | `fsx` | Amazon FSx | `create_file_system`, `describe_file_systems`, `update_file_system`, `delete_file_system`, `create_backup`, `describe_backups`, `delete_backup`, `create_data_repository_association`, `describe_data_repository_associations`, `delete_data_repository_association`, `create_volume`, `describe_volumes`, `delete_volume`, `tag_resource`, `untag_resource`, `wait_for_file_system`, `wait_for_backup` + more |
| 97 | `forecast` | Amazon Forecast | `create_dataset_group`, `describe_dataset_group`, `list_dataset_groups`, `delete_dataset_group`, `create_dataset`, `describe_dataset`, `create_dataset_import_job`, `describe_dataset_import_job`, `create_predictor`, `describe_predictor`, `create_forecast`, `describe_forecast`, `create_forecast_export_job`, `wait_for_predictor`, `wait_for_forecast` + more |
| 98 | `forecast_query` | Amazon Forecast Query | `query_forecast`, `query_what_if_forecast` |
| 99 | `documentdb` | Amazon DocumentDB | `create_db_cluster`, `describe_db_clusters`, `modify_db_cluster`, `delete_db_cluster`, `create_db_instance`, `describe_db_instances`, `modify_db_instance`, `delete_db_instance`, `create_db_cluster_snapshot`, `describe_db_cluster_snapshots`, `create_db_subnet_group`, `describe_db_subnet_groups`, `wait_for_db_cluster`, `wait_for_db_instance` + more |
| 100 | `bedrock_agent` | Bedrock Agent | `create_agent`, `get_agent`, `list_agents`, `update_agent`, `delete_agent`, `prepare_agent`, `create_agent_alias`, `get_agent_alias`, `list_agent_aliases`, `update_agent_alias`, `delete_agent_alias`, `create_knowledge_base`, `get_knowledge_base`, `list_knowledge_bases`, `delete_knowledge_base`, `associate_agent_knowledge_base`, `disassociate_agent_knowledge_base` + more |
| 101 | `connect` | Amazon Connect | `create_instance`, `describe_instance`, `list_instances`, `delete_instance`, `create_user`, `describe_user`, `list_users`, `update_user_identity_info`, `delete_user`, `create_contact_flow`, `describe_contact_flow`, `list_contact_flows`, `create_queue`, `describe_queue`, `list_queues`, `create_routing_profile`, `describe_routing_profile`, `list_routing_profiles`, `start_outbound_voice_contact`, `stop_contact`, `list_phone_numbers` + more |
| 102 | `iot` | IoT Core | `create_thing`, `describe_thing`, `list_things`, `update_thing`, `delete_thing`, `create_thing_group`, `describe_thing_group`, `add_thing_to_thing_group`, `create_policy`, `get_policy`, `attach_policy`, `detach_policy`, `create_topic_rule`, `get_topic_rule`, `list_topic_rules`, `create_job`, `describe_job`, `list_jobs`, `cancel_job`, `create_certificate_from_csr`, `describe_certificate`, `update_certificate`, `delete_certificate` + more |
| 103 | `iot_data` | IoT Data Plane | `publish`, `get_thing_shadow`, `update_thing_shadow`, `delete_thing_shadow`, `list_named_shadows_for_thing`, `get_retained_message`, `list_retained_messages` |
| 104 | `iot_greengrass` | IoT Greengrass V2 | `create_deployment`, `get_deployment`, `list_deployments`, `cancel_deployment`, `create_component_version`, `describe_component`, `list_components`, `delete_component`, `get_core_device`, `list_core_devices`, `list_effective_deployments`, `list_installed_components`, `batch_associate_client_device_with_core_device` |
| 105 | `iot_sitewise` | IoT SiteWise | `create_asset`, `describe_asset`, `list_assets`, `update_asset`, `delete_asset`, `create_asset_model`, `describe_asset_model`, `list_asset_models`, `update_asset_model`, `delete_asset_model`, `associate_assets`, `disassociate_assets`, `put_asset_property_value`, `get_asset_property_value`, `get_asset_property_aggregates`, `get_asset_property_value_history`, `create_portal`, `describe_portal`, `list_portals`, `create_gateway`, `describe_gateway`, `list_gateways` |
| 106 | `memorydb` | Amazon MemoryDB | `create_cluster`, `describe_clusters`, `update_cluster`, `delete_cluster`, `create_snapshot`, `describe_snapshots`, `delete_snapshot`, `copy_snapshot`, `create_subnet_group`, `describe_subnet_groups`, `create_acl`, `describe_acls`, `update_acl`, `delete_acl`, `create_user`, `describe_users`, `update_user`, `delete_user`, `wait_for_cluster` |
| 107 | `codeartifact` | CodeArtifact | `create_domain`, `describe_domain`, `list_domains`, `delete_domain`, `create_repository`, `describe_repository`, `list_repositories`, `delete_repository`, `list_packages`, `describe_package`, `list_package_versions`, `describe_package_version`, `get_authorization_token`, `get_repository_endpoint`, `associate_external_connection`, `disassociate_external_connection` |
| 108 | `codestar_connections` | CodeStar Connections | `create_connection`, `get_connection`, `list_connections`, `delete_connection`, `create_host`, `get_host`, `list_hosts`, `delete_host`, `list_tags_for_resource`, `tag_resource` |
| 109 | `cognito_identity` | Cognito Identity | `create_identity_pool`, `describe_identity_pool`, `list_identity_pools`, `update_identity_pool`, `delete_identity_pool`, `get_id`, `get_credentials_for_identity`, `get_open_id_token_for_developer_identity`, `set_identity_pool_roles`, `get_identity_pool_roles`, `list_identities` |
| 110 | `databrew` | Glue DataBrew | `create_dataset`, `describe_dataset`, `list_datasets`, `delete_dataset`, `update_dataset`, `create_project`, `describe_project`, `list_projects`, `delete_project`, `create_recipe`, `describe_recipe`, `list_recipes`, `create_recipe_job`, `describe_job`, `list_jobs` |
| 111 | `detective` | Amazon Detective | `create_graph`, `list_graphs`, `delete_graph`, `create_members`, `list_members`, `delete_members`, `get_members`, `accept_invitation`, `reject_invitation`, `start_monitoring_member`, `list_invitations`, `list_datasource_packages`, `update_datasource_packages`, `batch_get_graph_member_datasources` |
| 112 | `elastic_beanstalk` | Elastic Beanstalk | `create_application`, `describe_applications`, `delete_application`, `create_environment`, `describe_environments`, `update_environment`, `terminate_environment`, `create_application_version`, `describe_application_versions`, `list_platform_versions`, `describe_configuration_settings`, `rebuild_environment`, `wait_for_environment` |
| 113 | `emr_containers` | EMR on EKS | `create_virtual_cluster`, `describe_virtual_cluster`, `list_virtual_clusters`, `delete_virtual_cluster`, `start_job_run`, `describe_job_run`, `list_job_runs`, `cancel_job_run` |
| 114 | `emr_serverless` | EMR Serverless | `create_application`, `get_application`, `list_applications`, `delete_application`, `start_application`, `stop_application`, `start_job_run`, `get_job_run`, `list_job_runs` |
| 115 | `health` | AWS Health | `describe_events`, `describe_event_details`, `describe_affected_entities`, `describe_event_types`, `describe_event_aggregates`, `describe_entity_aggregates`, `describe_affected_accounts_for_organization`, `describe_events_for_organization` |
| 116 | `inspector` | Amazon Inspector | `create_findings_report`, `list_findings`, `get_findings_report_status`, `list_coverage`, `list_coverage_statistics`, `enable`, `disable`, `batch_get_account_status`, `describe_organization_configuration`, `update_organization_configuration`, `list_members`, `associate_member`, `disassociate_member`, `get_member` |
| 117 | `ivs` | Interactive Video Service | `create_channel`, `get_channel`, `list_channels`, `update_channel`, `delete_channel`, `create_stream_key`, `get_stream_key`, `list_stream_keys`, `delete_stream_key`, `get_stream`, `list_streams`, `stop_stream`, `put_metadata`, `create_recording_configuration`, `list_recording_configurations`, `get_recording_configuration` |
| 118 | `keyspaces` | Amazon Keyspaces | `create_keyspace`, `get_keyspace`, `list_keyspaces`, `delete_keyspace`, `create_table`, `get_table`, `list_tables`, `update_table`, `delete_table`, `restore_table`, `list_tags_for_resource`, `tag_resource` |
| 119 | `lex_models` | Lex V2 Models | `create_bot`, `describe_bot`, `list_bots`, `update_bot`, `delete_bot`, `create_bot_locale`, `describe_bot_locale`, `list_bot_locales`, `create_intent`, `list_intents`, `build_bot_locale`, `create_bot_version` |
| 120 | `lex_runtime` | Lex V2 Runtime | `recognize_text`, `recognize_utterance`, `put_session`, `get_session`, `delete_session` |
| 121 | `lightsail` | Amazon Lightsail | `create_instances`, `get_instance`, `get_instances`, `delete_instance`, `start_instance`, `stop_instance`, `reboot_instance`, `create_instance_snapshot`, `get_instance_snapshots`, `delete_instance_snapshot`, `get_blueprints`, `get_bundles`, `allocate_static_ip`, `release_static_ip`, `attach_static_ip`, `get_static_ip`, `open_instance_public_ports` |
| 122 | `macie` | Amazon Macie | `enable_macie`, `disable_macie`, `get_macie_session`, `create_classification_job`, `describe_classification_job`, `list_classification_jobs`, `create_custom_data_identifier`, `get_custom_data_identifier`, `list_custom_data_identifiers`, `delete_custom_data_identifier`, `list_findings`, `get_findings`, `create_findings_filter`, `get_findings_filter`, `list_findings_filters`, `get_bucket_statistics`, `describe_buckets`, `update_classification_scope` |
| 123 | `mediaconvert` | MediaConvert | `create_job`, `get_job`, `list_jobs`, `cancel_job`, `create_preset`, `get_preset`, `list_presets`, `delete_preset`, `create_job_template`, `get_job_template`, `list_job_templates`, `delete_job_template`, `create_queue`, `describe_endpoints` |
| 124 | `neptune` | Amazon Neptune | `create_db_cluster`, `describe_db_clusters`, `modify_db_cluster`, `delete_db_cluster`, `create_db_instance`, `describe_db_instances`, `modify_db_instance`, `delete_db_instance`, `create_db_cluster_snapshot`, `describe_db_cluster_snapshots`, `wait_for_db_cluster`, `wait_for_db_instance` |
| 125 | `neptune_graph` | Neptune Analytics | `create_graph`, `get_graph`, `list_graphs`, `update_graph`, `delete_graph`, `create_graph_snapshot`, `get_graph_snapshot`, `list_graph_snapshots`, `delete_graph_snapshot`, `wait_for_graph` |
| 126 | `redshift_serverless` | Redshift Serverless | `create_namespace`, `get_namespace`, `list_namespaces`, `delete_namespace`, `update_namespace`, `create_workgroup`, `get_workgroup`, `list_workgroups`, `delete_workgroup`, `update_workgroup` |
| 127 | `sagemaker_featurestore_runtime` | SageMaker Feature Store Runtime | `get_record`, `put_record`, `delete_record`, `batch_get_record` |
| 128 | `sagemaker_runtime` | SageMaker Runtime | `invoke_endpoint`, `invoke_endpoint_async`, `invoke_endpoint_with_response_stream` |
| 129 | `service_quotas` | Service Quotas | `get_service_quota`, `list_service_quotas`, `request_service_quota_increase`, `get_requested_service_quota_change`, `list_requested_service_quota_change_history`, `list_services`, `list_aws_default_service_quotas` |
| 130 | `sso_admin` | IAM Identity Center | `create_permission_set`, `describe_permission_set`, `list_permission_sets`, `delete_permission_set`, `update_permission_set`, `provision_permission_set`, `create_account_assignment`, `list_account_assignments`, `delete_account_assignment`, `attach_managed_policy_to_permission_set`, `list_managed_policies_in_permission_set`, `detach_managed_policy_from_permission_set`, `put_inline_policy_to_permission_set`, `list_instances`, `list_permission_sets_provisioned_to_account`, `list_accounts_for_provisioned_permission_set`, `list_permission_set_provisioning_status`, `create_instance_access_control_attribute_configuration`, `describe_instance_access_control_attribute_configuration`, `describe_account_assignment_creation_status` |
| 131 | `storage_gateway` | Storage Gateway | `activate_gateway`, `describe_gateway_information`, `list_gateways`, `update_gateway_information`, `shutdown_gateway`, `create_nfs_file_share`, `describe_nfs_file_shares`, `update_nfs_file_share`, `list_file_shares`, `create_cached_iscsi_volume`, `describe_cached_iscsi_volumes`, `list_volumes`, `add_cache`, `describe_cache` |
| 132 | `vpc_lattice` | VPC Lattice | `create_service_network`, `get_service_network`, `list_service_networks`, `delete_service_network`, `create_service`, `get_service`, `list_services`, `delete_service`, `create_target_group`, `get_target_group`, `list_target_groups`, `delete_target_group`, `register_targets`, `deregister_targets`, `create_listener`, `list_listeners` |
| 133 | `ai_ml_pipelines` | SageMaker + Bedrock *(multi-service)* | Multi-service ML pipeline orchestration |
| 134 | `infra_automation` | CloudFormation + EC2 + SSM *(multi-service)* | Multi-service infrastructure automation |
| 135 | `messaging` | SNS + SQS + SES *(multi-service)* | Multi-service messaging patterns |

---

## Native Async (`aws_util.aio`)

Every module above has a native async counterpart under `aws_util.aio`. The async package uses a custom engine (`aws_util.aio._engine`) built on **aiohttp** for true non-blocking HTTP, with **botocore** handling only serialization and request signing. The engine includes built-in circuit breaking, adaptive retry, and connection pooling.

```python
from aws_util.aio.s3 import upload_object, download_object
from aws_util.aio.dynamodb import put_item, get_item
from aws_util.aio.messaging import multi_channel_notifier
from aws_util.aio.resilience import circuit_breaker, retry_with_backoff

# All functions are native async -- no thread pool wrappers
result = await upload_object("my-bucket", "key.txt", b"data")
```

Key features:

- **Same signatures and return types** as the sync modules -- Pydantic models are imported directly from the sync layer.
- **`AsyncClient.call(operation, **params)`** for single API calls.
- **`AsyncClient.paginate(operation, result_key, ...)`** for auto-pagination.
- **`AsyncClient.wait_until(operation, check_fn, ...)`** for polling waiters.
- Decorator factories (e.g. `idempotent_handler`, `retry_with_backoff`, `cold_start_tracker`) return async wrappers that use `asyncio.sleep` and `asyncio.wait_for`.
- Pure-compute functions (e.g. `parse_event`, `lambda_response`, `emit_emf_metric`) are re-exported directly from the sync module.

---

## Placeholder Resolution

```python
from aws_util import retrieve

db_host     = retrieve("${ssm:/myapp/db/host}")
api_key     = retrieve("${secret:myapp/api-key}")
db_password = retrieve("${secret:myapp/db-credentials:password}")
conn        = retrieve("host=${ssm:/myapp/db/host} port=5432")
retrieve(42)  # → 42  (non-strings pass through unchanged)
```

```python
from aws_util import clear_ssm_cache, clear_secret_cache, clear_all_caches
clear_all_caches()
```

---

## Parameter Store

```python
from aws_util.parameter_store import (
    get_parameter, put_parameter, delete_parameter,
    get_parameters_by_path, get_parameters_batch,
)

value = get_parameter("/myapp/prod/db/host")
put_parameter("/myapp/prod/db/host", "db.internal", description="DB host")

# Load all parameters under a path prefix as a flat dict
params = get_parameters_by_path("/myapp/prod/")
print(params["db/host"], params["db/port"])

# Fetch a specific list of parameters in one request (auto-chunks at 10)
values = get_parameters_batch(["/myapp/prod/db/host", "/myapp/prod/db/port"])

delete_parameter("/myapp/prod/db/host")
```

---

## Secrets Manager

```python
from aws_util.secrets_manager import (
    get_secret, create_secret, update_secret, delete_secret,
    list_secrets, rotate_secret,
    batch_get_secret_value, cancel_rotate_secret, describe_secret,
    get_random_password, get_resource_policy, list_secret_version_ids,
    put_resource_policy, put_secret_value, remove_regions_from_replication,
    replicate_secret_to_regions, restore_secret, tag_resource,
    untag_resource, update_secret_version_stage, validate_resource_policy,
)

# Fetch whole secret or a single JSON key
raw   = get_secret("myapp/db-credentials")
passw = get_secret("myapp/db-credentials:password")

arn = create_secret(
    "myapp/db-credentials",
    value={"username": "admin", "password": "s3cr3t"},
    description="App DB credentials",
    tags={"env": "prod"},
)

update_secret("myapp/db-credentials", {"username": "admin", "password": "newpass"})

# List secrets whose name starts with a prefix
secrets = list_secrets(name_prefix="myapp/")
for s in secrets:
    print(s["name"], s["arn"])

# Trigger immediate rotation (Lambda must already be configured)
rotate_secret("myapp/db-credentials")

# Soft delete with 14-day recovery window
delete_secret("myapp/db-credentials", recovery_window_in_days=14)

# Batch retrieve multiple secrets at once
batch = batch_get_secret_value(["myapp/db-credentials", "myapp/api-key"])
for entry in batch:
    print(entry.name, entry.secret_string)

# Describe secret metadata (no value)
info = describe_secret("myapp/db-credentials")
print(info.rotation_enabled, info.last_changed_date)

# Generate a random password
pwd = get_random_password(password_length=40, exclude_punctuation=True)
print(pwd.random_password)

# Put a new version of a secret value
version_id = put_secret_value("myapp/db-credentials", secret_string="new-pass")

# Tag and untag secrets
tag_resource("myapp/db-credentials", {"team": "backend", "cost-center": "eng"})
untag_resource("myapp/db-credentials", ["cost-center"])

# List all versions of a secret
versions = list_secret_version_ids("myapp/db-credentials")
for v in versions:
    print(v.version_id, v.version_stages)

# Move a staging label between versions
update_secret_version_stage(
    "myapp/db-credentials", "AWSCURRENT",
    move_to_version_id="new-v", remove_from_version_id="old-v",
)

# Cancel a pending rotation
cancel_rotate_secret("myapp/db-credentials")

# Restore a deleted secret
restore_secret("myapp/db-credentials")

# Resource policy management
put_resource_policy("myapp/db-credentials", {"Version": "2012-10-17", "Statement": []})
policy = get_resource_policy("myapp/db-credentials")
result = validate_resource_policy({"Version": "2012-10-17", "Statement": []})
print(result.policy_validation_passed)

# Replication
replicate_secret_to_regions("myapp/db-credentials", [{"Region": "eu-west-1"}])
remove_regions_from_replication("myapp/db-credentials", ["eu-west-1"])
```

---

## S3

```python
from aws_util.s3 import (
    upload_file, upload_bytes, download_file, download_bytes,
    list_objects, object_exists, delete_object, copy_object, presigned_url,
    delete_prefix, move_object, batch_copy, download_as_text, get_object_metadata,
)

upload_file("bucket", "reports/q1.csv", "/tmp/q1.csv")
upload_bytes("bucket", "data.json", b'{"k":1}')
data = download_bytes("bucket", "data.json")
objects = list_objects("bucket", prefix="reports/")
url = presigned_url("bucket", "reports/q1.csv", expires_in=3600)
print(url.url)

# Delete everything under a prefix (batched automatically)
deleted = delete_prefix("bucket", "reports/2023/")
print(f"{deleted} objects removed")

# Atomic move (copy + delete)
move_object("src-bucket", "old/path/file.csv", "dst-bucket", "new/path/file.csv")

# Concurrent multi-object copy
batch_copy([
    {"src_bucket": "src", "src_key": "a.csv", "dst_bucket": "dst", "dst_key": "a.csv"},
    {"src_bucket": "src", "src_key": "b.csv", "dst_bucket": "dst", "dst_key": "b.csv"},
])

# Download a text file directly as a string
content = download_as_text("bucket", "config/settings.json")

# HEAD request — no body download
meta = get_object_metadata("bucket", "reports/q1.csv")
print(meta["ContentLength"], meta["LastModified"])
```

---

## DynamoDB

```python
from aws_util.dynamodb import DynamoKey, get_item, put_item, update_item, query, scan, batch_get
from boto3.dynamodb.conditions import Key, Attr

key = DynamoKey(partition_key="pk", partition_value="user#1")
item = get_item("Users", key)
put_item("Users", {"pk": "user#1", "name": "Alice"})
update_item("Users", key, {"name": "Alicia"})
items = query("Orders", Key("pk").eq("user#1"), scan_index_forward=False)
```

---

## SQS

```python
from aws_util.sqs import (
    get_queue_url, send_message, receive_messages, delete_message,
    send_large_batch, drain_queue, replay_dlq, wait_for_message,
    get_queue_attributes, create_queue, delete_queue, list_queues,
    set_queue_attributes, add_permission, remove_permission,
    tag_queue, untag_queue, list_queue_tags,
    change_message_visibility, change_message_visibility_batch,
    list_dead_letter_source_queues,
    start_message_move_task, cancel_message_move_task,
    list_message_move_tasks,
)

# Queue lifecycle
queue_url = create_queue("my-queue", attributes={"VisibilityTimeout": "60"})
urls = list_queues(prefix="my-")
set_queue_attributes(queue_url, {"DelaySeconds": "5"})
delete_queue(queue_url)

url = get_queue_url("my-queue")
send_message(url, {"order_id": "abc"})
messages = receive_messages(url, max_number=10, wait_seconds=20)
for m in messages:
    print(m.body_as_json())
    delete_message(url, m.receipt_handle)

# Change visibility timeout for a received message
change_message_visibility(url, messages[0].receipt_handle, visibility_timeout=120)

# Send any number of messages — automatically split into batches of 10
total = send_large_batch(url, [{"n": i} for i in range(50)])

# Process and delete every message in a queue (handler failures are logged)
def handle(msg):
    print(msg.body_as_json())

processed = drain_queue(url, handler=handle, batch_size=10)

# Move all DLQ messages back to the source queue (preserves MessageAttributes)
moved = replay_dlq(dlq_url="https://sqs.../my-queue-dlq", target_url=url)

# Block until a matching message arrives (or timeout).
# Note: non-matching messages remain invisible for the visibility timeout
# duration and may delay other consumers.
msg = wait_for_message(
    url,
    predicate=lambda m: m.body_as_json().get("type") == "order_placed",
    timeout=30.0,
)

# Fetch queue attributes (message count, ARN, etc.)
attrs = get_queue_attributes(url)
print(attrs["ApproximateNumberOfMessages"])

# Permissions
add_permission(url, "allow-account", ["123456789012"], ["SendMessage"])
remove_permission(url, "allow-account")

# Tags
tag_queue(url, {"env": "prod", "team": "backend"})
tags = list_queue_tags(url)
untag_queue(url, ["team"])

# Dead-letter queue helpers
source_queues = list_dead_letter_source_queues(dlq_url)

# Message move tasks (redrive)
result = start_message_move_task("arn:aws:sqs:...:my-dlq")
tasks = list_message_move_tasks("arn:aws:sqs:...:my-dlq")
cancel_message_move_task(result.task_handle)
```

---

## SNS

```python
from aws_util.sns import (
    publish, publish_batch, publish_fan_out, create_topic_if_not_exists,
    create_topic, delete_topic, get_topic_attributes, set_topic_attributes,
    list_topics, subscribe, unsubscribe, confirm_subscription,
    get_subscription_attributes, set_subscription_attributes,
    list_subscriptions, list_subscriptions_by_topic,
    add_permission, remove_permission,
    tag_resource, untag_resource, list_tags_for_resource,
    create_platform_application, delete_platform_application,
    get_platform_application_attributes, set_platform_application_attributes,
    list_platform_applications,
    create_platform_endpoint, delete_endpoint,
    get_endpoint_attributes, set_endpoint_attributes,
    list_endpoints_by_platform_application,
    check_if_phone_number_is_opted_out, opt_in_phone_number,
    list_phone_numbers_opted_out,
    get_sms_attributes, set_sms_attributes, list_origination_numbers,
    create_sms_sandbox_phone_number, delete_sms_sandbox_phone_number,
    verify_sms_sandbox_phone_number, list_sms_sandbox_phone_numbers,
    get_sms_sandbox_account_status,
    get_data_protection_policy, put_data_protection_policy,
    FanOutFailure,
)

# --- Topic management ---
arn = create_topic("my-topic", attributes={"DisplayName": "My Topic"})
delete_topic(arn)
attrs = get_topic_attributes(arn)
set_topic_attributes(arn, "DisplayName", "New Name")
all_arns = list_topics()

# Idempotent topic creation (fifo=True always sets FifoTopic: "true")
arn = create_topic_if_not_exists("my-notifications")

# --- Publishing ---
result = publish("arn:aws:sns:...:my-topic", {"event": "user_signup"})
publish_batch("arn:aws:sns:...:my-topic", [{"a": 1}, {"b": 2}])

# Fan-out: publish the same event to multiple topics concurrently.
publish_fan_out(
    ["arn:aws:sns:...:topic-a", "arn:aws:sns:...:topic-b"],
    {"event": "deploy_complete"},
    max_concurrency=10,
)

# --- Subscriptions ---
sub_arn = subscribe(arn, "sqs", "arn:aws:sqs:...:my-queue")
unsubscribe(sub_arn)
sub_attrs = get_subscription_attributes(sub_arn)
set_subscription_attributes(sub_arn, "RawMessageDelivery", "true")
subs = list_subscriptions()
topic_subs = list_subscriptions_by_topic(arn)

# --- Permissions & tagging ---
add_permission(arn, "allow-publish", ["123456789012"], ["Publish"])
remove_permission(arn, "allow-publish")
tag_resource(arn, [{"Key": "env", "Value": "prod"}])
tags = list_tags_for_resource(arn)
untag_resource(arn, ["env"])

# --- Platform applications & endpoints (push notifications) ---
pa_arn = create_platform_application("my-app", "GCM", {"PlatformCredential": "key"})
ep_arn = create_platform_endpoint(pa_arn, "device-token")
get_endpoint_attributes(ep_arn)
set_endpoint_attributes(ep_arn, {"Enabled": "true"})
list_endpoints_by_platform_application(pa_arn)
delete_endpoint(ep_arn)
delete_platform_application(pa_arn)

# --- SMS ---
opted_out = check_if_phone_number_is_opted_out("+12065551234")
opt_in_phone_number("+12065551234")
numbers = list_phone_numbers_opted_out()
sms_attrs = get_sms_attributes()
set_sms_attributes({"DefaultSMSType": "Transactional"})

# --- SMS Sandbox ---
in_sandbox = get_sms_sandbox_account_status()

# --- Data protection policy ---
policy = get_data_protection_policy(arn)
put_data_protection_policy(arn, '{"Statement": []}')
```

---

## Lambda

```python
from aws_util.lambda_ import invoke, invoke_async

result = invoke("my-function", {"key": "value"})
if result.succeeded:
    print(result.payload)
invoke_async("my-function", {"key": "value"})
```

---

## CloudWatch

```python
from aws_util.cloudwatch import MetricDimension, put_metric, LogEvent, put_log_events

put_metric("MyApp", "Latency", 120.5, "Milliseconds",
           dimensions=[MetricDimension(name="Endpoint", value="/api")])

put_log_events("/myapp", "2024-01-01", [LogEvent.now("request received")])
```

---

## STS

```python
from aws_util.sts import get_caller_identity, assume_role, assume_role_session

identity = get_caller_identity()
print(identity.account_id)

creds = assume_role("arn:aws:iam::123456789012:role/MyRole", "session")

# Get a boto3 Session under an assumed role — ready to create service clients
session = assume_role_session("arn:aws:iam::999999999999:role/CrossAccountRole", "audit")
s3 = session.client("s3")
```

---

## EventBridge

```python
from aws_util.eventbridge import put_event, put_events, put_events_chunked, list_rules, EventEntry, PutEventsResult

result = put_event("com.myapp.orders", "Order Placed", {"order_id": "ord_001"})

# put_events returns a PutEventsResult on partial failures (raises only when ALL fail)
result = put_events([EventEntry(source="com.myapp", detail_type="Tick", detail={"n": 1})])
print(result.successful_count, result.failed_count)

# Publish > 10 events automatically chunked into batches of 10
events = [EventEntry(source="com.myapp", detail_type="Tick", detail={"n": i}) for i in range(35)]
put_events_chunked(events)

# List all rules on the default bus
rules = list_rules()
for rule in rules:
    print(rule["Name"], rule["State"])
```

---

## KMS

```python
from aws_util.kms import encrypt, decrypt, generate_data_key, \
    envelope_encrypt, envelope_decrypt, re_encrypt

result = encrypt("alias/my-key", "sensitive-value")
plaintext = decrypt(result.ciphertext_blob)

data_key = generate_data_key("alias/my-key")
# use data_key.plaintext locally, store data_key.ciphertext_blob

# Envelope encryption (AES-GCM + KMS-wrapped key)
payload = envelope_encrypt("alias/my-key", b"secret data")
# store payload["ciphertext"] and payload["encrypted_data_key"] together
original = envelope_decrypt(payload["ciphertext"], payload["encrypted_data_key"])

# Key rotation: move ciphertext to a new key without exposing the plaintext
rotated = re_encrypt(result.ciphertext_blob, destination_key_id="alias/my-new-key")
print(rotated.key_id)  # new key ARN
```

---

## EC2

```python
from aws_util.ec2 import describe_instances, start_instances, stop_instances, create_image

instances = describe_instances(filters=[{"Name": "instance-state-name", "Values": ["running"]}])
for inst in instances:
    print(inst.instance_id, inst.instance_type, inst.state)

stop_instances(["i-1234567890abcdef0"])
ami_id = create_image("i-1234567890abcdef0", "my-backup-ami")
```

---

## RDS

```python
from aws_util.rds import describe_db_instances, start_db_instance, create_db_snapshot

instances = describe_db_instances()
start_db_instance("my-db")
snapshot = create_db_snapshot("my-db", "my-db-snapshot-2024")
```

---

## ECS

```python
from aws_util.ecs import run_task, describe_services, update_service

tasks = run_task("my-cluster", "my-task:5", subnets=["subnet-abc"], security_groups=["sg-xyz"])
services = describe_services("my-cluster", ["my-service"])
update_service("my-cluster", "my-service", desired_count=3)
```

---

## ECR

```python
from aws_util.ecr import get_auth_token, list_repositories, list_images, \
    ensure_repository, get_latest_image_tag

tokens = get_auth_token()
print(tokens[0].endpoint, tokens[0].username)

repos = list_repositories()
images = list_images("my-repo")

# Idempotent — creates the repo only if it doesn't exist
repo = ensure_repository("my-app", image_tag_mutability="IMMUTABLE", scan_on_push=True)
print(repo.repository_uri)

# Find the most recently pushed tag
tag = get_latest_image_tag("my-app")
print(tag)  # e.g. "v1.4.2"
```

---

## IAM

```python
from aws_util.iam import create_role, attach_role_policy, list_roles, \
    create_role_with_policies, ensure_role

role = create_role("MyLambdaRole", {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"},
                   "Action": "sts:AssumeRole"}]
})
attach_role_policy(role.role_name, "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")

# Create a role and attach multiple managed + inline policies in one call
role = create_role_with_policies(
    "MyAppRole",
    trust_policy={
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"},
                       "Action": "sts:AssumeRole"}],
    },
    managed_policy_arns=["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"],
    inline_policies={
        "AllowSQS": {
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Action": "sqs:*", "Resource": "*"}],
        }
    },
)

# Idempotent — creates the role only if it doesn't already exist
role, created = ensure_role(
    "MyAppRole",
    trust_policy={"Version": "2012-10-17", "Statement": [...]},
    managed_policy_arns=["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"],
)
```

---

## Cognito

```python
from aws_util.cognito import admin_create_user, admin_get_user, list_users, \
    admin_initiate_auth, get_or_create_user, bulk_create_users, reset_user_password

user = admin_create_user("us-east-1_abc123", "alice", attributes={"email": "alice@example.com"})
admin_set_user_password("us-east-1_abc123", "alice", "MyP@ssword1!", permanent=True)
auth = admin_initiate_auth("us-east-1_abc123", "client-id", "alice", "MyP@ssword1!")
print(auth.access_token)

# Idempotent — returns existing user or creates a new one
user, created = get_or_create_user(
    "us-east-1_abc123", "bob",
    attributes={"email": "bob@example.com"},
    temp_password="TempP@ss1!",
)

# Create multiple users in one call
users = bulk_create_users("us-east-1_abc123", [
    {"username": "carol", "attributes": {"email": "carol@example.com"}},
    {"username": "dave",  "attributes": {"email": "dave@example.com"}, "temp_password": "TempP@ss2!"},
])

# Trigger a password-reset email/SMS for a user
reset_user_password("us-east-1_abc123", "alice")
```

---

## Route 53

```python
from aws_util.route53 import list_hosted_zones, upsert_record, delete_record, \
    wait_for_change, bulk_upsert_records

zones = list_hosted_zones()
change_id = upsert_record("Z1234567890", "api.example.com", "A", ["1.2.3.4"])

# Wait for the DNS change to fully propagate (INSYNC)
wait_for_change(change_id, timeout=300)

# Upsert multiple records in a single API call
change_id = bulk_upsert_records("Z1234567890", [
    {"name": "api.example.com",  "record_type": "A",     "values": ["1.2.3.4"],         "ttl": 300},
    {"name": "www.example.com",  "record_type": "CNAME", "values": ["api.example.com"], "ttl": 60},
    {"name": "mail.example.com", "record_type": "MX",    "values": ["10 mail.example.com"]},
])
wait_for_change(change_id)
```

---

## ACM

```python
from aws_util.acm import (
    list_certificates, request_certificate, describe_certificate,
    wait_for_certificate, find_certificate_by_domain, ACMTag,
    add_tags_to_certificate, remove_tags_from_certificate,
    list_tags_for_certificate, get_certificate, export_certificate,
    import_certificate, renew_certificate, resend_validation_email,
    update_certificate_options, get_account_configuration,
    put_account_configuration,
)

certs = list_certificates(status_filter=["ISSUED"])
arn = request_certificate("api.example.com", subject_alternative_names=["www.example.com"])
cert = describe_certificate(arn)
print(cert.status, cert.not_after)

# Wait for DNS validation to complete
issued_cert = wait_for_certificate(arn, timeout=600)
print(issued_cert.status)  # "ISSUED"

# Look up a cert by domain without knowing its ARN
cert = find_certificate_by_domain("api.example.com")

# Tag management
add_tags_to_certificate(arn, [ACMTag(key="env", value="prod")])
tags = list_tags_for_certificate(arn)
remove_tags_from_certificate(arn, [ACMTag(key="env", value="prod")])

# Get certificate with chain
detail = get_certificate(arn)
print(detail.certificate, detail.certificate_chain)

# Import a third-party certificate
imported_arn = import_certificate(
    certificate=b"PEM_CERT", private_key=b"PEM_KEY",
    certificate_chain=b"PEM_CHAIN",
)

# Update certificate transparency logging
update_certificate_options(arn, logging_preference="ENABLED")

# Account-level configuration
put_account_configuration("my-token", days_before_expiry=30)
config = get_account_configuration()
```

---

## Step Functions

```python
from aws_util.stepfunctions import start_execution, wait_for_execution, \
    run_and_wait, get_execution_history

execution = start_execution("arn:aws:states:...:stateMachine:MyMachine", {"order_id": "abc"})
result = wait_for_execution(execution.execution_arn, timeout=300)
if result.succeeded:
    print(result.output)

# One-liner: start + wait
result = run_and_wait(
    "arn:aws:states:...:stateMachine:MyMachine",
    input_data={"order_id": "abc"},
    timeout=300,
)
if result.succeeded:
    print(result.output)

# Inspect every state transition and error for debugging
events = get_execution_history(result.execution_arn)
for event in events:
    print(event["type"], event.get("timestamp"))
```

---

## CloudFormation

```python
from aws_util.cloudformation import create_stack, wait_for_stack, get_stack_outputs, \
    deploy_stack, get_export_value

create_stack("my-stack", template_body=my_template, capabilities=["CAPABILITY_IAM"])
stack = wait_for_stack("my-stack")
if stack.is_healthy:
    outputs = get_stack_outputs("my-stack")
    print(outputs["ApiEndpoint"])

# Create or update a stack and wait — handles both cases automatically
stack = deploy_stack(
    "my-stack",
    template_body=my_template,
    parameters={"Env": "prod"},
    capabilities=["CAPABILITY_IAM"],
    timeout=900,
)
print(stack.status)  # "CREATE_COMPLETE" or "UPDATE_COMPLETE"

# Retrieve a cross-stack export value by its Export.Name
vpc_id = get_export_value("my-network-stack-VpcId")
```

---

## Kinesis

```python
from aws_util.kinesis import (
    put_record, put_records, get_records, consume_stream,
    create_stream, delete_stream, list_streams, describe_stream,
    describe_stream_summary, list_shards, get_shard_iterator,
    add_tags_to_stream, remove_tags_from_stream, list_tags_for_stream,
    increase_stream_retention_period, decrease_stream_retention_period,
    merge_shards, split_shard,
    start_stream_encryption, stop_stream_encryption,
    enable_enhanced_monitoring, disable_enhanced_monitoring,
    update_shard_count, update_stream_mode,
    register_stream_consumer, deregister_stream_consumer,
    describe_stream_consumer, list_stream_consumers,
    describe_limits, subscribe_to_shard,
    put_resource_policy, get_resource_policy, delete_resource_policy,
)

# --- Stream lifecycle ---
create_stream("my-stream", shard_count=2)
create_stream("on-demand-stream", stream_mode="ON_DEMAND")
delete_stream("old-stream", enforce_consumer_deletion=True)

# --- Put / get records ---
put_record("my-stream", {"event": "click", "user": "u1"}, partition_key="u1")
put_records("my-stream", [
    {"data": {"event": "view"}, "partition_key": "u2"},
    {"data": {"event": "buy"},  "partition_key": "u3"},
])
records = get_records("my-stream", "shardId-000000000000", limit=50)

# --- Stream info ---
info = describe_stream("my-stream")           # returns KinesisStream model
summary = describe_stream_summary("my-stream") # raw dict
streams = list_streams()
shards = list_shards("my-stream")
limits = describe_limits()

# --- Shard iterator ---
iterator = get_shard_iterator("my-stream", "shardId-000000000000")

# --- Tagging ---
add_tags_to_stream("my-stream", {"env": "prod", "team": "data"})
tags = list_tags_for_stream("my-stream")
remove_tags_from_stream("my-stream", ["env"])

# --- Retention ---
increase_stream_retention_period("my-stream", 168)
decrease_stream_retention_period("my-stream", 24)

# --- Shard management ---
update_shard_count("my-stream", target_shard_count=4)
split_shard("my-stream", "shardId-000", "170141183460469231731687303715884105728")
merge_shards("my-stream", "shardId-000", "shardId-001")

# --- Encryption ---
start_stream_encryption("my-stream", key_id="alias/aws/kinesis")
stop_stream_encryption("my-stream")

# --- Enhanced monitoring ---
enable_enhanced_monitoring("my-stream", ["ALL"])
disable_enhanced_monitoring("my-stream", ["ALL"])

# --- Stream mode ---
update_stream_mode("arn:aws:kinesis:us-east-1:123:stream/my-stream", "ON_DEMAND")

# --- Enhanced fan-out consumers ---
consumer = register_stream_consumer(
    "arn:aws:kinesis:us-east-1:123:stream/my-stream", "my-consumer"
)
consumers = list_stream_consumers("arn:aws:kinesis:us-east-1:123:stream/my-stream")
desc = describe_stream_consumer(consumer_arn=consumer.consumer_arn)
deregister_stream_consumer(consumer_arn=consumer.consumer_arn)

# --- Resource policies ---
put_resource_policy("arn:aws:kinesis:...", '{"Version":"2012-10-17","Statement":[]}')
policy = get_resource_policy("arn:aws:kinesis:...")
delete_resource_policy("arn:aws:kinesis:...")

# --- Consume all shards concurrently ---
def handle(record):
    print(record["partition_key"], record["data"])

total = consume_stream(
    "my-stream",
    handler=handle,
    shard_iterator_type="TRIM_HORIZON",
    duration_seconds=60,
)
print(f"Processed {total} records")
```

---

## Firehose

```python
from aws_util.firehose import put_record, put_record_batch, put_record_batch_with_retry

put_record("my-delivery-stream", {"event": "pageview"})
put_record_batch("my-delivery-stream", [{"a": 1}, {"b": 2}, {"c": 3}])

# Automatic retry for throttled/failed records
delivered = put_record_batch_with_retry(
    "my-delivery-stream",
    large_list_of_records,
    max_retries=3,
)
print(f"{delivered} records delivered")
```

---

## SES

```python
from aws_util.ses import send_email, send_templated_email, send_with_attachment, send_bulk

result = send_email(
    from_address="no-reply@example.com",
    to_addresses=["user@example.com"],
    subject="Welcome!",
    body_html="<h1>Hello</h1>",
    body_text="Hello",
)
print(result.message_id)

send_templated_email("no-reply@example.com", ["user@example.com"],
                     "WelcomeTemplate", {"name": "Alice"})

# Email with attachment
with open("report.pdf", "rb") as f:
    send_with_attachment(
        from_address="no-reply@example.com",
        to_addresses=["user@example.com"],
        subject="Monthly Report",
        body_text="Please find the report attached.",
        attachments=[{"filename": "report.pdf", "data": f.read(), "mimetype": "application/pdf"}],
    )

# Bulk send
send_bulk("no-reply@example.com", [
    {"to_addresses": ["a@example.com"], "subject": "Hi A", "body_text": "Hello A"},
    {"to_addresses": ["b@example.com"], "subject": "Hi B", "body_text": "Hello B"},
])
```

---

## Glue

```python
from aws_util.glue import start_job_run, wait_for_job_run, run_job_and_wait, stop_job_run

run_id = start_job_run("my-etl-job", arguments={"--input": "s3://bucket/input/"})
run = wait_for_job_run("my-etl-job", run_id, timeout=3600)
if run.succeeded:
    print(f"Completed in {run.execution_time}s")

# One-liner: start + wait
run = run_job_and_wait("my-etl-job", arguments={"--date": "2024-01-01"})

# Stop a running job
stop_job_run("my-etl-job", run_id)
```

---

## Athena

```python
from aws_util.athena import run_query, get_table_schema, run_ddl

rows = run_query(
    query="SELECT * FROM orders WHERE status = 'PENDING' LIMIT 100",
    database="my_database",
    output_location="s3://my-bucket/athena-results/",
)
for row in rows:
    print(row["order_id"], row["amount"])

# Inspect a table's columns
schema = get_table_schema("my_database", "orders", "s3://my-bucket/athena-results/")
for col in schema:
    print(col["name"], col["type"])

# Execute DDL
run_ddl("CREATE TABLE IF NOT EXISTS logs (ts STRING, msg STRING)",
        database="my_database", output_location="s3://my-bucket/athena-results/")
```

---

## Bedrock

```python
from aws_util.bedrock import invoke_claude, invoke_titan_text, list_foundation_models, \
    chat, embed_text, stream_invoke_claude

response = invoke_claude("Summarise this document in 3 bullet points: ...")
print(response)

titan_response = invoke_titan_text("What is machine learning?")

models = list_foundation_models(provider_name="Anthropic")

# Multi-turn conversation
reply = chat([
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "Paris."},
    {"role": "user", "content": "And the population?"},
])

# Generate embeddings (Titan)
vector = embed_text("the quick brown fox")  # returns list[float]

# Streaming response
for chunk in stream_invoke_claude("Write a short poem about clouds."):
    print(chunk, end="", flush=True)
```

---

## Rekognition

```python
from aws_util.rekognition import detect_labels, detect_faces, detect_text, compare_faces, \
    create_collection, index_face, search_face_by_image, delete_collection, ensure_collection

with open("photo.jpg", "rb") as f:
    image_bytes = f.read()

labels = detect_labels(image_bytes, min_confidence=80.0)
faces  = detect_faces(image_bytes, attributes=["ALL"])
texts  = detect_text(image_bytes)
matches = compare_faces(source_bytes, target_bytes, similarity_threshold=90.0)

# Face collection (1:N search)
create_collection("employees")
face_id = index_face("employees", image_bytes=image_bytes, external_image_id="emp_001")
results = search_face_by_image("employees", image_bytes=query_bytes, max_faces=3)
for r in results:
    print(r["external_image_id"], r["similarity"])
delete_collection("employees")

# Idempotent — creates the collection only if it doesn't already exist
arn, created = ensure_collection("employees")
print(f"Collection {'created' if created else 'already exists'}: {arn}")
```

---

## Textract

```python
from aws_util.textract import detect_document_text, analyze_document, \
    start_document_text_detection, wait_for_document_text_detection, \
    extract_text, extract_tables, extract_form_fields, extract_all

# Synchronous (single page)
with open("invoice.pdf", "rb") as f:
    doc_bytes = f.read()

# Plain text extraction
text = extract_text(document_bytes=doc_bytes)

# Tables as nested lists
tables = extract_tables(document_bytes=doc_bytes)
for table in tables:
    for row in table:
        print(row)

# Form key-value pairs
fields = extract_form_fields(document_bytes=doc_bytes)

# Everything in one call
result = extract_all(document_bytes=doc_bytes)
print(result["text"])
print(result["tables"])
print(result["form_fields"])

# Async (multi-page PDF in S3)
job_id = start_document_text_detection("my-bucket", "docs/report.pdf")
job_result = wait_for_document_text_detection(job_id, timeout=300)
words = [b.text for b in job_result.blocks if b.block_type == "WORD"]
```

---

## Comprehend

```python
from aws_util.comprehend import (
    detect_sentiment, detect_entities, detect_key_phrases,
    detect_dominant_language, detect_pii_entities,
    analyze_text, redact_pii, batch_detect_sentiment,
)

sentiment = detect_sentiment("I love this product!", language_code="en")
print(sentiment.sentiment, sentiment.positive)

entities = detect_entities("Jeff Bezos founded Amazon in Seattle.")
for e in entities:
    print(e.entity_type, e.text)

language = detect_dominant_language("Bonjour tout le monde")
print(language.language_code)  # "fr"

# All analyses in one parallel call
analysis = analyze_text("AWS is amazing! Jeff Bezos founded it. My SSN is 123-45-6789.")
print(analysis["sentiment"].sentiment)
print([e.text for e in analysis["entities"]])
print([p.pii_type for p in analysis["pii_entities"]])

# Redact PII from text
clean = redact_pii("Call me at 555-1234 or email bob@example.com")
# → "Call me at [REDACTED] or email [REDACTED]"

# Batch sentiment — up to 25 texts in one API call
results = batch_detect_sentiment([
    "The product is excellent!",
    "Terrible experience, very disappointing.",
    "It's okay, nothing special.",
])
for r in results:
    print(r.sentiment, r.positive)
```

---

## Translate

```python
from aws_util.translate import translate_text, list_languages, translate_batch

result = translate_text("Hello, world!", target_language_code="es")
print(result.translated_text)   # "¡Hola, mundo!"
print(result.source_language_code)  # "en" (auto-detected)

languages = list_languages()

# Translate a list of strings concurrently
results = translate_batch(
    ["Hello", "Good morning", "Thank you"],
    target_language_code="de",
)
for r in results:
    print(r.translated_text)
```

---

## Security Hub

```python
from aws_util.security_hub import (
    enable_security_hub, describe_hub, get_findings, update_findings,
    describe_standards, batch_enable_standards, list_members,
)

# Enable Security Hub with default standards
hub_arn = enable_security_hub()

# Describe hub configuration
hub = describe_hub()
print(hub.hub_arn, hub.auto_enable_controls)

# Retrieve high-severity findings
findings = get_findings(
    filters={"SeverityLabel": [{"Value": "HIGH", "Comparison": "EQUALS"}]},
)
for f in findings:
    print(f.title, f.severity_label, f.workflow_status)

# Resolve a finding
update_findings(
    [{"Id": f.finding_id, "ProductArn": f.product_arn}],
    workflow={"Status": "RESOLVED"},
    note={"Text": "Fixed in v2.1", "UpdatedBy": "security-team"},
)

# List available standards
standards = describe_standards()
for s in standards:
    print(s.name, s.standards_arn)
```

---

## CodeDeploy

```python
from aws_util.codedeploy import (
    create_application, get_application, list_applications, delete_application,
    create_deployment_group, get_deployment_group, list_deployment_groups,
    create_deployment, get_deployment, list_deployments,
    stop_deployment, continue_deployment,
    register_application_revision, get_application_revision,
    create_deployment_config, get_deployment_config,
    wait_for_deployment, deploy_and_wait,
)

# Create an application
app = create_application("my-app", compute_platform="Server")

# Create a deployment group
dg_id = create_deployment_group(
    "my-app", "prod-fleet",
    service_role_arn="arn:aws:iam::123456789012:role/CodeDeployRole",
    ec2_tag_filters=[{"Key": "env", "Value": "prod", "Type": "KEY_AND_VALUE"}],
)

# Create a deployment and wait for completion
result = deploy_and_wait(
    "my-app",
    deployment_group_name="prod-fleet",
    revision={
        "revisionType": "S3",
        "s3Location": {
            "bucket": "my-bucket",
            "key": "app.zip",
            "bundleType": "zip",
        },
    },
    timeout=1800,
)
print(result.status)  # "Succeeded"

# Or create deployment and wait separately
dep_id = create_deployment(
    "my-app",
    deployment_group_name="prod-fleet",
    revision={"revisionType": "S3", "s3Location": {"bucket": "b", "key": "k", "bundleType": "zip"}},
    description="v2.0 release",
)
result = wait_for_deployment(dep_id, timeout=600)
```

---

## CloudTrail

```python
from aws_util.cloudtrail import (
    create_trail, describe_trails, get_trail, update_trail, delete_trail,
    start_logging, stop_logging, get_trail_status,
    lookup_events, list_trails,
    create_event_data_store, describe_event_data_store,
    list_event_data_stores, delete_event_data_store,
    start_query, get_query_results, list_queries,
    put_event_selectors, get_event_selectors,
    put_insight_selectors, get_insight_selectors,
)

# Create a trail and start logging
trail = create_trail("my-trail", s3_bucket_name="my-log-bucket")
start_logging(trail.name)

# Check trail status
status = get_trail_status(trail.name)
print(status.is_logging)  # True

# Look up recent events
events = lookup_events(
    lookup_attributes=[{"AttributeKey": "EventName", "AttributeValue": "CreateBucket"}],
    max_results=10,
)
for event in events:
    print(event.event_name, event.username)

# Configure event selectors
put_event_selectors(
    trail.name,
    event_selectors=[{"ReadWriteType": "All", "IncludeManagementEvents": True}],
)

# CloudTrail Lake: create an event data store and run a query
eds = create_event_data_store("my-lake-store", retention_period=90)
query_id = start_query("SELECT * FROM my-lake-store LIMIT 10")
results = get_query_results(query_id)
print(results.query_status, len(results.query_result_rows))
```

---

## Config Loader *(SSM + Secrets Manager)*

```python
from aws_util.config_loader import (
    load_app_config, load_config_from_ssm, load_config_from_secret,
    resolve_config, get_db_credentials, get_ssm_parameter_map,
)

# Load all config concurrently from SSM path + multiple secrets
config = load_app_config(
    ssm_prefix="/myapp/prod/",
    secret_names=["myapp/db-credentials", "myapp/api-keys"],
)
print(config["db/host"])     # from SSM
print(config["password"])    # from secret
print("db/host" in config)   # True

# Get DB credentials with required-field validation
creds = get_db_credentials("myapp/db-credentials")
print(creds["username"], creds["password"], creds.get("host"))

# Fetch a specific list of SSM parameters as a dict
params = get_ssm_parameter_map(["/myapp/db/host", "/myapp/db/port"])

# Expand ${ssm:...} / ${secret:...} placeholders in a static config dict
raw_config = {
    "db_host":   "${ssm:/myapp/prod/db/host}",
    "api_key":   "${secret:myapp/api-keys:key}",
    "log_level": "INFO",
}
config = resolve_config(raw_config)
```

---

## Deployer *(Lambda + ECS + ECR + SSM)*

```python
from aws_util.deployer import (
    deploy_lambda_with_config,
    update_lambda_code_from_s3,
    update_lambda_alias,
    deploy_ecs_image,
    deploy_ecs_from_ecr,
    get_latest_ecr_image_uri,
)

# Full Lambda deploy: upload zip, pull env vars from SSM, publish + alias
result = deploy_lambda_with_config(
    function_name="my-function",
    zip_path="/dist/function.zip",
    ssm_prefix="/myapp/prod/",      # merged into env vars
    env_vars={"LOG_LEVEL": "INFO"}, # static overrides
    publish=True,
    alias="live",
)
print(result.function_arn, result.version, result.alias_arn)

# Deploy from S3
result = deploy_lambda_with_config(
    function_name="my-function",
    s3_bucket="my-artifacts",
    s3_key="builds/function-v2.zip",
    publish=True,
)

# Update ECS service to a new container image and wait for stability
ecs_result = deploy_ecs_image(
    cluster="my-cluster",
    service="my-service",
    new_image_uri="123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v1.5.0",
    wait=True,
    timeout=300,
)
print(ecs_result.new_task_definition_arn, ecs_result.deployment_id)

# Deploy the latest image from an ECR repository
ecs_result = deploy_ecs_from_ecr(
    cluster="my-cluster",
    service="my-service",
    repository_name="my-app",
    tag="latest",
)
```

---

## Notifier *(SNS + SES + SQS)*

```python
from aws_util.notifier import send_alert, notify_on_exception, broadcast, resolve_and_notify

# Send to any combination of channels concurrently
results = send_alert(
    subject="Deploy succeeded",
    message="Version 1.5 is live.",
    sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
    from_email="no-reply@example.com",
    to_emails=["ops@example.com", "cto@example.com"],
    queue_url="https://sqs.us-east-1.amazonaws.com/123/audit-log",
)
for r in results:
    print(r.channel, r.success, r.message_id)

# Decorator — auto-alert whenever the function raises
@notify_on_exception(
    sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
    from_email="no-reply@example.com",
    to_emails=["oncall@example.com"],
)
def nightly_job():
    ...  # any exception triggers an alert; exception is re-raised

# Fan-out to many destinations at once
result = broadcast(
    message="Scheduled maintenance in 30 minutes.",
    subject="Maintenance Notice",
    sns_topic_arns=["arn:aws:sns:...:team-a", "arn:aws:sns:...:team-b"],
    queue_urls=["https://sqs.../audit"],
    from_email="no-reply@example.com",
    to_email_groups=[["alice@example.com"], ["bob@example.com", "carol@example.com"]],
)
print(f"{len(result.succeeded)} delivered, {len(result.failed)} failed")

# Destinations resolved from SSM / Secrets Manager at runtime
resolve_and_notify(
    subject="Nightly ETL complete",
    message_template="Processed {rows} rows in {minutes} minutes.",
    ssm_topic_arn_param="/myapp/prod/alerts-topic-arn",
    secret_email_config="myapp/email-config",
    template_vars={"rows": 150_000, "minutes": 12},
)
```

---

## Data Pipeline *(S3 + Glue + Athena + Kinesis + DynamoDB + SQS)*

```python
from aws_util.data_pipeline import (
    run_glue_job, run_athena_query, fetch_athena_results,
    run_glue_then_query, export_query_to_s3_json,
    s3_json_to_dynamodb, s3_jsonl_to_sqs,
    kinesis_to_s3_snapshot, parallel_export,
)

# Run a Glue job and wait for completion
run = run_glue_job("my-etl-job", arguments={"input": "s3://raw/", "output": "s3://clean/"})
print(run.state, run.execution_time_seconds)

# Full pipeline: Glue ETL → Athena query
result = run_glue_then_query(
    glue_job_name="my-etl-job",
    athena_query="SELECT COUNT(*) FROM clean_orders WHERE status='COMPLETE'",
    athena_database="warehouse",
    athena_output_location="s3://my-bucket/athena-results/",
)
if result.athena_result and result.athena_result.state == "SUCCEEDED":
    rows = fetch_athena_results(result.athena_result.query_execution_id)

# Export Athena query results directly to S3 as a JSON array
count = export_query_to_s3_json(
    query="SELECT * FROM orders WHERE dt = '2024-01-01'",
    database="warehouse",
    staging_location="s3://my-bucket/athena-staging/",
    output_bucket="my-bucket",
    output_key="exports/orders-2024-01-01.json",
)
print(f"{count} rows exported")

# Load S3 JSON array into DynamoDB
written = s3_json_to_dynamodb("my-bucket", "exports/orders-2024-01-01.json", "Orders")

# Enqueue each line of a JSONL file as an SQS message
sent = s3_jsonl_to_sqs("my-bucket", "events/2024-01-01.jsonl", queue_url)

# Snapshot all Kinesis shards to S3 JSONL files
total = kinesis_to_s3_snapshot(
    stream_name="my-stream",
    output_bucket="my-bucket",
    output_key_prefix="snapshots/2024-01-01/",
)
print(f"{total} records written")

# Run multiple Athena queries concurrently and export each to S3
results = parallel_export(
    queries=[
        {"query": "SELECT * FROM orders", "database": "warehouse", "output_key": "orders.json", "label": "orders"},
        {"query": "SELECT * FROM users",  "database": "warehouse", "output_key": "users.json",  "label": "users"},
    ],
    staging_location="s3://my-bucket/staging/",
    output_bucket="my-bucket",
    output_key_prefix="exports/",
)
for r in results:
    print(r["label"], r["rows"], r["error"])
```

---

## Resource Ops *(SQS + DynamoDB + S3 + SSM + Lambda + ECR + Athena + STS)*

```python
from aws_util.resource_ops import (
    reprocess_sqs_dlq,
    backup_dynamodb_to_s3,
    sync_ssm_params_to_lambda_env,
    delete_stale_ecr_images,
    rebuild_athena_partitions,
    s3_inventory_to_dynamodb,
    cross_account_s3_copy,
    rotate_secret_and_notify,
    lambda_invoke_with_secret,
    publish_s3_keys_to_sqs,
)
```

| Function | Services | Description |
|---|---|---|
| `reprocess_sqs_dlq` | SQS | Re-drive messages from a dead-letter queue to its target queue |
| `backup_dynamodb_to_s3` | DynamoDB + S3 | Export a full DynamoDB table scan as a JSON file to S3 |
| `sync_ssm_params_to_lambda_env` | SSM + Lambda | Copy SSM parameters (by path prefix) into a Lambda's environment variables |
| `delete_stale_ecr_images` | ECR + SNS | Delete old untagged/excess images from an ECR repo, optionally notify via SNS |
| `rebuild_athena_partitions` | Athena + S3 | Run `MSCK REPAIR TABLE` and wait for completion |
| `s3_inventory_to_dynamodb` | S3 + DynamoDB | List S3 objects and write their metadata into a DynamoDB table |
| `cross_account_s3_copy` | STS + S3 | Assume a role in another account and copy an S3 object cross-account |
| `rotate_secret_and_notify` | Secrets Manager + SNS | Rotate a secret value and publish a notification |
| `lambda_invoke_with_secret` | Secrets Manager + Lambda | Fetch a secret, inject it as the Lambda payload, and invoke |
| `publish_s3_keys_to_sqs` | S3 + SQS | Fan-out S3 object keys (by prefix) as individual SQS messages |

---

## Security Ops *(S3 + IAM + KMS + Secrets Manager + SNS + Cognito + SES + SSM + CloudWatch + EC2 + CloudFormation)*

```python
from aws_util.security_ops import (
    audit_public_s3_buckets,
    rotate_iam_access_key,
    kms_encrypt_to_secret,
    iam_roles_report_to_s3,
    enforce_bucket_versioning,
    cognito_bulk_create_users,
    sync_secret_to_ssm,
    create_cloudwatch_alarm_with_sns,
    tag_ec2_instances_from_ssm,
    validate_and_store_cfn_template,
)
```

| Function | Services | Description |
|---|---|---|
| `audit_public_s3_buckets` | S3 + SNS | Scan all buckets for public ACLs; optionally alert via SNS |
| `rotate_iam_access_key` | IAM + Secrets Manager | Create a new access key, store it in Secrets Manager, delete the old one |
| `kms_encrypt_to_secret` | KMS + Secrets Manager | Encrypt plaintext with KMS and store the ciphertext as a secret |
| `iam_roles_report_to_s3` | IAM + S3 | Generate a JSON report of all IAM roles and upload to S3 |
| `enforce_bucket_versioning` | S3 + SNS | Enable versioning on a list of buckets; optionally notify via SNS |
| `cognito_bulk_create_users` | Cognito + SES | Bulk-create Cognito users and optionally send welcome emails via SES |
| `sync_secret_to_ssm` | Secrets Manager + SSM | Copy a secret value into an SSM parameter |
| `create_cloudwatch_alarm_with_sns` | CloudWatch + SNS | Create a CloudWatch alarm wired to an SNS topic |
| `tag_ec2_instances_from_ssm` | SSM + EC2 | Read tag values from SSM parameters and apply them to EC2 instances |
| `validate_and_store_cfn_template` | S3 + CloudFormation | Validate a CloudFormation template from S3 and store the validation result |

---

## Lambda Middleware *(Lambda + DynamoDB + SQS + CloudWatch + SSM)*

```python
from aws_util.lambda_middleware import (
    idempotent_handler,
    batch_processor,
    middleware_chain,
    lambda_timeout_guard,
    cold_start_tracker,
    lambda_response,
    cors_preflight,
    parse_event,
    evaluate_feature_flag,
    evaluate_feature_flags,
)
```

| Function | Services | Description |
|---|---|---|
| `idempotent_handler` | Lambda + DynamoDB | Decorator preventing duplicate side effects by caching results in DynamoDB keyed by event hash |
| `batch_processor` | Lambda + SQS/Kinesis/DDB Streams | Process batch records individually with partial failure responses for automatic retry of failed records |
| `middleware_chain` | Lambda | Build composable before/after middleware pipelines for Lambda handlers |
| `lambda_timeout_guard` | Lambda + SQS | Process items with timeout check; push unfinished work to SQS before Lambda times out |
| `cold_start_tracker` | Lambda + CloudWatch | Decorator emitting a `ColdStart` CloudWatch metric (1 = cold, 0 = warm) per invocation |
| `lambda_response` | Lambda + API Gateway | Build standardised API Gateway proxy responses with CORS headers and JSON serialisation |
| `cors_preflight` | Lambda + API Gateway | Generate CORS preflight (OPTIONS) responses with configurable origins, methods, and headers |
| `parse_event` | Lambda | Parse raw Lambda events into typed Pydantic models (API GW, SQS, SNS, S3, EventBridge, DynamoDB Stream, Kinesis) |
| `evaluate_feature_flag` | Lambda + SSM | Evaluate a single feature flag from SSM Parameter Store |
| `evaluate_feature_flags` | Lambda + SSM | Evaluate multiple feature flags from SSM Parameter Store |

---

## API Gateway & Authentication *(API Gateway + Lambda + DynamoDB + Cognito)*

```python
from aws_util.api_gateway import (
    jwt_authorizer,
    api_key_authorizer,
    request_validator,
    throttle_guard,
    websocket_connect,
    websocket_disconnect,
    websocket_list_connections,
    websocket_broadcast,
)
```

| Function | Services | Description |
|---|---|---|
| `jwt_authorizer` | API GW + Lambda + Cognito | Validate JWT tokens (Cognito/OIDC), check issuer, claims, expiry, return IAM policy |
| `api_key_authorizer` | API GW + Lambda + DynamoDB | Validate API keys stored in DynamoDB with owner and enabled checks |
| `request_validator` | API GW + Lambda | Validate request body against a Pydantic model, return structured errors |
| `throttle_guard` | API GW + Lambda + DynamoDB | Per-key rate limiter using DynamoDB atomic counters with TTL-based expiry |
| `websocket_connect` | API GW WebSocket + DynamoDB | Store a new WebSocket connection ID with optional metadata |
| `websocket_disconnect` | API GW WebSocket + DynamoDB | Remove a WebSocket connection from DynamoDB |
| `websocket_list_connections` | API GW WebSocket + DynamoDB | List all active WebSocket connections |
| `websocket_broadcast` | API GW WebSocket + DynamoDB | Broadcast a message to all connected clients, auto-remove stale connections |

---

## Event-Driven Orchestration *(EventBridge + Step Functions + Lambda + SQS + DynamoDB + Scheduler + Pipes)*

```python
from aws_util.event_orchestration import (
    create_eventbridge_rule,
    put_eventbridge_targets,
    delete_eventbridge_rule,
    create_schedule,
    delete_schedule,
    run_workflow,
    saga_orchestrator,
    fan_out_fan_in,
    start_event_replay,
    describe_event_replay,
    create_pipe,
    delete_pipe,
    create_sqs_event_source_mapping,
    delete_event_source_mapping,
)
```

| Function | Services | Description |
|---|---|---|
| `create_eventbridge_rule` | EventBridge | Create or update a rule with schedule expression or event pattern |
| `put_eventbridge_targets` | EventBridge | Add targets to an EventBridge rule |
| `delete_eventbridge_rule` | EventBridge | Delete a rule, optionally force-removing targets first |
| `create_schedule` | EventBridge Scheduler | Create a one-time or recurring schedule with flexible time window |
| `delete_schedule` | EventBridge Scheduler | Delete an EventBridge Scheduler schedule |
| `run_workflow` | Step Functions | Start a Step Functions execution and poll until completion |
| `saga_orchestrator` | Lambda | Execute a saga: sequence of Lambda steps with compensating rollbacks |
| `fan_out_fan_in` | SQS + DynamoDB | Dispatch work items to SQS in batches, optionally track in DynamoDB |
| `start_event_replay` | EventBridge | Replay archived events within a time window |
| `describe_event_replay` | EventBridge | Describe the current state of an event replay |
| `create_pipe` | EventBridge Pipes | Create a pipe: source → optional filter → optional enrichment → target |
| `delete_pipe` | EventBridge Pipes | Delete an EventBridge Pipe |
| `create_sqs_event_source_mapping` | Lambda + SQS | Create an SQS event-source mapping on a Lambda function |
| `delete_event_source_mapping` | Lambda | Delete a Lambda event-source mapping |

---

## Data Flow & ETL Pipelines *(S3 + DynamoDB + Kinesis + Firehose + OpenSearch + Glue + Athena + CloudWatch + SNS)*

```python
from aws_util.data_flow_etl import (
    s3_event_to_dynamodb,
    dynamodb_stream_to_opensearch,
    dynamodb_stream_to_s3_archive,
    s3_csv_to_dynamodb_bulk,
    kinesis_to_firehose_transformer,
    cross_region_s3_replicator,
    etl_status_tracker,
    s3_multipart_upload_manager,
    data_lake_partition_manager,
    repair_partitions,
)
```

| Function | Services | Description |
|---|---|---|
| `s3_event_to_dynamodb` | S3 + DynamoDB | Process S3 JSON/JSON-lines objects, optional transform, batch-write to DynamoDB |
| `dynamodb_stream_to_opensearch` | DDB Streams + OpenSearch | Index INSERT/MODIFY images into OpenSearch, remove on DELETE |
| `dynamodb_stream_to_s3_archive` | DDB Streams + S3 | Archive stream records to S3 in JSON-lines format, date-partitioned |
| `s3_csv_to_dynamodb_bulk` | S3 + DynamoDB | Read CSV from S3, optional column mapping, chunked batch-write to DynamoDB |
| `kinesis_to_firehose_transformer` | Kinesis + Firehose | Read Kinesis records, apply transformation, write to Firehose delivery stream |
| `cross_region_s3_replicator` | S3 + SNS | Replicate S3 objects across regions with metadata preservation + SNS notification |
| `etl_status_tracker` | DynamoDB + CloudWatch | Track multi-step ETL pipeline status in DynamoDB with optional CloudWatch metrics |
| `s3_multipart_upload_manager` | S3 | Multipart uploads with progress tracking and auto-abort on failure |
| `data_lake_partition_manager` | Glue + S3 | Add Glue partitions when new data lands, skip existing partitions |
| `repair_partitions` | Athena + Glue | Run MSCK REPAIR TABLE via Athena to auto-discover new partitions |

---

## Resilience & Error Handling *(Lambda + DynamoDB + SQS + SNS + S3)*

```python
from aws_util.resilience import (
    circuit_breaker,
    retry_with_backoff,
    dlq_monitor_and_alert,
    poison_pill_handler,
    lambda_destination_router,
    graceful_degradation,
    timeout_sentinel,
)
```

| Function | Services | Description |
|---|---|---|
| `circuit_breaker` | Lambda + DynamoDB | Circuit breaker pattern (closed/open/half-open) with DynamoDB state tracking — called as `circuit_breaker(func, ...)` (not a decorator). Writes to DynamoDB only on state transitions to reduce write volume |
| `retry_with_backoff` | Lambda (any service) | Decorator for exponential backoff with jitter, configurable retries and exception types |
| `dlq_monitor_and_alert` | SQS + SNS | Poll SQS DLQ depth, fire SNS alerts when messages accumulate above threshold |
| `poison_pill_handler` | SQS + S3 + DynamoDB | Detect repeatedly-failing messages via `ApproximateReceiveCount`, quarantine to S3 and/or DynamoDB |
| `lambda_destination_router` | Lambda + SQS/SNS/EventBridge | Configure Lambda async invocation destinations (on-success / on-failure) |
| `graceful_degradation` | Lambda + DynamoDB | Execute a callable with DynamoDB-cached fallback on downstream failure |
| `timeout_sentinel` | Lambda | Wrap external calls with a strict timeout shorter than the Lambda limit |

---

## Observability & Monitoring *(CloudWatch + X-Ray + Synthetics + CloudWatch Logs)*

```python
from aws_util.observability import (
    StructuredLogger, create_xray_trace, emit_emf_metric,
    emit_emf_metrics_batch, create_lambda_alarms, create_dlq_depth_alarm,
    run_log_insights_query, generate_lambda_dashboard,
    aggregate_errors, create_canary, delete_canary,
    build_service_map, get_trace_summaries,
)
```

| Function | Services | Description |
|---|---|---|
| `StructuredLogger` | CloudWatch Logs | JSON structured logger with correlation IDs, Lambda context injection, child loggers |
| `create_xray_trace` | X-Ray | Create custom X-Ray trace segments with subsegments and annotations |
| `batch_put_trace_segments` | X-Ray | Batch-submit multiple X-Ray trace segment documents |
| `emit_emf_metric` | CloudWatch | Emit a single CloudWatch metric via Embedded Metric Format (EMF) |
| `emit_emf_metrics_batch` | CloudWatch | Emit multiple metrics in a single EMF document |
| `create_lambda_alarms` | CloudWatch + SNS | Create error-rate and duration alarms for a Lambda function wired to SNS |
| `create_dlq_depth_alarm` | CloudWatch + SQS + SNS | Create a CloudWatch alarm on SQS DLQ depth |
| `run_log_insights_query` | CloudWatch Logs | Execute a CloudWatch Logs Insights query and return results |
| `generate_lambda_dashboard` | CloudWatch | Generate a CloudWatch dashboard JSON for Lambda functions |
| `aggregate_errors` | CloudWatch Logs + SNS | Scan log groups for errors, deduplicate, send digest via SNS |
| `create_canary` | Synthetics + S3 | Create a CloudWatch Synthetics canary for health-check monitoring |
| `delete_canary` | Synthetics | Stop and delete a CloudWatch Synthetics canary |
| `build_service_map` | X-Ray | Query X-Ray for a service dependency map |
| `get_trace_summaries` | X-Ray | Query X-Ray trace summaries with optional filter expression |

---

## Deployment & Release Management *(Lambda + CloudFormation + EventBridge + CloudWatch + S3)*

```python
from aws_util.deployment import (
    lambda_canary_deploy, lambda_layer_publisher,
    stack_deployer, environment_promoter, lambda_warmer,
    config_drift_detector, rollback_manager, lambda_package_builder,
)
```

| Function | Services | Description |
|---|---|---|
| `lambda_canary_deploy` | Lambda + CloudWatch | Publish new version, shift alias traffic with canary steps, auto-rollback on alarm |
| `lambda_layer_publisher` | Lambda + S3 | Package a directory into a Lambda Layer ZIP, publish, update functions |
| `stack_deployer` | CloudFormation + S3 | Deploy CFN/SAM stacks via change sets with auto-rollback and output capture |
| `environment_promoter` | Lambda + STS | Copy Lambda config, env vars, and aliases across accounts/stages |
| `lambda_warmer` | Lambda + EventBridge | Schedule periodic no-op invocations to keep Lambdas warm |
| `config_drift_detector` | Lambda + API Gateway + SSM + S3 | Compare deployed configs against desired state, report drift |
| `rollback_manager` | Lambda + CloudWatch | Detect error-rate spikes, auto-shift alias traffic to previous version |
| `lambda_package_builder` | Lambda + S3 | Bundle Python code + pip dependencies into a deployment ZIP, upload to S3 |

---

## Security & Compliance *(IAM + Lambda + Secrets Manager + SSM + SNS + EC2 + DynamoDB + SQS + S3 + KMS + WAF + Cognito)*

```python
from aws_util.security_compliance import (
    least_privilege_analyzer, secret_rotation_orchestrator,
    data_masking_processor, vpc_security_group_auditor,
    encryption_enforcer, api_gateway_waf_manager,
    compliance_snapshot, resource_policy_validator,
    cognito_auth_flow_manager,
)
```

| Function | Services | Description |
|---|---|---|
| `least_privilege_analyzer` | IAM + Lambda | Analyze Lambda execution roles for overly permissive policies |
| `secret_rotation_orchestrator` | Secrets Manager + Lambda + SSM + SNS | Rotate secrets, propagate new values to Lambda env vars and SSM, notify via SNS |
| `data_masking_processor` | Comprehend + CloudWatch Logs | Detect and mask PII in text or CloudWatch log events |
| `vpc_security_group_auditor` | EC2 | Audit security groups for overly permissive ingress rules (0.0.0.0/0) |
| `encryption_enforcer` | DynamoDB + SQS + SNS + S3 + KMS | Check encryption status across services, optionally remediate with KMS |
| `api_gateway_waf_manager` | WAF + API Gateway | Associate/disassociate WAF Web ACLs with API Gateway stages |
| `compliance_snapshot` | Lambda + IAM + DynamoDB + SQS + S3 + SNS | Generate a point-in-time compliance report across multiple services |
| `resource_policy_validator` | S3 + SQS + SNS + Lambda + KMS | Validate resource policies for public access, wildcard principals, missing conditions |
| `cognito_auth_flow_manager` | Cognito | Manage sign-up, sign-in, refresh, forgot-password, and MFA flows |

---

## Cost Optimization *(Lambda + CloudWatch + SQS + CloudWatch Logs + DynamoDB + Resource Groups Tagging)*

```python
from aws_util.cost_optimization import (
    lambda_right_sizer, unused_resource_finder,
    concurrency_optimizer, cost_attribution_tagger,
    dynamodb_capacity_advisor, log_retention_enforcer,
)
```

| Function | Services | Description |
|---|---|---|
| `lambda_right_sizer` | Lambda + CloudWatch | Invoke Lambda at multiple memory configs, measure duration/cost, recommend optimal setting |
| `unused_resource_finder` | Lambda + SQS + CloudWatch Logs | Find idle Lambda functions, empty SQS queues, orphaned log groups |
| `concurrency_optimizer` | Lambda + CloudWatch | Analyze Lambda concurrency metrics, recommend reserved/provisioned settings |
| `cost_attribution_tagger` | Resource Groups Tagging | Ensure cost-allocation tags on serverless resources, apply missing tags |
| `dynamodb_capacity_advisor` | DynamoDB + CloudWatch | Analyze consumed vs provisioned DynamoDB capacity, recommend on-demand or adjustments |
| `log_retention_enforcer` | CloudWatch Logs | Set/enforce CloudWatch Logs retention policies across Lambda log groups |

---

## Testing & Development *(Lambda + CloudFormation + DynamoDB + SQS + S3 + SNS)*

```python
from aws_util.testing_dev import (
    lambda_event_generator, local_dynamodb_seeder,
    integration_test_harness, mock_event_source,
    lambda_invoke_recorder, snapshot_tester,
)
```

| Function | Services | Description |
|---|---|---|
| `lambda_event_generator` | Lambda (all sources) | Generate realistic sample events for all Lambda trigger types (API GW, SQS, SNS, S3, DynamoDB Stream, EventBridge, Kinesis, Cognito) |
| `local_dynamodb_seeder` | DynamoDB | Seed DynamoDB with test data from JSON or CSV content |
| `integration_test_harness` | CloudFormation + Lambda + DynamoDB + SQS | Deploy temp CloudFormation stack, run tests, capture results, teardown |
| `mock_event_source` | SQS + S3 + Lambda | Create temp SQS queue and S3 bucket with event source mapping wired to Lambda |
| `lambda_invoke_recorder` | Lambda + S3 + DynamoDB | Record Lambda invocation request/response pairs to S3 and/or DynamoDB for replay testing |
| `snapshot_tester` | Lambda + S3 + SNS | Compare Lambda output against S3 baseline snapshots, alert on changes via SNS |

---

## Configuration & State Management *(SSM + Secrets Manager + DynamoDB + STS + Lambda + AppConfig)*

```python
from aws_util.config_state import (
    config_resolver, distributed_lock,
    state_machine_checkpoint, cross_account_role_assumer,
    environment_variable_sync, appconfig_feature_loader,
)
```

| Function | Services | Description |
|---|---|---|
| `config_resolver` | SSM + Secrets Manager | Hierarchical config from SSM Parameter Store by environment/service path, with secret injection |
| `distributed_lock` | DynamoDB | DynamoDB conditional writes with TTL for coordinating singleton Lambda executions |
| `state_machine_checkpoint` | DynamoDB | Save/restore Lambda execution state to DynamoDB for long-running multi-invocation processes |
| `cross_account_role_assumer` | STS | Chain STS assume_role calls for cross-account ops, cache + auto-refresh credentials |
| `environment_variable_sync` | SSM + Lambda | Sync Lambda env vars from SSM Parameter Store with change detection |
| `appconfig_feature_loader` | AppConfig | Fetch and cache AWS AppConfig feature flags with automatic refresh |

### `blue_green` -- Blue/green & canary deployments

```python
from aws_util.blue_green import (
    ecs_blue_green_deployer, weighted_routing_manager,
    lambda_provisioned_concurrency_scaler,
)
```

| Function | Services | Description |
|---|---|---|
| `ecs_blue_green_deployer` | ECS + ELBv2 + CloudWatch | Create green target group and ECS service, incrementally shift ALB listener weights with CloudWatch alarm gating and auto-rollback |
| `weighted_routing_manager` | Route53 + CloudWatch + SNS | Manage Route53 weighted record sets for canary traffic migration with health-check monitoring, auto-revert, and SNS notifications |
| `lambda_provisioned_concurrency_scaler` | Lambda + Application Auto Scaling + CloudWatch + SNS | Configure Lambda provisioned concurrency with alias management, target-tracking scaling, scheduled actions, and cold-start alarms |

### `cross_account` -- Cross-account AWS patterns

```python
from aws_util.cross_account import (
    cross_account_event_bus_federator,
    centralized_log_aggregator,
    multi_account_resource_inventory,
)
```

| Function | Services | Description |
|---|---|---|
| `cross_account_event_bus_federator` | EventBridge + STS + SQS | Set up cross-account EventBridge event routing with resource policies, forwarding rules, DLQ configuration, and connectivity validation |
| `centralized_log_aggregator` | CloudWatch Logs + Kinesis Firehose + S3 + STS | Configure cross-account CloudWatch Logs aggregation via Firehose to S3 with subscription filters, access policies, and lifecycle rules |
| `multi_account_resource_inventory` | Resource Groups Tagging + DynamoDB + S3 + STS | Inventory tagged resources across multiple accounts, batch-write to DynamoDB, and export to S3 as JSON |

### `event_patterns` -- Event-driven architecture patterns

```python
from aws_util.event_patterns import (
    transactional_outbox_processor,
    dlq_escalation_chain,
    event_sourcing_store,
)
```

| Function | Services | Description |
|---|---|---|
| `transactional_outbox_processor` | DynamoDB + SNS/SQS/EventBridge | Scan a DynamoDB outbox table for pending events, publish to SNS/SQS/EventBridge, and mark delivered with automatic retry and dead-letter handling |
| `dlq_escalation_chain` | SQS + SNS | Multi-tier DLQ escalation: reprocess messages through a chain of queues, escalating to SNS alerts when all retries are exhausted |
| `event_sourcing_store` | DynamoDB + S3 + SNS | Append events to a DynamoDB event store, maintain snapshots in S3, and publish change notifications to SNS |

### `database_migration` -- Zero-downtime database migration

```python
from aws_util.database_migration import (
    dynamodb_table_migrator,
    rds_blue_green_orchestrator,
)
```

| Function | Services | Description |
|---|---|---|
| `dynamodb_table_migrator` | DynamoDB + S3 | Migrate DynamoDB tables with schema transformation, backfill via scan-and-write with progress tracking and S3 backup |
| `rds_blue_green_orchestrator` | RDS + Route53 + Secrets Manager | Create RDS blue/green deployments, wait for sync, switch DNS via Route53, rotate credentials in Secrets Manager, and clean up old instances |

### `credential_rotation` -- Database credential rotation

```python
from aws_util.credential_rotation import database_credential_rotator
```

| Function | Services | Description |
|---|---|---|
| `database_credential_rotator` | Secrets Manager + RDS + SNS | Multi-step credential rotation: generate new password, update RDS master credentials, store in Secrets Manager, validate connectivity, and send SNS notifications |

### `disaster_recovery` -- DR orchestration & backup compliance

```python
from aws_util.disaster_recovery import (
    disaster_recovery_orchestrator,
    backup_compliance_manager,
)
```

| Function | Services | Description |
|---|---|---|
| `disaster_recovery_orchestrator` | EC2 + RDS + S3 + Route53 + SNS | Multi-region DR lifecycle: replicate AMIs and RDS snapshots, failover DNS, launch recovery instances, and send status notifications |
| `backup_compliance_manager` | Backup + DynamoDB + S3 + SNS | Audit AWS Backup vault compliance, verify retention policies, check backup freshness, and report violations via SNS |

### `cost_governance` -- Cost anomaly detection & savings analysis

```python
from aws_util.cost_governance import (
    cost_anomaly_detector,
    savings_plan_analyzer,
)
```

| Function | Services | Description |
|---|---|---|
| `cost_anomaly_detector` | Cost Explorer + CloudWatch + SNS | Detect cost anomalies by comparing current spend against historical baselines with configurable thresholds, publish CloudWatch metrics, and alert via SNS |
| `savings_plan_analyzer` | Cost Explorer + CloudWatch + SNS | Analyze Savings Plan utilization and coverage, identify optimization opportunities, publish metrics, and send recommendations via SNS |

### `security_automation` -- Automated security remediation

```python
from aws_util.security_automation import (
    guardduty_auto_remediator,
    config_rules_auto_remediator,
)
```

| Function | Services | Description |
|---|---|---|
| `guardduty_auto_remediator` | GuardDuty + EC2 + IAM + SNS | Automatically remediate GuardDuty findings: isolate compromised EC2 instances, disable leaked IAM credentials, and notify via SNS |
| `config_rules_auto_remediator` | Config + Lambda + S3 + SNS | Auto-remediate non-compliant AWS Config rules: enable S3 encryption/versioning/public-access blocks, invoke Lambda for custom fixes, and alert via SNS |

### `container_ops` -- ECS capacity provider optimization

```python
from aws_util.container_ops import ecs_capacity_provider_optimizer
```

| Function | Services | Description |
|---|---|---|
| `ecs_capacity_provider_optimizer` | ECS + Application Auto Scaling + CloudWatch | Analyze ECS cluster capacity, optimize Fargate/Fargate Spot ratios, configure auto-scaling policies, and publish utilization metrics |

### `ml_pipeline` -- SageMaker endpoint & model registry management

```python
from aws_util.ml_pipeline import (
    sagemaker_endpoint_manager,
    model_registry_promoter,
)
```

| Function | Services | Description |
|---|---|---|
| `sagemaker_endpoint_manager` | SageMaker + CloudWatch | Deploy SageMaker endpoints with A/B traffic splitting, auto-scaling, CloudWatch health monitoring, and variant-level metrics collection |
| `model_registry_promoter` | SageMaker + S3 + STS | Promote models through SageMaker Model Registry stages (dev → staging → prod) with optional cross-account S3 artifact copies |

### `networking` -- VPC connectivity automation

```python
from aws_util.networking import vpc_connectivity_manager
```

| Function | Services | Description |
|---|---|---|
| `vpc_connectivity_manager` | EC2 (VPC) + Route53 | Automate VPC peering, Transit Gateway attachments, and PrivateLink endpoint services with route table updates and DNS configuration |

---

## Error handling

All AWS errors are classified into a structured exception hierarchy defined in `aws_util.exceptions`. Every exception extends `RuntimeError` for backward compatibility — existing `except RuntimeError` handlers continue to work, while new code can catch the precise type it cares about.

```python
from aws_util.exceptions import (
    AwsUtilError,          # Base for all aws-util exceptions (extends RuntimeError)
    AwsServiceError,       # Catch-all for unclassified AWS API errors
    AwsThrottlingError,    # API throttling / rate limiting
    AwsNotFoundError,      # Resource does not exist
    AwsPermissionError,    # Caller lacks permission
    AwsConflictError,      # Resource already exists or is in use
    AwsValidationError,    # Invalid input parameters (also extends ValueError)
    AwsTimeoutError,       # Polling / operation timeout (also extends TimeoutError)
    wrap_aws_error,        # Classify any exception into the hierarchy
    classify_aws_error,    # Classify a botocore ClientError by error code
    ClientError,           # Re-exported from botocore for convenience
)
```

| Condition | Exception |
|---|---|
| AWS API throttling (e.g. `TooManyRequestsException`) | `AwsThrottlingError` |
| Resource not found (e.g. `ResourceNotFoundException`) | `AwsNotFoundError` |
| Permission denied (e.g. `AccessDeniedException`) | `AwsPermissionError` |
| Resource conflict (e.g. `ConflictException`) | `AwsConflictError` |
| Invalid parameters (e.g. `ValidationException`) | `AwsValidationError` |
| Any other AWS API call fails | `AwsServiceError` |
| Secret not valid JSON when key specified | `AwsServiceError` |
| JSON key not found in secret | `KeyError` |
| Batch size limit exceeded | `AwsValidationError` |
| Batch partially fails (SQS/SNS) | `AwsServiceError` with details |
| EventBridge partial failure | Returns `PutEventsResult` with failure details |
| EventBridge all events fail | `AwsServiceError` |
| SNS fan-out partial failure | `AwsServiceError` after collecting all results |
| `envelope_decrypt` AES-GCM authentication failure | `AwsServiceError` (from `InvalidTag` or `ValueError`) |
| Image/document source not specified | `ValueError` |
| Polling timeout exceeded | `AwsTimeoutError` |

### Client caching and credential rotation

boto3 clients are cached per `(service, region)` pair with a **15-minute TTL** and bounded to 64 entries. This ensures STS temporary credentials, `assume_role` sessions, and Lambda execution-role rotations are picked up automatically.

```python
from aws_util._client import clear_client_cache

# Force immediate credential refresh
clear_client_cache()
```

### Placeholder caching

`retrieve()` caches resolved SSM and Secrets Manager values for the lifetime of the process. In warm Lambda containers, call `clear_all_caches()` (or `clear_ssm_cache()` / `clear_secret_cache()`) to force re-resolution after rotation or updates.

---

## AWS IAM permissions

Minimum permissions required per service:

| Service | Required Actions |
|---|---|
| SSM | `ssm:GetParameter` `ssm:GetParameters` `ssm:GetParametersByPath` `ssm:PutParameter` `ssm:DeleteParameter` |
| Secrets Manager | `secretsmanager:GetSecretValue` `secretsmanager:CreateSecret` `secretsmanager:UpdateSecret` `secretsmanager:DeleteSecret` `secretsmanager:ListSecrets` `secretsmanager:RotateSecret` `secretsmanager:BatchGetSecretValue` `secretsmanager:CancelRotateSecret` `secretsmanager:DescribeSecret` `secretsmanager:GetRandomPassword` `secretsmanager:GetResourcePolicy` `secretsmanager:ListSecretVersionIds` `secretsmanager:PutResourcePolicy` `secretsmanager:PutSecretValue` `secretsmanager:RemoveRegionsFromReplication` `secretsmanager:ReplicateSecretToRegions` `secretsmanager:RestoreSecret` `secretsmanager:TagResource` `secretsmanager:UntagResource` `secretsmanager:UpdateSecretVersionStage` `secretsmanager:ValidateResourcePolicy` |
| S3 | `s3:GetObject` `s3:PutObject` `s3:DeleteObject` `s3:ListBucket` |
| DynamoDB | `dynamodb:GetItem` `dynamodb:PutItem` `dynamodb:UpdateItem` `dynamodb:DeleteItem` `dynamodb:Query` `dynamodb:Scan` `dynamodb:BatchGetItem` `dynamodb:BatchWriteItem` |
| SQS | `sqs:SendMessage` `sqs:ReceiveMessage` `sqs:DeleteMessage` `sqs:GetQueueUrl` `sqs:PurgeQueue` |
| SNS | `sns:Publish` `sns:CreateTopic` |
| Lambda | `lambda:InvokeFunction` |
| CloudWatch Metrics | `cloudwatch:PutMetricData` |
| CloudWatch Logs | `logs:CreateLogGroup` `logs:CreateLogStream` `logs:PutLogEvents` `logs:GetLogEvents` |
| STS | `sts:GetCallerIdentity` `sts:AssumeRole` |
| EventBridge | `events:PutEvents` |
| KMS | `kms:Encrypt` `kms:Decrypt` `kms:GenerateDataKey` |
| EC2 | `ec2:DescribeInstances` `ec2:StartInstances` `ec2:StopInstances` `ec2:RebootInstances` `ec2:TerminateInstances` `ec2:CreateImage` |
| RDS | `rds:DescribeDBInstances` `rds:StartDBInstance` `rds:StopDBInstance` `rds:CreateDBSnapshot` `rds:DeleteDBSnapshot` |
| ECS | `ecs:RunTask` `ecs:StopTask` `ecs:DescribeTasks` `ecs:ListTasks` `ecs:DescribeServices` `ecs:UpdateService` |
| ECR | `ecr:GetAuthorizationToken` `ecr:DescribeRepositories` `ecr:CreateRepository` `ecr:ListImages` `ecr:DescribeImages` |
| IAM | `iam:CreateRole` `iam:DeleteRole` `iam:GetRole` `iam:ListRoles` `iam:AttachRolePolicy` `iam:DetachRolePolicy` `iam:CreatePolicy` `iam:DeletePolicy` |
| Cognito | `cognito-idp:AdminCreateUser` `cognito-idp:AdminGetUser` `cognito-idp:AdminDeleteUser` `cognito-idp:ListUsers` `cognito-idp:AdminInitiateAuth` |
| Route 53 | `route53:ListHostedZones` `route53:ChangeResourceRecordSets` `route53:ListResourceRecordSets` |
| ACM | `acm:ListCertificates` `acm:DescribeCertificate` `acm:RequestCertificate` `acm:DeleteCertificate` `acm:GetCertificate` `acm:ImportCertificate` `acm:ExportCertificate` `acm:RenewCertificate` `acm:AddTagsToCertificate` `acm:RemoveTagsFromCertificate` `acm:ListTagsForCertificate` `acm:ResendValidationEmail` `acm:UpdateCertificateOptions` `acm:GetAccountConfiguration` `acm:PutAccountConfiguration` |
| Step Functions | `states:StartExecution` `states:DescribeExecution` `states:StopExecution` `states:ListExecutions` |
| CloudFormation | `cloudformation:CreateStack` `cloudformation:UpdateStack` `cloudformation:DeleteStack` `cloudformation:DescribeStacks` `cloudformation:ListStacks` |
| Kinesis | `kinesis:PutRecord` `kinesis:PutRecords` `kinesis:GetRecords` `kinesis:GetShardIterator` `kinesis:DescribeStreamSummary` `kinesis:ListStreams` `kinesis:CreateStream` `kinesis:DeleteStream` `kinesis:ListShards` `kinesis:AddTagsToStream` `kinesis:RemoveTagsFromStream` `kinesis:ListTagsForStream` `kinesis:IncreaseStreamRetentionPeriod` `kinesis:DecreaseStreamRetentionPeriod` `kinesis:MergeShards` `kinesis:SplitShard` `kinesis:StartStreamEncryption` `kinesis:StopStreamEncryption` `kinesis:EnableEnhancedMonitoring` `kinesis:DisableEnhancedMonitoring` `kinesis:UpdateShardCount` `kinesis:UpdateStreamMode` `kinesis:RegisterStreamConsumer` `kinesis:DeregisterStreamConsumer` `kinesis:DescribeStreamConsumer` `kinesis:ListStreamConsumers` `kinesis:DescribeLimits` `kinesis:SubscribeToShard` `kinesis:PutResourcePolicy` `kinesis:GetResourcePolicy` `kinesis:DeleteResourcePolicy` |
| Firehose | `firehose:PutRecord` `firehose:PutRecordBatch` `firehose:ListDeliveryStreams` `firehose:DescribeDeliveryStream` |
| SES | `ses:SendEmail` `ses:SendTemplatedEmail` `ses:SendRawEmail` `ses:VerifyEmailAddress` `ses:ListVerifiedEmailAddresses` |
| Glue | `glue:StartJobRun` `glue:GetJobRun` `glue:GetJob` `glue:GetJobs` `glue:GetJobRuns` `glue:BatchStopJobRun` |
| Athena | `athena:StartQueryExecution` `athena:GetQueryExecution` `athena:GetQueryResults` `athena:StopQueryExecution` |
| Bedrock | `bedrock:InvokeModel` `bedrock:InvokeModelWithResponseStream` `bedrock:ListFoundationModels` |
| Rekognition | `rekognition:DetectLabels` `rekognition:DetectFaces` `rekognition:DetectText` `rekognition:CompareFaces` `rekognition:DetectModerationLabels` `rekognition:CreateCollection` `rekognition:DeleteCollection` `rekognition:IndexFaces` `rekognition:SearchFacesByImage` |
| Textract | `textract:DetectDocumentText` `textract:AnalyzeDocument` `textract:StartDocumentTextDetection` `textract:GetDocumentTextDetection` |
| Comprehend | `comprehend:DetectSentiment` `comprehend:DetectEntities` `comprehend:DetectKeyPhrases` `comprehend:DetectDominantLanguage` `comprehend:DetectPiiEntities` `comprehend:BatchDetectSentiment` |
| Translate | `translate:TranslateText` `translate:ListLanguages` |
| Security Hub | `securityhub:EnableSecurityHub` `securityhub:DisableSecurityHub` `securityhub:DescribeHub` `securityhub:GetFindings` `securityhub:BatchUpdateFindings` `securityhub:GetInsightResults` `securityhub:GetInsights` `securityhub:CreateInsight` `securityhub:UpdateInsight` `securityhub:DeleteInsight` `securityhub:EnableImportFindingsForProduct` `securityhub:DisableImportFindingsForProduct` `securityhub:ListEnabledProductsForImport` `securityhub:GetEnabledStandards` `securityhub:BatchEnableStandards` `securityhub:BatchDisableStandards` `securityhub:DescribeStandards` `securityhub:DescribeStandardsControls` `securityhub:UpdateStandardsControl` `securityhub:InviteMembers` `securityhub:ListMembers` `securityhub:GetMembers` `securityhub:CreateMembers` `securityhub:DeleteMembers` `securityhub:GetAdministratorAccount` `securityhub:AcceptAdministratorInvitation` |
| config_loader | *(union of SSM + Secrets Manager permissions above)* |
| deployer | `lambda:UpdateFunctionCode` `lambda:UpdateFunctionConfiguration` `lambda:PublishVersion` `lambda:CreateAlias` `lambda:UpdateAlias` `lambda:GetFunctionConfiguration` `ecs:DescribeServices` `ecs:DescribeTaskDefinition` `ecs:RegisterTaskDefinition` `ecs:UpdateService` `ecs:DescribeContainerInstances` `ecr:DescribeImages` `ecr:DescribeRepositories` |
| notifier | *(union of SNS `sns:Publish`, SES `ses:SendEmail`, SQS `sqs:SendMessage` plus SSM/Secrets Manager read permissions for `resolve_and_notify`)* |
| data_pipeline | `glue:StartJobRun` `glue:GetJobRun` `athena:StartQueryExecution` `athena:GetQueryExecution` `athena:GetQueryResults` `kinesis:GetShardIterator` `kinesis:GetRecords` `kinesis:ListShards` `kinesis:DescribeStreamSummary` `dynamodb:BatchWriteItem` `sqs:SendMessage` `s3:GetObject` `s3:PutObject` |
| resource_ops | `sqs:ReceiveMessage` `sqs:SendMessage` `sqs:DeleteMessage` `dynamodb:Scan` `s3:PutObject` `s3:ListObjectsV2` `s3:GetObject` `ssm:GetParametersByPath` `lambda:UpdateFunctionConfiguration` `lambda:Invoke` `ecr:DescribeImages` `ecr:BatchDeleteImage` `sns:Publish` `athena:StartQueryExecution` `athena:GetQueryExecution` `sts:AssumeRole` `secretsmanager:GetSecretValue` `secretsmanager:PutSecretValue` `dynamodb:BatchWriteItem` |
| security_ops | `s3:ListBuckets` `s3:GetBucketAcl` `s3:PutBucketVersioning` `s3:GetBucketVersioning` `s3:GetObject` `s3:PutObject` `iam:CreateAccessKey` `iam:DeleteAccessKey` `iam:ListAccessKeys` `iam:ListRoles` `kms:Encrypt` `secretsmanager:CreateSecret` `secretsmanager:GetSecretValue` `secretsmanager:PutSecretValue` `sns:Publish` `sns:CreateTopic` `sns:Subscribe` `cognito-idp:AdminCreateUser` `ses:SendEmail` `ssm:PutParameter` `cloudwatch:PutMetricAlarm` `ec2:CreateTags` `ec2:DescribeInstances` `cloudformation:ValidateTemplate` |
| lambda_middleware | `dynamodb:GetItem` `dynamodb:PutItem` `sqs:SendMessage` `cloudwatch:PutMetricData` `ssm:GetParameter` |
| api_gateway | `dynamodb:GetItem` `dynamodb:PutItem` `dynamodb:DeleteItem` `dynamodb:Scan` `dynamodb:UpdateItem` `execute-api:ManageConnections` |
| event_orchestration | `events:PutRule` `events:PutTargets` `events:DeleteRule` `events:RemoveTargets` `events:ListTargetsByRule` `events:StartReplay` `events:DescribeReplay` `scheduler:CreateSchedule` `scheduler:DeleteSchedule` `states:StartExecution` `states:DescribeExecution` `lambda:InvokeFunction` `lambda:CreateEventSourceMapping` `lambda:DeleteEventSourceMapping` `sqs:SendMessageBatch` `dynamodb:PutItem` `pipes:CreatePipe` `pipes:DeletePipe` |
| data_flow_etl | `s3:GetObject` `s3:PutObject` `s3:CreateMultipartUpload` `s3:UploadPart` `s3:CompleteMultipartUpload` `s3:AbortMultipartUpload` `dynamodb:BatchWriteItem` `dynamodb:PutItem` `kinesis:DescribeStream` `kinesis:GetShardIterator` `kinesis:GetRecords` `firehose:PutRecordBatch` `sns:Publish` `cloudwatch:PutMetricData` `glue:GetTable` `glue:CreatePartition` `athena:StartQueryExecution` |
| resilience | `dynamodb:GetItem` `dynamodb:PutItem` `sqs:GetQueueAttributes` `sns:Publish` `s3:PutObject` `lambda:PutFunctionEventInvokeConfig` |
| observability | `xray:PutTraceSegments` `xray:GetTraceSummaries` `xray:GetServiceGraph` `logs:StartQuery` `logs:GetQueryResults` `logs:DescribeLogGroups` `logs:DescribeLogStreams` `logs:FilterLogEvents` `cloudwatch:PutMetricAlarm` `cloudwatch:PutDashboard` `synthetics:CreateCanary` `synthetics:StartCanary` `synthetics:StopCanary` `synthetics:DeleteCanary` `sns:Publish` |
| deployment | `lambda:GetFunction` `lambda:PublishVersion` `lambda:CreateAlias` `lambda:UpdateAlias` `lambda:GetAlias` `lambda:AddPermission` `lambda:PublishLayerVersion` `lambda:UpdateFunctionConfiguration` `lambda:GetFunctionConfiguration` `cloudformation:CreateChangeSet` `cloudformation:DescribeChangeSet` `cloudformation:ExecuteChangeSet` `cloudformation:DeleteChangeSet` `cloudformation:DescribeStacks` `cloudformation:GetTemplate` `events:PutRule` `events:PutTargets` `events:RemoveTargets` `events:DeleteRule` `cloudwatch:GetMetricStatistics` `s3:PutObject` `s3:GetObject` `ssm:GetParameter` `sts:AssumeRole` |
| security_compliance | `iam:GetRole` `iam:ListAttachedRolePolicies` `iam:GetPolicy` `iam:GetPolicyVersion` `lambda:ListFunctions` `lambda:GetFunction` `lambda:UpdateFunctionConfiguration` `secretsmanager:GetSecretValue` `secretsmanager:PutSecretValue` `secretsmanager:UpdateSecret` `ssm:PutParameter` `sns:Publish` `comprehend:DetectPiiEntities` `logs:DescribeLogGroups` `logs:FilterLogEvents` `ec2:DescribeSecurityGroups` `ec2:RevokeSecurityGroupIngress` `dynamodb:DescribeTable` `dynamodb:UpdateTable` `sqs:GetQueueAttributes` `sqs:SetQueueAttributes` `sns:GetTopicAttributes` `sns:SetTopicAttributes` `s3:GetBucketEncryption` `s3:PutBucketEncryption` `s3:GetBucketPolicy` `s3:GetBucketPublicAccessBlock` `kms:DescribeKey` `kms:GetKeyPolicy` `lambda:GetPolicy` `wafv2:AssociateWebACL` `wafv2:DisassociateWebACL` `cognito-idp:SignUp` `cognito-idp:InitiateAuth` `cognito-idp:ForgotPassword` `cognito-idp:ConfirmForgotPassword` `cognito-idp:RespondToAuthChallenge` |
| cost_optimization | `lambda:GetFunctionConfiguration` `lambda:UpdateFunctionConfiguration` `lambda:InvokeFunction` `lambda:ListFunctions` `cloudwatch:GetMetricStatistics` `sqs:ListQueues` `sqs:GetQueueAttributes` `logs:DescribeLogGroups` `logs:PutRetentionPolicy` `dynamodb:DescribeTable` `tag:GetResources` `tag:TagResources` |
| testing_dev | `lambda:InvokeFunction` `lambda:CreateEventSourceMapping` `cloudformation:CreateStack` `cloudformation:DescribeStacks` `cloudformation:DeleteStack` `dynamodb:BatchWriteItem` `sqs:CreateQueue` `sqs:GetQueueAttributes` `sqs:ReceiveMessage` `s3:CreateBucket` `s3:PutObject` `s3:GetObject` `s3:PutBucketNotificationConfiguration` `sns:Publish` |
| config_state | `ssm:GetParametersByPath` `secretsmanager:GetSecretValue` `dynamodb:PutItem` `dynamodb:GetItem` `dynamodb:DeleteItem` `sts:AssumeRole` `lambda:GetFunctionConfiguration` `lambda:UpdateFunctionConfiguration` `appconfig:GetLatestConfiguration` `appconfig:StartConfigurationSession` |
| blue_green | `ecs:CreateService` `ecs:UpdateService` `ecs:DescribeServices` `elasticloadbalancing:DescribeListeners` `elasticloadbalancing:ModifyListener` `elasticloadbalancing:CreateTargetGroup` `elasticloadbalancing:DescribeTargetGroups` `route53:ChangeResourceRecordSets` `route53:GetHealthCheckStatus` `cloudwatch:DescribeAlarms` `cloudwatch:PutMetricAlarm` `sns:Publish` `lambda:GetAlias` `lambda:CreateAlias` `application-autoscaling:RegisterScalableTarget` `application-autoscaling:PutScalingPolicy` `application-autoscaling:PutScheduledAction` |
| cross_account | `sts:AssumeRole` `events:PutPermission` `events:PutRule` `events:PutTargets` `events:PutEvents` `firehose:CreateDeliveryStream` `logs:PutDestination` `logs:PutDestinationPolicy` `logs:DescribeDestinations` `logs:DescribeLogGroups` `logs:PutSubscriptionFilter` `s3:GetBucketLifecycleConfiguration` `s3:PutBucketLifecycleConfiguration` `s3:PutObject` `dynamodb:BatchWriteItem` `tag:GetResources` |

---

## License

MIT
