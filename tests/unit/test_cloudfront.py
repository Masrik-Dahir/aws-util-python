"""Tests for aws_util.cloudfront module."""
from __future__ import annotations

import time

import boto3
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.cloudfront as cf_mod
from aws_util.cloudfront import (
    CachePolicyResult,
    DistributionResult,
    InvalidationResult,
    OriginAccessControlResult,
    create_distribution,
    create_invalidation,
    create_origin_access_control,
    delete_distribution,
    delete_origin_access_control,
    get_distribution,
    get_invalidation,
    get_origin_access_control,
    invalidate_and_wait,
    list_distributions,
    list_invalidations,
    list_origin_access_controls,
    update_distribution,
    wait_for_distribution,
    associate_alias,
    associate_distribution_tenant_web_acl,
    associate_distribution_web_acl,
    copy_distribution,
    create_anycast_ip_list,
    create_cache_policy,
    create_cloud_front_origin_access_identity,
    create_connection_group,
    create_continuous_deployment_policy,
    create_distribution_tenant,
    create_distribution_with_tags,
    create_field_level_encryption_config,
    create_field_level_encryption_profile,
    create_function,
    create_invalidation_for_distribution_tenant,
    create_key_group,
    create_key_value_store,
    create_monitoring_subscription,
    create_origin_request_policy,
    create_public_key,
    create_realtime_log_config,
    create_response_headers_policy,
    create_streaming_distribution,
    create_streaming_distribution_with_tags,
    create_vpc_origin,
    delete_anycast_ip_list,
    delete_cache_policy,
    delete_cloud_front_origin_access_identity,
    delete_connection_group,
    delete_continuous_deployment_policy,
    delete_distribution_tenant,
    delete_field_level_encryption_config,
    delete_field_level_encryption_profile,
    delete_function,
    delete_key_group,
    delete_key_value_store,
    delete_monitoring_subscription,
    delete_origin_request_policy,
    delete_public_key,
    delete_realtime_log_config,
    delete_resource_policy,
    delete_response_headers_policy,
    delete_streaming_distribution,
    delete_vpc_origin,
    describe_function,
    describe_key_value_store,
    disassociate_distribution_tenant_web_acl,
    disassociate_distribution_web_acl,
    get_anycast_ip_list,
    get_cache_policy,
    get_cache_policy_config,
    get_cloud_front_origin_access_identity,
    get_cloud_front_origin_access_identity_config,
    get_connection_group,
    get_connection_group_by_routing_endpoint,
    get_continuous_deployment_policy,
    get_continuous_deployment_policy_config,
    get_distribution_config,
    get_distribution_tenant,
    get_distribution_tenant_by_domain,
    get_field_level_encryption,
    get_field_level_encryption_config,
    get_field_level_encryption_profile,
    get_field_level_encryption_profile_config,
    get_function,
    get_invalidation_for_distribution_tenant,
    get_key_group,
    get_key_group_config,
    get_managed_certificate_details,
    get_monitoring_subscription,
    get_origin_access_control_config,
    get_origin_request_policy,
    get_origin_request_policy_config,
    get_public_key,
    get_public_key_config,
    get_realtime_log_config,
    get_resource_policy,
    get_response_headers_policy,
    get_response_headers_policy_config,
    get_streaming_distribution,
    get_streaming_distribution_config,
    get_vpc_origin,
    list_anycast_ip_lists,
    list_cache_policies,
    list_cloud_front_origin_access_identities,
    list_conflicting_aliases,
    list_connection_groups,
    list_continuous_deployment_policies,
    list_distribution_tenants,
    list_distribution_tenants_by_customization,
    list_distributions_by_anycast_ip_list_id,
    list_distributions_by_cache_policy_id,
    list_distributions_by_connection_mode,
    list_distributions_by_key_group,
    list_distributions_by_origin_request_policy_id,
    list_distributions_by_owned_resource,
    list_distributions_by_realtime_log_config,
    list_distributions_by_response_headers_policy_id,
    list_distributions_by_vpc_origin_id,
    list_distributions_by_web_acl_id,
    list_domain_conflicts,
    list_field_level_encryption_configs,
    list_field_level_encryption_profiles,
    list_functions,
    list_invalidations_for_distribution_tenant,
    list_key_groups,
    list_key_value_stores,
    list_origin_request_policies,
    list_public_keys,
    list_realtime_log_configs,
    list_response_headers_policies,
    list_streaming_distributions,
    list_tags_for_resource,
    list_vpc_origins,
    publish_function,
    put_resource_policy,
    run_function,
    tag_resource,
    untag_resource,
    update_anycast_ip_list,
    update_cache_policy,
    update_cloud_front_origin_access_identity,
    update_connection_group,
    update_continuous_deployment_policy,
    update_distribution_tenant,
    update_distribution_with_staging_config,
    update_domain_association,
    update_field_level_encryption_config,
    update_field_level_encryption_profile,
    update_function,
    update_key_group,
    update_key_value_store,
    update_origin_access_control,
    update_origin_request_policy,
    update_public_key,
    update_realtime_log_config,
    update_response_headers_policy,
    update_streaming_distribution,
    update_vpc_origin,
    verify_dns_configuration,
)

REGION = "us-east-1"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_ORIGINS = [
    {
        "DomainName": "mybucket.s3.amazonaws.com",
        "Id": "myS3Origin",
        "S3OriginConfig": {"OriginAccessIdentity": ""},
    }
]

SAMPLE_CACHE_BEHAVIOR = {
    "TargetOriginId": "myS3Origin",
    "ViewerProtocolPolicy": "redirect-to-https",
    "ForwardedValues": {
        "QueryString": False,
        "Cookies": {"Forward": "none"},
    },
    "TrustedSigners": {"Enabled": False, "Quantity": 0},
    "MinTTL": 0,
}


