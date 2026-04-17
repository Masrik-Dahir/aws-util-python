"""Native async deployment utilities using :mod:`aws_util.aio._engine`.

Provides high-level async functions for Lambda deployment workflows:
canary deploy, layer publisher, stack deployer, environment promoter,
Lambda warmer, config drift detector, rollback manager, and package builder.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
import json
import logging
import os
import subprocess
import tempfile
import time
import zipfile
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.deployment import (
    AppRunnerDeployResult,
    BatchJobResult,
    BeanstalkRefreshResult,
    CanaryDeployResult,
    ConfigMapSyncResult,
    DriftDetectionResult,
    DriftReport,
    EnvironmentPromoteResult,
    ExecutionTrackerResult,
    InvalidationLogResult,
    LambdaWarmerResult,
    LayerPublishResult,
    NodeGroupScaleResult,
    PackageBuildResult,
    RollbackResult,
    ScheduledActionResult,
    StackDeployResult,
)
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
# 1. Lambda canary deploy
# ---------------------------------------------------------------------------


async def lambda_canary_deploy(
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
    lam = async_client("lambda", region_name)
    cw = async_client("cloudwatch", region_name)

    if steps is None:
        steps = [0.1, 0.5, 1.0]

    # Publish new version
    try:
        publish_resp = await lam.call(
            "PublishVersion",
            FunctionName=function_name,
        )
        new_version = publish_resp["Version"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to publish version for {function_name}") from exc

    # Get current alias to find the original version
    try:
        alias_resp = await lam.call(
            "GetAlias",
            FunctionName=function_name,
            Name=alias_name,
        )
        original_version = alias_resp["FunctionVersion"]
    except RuntimeError as exc:
        if "ResourceNotFoundException" not in str(exc):
            raise
        # Alias doesn't exist -- create pointing to new version
        try:
            await lam.call(
                "CreateAlias",
                FunctionName=function_name,
                Name=alias_name,
                FunctionVersion=new_version,
            )
        except Exception as create_exc:
            raise wrap_aws_error(create_exc, f"Failed to create alias {alias_name}") from create_exc
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
            await lam.call("UpdateAlias", **update_kwargs)
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to update alias {alias_name}") from exc

        # Check alarms
        if alarm_names and weight < 1.0:
            await asyncio.sleep(interval_seconds)
            try:
                alarm_resp = await cw.call(
                    "DescribeAlarms",
                    AlarmNames=alarm_names,
                )
                for alarm in alarm_resp.get("MetricAlarms", []):
                    if alarm["StateValue"] == "ALARM":
                        # Rollback
                        await lam.call(
                            "UpdateAlias",
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
            except Exception as exc:
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


async def lambda_layer_publisher(
    layer_name: str,
    directory: str,
    compatible_runtimes: list[str] | None = None,
    description: str = "",
    function_names: list[str] | None = None,
    region_name: str | None = None,
) -> LayerPublishResult:
    """Package a directory into a Lambda Layer ZIP and publish it.

    Args:
        layer_name: Name for the Lambda layer.
        directory: Local directory to package into the layer.
        compatible_runtimes: List of compatible runtimes.
        description: Layer description.
        function_names: Lambda functions to update with the new layer.
        region_name: AWS region override.

    Returns:
        A :class:`LayerPublishResult` with the published layer details.

    Raises:
        RuntimeError: If packaging or publishing fails.
    """
    lam = async_client("lambda", region_name)

    # Build ZIP from directory (disk I/O in a thread)
    def _build_zip() -> bytes:
        buf = io.BytesIO()
        try:
            with zipfile.ZipFile(
                buf,
                "w",
                zipfile.ZIP_DEFLATED,
            ) as zf:
                for root, _dirs, files in os.walk(directory):
                    for fname in files:
                        full_path = os.path.join(root, fname)
                        arcname = os.path.relpath(
                            full_path,
                            directory,
                        )
                        zf.write(full_path, arcname)
        except OSError as exc:
            raise wrap_aws_error(exc, f"Failed to package directory {directory}") from exc
        return buf.getvalue()

    zip_bytes = await asyncio.to_thread(_build_zip)

    # Publish layer version
    publish_kwargs: dict[str, Any] = {
        "LayerName": layer_name,
        "Content": {"ZipFile": zip_bytes},
        "Description": description,
    }
    if compatible_runtimes:
        publish_kwargs["CompatibleRuntimes"] = compatible_runtimes

    try:
        resp = await lam.call(
            "PublishLayerVersion",
            **publish_kwargs,
        )
        version_number = resp["Version"]
        layer_arn = resp["LayerVersionArn"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to publish layer {layer_name}") from exc

    # Update functions to use the new layer
    updated_functions: list[str] = []
    if function_names:
        for fn_name in function_names:
            try:
                config = await lam.call(
                    "GetFunctionConfiguration",
                    FunctionName=fn_name,
                )
                existing_layers = [lyr["Arn"] for lyr in config.get("Layers", [])]
                new_layers = [
                    arn
                    for arn in existing_layers
                    if not arn.startswith(layer_arn.rsplit(":", 1)[0])
                ]
                new_layers.append(layer_arn)

                await lam.call(
                    "UpdateFunctionConfiguration",
                    FunctionName=fn_name,
                    Layers=new_layers,
                )
                updated_functions.append(fn_name)
            except Exception as exc:
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


async def _get_stack_outputs(
    cfn: Any,
    stack_name: str,
) -> dict[str, str]:
    """Extract outputs from a CloudFormation stack."""
    try:
        resp = await cfn.call(
            "DescribeStacks",
            StackName=stack_name,
        )
        stacks = resp.get("Stacks", [])
        if not stacks:
            return {}
        raw_outputs = stacks[0].get("Outputs", [])
        return {o["OutputKey"]: o["OutputValue"] for o in raw_outputs}
    except Exception:
        return {}


async def stack_deployer(
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

    Args:
        stack_name: CloudFormation stack name.
        template_body: Template body string.
        template_url: S3 URL of the template.
        parameters: Stack parameters as key-value pairs.
        capabilities: IAM capabilities.
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

    cfn = async_client("cloudformation", region_name)

    # Check if stack exists
    stack_exists = False
    try:
        await cfn.call("DescribeStacks", StackName=stack_name)
        stack_exists = True
    except RuntimeError:
        pass

    change_set_name = f"{stack_name}-cs-{int(time.time())}"
    cs_type = "UPDATE" if stack_exists else "CREATE"

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
        cs_resp = await cfn.call("CreateChangeSet", **cs_kwargs)
        change_set_id = cs_resp["Id"]
        stack_id = cs_resp["StackId"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create change set for {stack_name}") from exc

    # Wait for change set to be ready
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            desc = await cfn.call(
                "DescribeChangeSet",
                ChangeSetName=change_set_id,
            )
            status = desc["Status"]
            if status == "CREATE_COMPLETE":
                break
            if status == "FAILED":
                reason = desc.get("StatusReason", "Unknown")
                if "didn't contain changes" in reason.lower() or "no updates" in reason.lower():
                    with contextlib.suppress(RuntimeError):
                        await cfn.call(
                            "DeleteChangeSet",
                            ChangeSetName=change_set_id,
                        )
                    outputs = await _get_stack_outputs(
                        cfn,
                        stack_name,
                    )
                    return StackDeployResult(
                        stack_name=stack_name,
                        stack_id=stack_id,
                        status="NO_CHANGES",
                        outputs=outputs,
                        change_set_id=change_set_id,
                    )
                raise AwsServiceError(f"Change set failed: {reason}")
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to describe change set") from exc
        await asyncio.sleep(2)
    else:
        raise TimeoutError(
            f"Change set for {stack_name} did not become ready within {timeout_seconds}s"
        )

    # Execute change set
    try:
        await cfn.call(
            "ExecuteChangeSet",
            ChangeSetName=change_set_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to execute change set for {stack_name}") from exc

    # Wait for stack to reach terminal state
    while time.time() < deadline:
        try:
            stack_desc = await cfn.call(
                "DescribeStacks",
                StackName=stack_name,
            )
            stacks = stack_desc["Stacks"]
            if not stacks:
                raise AwsServiceError(f"Stack {stack_name} not found")
            stack_status = stacks[0].get(
                "StackStatus",
                stacks[0].get("Status", ""),
            )
            if stack_status.endswith("_COMPLETE"):
                if "ROLLBACK" in stack_status:
                    raise AwsServiceError(f"Stack {stack_name} rolled back: {stack_status}")
                outputs = await _get_stack_outputs(
                    cfn,
                    stack_name,
                )
                return StackDeployResult(
                    stack_name=stack_name,
                    stack_id=stack_id,
                    status=stack_status,
                    outputs=outputs,
                    change_set_id=change_set_id,
                )
            if stack_status.endswith("_FAILED"):
                raise AwsServiceError(f"Stack {stack_name} failed: {stack_status}")
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to describe stack {stack_name}") from exc
        await asyncio.sleep(2)

    raise TimeoutError(f"Stack {stack_name} did not complete within {timeout_seconds}s")


# ---------------------------------------------------------------------------
# 4. Environment promoter
# ---------------------------------------------------------------------------


async def environment_promoter(
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

    Args:
        function_name: Base function name.
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

    source_lam = async_client("lambda", src_region)
    source_func = f"{function_name}-{source_stage}"
    target_func = f"{function_name}-{target_stage}"

    # Read source configuration
    try:
        src_config = await source_lam.call(
            "GetFunctionConfiguration",
            FunctionName=source_func,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get config for {source_func}") from exc

    env_vars = src_config.get("Environment", {}).get("Variables", {})
    if extra_env_vars:
        env_vars.update(extra_env_vars)

    # Get target client (optionally cross-account)
    if target_role_arn:
        sts = async_client("sts", region_name)
        try:
            creds_resp = await sts.call(
                "AssumeRole",
                RoleArn=target_role_arn,
                RoleSessionName="env-promoter",
            )
            creds = creds_resp["Credentials"]
            import boto3

            target_lam_sync = boto3.client(
                "lambda",
                region_name=tgt_region,
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"],
            )
            # Use to_thread for cross-account calls
            await asyncio.to_thread(
                target_lam_sync.update_function_configuration,
                FunctionName=target_func,
                Environment={"Variables": env_vars},
                Timeout=src_config.get("Timeout", 30),
                MemorySize=src_config.get("MemorySize", 128),
            )
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to promote to {target_func}") from exc

        # Alias handling for cross-account
        alias_created = False
        if alias_name:
            try:
                try:
                    await asyncio.to_thread(
                        target_lam_sync.get_alias,
                        FunctionName=target_func,
                        Name=alias_name,
                    )
                    publish_resp = await asyncio.to_thread(
                        target_lam_sync.publish_version,
                        FunctionName=target_func,
                    )
                    await asyncio.to_thread(
                        target_lam_sync.update_alias,
                        FunctionName=target_func,
                        Name=alias_name,
                        FunctionVersion=publish_resp["Version"],
                    )
                except Exception:
                    publish_resp = await asyncio.to_thread(
                        target_lam_sync.publish_version,
                        FunctionName=target_func,
                    )
                    await asyncio.to_thread(
                        target_lam_sync.create_alias,
                        FunctionName=target_func,
                        Name=alias_name,
                        FunctionVersion=publish_resp["Version"],
                    )
                    alias_created = True
            except Exception as exc:
                raise wrap_aws_error(
                    exc, f"Failed to create alias {alias_name} on {target_func}"
                ) from exc
    else:
        target_lam = async_client("lambda", tgt_region)
        try:
            await target_lam.call(
                "UpdateFunctionConfiguration",
                FunctionName=target_func,
                Environment={"Variables": env_vars},
                Timeout=src_config.get("Timeout", 30),
                MemorySize=src_config.get("MemorySize", 128),
            )
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to update config for {target_func}") from exc

        alias_created = False
        if alias_name:
            try:
                await target_lam.call(
                    "GetAlias",
                    FunctionName=target_func,
                    Name=alias_name,
                )
                publish_resp = await target_lam.call(  # type: ignore[assignment]
                    "PublishVersion",
                    FunctionName=target_func,
                )
                await target_lam.call(
                    "UpdateAlias",
                    FunctionName=target_func,
                    Name=alias_name,
                    FunctionVersion=publish_resp["Version"],
                )
            except RuntimeError:
                try:
                    publish_resp = await target_lam.call(  # type: ignore[assignment]
                        "PublishVersion",
                        FunctionName=target_func,
                    )
                    await target_lam.call(
                        "CreateAlias",
                        FunctionName=target_func,
                        Name=alias_name,
                        FunctionVersion=publish_resp["Version"],
                    )
                    alias_created = True
                except Exception as exc:
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


async def lambda_warmer(
    function_name: str,
    schedule_expression: str = "rate(5 minutes)",
    rule_name: str | None = None,
    payload: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> LambdaWarmerResult:
    """Create an EventBridge rule to keep a Lambda warm.

    Args:
        function_name: Lambda function name or ARN.
        schedule_expression: EventBridge schedule.
        rule_name: Custom rule name.
        payload: Custom warm-up payload.
        region_name: AWS region override.

    Returns:
        A :class:`LambdaWarmerResult` with rule details.

    Raises:
        RuntimeError: If EventBridge or Lambda API calls fail.
    """
    events = async_client("events", region_name)
    lam = async_client("lambda", region_name)

    if rule_name is None:
        rule_name = f"warmer-{function_name}"
    if payload is None:
        payload = {"warmer": True}

    # Get function ARN
    try:
        fn_config = await lam.call(
            "GetFunctionConfiguration",
            FunctionName=function_name,
        )
        function_arn = fn_config["FunctionArn"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get function {function_name}") from exc

    # Create or update rule
    try:
        rule_resp = await events.call(
            "PutRule",
            Name=rule_name,
            ScheduleExpression=schedule_expression,
            State="ENABLED",
        )
        rule_arn = rule_resp["RuleArn"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create rule {rule_name}") from exc

    # Add Lambda permission for EventBridge
    try:
        await lam.call(
            "AddPermission",
            FunctionName=function_name,
            StatementId=f"{rule_name}-invoke",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=rule_arn,
        )
    except RuntimeError:
        pass  # Permission may already exist

    # Add target
    try:
        await events.call(
            "PutTargets",
            Rule=rule_name,
            Targets=[
                {
                    "Id": f"{function_name}-warmer",
                    "Arn": function_arn,
                    "Input": json.dumps(payload),
                },
            ],
        )
    except Exception as exc:
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


async def config_drift_detector(
    function_names: list[str] | None = None,
    api_ids: list[str] | None = None,
    desired_state_ssm_prefix: str | None = None,
    desired_state_s3: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DriftDetectionResult:
    """Compare deployed Lambda/API GW configs against desired state.

    Args:
        function_names: Lambda functions to check.
        api_ids: API Gateway REST API IDs to check.
        desired_state_ssm_prefix: SSM parameter prefix containing desired
            config as JSON values.
        desired_state_s3: Dict with ``"bucket"`` and ``"key"``.
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
        ssm = async_client("ssm", region_name)
        try:
            params = await ssm.paginate(
                "GetParametersByPath",
                "Parameters",
                Path=desired_state_ssm_prefix,
                Recursive=True,
                WithDecryption=True,
            )
            for param in params:
                key = param["Name"].replace(
                    desired_state_ssm_prefix,
                    "",
                )
                try:
                    desired[key] = json.loads(param["Value"])
                except (json.JSONDecodeError, TypeError):
                    desired[key] = param["Value"]
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to load desired state from SSM") from exc

    if desired_state_s3:
        s3 = async_client("s3", region_name)
        try:
            resp = await s3.call(
                "GetObject",
                Bucket=desired_state_s3["bucket"],
                Key=desired_state_s3["key"],
            )
            body = resp.get("Body", b"")
            if hasattr(body, "read"):
                body = body.read()
            if isinstance(body, bytes):
                body = body.decode("utf-8")
            s3_desired = json.loads(body)
            desired.update(s3_desired)
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to load desired state from S3") from exc

    # Check Lambda functions
    if function_names:
        lam = async_client("lambda", region_name)
        for fn_name in function_names:
            resources_checked += 1
            try:
                config = await lam.call(
                    "GetFunctionConfiguration",
                    FunctionName=fn_name,
                )
            except Exception as exc:
                raise wrap_aws_error(exc, f"Failed to get config for {fn_name}") from exc

            fn_desired = desired.get(fn_name, {})
            if isinstance(fn_desired, dict):
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
                if "Environment" in fn_desired:
                    actual_env = config.get(
                        "Environment",
                        {},
                    ).get("Variables", {})
                    expected_env = fn_desired["Environment"].get("Variables", {})
                    for key, val in expected_env.items():
                        actual_val = actual_env.get(key)
                        if actual_val != val:
                            drift_items.append(
                                DriftReport(
                                    resource_type="Lambda",
                                    resource_name=fn_name,
                                    property_name=(f"Environment.Variables.{key}"),
                                    expected=str(val),
                                    actual=str(actual_val),
                                )
                            )

    # Check API Gateway
    if api_ids:
        apigw = async_client("apigateway", region_name)
        for api_id in api_ids:
            resources_checked += 1
            try:
                api = await apigw.call(
                    "GetRestApi",
                    restApiId=api_id,
                )
            except Exception as exc:
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


