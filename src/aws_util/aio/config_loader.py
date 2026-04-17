"""Native async config loader using :mod:`aws_util.aio._engine`.

Combines SSM Parameter Store and Secrets Manager into higher-level helpers
for the common pattern of loading all app settings at startup.
"""

from __future__ import annotations

import asyncio
import json
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.config_loader import (
    _FLAG_CACHE,
    AppConfig,
    FeatureFlagResult,
    ParameterReplicateResult,
)
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AppConfig",
    "FeatureFlagResult",
    "ParameterReplicateResult",
    "appconfig_feature_flag_loader",
    "cross_region_parameter_replicator",
    "get_db_credentials",
    "get_ssm_parameter_map",
    "load_app_config",
    "load_config_from_secret",
    "load_config_from_ssm",
    "resolve_config",
]


async def load_config_from_ssm(
    path: str,
    strip_prefix: bool = True,
    recursive: bool = True,
    region_name: str | None = None,
) -> dict[str, str]:
    """Load all SSM parameters under *path* as a flat dict.

    Args:
        path: SSM path prefix, e.g. ``"/myapp/prod/"``.
        strip_prefix: If ``True`` (default), remove the *path* prefix from
            the returned keys so ``"/myapp/prod/db/host"`` becomes
            ``"db/host"``.
        recursive: Include parameters in sub-paths (default ``True``).
        region_name: AWS region override.

    Returns:
        A dict mapping parameter name -> value.

    Raises:
        RuntimeError: If the SSM API call fails.
    """
    client = async_client("ssm", region_name)
    raw: dict[str, str] = {}
    try:
        params = await client.paginate(
            "GetParametersByPath",
            "Parameters",
            Path=path,
            Recursive=recursive,
            WithDecryption=True,
        )
        for param in params:
            raw[param["Name"]] = param["Value"]
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to load SSM parameters under {path}") from exc

    if not strip_prefix:
        return raw
    prefix = path.rstrip("/") + "/"
    return {(k[len(prefix) :] if k.startswith(prefix) else k): v for k, v in raw.items()}


