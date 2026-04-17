"""Cost Optimization utilities for serverless architectures.

Provides helpers for reducing and managing AWS costs:

- **Lambda right-sizer** — Invoke Lambda at multiple memory configs,
  measure duration/cost, recommend optimal.
- **Unused resource finder** — Find idle Lambda functions, empty SQS
  queues, orphaned log groups.
- **Concurrency optimizer** — Analyze Lambda concurrency metrics,
  recommend reserved/provisioned settings.
- **Cost attribution tagger** — Ensure cost-allocation tags on all
  serverless resources.
- **DynamoDB capacity advisor** — Analyze consumed vs provisioned
  DynamoDB capacity, recommend on-demand or adjustments.
- **Log retention enforcer** — Set CloudWatch Logs retention policies
  across all Lambda log groups.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "CURAnalysisResult",
    "ConcurrencyOptimizerResult",
    "ConcurrencyRecommendation",
    "CostAttributionTaggerResult",
    "DeadCodeResult",
    "DynamoDBCapacityAdvice",
    "DynamoDBCapacityAdvisorResult",
    "ECRPolicyResult",
    "IdleInstanceResult",
    "IdleRDSResult",
    "LambdaRightSizerResult",
    "LogRetentionChange",
    "LogRetentionEnforcerResult",
    "MemoryConfig",
    "SPCoverageResult",
    "TagComplianceResource",
    "TieringResult",
    "TrustedAdvisorResult",
    "UnusedResource",
    "UnusedResourceFinderResult",
    "concurrency_optimizer",
    "cost_and_usage_report_analyzer",
    "cost_attribution_tagger",
    "dynamodb_capacity_advisor",
    "ec2_idle_instance_stopper",
    "ecr_lifecycle_policy_applier",
    "lambda_dead_code_detector",
    "lambda_right_sizer",
    "log_retention_enforcer",
    "rds_idle_snapshot_and_delete",
    "s3_intelligent_tiering_enrollor",
    "savings_plan_coverage_reporter",
    "trusted_advisor_report_to_s3",
    "unused_resource_finder",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class MemoryConfig(BaseModel):
    """Result of a single Lambda memory configuration test."""

    model_config = ConfigDict(frozen=True)

    memory_mb: int
    avg_duration_ms: float
    estimated_cost_per_invocation: float


class LambdaRightSizerResult(BaseModel):
    """Result of Lambda right-sizing analysis."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    configurations: list[MemoryConfig] = []
    recommended_memory_mb: int = 128
    estimated_savings_pct: float = 0.0


class UnusedResource(BaseModel):
    """A single unused or idle resource."""

    model_config = ConfigDict(frozen=True)

    resource_type: str
    resource_id: str
    reason: str


class UnusedResourceFinderResult(BaseModel):
    """Result of scanning for unused resources."""

    model_config = ConfigDict(frozen=True)

    idle_lambdas: list[UnusedResource] = []
    empty_queues: list[UnusedResource] = []
    orphaned_log_groups: list[UnusedResource] = []
    total_found: int = 0


class ConcurrencyRecommendation(BaseModel):
    """Concurrency recommendation for a Lambda function."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    max_concurrent: int = 0
    avg_concurrent: float = 0.0
    recommended_reserved: int = 0
    recommendation: str = ""


class ConcurrencyOptimizerResult(BaseModel):
    """Result of concurrency optimization analysis."""

    model_config = ConfigDict(frozen=True)

    functions: list[ConcurrencyRecommendation] = []
    total_analyzed: int = 0


class TagComplianceResource(BaseModel):
    """A resource with its tag compliance status."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str
    resource_type: str
    missing_tags: list[str] = []
    compliant: bool = True


class CostAttributionTaggerResult(BaseModel):
    """Result of cost-allocation tag enforcement."""

    model_config = ConfigDict(frozen=True)

    resources_checked: int = 0
    resources_tagged: int = 0
    already_compliant: int = 0
    failures: list[str] = []


class DynamoDBCapacityAdvice(BaseModel):
    """Capacity advice for a single DynamoDB table."""

    model_config = ConfigDict(frozen=True)

    table_name: str
    billing_mode: str = ""
    provisioned_rcu: int = 0
    provisioned_wcu: int = 0
    consumed_rcu: float = 0.0
    consumed_wcu: float = 0.0
    recommendation: str = ""


class DynamoDBCapacityAdvisorResult(BaseModel):
    """Result of DynamoDB capacity analysis."""

    model_config = ConfigDict(frozen=True)

    tables: list[DynamoDBCapacityAdvice] = []
    total_analyzed: int = 0


class LogRetentionChange(BaseModel):
    """A single log group retention change."""

    model_config = ConfigDict(frozen=True)

    log_group: str
    previous_retention_days: int | None = None
    new_retention_days: int


class LogRetentionEnforcerResult(BaseModel):
    """Result of log retention enforcement."""

    model_config = ConfigDict(frozen=True)

    groups_updated: int = 0
    groups_already_compliant: int = 0
    changes: list[LogRetentionChange] = []
    failures: list[str] = []


# ---------------------------------------------------------------------------
# 1. Lambda Right-Sizer
# ---------------------------------------------------------------------------


