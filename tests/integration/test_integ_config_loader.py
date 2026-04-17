"""Integration tests for aws_util.config_loader against LocalStack."""
from __future__ import annotations

import json

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. load_config_from_ssm
# ---------------------------------------------------------------------------


class TestLoadConfigFromSsm:
    def test_loads_params(self):
        from aws_util.config_loader import load_config_from_ssm

        ssm = ls_client("ssm")
        ssm.put_parameter(Name="/app/test/db_host", Value="localhost", Type="String", Overwrite=True)
        ssm.put_parameter(Name="/app/test/db_port", Value="5432", Type="String", Overwrite=True)

        result = load_config_from_ssm(path="/app/test/", region_name=REGION)
        assert result["db_host"] == "localhost"
        assert result["db_port"] == "5432"

    def test_empty_path(self):
        from aws_util.config_loader import load_config_from_ssm

        result = load_config_from_ssm(path="/nonexistent/path/", region_name=REGION)
        assert result == {}


# ---------------------------------------------------------------------------
# 2. load_config_from_secret
# ---------------------------------------------------------------------------


class TestLoadConfigFromSecret:
    def test_loads_secret(self):
        from aws_util.config_loader import load_config_from_secret

        sm = ls_client("secretsmanager")
        try:
            sm.create_secret(
                Name="test-config-secret",
                SecretString=json.dumps({"api_key": "abc123", "api_url": "https://api.example.com"}),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId="test-config-secret",
                    SecretString=json.dumps({"api_key": "abc123", "api_url": "https://api.example.com"}),
                )
            else:
                raise

        result = load_config_from_secret(
            secret_name="test-config-secret",
            region_name=REGION,
        )
        assert result["api_key"] == "abc123"
        assert result["api_url"] == "https://api.example.com"


# ---------------------------------------------------------------------------
# 3. resolve_config (placeholder resolution)
# ---------------------------------------------------------------------------


class TestResolveConfig:
    def test_resolves_placeholders(self):
        from aws_util.config_loader import resolve_config

        ssm = ls_client("ssm")
        ssm.put_parameter(Name="/rc/test/host", Value="db.example.com", Type="String", Overwrite=True)

        sm = ls_client("secretsmanager")
        try:
            sm.create_secret(
                Name="rc-test-secret",
                SecretString=json.dumps({"password": "s3cret"}),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId="rc-test-secret",
                    SecretString=json.dumps({"password": "s3cret"}),
                )
            else:
                raise

        # resolve_config takes a config dict with ${ssm:...} / ${secret:...} placeholders
        config = {
            "host": "${ssm:/rc/test/host}",
            "password": "${secret:rc-test-secret:password}",
        }
        result = resolve_config(config=config, region_name=REGION)
        assert result["host"] == "db.example.com"
        assert result["password"] == "s3cret"


# ---------------------------------------------------------------------------
# 4. get_db_credentials
# ---------------------------------------------------------------------------


