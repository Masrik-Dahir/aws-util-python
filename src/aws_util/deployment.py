"""deployment — Deployment & release management utilities.

Provides high-level functions for Lambda deployment workflows:

- **lambda_canary_deploy** — Publish new version, shift alias traffic gradually
  with auto-rollback on CloudWatch alarm breach.
- **lambda_layer_publisher** — Package a directory into a Lambda Layer ZIP,
  publish, and update functions to the new version.
- **stack_deployer** — Deploy CloudFormation/SAM stacks with change-set review,
  auto-rollback, and output capture.
- **environment_promoter** — Copy Lambda configs, env vars, and aliases across
  accounts/stages (dev -> staging -> prod).
- **lambda_warmer** — Create a scheduled EventBridge rule that invokes a Lambda
  with a no-op payload to avoid cold starts.
- **config_drift_detector** — Compare deployed Lambda/API Gateway configs against
  desired state in SSM/S3, report drift.
- **rollback_manager** — Detect error-rate spikes, auto-shift Lambda alias
  traffic to the previous stable version.
- **lambda_package_builder** — Bundle Python Lambda code + dependencies into
  a deployment ZIP, upload to S3.
"""

from __future__ import annotations

import contextlib
import io
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "AppRunnerDeployResult",
    "BatchJobResult",
    "BeanstalkRefreshResult",
    "CanaryDeployResult",
    "ConfigMapSyncResult",
    "DriftDetectionResult",
    "DriftReport",
    "EnvironmentPromoteResult",
    "ExecutionTrackerResult",
    "InvalidationLogResult",
    "LambdaWarmerResult",
    "LayerPublishResult",
    "NodeGroupScaleResult",
    "PackageBuildResult",
    "RollbackResult",
    "ScheduledActionResult",
    "StackDeployResult",
    "app_runner_auto_deployer",
    "autoscaling_scheduled_action_manager",
    "batch_job_monitor",
    "cloudfront_invalidation_with_logging",
    "config_drift_detector",
    "eks_config_map_sync",
    "eks_node_group_scaler",
    "elastic_beanstalk_env_refresher",
    "environment_promoter",
    "lambda_canary_deploy",
    "lambda_layer_publisher",
    "lambda_package_builder",
    "lambda_warmer",
    "rollback_manager",
    "stack_deployer",
    "stepfunctions_execution_tracker",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CanaryDeployResult(BaseModel):
    """Result of a Lambda canary deployment."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    new_version: str
    alias_name: str
    final_weight: float
    rolled_back: bool = False


class LayerPublishResult(BaseModel):
    """Result of publishing a Lambda layer."""

    model_config = ConfigDict(frozen=True)

    layer_name: str
    version_number: int
    layer_arn: str
    functions_updated: list[str] = []


class StackDeployResult(BaseModel):
    """Result of a CloudFormation stack deployment."""

    model_config = ConfigDict(frozen=True)

    stack_name: str
    stack_id: str
    status: str
    outputs: dict[str, str] = {}
    change_set_id: str = ""


class EnvironmentPromoteResult(BaseModel):
    """Result of promoting a Lambda environment across stages."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    source_stage: str
    target_stage: str
    env_vars_copied: int
    alias_created: bool = False