def lambda_right_sizer(
    function_name: str,
    memory_configs: list[int] | None = None,
    invocations_per_config: int = 5,
    region_name: str | None = None,
) -> LambdaRightSizerResult:
    """Invoke Lambda at multiple memory configs and recommend optimal.

    Measures duration and estimates cost for each memory configuration,
    then recommends the most cost-effective setting.

    Args:
        function_name: Name or ARN of the Lambda function.
        memory_configs: List of memory sizes in MB to test.  Defaults
            to ``[128, 256, 512, 1024]``.
        invocations_per_config: Number of invocations per config for
            averaging (default 5).
        region_name: AWS region override.

    Returns:
        A :class:`LambdaRightSizerResult` with recommendations.

    Raises:
        RuntimeError: If retrieving function config or CloudWatch
            metrics fails.
    """
    if memory_configs is None:
        memory_configs = [128, 256, 512, 1024]

    lam = get_client("lambda", region_name=region_name)
    cw = get_client("cloudwatch", region_name=region_name)

    # Read original memory so we can restore
    try:
        func_config = lam.get_function_configuration(
            FunctionName=function_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get config for {function_name}") from exc

    original_memory = func_config["MemorySize"]
    configs: list[MemoryConfig] = []
    best_cost = float("inf")
    best_memory = memory_configs[0]

    for mem in memory_configs:
        # Update memory
        try:
            lam.update_function_configuration(
                FunctionName=function_name,
                MemorySize=mem,
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to update {function_name} to {mem}MB") from exc

        # Invoke N times
        durations: list[float] = []
        for _ in range(invocations_per_config):
            try:
                resp = lam.invoke(
                    FunctionName=function_name,
                    InvocationType="RequestResponse",
                    Payload=b"{}",
                )
                # Duration from CloudWatch is more accurate, but
                # we also read the billed duration from the response
                # log for approximation
                dur = (
                    resp.get("ResponseMetadata", {})
                    .get("HTTPHeaders", {})
                    .get("x-amz-log-result", "0")
                )
                durations.append(float(dur) if dur != "0" else 100.0)
            except ClientError as exc:
                raise wrap_aws_error(exc, f"Failed to invoke {function_name}") from exc

        # Query CloudWatch for average duration
        end_time = datetime.now(tz=UTC)
        start_time = end_time - timedelta(minutes=5)
        try:
            metrics = cw.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Duration",
                Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Average"],
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get metrics for {function_name}") from exc

        datapoints = metrics.get("Datapoints", [])
        if datapoints:
            avg_dur = datapoints[0].get("Average", 100.0)
        else:
            avg_dur = sum(durations) / len(durations) if durations else 100.0

        # Cost model: price per 1ms per GB
        gb_seconds = (mem / 1024.0) * (avg_dur / 1000.0)
        cost = gb_seconds * 0.0000166667  # ~$0.0000166667 per GB-s

        mc = MemoryConfig(
            memory_mb=mem,
            avg_duration_ms=round(avg_dur, 2),
            estimated_cost_per_invocation=round(cost, 10),
        )
        configs.append(mc)

        if cost < best_cost:
            best_cost = cost
            best_memory = mem

    # Restore original memory
    try:
        lam.update_function_configuration(
            FunctionName=function_name,
            MemorySize=original_memory,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to restore {function_name} to {original_memory}MB"
        ) from exc

    # Calculate savings
    original_config = next((c for c in configs if c.memory_mb == original_memory), None)
    if original_config and original_config.estimated_cost_per_invocation:
        savings = (1.0 - best_cost / original_config.estimated_cost_per_invocation) * 100.0
    else:
        savings = 0.0

    logger.info(
        "Right-sizer: %s recommended %dMB (%.1f%% savings)",
        function_name,
        best_memory,
        savings,
    )
    return LambdaRightSizerResult(
        function_name=function_name,
        configurations=configs,
        recommended_memory_mb=best_memory,
        estimated_savings_pct=round(max(savings, 0.0), 2),
    )


# ---------------------------------------------------------------------------
# 2. Unused Resource Finder
# ---------------------------------------------------------------------------


def unused_resource_finder(
    days_inactive: int = 30,
    region_name: str | None = None,
) -> UnusedResourceFinderResult:
    """Find idle Lambda functions, empty SQS queues, orphaned log groups.

    Scans multiple services to identify resources that are unused or
    idle and could be cleaned up to reduce costs.

    Args:
        days_inactive: Number of days of inactivity to consider a
            resource idle (default 30).
        region_name: AWS region override.

    Returns:
        An :class:`UnusedResourceFinderResult` with all found resources.

    Raises:
        RuntimeError: If listing resources fails.
    """
    lam = get_client("lambda", region_name=region_name)
    sqs = get_client("sqs", region_name=region_name)
    logs = get_client("logs", region_name=region_name)

    idle_lambdas: list[UnusedResource] = []
    empty_queues: list[UnusedResource] = []
    orphaned_log_groups: list[UnusedResource] = []

    # --- Idle Lambda functions ---
    try:
        funcs_resp = lam.list_functions()
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list Lambda functions") from exc

    cutoff = datetime.now(tz=UTC) - timedelta(days=days_inactive)
    for func in funcs_resp.get("Functions", []):
        last_modified = func.get("LastModified", "")
        if last_modified:
            # Lambda returns ISO-8601 timestamps
            try:
                mod_dt = datetime.fromisoformat(last_modified.replace("+0000", "+00:00"))
                if mod_dt < cutoff:
                    idle_lambdas.append(
                        UnusedResource(
                            resource_type="Lambda",
                            resource_id=func["FunctionName"],
                            reason=(f"Not modified in {days_inactive} days"),
                        )
                    )
            except (ValueError, TypeError):
                pass  # Skip unparseable dates

    # --- Empty SQS queues ---
    try:
        queues_resp = sqs.list_queues()
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list SQS queues") from exc

    for queue_url in queues_resp.get("QueueUrls", []):
        try:
            attrs = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=["ApproximateNumberOfMessages"],
            )
            count = int(attrs.get("Attributes", {}).get("ApproximateNumberOfMessages", "0"))
            if count == 0:
                empty_queues.append(
                    UnusedResource(
                        resource_type="SQS",
                        resource_id=queue_url,
                        reason="Queue is empty",
                    )
                )
        except ClientError:
            pass  # Skip inaccessible queues

    # --- Orphaned log groups ---
    try:
        log_groups_resp = logs.describe_log_groups()
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list log groups") from exc

    lambda_names = {f.get("FunctionName", "") for f in funcs_resp.get("Functions", [])}
    for lg in log_groups_resp.get("logGroups", []):
        name = lg.get("logGroupName", "")
        if name.startswith("/aws/lambda/"):
            fn_name = name.replace("/aws/lambda/", "")
            if fn_name not in lambda_names:
                orphaned_log_groups.append(
                    UnusedResource(
                        resource_type="CloudWatchLogs",
                        resource_id=name,
                        reason=("Log group for non-existent Lambda function"),
                    )
                )

    total = len(idle_lambdas) + len(empty_queues) + len(orphaned_log_groups)
    logger.info("Unused resource finder: %d idle resources found", total)
    return UnusedResourceFinderResult(
        idle_lambdas=idle_lambdas,
        empty_queues=empty_queues,
        orphaned_log_groups=orphaned_log_groups,
        total_found=total,
    )


# ---------------------------------------------------------------------------
# 3. Concurrency Optimizer
# ---------------------------------------------------------------------------


def concurrency_optimizer(
    function_names: list[str],
    lookback_minutes: int = 60,
    region_name: str | None = None,
) -> ConcurrencyOptimizerResult:
    """Analyze Lambda concurrency metrics and recommend settings.

    Queries CloudWatch for concurrency metrics across the given
    Lambda functions and recommends reserved or provisioned
    concurrency settings.

    Args:
        function_names: List of Lambda function names to analyze.
        lookback_minutes: Minutes of history to analyze (default 60).
        region_name: AWS region override.

    Returns:
        A :class:`ConcurrencyOptimizerResult` with recommendations.

    Raises:
        RuntimeError: If querying CloudWatch metrics fails.
    """
    cw = get_client("cloudwatch", region_name=region_name)
    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(minutes=lookback_minutes)

    recommendations: list[ConcurrencyRecommendation] = []
    for fn in function_names:
        try:
            resp = cw.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="ConcurrentExecutions",
                Dimensions=[
                    {"Name": "FunctionName", "Value": fn},
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Maximum", "Average"],
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get concurrency metrics for {fn}") from exc

        datapoints = resp.get("Datapoints", [])
        if datapoints:
            max_conc = max(int(dp.get("Maximum", 0)) for dp in datapoints)
            avg_conc = sum(dp.get("Average", 0.0) for dp in datapoints) / len(datapoints)
        else:
            max_conc = 0
            avg_conc = 0.0

        # Recommendation logic
        if max_conc == 0:
            rec = "No concurrency data; consider unreserved."
            reserved = 0
        elif max_conc < 5:
            rec = "Low concurrency; unreserved is sufficient."
            reserved = 0
        elif max_conc < 50:
            rec = (
                f"Moderate concurrency (max={max_conc}); "
                f"consider reserved concurrency of {max_conc + 10}."
            )
            reserved = max_conc + 10
        else:
            rec = (
                f"High concurrency (max={max_conc}); "
                f"consider provisioned concurrency of "
                f"{int(avg_conc) + 10}."
            )
            reserved = int(avg_conc) + 10

        recommendations.append(
            ConcurrencyRecommendation(
                function_name=fn,
                max_concurrent=max_conc,
                avg_concurrent=round(avg_conc, 2),
                recommended_reserved=reserved,
                recommendation=rec,
            )
        )

    logger.info(
        "Concurrency optimizer: analyzed %d functions",
        len(function_names),
    )
    return ConcurrencyOptimizerResult(
        functions=recommendations,
        total_analyzed=len(function_names),
    )


# ---------------------------------------------------------------------------
# 4. Cost Attribution Tagger
# ---------------------------------------------------------------------------


def cost_attribution_tagger(
    resource_arns: list[str],
    required_tags: dict[str, str],
    region_name: str | None = None,
) -> CostAttributionTaggerResult:
    """Ensure cost-allocation tags on serverless resources.

    Checks each resource for the required tags and applies any that
    are missing using the Resource Groups Tagging API.

    Args:
        resource_arns: List of resource ARNs to check and tag.
        required_tags: Dict of tag key-value pairs that must be present.
        region_name: AWS region override.

    Returns:
        A :class:`CostAttributionTaggerResult` with compliance summary.

    Raises:
        RuntimeError: If the tagging API calls fail.
    """
    tagging = get_client("resourcegroupstaggingapi", region_name=region_name)

    checked = 0
    tagged = 0
    compliant = 0
    failures: list[str] = []

    for arn in resource_arns:
        checked += 1
        try:
            resp = tagging.get_resources(
                TagFilters=[],
                ResourceARNList=[arn],
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get tags for {arn}") from exc

        resource_list = resp.get("ResourceTagMappingList", [])
        existing_tags: dict[str, str] = {}
        if resource_list:
            for tag in resource_list[0].get("Tags", []):
                existing_tags[tag["Key"]] = tag["Value"]

        missing: dict[str, str] = {}
        for key, value in required_tags.items():
            if key not in existing_tags:
                missing[key] = value

        if not missing:
            compliant += 1
            continue

        # Apply missing tags
        tags_to_apply = {**existing_tags, **missing}
        try:
            resp = tagging.tag_resources(
                ResourceARNList=[arn],
                Tags=tags_to_apply,
            )
        except ClientError as exc:
            failures.append(f"{arn}: {exc}")
            continue

        failed = resp.get("FailedResourcesMap", {})
        if failed:
            failures.append(f"{arn}: tagging partially failed")
        else:
            tagged += 1

    logger.info(
        "Cost attribution tagger: %d checked, %d tagged, %d compliant, %d failures",
        checked,
        tagged,
        compliant,
        len(failures),
    )
    return CostAttributionTaggerResult(
        resources_checked=checked,
        resources_tagged=tagged,
        already_compliant=compliant,
        failures=failures,
    )


# ---------------------------------------------------------------------------
# 5. DynamoDB Capacity Advisor
# ---------------------------------------------------------------------------


def dynamodb_capacity_advisor(
    table_names: list[str],
    lookback_minutes: int = 60,
    region_name: str | None = None,
) -> DynamoDBCapacityAdvisorResult:
    """Analyze DynamoDB capacity and recommend billing mode adjustments.

    Compares provisioned throughput against consumed capacity from
    CloudWatch metrics, recommending on-demand or adjusted provisioned
    capacity.

    Args:
        table_names: List of DynamoDB table names to analyze.
        lookback_minutes: Minutes of history to analyze (default 60).
        region_name: AWS region override.

    Returns:
        A :class:`DynamoDBCapacityAdvisorResult` with recommendations.

    Raises:
        RuntimeError: If describing tables or querying metrics fails.
    """
    ddb = get_client("dynamodb", region_name=region_name)
    cw = get_client("cloudwatch", region_name=region_name)

    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(minutes=lookback_minutes)

    tables: list[DynamoDBCapacityAdvice] = []

    for table_name in table_names:
        # Describe table to get provisioned throughput
        try:
            desc = ddb.describe_table(TableName=table_name)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe table {table_name}") from exc

        table_info = desc["Table"]
        billing = table_info.get("BillingModeSummary", {}).get("BillingMode", "PROVISIONED")
        throughput = table_info.get("ProvisionedThroughput", {})
        prov_rcu = int(throughput.get("ReadCapacityUnits", 0))
        prov_wcu = int(throughput.get("WriteCapacityUnits", 0))

        # Get consumed RCU
        consumed_rcu = 0.0
        try:
            rcu_resp = cw.get_metric_statistics(
                Namespace="AWS/DynamoDB",
                MetricName="ConsumedReadCapacityUnits",
                Dimensions=[
                    {"Name": "TableName", "Value": table_name},
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )
            rcu_dps = rcu_resp.get("Datapoints", [])
            if rcu_dps:
                consumed_rcu = sum(dp.get("Sum", 0.0) for dp in rcu_dps) / len(rcu_dps)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get RCU metrics for {table_name}") from exc

        # Get consumed WCU
        consumed_wcu = 0.0
        try:
            wcu_resp = cw.get_metric_statistics(
                Namespace="AWS/DynamoDB",
                MetricName="ConsumedWriteCapacityUnits",
                Dimensions=[
                    {"Name": "TableName", "Value": table_name},
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"],
            )
            wcu_dps = wcu_resp.get("Datapoints", [])
            if wcu_dps:
                consumed_wcu = sum(dp.get("Sum", 0.0) for dp in wcu_dps) / len(wcu_dps)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get WCU metrics for {table_name}") from exc

        # Recommendation logic
        if billing == "PAY_PER_REQUEST":
            recommendation = "Already using on-demand billing; no change needed."
        elif prov_rcu == 0 and prov_wcu == 0:
            recommendation = "Provisioned at zero; consider on-demand billing."
        else:
            rcu_util = consumed_rcu / prov_rcu if prov_rcu > 0 else 0.0
            wcu_util = consumed_wcu / prov_wcu if prov_wcu > 0 else 0.0
            if rcu_util < 0.2 and wcu_util < 0.2:
                recommendation = (
                    "Very low utilization; switch to on-demand or reduce provisioned capacity."
                )
            elif rcu_util > 0.8 or wcu_util > 0.8:
                recommendation = (
                    "High utilization; consider increasing provisioned capacity or auto-scaling."
                )
            else:
                recommendation = "Utilization is moderate; current settings are reasonable."

        tables.append(
            DynamoDBCapacityAdvice(
                table_name=table_name,
                billing_mode=billing,
                provisioned_rcu=prov_rcu,
                provisioned_wcu=prov_wcu,
                consumed_rcu=round(consumed_rcu, 2),
                consumed_wcu=round(consumed_wcu, 2),
                recommendation=recommendation,
            )
        )

    logger.info(
        "DynamoDB capacity advisor: analyzed %d tables",
        len(table_names),
    )
    return DynamoDBCapacityAdvisorResult(
        tables=tables,
        total_analyzed=len(table_names),
    )


# ---------------------------------------------------------------------------
# 6. Log Retention Enforcer
# ---------------------------------------------------------------------------


def log_retention_enforcer(
    retention_days: int = 30,
    log_group_prefix: str = "/aws/lambda/",
    region_name: str | None = None,
) -> LogRetentionEnforcerResult:
    """Set CloudWatch Logs retention across Lambda log groups.

    Scans log groups matching the given prefix and ensures each has
    a retention policy of at most *retention_days*.  Groups with
    no retention (infinite) or a longer retention are updated.

    Args:
        retention_days: Desired maximum retention in days (default 30).
            Must be a valid CloudWatch Logs retention value.
        log_group_prefix: Prefix to filter log groups (default
            ``/aws/lambda/``).
        region_name: AWS region override.

    Returns:
        A :class:`LogRetentionEnforcerResult` with change details.

    Raises:
        RuntimeError: If listing or updating log groups fails.
    """
    logs = get_client("logs", region_name=region_name)
    changes: list[LogRetentionChange] = []
    failures: list[str] = []
    updated = 0
    compliant = 0

    try:
        resp = logs.describe_log_groups(
            logGroupNamePrefix=log_group_prefix,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list log groups") from exc

    for lg in resp.get("logGroups", []):
        name = lg.get("logGroupName", "")
        current = lg.get("retentionInDays")

        if current is not None and current <= retention_days:
            compliant += 1
            continue

        try:
            logs.put_retention_policy(
                logGroupName=name,
                retentionInDays=retention_days,
            )
        except ClientError as exc:
            failures.append(f"{name}: {exc}")
            continue

        changes.append(
            LogRetentionChange(
                log_group=name,
                previous_retention_days=current,
                new_retention_days=retention_days,
            )
        )
        updated += 1

    logger.info(
        "Log retention enforcer: %d updated, %d compliant, %d failures",
        updated,
        compliant,
        len(failures),
    )
    return LogRetentionEnforcerResult(
        groups_updated=updated,
        groups_already_compliant=compliant,
        changes=changes,
        failures=failures,
    )


# ---------------------------------------------------------------------------
# 7. Trusted Advisor report to S3
# ---------------------------------------------------------------------------


class TrustedAdvisorResult(BaseModel):
    """Result of pulling Trusted Advisor data and uploading to S3."""

    model_config = ConfigDict(frozen=True)

    checks_count: int
    flagged_resources: int
    s3_key: str
    alerts_sent: int


def trusted_advisor_report_to_s3(
    bucket: str,
    report_key: str,
    sns_topic_arn: str | None = None,
    check_categories: list[str] | None = None,
    region_name: str | None = None,
) -> TrustedAdvisorResult:
    """Pull Trusted Advisor check results, upload to S3, alert via SNS.

    Enumerates all Trusted Advisor checks (optionally filtered by category),
    fetches each check result, uploads the combined JSON report to S3, and
    publishes SNS messages for checks with ``"error"`` or ``"warning"`` status.

    Args:
        bucket: S3 bucket for the report.
        report_key: S3 object key to write the JSON report to.
        sns_topic_arn: Optional SNS topic for high-severity alerts.
        check_categories: Optional list of category names to filter checks.
        region_name: AWS region override (must be ``us-east-1`` for Support API).

    Returns:
        A :class:`TrustedAdvisorResult` with check counts and S3 key.

    Raises:
        RuntimeError: If Support, S3, or SNS calls fail.
    """
    import json as _json

    support = get_client("support", region_name or "us-east-1")
    s3 = get_client("s3", region_name)

    try:
        checks_resp = support.describe_trusted_advisor_checks(language="en")
        all_checks = checks_resp.get("checks", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, "trusted_advisor_report_to_s3 describe_checks failed") from exc

    if check_categories:
        all_checks = [c for c in all_checks if c.get("category") in check_categories]

    report: list[dict] = []
    flagged = 0
    alerts_sent = 0

    for check in all_checks:
        check_id = check["id"]
        try:
            result_resp = support.describe_trusted_advisor_check_result(
                checkId=check_id, language="en"
            )
            result = result_resp.get("result", {})
            status = result.get("status", "ok")
            flagged_resources = result.get("flaggedResources", [])
            flagged += len(flagged_resources)
            report.append({"check": check, "result": result})

            if status in ("error", "warning") and sns_topic_arn:
                sns = get_client("sns", region_name)
                try:
                    sns.publish(
                        TopicArn=sns_topic_arn,
                        Subject=f"Trusted Advisor Alert: {check.get('name', check_id)}",
                        Message=_json.dumps(
                            {
                                "check_name": check.get("name"),
                                "status": status,
                                "flagged_resources": len(flagged_resources),
                            },
                            indent=2,
                        ),
                    )
                    alerts_sent += 1
                except ClientError:
                    pass
        except ClientError:
            continue

    report_body = _json.dumps(
        {"checks": report, "generated_at": datetime.now(tz=UTC).isoformat()}, indent=2, default=str
    )
    try:
        s3.put_object(Bucket=bucket, Key=report_key, Body=report_body.encode())
    except ClientError as exc:
        raise wrap_aws_error(exc, "trusted_advisor_report_to_s3 s3 upload failed") from exc

    logger.info(
        "Trusted Advisor: %d checks, %d flagged, %d alerts", len(all_checks), flagged, alerts_sent
    )
    return TrustedAdvisorResult(
        checks_count=len(all_checks),
        flagged_resources=flagged,
        s3_key=report_key,
        alerts_sent=alerts_sent,
    )


# ---------------------------------------------------------------------------
# 8. Cost and usage report analyzer
# ---------------------------------------------------------------------------


class CURAnalysisResult(BaseModel):
    """Result of running a CUR Athena analysis."""

    model_config = ConfigDict(frozen=True)

    query_execution_id: str
    services_analyzed: int
    anomalies_found: int
    alert_sent: bool


def cost_and_usage_report_analyzer(
    database: str,
    table: str,
    output_location: str,
    threshold_percent: float,
    sns_topic_arn: str,
    region_name: str | None = None,
) -> CURAnalysisResult:
    """Run Athena query on CUR data and push anomalies to SNS.

    Executes an aggregation SQL query on the CUR table via Athena, polls
    for completion, flags services whose cost exceeds ``threshold_percent``
    of the total spend, and publishes an SNS alert if anomalies are found.

    Args:
        database: Athena database name.
        table: Athena/CUR table name.
        output_location: S3 URI for Athena query results (``s3://bucket/prefix/``).
        threshold_percent: Percent of total spend to flag a service as anomalous.
        sns_topic_arn: SNS topic ARN for anomaly alerts.
        region_name: AWS region override.

    Returns:
        A :class:`CURAnalysisResult` with query ID and anomaly counts.

    Raises:
        RuntimeError: If Athena query or SNS publish fails.
    """
    import json as _json
    import time

    athena = get_client("athena", region_name)
    sns = get_client("sns", region_name)

    sql = (
        f"SELECT line_item_product_code, SUM(line_item_unblended_cost) AS total_cost "
        f"FROM {database}.{table} "
        f"GROUP BY line_item_product_code ORDER BY total_cost DESC"
    )

    try:
        start_resp = athena.start_query_execution(
            QueryString=sql,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
        )
        execution_id = start_resp["QueryExecutionId"]
    except ClientError as exc:
        raise wrap_aws_error(exc, "cost_and_usage_report_analyzer start_query failed") from exc

    # Poll until completion (max ~5 minutes)
    for _ in range(60):
        try:
            status_resp = athena.get_query_execution(QueryExecutionId=execution_id)
            state = status_resp["QueryExecution"]["Status"]["State"]
            if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
                break
        except ClientError as exc:
            raise wrap_aws_error(
                exc, "cost_and_usage_report_analyzer get_query_execution failed"
            ) from exc
        time.sleep(5)
    else:
        raise RuntimeError("cost_and_usage_report_analyzer: Athena query timed out")

    if state != "SUCCEEDED":
        raise RuntimeError(f"cost_and_usage_report_analyzer: query ended with state {state!r}")

    try:
        results_resp = athena.get_query_results(QueryExecutionId=execution_id)
        rows = results_resp.get("ResultSet", {}).get("Rows", [])
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "cost_and_usage_report_analyzer get_query_results failed"
        ) from exc

    # Skip header row; compute total spend
    data_rows = rows[1:] if len(rows) > 1 else []
    total_spend = sum(float(r["Data"][1].get("VarCharValue", "0") or "0") for r in data_rows)
    anomalies: list[str] = []
    for row in data_rows:
        service = row["Data"][0].get("VarCharValue", "unknown")
        cost = float(row["Data"][1].get("VarCharValue", "0") or "0")
        if total_spend > 0 and (cost / total_spend * 100) > threshold_percent:
            anomalies.append(f"{service}: ${cost:.2f}")

    alert_sent = False
    if anomalies:
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=f"CUR Anomaly: {len(anomalies)} service(s) exceed {threshold_percent}% threshold",
                Message=_json.dumps({"anomalies": anomalies, "total_spend": total_spend}, indent=2),
            )
            alert_sent = True
        except ClientError as exc:
            raise wrap_aws_error(exc, "cost_and_usage_report_analyzer SNS publish failed") from exc

    logger.info("CUR analyzer: %d services, %d anomalies", len(data_rows), len(anomalies))
    return CURAnalysisResult(
        query_execution_id=execution_id,
        services_analyzed=len(data_rows),
        anomalies_found=len(anomalies),
        alert_sent=alert_sent,
    )


# ---------------------------------------------------------------------------
# 9. Savings Plans coverage reporter
# ---------------------------------------------------------------------------


class SPCoverageResult(BaseModel):
    """Result of Savings Plans coverage reporting."""

    model_config = ConfigDict(frozen=True)

    coverage_percent: float
    total_spend: float
    covered_spend: float
    s3_key: str


def savings_plan_coverage_reporter(
    bucket: str,
    report_key: str,
    start_date: str,
    end_date: str,
    metric_namespace: str,
    region_name: str | None = None,
) -> SPCoverageResult:
    """Query Cost Explorer for Savings Plans coverage and report to S3 + CloudWatch.

    Fetches coverage data for the given date range, uploads a JSON summary
    to S3, and publishes the coverage percentage as a CloudWatch custom metric.

    Args:
        bucket: S3 bucket for the report.
        report_key: S3 object key for the JSON summary.
        start_date: Coverage period start date (``YYYY-MM-DD``).
        end_date: Coverage period end date (``YYYY-MM-DD``).
        metric_namespace: CloudWatch namespace for the coverage metric.
        region_name: AWS region override.

    Returns:
        A :class:`SPCoverageResult` with coverage percentage and spend figures.

    Raises:
        RuntimeError: If Cost Explorer, S3, or CloudWatch calls fail.
    """
    import json as _json

    ce = get_client("ce", region_name)
    s3 = get_client("s3", region_name)
    cw = get_client("cloudwatch", region_name)

    try:
        resp = ce.get_savings_plans_coverage(
            TimePeriod={"Start": start_date, "End": end_date},
            Granularity="MONTHLY",
        )
        coverages = resp.get("SavingsPlansCoverages", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, "savings_plan_coverage_reporter get_coverage failed") from exc

    total_spend = 0.0
    covered_spend = 0.0
    for cov in coverages:
        metrics = cov.get("Coverage", {})
        total_spend += float(metrics.get("TotalCost", {}).get("Amount", "0") or "0")
        covered_spend += float(metrics.get("CoveredCost", {}).get("Amount", "0") or "0")

    coverage_pct = (covered_spend / total_spend * 100.0) if total_spend > 0 else 0.0

    report = _json.dumps(
        {
            "start_date": start_date,
            "end_date": end_date,
            "coverage_percent": round(coverage_pct, 2),
            "total_spend": round(total_spend, 4),
            "covered_spend": round(covered_spend, 4),
        },
        indent=2,
    )
    try:
        s3.put_object(Bucket=bucket, Key=report_key, Body=report.encode())
    except ClientError as exc:
        raise wrap_aws_error(exc, "savings_plan_coverage_reporter s3 upload failed") from exc

    try:
        cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    "MetricName": "SavingsPlanCoveragePercent",
                    "Value": coverage_pct,
                    "Unit": "Percent",
                }
            ],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "savings_plan_coverage_reporter put_metric_data failed") from exc

    logger.info(
        "SP coverage: %.1f%% (total=%.2f, covered=%.2f)", coverage_pct, total_spend, covered_spend
    )
    return SPCoverageResult(
        coverage_percent=round(coverage_pct, 2),
        total_spend=round(total_spend, 4),
        covered_spend=round(covered_spend, 4),
        s3_key=report_key,
    )


# ---------------------------------------------------------------------------
# 10. EC2 idle instance stopper
# ---------------------------------------------------------------------------


class IdleInstanceResult(BaseModel):
    """Result of EC2 idle instance detection and stopping."""

    model_config = ConfigDict(frozen=True)

    instances_checked: int
    idle_found: int
    stopped_count: int
    watched_count: int


def ec2_idle_instance_stopper(
    table_name: str,
    cpu_threshold: float = 5.0,
    grace_period_hours: int = 24,
    region_name: str | None = None,
) -> IdleInstanceResult:
    """Find EC2 instances with low CPU, tag in DynamoDB, stop after grace period.

    Checks average CPUUtilization for all running instances over the last
    hour. Instances below ``cpu_threshold``% are added to a DynamoDB watch
    list; if they are already in the watch list past ``grace_period_hours``,
    they are stopped.

    Args:
        table_name: DynamoDB table for the idle watch list.
        cpu_threshold: CPU % below which an instance is considered idle (default 5.0).
        grace_period_hours: Hours an instance must be on the watch list before stopping (default 24).
        region_name: AWS region override.

    Returns:
        An :class:`IdleInstanceResult` with check and action counts.

    Raises:
        RuntimeError: If EC2, CloudWatch, or DynamoDB calls fail.
    """
    import time

    ec2 = get_client("ec2", region_name)
    cw = get_client("cloudwatch", region_name)
    ddb = get_client("dynamodb", region_name)

    try:
        resp = ec2.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )
        instances = [i for r in resp.get("Reservations", []) for i in r.get("Instances", [])]
    except ClientError as exc:
        raise wrap_aws_error(exc, "ec2_idle_instance_stopper describe_instances failed") from exc

    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(hours=1)
    idle_found = 0
    stopped_count = 0
    watched_count = 0
    now_ts = int(time.time())
    grace_seconds = grace_period_hours * 3600

    for inst in instances:
        iid = inst["InstanceId"]
        try:
            metrics = cw.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": iid}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=["Average"],
            )
            dps = metrics.get("Datapoints", [])
            avg_cpu = sum(dp["Average"] for dp in dps) / len(dps) if dps else 100.0
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"ec2_idle_instance_stopper metrics failed for {iid}"
            ) from exc

        if avg_cpu >= cpu_threshold:
            continue

        idle_found += 1
        # Check DynamoDB watch list
        try:
            ddb_resp = ddb.get_item(TableName=table_name, Key={"pk": {"S": iid}})
            existing = ddb_resp.get("Item")
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"ec2_idle_instance_stopper ddb get_item failed for {iid}"
            ) from exc

        if existing:
            first_seen = int(existing.get("first_seen", {}).get("N", str(now_ts)))
            if (now_ts - first_seen) >= grace_seconds:
                try:
                    ec2.stop_instances(InstanceIds=[iid])
                    stopped_count += 1
                except ClientError as exc:
                    raise wrap_aws_error(
                        exc, f"ec2_idle_instance_stopper stop failed for {iid}"
                    ) from exc
        else:
            try:
                ddb.put_item(
                    TableName=table_name,
                    Item={
                        "pk": {"S": iid},
                        "first_seen": {"N": str(now_ts)},
                        "avg_cpu": {"N": str(round(avg_cpu, 2))},
                    },
                )
                watched_count += 1
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"ec2_idle_instance_stopper ddb put_item failed for {iid}"
                ) from exc

    logger.info(
        "EC2 idle stopper: checked=%d idle=%d stopped=%d watched=%d",
        len(instances),
        idle_found,
        stopped_count,
        watched_count,
    )
    return IdleInstanceResult(
        instances_checked=len(instances),
        idle_found=idle_found,
        stopped_count=stopped_count,
        watched_count=watched_count,
    )