async def load_config_from_secret(
    secret_name: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Parse a JSON Secrets Manager secret and return its fields as a dict.

    Args:
        secret_name: Secret name, path, or ARN.  Must be a JSON object.
        region_name: AWS region override.

    Returns:
        A dict of all top-level key -> value pairs in the secret.

    Raises:
        ValueError: If the secret value is not valid JSON.
        RuntimeError: If the Secrets Manager API call fails.
    """
    client = async_client("secretsmanager", region_name)
    try:
        resp = await client.call("GetSecretValue", SecretId=secret_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to load secret {secret_name!r}") from exc

    raw = resp.get("SecretString", "{}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Secret {secret_name!r} is not valid JSON: {exc}") from exc


async def load_app_config(
    ssm_prefix: str | None = None,
    secret_names: list[str] | None = None,
    region_name: str | None = None,
) -> AppConfig:
    """Load and merge application config from SSM Parameter Store and Secrets Manager.

    All sources are fetched concurrently.  Merge order (highest precedence last):

    1. Each secret in *secret_names* (in order -- later secrets override earlier
       ones for duplicate keys).
    2. SSM parameters under *ssm_prefix* (highest precedence).

    Args:
        ssm_prefix: SSM path prefix -- all parameters under this path are
            included, with the prefix stripped from the key names.
        secret_names: List of Secrets Manager secret names whose JSON fields
            are merged into the config.
        region_name: AWS region override.

    Returns:
        An :class:`AppConfig` containing the merged values.

    Raises:
        RuntimeError: If any underlying API call fails.
    """
    tasks: dict[str, Any] = {}

    if secret_names:
        for name in secret_names:
            tasks[f"secret:{name}"] = load_config_from_secret(name, region_name=region_name)
    if ssm_prefix:
        tasks["ssm"] = load_config_from_ssm(ssm_prefix, region_name=region_name)

    results: dict[str, dict] = {}
    if tasks:
        gathered = await asyncio.gather(*tasks.values(), return_exceptions=False)
        for key, result in zip(tasks.keys(), gathered, strict=False):
            results[key] = result

    merged: dict[str, Any] = {}
    for name in secret_names or []:
        merged.update(results.get(f"secret:{name}", {}))
    if ssm_prefix:
        merged.update(results.get("ssm", {}))

    return AppConfig(values=merged)


async def resolve_config(
    config: dict[str, Any],
    region_name: str | None = None,
) -> dict[str, Any]:
    """Resolve ``${ssm:...}`` and ``${secret:...}`` placeholders in all string
    values of a config dict.

    Recursively processes nested dicts and lists.  Non-string scalars pass
    through unchanged.

    Args:
        config: Dict of configuration values, potentially containing
            placeholder strings.
        region_name: AWS region override (unused -- placeholder resolution uses
            the boto3-resolved region, but kept for API consistency).

    Returns:
        A new dict with all placeholders expanded.

    Raises:
        RuntimeError: If any placeholder cannot be resolved.
    """
    from aws_util.aio.placeholder import retrieve

    async def _resolve(value: Any) -> Any:
        if isinstance(value, str):
            return await retrieve(value)
        if isinstance(value, dict):
            resolved = {}
            for k, v in value.items():
                resolved[k] = await _resolve(v)
            return resolved
        if isinstance(value, list):
            return [await _resolve(item) for item in value]
        return value

    resolved: dict[str, Any] = {}
    for k, v in config.items():
        resolved[k] = await _resolve(v)
    return resolved


async def get_db_credentials(
    secret_name: str,
    region_name: str | None = None,
) -> dict[str, str]:
    """Fetch database credentials stored as a JSON Secrets Manager secret.

    Expects the secret to be a JSON object with at least ``"username"`` and
    ``"password"`` keys.  Additional keys (e.g. ``"host"``, ``"port"``,
    ``"dbname"``) are included in the returned dict.

    Args:
        secret_name: Secret name or ARN.
        region_name: AWS region override.

    Returns:
        A dict of credential fields.

    Raises:
        ValueError: If the secret is not valid JSON or is missing required
            keys.
        RuntimeError: If the API call fails.
    """
    creds = await load_config_from_secret(secret_name, region_name=region_name)
    missing = [k for k in ("username", "password") if k not in creds]
    if missing:
        raise ValueError(f"Secret {secret_name!r} is missing required keys: {missing}")
    return creds


async def get_ssm_parameter_map(
    names: list[str],
    region_name: str | None = None,
) -> dict[str, str]:
    """Fetch multiple specific SSM parameters by name and return them as a dict.

    Unlike :func:`load_config_from_ssm` (which loads by path prefix), this
    fetches an exact list of parameter names, chunking requests automatically.

    Args:
        names: List of SSM parameter names.
        region_name: AWS region override.

    Returns:
        A dict mapping parameter name -> value.  Missing parameters are
        silently omitted.

    Raises:
        RuntimeError: If any batch call fails.
    """
    client = async_client("ssm", region_name)
    result: dict[str, str] = {}

    for i in range(0, len(names), 10):
        chunk = names[i : i + 10]
        try:
            resp = await client.call("GetParameters", Names=chunk, WithDecryption=True)
            for param in resp.get("Parameters", []):
                result[param["Name"]] = param["Value"]
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to fetch SSM parameters batch") from exc

    return result


# ---------------------------------------------------------------------------
# AppConfig feature flag loader
# ---------------------------------------------------------------------------


async def appconfig_feature_flag_loader(
    application_id: str,
    environment_id: str,
    configuration_profile_id: str,
    metric_namespace: str | None = None,
    region_name: str | None = None,
) -> FeatureFlagResult:
    """Fetch AppConfig configuration profile, cache in memory, emit cache metrics.

    Starts an AppConfig Data session and retrieves the latest configuration.
    Responses are cached in a module-level dict shared with the sync module.

    Args:
        application_id: AppConfig application ID or name.
        environment_id: AppConfig environment ID or name.
        configuration_profile_id: AppConfig configuration profile ID.
        metric_namespace: Optional CloudWatch namespace for cache metrics.
        region_name: AWS region override.

    Returns:
        A :class:`FeatureFlagResult` with flag values and cache status.

    Raises:
        RuntimeError: If AppConfig Data or CloudWatch API calls fail.
    """
    appconfigdata = async_client("appconfigdata", region_name)

    cache_key = f"{application_id}/{environment_id}/{configuration_profile_id}"
    now = time.time()
    cached = False
    cache_age = 0.0

    if cache_key in _FLAG_CACHE:
        cached_flags, cached_version, fetched_at = _FLAG_CACHE[cache_key]
        cache_age = now - fetched_at
        cached = True
        flags = cached_flags
        version = cached_version
    else:
        try:
            session_resp = await appconfigdata.call(
                "StartConfigurationSession",
                ApplicationIdentifier=application_id,
                EnvironmentIdentifier=environment_id,
                ConfigurationProfileIdentifier=configuration_profile_id,
            )
            session_token = session_resp["InitialConfigurationToken"]
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to start AppConfig session") from exc

        try:
            config_resp = await appconfigdata.call(
                "GetLatestConfiguration",
                ConfigurationToken=session_token,
            )
            raw = config_resp.get("Configuration", b"")
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8")
            version = config_resp.get("VersionLabel", "unknown")
        except Exception as exc:
            raise wrap_aws_error(exc, "Failed to get AppConfig configuration") from exc

        try:
            flags = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            flags = {"raw": raw}

        _FLAG_CACHE[cache_key] = (flags, version, now)

    if metric_namespace:
        cw = async_client("cloudwatch", region_name)
        try:
            await cw.call(
                "PutMetricData",
                Namespace=metric_namespace,
                MetricData=[
                    {
                        "MetricName": "FeatureFlagCacheHit" if cached else "FeatureFlagCacheMiss",
                        "Dimensions": [{"Name": "ProfileId", "Value": configuration_profile_id}],
                        "Value": 1.0,
                        "Unit": "Count",
                    }
                ],
            )
        except Exception as exc:
            import logging

            logging.getLogger(__name__).warning("Failed to emit feature flag metric: %s", exc)

    return FeatureFlagResult(
        flags=flags,
        version=version,
        cached=cached,
        cache_age_seconds=round(cache_age, 2),
    )


# ---------------------------------------------------------------------------
# Cross-region parameter replicator
# ---------------------------------------------------------------------------


async def cross_region_parameter_replicator(
    parameter_names: list[str],
    source_region: str,
    target_regions: list[str],
    log_group_name: str | None = None,
    region_name: str | None = None,
) -> ParameterReplicateResult:
    """Read SSM parameters from source region and write to target regions.

    Fetches each parameter by name from *source_region* using
    ``get_parameter``, then calls ``put_parameter`` in each target region.
    Optionally logs sync operations to CloudWatch Logs.

    Args:
        parameter_names: List of fully-qualified SSM parameter names.
        source_region: AWS region to read parameters from.
        target_regions: List of AWS regions to replicate parameters to.
        log_group_name: Optional CloudWatch Logs group for sync logging.
        region_name: AWS region for CloudWatch Logs.

    Returns:
        A :class:`ParameterReplicateResult` with replication counts.

    Raises:
        RuntimeError: If SSM API calls fail.
    """
    import logging as _logging

    logger = _logging.getLogger(__name__)
    src_ssm = async_client("ssm", source_region)
    cw_region = region_name or source_region
    logs_client = async_client("logs", cw_region) if log_group_name else None

    replicated = 0
    failures = 0
    log_events: list[dict[str, Any]] = []

    for name in parameter_names:
        try:
            param_resp = await src_ssm.call("GetParameter", Name=name, WithDecryption=True)
            param = param_resp["Parameter"]
            value = param["Value"]
            param_type = param.get("Type", "String")
        except Exception as exc:
            logger.warning("Failed to read parameter %s from %s: %s", name, source_region, exc)
            failures += len(target_regions)
            continue

        for tgt_region in target_regions:
            tgt_ssm = async_client("ssm", tgt_region)
            try:
                await tgt_ssm.call(
                    "PutParameter",
                    Name=name,
                    Value=value,
                    Type=param_type,
                    Overwrite=True,
                )
                replicated += 1
                log_events.append(
                    {
                        "timestamp": int(time.time() * 1000),
                        "message": json.dumps(
                            {
                                "action": "replicated",
                                "parameter": name,
                                "target_region": tgt_region,
                            }
                        ),
                    }
                )
            except Exception as exc:
                logger.warning("Failed to replicate %s to %s: %s", name, tgt_region, exc)
                failures += 1
                log_events.append(
                    {
                        "timestamp": int(time.time() * 1000),
                        "message": json.dumps(
                            {
                                "action": "failed",
                                "parameter": name,
                                "target_region": tgt_region,
                                "error": str(exc),
                            }
                        ),
                    }
                )

    if log_group_name and log_events and logs_client:
        log_stream = f"param-replication-{int(time.time())}"
        try:
            try:
                await logs_client.call("CreateLogGroup", logGroupName=log_group_name)
            except RuntimeError:
                pass
            try:
                await logs_client.call(
                    "CreateLogStream",
                    logGroupName=log_group_name,
                    logStreamName=log_stream,
                )
            except RuntimeError:
                pass
            await logs_client.call(
                "PutLogEvents",
                logGroupName=log_group_name,
                logStreamName=log_stream,
                logEvents=log_events[:10000],
            )
        except Exception as exc:
            logger.warning("Failed to write replication logs: %s", exc)

    return ParameterReplicateResult(
        parameters_replicated=replicated,
        target_regions=target_regions,
        failures=failures,
    )