async def rollback_manager(
    function_name: str,
    alias_name: str,
    error_metric_name: str = "Errors",
    error_threshold: float = 5.0,
    evaluation_minutes: int = 5,
    region_name: str | None = None,
) -> RollbackResult:
    """Detect error-rate spikes and auto-roll back a Lambda alias.

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
    lam = async_client("lambda", region_name)
    cw = async_client("cloudwatch", region_name)

    try:
        alias_resp = await lam.call(
            "GetAlias",
            FunctionName=function_name,
            Name=alias_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get alias {alias_name} for {function_name}") from exc

    current_version = alias_resp["FunctionVersion"]
    routing = alias_resp.get("RoutingConfig", {})
    additional_weights = routing.get(
        "AdditionalVersionWeights",
        {},
    )

    if additional_weights:
        next(iter(additional_weights.keys()))
        previous_version = current_version
    else:
        previous_version = str(max(1, int(current_version) - 1))

    # Query CloudWatch metrics
    import datetime as _dt

    end_time = _dt.datetime.now(tz=_dt.UTC)
    start_time = end_time - _dt.timedelta(
        minutes=evaluation_minutes,
    )

    try:
        metric_resp = await cw.call(
            "GetMetricStatistics",
            Namespace="AWS/Lambda",
            MetricName=error_metric_name,
            Dimensions=[
                {
                    "Name": "FunctionName",
                    "Value": function_name,
                },
            ],
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Period=evaluation_minutes * 60,
            Statistics=["Sum"],
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get metrics for {function_name}") from exc

    datapoints = metric_resp.get("Datapoints", [])
    error_rate = sum(dp.get("Sum", 0.0) for dp in datapoints)

    if error_rate > error_threshold:
        try:
            await lam.call(
                "UpdateAlias",
                FunctionName=function_name,
                Name=alias_name,
                FunctionVersion=previous_version,
                RoutingConfig={},
            )
        except Exception as exc:
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


def _should_exclude(path: str, patterns: list[str]) -> bool:
    """Check if a file path matches any exclusion pattern."""
    import fnmatch

    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        for part in path.replace("\\", "/").split("/"):
            if fnmatch.fnmatch(part, pattern):
                return True
    return False


async def lambda_package_builder(
    source_dir: str,
    s3_bucket: str,
    s3_key: str,
    requirements_file: str | None = None,
    exclude_patterns: list[str] | None = None,
    region_name: str | None = None,
) -> PackageBuildResult:
    """Bundle Python Lambda code + dependencies into a ZIP and upload to S3.

    Args:
        source_dir: Directory containing Lambda code.
        s3_bucket: S3 bucket for the deployment package.
        s3_key: S3 key for the ZIP file.
        requirements_file: Path to ``requirements.txt``.
        exclude_patterns: File patterns to exclude.
        region_name: AWS region override.

    Returns:
        A :class:`PackageBuildResult` with upload details.

    Raises:
        RuntimeError: If packaging or upload fails.
    """
    s3 = async_client("s3", region_name)

    if exclude_patterns is None:
        exclude_patterns = ["__pycache__", "*.pyc", ".git"]

    # Build ZIP in a thread (CPU/disk bound)
    def _build_zip() -> tuple[bytes, int]:
        buf = io.BytesIO()
        files_included = 0

        with zipfile.ZipFile(
            buf,
            "w",
            zipfile.ZIP_DEFLATED,
        ) as zf:
            if requirements_file:
                with tempfile.TemporaryDirectory() as tmpdir:
                    try:
                        subprocess.run(
                            [
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
                        raise AwsServiceError(f"Failed to install dependencies: {exc}") from exc

                    for root, _dirs, files in os.walk(tmpdir):
                        for fname in files:
                            full_path = os.path.join(
                                root,
                                fname,
                            )
                            arcname = os.path.relpath(
                                full_path,
                                tmpdir,
                            )
                            if not _should_exclude(
                                arcname,
                                exclude_patterns,
                            ):
                                zf.write(full_path, arcname)
                                files_included += 1

            for root, _dirs, files in os.walk(source_dir):
                for fname in files:
                    full_path = os.path.join(root, fname)
                    arcname = os.path.relpath(
                        full_path,
                        source_dir,
                    )
                    if not _should_exclude(
                        arcname,
                        exclude_patterns,
                    ):
                        zf.write(full_path, arcname)
                        files_included += 1

        return buf.getvalue(), files_included

    zip_bytes, files_included = await asyncio.to_thread(
        _build_zip,
    )

    try:
        await s3.call(
            "PutObject",
            Bucket=s3_bucket,
            Key=s3_key,
            Body=zip_bytes,
        )
    except Exception as exc:
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


async def cloudfront_invalidation_with_logging(
    distribution_id: str,
    paths: list[str],
    log_group_name: str,
    region_name: str | None = None,
) -> InvalidationLogResult:
    """Submit a CloudFront invalidation, wait for completion, log to CloudWatch.

    Args:
        distribution_id: CloudFront distribution ID.
        paths: List of URL paths to invalidate.
        log_group_name: CloudWatch Logs group name.
        region_name: AWS region override.

    Returns:
        An :class:`InvalidationLogResult` with invalidation details.

    Raises:
        RuntimeError: If CloudFront or CloudWatch Logs API calls fail.
    """
    import uuid

    cf = async_client("cloudfront", region_name)
    logs = async_client("logs", region_name)

    caller_ref = str(uuid.uuid4())
    try:
        resp = await cf.call(
            "CreateInvalidation",
            DistributionId=distribution_id,
            InvalidationBatch={
                "Paths": {"Quantity": len(paths), "Items": paths},
                "CallerReference": caller_ref,
            },
        )
        inv = resp["Invalidation"]
        inv_id = inv["Id"]
        status = inv["Status"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create invalidation for {distribution_id}") from exc

    # Poll until Completed
    for _ in range(120):
        if status == "Completed":
            break
        await asyncio.sleep(5)
        try:
            get_resp = await cf.call(
                "GetInvalidation",
                DistributionId=distribution_id,
                Id=inv_id,
            )
            status = get_resp["Invalidation"]["Status"]
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to poll invalidation {inv_id}") from exc

    # Log to CloudWatch
    import json as _json

    log_stream = f"invalidation-{inv_id}"
    log_msg = _json.dumps(
        {
            "invalidation_id": inv_id,
            "distribution_id": distribution_id,
            "status": status,
            "paths": paths,
        }
    )
    logged = False
    try:
        try:
            await logs.call("CreateLogGroup", logGroupName=log_group_name)
        except RuntimeError:
            pass
        try:
            await logs.call(
                "CreateLogStream", logGroupName=log_group_name, logStreamName=log_stream
            )
        except RuntimeError:
            pass
        await logs.call(
            "PutLogEvents",
            logGroupName=log_group_name,
            logStreamName=log_stream,
            logEvents=[{"timestamp": int(time.time() * 1000), "message": log_msg}],
        )
        logged = True
    except Exception as exc:
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


async def elastic_beanstalk_env_refresher(
    application_name: str,
    environment_name: str,
    version_label: str,
    ssm_prefix: str,
    region_name: str | None = None,
) -> BeanstalkRefreshResult:
    """Deploy a new Beanstalk version with SSM Parameter Store env vars injected.

    Args:
        application_name: Elastic Beanstalk application name.
        environment_name: Target environment name.
        version_label: Application version to deploy.
        ssm_prefix: SSM parameter hierarchy prefix.
        region_name: AWS region override.

    Returns:
        A :class:`BeanstalkRefreshResult` with environment status.

    Raises:
        RuntimeError: If SSM or Beanstalk API calls fail.
    """
    ssm = async_client("ssm", region_name)
    eb = async_client("elasticbeanstalk", region_name)

    option_settings: list[dict[str, str]] = []
    try:
        params = await ssm.paginate(
            "GetParametersByPath",
            "Parameters",
            Path=ssm_prefix,
            Recursive=True,
            WithDecryption=True,
        )
        for param in params:
            var_name = param["Name"].split("/")[-1]
            option_settings.append(
                {
                    "Namespace": "aws:elasticbeanstalk:application:environment",
                    "OptionName": var_name,
                    "Value": param["Value"],
                }
            )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to read SSM prefix {ssm_prefix}") from exc

    try:
        await eb.call(
            "UpdateEnvironment",
            ApplicationName=application_name,
            EnvironmentName=environment_name,
            VersionLabel=version_label,
            OptionSettings=option_settings,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to update Beanstalk environment {environment_name}"
        ) from exc

    env_id = ""
    env_status = "Updating"
    try:
        desc = await eb.call(
            "DescribeEnvironments",
            ApplicationName=application_name,
            EnvironmentNames=[environment_name],
        )
        envs = desc.get("Environments", [])
        if envs:
            env_id = envs[0].get("EnvironmentId", "")
            env_status = envs[0].get("Status", "Updating")
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to describe environment {environment_name}") from exc

    return BeanstalkRefreshResult(
        environment_id=env_id,
        status=env_status,
        params_injected=len(option_settings),
    )


# ---------------------------------------------------------------------------
# 11. App Runner auto deployer
# ---------------------------------------------------------------------------


async def app_runner_auto_deployer(
    service_arn: str,
    repository_name: str,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> AppRunnerDeployResult:
    """Check ECR for the latest image, update App Runner if changed, notify via SNS.

    Args:
        service_arn: App Runner service ARN.
        repository_name: ECR repository name.
        sns_topic_arn: Optional SNS topic ARN.
        region_name: AWS region override.

    Returns:
        An :class:`AppRunnerDeployResult` with update details.

    Raises:
        RuntimeError: If ECR, App Runner, or SNS API calls fail.
    """
    import json as _json

    ecr = async_client("ecr", region_name)
    apprunner = async_client("apprunner", region_name)

    try:
        images_resp = await ecr.call(
            "DescribeImages",
            repositoryName=repository_name,
            filter={"tagStatus": "TAGGED"},
        )
        images = sorted(
            images_resp.get("imageDetails", []),
            key=lambda x: x.get("imagePushedAt", 0),
            reverse=True,
        )
        latest_tag = images[0]["imageTags"][0] if images else "latest"
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to describe ECR images for {repository_name}") from exc

    try:
        svc_resp = await apprunner.call("DescribeService", ServiceArn=service_arn)
        svc = svc_resp["Service"]
        service_id = svc["ServiceId"]
        current_img = (
            svc.get("SourceConfiguration", {}).get("ImageRepository", {}).get("ImageIdentifier", "")
        )
        current_tag = current_img.split(":")[-1] if ":" in current_img else ""
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to describe App Runner service {service_arn}") from exc

    if current_tag == latest_tag:
        return AppRunnerDeployResult(
            service_id=service_id,
            image_updated=False,
            new_image_tag=latest_tag,
        )

    registry_id = images[0].get("registryId", "") if images else ""
    new_image_uri = f"{registry_id}.dkr.ecr.{region_name or 'us-east-1'}.amazonaws.com/{repository_name}:{latest_tag}"

    try:
        update_resp = await apprunner.call(
            "UpdateService",
            ServiceArn=service_arn,
            SourceConfiguration={
                "ImageRepository": {
                    "ImageIdentifier": new_image_uri,
                    "ImageRepositoryType": "ECR",
                }
            },
        )
        operation_id = update_resp.get("OperationId")
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to update App Runner service {service_arn}") from exc

    if sns_topic_arn:
        sns = async_client("sns", region_name)
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject="App Runner Service Updated",
                Message=_json.dumps(
                    {
                        "service_arn": service_arn,
                        "new_image": new_image_uri,
                        "operation_id": operation_id,
                    }
                ),
            )
        except Exception as exc:
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


async def eks_node_group_scaler(
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

    Args:
        cluster_name: EKS cluster name.
        nodegroup_name: Managed node group name.
        metric_name: CloudWatch metric name.
        metric_namespace: CloudWatch metric namespace.
        threshold: Metric value above which scale-up is triggered.
        scale_up_size: Desired count when scaling up.
        scale_down_size: Desired count when scaling down.
        region_name: AWS region override.

    Returns:
        A :class:`NodeGroupScaleResult` with before/after sizes.

    Raises:
        RuntimeError: If EKS or CloudWatch API calls fail.
    """
    import datetime

    eks = async_client("eks", region_name)
    cw = async_client("cloudwatch", region_name)

    try:
        ng_resp = await eks.call(
            "DescribeNodegroup",
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
        )
        scaling = ng_resp["nodegroup"]["scalingConfig"]
        current_size = scaling.get("desiredSize", 0)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to describe node group {nodegroup_name}") from exc

    end_time = datetime.datetime.now(tz=datetime.UTC)
    start_time = end_time - datetime.timedelta(minutes=5)
    try:
        metric_resp = await cw.call(
            "GetMetricStatistics",
            Namespace=metric_namespace,
            MetricName=metric_name,
            Dimensions=[{"Name": "ClusterName", "Value": cluster_name}],
            StartTime=start_time.isoformat(),
            EndTime=end_time.isoformat(),
            Period=300,
            Statistics=["Average"],
        )
        datapoints = metric_resp.get("Datapoints", [])
        metric_value = datapoints[-1]["Average"] if datapoints else 0.0
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get metric {metric_name}") from exc

    desired_size = scale_up_size if metric_value > threshold else scale_down_size
    scaled = desired_size != current_size

    if scaled:
        try:
            await eks.call(
                "UpdateNodegroupConfig",
                clusterName=cluster_name,
                nodegroupName=nodegroup_name,
                scalingConfig={"desiredSize": desired_size},
            )
        except Exception as exc:
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