# ---------------------------------------------------------------------------
# 11. RDS idle snapshot and delete
# ---------------------------------------------------------------------------


class IdleRDSResult(BaseModel):
    """Result of RDS idle instance snapshot and optional deletion."""

    model_config = ConfigDict(frozen=True)

    instances_checked: int
    idle_found: int
    snapshots_created: int
    deleted_count: int
    dry_run: bool


def rds_idle_snapshot_and_delete(
    lookback_days: int = 7,
    sns_topic_arn: str | None = None,
    dry_run: bool = True,
    region_name: str | None = None,
) -> IdleRDSResult:
    """Find zero-connection RDS instances, snapshot them, optionally delete.

    Queries CloudWatch for ``DatabaseConnections`` (sum) over the lookback
    period. Instances with zero connections get a final snapshot created;
    if ``dry_run`` is False they are also deleted.

    Args:
        lookback_days: Days of connection history to evaluate (default 7).
        sns_topic_arn: Optional SNS topic for notifications.
        dry_run: When True, snapshot but do not delete (default True).
        region_name: AWS region override.

    Returns:
        An :class:`IdleRDSResult` with action counts.

    Raises:
        RuntimeError: If RDS, CloudWatch, or SNS calls fail.
    """
    import time

    rds = get_client("rds", region_name)
    cw = get_client("cloudwatch", region_name)

    try:
        db_resp = rds.describe_db_instances()
        instances = db_resp.get("DBInstances", [])
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "rds_idle_snapshot_and_delete describe_db_instances failed"
        ) from exc

    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(days=lookback_days)
    idle_found = 0
    snapshots_created = 0
    deleted_count = 0

    for inst in instances:
        db_id = inst["DBInstanceIdentifier"]
        try:
            metrics = cw.get_metric_statistics(
                Namespace="AWS/RDS",
                MetricName="DatabaseConnections",
                Dimensions=[{"Name": "DBInstanceIdentifier", "Value": db_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=lookback_days * 86400,
                Statistics=["Sum"],
            )
            dps = metrics.get("Datapoints", [])
            total_connections = sum(dp["Sum"] for dp in dps) if dps else -1
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"rds_idle_snapshot_and_delete metrics failed for {db_id}"
            ) from exc

        if total_connections != 0:
            continue

        idle_found += 1
        snapshot_id = f"idle-final-{db_id}-{int(time.time())}"
        try:
            rds.create_db_snapshot(DBSnapshotIdentifier=snapshot_id, DBInstanceIdentifier=db_id)
            snapshots_created += 1
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"rds_idle_snapshot_and_delete create_snapshot failed for {db_id}"
            ) from exc

        if not dry_run:
            try:
                rds.delete_db_instance(
                    DBInstanceIdentifier=db_id,
                    SkipFinalSnapshot=True,
                )
                deleted_count += 1
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"rds_idle_snapshot_and_delete delete failed for {db_id}"
                ) from exc

        if sns_topic_arn:
            sns = get_client("sns", region_name)
            try:
                sns.publish(
                    TopicArn=sns_topic_arn,
                    Subject=f"RDS Idle Instance: {db_id}",
                    Message=f"Snapshot {snapshot_id} created. Deleted: {not dry_run}.",
                )
            except ClientError:
                pass

    logger.info(
        "RDS idle: checked=%d idle=%d snapshots=%d deleted=%d dry_run=%s",
        len(instances),
        idle_found,
        snapshots_created,
        deleted_count,
        dry_run,
    )
    return IdleRDSResult(
        instances_checked=len(instances),
        idle_found=idle_found,
        snapshots_created=snapshots_created,
        deleted_count=deleted_count,
        dry_run=dry_run,
    )