class LambdaWarmerResult(BaseModel):
    """Result of setting up a Lambda warmer."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    rule_name: str
    rule_arn: str
    schedule_expression: str


class DriftReport(BaseModel):
    """A single drift item for a resource."""

    model_config = ConfigDict(frozen=True)

    resource_type: str
    resource_name: str
    property_name: str
    expected: str
    actual: str


class DriftDetectionResult(BaseModel):
    """Result of config drift detection."""

    model_config = ConfigDict(frozen=True)

    drifted: bool
    drift_items: list[DriftReport] = []
    resources_checked: int = 0


class RollbackResult(BaseModel):
    """Result of a rollback operation."""

    model_config = ConfigDict(frozen=True)

    function_name: str
    alias_name: str
    rolled_back: bool
    previous_version: str
    error_rate: float = 0.0


class PackageBuildResult(BaseModel):
    """Result of building a Lambda deployment package."""

    model_config = ConfigDict(frozen=True)

    s3_bucket: str
    s3_key: str
    zip_size_bytes: int
    files_included: int


# ---------------------------------------------------------------------------
# 1. Lambda canary deploy
# ---------------------------------------------------------------------------


def lambda_canary_deploy(
    function_name: str,
    alias_name: str,
    steps: list[float] | None = None,
    interval_seconds: int = 60,
    alarm_names: list[str] | None = None,
    region_name: str | None = None,
) -> CanaryDeployResult:
    """Publish a new Lambda version and shift alias traffic gradually.

    Publishes a new version, then shifts traffic from the current version
    to the new one in incremental steps.  After each step the function
    checks the specified CloudWatch alarms; if any are in ALARM state the
    deployment rolls back to the original version.

    Args:
        function_name: Lambda function name.
        alias_name: Alias to update (e.g. ``"live"``).
        steps: Weight percentages for each step (0.0-1.0).
            Defaults to ``[0.1, 0.5, 1.0]``.
        interval_seconds: Seconds to wait between steps.
        alarm_names: CloudWatch alarm names to monitor.
        region_name: AWS region override.

    Returns:
        A :class:`CanaryDeployResult` with deployment outcome.

    Raises:
        RuntimeError: If Lambda API calls fail.
    """
    lam = get_client("lambda", region_name)
    cw = get_client("cloudwatch", region_name)

    if steps is None:
        steps = [0.1, 0.5, 1.0]

    # Publish new version
    try:
        publish_resp = lam.publish_version(FunctionName=function_name)
        new_version = publish_resp["Version"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to publish version for {function_name}") from exc

    # Get current alias to find the original version
    try:
        alias_resp = lam.get_alias(
            FunctionName=function_name,
            Name=alias_name,
        )
        original_version = alias_resp["FunctionVersion"]
    except ClientError:
        # Alias doesn't exist — create pointing to new version
        try:
            lam.create_alias(
                FunctionName=function_name,
                Name=alias_name,
                FunctionVersion=new_version,
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to create alias {alias_name}") from exc
        return CanaryDeployResult(
            function_name=function_name,
            new_version=new_version,
            alias_name=alias_name,
            final_weight=1.0,
        )

    # Gradually shift traffic
    for weight in steps:
        routing_config: dict[str, Any] = {}
        if weight < 1.0:
            routing_config = {
                "AdditionalVersionWeights": {new_version: weight},
            }
            func_version = original_version
        else:
            func_version = new_version

        try:
            update_kwargs: dict[str, Any] = {
                "FunctionName": function_name,
                "Name": alias_name,
                "FunctionVersion": func_version,
            }
            if routing_config:
                update_kwargs["RoutingConfig"] = routing_config
            lam.update_alias(**update_kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to update alias {alias_name}") from exc

        # Check alarms
        if alarm_names and weight < 1.0:
            time.sleep(interval_seconds)
            try:
                alarm_resp = cw.describe_alarms(AlarmNames=alarm_names)
                for alarm in alarm_resp.get("MetricAlarms", []):
                    if alarm["StateValue"] == "ALARM":
                        # Rollback
                        lam.update_alias(
                            FunctionName=function_name,
                            Name=alias_name,
                            FunctionVersion=original_version,
                        )
                        logger.warning(
                            "Canary deploy rolled back for %s due to alarm %s",
                            function_name,
                            alarm["AlarmName"],
                        )
                        return CanaryDeployResult(
                            function_name=function_name,
                            new_version=new_version,
                            alias_name=alias_name,
                            final_weight=weight,
                            rolled_back=True,
                        )
            except ClientError as exc:
                raise wrap_aws_error(exc, "Failed to check alarms") from exc

    return CanaryDeployResult(
        function_name=function_name,
        new_version=new_version,
        alias_name=alias_name,
        final_weight=1.0,
    )


# ---------------------------------------------------------------------------
# 2. Lambda layer publisher
# ---------------------------------------------------------------------------


def lambda_layer_publisher(
    layer_name: str,
    directory: str,
    compatible_runtimes: list[str] | None = None,
    description: str = "",
    function_names: list[str] | None = None,
    region_name: str | None = None,
) -> LayerPublishResult:
    """Package a directory into a Lambda Layer ZIP and publish it.

    Optionally updates the specified Lambda functions to use the new
    layer version.

    Args:
        layer_name: Name for the Lambda layer.
        directory: Local directory to package into the layer.
        compatible_runtimes: List of compatible runtimes (e.g.
            ``["python3.12"]``).
        description: Layer description.
        function_names: Lambda functions to update with the new layer.
        region_name: AWS region override.

    Returns:
        A :class:`LayerPublishResult` with the published layer details.

    Raises:
        RuntimeError: If packaging or publishing fails.
    """
    lam = get_client("lambda", region_name)

    # Build ZIP from directory
    buf = io.BytesIO()
    try:
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _dirs, files in os.walk(directory):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    arcname = os.path.relpath(full_path, directory)
                    zf.write(full_path, arcname)
    except OSError as exc:
        raise wrap_aws_error(exc, f"Failed to package directory {directory}") from exc

    zip_bytes = buf.getvalue()

    # Publish layer version
    publish_kwargs: dict[str, Any] = {
        "LayerName": layer_name,
        "Content": {"ZipFile": zip_bytes},
        "Description": description,
    }
    if compatible_runtimes:
        publish_kwargs["CompatibleRuntimes"] = compatible_runtimes

    try:
        resp = lam.publish_layer_version(**publish_kwargs)
        version_number = resp["Version"]
        layer_arn = resp["LayerVersionArn"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to publish layer {layer_name}") from exc

    # Update functions to use the new layer
    updated_functions: list[str] = []
    if function_names:
        for fn_name in function_names:
            try:
                config = lam.get_function_configuration(
                    FunctionName=fn_name,
                )
                existing_layers = [lyr["Arn"] for lyr in config.get("Layers", [])]
                # Replace any existing version of this layer or append
                new_layers = [
                    arn
                    for arn in existing_layers
                    if not arn.startswith(layer_arn.rsplit(":", 1)[0])
                ]
                new_layers.append(layer_arn)

                lam.update_function_configuration(
                    FunctionName=fn_name,
                    Layers=new_layers,
                )
                updated_functions.append(fn_name)
            except ClientError as exc:
                logger.warning(
                    "Failed to update function %s with layer: %s",
                    fn_name,
                    exc,
                )

    return LayerPublishResult(
        layer_name=layer_name,
        version_number=version_number,
        layer_arn=layer_arn,
        functions_updated=updated_functions,
    )


# ---------------------------------------------------------------------------
# 3. Stack deployer
# ---------------------------------------------------------------------------


def stack_deployer(
    stack_name: str,
    template_body: str | None = None,
    template_url: str | None = None,
    parameters: dict[str, str] | None = None,
    capabilities: list[str] | None = None,
    tags: dict[str, str] | None = None,
    timeout_seconds: int = 600,
    region_name: str | None = None,
) -> StackDeployResult:
    """Deploy a CloudFormation stack using change sets with auto-rollback.

    Creates a change set, executes it, and waits for completion.
    Captures stack outputs on success.

    Args:
        stack_name: CloudFormation stack name.
        template_body: Template body string.
        template_url: S3 URL of the template.
        parameters: Stack parameters as key-value pairs.
        capabilities: IAM capabilities (e.g. ``["CAPABILITY_IAM"]``).
        tags: Stack tags as key-value pairs.
        timeout_seconds: Maximum wait time for stack completion.
        region_name: AWS region override.

    Returns:
        A :class:`StackDeployResult` with stack status and outputs.

    Raises:
        RuntimeError: If stack deployment fails.
        ValueError: If neither template_body nor template_url is provided.
        TimeoutError: If stack does not complete within timeout.
    """
    if not template_body and not template_url:
        raise ValueError("Either template_body or template_url is required")

    cfn = get_client("cloudformation", region_name)

    # Check if stack exists
    stack_exists = False
    try:
        cfn.describe_stacks(StackName=stack_name)
        stack_exists = True
    except ClientError:
        pass

    change_set_name = f"{stack_name}-cs-{int(time.time())}"
    cs_type = "UPDATE" if stack_exists else "CREATE"

    # Build change set kwargs
    cs_kwargs: dict[str, Any] = {
        "StackName": stack_name,
        "ChangeSetName": change_set_name,
        "ChangeSetType": cs_type,
    }
    if template_body:
        cs_kwargs["TemplateBody"] = template_body
    if template_url:
        cs_kwargs["TemplateURL"] = template_url
    if parameters:
        cs_kwargs["Parameters"] = [
            {"ParameterKey": k, "ParameterValue": v} for k, v in parameters.items()
        ]
    if capabilities:
        cs_kwargs["Capabilities"] = capabilities
    if tags:
        cs_kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]

    try:
        cs_resp = cfn.create_change_set(**cs_kwargs)
        change_set_id = cs_resp["Id"]
        stack_id = cs_resp["StackId"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create change set for {stack_name}") from exc

    # Wait for change set to be ready
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            desc = cfn.describe_change_set(ChangeSetName=change_set_id)
            status = desc["Status"]
            if status == "CREATE_COMPLETE":
                break
            if status == "FAILED":
                reason = desc.get("StatusReason", "Unknown")
                # No changes to deploy — treat as success
                if "didn't contain changes" in reason.lower() or ("no updates" in reason.lower()):
                    with contextlib.suppress(ClientError):
                        cfn.delete_change_set(ChangeSetName=change_set_id)
                    outputs = _get_stack_outputs(cfn, stack_name)
                    return StackDeployResult(
                        stack_name=stack_name,
                        stack_id=stack_id,
                        status="NO_CHANGES",
                        outputs=outputs,
                        change_set_id=change_set_id,
                    )
                raise AwsServiceError(f"Change set failed: {reason}")
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to describe change set") from exc
        time.sleep(2)
    else:
        raise TimeoutError(
            f"Change set for {stack_name} did not become ready within {timeout_seconds}s"
        )

    # Execute change set
    try:
        cfn.execute_change_set(ChangeSetName=change_set_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to execute change set for {stack_name}") from exc

    # Wait for stack to reach terminal state
    while time.time() < deadline:
        try:
            stack_desc = cfn.describe_stacks(StackName=stack_name)
            stacks = stack_desc["Stacks"]
            if not stacks:
                raise AwsServiceError(f"Stack {stack_name} not found")
            stack_status = stacks[0].get("StackStatus", stacks[0].get("Status", ""))
            if stack_status.endswith("_COMPLETE"):
                if "ROLLBACK" in stack_status:
                    raise AwsServiceError(f"Stack {stack_name} rolled back: {stack_status}")
                outputs = _get_stack_outputs(cfn, stack_name)
                return StackDeployResult(
                    stack_name=stack_name,
                    stack_id=stack_id,
                    status=stack_status,
                    outputs=outputs,
                    change_set_id=change_set_id,
                )
            if stack_status.endswith("_FAILED"):
                raise AwsServiceError(f"Stack {stack_name} failed: {stack_status}")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe stack {stack_name}") from exc
        time.sleep(2)

    raise TimeoutError(f"Stack {stack_name} did not complete within {timeout_seconds}s")


def _get_stack_outputs(cfn: Any, stack_name: str) -> dict[str, str]:
    """Extract outputs from a CloudFormation stack."""
    try:
        resp = cfn.describe_stacks(StackName=stack_name)
        stacks = resp.get("Stacks", [])
        if not stacks:
            return {}
        raw_outputs = stacks[0].get("Outputs", [])
        return {o["OutputKey"]: o["OutputValue"] for o in raw_outputs}
    except ClientError:
        return {}


# ---------------------------------------------------------------------------
# 4. Environment promoter
# ---------------------------------------------------------------------------


def environment_promoter(
    function_name: str,
    source_stage: str,
    target_stage: str,
    source_region: str | None = None,
    target_region: str | None = None,
    target_role_arn: str | None = None,
    alias_name: str | None = None,
    extra_env_vars: dict[str, str] | None = None,
    region_name: str | None = None,
) -> EnvironmentPromoteResult:
    """Copy Lambda config and env vars from one stage to another.

    Reads the source function's environment variables and configuration,
    then applies them to the target function.  Supports cross-account
    promotion via STS role assumption.

    Args:
        function_name: Base function name (stage is appended, e.g.
            ``"my-func-dev"`` / ``"my-func-prod"``).
        source_stage: Source stage suffix (e.g. ``"dev"``).
        target_stage: Target stage suffix (e.g. ``"prod"``).
        source_region: Region for the source function.
        target_region: Region for the target function.
        target_role_arn: IAM role ARN to assume for cross-account.
        alias_name: Optional alias to create/update on the target.
        extra_env_vars: Additional env vars to merge.
        region_name: Default AWS region.

    Returns:
        An :class:`EnvironmentPromoteResult` with promotion details.

    Raises:
        RuntimeError: If Lambda API calls fail.
    """
    src_region = source_region or region_name
    tgt_region = target_region or region_name

    source_lam = get_client("lambda", src_region)
    source_func = f"{function_name}-{source_stage}"
    target_func = f"{function_name}-{target_stage}"

    # Read source configuration
    try:
        src_config = source_lam.get_function_configuration(
            FunctionName=source_func,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get config for {source_func}") from exc

    env_vars = src_config.get("Environment", {}).get("Variables", {})
    if extra_env_vars:
        env_vars.update(extra_env_vars)

    # Get target client (optionally cross-account)
    if target_role_arn:
        sts = get_client("sts", region_name)
        try:
            creds = sts.assume_role(
                RoleArn=target_role_arn,
                RoleSessionName="env-promoter",
            )["Credentials"]
            import boto3

            target_lam = boto3.client(
                "lambda",
                region_name=tgt_region,
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"],
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to assume role {target_role_arn}") from exc
    else:
        target_lam = get_client("lambda", tgt_region)

    # Update target function config
    try:
        target_lam.update_function_configuration(
            FunctionName=target_func,
            Environment={"Variables": env_vars},
            Timeout=src_config.get("Timeout", 30),
            MemorySize=src_config.get("MemorySize", 128),
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update config for {target_func}") from exc

    # Optionally create/update alias
    alias_created = False
    if alias_name:
        try:
            target_lam.get_alias(
                FunctionName=target_func,
                Name=alias_name,
            )
            # Alias exists — update
            publish_resp = target_lam.publish_version(
                FunctionName=target_func,
            )
            target_lam.update_alias(
                FunctionName=target_func,
                Name=alias_name,
                FunctionVersion=publish_resp["Version"],
            )
        except ClientError:
            # Alias doesn't exist — create
            try:
                publish_resp = target_lam.publish_version(
                    FunctionName=target_func,
                )
                target_lam.create_alias(
                    FunctionName=target_func,
                    Name=alias_name,
                    FunctionVersion=publish_resp["Version"],
                )
                alias_created = True
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"Failed to create alias {alias_name} on {target_func}"
                ) from exc

    return EnvironmentPromoteResult(
        function_name=function_name,
        source_stage=source_stage,
        target_stage=target_stage,
        env_vars_copied=len(env_vars),
        alias_created=alias_created,
    )


# ---------------------------------------------------------------------------
# 5. Lambda warmer
# ---------------------------------------------------------------------------


def lambda_warmer(
    function_name: str,
    schedule_expression: str = "rate(5 minutes)",
    rule_name: str | None = None,
    payload: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> LambdaWarmerResult:
    """Create an EventBridge rule to keep a Lambda warm.

    Sets up a scheduled rule that invokes the Lambda function with a
    no-op payload to prevent cold starts.

    Args:
        function_name: Lambda function name or ARN.
        schedule_expression: EventBridge schedule (default ``"rate(5 minutes)"``).
        rule_name: Custom rule name.  Defaults to ``"warmer-{function_name}"``.
        payload: Custom warm-up payload.  Defaults to ``{"warmer": true}``.
        region_name: AWS region override.

    Returns:
        A :class:`LambdaWarmerResult` with rule details.

    Raises:
        RuntimeError: If EventBridge or Lambda API calls fail.
    """
    events = get_client("events", region_name)
    lam = get_client("lambda", region_name)

    if rule_name is None:
        rule_name = f"warmer-{function_name}"
    if payload is None:
        payload = {"warmer": True}

    # Get function ARN
    try:
        fn_config = lam.get_function_configuration(
            FunctionName=function_name,
        )
        function_arn = fn_config["FunctionArn"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get function {function_name}") from exc

    # Create or update rule
    try:
        rule_resp = events.put_rule(
            Name=rule_name,
            ScheduleExpression=schedule_expression,
            State="ENABLED",
        )
        rule_arn = rule_resp["RuleArn"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create rule {rule_name}") from exc

    # Add Lambda permission for EventBridge
    try:
        lam.add_permission(
            FunctionName=function_name,
            StatementId=f"{rule_name}-invoke",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=rule_arn,
        )
    except ClientError:
        # Permission may already exist
        pass

    # Add target
    try:
        events.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    "Id": f"{function_name}-warmer",
                    "Arn": function_arn,
                    "Input": json.dumps(payload),
                },
            ],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to add target for rule {rule_name}") from exc

    return LambdaWarmerResult(
        function_name=function_name,
        rule_name=rule_name,
        rule_arn=rule_arn,
        schedule_expression=schedule_expression,
    )


# ---------------------------------------------------------------------------
# 6. Config drift detector
# ---------------------------------------------------------------------------


def config_drift_detector(
    function_names: list[str] | None = None,
    api_ids: list[str] | None = None,
    desired_state_ssm_prefix: str | None = None,
    desired_state_s3: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DriftDetectionResult:
    """Compare deployed Lambda/API GW configs against desired state.

    Reads desired state from SSM parameters or an S3 JSON object and
    compares it against live Lambda and API Gateway configurations.

    Args:
        function_names: Lambda functions to check.
        api_ids: API Gateway REST API IDs to check.
        desired_state_ssm_prefix: SSM parameter prefix containing desired
            config as JSON values.
        desired_state_s3: Dict with ``"bucket"`` and ``"key"`` pointing
            to a JSON object in S3 containing desired state.
        region_name: AWS region override.

    Returns:
        A :class:`DriftDetectionResult` with drift items.

    Raises:
        RuntimeError: If API calls fail.
    """
    drift_items: list[DriftReport] = []
    resources_checked = 0

    # Load desired state
    desired: dict[str, Any] = {}

    if desired_state_ssm_prefix:
        ssm = get_client("ssm", region_name)
        try:
            paginator = ssm.get_paginator("get_parameters_by_path")
            for page in paginator.paginate(
                Path=desired_state_ssm_prefix,
                Recursive=True,
                WithDecryption=True,
            ):
                for param in page["Parameters"]:
                    key = param["Name"].replace(
                        desired_state_ssm_prefix,
                        "",
                    )
                    try:
                        desired[key] = json.loads(param["Value"])
                    except (json.JSONDecodeError, TypeError):
                        desired[key] = param["Value"]
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to load desired state from SSM") from exc

    if desired_state_s3:
        s3 = get_client("s3", region_name)
        try:
            resp = s3.get_object(
                Bucket=desired_state_s3["bucket"],
                Key=desired_state_s3["key"],
            )
            s3_desired = json.loads(resp["Body"].read().decode("utf-8"))
            desired.update(s3_desired)
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to load desired state from S3") from exc

    # Check Lambda functions
    if function_names:
        lam = get_client("lambda", region_name)
        for fn_name in function_names:
            resources_checked += 1
            try:
                config = lam.get_function_configuration(
                    FunctionName=fn_name,
                )
            except ClientError as exc:
                raise wrap_aws_error(exc, f"Failed to get config for {fn_name}") from exc

            fn_desired = desired.get(fn_name, {})
            if isinstance(fn_desired, dict):
                # Check memory
                if "MemorySize" in fn_desired:
                    actual_mem = config.get("MemorySize", 0)
                    expected_mem = fn_desired["MemorySize"]
                    if actual_mem != expected_mem:
                        drift_items.append(
                            DriftReport(
                                resource_type="Lambda",
                                resource_name=fn_name,
                                property_name="MemorySize",
                                expected=str(expected_mem),
                                actual=str(actual_mem),
                            )
                        )
                # Check timeout
                if "Timeout" in fn_desired:
                    actual_to = config.get("Timeout", 0)
                    expected_to = fn_desired["Timeout"]
                    if actual_to != expected_to:
                        drift_items.append(
                            DriftReport(
                                resource_type="Lambda",
                                resource_name=fn_name,
                                property_name="Timeout",
                                expected=str(expected_to),
                                actual=str(actual_to),
                            )
                        )
                # Check env vars
                if "Environment" in fn_desired:
                    actual_env = config.get(
                        "Environment",
                        {},
                    ).get("Variables", {})
                    expected_env = fn_desired["Environment"].get(
                        "Variables",
                        {},
                    )
                    for key, val in expected_env.items():
                        actual_val = actual_env.get(key)
                        if actual_val != val:
                            drift_items.append(
                                DriftReport(
                                    resource_type="Lambda",
                                    resource_name=fn_name,
                                    property_name=f"Environment.Variables.{key}",
                                    expected=str(val),
                                    actual=str(actual_val),
                                )
                            )

    # Check API Gateway
    if api_ids:
        apigw = get_client("apigateway", region_name)
        for api_id in api_ids:
            resources_checked += 1
            try:
                api = apigw.get_rest_api(restApiId=api_id)
            except ClientError as exc:
                raise wrap_aws_error(exc, f"Failed to get API {api_id}") from exc

            api_desired = desired.get(api_id, {})
            if isinstance(api_desired, dict):
                if "name" in api_desired and api["name"] != api_desired["name"]:
                    drift_items.append(
                        DriftReport(
                            resource_type="APIGateway",
                            resource_name=api_id,
                            property_name="name",
                            expected=str(api_desired["name"]),
                            actual=str(api["name"]),
                        )
                    )
                if "description" in api_desired:
                    actual_desc = api.get("description", "")
                    if actual_desc != api_desired["description"]:
                        drift_items.append(
                            DriftReport(
                                resource_type="APIGateway",
                                resource_name=api_id,
                                property_name="description",
                                expected=str(api_desired["description"]),
                                actual=str(actual_desc),
                            )
                        )

    return DriftDetectionResult(
        drifted=len(drift_items) > 0,
        drift_items=drift_items,
        resources_checked=resources_checked,
    )


# ---------------------------------------------------------------------------
# 7. Rollback manager
# ---------------------------------------------------------------------------


def rollback_manager(
    function_name: str,
    alias_name: str,
    error_metric_name: str = "Errors",
    error_threshold: float = 5.0,
    evaluation_minutes: int = 5,
    region_name: str | None = None,
) -> RollbackResult:
    """Detect error-rate spikes and auto-roll back a Lambda alias.

    Queries CloudWatch for recent error metrics.  If the error count
    exceeds the threshold, the alias is shifted back to the previous
    stable version.

    Args:
        function_name: Lambda function name.
        alias_name: Alias to inspect and potentially roll back.
        error_metric_name: CloudWatch metric name (default ``"Errors"``).
        error_threshold: Error count threshold to trigger rollback.
        evaluation_minutes: Minutes of metric data to evaluate.
        region_name: AWS region override.

    Returns:
        A :class:`RollbackResult` with rollback outcome.

    Raises:
        RuntimeError: If API calls fail.
    """
    lam = get_client("lambda", region_name)
    cw = get_client("cloudwatch", region_name)

    # Get current alias configuration
    try:
        alias_resp = lam.get_alias(
            FunctionName=function_name,
            Name=alias_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get alias {alias_name} for {function_name}") from exc

    current_version = alias_resp["FunctionVersion"]
    routing = alias_resp.get("RoutingConfig", {})
    additional_weights = routing.get("AdditionalVersionWeights", {})

    # Determine the "new" version (from routing weights) and "previous"
    if additional_weights:
        next(iter(additional_weights.keys()))
        previous_version = current_version
    else:
        # No canary routing — current is the deployed version
        previous_version = str(max(1, int(current_version) - 1))

    # Query CloudWatch metrics
    import datetime

    end_time = datetime.datetime.now(tz=datetime.UTC)
    start_time = end_time - datetime.timedelta(
        minutes=evaluation_minutes,
    )

    try:
        metric_resp = cw.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName=error_metric_name,
            Dimensions=[
                {"Name": "FunctionName", "Value": function_name},
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=evaluation_minutes * 60,
            Statistics=["Sum"],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get metrics for {function_name}") from exc

    datapoints = metric_resp.get("Datapoints", [])
    error_rate = sum(dp.get("Sum", 0.0) for dp in datapoints)

    if error_rate > error_threshold:
        # Roll back
        try:
            lam.update_alias(
                FunctionName=function_name,
                Name=alias_name,
                FunctionVersion=previous_version,
                RoutingConfig={},
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to roll back alias {alias_name}") from exc

        logger.warning(
            "Rolled back %s alias %s to version %s (error rate: %.1f)",
            function_name,
            alias_name,
            previous_version,
            error_rate,
        )
        return RollbackResult(
            function_name=function_name,
            alias_name=alias_name,
            rolled_back=True,
            previous_version=previous_version,
            error_rate=error_rate,
        )

    return RollbackResult(
        function_name=function_name,
        alias_name=alias_name,
        rolled_back=False,
        previous_version=previous_version,
        error_rate=error_rate,
    )


# ---------------------------------------------------------------------------
# 8. Lambda package builder
# ---------------------------------------------------------------------------


def lambda_package_builder(
    source_dir: str,
    s3_bucket: str,
    s3_key: str,
    requirements_file: str | None = None,
    exclude_patterns: list[str] | None = None,
    region_name: str | None = None,
) -> PackageBuildResult:
    """Bundle Python Lambda code + dependencies into a ZIP and upload to S3.

    Packages the source directory (and optionally pip-installed
    dependencies) into a deployment ZIP and uploads it to S3.

    Args:
        source_dir: Directory containing Lambda code.
        s3_bucket: S3 bucket for the deployment package.
        s3_key: S3 key for the ZIP file.
        requirements_file: Path to ``requirements.txt`` for dependency
            installation.  ``None`` skips dependency bundling.
        exclude_patterns: File patterns to exclude (e.g.
            ``["__pycache__", "*.pyc"]``).
        region_name: AWS region override.

    Returns:
        A :class:`PackageBuildResult` with upload details.

    Raises:
        RuntimeError: If packaging or upload fails.
    """
    s3 = get_client("s3", region_name)

    if exclude_patterns is None:
        exclude_patterns = ["__pycache__", "*.pyc", ".git"]

    buf = io.BytesIO()
    files_included = 0

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # Install dependencies if requirements file given
        if requirements_file:
            with tempfile.TemporaryDirectory() as tmpdir:
                try:
                    subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "pip",
                            "install",
                            "-r",
                            requirements_file,
                            "-t",
                            tmpdir,
                            "--quiet",
                        ],
                        check=True,
                        capture_output=True,
                    )
                except subprocess.CalledProcessError as exc:
                    raise wrap_aws_error(exc, "Failed to install dependencies") from exc

                for root, _dirs, files in os.walk(tmpdir):
                    for fname in files:
                        full_path = os.path.join(root, fname)
                        arcname = os.path.relpath(full_path, tmpdir)
                        if not _should_exclude(
                            arcname,
                            exclude_patterns,
                        ):
                            zf.write(full_path, arcname)
                            files_included += 1

        # Add source code
        for root, _dirs, files in os.walk(source_dir):
            for fname in files:
                full_path = os.path.join(root, fname)
                arcname = os.path.relpath(full_path, source_dir)
                if not _should_exclude(arcname, exclude_patterns):
                    zf.write(full_path, arcname)
                    files_included += 1

    zip_bytes = buf.getvalue()

    try:
        s3.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=zip_bytes,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to upload package to s3://{s3_bucket}/{s3_key}") from exc

    return PackageBuildResult(
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        zip_size_bytes=len(zip_bytes),
        files_included=files_included,
    )


# ---------------------------------------------------------------------------
# 9. CloudFront invalidation with logging
# ---------------------------------------------------------------------------


class InvalidationLogResult(BaseModel):
    """Result of a CloudFront invalidation with CloudWatch logging."""

    model_config = ConfigDict(frozen=True)

    invalidation_id: str
    status: str
    paths_invalidated: int
    logged: bool


def cloudfront_invalidation_with_logging(
    distribution_id: str,
    paths: list[str],
    log_group_name: str,
    region_name: str | None = None,
) -> InvalidationLogResult:
    """Submit a CloudFront invalidation, wait for completion, log to CloudWatch.

    Creates an invalidation for the specified paths on the given distribution,
    polls until the invalidation reaches the ``Completed`` state, then records
    the result to a CloudWatch Logs log group.

    Args:
        distribution_id: CloudFront distribution ID.
        paths: List of URL paths to invalidate (e.g. ``["/index.html", "/*"]``).
        log_group_name: CloudWatch Logs group name to write the result.
        region_name: AWS region override.

    Returns:
        An :class:`InvalidationLogResult` with invalidation details.

    Raises:
        RuntimeError: If CloudFront or CloudWatch Logs API calls fail.
    """
    import uuid

    cf = get_client("cloudfront", region_name)
    logs = get_client("logs", region_name)

    caller_ref = str(uuid.uuid4())
    try:
        resp = cf.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                "Paths": {"Quantity": len(paths), "Items": paths},
                "CallerReference": caller_ref,
            },
        )
        inv = resp["Invalidation"]
        inv_id = inv["Id"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create invalidation for {distribution_id}") from exc

    # Poll until Completed (max 120 iterations, 5s each = 10 min)
    status = inv["Status"]
    for _ in range(120):
        if status == "Completed":
            break
        time.sleep(5)
        try:
            get_resp = cf.get_invalidation(
                DistributionId=distribution_id,
                Id=inv_id,
            )
            status = get_resp["Invalidation"]["Status"]
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll invalidation {inv_id}") from exc

    # Log to CloudWatch
    logged = False
    log_stream = f"invalidation-{inv_id}"
    log_msg = json.dumps(
        {
            "invalidation_id": inv_id,
            "distribution_id": distribution_id,
            "status": status,
            "paths": paths,
        }
    )
    try:
        try:
            logs.create_log_group(logGroupName=log_group_name)
        except ClientError:
            pass
        try:
            logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream)
        except ClientError:
            pass
        logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream,
            logEvents=[{"timestamp": int(time.time() * 1000), "message": log_msg}],
        )
        logged = True
    except ClientError as exc:
        logger.warning("Failed to log invalidation result: %s", exc)

    return InvalidationLogResult(
        invalidation_id=inv_id,
        status=status,
        paths_invalidated=len(paths),
        logged=logged,
    )


# ---------------------------------------------------------------------------
# 10. Elastic Beanstalk env refresher
# ---------------------------------------------------------------------------


class BeanstalkRefreshResult(BaseModel):
    """Result of a Beanstalk environment refresh."""

    model_config = ConfigDict(frozen=True)

    environment_id: str
    status: str
    params_injected: int


def elastic_beanstalk_env_refresher(
    application_name: str,
    environment_name: str,
    version_label: str,
    ssm_prefix: str,
    region_name: str | None = None,
) -> BeanstalkRefreshResult:
    """Deploy a new Beanstalk version with SSM Parameter Store env vars injected.

    Fetches parameters from SSM under *ssm_prefix*, converts them to
    Elastic Beanstalk OptionSettings, then calls ``update_environment``.

    Args:
        application_name: Elastic Beanstalk application name.
        environment_name: Target environment name.
        version_label: Application version to deploy.
        ssm_prefix: SSM parameter hierarchy prefix to read env vars from.
        region_name: AWS region override.

    Returns:
        A :class:`BeanstalkRefreshResult` with environment status.

    Raises:
        RuntimeError: If SSM or Beanstalk API calls fail.
    """
    ssm = get_client("ssm", region_name)
    eb = get_client("elasticbeanstalk", region_name)

    # Fetch SSM parameters
    option_settings: list[dict[str, str]] = []
    try:
        paginator = ssm.get_paginator("get_parameters_by_path")
        for page in paginator.paginate(Path=ssm_prefix, Recursive=True, WithDecryption=True):
            for param in page["Parameters"]:
                var_name = param["Name"].split("/")[-1]
                option_settings.append(
                    {
                        "Namespace": "aws:elasticbeanstalk:application:environment",
                        "OptionName": var_name,
                        "Value": param["Value"],
                    }
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to read SSM prefix {ssm_prefix}") from exc

    # Update environment
    try:
        eb.update_environment(
            ApplicationName=application_name,
            EnvironmentName=environment_name,
            VersionLabel=version_label,
            OptionSettings=option_settings,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to update Beanstalk environment {environment_name}"
        ) from exc

    # Verify status
    env_id = ""
    env_status = "Updating"
    try:
        desc = eb.describe_environments(
            ApplicationName=application_name,
            EnvironmentNames=[environment_name],
        )
        envs = desc.get("Environments", [])
        if envs:
            env_id = envs[0].get("EnvironmentId", "")
            env_status = envs[0].get("Status", "Updating")
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to describe environment {environment_name}") from exc

    return BeanstalkRefreshResult(
        environment_id=env_id,
        status=env_status,
        params_injected=len(option_settings),
    )


# ---------------------------------------------------------------------------
# 11. App Runner auto deployer
# ---------------------------------------------------------------------------


class AppRunnerDeployResult(BaseModel):
    """Result of an App Runner auto-deployment."""

    model_config = ConfigDict(frozen=True)

    service_id: str
    image_updated: bool
    new_image_tag: str
    operation_id: str | None = None


def app_runner_auto_deployer(
    service_arn: str,
    repository_name: str,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> AppRunnerDeployResult:
    """Check ECR for the latest image tag, update App Runner if changed, notify via SNS.

    Queries ECR for the most recently pushed image in *repository_name*,
    compares it to the image currently configured in the App Runner service,
    and triggers an update if the tag has changed.

    Args:
        service_arn: App Runner service ARN.
        repository_name: ECR repository name (without registry URL).
        sns_topic_arn: Optional SNS topic ARN for update notification.
        region_name: AWS region override.

    Returns:
        An :class:`AppRunnerDeployResult` with update details.

    Raises:
        RuntimeError: If ECR, App Runner, or SNS API calls fail.
    """
    ecr = get_client("ecr", region_name)
    apprunner = get_client("apprunner", region_name)

    # Get latest image tag from ECR
    try:
        images_resp = ecr.describe_images(
            repositoryName=repository_name,
            filter={"tagStatus": "TAGGED"},
        )
        images = sorted(
            images_resp.get("imageDetails", []),
            key=lambda x: x.get("imagePushedAt", 0),
            reverse=True,
        )
        latest_tag = images[0]["imageTags"][0] if images else "latest"
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to describe ECR images for {repository_name}") from exc

    # Get current service image
    try:
        svc_resp = apprunner.describe_service(ServiceArn=service_arn)
        svc = svc_resp["Service"]
        service_id = svc["ServiceId"]
        current_img = (
            svc.get("SourceConfiguration", {}).get("ImageRepository", {}).get("ImageIdentifier", "")
        )
        current_tag = current_img.split(":")[-1] if ":" in current_img else ""
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to describe App Runner service {service_arn}") from exc

    if current_tag == latest_tag:
        return AppRunnerDeployResult(
            service_id=service_id,
            image_updated=False,
            new_image_tag=latest_tag,
        )

    # Build new image URI
    registry_id = images[0].get("registryId", "") if images else ""
    new_image_uri = f"{registry_id}.dkr.ecr.{region_name or 'us-east-1'}.amazonaws.com/{repository_name}:{latest_tag}"

    try:
        update_resp = apprunner.update_service(
            ServiceArn=service_arn,
            SourceConfiguration={
                "ImageRepository": {
                    "ImageIdentifier": new_image_uri,
                    "ImageRepositoryType": "ECR",
                }
            },
        )
        operation_id = update_resp.get("OperationId")
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update App Runner service {service_arn}") from exc

    # Notify via SNS
    if sns_topic_arn:
        sns = get_client("sns", region_name)
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject="App Runner Service Updated",
                Message=json.dumps(
                    {
                        "service_arn": service_arn,
                        "new_image": new_image_uri,
                        "operation_id": operation_id,
                    }
                ),
            )
        except ClientError as exc:
            logger.warning("Failed to publish App Runner SNS notification: %s", exc)

    return AppRunnerDeployResult(
        service_id=service_id,
        image_updated=True,
        new_image_tag=latest_tag,
        operation_id=operation_id,
    )


# ---------------------------------------------------------------------------
# 12. EKS node group scaler
# ---------------------------------------------------------------------------


class NodeGroupScaleResult(BaseModel):
    """Result of an EKS node group scaling operation."""

    model_config = ConfigDict(frozen=True)

    cluster_name: str
    current_size: int
    desired_size: int
    scaled: bool


def eks_node_group_scaler(
    cluster_name: str,
    nodegroup_name: str,
    metric_name: str,
    metric_namespace: str,
    threshold: float,
    scale_up_size: int,
    scale_down_size: int,
    region_name: str | None = None,
) -> NodeGroupScaleResult:
    """Scale an EKS managed node group based on a CloudWatch metric.

    Reads the specified CloudWatch metric, compares it to *threshold*,
    and scales the node group up or down accordingly.

    Args:
        cluster_name: EKS cluster name.
        nodegroup_name: Managed node group name.
        metric_name: CloudWatch metric name to evaluate.
        metric_namespace: CloudWatch metric namespace.
        threshold: Metric value above which scale-up is triggered.
        scale_up_size: Desired node count when scaling up.
        scale_down_size: Desired node count when scaling down.
        region_name: AWS region override.

    Returns:
        A :class:`NodeGroupScaleResult` with before/after sizes.

    Raises:
        RuntimeError: If EKS or CloudWatch API calls fail.
    """
    import datetime

    eks = get_client("eks", region_name)
    cw = get_client("cloudwatch", region_name)

    # Get current node group size
    try:
        ng_resp = eks.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
        scaling = ng_resp["nodegroup"]["scalingConfig"]
        current_size = scaling.get("desiredSize", 0)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to describe node group {nodegroup_name}") from exc

    # Get metric
    end_time = datetime.datetime.now(tz=datetime.UTC)
    start_time = end_time - datetime.timedelta(minutes=5)
    try:
        metric_resp = cw.get_metric_statistics(
            Namespace=metric_namespace,
            MetricName=metric_name,
            Dimensions=[{"Name": "ClusterName", "Value": cluster_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"],
        )
        datapoints = metric_resp.get("Datapoints", [])
        metric_value = datapoints[-1]["Average"] if datapoints else 0.0
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get metric {metric_name}") from exc

    desired_size = scale_up_size if metric_value > threshold else scale_down_size
    scaled = desired_size != current_size

    if scaled:
        try:
            eks.update_nodegroup_config(
                clusterName=cluster_name,
                nodegroupName=nodegroup_name,
                scalingConfig={"desiredSize": desired_size},
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to scale node group {nodegroup_name}") from exc

    return NodeGroupScaleResult(
        cluster_name=cluster_name,
        current_size=current_size,
        desired_size=desired_size,
        scaled=scaled,
    )


# ---------------------------------------------------------------------------
# 13. EKS config map sync
# ---------------------------------------------------------------------------


class ConfigMapSyncResult(BaseModel):
    """Result of syncing SSM parameters to DynamoDB for K8s ConfigMap."""

    model_config = ConfigDict(frozen=True)

    parameters_synced: int
    config_map_name: str
    table_updated: bool


def eks_config_map_sync(
    cluster_name: str,
    ssm_prefix: str,
    table_name: str,
    config_map_name: str,
    region_name: str | None = None,
) -> ConfigMapSyncResult:
    """Sync SSM Parameter Store hierarchy to DynamoDB as ConfigMap data.

    Reads all parameters under *ssm_prefix* from SSM Parameter Store,
    formats them as key-value pairs, and stores them in a DynamoDB item
    for a Kubernetes controller to consume as a ConfigMap.

    Args:
        cluster_name: EKS cluster name (stored as metadata).
        ssm_prefix: SSM path prefix to read parameters from.
        table_name: DynamoDB table name.
        config_map_name: ConfigMap name (stored as metadata).
        region_name: AWS region override.

    Returns:
        A :class:`ConfigMapSyncResult` with sync counts.

    Raises:
        RuntimeError: If SSM or DynamoDB API calls fail.
    """
    ssm = get_client("ssm", region_name)
    ddb = get_client("dynamodb", region_name)

    data: dict[str, str] = {}
    try:
        paginator = ssm.get_paginator("get_parameters_by_path")
        for page in paginator.paginate(Path=ssm_prefix, Recursive=True, WithDecryption=True):
            for param in page["Parameters"]:
                key = param["Name"].split("/")[-1]
                data[key] = param["Value"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to read SSM prefix {ssm_prefix}") from exc

    # Store in DynamoDB
    table_updated = False
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"configmap#{cluster_name}#{config_map_name}"},
                "cluster_name": {"S": cluster_name},
                "config_map_name": {"S": config_map_name},
                "data": {"S": json.dumps(data)},
                "updated_at": {"N": str(int(time.time()))},
            },
        )
        table_updated = True
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to put ConfigMap data in DynamoDB {table_name}") from exc

    return ConfigMapSyncResult(
        parameters_synced=len(data),
        config_map_name=config_map_name,
        table_updated=table_updated,
    )


# ---------------------------------------------------------------------------
# 14. Batch job monitor
# ---------------------------------------------------------------------------


class BatchJobResult(BaseModel):
    """Result of a monitored AWS Batch job."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    status: str
    duration_seconds: float
    metrics_published: int


