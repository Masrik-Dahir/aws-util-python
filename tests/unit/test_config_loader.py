"""Tests for aws_util.config_loader module."""
from __future__ import annotations

import json
import pytest

from aws_util.config_loader import (
    AppConfig,
    get_db_credentials,
    get_ssm_parameter_map,
    load_app_config,
    load_config_from_secret,
    load_config_from_ssm,
    resolve_config,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# AppConfig model
# ---------------------------------------------------------------------------


def test_app_config_get_existing_key():
    cfg = AppConfig(values={"host": "db.example.com"})
    assert cfg.get("host") == "db.example.com"


def test_app_config_get_missing_key_default():
    cfg = AppConfig(values={})
    assert cfg.get("missing") is None


def test_app_config_get_missing_key_custom_default():
    cfg = AppConfig(values={})
    assert cfg.get("missing", "fallback") == "fallback"


def test_app_config_getitem():
    cfg = AppConfig(values={"port": 5432})
    assert cfg["port"] == 5432


def test_app_config_getitem_missing_raises():
    cfg = AppConfig(values={})
    with pytest.raises(KeyError):
        _ = cfg["nonexistent"]


def test_app_config_contains_true():
    cfg = AppConfig(values={"key": "val"})
    assert "key" in cfg


def test_app_config_contains_false():
    cfg = AppConfig(values={"key": "val"})
    assert "other" not in cfg


def test_app_config_repr():
    cfg = AppConfig(values={"a": 1, "b": 2})
    r = repr(cfg)
    assert "AppConfig" in r
    assert "a" in r


def test_app_config_is_frozen():
    cfg = AppConfig(values={"x": 1})
    with pytest.raises(Exception):  # Pydantic frozen raises ValidationError or similar
        cfg.values = {}  # type: ignore[misc]


# ---------------------------------------------------------------------------
# load_config_from_ssm
# ---------------------------------------------------------------------------


def test_load_config_from_ssm_with_strip_prefix(ssm_client):
    ssm_client.put_parameter(Name="/app/prod/db/host", Value="prod-db", Type="String")
    ssm_client.put_parameter(Name="/app/prod/db/port", Value="5432", Type="String")
    result = load_config_from_ssm("/app/prod", region_name=REGION)
    assert result["db/host"] == "prod-db"
    assert result["db/port"] == "5432"


def test_load_config_from_ssm_without_strip_prefix(ssm_client):
    ssm_client.put_parameter(Name="/app/env/key", Value="val", Type="String")
    result = load_config_from_ssm("/app/env", strip_prefix=False, region_name=REGION)
    assert result["/app/env/key"] == "val"


def test_load_config_from_ssm_empty_path(ssm_client):
    result = load_config_from_ssm("/nonexistent/path", region_name=REGION)
    assert result == {}


# ---------------------------------------------------------------------------
# load_config_from_secret
# ---------------------------------------------------------------------------


def test_load_config_from_secret_valid_json(secrets_client):
    secrets_client.create_secret(
        Name="app/config",
        SecretString=json.dumps({"host": "db", "port": "5432"}),
    )
    result = load_config_from_secret("app/config", region_name=REGION)
    assert result["host"] == "db"
    assert result["port"] == "5432"


def test_load_config_from_secret_invalid_json(secrets_client):
    secrets_client.create_secret(Name="app/bad", SecretString="not-json")
    with pytest.raises(ValueError, match="not valid JSON"):
        load_config_from_secret("app/bad", region_name=REGION)


# ---------------------------------------------------------------------------
# load_app_config
# ---------------------------------------------------------------------------


def test_load_app_config_from_ssm_only(ssm_client):
    ssm_client.put_parameter(Name="/cfg/key", Value="ssm-val", Type="String")
    cfg = load_app_config(ssm_prefix="/cfg", region_name=REGION)
    assert cfg["key"] == "ssm-val"


def test_load_app_config_from_secrets_only(secrets_client):
    secrets_client.create_secret(
        Name="my/app/secret",
        SecretString=json.dumps({"username": "alice"}),
    )
    cfg = load_app_config(secret_names=["my/app/secret"], region_name=REGION)
    assert cfg["username"] == "alice"


def test_load_app_config_merged(ssm_client, secrets_client):
    ssm_client.put_parameter(Name="/merge/host", Value="prod-host", Type="String")
    secrets_client.create_secret(
        Name="merge/secret",
        SecretString=json.dumps({"password": "s3cr3t"}),
    )
    cfg = load_app_config(
        ssm_prefix="/merge",
        secret_names=["merge/secret"],
        region_name=REGION,
    )
    assert cfg["host"] == "prod-host"
    assert cfg["password"] == "s3cr3t"


def test_load_app_config_ssm_overrides_secret(ssm_client, secrets_client):
    """SSM should take precedence over secrets for duplicate keys."""
    ssm_client.put_parameter(Name="/over/host", Value="ssm-host", Type="String")
    secrets_client.create_secret(
        Name="over/secret",
        SecretString=json.dumps({"host": "secret-host"}),
    )
    cfg = load_app_config(
        ssm_prefix="/over",
        secret_names=["over/secret"],
        region_name=REGION,
    )
    assert cfg["host"] == "ssm-host"


def test_load_app_config_empty_returns_empty():
    cfg = load_app_config(region_name=REGION)
    assert "anything" not in cfg


# ---------------------------------------------------------------------------
# resolve_config
# ---------------------------------------------------------------------------


def test_resolve_config_plain_strings():
    result = resolve_config({"key": "plain-value"}, region_name=REGION)
    assert result["key"] == "plain-value"


def test_resolve_config_nested_dict(ssm_client):
    ssm_client.put_parameter(Name="/r/host", Value="resolved-host", Type="String")
    result = resolve_config(
        {"db": {"host": "${ssm:/r/host}"}},
        region_name=REGION,
    )
    assert result["db"]["host"] == "resolved-host"


def test_resolve_config_list_values(ssm_client):
    ssm_client.put_parameter(Name="/r/item", Value="resolved-item", Type="String")
    result = resolve_config(
        {"items": ["${ssm:/r/item}", "plain"]},
        region_name=REGION,
    )
    assert result["items"][0] == "resolved-item"
    assert result["items"][1] == "plain"


def test_resolve_config_non_string_passthrough():
    result = resolve_config({"count": 42, "flag": True, "data": None})
    assert result["count"] == 42
    assert result["flag"] is True
    assert result["data"] is None


# ---------------------------------------------------------------------------
# get_db_credentials
# ---------------------------------------------------------------------------


def test_get_db_credentials_valid(secrets_client):
    secrets_client.create_secret(
        Name="db/creds",
        SecretString=json.dumps({
            "username": "admin",
            "password": "secret",
            "host": "db.example.com",
        }),
    )
    creds = get_db_credentials("db/creds", region_name=REGION)
    assert creds["username"] == "admin"
    assert creds["password"] == "secret"
    assert creds["host"] == "db.example.com"


def test_get_db_credentials_missing_username(secrets_client):
    secrets_client.create_secret(
        Name="db/bad",
        SecretString=json.dumps({"password": "secret"}),
    )
    with pytest.raises(ValueError, match="missing required keys"):
        get_db_credentials("db/bad", region_name=REGION)


def test_get_db_credentials_missing_password(secrets_client):
    secrets_client.create_secret(
        Name="db/nopass",
        SecretString=json.dumps({"username": "admin"}),
    )
    with pytest.raises(ValueError, match="missing required keys"):
        get_db_credentials("db/nopass", region_name=REGION)


# ---------------------------------------------------------------------------
# get_ssm_parameter_map
# ---------------------------------------------------------------------------


def test_get_ssm_parameter_map_basic(ssm_client):
    ssm_client.put_parameter(Name="/m/a", Value="va", Type="String")
    ssm_client.put_parameter(Name="/m/b", Value="vb", Type="String")
    result = get_ssm_parameter_map(["/m/a", "/m/b"], region_name=REGION)
    assert result["/m/a"] == "va"
    assert result["/m/b"] == "vb"


def test_get_ssm_parameter_map_chunking(ssm_client):
    """More than 10 parameters should be chunked into batches of 10."""
    names = []
    for i in range(15):
        name = f"/chunk/{i}"
        ssm_client.put_parameter(Name=name, Value=str(i), Type="String")
        names.append(name)
    result = get_ssm_parameter_map(names, region_name=REGION)
    assert len(result) == 15
    assert result["/chunk/0"] == "0"
    assert result["/chunk/14"] == "14"


def test_get_ssm_parameter_map_empty():
    result = get_ssm_parameter_map([], region_name=REGION)
    assert result == {}


# ---------------------------------------------------------------------------
# appconfig_feature_flag_loader
# ---------------------------------------------------------------------------

import time as _time_mod
from unittest.mock import MagicMock

from botocore.exceptions import ClientError

import aws_util.config_loader as _config_mod
from aws_util.config_loader import (
    FeatureFlagResult,
    appconfig_feature_flag_loader,
    ParameterReplicateResult,
    cross_region_parameter_replicator,
)


def _client_error(code: str, message: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": message}}, "Op")


class TestAppconfigFeatureFlagLoader:
    def _factory(self, appconfig: MagicMock, cw: MagicMock | None = None):
        def _get_client(service: str, *a, **kw):
            if service == "appconfigdata":
                return appconfig
            if service == "cloudwatch":
                return cw or MagicMock()
            return MagicMock()
        return _get_client

    def test_success_cache_miss(self, monkeypatch):
        # Clear module-level cache
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok-1"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": b'{"feature_x": true}',
            "VersionLabel": "v1",
        }
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        result = appconfig_feature_flag_loader(
            application_id="app-1",
            environment_id="env-1",
            configuration_profile_id="prof-1",
        )
        assert isinstance(result, FeatureFlagResult)
        assert result.flags == {"feature_x": True}
        assert result.version == "v1"
        assert result.cached is False

    def test_cache_hit(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        # Seed cache
        key = "app-1/env-1/prof-1"
        _config_mod._FLAG_CACHE[key] = ({"cached_flag": True}, "v2", _time_mod.time())
        appconfig = MagicMock()
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        result = appconfig_feature_flag_loader(
            application_id="app-1",
            environment_id="env-1",
            configuration_profile_id="prof-1",
        )
        assert result.cached is True
        assert result.flags == {"cached_flag": True}
        assert result.version == "v2"
        appconfig.start_configuration_session.assert_not_called()

    def test_start_session_error(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.side_effect = _client_error(
            "BadRequestException"
        )
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        with pytest.raises(RuntimeError, match="Failed to start AppConfig session"):
            appconfig_feature_flag_loader("a", "e", "p")

    def test_get_latest_configuration_error(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.side_effect = _client_error(
            "InternalServerException"
        )
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        with pytest.raises(RuntimeError, match="Failed to get AppConfig configuration"):
            appconfig_feature_flag_loader("a", "e", "p")

    def test_invalid_json_returns_raw(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": b"not-json",
            "VersionLabel": "v3",
        }
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        result = appconfig_feature_flag_loader("a", "e", "p")
        assert result.flags == {"raw": "not-json"}

    def test_empty_configuration(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": b"   ",
            "VersionLabel": "v4",
        }
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        result = appconfig_feature_flag_loader("a", "e", "p")
        assert result.flags == {}

    def test_string_configuration(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": '{"flag": 1}',
            "VersionLabel": "v5",
        }
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig))
        result = appconfig_feature_flag_loader("a", "e", "p")
        assert result.flags == {"flag": 1}

    def test_with_metric_namespace_miss(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": b'{"k": 1}',
            "VersionLabel": "v6",
        }
        cw = MagicMock()
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig, cw))
        result = appconfig_feature_flag_loader(
            "a", "e", "p", metric_namespace="MyApp/Flags"
        )
        assert result.cached is False
        cw.put_metric_data.assert_called_once()
        call_args = cw.put_metric_data.call_args
        metric_data = call_args[1]["MetricData"][0]
        assert metric_data["MetricName"] == "FeatureFlagCacheMiss"

    def test_with_metric_namespace_hit(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        key = "a2/e2/p2"
        _config_mod._FLAG_CACHE[key] = ({"f": 1}, "v7", _time_mod.time())
        appconfig = MagicMock()
        cw = MagicMock()
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig, cw))
        result = appconfig_feature_flag_loader(
            "a2", "e2", "p2", metric_namespace="MyApp/Flags"
        )
        assert result.cached is True
        call_args = cw.put_metric_data.call_args
        metric_data = call_args[1]["MetricData"][0]
        assert metric_data["MetricName"] == "FeatureFlagCacheHit"

    def test_metric_publish_failure_is_non_fatal(self, monkeypatch):
        _config_mod._FLAG_CACHE.clear()
        appconfig = MagicMock()
        appconfig.start_configuration_session.return_value = {
            "InitialConfigurationToken": "tok"
        }
        appconfig.get_latest_configuration.return_value = {
            "Configuration": b'{"k": 1}',
            "VersionLabel": "v8",
        }
        cw = MagicMock()
        cw.put_metric_data.side_effect = _client_error("InternalError")
        monkeypatch.setattr(_config_mod, "get_client", self._factory(appconfig, cw))
        # Should NOT raise
        result = appconfig_feature_flag_loader(
            "a", "e", "p", metric_namespace="MyApp/Flags"
        )
        assert result.flags == {"k": 1}