def _create_dist(region_name: str = REGION, **kwargs):
    """Helper to create a distribution via the module function."""
    return create_distribution(
        origins=kwargs.pop("origins", SAMPLE_ORIGINS),
        default_cache_behavior=kwargs.pop(
            "default_cache_behavior", SAMPLE_CACHE_BEHAVIOR
        ),
        region_name=region_name,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_distribution_result_model():
    result = DistributionResult(
        id="ABC123",
        arn="arn:aws:cloudfront::123456:distribution/ABC123",
        domain_name="d1234.cloudfront.net",
        status="Deployed",
        origins=[{"DomainName": "example.com", "Id": "origin1"}],
        enabled=True,
        comment="test",
        etag="ETAG1",
    )
    assert result.id == "ABC123"
    assert result.enabled is True
    assert result.etag == "ETAG1"
    assert len(result.origins) == 1


def test_invalidation_result_model():
    result = InvalidationResult(
        id="INV123",
        distribution_id="DIST1",
        status="Completed",
        paths=["/*"],
    )
    assert result.id == "INV123"
    assert result.distribution_id == "DIST1"
    assert result.paths == ["/*"]


def test_origin_access_control_result_model():
    result = OriginAccessControlResult(
        id="OAC1",
        name="my-oac",
        signing_protocol="sigv4",
        signing_behavior="always",
        origin_type="s3",
    )
    assert result.id == "OAC1"
    assert result.name == "my-oac"


def test_cache_policy_result_model():
    result = CachePolicyResult(
        id="CP1",
        name="my-policy",
        comment="test",
        min_ttl=0,
        max_ttl=86400,
        default_ttl=3600,
    )
    assert result.id == "CP1"
    assert result.default_ttl == 3600


# ---------------------------------------------------------------------------
# create_distribution
# ---------------------------------------------------------------------------


def test_create_distribution_success():
    result = _create_dist(comment="test-dist")
    assert isinstance(result, DistributionResult)
    assert result.id
    assert result.arn
    assert result.domain_name
    assert result.status
    assert result.comment == "test-dist"


def test_create_distribution_with_caller_reference():
    result = _create_dist(caller_reference="my-unique-ref")
    assert result.id


def test_create_distribution_disabled():
    result = _create_dist(enabled=False)
    assert result.id


def test_create_distribution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_distribution.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "CreateDistribution",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_distribution failed"):
        _create_dist()


# ---------------------------------------------------------------------------
# get_distribution
# ---------------------------------------------------------------------------


def test_get_distribution_success():
    created = _create_dist()
    result = get_distribution(created.id, region_name=REGION)
    assert result.id == created.id
    assert result.etag is not None


def test_get_distribution_not_found(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution.side_effect = ClientError(
        {"Error": {"Code": "NoSuchDistribution", "Message": "not found"}},
        "GetDistribution",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_distribution failed"):
        get_distribution("NONEXISTENT", region_name=REGION)


# ---------------------------------------------------------------------------
# list_distributions
# ---------------------------------------------------------------------------


def test_list_distributions_empty():
    result = list_distributions(region_name=REGION)
    assert isinstance(result, list)
    assert len(result) == 0


def test_list_distributions_with_items():
    _create_dist()
    result = list_distributions(region_name=REGION)
    assert len(result) >= 1
    assert isinstance(result[0], DistributionResult)


def test_list_distributions_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListDistributions",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_distributions failed"):
        list_distributions(region_name=REGION)


# ---------------------------------------------------------------------------
# update_distribution
# ---------------------------------------------------------------------------


def test_update_distribution_success():
    created = _create_dist(comment="original")
    fetched = get_distribution(created.id, region_name=REGION)
    assert fetched.etag is not None

    # Get the full config from the raw client to use for update
    client = boto3.client("cloudfront", region_name=REGION)
    raw = client.get_distribution(Id=created.id)
    config = raw["Distribution"]["DistributionConfig"]
    config["Comment"] = "updated"

    result = update_distribution(
        created.id,
        distribution_config=config,
        if_match=fetched.etag,
        region_name=REGION,
    )
    assert result.comment == "updated"


def test_update_distribution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_distribution.side_effect = ClientError(
        {"Error": {"Code": "InvalidIfMatchVersion", "Message": "bad etag"}},
        "UpdateDistribution",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="update_distribution failed"):
        update_distribution(
            "DIST1",
            distribution_config={},
            if_match="bad-etag",
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# delete_distribution
# ---------------------------------------------------------------------------


def test_delete_distribution_success():
    created = _create_dist(enabled=False)
    fetched = get_distribution(created.id, region_name=REGION)
    delete_distribution(
        created.id, if_match=fetched.etag, region_name=REGION
    )
    # Verify deleted by listing
    dists = list_distributions(region_name=REGION)
    assert not any(d.id == created.id for d in dists)


def test_delete_distribution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_distribution.side_effect = ClientError(
        {"Error": {"Code": "NoSuchDistribution", "Message": "not found"}},
        "DeleteDistribution",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_distribution failed"):
        delete_distribution(
            "NONEXISTENT", if_match="etag", region_name=REGION
        )


# ---------------------------------------------------------------------------
# create_invalidation
# ---------------------------------------------------------------------------


def test_create_invalidation_success():
    created = _create_dist()
    result = create_invalidation(
        created.id, paths=["/*"], region_name=REGION
    )
    assert isinstance(result, InvalidationResult)
    assert result.id
    assert result.distribution_id == created.id
    assert result.paths == ["/*"]


def test_create_invalidation_with_caller_reference():
    created = _create_dist()
    result = create_invalidation(
        created.id,
        paths=["/index.html"],
        caller_reference="my-inv-ref",
        region_name=REGION,
    )
    assert result.id


def test_create_invalidation_multiple_paths():
    created = _create_dist()
    result = create_invalidation(
        created.id,
        paths=["/css/*", "/js/*", "/images/*"],
        region_name=REGION,
    )
    assert len(result.paths) == 3


def test_create_invalidation_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_invalidation.side_effect = ClientError(
        {"Error": {"Code": "NoSuchDistribution", "Message": "not found"}},
        "CreateInvalidation",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_invalidation failed"):
        create_invalidation(
            "NONEXISTENT", paths=["/*"], region_name=REGION
        )


# ---------------------------------------------------------------------------
# get_invalidation
# ---------------------------------------------------------------------------


def test_get_invalidation_success():
    created = _create_dist()
    inv = create_invalidation(
        created.id, paths=["/*"], region_name=REGION
    )
    result = get_invalidation(
        created.id, inv.id, region_name=REGION
    )
    assert result.id == inv.id
    assert result.distribution_id == created.id


def test_get_invalidation_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invalidation.side_effect = ClientError(
        {"Error": {"Code": "NoSuchInvalidation", "Message": "not found"}},
        "GetInvalidation",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_invalidation failed"):
        get_invalidation("DIST1", "INV1", region_name=REGION)


# ---------------------------------------------------------------------------
# list_invalidations
# ---------------------------------------------------------------------------


def test_list_invalidations_empty():
    created = _create_dist()
    result = list_invalidations(created.id, region_name=REGION)
    assert isinstance(result, list)
    assert len(result) == 0


def test_list_invalidations_with_items():
    created = _create_dist()
    create_invalidation(created.id, paths=["/*"], region_name=REGION)
    result = list_invalidations(created.id, region_name=REGION)
    assert len(result) >= 1


def test_list_invalidations_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListInvalidations",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_invalidations failed"):
        list_invalidations("DIST1", region_name=REGION)


# ---------------------------------------------------------------------------
# create_origin_access_control
# ---------------------------------------------------------------------------


def test_create_origin_access_control_success():
    result = create_origin_access_control(
        "test-oac", region_name=REGION
    )
    assert isinstance(result, OriginAccessControlResult)
    assert result.id
    assert result.name == "test-oac"
    assert result.signing_protocol == "sigv4"
    assert result.signing_behavior == "always"
    assert result.origin_type == "s3"


def test_create_origin_access_control_custom_params():
    result = create_origin_access_control(
        "custom-oac",
        signing_protocol="sigv4",
        signing_behavior="always",
        origin_type="s3",
        description="my description",
        region_name=REGION,
    )
    assert result.name == "custom-oac"


def test_create_origin_access_control_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_origin_access_control.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "CreateOriginAccessControl",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_origin_access_control failed"):
        create_origin_access_control("bad-oac", region_name=REGION)


# ---------------------------------------------------------------------------
# get_origin_access_control
# ---------------------------------------------------------------------------


def test_get_origin_access_control_success():
    created = create_origin_access_control(
        "test-get-oac", region_name=REGION
    )
    result = get_origin_access_control(created.id, region_name=REGION)
    assert result.id == created.id
    assert result.name == "test-get-oac"


def test_get_origin_access_control_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_access_control.side_effect = ClientError(
        {"Error": {"Code": "NoSuchOriginAccessControl", "Message": "not found"}},
        "GetOriginAccessControl",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_origin_access_control failed"):
        get_origin_access_control("NONEXISTENT", region_name=REGION)


# ---------------------------------------------------------------------------
# list_origin_access_controls
# ---------------------------------------------------------------------------


def test_list_origin_access_controls_empty():
    result = list_origin_access_controls(region_name=REGION)
    assert isinstance(result, list)
    assert len(result) == 0


def test_list_origin_access_controls_with_items():
    create_origin_access_control("list-oac", region_name=REGION)
    result = list_origin_access_controls(region_name=REGION)
    assert len(result) >= 1


def test_list_origin_access_controls_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_origin_access_controls.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListOriginAccessControls",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_origin_access_controls failed"):
        list_origin_access_controls(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_origin_access_control
# ---------------------------------------------------------------------------


def test_delete_origin_access_control_success():
    created = create_origin_access_control(
        "del-oac", region_name=REGION
    )
    # Get ETag
    client = boto3.client("cloudfront", region_name=REGION)
    resp = client.get_origin_access_control(Id=created.id)
    etag = resp["ETag"]
    delete_origin_access_control(
        created.id, if_match=etag, region_name=REGION
    )
    # Verify deleted
    result = list_origin_access_controls(region_name=REGION)
    assert not any(o.id == created.id for o in result)


def test_delete_origin_access_control_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_origin_access_control.side_effect = ClientError(
        {"Error": {"Code": "NoSuchOriginAccessControl", "Message": "not found"}},
        "DeleteOriginAccessControl",
    )
    monkeypatch.setattr(cf_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(
        RuntimeError, match="delete_origin_access_control failed"
    ):
        delete_origin_access_control(
            "NONEXISTENT", if_match="etag", region_name=REGION
        )


# ---------------------------------------------------------------------------
# wait_for_distribution
# ---------------------------------------------------------------------------


def test_wait_for_distribution_already_deployed():
    created = _create_dist()
    # moto returns Deployed immediately
    result = wait_for_distribution(
        created.id,
        target_status="Deployed",
        timeout=5,
        poll_interval=0.01,
        region_name=REGION,
    )
    assert result.status == "Deployed"


def test_wait_for_distribution_timeout(monkeypatch):
    # Simulate a distribution that never reaches target status
    in_progress = DistributionResult(
        id="DIST1",
        arn="arn:...",
        domain_name="d1.cloudfront.net",
        status="InProgress",
    )
    monkeypatch.setattr(
        cf_mod,
        "get_distribution",
        lambda dist_id, region_name=None: in_progress,
    )
    monkeypatch.setattr(time, "sleep", lambda s: None)

    with pytest.raises(RuntimeError, match="did not reach"):
        wait_for_distribution(
            "DIST1",
            target_status="Deployed",
            timeout=0.0,
            poll_interval=0.0,
            region_name=REGION,
        )


def test_wait_for_distribution_polls_then_deployed(monkeypatch):
    in_progress = DistributionResult(
        id="DIST1",
        arn="arn:...",
        domain_name="d1.cloudfront.net",
        status="InProgress",
    )
    deployed = DistributionResult(
        id="DIST1",
        arn="arn:...",
        domain_name="d1.cloudfront.net",
        status="Deployed",
    )
    call_count = {"n": 0}

    def fake_get(dist_id, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return in_progress
        return deployed

    monkeypatch.setattr(cf_mod, "get_distribution", fake_get)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    result = wait_for_distribution(
        "DIST1",
        timeout=10.0,
        poll_interval=0.001,
        region_name=REGION,
    )
    assert result.status == "Deployed"


# ---------------------------------------------------------------------------
# invalidate_and_wait
# ---------------------------------------------------------------------------


def test_invalidate_and_wait_success():
    created = _create_dist()
    # moto returns Completed immediately
    result = invalidate_and_wait(
        created.id,
        paths=["/*"],
        timeout=5,
        poll_interval=0.01,
        region_name=REGION,
    )
    assert result.status.upper() == "COMPLETED"


def test_invalidate_and_wait_timeout(monkeypatch):
    inv = InvalidationResult(
        id="INV1",
        distribution_id="DIST1",
        status="InProgress",
        paths=["/*"],
    )
    monkeypatch.setattr(
        cf_mod,
        "create_invalidation",
        lambda dist_id, paths, caller_reference=None, region_name=None: inv,
    )
    monkeypatch.setattr(
        cf_mod,
        "get_invalidation",
        lambda dist_id, inv_id, region_name=None: inv,
    )
    monkeypatch.setattr(time, "sleep", lambda s: None)

    with pytest.raises(RuntimeError, match="did not complete"):
        invalidate_and_wait(
            "DIST1",
            paths=["/*"],
            timeout=0.0,
            poll_interval=0.0,
            region_name=REGION,
        )


def test_invalidate_and_wait_polls_then_completed(monkeypatch):
    in_progress = InvalidationResult(
        id="INV1",
        distribution_id="DIST1",
        status="InProgress",
        paths=["/*"],
    )
    completed = InvalidationResult(
        id="INV1",
        distribution_id="DIST1",
        status="Completed",
        paths=["/*"],
    )
    monkeypatch.setattr(
        cf_mod,
        "create_invalidation",
        lambda dist_id, paths, caller_reference=None, region_name=None: in_progress,
    )
    call_count = {"n": 0}

    def fake_get_inv(dist_id, inv_id, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return in_progress
        return completed

    monkeypatch.setattr(cf_mod, "get_invalidation", fake_get_inv)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    result = invalidate_and_wait(
        "DIST1",
        paths=["/*"],
        timeout=10.0,
        poll_interval=0.001,
        region_name=REGION,
    )
    assert result.status == "Completed"


# ---------------------------------------------------------------------------
# _parse helpers edge cases
# ---------------------------------------------------------------------------


def test_parse_distribution_origins_as_list():
    """Test _parse_distribution with origins as a plain list."""
    dist = {
        "Id": "D1",
        "ARN": "arn:...",
        "DomainName": "d1.cloudfront.net",
        "Status": "Deployed",
        "LastModifiedTime": None,
        "Origins": [{"DomainName": "example.com", "Id": "o1"}],
        "Enabled": True,
        "Comment": "",
    }
    result = cf_mod._parse_distribution(dist)
    assert len(result.origins) == 1


def test_parse_invalidation_no_batch():
    """Test _parse_invalidation with no InvalidationBatch."""
    inv = {
        "Id": "INV1",
        "Status": "Completed",
        "CreateTime": None,
    }
    result = cf_mod._parse_invalidation(inv, "DIST1")
    assert result.paths == []
    assert result.create_time is None


# ---------------------------------------------------------------------------
# __all__ exports
# ---------------------------------------------------------------------------


def test_all_exports():
    assert "DistributionResult" in cf_mod.__all__
    assert "InvalidationResult" in cf_mod.__all__
    assert "OriginAccessControlResult" in cf_mod.__all__
    assert "CachePolicyResult" in cf_mod.__all__
    assert "create_distribution" in cf_mod.__all__
    assert "get_distribution" in cf_mod.__all__
    assert "list_distributions" in cf_mod.__all__
    assert "update_distribution" in cf_mod.__all__
    assert "delete_distribution" in cf_mod.__all__
    assert "create_invalidation" in cf_mod.__all__
    assert "get_invalidation" in cf_mod.__all__
    assert "list_invalidations" in cf_mod.__all__
    assert "create_origin_access_control" in cf_mod.__all__
    assert "get_origin_access_control" in cf_mod.__all__
    assert "list_origin_access_controls" in cf_mod.__all__
    assert "delete_origin_access_control" in cf_mod.__all__
    assert "wait_for_distribution" in cf_mod.__all__
    assert "invalidate_and_wait" in cf_mod.__all__


def test_associate_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_alias.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    associate_alias("test-target_distribution_id", "test-alias", region_name=REGION)
    mock_client.associate_alias.assert_called_once()


def test_associate_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_alias",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate alias"):
        associate_alias("test-target_distribution_id", "test-alias", region_name=REGION)


def test_associate_distribution_tenant_web_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_distribution_tenant_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", region_name=REGION)
    mock_client.associate_distribution_tenant_web_acl.assert_called_once()


def test_associate_distribution_tenant_web_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_distribution_tenant_web_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_distribution_tenant_web_acl",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate distribution tenant web acl"):
        associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", region_name=REGION)


def test_associate_distribution_web_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_distribution_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    associate_distribution_web_acl("test-id", "test-web_acl_arn", region_name=REGION)
    mock_client.associate_distribution_web_acl.assert_called_once()


def test_associate_distribution_web_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_distribution_web_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_distribution_web_acl",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate distribution web acl"):
        associate_distribution_web_acl("test-id", "test-web_acl_arn", region_name=REGION)


def test_copy_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    copy_distribution("test-primary_distribution_id", "test-caller_reference", region_name=REGION)
    mock_client.copy_distribution.assert_called_once()


def test_copy_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_distribution",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy distribution"):
        copy_distribution("test-primary_distribution_id", "test-caller_reference", region_name=REGION)


def test_create_anycast_ip_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_anycast_ip_list("test-name", 1, region_name=REGION)
    mock_client.create_anycast_ip_list.assert_called_once()


def test_create_anycast_ip_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_anycast_ip_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_anycast_ip_list",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create anycast ip list"):
        create_anycast_ip_list("test-name", 1, region_name=REGION)


def test_create_cache_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_cache_policy({}, region_name=REGION)
    mock_client.create_cache_policy.assert_called_once()


def test_create_cache_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cache_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cache policy"):
        create_cache_policy({}, region_name=REGION)


def test_create_cloud_front_origin_access_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_cloud_front_origin_access_identity({}, region_name=REGION)
    mock_client.create_cloud_front_origin_access_identity.assert_called_once()


def test_create_cloud_front_origin_access_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cloud_front_origin_access_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cloud_front_origin_access_identity",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cloud front origin access identity"):
        create_cloud_front_origin_access_identity({}, region_name=REGION)


def test_create_connection_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_connection_group("test-name", region_name=REGION)
    mock_client.create_connection_group.assert_called_once()


def test_create_connection_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_connection_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create connection group"):
        create_connection_group("test-name", region_name=REGION)


def test_create_continuous_deployment_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_continuous_deployment_policy({}, region_name=REGION)
    mock_client.create_continuous_deployment_policy.assert_called_once()


def test_create_continuous_deployment_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_continuous_deployment_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_continuous_deployment_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create continuous deployment policy"):
        create_continuous_deployment_policy({}, region_name=REGION)


def test_create_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_distribution_tenant("test-distribution_id", "test-name", [], region_name=REGION)
    mock_client.create_distribution_tenant.assert_called_once()


def test_create_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create distribution tenant"):
        create_distribution_tenant("test-distribution_id", "test-name", [], region_name=REGION)


def test_create_distribution_with_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_distribution_with_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_distribution_with_tags({}, region_name=REGION)
    mock_client.create_distribution_with_tags.assert_called_once()


def test_create_distribution_with_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_distribution_with_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_distribution_with_tags",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create distribution with tags"):
        create_distribution_with_tags({}, region_name=REGION)


def test_create_field_level_encryption_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_field_level_encryption_config({}, region_name=REGION)
    mock_client.create_field_level_encryption_config.assert_called_once()


def test_create_field_level_encryption_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_field_level_encryption_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_field_level_encryption_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create field level encryption config"):
        create_field_level_encryption_config({}, region_name=REGION)


def test_create_field_level_encryption_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_field_level_encryption_profile({}, region_name=REGION)
    mock_client.create_field_level_encryption_profile.assert_called_once()


def test_create_field_level_encryption_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_field_level_encryption_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_field_level_encryption_profile",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create field level encryption profile"):
        create_field_level_encryption_profile({}, region_name=REGION)


def test_create_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_function("test-name", {}, "test-function_code", region_name=REGION)
    mock_client.create_function.assert_called_once()


def test_create_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create function"):
        create_function("test-name", {}, "test-function_code", region_name=REGION)


def test_create_invalidation_for_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_invalidation_for_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_invalidation_for_distribution_tenant("test-id", {}, region_name=REGION)
    mock_client.create_invalidation_for_distribution_tenant.assert_called_once()


def test_create_invalidation_for_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_invalidation_for_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_invalidation_for_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create invalidation for distribution tenant"):
        create_invalidation_for_distribution_tenant("test-id", {}, region_name=REGION)


def test_create_key_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_key_group({}, region_name=REGION)
    mock_client.create_key_group.assert_called_once()


def test_create_key_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create key group"):
        create_key_group({}, region_name=REGION)


def test_create_key_value_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_value_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_key_value_store("test-name", region_name=REGION)
    mock_client.create_key_value_store.assert_called_once()


def test_create_key_value_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_value_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key_value_store",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create key value store"):
        create_key_value_store("test-name", region_name=REGION)