# ---------------------------------------------------------------------------
# 12. ECR lifecycle policy applier
# ---------------------------------------------------------------------------


class ECRPolicyResult(BaseModel):
    """Result of applying lifecycle policies to ECR repositories."""

    model_config = ConfigDict(frozen=True)

    repositories_updated: int
    already_configured: int
    errors: int


def ecr_lifecycle_policy_applier(
    table_name: str,
    max_image_count: int = 100,
    region_name: str | None = None,
) -> ECRPolicyResult:
    """Apply a standard lifecycle policy to all ECR repositories.

    Enumerates all ECR repositories, applies a lifecycle policy that caps
    images at ``max_image_count``, and records results in DynamoDB.

    Args:
        table_name: DynamoDB table to record policy application results.
        max_image_count: Maximum number of images to retain per repo (default 100).
        region_name: AWS region override.

    Returns:
        An :class:`ECRPolicyResult` with update counts.

    Raises:
        RuntimeError: If ECR or DynamoDB calls fail.
    """
    import json as _json
    import time

    ecr = get_client("ecr", region_name)
    ddb = get_client("dynamodb", region_name)

    lifecycle_policy = _json.dumps(
        {
            "rules": [
                {
                    "rulePriority": 1,
                    "description": f"Keep last {max_image_count} images",
                    "selection": {
                        "tagStatus": "any",
                        "countType": "imageCountMoreThan",
                        "countNumber": max_image_count,
                    },
                    "action": {"type": "expire"},
                }
            ]
        }
    )

    try:
        repos_resp = ecr.describe_repositories()
        repos = repos_resp.get("repositories", [])
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "ecr_lifecycle_policy_applier describe_repositories failed"
        ) from exc

    updated = 0
    already = 0
    errors = 0

    for repo in repos:
        repo_name = repo["repositoryName"]
        try:
            ecr.put_lifecycle_policy(
                repositoryName=repo_name,
                lifecyclePolicyText=lifecycle_policy,
            )
            updated += 1
            status = "updated"
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code == "LifecyclePolicyAlreadyExistsException":
                already += 1
                status = "already_configured"
            else:
                errors += 1
                status = f"error:{code}"

        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": repo_name},
                    "sk": {"S": str(int(time.time()))},
                    "status": {"S": status},
                    "max_image_count": {"N": str(max_image_count)},
                },
            )
        except ClientError:
            pass

    logger.info("ECR lifecycle: updated=%d already=%d errors=%d", updated, already, errors)
    return ECRPolicyResult(repositories_updated=updated, already_configured=already, errors=errors)