def batch_job_monitor(
    job_name: str,
    job_queue: str,
    job_definition: str,
    parameters: dict[str, str] | None = None,
    metric_namespace: str = "AwsUtil/Batch",
    region_name: str | None = None,
) -> BatchJobResult:
    """Submit an AWS Batch job, poll until terminal state, publish metrics to CloudWatch.

    Args:
        job_name: Name for the submitted Batch job.
        job_queue: Batch job queue name or ARN.
        job_definition: Batch job definition name or ARN.
        parameters: Optional job parameters dict.
        metric_namespace: CloudWatch namespace for job metrics.
        region_name: AWS region override.

    Returns:
        A :class:`BatchJobResult` with job status and timing.

    Raises:
        RuntimeError: If Batch or CloudWatch API calls fail.
    """
    batch = get_client("batch", region_name)
    cw = get_client("cloudwatch", region_name)

    submit_kwargs: dict[str, Any] = {
        "jobName": job_name,
        "jobQueue": job_queue,
        "jobDefinition": job_definition,
    }
    if parameters:
        submit_kwargs["parameters"] = parameters

    try:
        submit_resp = batch.submit_job(**submit_kwargs)
        job_id = submit_resp["jobId"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to submit Batch job {job_name}") from exc

    start_time = time.time()
    status = "SUBMITTED"
    terminal_states = {"SUCCEEDED", "FAILED"}

    for _ in range(120):
        if status in terminal_states:
            break
        time.sleep(15)
        try:
            desc_resp = batch.describe_jobs(jobs=[job_id])
            jobs = desc_resp.get("jobs", [])
            if jobs:
                status = jobs[0].get("status", status)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe Batch job {job_id}") from exc

    duration = time.time() - start_time

    # Publish metrics
    metrics_published = 0
    try:
        cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    "MetricName": "JobDuration",
                    "Dimensions": [{"Name": "JobName", "Value": job_name}],
                    "Value": duration,
                    "Unit": "Seconds",
                },
                {
                    "MetricName": "JobSuccess",
                    "Dimensions": [{"Name": "JobName", "Value": job_name}],
                    "Value": 1.0 if status == "SUCCEEDED" else 0.0,
                    "Unit": "Count",
                },
            ],
        )
        metrics_published = 2
    except ClientError as exc:
        logger.warning("Failed to publish Batch job metrics: %s", exc)

    return BatchJobResult(
        job_id=job_id,
        status=status,
        duration_seconds=round(duration, 2),
        metrics_published=metrics_published,
    )