def test_create_monitoring_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_monitoring_subscription.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_monitoring_subscription("test-distribution_id", {}, region_name=REGION)
    mock_client.create_monitoring_subscription.assert_called_once()


def test_create_monitoring_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_monitoring_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_monitoring_subscription",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create monitoring subscription"):
        create_monitoring_subscription("test-distribution_id", {}, region_name=REGION)


def test_create_origin_request_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_origin_request_policy({}, region_name=REGION)
    mock_client.create_origin_request_policy.assert_called_once()


def test_create_origin_request_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_origin_request_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_origin_request_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create origin request policy"):
        create_origin_request_policy({}, region_name=REGION)


def test_create_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_public_key({}, region_name=REGION)
    mock_client.create_public_key.assert_called_once()


def test_create_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_public_key",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create public key"):
        create_public_key({}, region_name=REGION)


def test_create_realtime_log_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_realtime_log_config([], [], "test-name", 1, region_name=REGION)
    mock_client.create_realtime_log_config.assert_called_once()


def test_create_realtime_log_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_realtime_log_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_realtime_log_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create realtime log config"):
        create_realtime_log_config([], [], "test-name", 1, region_name=REGION)


def test_create_response_headers_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_response_headers_policy({}, region_name=REGION)
    mock_client.create_response_headers_policy.assert_called_once()


def test_create_response_headers_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_response_headers_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_response_headers_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create response headers policy"):
        create_response_headers_policy({}, region_name=REGION)


def test_create_streaming_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_streaming_distribution({}, region_name=REGION)
    mock_client.create_streaming_distribution.assert_called_once()


def test_create_streaming_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_streaming_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_streaming_distribution",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create streaming distribution"):
        create_streaming_distribution({}, region_name=REGION)


def test_create_streaming_distribution_with_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_streaming_distribution_with_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_streaming_distribution_with_tags({}, region_name=REGION)
    mock_client.create_streaming_distribution_with_tags.assert_called_once()


def test_create_streaming_distribution_with_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_streaming_distribution_with_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_streaming_distribution_with_tags",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create streaming distribution with tags"):
        create_streaming_distribution_with_tags({}, region_name=REGION)


def test_create_vpc_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_origin.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_vpc_origin({}, region_name=REGION)
    mock_client.create_vpc_origin.assert_called_once()


def test_create_vpc_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_origin",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc origin"):
        create_vpc_origin({}, region_name=REGION)


def test_delete_anycast_ip_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_anycast_ip_list("test-id", "test-if_match", region_name=REGION)
    mock_client.delete_anycast_ip_list.assert_called_once()