# ---------------------------------------------------------------------------
# 13. S3 Intelligent-Tiering enrollor
# ---------------------------------------------------------------------------


class TieringResult(BaseModel):
    """Result of enrolling S3 buckets in Intelligent-Tiering."""

    model_config = ConfigDict(frozen=True)

    buckets_checked: int
    buckets_enrolled: int
    already_enrolled: int


def s3_intelligent_tiering_enrollor(
    metric_namespace: str,
    archive_access_days: int = 90,
    deep_archive_days: int = 180,
    region_name: str | None = None,
) -> TieringResult:
    """Apply Intelligent-Tiering configuration to all S3 buckets.

    Iterates all buckets, applies an Intelligent-Tiering configuration with
    configurable archive/deep-archive transition days, and logs the enrollment
    count as a CloudWatch custom metric.

    Args:
        metric_namespace: CloudWatch namespace for the tiering metric.
        archive_access_days: Days before transitioning to Archive Access tier (default 90).
        deep_archive_days: Days before transitioning to Deep Archive Access tier (default 180).
        region_name: AWS region override.

    Returns:
        A :class:`TieringResult` with enrollment counts.

    Raises:
        RuntimeError: If S3 or CloudWatch calls fail.
    """
    s3 = get_client("s3", region_name)
    cw = get_client("cloudwatch", region_name)

    try:
        buckets = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    except ClientError as exc:
        raise wrap_aws_error(exc, "s3_intelligent_tiering_enrollor list_buckets failed") from exc

    tiering_id = "aws-util-intelligent-tiering"
    tiering_config = {
        "Id": tiering_id,
        "Status": "Enabled",
        "Tierings": [
            {"Days": archive_access_days, "AccessTier": "ARCHIVE_ACCESS"},
            {"Days": deep_archive_days, "AccessTier": "DEEP_ARCHIVE_ACCESS"},
        ],
    }

    enrolled = 0
    already = 0

    for bucket in buckets:
        try:
            s3.put_bucket_intelligent_tiering_configuration(
                Bucket=bucket,
                Id=tiering_id,
                IntelligentTieringConfiguration=tiering_config,
            )
            enrolled += 1
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code in ("NoSuchBucket",):
                continue
            already += 1  # treat other errors as already-configured for idempotency

    try:
        cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    "MetricName": "BucketsEnrolledInIntelligentTiering",
                    "Value": enrolled,
                    "Unit": "Count",
                }
            ],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "s3_intelligent_tiering_enrollor put_metric_data failed") from exc

    logger.info("S3 tiering: checked=%d enrolled=%d already=%d", len(buckets), enrolled, already)
    return TieringResult(
        buckets_checked=len(buckets), buckets_enrolled=enrolled, already_enrolled=already
    )