# ---------------------------------------------------------------------------
# 15. Auto Scaling scheduled action manager
# ---------------------------------------------------------------------------


class ScheduledActionResult(BaseModel):
    """Result of syncing Auto Scaling scheduled actions."""

    model_config = ConfigDict(frozen=True)

    actions_synced: int
    actions_created: int
    actions_updated: int


def autoscaling_scheduled_action_manager(
    asg_name: str,
    table_name: str,
    region_name: str | None = None,
) -> ScheduledActionResult:
    """Create/update Auto Scaling Group scheduled actions from DynamoDB config.

    Scans *table_name* for items where ``pk`` equals *asg_name*, each
    representing a scheduled scaling action, and upserts them via
    ``put_scheduled_update_group_action``.

    Args:
        asg_name: Auto Scaling Group name.
        table_name: DynamoDB table containing schedule configs.
        region_name: AWS region override.

    Returns:
        A :class:`ScheduledActionResult` with sync counts.

    Raises:
        RuntimeError: If DynamoDB or Auto Scaling API calls fail.
    """
    ddb = get_client("dynamodb", region_name)
    asg_client = get_client("autoscaling", region_name)

    # Scan DynamoDB for schedule configs
    schedule_items: list[dict[str, Any]] = []
    try:
        resp = ddb.scan(
            TableName=table_name,
            FilterExpression="pk = :pk",
            ExpressionAttributeValues={":pk": {"S": asg_name}},
        )
        schedule_items = resp.get("Items", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to scan DynamoDB table {table_name}") from exc

    actions_created = 0
    actions_updated = 0

    for item in schedule_items:
        action_name = item.get("action_name", {}).get("S", "")
        recurrence = item.get("recurrence", {}).get("S", "")
        desired = int(item.get("desired_capacity", {}).get("N", "0"))
        min_size = int(item.get("min_size", {}).get("N", "0"))
        max_size = int(item.get("max_size", {}).get("N", "0"))

        if not action_name:
            continue

        action_kwargs: dict[str, Any] = {
            "AutoScalingGroupName": asg_name,
            "ScheduledActionName": action_name,
            "DesiredCapacity": desired,
            "MinSize": min_size,
            "MaxSize": max_size,
        }
        if recurrence:
            action_kwargs["Recurrence"] = recurrence

        try:
            # Check if action already exists
            existing = asg_client.describe_scheduled_actions(
                AutoScalingGroupName=asg_name,
                ScheduledActionNames=[action_name],
            ).get("ScheduledUpdateGroupActions", [])
            asg_client.put_scheduled_update_group_action(**action_kwargs)
            if existing:
                actions_updated += 1
            else:
                actions_created += 1
        except ClientError as exc:
            logger.warning("Failed to upsert scheduled action %s: %s", action_name, exc)

    return ScheduledActionResult(
        actions_synced=len(schedule_items),
        actions_created=actions_created,
        actions_updated=actions_updated,
    )


# ---------------------------------------------------------------------------
# 16. Step Functions execution tracker
# ---------------------------------------------------------------------------


class ExecutionTrackerResult(BaseModel):
    """Result of a tracked Step Functions execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str
    status: str
    duration_seconds: float
    output: dict[str, Any] | None = None


def stepfunctions_execution_tracker(
    state_machine_arn: str,
    input_data: dict[str, Any],
    execution_name: str | None = None,
    table_name: str = "",
    metric_namespace: str = "AwsUtil/StepFunctions",
    region_name: str | None = None,
) -> ExecutionTrackerResult:
    """Start a Step Functions execution, store ARN in DynamoDB, poll and emit metrics.

    Starts an execution, records its ARN to DynamoDB for auditing, polls
    ``describe_execution`` until a terminal state is reached, then emits
    a duration metric to CloudWatch.

    Args:
        state_machine_arn: Step Functions state machine ARN.
        input_data: JSON-serialisable input dict for the execution.
        execution_name: Optional name for the execution.
        table_name: DynamoDB table to record the execution ARN.
        metric_namespace: CloudWatch namespace for duration metric.
        region_name: AWS region override.

    Returns:
        An :class:`ExecutionTrackerResult` with status and output.

    Raises:
        RuntimeError: If Step Functions, DynamoDB, or CloudWatch calls fail.
    """
    import uuid

    sfn = get_client("stepfunctions", region_name)
    ddb = get_client("dynamodb", region_name)
    cw = get_client("cloudwatch", region_name)

    exec_name = execution_name or f"exec-{uuid.uuid4().hex[:8]}"

    # Start execution
    try:
        start_resp = sfn.start_execution(
            stateMachineArn=state_machine_arn,
            name=exec_name,
            input=json.dumps(input_data),
        )
        execution_arn = start_resp["executionArn"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start execution for {state_machine_arn}") from exc

    start_ts = int(time.time())

    # Store in DynamoDB
    if table_name:
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": execution_arn},
                    "state_machine_arn": {"S": state_machine_arn},
                    "execution_name": {"S": exec_name},
                    "started_at": {"N": str(start_ts)},
                    "status": {"S": "RUNNING"},
                },
            )
        except ClientError as exc:
            logger.warning("Failed to record execution in DynamoDB: %s", exc)

    # Poll until terminal
    start_time = time.time()
    status = "RUNNING"
    raw_output: str | None = None
    terminal_states = {"SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"}

    for _ in range(120):
        if status in terminal_states:
            break
        time.sleep(15)
        try:
            desc = sfn.describe_execution(executionArn=execution_arn)
            status = desc.get("status", status)
            raw_output = desc.get("output")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe execution {execution_arn}") from exc

    duration = time.time() - start_time
    output: dict[str, Any] | None = None
    if raw_output:
        try:
            output = json.loads(raw_output)
        except json.JSONDecodeError:
            output = {"raw": raw_output}

    # Emit duration metric
    try:
        cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    "MetricName": "ExecutionDuration",
                    "Dimensions": [{"Name": "StateMachineArn", "Value": state_machine_arn}],
                    "Value": duration,
                    "Unit": "Seconds",
                }
            ],
        )
    except ClientError as exc:
        logger.warning("Failed to emit Step Functions metric: %s", exc)

    return ExecutionTrackerResult(
        execution_arn=execution_arn,
        status=status,
        duration_seconds=round(duration, 2),
        output=output,
    )


def _should_exclude(path: str, patterns: list[str]) -> bool:
    """Check if a file path matches any exclusion pattern."""
    import fnmatch

    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        # Also check if any path component matches
        for part in path.replace("\\", "/").split("/"):
            if fnmatch.fnmatch(part, pattern):
                return True
    return False