def test_delete_anycast_ip_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_anycast_ip_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_anycast_ip_list",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete anycast ip list"):
        delete_anycast_ip_list("test-id", "test-if_match", region_name=REGION)


def test_delete_cache_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_cache_policy("test-id", region_name=REGION)
    mock_client.delete_cache_policy.assert_called_once()


def test_delete_cache_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cache_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cache policy"):
        delete_cache_policy("test-id", region_name=REGION)


def test_delete_cloud_front_origin_access_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_cloud_front_origin_access_identity("test-id", region_name=REGION)
    mock_client.delete_cloud_front_origin_access_identity.assert_called_once()


def test_delete_cloud_front_origin_access_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cloud_front_origin_access_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cloud_front_origin_access_identity",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cloud front origin access identity"):
        delete_cloud_front_origin_access_identity("test-id", region_name=REGION)


def test_delete_connection_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_connection_group("test-id", "test-if_match", region_name=REGION)
    mock_client.delete_connection_group.assert_called_once()


def test_delete_connection_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connection group"):
        delete_connection_group("test-id", "test-if_match", region_name=REGION)


def test_delete_continuous_deployment_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_continuous_deployment_policy("test-id", region_name=REGION)
    mock_client.delete_continuous_deployment_policy.assert_called_once()


def test_delete_continuous_deployment_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_continuous_deployment_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_continuous_deployment_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete continuous deployment policy"):
        delete_continuous_deployment_policy("test-id", region_name=REGION)


def test_delete_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_distribution_tenant("test-id", "test-if_match", region_name=REGION)
    mock_client.delete_distribution_tenant.assert_called_once()


def test_delete_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete distribution tenant"):
        delete_distribution_tenant("test-id", "test-if_match", region_name=REGION)


def test_delete_field_level_encryption_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_field_level_encryption_config("test-id", region_name=REGION)
    mock_client.delete_field_level_encryption_config.assert_called_once()


def test_delete_field_level_encryption_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_field_level_encryption_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete field level encryption config"):
        delete_field_level_encryption_config("test-id", region_name=REGION)


def test_delete_field_level_encryption_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_field_level_encryption_profile("test-id", region_name=REGION)
    mock_client.delete_field_level_encryption_profile.assert_called_once()


def test_delete_field_level_encryption_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_field_level_encryption_profile",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete field level encryption profile"):
        delete_field_level_encryption_profile("test-id", region_name=REGION)


def test_delete_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_function("test-name", "test-if_match", region_name=REGION)
    mock_client.delete_function.assert_called_once()


def test_delete_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete function"):
        delete_function("test-name", "test-if_match", region_name=REGION)


def test_delete_key_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_key_group("test-id", region_name=REGION)
    mock_client.delete_key_group.assert_called_once()


def test_delete_key_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_key_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete key group"):
        delete_key_group("test-id", region_name=REGION)


def test_delete_key_value_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_value_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_key_value_store("test-name", "test-if_match", region_name=REGION)
    mock_client.delete_key_value_store.assert_called_once()


def test_delete_key_value_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_value_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_key_value_store",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete key value store"):
        delete_key_value_store("test-name", "test-if_match", region_name=REGION)


def test_delete_monitoring_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_monitoring_subscription.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_monitoring_subscription("test-distribution_id", region_name=REGION)
    mock_client.delete_monitoring_subscription.assert_called_once()


def test_delete_monitoring_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_monitoring_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_monitoring_subscription",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete monitoring subscription"):
        delete_monitoring_subscription("test-distribution_id", region_name=REGION)


def test_delete_origin_request_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_origin_request_policy("test-id", region_name=REGION)
    mock_client.delete_origin_request_policy.assert_called_once()


def test_delete_origin_request_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_origin_request_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_origin_request_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete origin request policy"):
        delete_origin_request_policy("test-id", region_name=REGION)


def test_delete_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_public_key("test-id", region_name=REGION)
    mock_client.delete_public_key.assert_called_once()


def test_delete_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_public_key",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete public key"):
        delete_public_key("test-id", region_name=REGION)


def test_delete_realtime_log_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_realtime_log_config(region_name=REGION)
    mock_client.delete_realtime_log_config.assert_called_once()


def test_delete_realtime_log_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_realtime_log_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_realtime_log_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete realtime log config"):
        delete_realtime_log_config(region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_response_headers_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_response_headers_policy("test-id", region_name=REGION)
    mock_client.delete_response_headers_policy.assert_called_once()


def test_delete_response_headers_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_response_headers_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_response_headers_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete response headers policy"):
        delete_response_headers_policy("test-id", region_name=REGION)


def test_delete_streaming_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_streaming_distribution("test-id", region_name=REGION)
    mock_client.delete_streaming_distribution.assert_called_once()


def test_delete_streaming_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_streaming_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_streaming_distribution",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete streaming distribution"):
        delete_streaming_distribution("test-id", region_name=REGION)


def test_delete_vpc_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_origin.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_vpc_origin("test-id", "test-if_match", region_name=REGION)
    mock_client.delete_vpc_origin.assert_called_once()


def test_delete_vpc_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_origin",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc origin"):
        delete_vpc_origin("test-id", "test-if_match", region_name=REGION)


def test_describe_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    describe_function("test-name", region_name=REGION)
    mock_client.describe_function.assert_called_once()


def test_describe_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe function"):
        describe_function("test-name", region_name=REGION)


def test_describe_key_value_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_value_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    describe_key_value_store("test-name", region_name=REGION)
    mock_client.describe_key_value_store.assert_called_once()


def test_describe_key_value_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_value_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_key_value_store",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe key value store"):
        describe_key_value_store("test-name", region_name=REGION)


def test_disassociate_distribution_tenant_web_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_distribution_tenant_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    disassociate_distribution_tenant_web_acl("test-id", region_name=REGION)
    mock_client.disassociate_distribution_tenant_web_acl.assert_called_once()


def test_disassociate_distribution_tenant_web_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_distribution_tenant_web_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_distribution_tenant_web_acl",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate distribution tenant web acl"):
        disassociate_distribution_tenant_web_acl("test-id", region_name=REGION)


def test_disassociate_distribution_web_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_distribution_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    disassociate_distribution_web_acl("test-id", region_name=REGION)
    mock_client.disassociate_distribution_web_acl.assert_called_once()


def test_disassociate_distribution_web_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_distribution_web_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_distribution_web_acl",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate distribution web acl"):
        disassociate_distribution_web_acl("test-id", region_name=REGION)


def test_get_anycast_ip_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_anycast_ip_list("test-id", region_name=REGION)
    mock_client.get_anycast_ip_list.assert_called_once()


def test_get_anycast_ip_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_anycast_ip_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_anycast_ip_list",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get anycast ip list"):
        get_anycast_ip_list("test-id", region_name=REGION)


def test_get_cache_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_cache_policy("test-id", region_name=REGION)
    mock_client.get_cache_policy.assert_called_once()


def test_get_cache_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cache_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cache_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cache policy"):
        get_cache_policy("test-id", region_name=REGION)


def test_get_cache_policy_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cache_policy_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_cache_policy_config("test-id", region_name=REGION)
    mock_client.get_cache_policy_config.assert_called_once()


def test_get_cache_policy_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cache_policy_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cache_policy_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cache policy config"):
        get_cache_policy_config("test-id", region_name=REGION)


def test_get_cloud_front_origin_access_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_cloud_front_origin_access_identity("test-id", region_name=REGION)
    mock_client.get_cloud_front_origin_access_identity.assert_called_once()


def test_get_cloud_front_origin_access_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cloud_front_origin_access_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cloud_front_origin_access_identity",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cloud front origin access identity"):
        get_cloud_front_origin_access_identity("test-id", region_name=REGION)


def test_get_cloud_front_origin_access_identity_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cloud_front_origin_access_identity_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_cloud_front_origin_access_identity_config("test-id", region_name=REGION)
    mock_client.get_cloud_front_origin_access_identity_config.assert_called_once()


def test_get_cloud_front_origin_access_identity_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cloud_front_origin_access_identity_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cloud_front_origin_access_identity_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cloud front origin access identity config"):
        get_cloud_front_origin_access_identity_config("test-id", region_name=REGION)


def test_get_connection_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_connection_group("test-identifier", region_name=REGION)
    mock_client.get_connection_group.assert_called_once()


def test_get_connection_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connection_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connection group"):
        get_connection_group("test-identifier", region_name=REGION)


def test_get_connection_group_by_routing_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_group_by_routing_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_connection_group_by_routing_endpoint("test-routing_endpoint", region_name=REGION)
    mock_client.get_connection_group_by_routing_endpoint.assert_called_once()


def test_get_connection_group_by_routing_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_group_by_routing_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connection_group_by_routing_endpoint",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connection group by routing endpoint"):
        get_connection_group_by_routing_endpoint("test-routing_endpoint", region_name=REGION)


def test_get_continuous_deployment_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_continuous_deployment_policy("test-id", region_name=REGION)
    mock_client.get_continuous_deployment_policy.assert_called_once()


def test_get_continuous_deployment_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_continuous_deployment_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_continuous_deployment_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get continuous deployment policy"):
        get_continuous_deployment_policy("test-id", region_name=REGION)


def test_get_continuous_deployment_policy_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_continuous_deployment_policy_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_continuous_deployment_policy_config("test-id", region_name=REGION)
    mock_client.get_continuous_deployment_policy_config.assert_called_once()


def test_get_continuous_deployment_policy_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_continuous_deployment_policy_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_continuous_deployment_policy_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get continuous deployment policy config"):
        get_continuous_deployment_policy_config("test-id", region_name=REGION)


def test_get_distribution_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_distribution_config("test-id", region_name=REGION)
    mock_client.get_distribution_config.assert_called_once()


def test_get_distribution_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get distribution config"):
        get_distribution_config("test-id", region_name=REGION)


def test_get_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_distribution_tenant("test-identifier", region_name=REGION)
    mock_client.get_distribution_tenant.assert_called_once()


def test_get_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get distribution tenant"):
        get_distribution_tenant("test-identifier", region_name=REGION)