# ---------------------------------------------------------------------------
# cross_region_parameter_replicator
# ---------------------------------------------------------------------------


class TestCrossRegionParameterReplicator:
    def test_success(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.return_value = {
            "Parameter": {"Value": "val1", "Type": "String"}
        }
        tgt_ssm = MagicMock()

        def _get_client(service, region=None):
            if service == "ssm":
                if region == "us-east-1":
                    return src_ssm
                return tgt_ssm
            if service == "logs":
                return MagicMock()
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        result = cross_region_parameter_replicator(
            parameter_names=["/app/key"],
            source_region="us-east-1",
            target_regions=["eu-west-1", "ap-southeast-1"],
        )
        assert isinstance(result, ParameterReplicateResult)
        assert result.parameters_replicated == 2
        assert result.target_regions == ["eu-west-1", "ap-southeast-1"]
        assert result.failures == 0

    def test_source_read_failure(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.side_effect = _client_error("ParameterNotFound")

        def _get_client(service, region=None):
            if service == "ssm":
                return src_ssm
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        result = cross_region_parameter_replicator(
            parameter_names=["/app/bad"],
            source_region="us-east-1",
            target_regions=["eu-west-1"],
        )
        assert result.parameters_replicated == 0
        assert result.failures == 1

    def test_target_write_failure(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.return_value = {
            "Parameter": {"Value": "val", "Type": "String"}
        }
        tgt_ssm = MagicMock()
        tgt_ssm.put_parameter.side_effect = _client_error("AccessDenied")

        def _get_client(service, region=None):
            if service == "ssm":
                if region == "us-east-1":
                    return src_ssm
                return tgt_ssm
            if service == "logs":
                return MagicMock()
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        result = cross_region_parameter_replicator(
            parameter_names=["/app/key"],
            source_region="us-east-1",
            target_regions=["eu-west-1"],
        )
        assert result.parameters_replicated == 0
        assert result.failures == 1

    def test_with_log_group(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.return_value = {
            "Parameter": {"Value": "v", "Type": "String"}
        }
        tgt_ssm = MagicMock()
        logs = MagicMock()

        def _get_client(service, region=None):
            if service == "ssm":
                if region == "us-east-1":
                    return src_ssm
                return tgt_ssm
            if service == "logs":
                return logs
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        result = cross_region_parameter_replicator(
            parameter_names=["/app/key"],
            source_region="us-east-1",
            target_regions=["eu-west-1"],
            log_group_name="/replication/logs",
        )
        assert result.parameters_replicated == 1
        logs.put_log_events.assert_called_once()

    def test_log_write_failure_is_non_fatal(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.return_value = {
            "Parameter": {"Value": "v", "Type": "String"}
        }
        tgt_ssm = MagicMock()
        logs = MagicMock()
        logs.put_log_events.side_effect = _client_error("InvalidSequenceTokenException")

        def _get_client(service, region=None):
            if service == "ssm":
                if region == "us-east-1":
                    return src_ssm
                return tgt_ssm
            if service == "logs":
                return logs
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        # Should not raise
        result = cross_region_parameter_replicator(
            parameter_names=["/app/key"],
            source_region="us-east-1",
            target_regions=["eu-west-1"],
            log_group_name="/logs",
        )
        assert result.parameters_replicated == 1

    def test_no_log_group(self, monkeypatch):
        src_ssm = MagicMock()
        src_ssm.get_parameter.return_value = {
            "Parameter": {"Value": "v", "Type": "String"}
        }
        tgt_ssm = MagicMock()

        def _get_client(service, region=None):
            if service == "ssm":
                if region == "us-east-1":
                    return src_ssm
                return tgt_ssm
            return MagicMock()

        monkeypatch.setattr(_config_mod, "get_client", _get_client)
        result = cross_region_parameter_replicator(
            parameter_names=["/app/k1", "/app/k2"],
            source_region="us-east-1",
            target_regions=["eu-west-1"],
        )
        assert result.parameters_replicated == 2
        assert result.failures == 0