# ---------------------------------------------------------------------------
# 14. Lambda dead code detector
# ---------------------------------------------------------------------------


class DeadCodeResult(BaseModel):
    """Result of Lambda dead code detection."""

    model_config = ConfigDict(frozen=True)

    functions_checked: int
    dead_functions: int
    archived_count: int
    dead_function_names: list[str]


def lambda_dead_code_detector(
    lookback_days: int = 30,
    bucket: str | None = None,
    archive_prefix: str = "lambda-archive/",
    region_name: str | None = None,
) -> DeadCodeResult:
    """Find Lambda functions with zero invocations and optionally archive code to S3.

    Queries CloudWatch for ``Invocations`` sum over the lookback period. Functions
    with zero invocations are flagged; if a ``bucket`` is supplied, the function
    code is downloaded from the presigned URL and uploaded to S3.

    Args:
        lookback_days: Days of invocation history to check (default 30).
        bucket: Optional S3 bucket to archive dead function code into.
        archive_prefix: S3 key prefix for archived code (default ``"lambda-archive/"``).
        region_name: AWS region override.

    Returns:
        A :class:`DeadCodeResult` with dead function names and archive count.

    Raises:
        RuntimeError: If Lambda, CloudWatch, or S3 calls fail.
    """
    import urllib.request

    lam = get_client("lambda", region_name)
    cw = get_client("cloudwatch", region_name)

    try:
        funcs_resp = lam.list_functions()
        functions = funcs_resp.get("Functions", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, "lambda_dead_code_detector list_functions failed") from exc

    end_time = datetime.now(tz=UTC)
    start_time = end_time - timedelta(days=lookback_days)
    dead_names: list[str] = []
    archived_count = 0

    for func in functions:
        fn_name = func["FunctionName"]
        try:
            metrics = cw.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Invocations",
                Dimensions=[{"Name": "FunctionName", "Value": fn_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=lookback_days * 86400,
                Statistics=["Sum"],
            )
            dps = metrics.get("Datapoints", [])
            total_invocations = sum(dp["Sum"] for dp in dps) if dps else 0.0
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"lambda_dead_code_detector metrics failed for {fn_name}"
            ) from exc

        if total_invocations > 0:
            continue

        dead_names.append(fn_name)

        if bucket:
            try:
                fn_detail = lam.get_function(FunctionName=fn_name)
                code_url = fn_detail.get("Code", {}).get("Location", "")
                if code_url:
                    with urllib.request.urlopen(code_url) as response:
                        code_bytes = response.read()
                    s3 = get_client("s3", region_name)
                    s3_key = f"{archive_prefix}{fn_name}.zip"
                    s3.put_object(Bucket=bucket, Key=s3_key, Body=code_bytes)
                    archived_count += 1
            except (ClientError, Exception):
                pass  # archive failure is non-fatal

    logger.info(
        "Lambda dead code: checked=%d dead=%d archived=%d",
        len(functions),
        len(dead_names),
        archived_count,
    )
    return DeadCodeResult(
        functions_checked=len(functions),
        dead_functions=len(dead_names),
        archived_count=archived_count,
        dead_function_names=dead_names,
    )