def test_get_distribution_tenant_by_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_tenant_by_domain.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_distribution_tenant_by_domain("test-domain", region_name=REGION)
    mock_client.get_distribution_tenant_by_domain.assert_called_once()


def test_get_distribution_tenant_by_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_distribution_tenant_by_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_tenant_by_domain",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get distribution tenant by domain"):
        get_distribution_tenant_by_domain("test-domain", region_name=REGION)


def test_get_field_level_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_field_level_encryption("test-id", region_name=REGION)
    mock_client.get_field_level_encryption.assert_called_once()


def test_get_field_level_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_field_level_encryption",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get field level encryption"):
        get_field_level_encryption("test-id", region_name=REGION)


def test_get_field_level_encryption_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_field_level_encryption_config("test-id", region_name=REGION)
    mock_client.get_field_level_encryption_config.assert_called_once()


def test_get_field_level_encryption_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_field_level_encryption_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get field level encryption config"):
        get_field_level_encryption_config("test-id", region_name=REGION)


def test_get_field_level_encryption_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_field_level_encryption_profile("test-id", region_name=REGION)
    mock_client.get_field_level_encryption_profile.assert_called_once()


def test_get_field_level_encryption_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_field_level_encryption_profile",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get field level encryption profile"):
        get_field_level_encryption_profile("test-id", region_name=REGION)


def test_get_field_level_encryption_profile_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_profile_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_field_level_encryption_profile_config("test-id", region_name=REGION)
    mock_client.get_field_level_encryption_profile_config.assert_called_once()


def test_get_field_level_encryption_profile_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_field_level_encryption_profile_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_field_level_encryption_profile_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get field level encryption profile config"):
        get_field_level_encryption_profile_config("test-id", region_name=REGION)


def test_get_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_function("test-name", region_name=REGION)
    mock_client.get_function.assert_called_once()


def test_get_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get function"):
        get_function("test-name", region_name=REGION)


def test_get_invalidation_for_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invalidation_for_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_invalidation_for_distribution_tenant("test-distribution_tenant_id", "test-id", region_name=REGION)
    mock_client.get_invalidation_for_distribution_tenant.assert_called_once()


def test_get_invalidation_for_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invalidation_for_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_invalidation_for_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get invalidation for distribution tenant"):
        get_invalidation_for_distribution_tenant("test-distribution_tenant_id", "test-id", region_name=REGION)


def test_get_key_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_key_group("test-id", region_name=REGION)
    mock_client.get_key_group.assert_called_once()


def test_get_key_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get key group"):
        get_key_group("test-id", region_name=REGION)


def test_get_key_group_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_group_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_key_group_config("test-id", region_name=REGION)
    mock_client.get_key_group_config.assert_called_once()


def test_get_key_group_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_group_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_group_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get key group config"):
        get_key_group_config("test-id", region_name=REGION)


def test_get_managed_certificate_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_certificate_details.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_managed_certificate_details("test-identifier", region_name=REGION)
    mock_client.get_managed_certificate_details.assert_called_once()


def test_get_managed_certificate_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_certificate_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_managed_certificate_details",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get managed certificate details"):
        get_managed_certificate_details("test-identifier", region_name=REGION)


def test_get_monitoring_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_monitoring_subscription.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_monitoring_subscription("test-distribution_id", region_name=REGION)
    mock_client.get_monitoring_subscription.assert_called_once()


def test_get_monitoring_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_monitoring_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_monitoring_subscription",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get monitoring subscription"):
        get_monitoring_subscription("test-distribution_id", region_name=REGION)


def test_get_origin_access_control_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_access_control_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_origin_access_control_config("test-id", region_name=REGION)
    mock_client.get_origin_access_control_config.assert_called_once()


def test_get_origin_access_control_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_access_control_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_origin_access_control_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get origin access control config"):
        get_origin_access_control_config("test-id", region_name=REGION)


def test_get_origin_request_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_origin_request_policy("test-id", region_name=REGION)
    mock_client.get_origin_request_policy.assert_called_once()


def test_get_origin_request_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_request_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_origin_request_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get origin request policy"):
        get_origin_request_policy("test-id", region_name=REGION)


def test_get_origin_request_policy_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_request_policy_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_origin_request_policy_config("test-id", region_name=REGION)
    mock_client.get_origin_request_policy_config.assert_called_once()


def test_get_origin_request_policy_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_origin_request_policy_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_origin_request_policy_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get origin request policy config"):
        get_origin_request_policy_config("test-id", region_name=REGION)


def test_get_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_public_key("test-id", region_name=REGION)
    mock_client.get_public_key.assert_called_once()


def test_get_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_public_key",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get public key"):
        get_public_key("test-id", region_name=REGION)


def test_get_public_key_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_public_key_config("test-id", region_name=REGION)
    mock_client.get_public_key_config.assert_called_once()


def test_get_public_key_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_public_key_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get public key config"):
        get_public_key_config("test-id", region_name=REGION)


def test_get_realtime_log_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_realtime_log_config(region_name=REGION)
    mock_client.get_realtime_log_config.assert_called_once()


def test_get_realtime_log_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_realtime_log_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_realtime_log_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get realtime log config"):
        get_realtime_log_config(region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_get_response_headers_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_response_headers_policy("test-id", region_name=REGION)
    mock_client.get_response_headers_policy.assert_called_once()


def test_get_response_headers_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_response_headers_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_response_headers_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get response headers policy"):
        get_response_headers_policy("test-id", region_name=REGION)


def test_get_response_headers_policy_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_response_headers_policy_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_response_headers_policy_config("test-id", region_name=REGION)
    mock_client.get_response_headers_policy_config.assert_called_once()


def test_get_response_headers_policy_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_response_headers_policy_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_response_headers_policy_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get response headers policy config"):
        get_response_headers_policy_config("test-id", region_name=REGION)


def test_get_streaming_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_streaming_distribution("test-id", region_name=REGION)
    mock_client.get_streaming_distribution.assert_called_once()


def test_get_streaming_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_streaming_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_streaming_distribution",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get streaming distribution"):
        get_streaming_distribution("test-id", region_name=REGION)


def test_get_streaming_distribution_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_streaming_distribution_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_streaming_distribution_config("test-id", region_name=REGION)
    mock_client.get_streaming_distribution_config.assert_called_once()


def test_get_streaming_distribution_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_streaming_distribution_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_streaming_distribution_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get streaming distribution config"):
        get_streaming_distribution_config("test-id", region_name=REGION)


def test_get_vpc_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_origin.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_vpc_origin("test-id", region_name=REGION)
    mock_client.get_vpc_origin.assert_called_once()


def test_get_vpc_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpc_origin",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get vpc origin"):
        get_vpc_origin("test-id", region_name=REGION)


def test_list_anycast_ip_lists(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_anycast_ip_lists.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_anycast_ip_lists(region_name=REGION)
    mock_client.list_anycast_ip_lists.assert_called_once()


def test_list_anycast_ip_lists_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_anycast_ip_lists.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_anycast_ip_lists",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list anycast ip lists"):
        list_anycast_ip_lists(region_name=REGION)


def test_list_cache_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cache_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_cache_policies(region_name=REGION)
    mock_client.list_cache_policies.assert_called_once()


def test_list_cache_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cache_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cache_policies",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cache policies"):
        list_cache_policies(region_name=REGION)


def test_list_cloud_front_origin_access_identities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cloud_front_origin_access_identities.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_cloud_front_origin_access_identities(region_name=REGION)
    mock_client.list_cloud_front_origin_access_identities.assert_called_once()


def test_list_cloud_front_origin_access_identities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cloud_front_origin_access_identities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cloud_front_origin_access_identities",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cloud front origin access identities"):
        list_cloud_front_origin_access_identities(region_name=REGION)


def test_list_conflicting_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_conflicting_aliases.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_conflicting_aliases("test-distribution_id", "test-alias", region_name=REGION)
    mock_client.list_conflicting_aliases.assert_called_once()


def test_list_conflicting_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_conflicting_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_conflicting_aliases",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list conflicting aliases"):
        list_conflicting_aliases("test-distribution_id", "test-alias", region_name=REGION)


def test_list_connection_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connection_groups.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_connection_groups(region_name=REGION)
    mock_client.list_connection_groups.assert_called_once()


def test_list_connection_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connection_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_connection_groups",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list connection groups"):
        list_connection_groups(region_name=REGION)


def test_list_continuous_deployment_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_continuous_deployment_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_continuous_deployment_policies(region_name=REGION)
    mock_client.list_continuous_deployment_policies.assert_called_once()


def test_list_continuous_deployment_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_continuous_deployment_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_continuous_deployment_policies",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list continuous deployment policies"):
        list_continuous_deployment_policies(region_name=REGION)


def test_list_distribution_tenants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distribution_tenants.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distribution_tenants(region_name=REGION)
    mock_client.list_distribution_tenants.assert_called_once()


def test_list_distribution_tenants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distribution_tenants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distribution_tenants",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distribution tenants"):
        list_distribution_tenants(region_name=REGION)


def test_list_distribution_tenants_by_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distribution_tenants_by_customization.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distribution_tenants_by_customization(region_name=REGION)
    mock_client.list_distribution_tenants_by_customization.assert_called_once()


def test_list_distribution_tenants_by_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distribution_tenants_by_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distribution_tenants_by_customization",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distribution tenants by customization"):
        list_distribution_tenants_by_customization(region_name=REGION)


def test_list_distributions_by_anycast_ip_list_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_anycast_ip_list_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", region_name=REGION)
    mock_client.list_distributions_by_anycast_ip_list_id.assert_called_once()


def test_list_distributions_by_anycast_ip_list_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_anycast_ip_list_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_anycast_ip_list_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by anycast ip list id"):
        list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", region_name=REGION)


def test_list_distributions_by_cache_policy_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_cache_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_cache_policy_id("test-cache_policy_id", region_name=REGION)
    mock_client.list_distributions_by_cache_policy_id.assert_called_once()


def test_list_distributions_by_cache_policy_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_cache_policy_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_cache_policy_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by cache policy id"):
        list_distributions_by_cache_policy_id("test-cache_policy_id", region_name=REGION)


