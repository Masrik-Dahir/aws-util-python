"""config_loader — Batch application config loading from SSM + Secrets Manager.

Combines :mod:`aws_util.parameter_store` and :mod:`aws_util.secrets_manager`
into higher-level helpers for the common pattern of loading all app settings
at startup.
"""

from __future__ import annotations

import json
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
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

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AppConfig(BaseModel):
    """A merged application configuration loaded from SSM and Secrets Manager.

    Behaves like a read-only dict: supports ``config["key"]``, ``config.get()``,
    and ``"key" in config``.
    """

    model_config = ConfigDict(frozen=True)

    values: dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if not present."""
        return self.values.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.values[key]

    def __contains__(self, key: object) -> bool:
        return key in self.values

    def __repr__(self) -> str:
        return f"AppConfig(keys={list(self.values.keys())})"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_config_from_ssm(
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
        A dict mapping parameter name → value.

    Raises:
        RuntimeError: If the SSM API call fails.
    """
    from aws_util.parameter_store import get_parameters_by_path

    raw = get_parameters_by_path(path, recursive=recursive, region_name=region_name)
    if not strip_prefix:
        return raw
    prefix = path.rstrip("/") + "/"
    return {(k[len(prefix) :] if k.startswith(prefix) else k): v for k, v in raw.items()}