class TestGetDbCredentials:
    def test_returns_credentials(self):
        from aws_util.config_loader import get_db_credentials

        sm = ls_client("secretsmanager")
        try:
            sm.create_secret(
                Name="test-db-creds",
                SecretString=json.dumps({
                    "host": "db.example.com",
                    "port": 5432,
                    "username": "admin",
                    "password": "secret",
                    "dbname": "mydb",
                }),
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceExistsException":
                sm.put_secret_value(
                    SecretId="test-db-creds",
                    SecretString=json.dumps({
                        "host": "db.example.com",
                        "port": 5432,
                        "username": "admin",
                        "password": "secret",
                        "dbname": "mydb",
                    }),
                )
            else:
                raise

        result = get_db_credentials(
            secret_name="test-db-creds",
            region_name=REGION,
        )
        assert result["host"] == "db.example.com"
        assert result["username"] == "admin"


# ---------------------------------------------------------------------------
# 5. get_ssm_parameter_map
# ---------------------------------------------------------------------------


class TestGetSsmParameterMap:
    def test_returns_map(self):
        from aws_util.config_loader import get_ssm_parameter_map

        ssm = ls_client("ssm")
        ssm.put_parameter(Name="/pm/key1", Value="val1", Type="String", Overwrite=True)
        ssm.put_parameter(Name="/pm/key2", Value="val2", Type="String", Overwrite=True)

        result = get_ssm_parameter_map(
            names=["/pm/key1", "/pm/key2"],
            region_name=REGION,
        )
        assert result["/pm/key1"] == "val1"
        assert result["/pm/key2"] == "val2"


# ---------------------------------------------------------------------------
# 6. load_app_config
# ---------------------------------------------------------------------------


class TestLoadAppConfig:
    def test_returns_app_config(self):
        from aws_util.config_loader import load_app_config

        ssm = ls_client("ssm")
        ssm.put_parameter(Name="/lac/test/flag", Value="true", Type="String", Overwrite=True)

        result = load_app_config(
            ssm_prefix="/lac/test/",
            region_name=REGION,
        )
        assert "flag" in result
        assert result["flag"] == "true"


# ---------------------------------------------------------------------------
# 7. appconfig_feature_flag_loader
# ---------------------------------------------------------------------------


class TestAppconfigFeatureFlagLoader:
    @pytest.mark.skip(reason="AppConfig Data (appconfigdata) not available in LocalStack community")
    def test_loads_flags(self):
        from aws_util.config_loader import appconfig_feature_flag_loader

        result = appconfig_feature_flag_loader(
            application_id="test-app",
            environment_id="test-env",
            configuration_profile_id="test-profile",
            region_name=REGION,
        )
        assert isinstance(result.flags, dict)
        assert isinstance(result.version, str)
        assert isinstance(result.cached, bool)
        assert isinstance(result.cache_age_seconds, float)


# ---------------------------------------------------------------------------
# 8. cross_region_parameter_replicator
# ---------------------------------------------------------------------------


class TestCrossRegionParameterReplicator:
    def test_replicates_parameters(self):
        from aws_util.config_loader import cross_region_parameter_replicator

        ssm = ls_client("ssm")
        # Create source parameters
        ssm.put_parameter(
            Name="/replicate/test/param-a",
            Value="value-a",
            Type="String",
            Overwrite=True,
        )
        ssm.put_parameter(
            Name="/replicate/test/param-b",
            Value="value-b",
            Type="String",
            Overwrite=True,
        )

        # Replicate from REGION to REGION (LocalStack uses a single endpoint
        # regardless of region, so this exercises the full code path).
        result = cross_region_parameter_replicator(
            parameter_names=["/replicate/test/param-a", "/replicate/test/param-b"],
            source_region=REGION,
            target_regions=[REGION],
            region_name=REGION,
        )
        assert result.parameters_replicated == 2
        assert result.target_regions == [REGION]
        assert result.failures == 0

    def test_replicates_with_logging(self):
        from aws_util.config_loader import cross_region_parameter_replicator

        ssm = ls_client("ssm")
        ssm.put_parameter(
            Name="/replicate/log-test/param",
            Value="log-value",
            Type="String",
            Overwrite=True,
        )

        logs = ls_client("logs")
        log_group = "/test/replicator-log"
        try:
            logs.create_log_group(logGroupName=log_group)
        except Exception:
            pass

        result = cross_region_parameter_replicator(
            parameter_names=["/replicate/log-test/param"],
            source_region=REGION,
            target_regions=[REGION],
            log_group_name=log_group,
            region_name=REGION,
        )
        assert result.parameters_replicated == 1
        assert result.failures == 0

        # Cleanup
        try:
            logs.delete_log_group(logGroupName=log_group)
        except Exception:
            pass

    def test_handles_missing_parameter(self):
        from aws_util.config_loader import cross_region_parameter_replicator

        # Attempt to replicate a parameter that does not exist
        result = cross_region_parameter_replicator(
            parameter_names=["/replicate/nonexistent/param-xyz"],
            source_region=REGION,
            target_regions=[REGION],
            region_name=REGION,
        )
        # The function logs a warning and counts failures rather than raising
        assert result.parameters_replicated == 0
        assert result.failures >= 1