def test_list_distributions_by_connection_mode(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_connection_mode.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_connection_mode("test-connection_mode", region_name=REGION)
    mock_client.list_distributions_by_connection_mode.assert_called_once()


def test_list_distributions_by_connection_mode_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_connection_mode.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_connection_mode",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by connection mode"):
        list_distributions_by_connection_mode("test-connection_mode", region_name=REGION)


def test_list_distributions_by_key_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_key_group("test-key_group_id", region_name=REGION)
    mock_client.list_distributions_by_key_group.assert_called_once()


def test_list_distributions_by_key_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_key_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_key_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by key group"):
        list_distributions_by_key_group("test-key_group_id", region_name=REGION)


def test_list_distributions_by_origin_request_policy_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_origin_request_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", region_name=REGION)
    mock_client.list_distributions_by_origin_request_policy_id.assert_called_once()


def test_list_distributions_by_origin_request_policy_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_origin_request_policy_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_origin_request_policy_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by origin request policy id"):
        list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", region_name=REGION)


def test_list_distributions_by_owned_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_owned_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_owned_resource("test-resource_arn", region_name=REGION)
    mock_client.list_distributions_by_owned_resource.assert_called_once()


def test_list_distributions_by_owned_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_owned_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_owned_resource",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by owned resource"):
        list_distributions_by_owned_resource("test-resource_arn", region_name=REGION)


def test_list_distributions_by_realtime_log_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_realtime_log_config(region_name=REGION)
    mock_client.list_distributions_by_realtime_log_config.assert_called_once()


def test_list_distributions_by_realtime_log_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_realtime_log_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_realtime_log_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by realtime log config"):
        list_distributions_by_realtime_log_config(region_name=REGION)


def test_list_distributions_by_response_headers_policy_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_response_headers_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", region_name=REGION)
    mock_client.list_distributions_by_response_headers_policy_id.assert_called_once()


def test_list_distributions_by_response_headers_policy_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_response_headers_policy_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_response_headers_policy_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by response headers policy id"):
        list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", region_name=REGION)


def test_list_distributions_by_vpc_origin_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_vpc_origin_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_vpc_origin_id("test-vpc_origin_id", region_name=REGION)
    mock_client.list_distributions_by_vpc_origin_id.assert_called_once()


def test_list_distributions_by_vpc_origin_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_vpc_origin_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_vpc_origin_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by vpc origin id"):
        list_distributions_by_vpc_origin_id("test-vpc_origin_id", region_name=REGION)


def test_list_distributions_by_web_acl_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_web_acl_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_web_acl_id("test-web_acl_id", region_name=REGION)
    mock_client.list_distributions_by_web_acl_id.assert_called_once()


def test_list_distributions_by_web_acl_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_distributions_by_web_acl_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_distributions_by_web_acl_id",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list distributions by web acl id"):
        list_distributions_by_web_acl_id("test-web_acl_id", region_name=REGION)


def test_list_domain_conflicts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_conflicts.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_domain_conflicts("test-domain", {}, region_name=REGION)
    mock_client.list_domain_conflicts.assert_called_once()


def test_list_domain_conflicts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_conflicts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_domain_conflicts",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list domain conflicts"):
        list_domain_conflicts("test-domain", {}, region_name=REGION)


def test_list_field_level_encryption_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_configs.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_field_level_encryption_configs(region_name=REGION)
    mock_client.list_field_level_encryption_configs.assert_called_once()


def test_list_field_level_encryption_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_field_level_encryption_configs",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list field level encryption configs"):
        list_field_level_encryption_configs(region_name=REGION)


def test_list_field_level_encryption_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_profiles.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_field_level_encryption_profiles(region_name=REGION)
    mock_client.list_field_level_encryption_profiles.assert_called_once()


def test_list_field_level_encryption_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_field_level_encryption_profiles",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list field level encryption profiles"):
        list_field_level_encryption_profiles(region_name=REGION)


def test_list_functions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_functions(region_name=REGION)
    mock_client.list_functions.assert_called_once()


def test_list_functions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_functions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_functions",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list functions"):
        list_functions(region_name=REGION)


def test_list_invalidations_for_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invalidations_for_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_invalidations_for_distribution_tenant("test-id", region_name=REGION)
    mock_client.list_invalidations_for_distribution_tenant.assert_called_once()


def test_list_invalidations_for_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invalidations_for_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_invalidations_for_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list invalidations for distribution tenant"):
        list_invalidations_for_distribution_tenant("test-id", region_name=REGION)


def test_list_key_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_groups.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_key_groups(region_name=REGION)
    mock_client.list_key_groups.assert_called_once()


def test_list_key_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_key_groups",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list key groups"):
        list_key_groups(region_name=REGION)


def test_list_key_value_stores(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_value_stores.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_key_value_stores(region_name=REGION)
    mock_client.list_key_value_stores.assert_called_once()


def test_list_key_value_stores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_value_stores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_key_value_stores",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list key value stores"):
        list_key_value_stores(region_name=REGION)


def test_list_origin_request_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_origin_request_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_origin_request_policies(region_name=REGION)
    mock_client.list_origin_request_policies.assert_called_once()


def test_list_origin_request_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_origin_request_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_origin_request_policies",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list origin request policies"):
        list_origin_request_policies(region_name=REGION)


def test_list_public_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_public_keys(region_name=REGION)
    mock_client.list_public_keys.assert_called_once()


def test_list_public_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_public_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_public_keys",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list public keys"):
        list_public_keys(region_name=REGION)


def test_list_realtime_log_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_realtime_log_configs.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_realtime_log_configs(region_name=REGION)
    mock_client.list_realtime_log_configs.assert_called_once()


def test_list_realtime_log_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_realtime_log_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_realtime_log_configs",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list realtime log configs"):
        list_realtime_log_configs(region_name=REGION)


def test_list_response_headers_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_response_headers_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_response_headers_policies(region_name=REGION)
    mock_client.list_response_headers_policies.assert_called_once()


def test_list_response_headers_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_response_headers_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_response_headers_policies",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list response headers policies"):
        list_response_headers_policies(region_name=REGION)


def test_list_streaming_distributions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_streaming_distributions.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_streaming_distributions(region_name=REGION)
    mock_client.list_streaming_distributions.assert_called_once()


def test_list_streaming_distributions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_streaming_distributions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_streaming_distributions",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list streaming distributions"):
        list_streaming_distributions(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource", region_name=REGION)


def test_list_vpc_origins(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_origins.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_vpc_origins(region_name=REGION)
    mock_client.list_vpc_origins.assert_called_once()


def test_list_vpc_origins_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_origins.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_origins",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc origins"):
        list_vpc_origins(region_name=REGION)


def test_publish_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    publish_function("test-name", "test-if_match", region_name=REGION)
    mock_client.publish_function.assert_called_once()


def test_publish_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to publish function"):
        publish_function("test-name", "test-if_match", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy_document", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy_document", region_name=REGION)


def test_run_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    run_function("test-name", "test-if_match", "test-event_object", region_name=REGION)
    mock_client.test_function.assert_called_once()


def test_run_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run function"):
        run_function("test-name", "test-if_match", "test-event_object", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource", {}, region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource", {}, region_name=REGION)


def test_update_anycast_ip_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_anycast_ip_list("test-id", "test-if_match", region_name=REGION)
    mock_client.update_anycast_ip_list.assert_called_once()


def test_update_anycast_ip_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_anycast_ip_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_anycast_ip_list",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update anycast ip list"):
        update_anycast_ip_list("test-id", "test-if_match", region_name=REGION)


def test_update_cache_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_cache_policy({}, "test-id", region_name=REGION)
    mock_client.update_cache_policy.assert_called_once()


def test_update_cache_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cache_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cache_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update cache policy"):
        update_cache_policy({}, "test-id", region_name=REGION)


def test_update_cloud_front_origin_access_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_cloud_front_origin_access_identity({}, "test-id", region_name=REGION)
    mock_client.update_cloud_front_origin_access_identity.assert_called_once()


def test_update_cloud_front_origin_access_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cloud_front_origin_access_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cloud_front_origin_access_identity",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update cloud front origin access identity"):
        update_cloud_front_origin_access_identity({}, "test-id", region_name=REGION)


def test_update_connection_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_connection_group("test-id", "test-if_match", region_name=REGION)
    mock_client.update_connection_group.assert_called_once()


def test_update_connection_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connection_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connection group"):
        update_connection_group("test-id", "test-if_match", region_name=REGION)


def test_update_continuous_deployment_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_continuous_deployment_policy({}, "test-id", region_name=REGION)
    mock_client.update_continuous_deployment_policy.assert_called_once()


def test_update_continuous_deployment_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_continuous_deployment_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_continuous_deployment_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update continuous deployment policy"):
        update_continuous_deployment_policy({}, "test-id", region_name=REGION)


def test_update_distribution_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_distribution_tenant("test-id", "test-if_match", region_name=REGION)
    mock_client.update_distribution_tenant.assert_called_once()


def test_update_distribution_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_distribution_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_distribution_tenant",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update distribution tenant"):
        update_distribution_tenant("test-id", "test-if_match", region_name=REGION)


def test_update_distribution_with_staging_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_distribution_with_staging_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_distribution_with_staging_config("test-id", region_name=REGION)
    mock_client.update_distribution_with_staging_config.assert_called_once()


def test_update_distribution_with_staging_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_distribution_with_staging_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_distribution_with_staging_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update distribution with staging config"):
        update_distribution_with_staging_config("test-id", region_name=REGION)


def test_update_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_domain_association("test-domain", {}, region_name=REGION)
    mock_client.update_domain_association.assert_called_once()


def test_update_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_domain_association",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update domain association"):
        update_domain_association("test-domain", {}, region_name=REGION)


def test_update_field_level_encryption_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_field_level_encryption_config({}, "test-id", region_name=REGION)
    mock_client.update_field_level_encryption_config.assert_called_once()