async def eks_config_map_sync(
    cluster_name: str,
    ssm_prefix: str,
    table_name: str,
    config_map_name: str,
    region_name: str | None = None,
) -> ConfigMapSyncResult:
    """Sync SSM Parameter Store hierarchy to DynamoDB as ConfigMap data.

    Args:
        cluster_name: EKS cluster name (stored as metadata).
        ssm_prefix: SSM path prefix.
        table_name: DynamoDB table name.
        config_map_name: ConfigMap name (stored as metadata).
        region_name: AWS region override.

    Returns:
        A :class:`ConfigMapSyncResult` with sync counts.

    Raises:
        RuntimeError: If SSM or DynamoDB API calls fail.
    """
    import json as _json

    ssm = async_client("ssm", region_name)
    ddb = async_client("dynamodb", region_name)

    data: dict[str, str] = {}
    try:
        params = await ssm.paginate(
            "GetParametersByPath",
            "Parameters",
            Path=ssm_prefix,
            Recursive=True,
            WithDecryption=True,
        )
        for param in params:
            key = param["Name"].split("/")[-1]
            data[key] = param["Value"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to read SSM prefix {ssm_prefix}") from exc

    table_updated = False
    try:
        await ddb.call(
            "PutItem",
            TableName=table_name,
            Item={
                "pk": {"S": f"configmap#{cluster_name}#{config_map_name}"},
                "cluster_name": {"S": cluster_name},
                "config_map_name": {"S": config_map_name},
                "data": {"S": _json.dumps(data)},
                "updated_at": {"N": str(int(time.time()))},
            },
        )
        table_updated = True
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to put ConfigMap data in DynamoDB {table_name}") from exc

    return ConfigMapSyncResult(
        parameters_synced=len(data),
        config_map_name=config_map_name,
        table_updated=table_updated,
    )


# ---------------------------------------------------------------------------
# 14. Batch job monitor
# ---------------------------------------------------------------------------


async def batch_job_monitor(
    job_name: str,
    job_queue: str,
    job_definition: str,
    parameters: dict[str, str] | None = None,
    metric_namespace: str = "AwsUtil/Batch",
    region_name: str | None = None,
) -> BatchJobResult:
    """Submit a Batch job, poll until terminal state, publish metrics to CloudWatch.

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
    batch = async_client("batch", region_name)
    cw = async_client("cloudwatch", region_name)

    submit_kwargs: dict[str, Any] = {
        "jobName": job_name,
        "jobQueue": job_queue,
        "jobDefinition": job_definition,
    }
    if parameters:
        submit_kwargs["parameters"] = parameters

    try:
        submit_resp = await batch.call("SubmitJob", **submit_kwargs)
        job_id = submit_resp["jobId"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to submit Batch job {job_name}") from exc

    start_time = time.time()
    status = "SUBMITTED"
    terminal_states = {"SUCCEEDED", "FAILED"}

    for _ in range(120):
        if status in terminal_states:
            break
        await asyncio.sleep(15)
        try:
            desc_resp = await batch.call("DescribeJobs", jobs=[job_id])
            jobs = desc_resp.get("jobs", [])
            if jobs:
                status = jobs[0].get("status", status)
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to describe Batch job {job_id}") from exc

    duration = time.time() - start_time
    metrics_published = 0
    try:
        await cw.call(
            "PutMetricData",
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
    except Exception as exc:
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


async def autoscaling_scheduled_action_manager(
    asg_name: str,
    table_name: str,
    region_name: str | None = None,
) -> ScheduledActionResult:
    """Create/update Auto Scaling Group scheduled actions from DynamoDB config.

    Args:
        asg_name: Auto Scaling Group name.
        table_name: DynamoDB table containing schedule configs.
        region_name: AWS region override.

    Returns:
        A :class:`ScheduledActionResult` with sync counts.

    Raises:
        RuntimeError: If DynamoDB or Auto Scaling API calls fail.
    """
    ddb = async_client("dynamodb", region_name)
    asg_client = async_client("autoscaling", region_name)

    schedule_items: list[dict[str, Any]] = []
    try:
        resp = await ddb.call(
            "Scan",
            TableName=table_name,
            FilterExpression="pk = :pk",
            ExpressionAttributeValues={":pk": {"S": asg_name}},
        )
        schedule_items = resp.get("Items", [])
    except Exception as exc:
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
            existing = await asg_client.call(
                "DescribeScheduledActions",
                AutoScalingGroupName=asg_name,
                ScheduledActionNames=[action_name],
            )
            await asg_client.call("PutScheduledUpdateGroupAction", **action_kwargs)
            if existing.get("ScheduledUpdateGroupActions"):
                actions_updated += 1
            else:
                actions_created += 1
        except Exception as exc:
            logger.warning("Failed to upsert scheduled action %s: %s", action_name, exc)

    return ScheduledActionResult(
        actions_synced=len(schedule_items),
        actions_created=actions_created,
        actions_updated=actions_updated,
    )


# ---------------------------------------------------------------------------
# 16. Step Functions execution tracker
# ---------------------------------------------------------------------------


async def stepfunctions_execution_tracker(
    state_machine_arn: str,
    input_data: dict[str, Any],
    execution_name: str | None = None,
    table_name: str = "",
    metric_namespace: str = "AwsUtil/StepFunctions",
    region_name: str | None = None,
) -> ExecutionTrackerResult:
    """Start a Step Functions execution, store ARN in DynamoDB, poll and emit metrics.

    Args:
        state_machine_arn: Step Functions state machine ARN.
        input_data: JSON-serialisable input dict.
        execution_name: Optional name for the execution.
        table_name: DynamoDB table to record the execution ARN.
        metric_namespace: CloudWatch namespace for duration metric.
        region_name: AWS region override.

    Returns:
        An :class:`ExecutionTrackerResult` with status and output.

    Raises:
        RuntimeError: If Step Functions, DynamoDB, or CloudWatch calls fail.
    """
    import json as _json
    import uuid

    sfn = async_client("stepfunctions", region_name)
    ddb = async_client("dynamodb", region_name)
    cw = async_client("cloudwatch", region_name)

    exec_name = execution_name or f"exec-{uuid.uuid4().hex[:8]}"

    try:
        start_resp = await sfn.call(
            "StartExecution",
            stateMachineArn=state_machine_arn,
            name=exec_name,
            input=_json.dumps(input_data),
        )
        execution_arn = start_resp["executionArn"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to start execution for {state_machine_arn}") from exc

    start_ts = int(time.time())

    if table_name:
        try:
            await ddb.call(
                "PutItem",
                TableName=table_name,
                Item={
                    "pk": {"S": execution_arn},
                    "state_machine_arn": {"S": state_machine_arn},
                    "execution_name": {"S": exec_name},
                    "started_at": {"N": str(start_ts)},
                    "status": {"S": "RUNNING"},
                },
            )
        except Exception as exc:
            logger.warning("Failed to record execution in DynamoDB: %s", exc)

    start_time = time.time()
    status = "RUNNING"
    raw_output: str | None = None
    terminal_states = {"SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"}

    for _ in range(120):
        if status in terminal_states:
            break
        await asyncio.sleep(15)
        try:
            desc = await sfn.call("DescribeExecution", executionArn=execution_arn)
            status = desc.get("status", status)
            raw_output = desc.get("output")
        except Exception as exc:
            raise wrap_aws_error(exc, f"Failed to describe execution {execution_arn}") from exc

    duration = time.time() - start_time
    output: dict[str, Any] | None = None
    if raw_output:
        try:
            output = _json.loads(raw_output)
        except (json.JSONDecodeError, Exception):
            output = {"raw": raw_output}

    try:
        await cw.call(
            "PutMetricData",
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
    except Exception as exc:
        logger.warning("Failed to emit Step Functions metric: %s", exc)

    return ExecutionTrackerResult(
        execution_arn=execution_arn,
        status=status,
        duration_seconds=round(duration, 2),
        output=output,
    )