def load_config_from_secret(
    secret_name: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Parse a JSON Secrets Manager secret and return its fields as a dict.

    Args:
        secret_name: Secret name, path, or ARN.  Must be a JSON object.
        region_name: AWS region override.

    Returns:
        A dict of all top-level key → value pairs in the secret.

    Raises:
        ValueError: If the secret value is not valid JSON.
        RuntimeError: If the Secrets Manager API call fails.
    """
    from aws_util.secrets_manager import get_secret

    raw = get_secret(secret_name, region_name=region_name)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Secret {secret_name!r} is not valid JSON: {exc}") from exc


def load_app_config(
    ssm_prefix: str | None = None,
    secret_names: list[str] | None = None,
    region_name: str | None = None,
) -> AppConfig:
    """Load and merge application config from SSM Parameter Store and Secrets Manager.

    All sources are fetched concurrently.  Merge order (highest precedence last):

    1. Each secret in *secret_names* (in order — later secrets override earlier
       ones for duplicate keys).
    2. SSM parameters under *ssm_prefix* (highest precedence).

    Args:
        ssm_prefix: SSM path prefix — all parameters under this path are
            included, with the prefix stripped from the key names.
        secret_names: List of Secrets Manager secret names whose JSON fields
            are merged into the config.
        region_name: AWS region override.

    Returns:
        An :class:`AppConfig` containing the merged values.

    Raises:
        RuntimeError: If any underlying API call fails.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    tasks: dict[str, Any] = {}
    if secret_names:
        for name in secret_names:
            tasks[f"secret:{name}"] = lambda n=name: load_config_from_secret(
                n, region_name=region_name
            )
    if ssm_prefix:
        tasks["ssm"] = lambda: load_config_from_ssm(ssm_prefix, region_name=region_name)

    results: dict[str, dict] = {}
    if tasks:
        with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
            futures = {pool.submit(fn): key for key, fn in tasks.items()}
            for future in as_completed(futures):
                key = futures[future]
                results[key] = future.result()

    merged: dict[str, Any] = {}
    for name in secret_names or []:
        merged.update(results.get(f"secret:{name}", {}))
    if ssm_prefix:
        merged.update(results.get("ssm", {}))

    return AppConfig(values=merged)


def resolve_config(
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
        region_name: AWS region override (unused — placeholder resolution uses
            the boto3-resolved region, but kept for API consistency).

    Returns:
        A new dict with all placeholders expanded.

    Raises:
        RuntimeError: If any placeholder cannot be resolved.
    """
    from aws_util.placeholder import retrieve

    def _resolve(value: Any) -> Any:
        if isinstance(value, str):
            return retrieve(value)
        if isinstance(value, dict):
            return {k: _resolve(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_resolve(item) for item in value]
        return value

    return {k: _resolve(v) for k, v in config.items()}


def get_db_credentials(
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
    creds = load_config_from_secret(secret_name, region_name=region_name)
    missing = [k for k in ("username", "password") if k not in creds]
    if missing:
        raise ValueError(f"Secret {secret_name!r} is missing required keys: {missing}")
    return creds


def get_ssm_parameter_map(
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
        A dict mapping parameter name → value.  Missing parameters are
        silently omitted.

    Raises:
        RuntimeError: If any batch call fails.
    """
    from aws_util.parameter_store import get_parameters_batch

    result: dict[str, str] = {}
    for i in range(0, len(names), 10):
        chunk = names[i : i + 10]
        result.update(get_parameters_batch(chunk, region_name=region_name))
    return result


# ---------------------------------------------------------------------------
# AppConfig feature flag loader
# ---------------------------------------------------------------------------

# Module-level cache: {session_token: (flags, version, fetched_at)}
_FLAG_CACHE: dict[str, tuple[dict[str, Any], str, float]] = {}


class FeatureFlagResult(BaseModel):
    """Result of loading AppConfig feature flags."""

    model_config = ConfigDict(frozen=True)

    flags: dict[str, Any]
    version: str
    cached: bool
    cache_age_seconds: float


def appconfig_feature_flag_loader(
    application_id: str,
    environment_id: str,
    configuration_profile_id: str,
    metric_namespace: str | None = None,
    region_name: str | None = None,
) -> FeatureFlagResult:
    """Fetch AppConfig configuration profile, cache in memory, emit cache metrics.

    Starts an AppConfig Data session and retrieves the latest configuration.
    Responses are cached in a module-level dict to avoid redundant API calls
    within the same process lifetime.

    Args:
        application_id: AppConfig application ID or name.
        environment_id: AppConfig environment ID or name.
        configuration_profile_id: AppConfig configuration profile ID or name.
        metric_namespace: Optional CloudWatch namespace for cache metrics.
        region_name: AWS region override.

    Returns:
        A :class:`FeatureFlagResult` with flag values and cache status.

    Raises:
        RuntimeError: If AppConfig Data or CloudWatch API calls fail.
    """
    appconfigdata = get_client("appconfigdata", region_name)

    cache_key = f"{application_id}/{environment_id}/{configuration_profile_id}"
    now = time.time()
    cached = False
    cache_age = 0.0

    # Check cache
    if cache_key in _FLAG_CACHE:
        cached_flags, cached_version, fetched_at = _FLAG_CACHE[cache_key]
        cache_age = now - fetched_at
        cached = True
        flags = cached_flags
        version = cached_version
    else:
        # Start session and fetch
        try:
            session_resp = appconfigdata.start_configuration_session(
                ApplicationIdentifier=application_id,
                EnvironmentIdentifier=environment_id,
                ConfigurationProfileIdentifier=configuration_profile_id,
            )
            session_token = session_resp["InitialConfigurationToken"]
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to start AppConfig session") from exc

        try:
            config_resp = appconfigdata.get_latest_configuration(
                ConfigurationToken=session_token,
            )
            raw = config_resp.get("Configuration", b"")
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8")
            version = config_resp.get("VersionLabel", "unknown")
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to get AppConfig configuration") from exc

        try:
            flags = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            flags = {"raw": raw}

        _FLAG_CACHE[cache_key] = (flags, version, now)

    # Emit CloudWatch cache metric
    if metric_namespace:
        cw = get_client("cloudwatch", region_name)
        try:
            cw.put_metric_data(
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
        except ClientError as exc:
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


class ParameterReplicateResult(BaseModel):
    """Result of cross-region SSM parameter replication."""

    model_config = ConfigDict(frozen=True)

    parameters_replicated: int
    target_regions: list[str]
    failures: int


def cross_region_parameter_replicator(
    parameter_names: list[str],
    source_region: str,
    target_regions: list[str],
    log_group_name: str | None = None,
    region_name: str | None = None,
) -> ParameterReplicateResult:
    """Read SSM parameters from source region and write to target regions.

    Fetches each parameter by name from *source_region* using
    ``get_parameter``, then calls ``put_parameter`` (with ``Overwrite=True``)
    in each target region.  Optionally logs sync operations to CloudWatch Logs.

    Args:
        parameter_names: List of fully-qualified SSM parameter names.
        source_region: AWS region to read parameters from.
        target_regions: List of AWS regions to replicate parameters to.
        log_group_name: Optional CloudWatch Logs group for sync logging.
        region_name: AWS region for CloudWatch Logs (defaults to source).
        region_name: AWS region override (used for CloudWatch Logs).

    Returns:
        A :class:`ParameterReplicateResult` with replication counts.

    Raises:
        RuntimeError: If SSM API calls fail.
    """
    import logging as _logging

    logger = _logging.getLogger(__name__)
    src_ssm = get_client("ssm", source_region)
    cw_region = region_name or source_region
    logs_client = get_client("logs", cw_region) if log_group_name else None

    replicated = 0
    failures = 0
    log_events: list[dict[str, Any]] = []

    for name in parameter_names:
        # Read from source
        try:
            param_resp = src_ssm.get_parameter(Name=name, WithDecryption=True)
            param = param_resp["Parameter"]
            value = param["Value"]
            param_type = param.get("Type", "String")
        except ClientError as exc:
            logger.warning("Failed to read parameter %s from %s: %s", name, source_region, exc)
            failures += len(target_regions)
            continue

        # Write to each target region
        for tgt_region in target_regions:
            tgt_ssm = get_client("ssm", tgt_region)
            try:
                tgt_ssm.put_parameter(
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
            except ClientError as exc:
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

    # Write log events
    if log_group_name and log_events and logs_client:
        log_stream = f"param-replication-{int(time.time())}"
        try:
            try:
                logs_client.create_log_group(logGroupName=log_group_name)
            except ClientError:
                pass
            try:
                logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream)
            except ClientError:
                pass
            logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream,
                logEvents=log_events[:10000],  # CloudWatch limit
            )
        except ClientError as exc:
            logger.warning("Failed to write replication logs: %s", exc)

    return ParameterReplicateResult(
        parameters_replicated=replicated,
        target_regions=target_regions,
        failures=failures,
    )