def test_update_field_level_encryption_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_field_level_encryption_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update field level encryption config"):
        update_field_level_encryption_config({}, "test-id", region_name=REGION)


def test_update_field_level_encryption_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_field_level_encryption_profile({}, "test-id", region_name=REGION)
    mock_client.update_field_level_encryption_profile.assert_called_once()


def test_update_field_level_encryption_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_field_level_encryption_profile",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update field level encryption profile"):
        update_field_level_encryption_profile({}, "test-id", region_name=REGION)


def test_update_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_function("test-name", "test-if_match", {}, "test-function_code", region_name=REGION)
    mock_client.update_function.assert_called_once()


def test_update_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_function",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update function"):
        update_function("test-name", "test-if_match", {}, "test-function_code", region_name=REGION)


def test_update_key_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_key_group({}, "test-id", region_name=REGION)
    mock_client.update_key_group.assert_called_once()


def test_update_key_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_key_group",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update key group"):
        update_key_group({}, "test-id", region_name=REGION)


def test_update_key_value_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_value_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_key_value_store("test-name", "test-comment", "test-if_match", region_name=REGION)
    mock_client.update_key_value_store.assert_called_once()


def test_update_key_value_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_value_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_key_value_store",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update key value store"):
        update_key_value_store("test-name", "test-comment", "test-if_match", region_name=REGION)


def test_update_origin_access_control(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_origin_access_control.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_origin_access_control({}, "test-id", region_name=REGION)
    mock_client.update_origin_access_control.assert_called_once()


def test_update_origin_access_control_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_origin_access_control.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_origin_access_control",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update origin access control"):
        update_origin_access_control({}, "test-id", region_name=REGION)


def test_update_origin_request_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_origin_request_policy({}, "test-id", region_name=REGION)
    mock_client.update_origin_request_policy.assert_called_once()


def test_update_origin_request_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_origin_request_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_origin_request_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update origin request policy"):
        update_origin_request_policy({}, "test-id", region_name=REGION)


def test_update_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_public_key({}, "test-id", region_name=REGION)
    mock_client.update_public_key.assert_called_once()


def test_update_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_public_key",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update public key"):
        update_public_key({}, "test-id", region_name=REGION)


def test_update_realtime_log_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_realtime_log_config(region_name=REGION)
    mock_client.update_realtime_log_config.assert_called_once()


def test_update_realtime_log_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_realtime_log_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_realtime_log_config",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update realtime log config"):
        update_realtime_log_config(region_name=REGION)


def test_update_response_headers_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_response_headers_policy({}, "test-id", region_name=REGION)
    mock_client.update_response_headers_policy.assert_called_once()


def test_update_response_headers_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_response_headers_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_response_headers_policy",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update response headers policy"):
        update_response_headers_policy({}, "test-id", region_name=REGION)


def test_update_streaming_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_streaming_distribution({}, "test-id", region_name=REGION)
    mock_client.update_streaming_distribution.assert_called_once()


def test_update_streaming_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_streaming_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_streaming_distribution",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update streaming distribution"):
        update_streaming_distribution({}, "test-id", region_name=REGION)


def test_update_vpc_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_origin.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_vpc_origin({}, "test-id", "test-if_match", region_name=REGION)
    mock_client.update_vpc_origin.assert_called_once()


def test_update_vpc_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vpc_origin",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vpc origin"):
        update_vpc_origin({}, "test-id", "test-if_match", region_name=REGION)


def test_verify_dns_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_dns_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    verify_dns_configuration("test-identifier", region_name=REGION)
    mock_client.verify_dns_configuration.assert_called_once()


def test_verify_dns_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_dns_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_dns_configuration",
    )
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify dns configuration"):
        verify_dns_configuration("test-identifier", region_name=REGION)


def test_associate_distribution_tenant_web_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import associate_distribution_tenant_web_acl
    mock_client = MagicMock()
    mock_client.associate_distribution_tenant_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", if_match="test-if_match", region_name="us-east-1")
    mock_client.associate_distribution_tenant_web_acl.assert_called_once()

def test_associate_distribution_web_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import associate_distribution_web_acl
    mock_client = MagicMock()
    mock_client.associate_distribution_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    associate_distribution_web_acl("test-id", "test-web_acl_arn", if_match="test-if_match", region_name="us-east-1")
    mock_client.associate_distribution_web_acl.assert_called_once()

def test_copy_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import copy_distribution
    mock_client = MagicMock()
    mock_client.copy_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    copy_distribution("test-primary_distribution_id", "test-caller_reference", staging="test-staging", if_match="test-if_match", enabled=True, region_name="us-east-1")
    mock_client.copy_distribution.assert_called_once()

def test_create_anycast_ip_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import create_anycast_ip_list
    mock_client = MagicMock()
    mock_client.create_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_anycast_ip_list("test-name", 1, tags=[{"Key": "k", "Value": "v"}], ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.create_anycast_ip_list.assert_called_once()

def test_create_connection_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import create_connection_group
    mock_client = MagicMock()
    mock_client.create_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_connection_group("test-name", ipv6_enabled="test-ipv6_enabled", tags=[{"Key": "k", "Value": "v"}], anycast_ip_list_id="test-anycast_ip_list_id", enabled=True, region_name="us-east-1")
    mock_client.create_connection_group.assert_called_once()

def test_create_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import create_distribution_tenant
    mock_client = MagicMock()
    mock_client.create_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_distribution_tenant("test-distribution_id", "test-name", "test-domains", tags=[{"Key": "k", "Value": "v"}], customizations="test-customizations", parameters="test-parameters", connection_group_id="test-connection_group_id", managed_certificate_request="test-managed_certificate_request", enabled=True, region_name="us-east-1")
    mock_client.create_distribution_tenant.assert_called_once()

def test_create_key_value_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import create_key_value_store
    mock_client = MagicMock()
    mock_client.create_key_value_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_key_value_store("test-name", comment="test-comment", import_source=1, region_name="us-east-1")
    mock_client.create_key_value_store.assert_called_once()

def test_create_vpc_origin_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import create_vpc_origin
    mock_client = MagicMock()
    mock_client.create_vpc_origin.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    create_vpc_origin({}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vpc_origin.assert_called_once()

def test_delete_cache_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_cache_policy
    mock_client = MagicMock()
    mock_client.delete_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_cache_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_cache_policy.assert_called_once()

def test_delete_cloud_front_origin_access_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_cloud_front_origin_access_identity
    mock_client = MagicMock()
    mock_client.delete_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_cloud_front_origin_access_identity("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_cloud_front_origin_access_identity.assert_called_once()

def test_delete_continuous_deployment_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_continuous_deployment_policy
    mock_client = MagicMock()
    mock_client.delete_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_continuous_deployment_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_continuous_deployment_policy.assert_called_once()

def test_delete_field_level_encryption_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_field_level_encryption_config
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_field_level_encryption_config("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_field_level_encryption_config.assert_called_once()

def test_delete_field_level_encryption_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_field_level_encryption_profile
    mock_client = MagicMock()
    mock_client.delete_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_field_level_encryption_profile("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_field_level_encryption_profile.assert_called_once()

def test_delete_key_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_key_group
    mock_client = MagicMock()
    mock_client.delete_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_key_group("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_key_group.assert_called_once()

def test_delete_origin_request_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_origin_request_policy
    mock_client = MagicMock()
    mock_client.delete_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_origin_request_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_origin_request_policy.assert_called_once()

def test_delete_public_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_public_key
    mock_client = MagicMock()
    mock_client.delete_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_public_key("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_public_key.assert_called_once()

def test_delete_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_realtime_log_config
    mock_client = MagicMock()
    mock_client.delete_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_realtime_log_config(name="test-name", arn="test-arn", region_name="us-east-1")
    mock_client.delete_realtime_log_config.assert_called_once()

def test_delete_response_headers_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_response_headers_policy
    mock_client = MagicMock()
    mock_client.delete_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_response_headers_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_response_headers_policy.assert_called_once()

def test_delete_streaming_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import delete_streaming_distribution
    mock_client = MagicMock()
    mock_client.delete_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    delete_streaming_distribution("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.delete_streaming_distribution.assert_called_once()

def test_describe_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import describe_function
    mock_client = MagicMock()
    mock_client.describe_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    describe_function("test-name", stage="test-stage", region_name="us-east-1")
    mock_client.describe_function.assert_called_once()

def test_disassociate_distribution_tenant_web_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import disassociate_distribution_tenant_web_acl
    mock_client = MagicMock()
    mock_client.disassociate_distribution_tenant_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    disassociate_distribution_tenant_web_acl("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.disassociate_distribution_tenant_web_acl.assert_called_once()

def test_disassociate_distribution_web_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import disassociate_distribution_web_acl
    mock_client = MagicMock()
    mock_client.disassociate_distribution_web_acl.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    disassociate_distribution_web_acl("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.disassociate_distribution_web_acl.assert_called_once()

def test_get_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import get_function
    mock_client = MagicMock()
    mock_client.get_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_function("test-name", stage="test-stage", region_name="us-east-1")
    mock_client.get_function.assert_called_once()

def test_get_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import get_realtime_log_config
    mock_client = MagicMock()
    mock_client.get_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    get_realtime_log_config(name="test-name", arn="test-arn", region_name="us-east-1")
    mock_client.get_realtime_log_config.assert_called_once()

def test_list_anycast_ip_lists_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_anycast_ip_lists
    mock_client = MagicMock()
    mock_client.list_anycast_ip_lists.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_anycast_ip_lists(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_anycast_ip_lists.assert_called_once()

def test_list_cache_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_cache_policies
    mock_client = MagicMock()
    mock_client.list_cache_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_cache_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_cache_policies.assert_called_once()

def test_list_cloud_front_origin_access_identities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_cloud_front_origin_access_identities
    mock_client = MagicMock()
    mock_client.list_cloud_front_origin_access_identities.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_cloud_front_origin_access_identities(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_cloud_front_origin_access_identities.assert_called_once()

def test_list_conflicting_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_conflicting_aliases
    mock_client = MagicMock()
    mock_client.list_conflicting_aliases.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_conflicting_aliases("test-distribution_id", "test-alias", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_conflicting_aliases.assert_called_once()

def test_list_connection_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_connection_groups
    mock_client = MagicMock()
    mock_client.list_connection_groups.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_connection_groups(association_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_connection_groups.assert_called_once()

def test_list_continuous_deployment_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_continuous_deployment_policies
    mock_client = MagicMock()
    mock_client.list_continuous_deployment_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_continuous_deployment_policies(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_continuous_deployment_policies.assert_called_once()

def test_list_distribution_tenants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distribution_tenants
    mock_client = MagicMock()
    mock_client.list_distribution_tenants.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distribution_tenants(association_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distribution_tenants.assert_called_once()

def test_list_distribution_tenants_by_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distribution_tenants_by_customization
    mock_client = MagicMock()
    mock_client.list_distribution_tenants_by_customization.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distribution_tenants_by_customization(web_acl_arn="test-web_acl_arn", certificate_arn="test-certificate_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distribution_tenants_by_customization.assert_called_once()

def test_list_distributions_by_anycast_ip_list_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_anycast_ip_list_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_anycast_ip_list_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_anycast_ip_list_id.assert_called_once()

def test_list_distributions_by_cache_policy_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_cache_policy_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_cache_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_cache_policy_id("test-cache_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_cache_policy_id.assert_called_once()

def test_list_distributions_by_connection_mode_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_connection_mode
    mock_client = MagicMock()
    mock_client.list_distributions_by_connection_mode.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_connection_mode("test-connection_mode", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_connection_mode.assert_called_once()

def test_list_distributions_by_key_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_key_group
    mock_client = MagicMock()
    mock_client.list_distributions_by_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_key_group("test-key_group_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_key_group.assert_called_once()

def test_list_distributions_by_origin_request_policy_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_origin_request_policy_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_origin_request_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_origin_request_policy_id.assert_called_once()

def test_list_distributions_by_owned_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_owned_resource
    mock_client = MagicMock()
    mock_client.list_distributions_by_owned_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_owned_resource("test-resource_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_owned_resource.assert_called_once()

def test_list_distributions_by_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_realtime_log_config
    mock_client = MagicMock()
    mock_client.list_distributions_by_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_realtime_log_config(marker="test-marker", max_items=1, realtime_log_config_name={}, realtime_log_config_arn={}, region_name="us-east-1")
    mock_client.list_distributions_by_realtime_log_config.assert_called_once()

def test_list_distributions_by_response_headers_policy_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_response_headers_policy_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_response_headers_policy_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_response_headers_policy_id.assert_called_once()

def test_list_distributions_by_vpc_origin_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_vpc_origin_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_vpc_origin_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_vpc_origin_id("test-vpc_origin_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_vpc_origin_id.assert_called_once()

def test_list_distributions_by_web_acl_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_distributions_by_web_acl_id
    mock_client = MagicMock()
    mock_client.list_distributions_by_web_acl_id.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_distributions_by_web_acl_id("test-web_acl_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_distributions_by_web_acl_id.assert_called_once()

def test_list_domain_conflicts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_domain_conflicts
    mock_client = MagicMock()
    mock_client.list_domain_conflicts.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_domain_conflicts("test-domain", "test-domain_control_validation_resource", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_domain_conflicts.assert_called_once()

def test_list_field_level_encryption_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_field_level_encryption_configs
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_configs.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_field_level_encryption_configs(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_field_level_encryption_configs.assert_called_once()

def test_list_field_level_encryption_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_field_level_encryption_profiles
    mock_client = MagicMock()
    mock_client.list_field_level_encryption_profiles.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_field_level_encryption_profiles(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_field_level_encryption_profiles.assert_called_once()

def test_list_functions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_functions
    mock_client = MagicMock()
    mock_client.list_functions.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_functions(marker="test-marker", max_items=1, stage="test-stage", region_name="us-east-1")
    mock_client.list_functions.assert_called_once()

def test_list_invalidations_for_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_invalidations_for_distribution_tenant
    mock_client = MagicMock()
    mock_client.list_invalidations_for_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_invalidations_for_distribution_tenant("test-id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_invalidations_for_distribution_tenant.assert_called_once()

def test_list_key_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_key_groups
    mock_client = MagicMock()
    mock_client.list_key_groups.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_key_groups(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_key_groups.assert_called_once()

def test_list_key_value_stores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_key_value_stores
    mock_client = MagicMock()
    mock_client.list_key_value_stores.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_key_value_stores(marker="test-marker", max_items=1, status="test-status", region_name="us-east-1")
    mock_client.list_key_value_stores.assert_called_once()

def test_list_origin_request_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_origin_request_policies
    mock_client = MagicMock()
    mock_client.list_origin_request_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_origin_request_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_origin_request_policies.assert_called_once()

def test_list_public_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_public_keys
    mock_client = MagicMock()
    mock_client.list_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_public_keys(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_public_keys.assert_called_once()

def test_list_realtime_log_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_realtime_log_configs
    mock_client = MagicMock()
    mock_client.list_realtime_log_configs.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_realtime_log_configs(max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_realtime_log_configs.assert_called_once()

def test_list_response_headers_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_response_headers_policies
    mock_client = MagicMock()
    mock_client.list_response_headers_policies.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_response_headers_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_response_headers_policies.assert_called_once()

def test_list_streaming_distributions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_streaming_distributions
    mock_client = MagicMock()
    mock_client.list_streaming_distributions.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_streaming_distributions(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_streaming_distributions.assert_called_once()

def test_list_vpc_origins_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import list_vpc_origins
    mock_client = MagicMock()
    mock_client.list_vpc_origins.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    list_vpc_origins(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_vpc_origins.assert_called_once()

def test_run_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import run_function
    mock_client = MagicMock()
    mock_client.test_function.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    run_function("test-name", "test-if_match", "test-event_object", stage="test-stage", region_name="us-east-1")
    mock_client.test_function.assert_called_once()

def test_update_anycast_ip_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_anycast_ip_list
    mock_client = MagicMock()
    mock_client.update_anycast_ip_list.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_anycast_ip_list("test-id", "test-if_match", ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.update_anycast_ip_list.assert_called_once()

def test_update_cache_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_cache_policy
    mock_client = MagicMock()
    mock_client.update_cache_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_cache_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_cache_policy.assert_called_once()

def test_update_cloud_front_origin_access_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_cloud_front_origin_access_identity
    mock_client = MagicMock()
    mock_client.update_cloud_front_origin_access_identity.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_cloud_front_origin_access_identity({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_cloud_front_origin_access_identity.assert_called_once()

def test_update_connection_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_connection_group
    mock_client = MagicMock()
    mock_client.update_connection_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_connection_group("test-id", "test-if_match", ipv6_enabled="test-ipv6_enabled", anycast_ip_list_id="test-anycast_ip_list_id", enabled=True, region_name="us-east-1")
    mock_client.update_connection_group.assert_called_once()

def test_update_continuous_deployment_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_continuous_deployment_policy
    mock_client = MagicMock()
    mock_client.update_continuous_deployment_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_continuous_deployment_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_continuous_deployment_policy.assert_called_once()

def test_update_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_distribution_tenant
    mock_client = MagicMock()
    mock_client.update_distribution_tenant.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_distribution_tenant("test-id", "test-if_match", distribution_id="test-distribution_id", domains="test-domains", customizations="test-customizations", parameters="test-parameters", connection_group_id="test-connection_group_id", managed_certificate_request="test-managed_certificate_request", enabled=True, region_name="us-east-1")
    mock_client.update_distribution_tenant.assert_called_once()

def test_update_distribution_with_staging_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_distribution_with_staging_config
    mock_client = MagicMock()
    mock_client.update_distribution_with_staging_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_distribution_with_staging_config("test-id", staging_distribution_id="test-staging_distribution_id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_distribution_with_staging_config.assert_called_once()

def test_update_domain_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_domain_association
    mock_client = MagicMock()
    mock_client.update_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_domain_association("test-domain", "test-target_resource", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_domain_association.assert_called_once()

def test_update_field_level_encryption_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_field_level_encryption_config
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_field_level_encryption_config({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_field_level_encryption_config.assert_called_once()

def test_update_field_level_encryption_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_field_level_encryption_profile
    mock_client = MagicMock()
    mock_client.update_field_level_encryption_profile.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_field_level_encryption_profile({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_field_level_encryption_profile.assert_called_once()

def test_update_key_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_key_group
    mock_client = MagicMock()
    mock_client.update_key_group.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_key_group({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_key_group.assert_called_once()

def test_update_origin_access_control_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_origin_access_control
    mock_client = MagicMock()
    mock_client.update_origin_access_control.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_origin_access_control({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_origin_access_control.assert_called_once()

def test_update_origin_request_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_origin_request_policy
    mock_client = MagicMock()
    mock_client.update_origin_request_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_origin_request_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_origin_request_policy.assert_called_once()

def test_update_public_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_public_key
    mock_client = MagicMock()
    mock_client.update_public_key.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_public_key({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_public_key.assert_called_once()

def test_update_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_realtime_log_config
    mock_client = MagicMock()
    mock_client.update_realtime_log_config.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_realtime_log_config(end_points="test-end_points", fields="test-fields", name="test-name", arn="test-arn", sampling_rate="test-sampling_rate", region_name="us-east-1")
    mock_client.update_realtime_log_config.assert_called_once()

def test_update_response_headers_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_response_headers_policy
    mock_client = MagicMock()
    mock_client.update_response_headers_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_response_headers_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_response_headers_policy.assert_called_once()

def test_update_streaming_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import update_streaming_distribution
    mock_client = MagicMock()
    mock_client.update_streaming_distribution.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    update_streaming_distribution({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.update_streaming_distribution.assert_called_once()

def test_verify_dns_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudfront import verify_dns_configuration
    mock_client = MagicMock()
    mock_client.verify_dns_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudfront.get_client", lambda *a, **kw: mock_client)
    verify_dns_configuration("test-identifier", domain="test-domain", region_name="us-east-1")
    mock_client.verify_dns_configuration.assert_called_once()
