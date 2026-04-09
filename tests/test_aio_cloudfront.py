"""Tests for aws_util.aio.cloudfront — native async CloudFront utilities."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.cloudfront import (
    CachePolicyResult,
    DistributionResult,
    InvalidationResult,
    OriginAccessControlResult,
)

import aws_util.aio.cloudfront as cf_mod
from aws_util.aio.cloudfront import (
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
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client(monkeypatch):
    """Replace ``async_client`` so every function gets a mock client."""
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.cloudfront.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# create_distribution
# ---------------------------------------------------------------------------


async def test_create_distribution_success(mock_client):
    mock_client.call.return_value = {
        "Distribution": {
            "Id": "DIST1",
            "ARN": "arn:aws:cloudfront::123:distribution/DIST1",
            "DomainName": "d1.cloudfront.net",
            "Status": "InProgress",
            "LastModifiedTime": "2025-01-01T00:00:00Z",
            "DistributionConfig": {
                "Comment": "test",
                "Enabled": True,
                "Origins": {
                    "Items": [{"DomainName": "example.com", "Id": "o1"}],
                },
            },
        },
        "ETag": "E1",
    }
    result = await create_distribution(
        origins=[{"DomainName": "example.com", "Id": "o1"}],
        default_cache_behavior={"TargetOriginId": "o1"},
        comment="test",
    )
    assert result.id == "DIST1"
    assert result.etag == "E1"
    assert result.comment == "test"


async def test_create_distribution_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_distribution(
            origins=[],
            default_cache_behavior={},
        )


async def test_create_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_distribution failed"):
        await create_distribution(
            origins=[],
            default_cache_behavior={},
        )


async def test_create_distribution_with_caller_reference(mock_client):
    mock_client.call.return_value = {
        "Distribution": {
            "Id": "DIST2",
            "ARN": "arn:...",
            "DomainName": "d2.cloudfront.net",
            "Status": "InProgress",
            "DistributionConfig": {
                "Comment": "",
                "Enabled": True,
                "Origins": {"Items": []},
            },
        },
        "ETag": "E2",
    }
    await create_distribution(
        origins=[],
        default_cache_behavior={},
        caller_reference="my-ref",
    )
    call_kwargs = mock_client.call.call_args
    config = call_kwargs[1]["DistributionConfig"]
    assert config["CallerReference"] == "my-ref"


# ---------------------------------------------------------------------------
# get_distribution
# ---------------------------------------------------------------------------


async def test_get_distribution_success(mock_client):
    mock_client.call.return_value = {
        "Distribution": {
            "Id": "DIST1",
            "ARN": "arn:...",
            "DomainName": "d1.cloudfront.net",
            "Status": "Deployed",
            "LastModifiedTime": "2025-01-01",
            "DistributionConfig": {
                "Comment": "hello",
                "Enabled": True,
                "Origins": {"Items": []},
            },
        },
        "ETag": "ETAG1",
    }
    result = await get_distribution("DIST1")
    assert result.id == "DIST1"
    assert result.status == "Deployed"
    assert result.etag == "ETAG1"


async def test_get_distribution_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("not found")
    with pytest.raises(RuntimeError, match="not found"):
        await get_distribution("DIST1")


async def test_get_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="get_distribution failed"):
        await get_distribution("DIST1")


# ---------------------------------------------------------------------------
# list_distributions
# ---------------------------------------------------------------------------


async def test_list_distributions_empty(mock_client):
    mock_client.call.return_value = {
        "DistributionList": {"Items": [], "IsTruncated": False},
    }
    result = await list_distributions()
    assert result == []


async def test_list_distributions_single_page(mock_client):
    mock_client.call.return_value = {
        "DistributionList": {
            "Items": [
                {
                    "Id": "D1",
                    "ARN": "arn:...",
                    "DomainName": "d1.cloudfront.net",
                    "Status": "Deployed",
                    "Origins": {"Items": []},
                    "Comment": "",
                    "Enabled": True,
                }
            ],
            "IsTruncated": False,
        },
    }
    result = await list_distributions()
    assert len(result) == 1
    assert result[0].id == "D1"


async def test_list_distributions_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "DistributionList": {
                "Items": [
                    {
                        "Id": "D1",
                        "ARN": "arn:...",
                        "DomainName": "d1.cloudfront.net",
                        "Status": "Deployed",
                        "Origins": {"Items": []},
                        "Comment": "",
                        "Enabled": True,
                    }
                ],
                "IsTruncated": True,
                "NextMarker": "next1",
            },
        },
        {
            "DistributionList": {
                "Items": [
                    {
                        "Id": "D2",
                        "ARN": "arn:...",
                        "DomainName": "d2.cloudfront.net",
                        "Status": "Deployed",
                        "Origins": {"Items": []},
                        "Comment": "",
                        "Enabled": True,
                    }
                ],
                "IsTruncated": False,
            },
        },
    ]
    result = await list_distributions()
    assert len(result) == 2


async def test_list_distributions_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions()


async def test_list_distributions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="list_distributions failed"):
        await list_distributions()


# ---------------------------------------------------------------------------
# update_distribution
# ---------------------------------------------------------------------------


async def test_update_distribution_success(mock_client):
    mock_client.call.return_value = {
        "Distribution": {
            "Id": "DIST1",
            "ARN": "arn:...",
            "DomainName": "d1.cloudfront.net",
            "Status": "InProgress",
            "DistributionConfig": {
                "Comment": "updated",
                "Enabled": True,
                "Origins": {"Items": []},
            },
        },
        "ETag": "E2",
    }
    result = await update_distribution(
        "DIST1",
        distribution_config={"Comment": "updated"},
        if_match="E1",
    )
    assert result.comment == "updated"
    assert result.etag == "E2"


async def test_update_distribution_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_distribution(
            "DIST1", distribution_config={}, if_match="E1"
        )


async def test_update_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_distribution failed"):
        await update_distribution(
            "DIST1", distribution_config={}, if_match="E1"
        )


# ---------------------------------------------------------------------------
# delete_distribution
# ---------------------------------------------------------------------------


async def test_delete_distribution_success(mock_client):
    mock_client.call.return_value = {}
    await delete_distribution("DIST1", if_match="E1")
    mock_client.call.assert_called_once()


async def test_delete_distribution_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_distribution("DIST1", if_match="E1")


async def test_delete_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_distribution failed"):
        await delete_distribution("DIST1", if_match="E1")


# ---------------------------------------------------------------------------
# create_invalidation
# ---------------------------------------------------------------------------


async def test_create_invalidation_success(mock_client):
    mock_client.call.return_value = {
        "Invalidation": {
            "Id": "INV1",
            "Status": "InProgress",
            "CreateTime": "2025-01-01",
            "InvalidationBatch": {
                "Paths": {"Items": ["/*"]},
                "CallerReference": "ref1",
            },
        },
    }
    result = await create_invalidation("DIST1", paths=["/*"])
    assert result.id == "INV1"
    assert result.distribution_id == "DIST1"
    assert result.paths == ["/*"]


async def test_create_invalidation_with_caller_reference(mock_client):
    mock_client.call.return_value = {
        "Invalidation": {
            "Id": "INV2",
            "Status": "InProgress",
            "InvalidationBatch": {
                "Paths": {"Items": ["/index.html"]},
                "CallerReference": "my-ref",
            },
        },
    }
    await create_invalidation(
        "DIST1", paths=["/index.html"], caller_reference="my-ref"
    )
    call_kwargs = mock_client.call.call_args
    batch = call_kwargs[1]["InvalidationBatch"]
    assert batch["CallerReference"] == "my-ref"


async def test_create_invalidation_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_invalidation("DIST1", paths=["/*"])


async def test_create_invalidation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_invalidation failed"):
        await create_invalidation("DIST1", paths=["/*"])


# ---------------------------------------------------------------------------
# get_invalidation
# ---------------------------------------------------------------------------


async def test_get_invalidation_success(mock_client):
    mock_client.call.return_value = {
        "Invalidation": {
            "Id": "INV1",
            "Status": "Completed",
            "CreateTime": "2025-01-01",
            "InvalidationBatch": {
                "Paths": {"Items": ["/*"]},
                "CallerReference": "ref1",
            },
        },
    }
    result = await get_invalidation("DIST1", "INV1")
    assert result.id == "INV1"
    assert result.status == "Completed"


async def test_get_invalidation_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_invalidation("DIST1", "INV1")


async def test_get_invalidation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_invalidation failed"):
        await get_invalidation("DIST1", "INV1")


# ---------------------------------------------------------------------------
# list_invalidations
# ---------------------------------------------------------------------------


async def test_list_invalidations_empty(mock_client):
    mock_client.call.return_value = {
        "InvalidationList": {"Items": [], "IsTruncated": False},
    }
    result = await list_invalidations("DIST1")
    assert result == []


async def test_list_invalidations_single_page(mock_client):
    mock_client.call.return_value = {
        "InvalidationList": {
            "Items": [
                {
                    "Id": "INV1",
                    "Status": "Completed",
                    "CreateTime": "2025-01-01",
                }
            ],
            "IsTruncated": False,
        },
    }
    result = await list_invalidations("DIST1")
    assert len(result) == 1
    assert result[0].distribution_id == "DIST1"


async def test_list_invalidations_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "InvalidationList": {
                "Items": [
                    {"Id": "INV1", "Status": "Completed", "CreateTime": "2025-01-01"}
                ],
                "IsTruncated": True,
                "NextMarker": "next1",
            },
        },
        {
            "InvalidationList": {
                "Items": [
                    {"Id": "INV2", "Status": "Completed"}
                ],
                "IsTruncated": False,
            },
        },
    ]
    result = await list_invalidations("DIST1")
    assert len(result) == 2


async def test_list_invalidations_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_invalidations("DIST1")


async def test_list_invalidations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="list_invalidations failed"):
        await list_invalidations("DIST1")


async def test_list_invalidations_with_none_create_time(mock_client):
    mock_client.call.return_value = {
        "InvalidationList": {
            "Items": [
                {"Id": "INV1", "Status": "Completed", "CreateTime": None}
            ],
            "IsTruncated": False,
        },
    }
    result = await list_invalidations("DIST1")
    assert result[0].create_time is None


# ---------------------------------------------------------------------------
# create_origin_access_control
# ---------------------------------------------------------------------------


async def test_create_origin_access_control_success(mock_client):
    mock_client.call.return_value = {
        "OriginAccessControl": {
            "Id": "OAC1",
            "OriginAccessControlConfig": {
                "Name": "my-oac",
                "SigningProtocol": "sigv4",
                "SigningBehavior": "always",
                "OriginAccessControlOriginType": "s3",
            },
        },
    }
    result = await create_origin_access_control("my-oac")
    assert result.id == "OAC1"
    assert result.name == "my-oac"


async def test_create_origin_access_control_custom_params(mock_client):
    mock_client.call.return_value = {
        "OriginAccessControl": {
            "Id": "OAC2",
            "OriginAccessControlConfig": {
                "Name": "custom",
                "SigningProtocol": "sigv4",
                "SigningBehavior": "always",
                "OriginAccessControlOriginType": "s3",
            },
        },
    }
    await create_origin_access_control(
        "custom",
        signing_protocol="sigv4",
        signing_behavior="always",
        origin_type="s3",
        description="desc",
    )
    call_kwargs = mock_client.call.call_args
    config = call_kwargs[1]["OriginAccessControlConfig"]
    assert config["Description"] == "desc"


async def test_create_origin_access_control_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_origin_access_control("bad")


async def test_create_origin_access_control_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="create_origin_access_control failed"
    ):
        await create_origin_access_control("bad")


# ---------------------------------------------------------------------------
# get_origin_access_control
# ---------------------------------------------------------------------------


async def test_get_origin_access_control_success(mock_client):
    mock_client.call.return_value = {
        "OriginAccessControl": {
            "Id": "OAC1",
            "OriginAccessControlConfig": {
                "Name": "my-oac",
                "SigningProtocol": "sigv4",
                "SigningBehavior": "always",
                "OriginAccessControlOriginType": "s3",
            },
        },
    }
    result = await get_origin_access_control("OAC1")
    assert result.id == "OAC1"
    assert result.name == "my-oac"


async def test_get_origin_access_control_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_origin_access_control("OAC1")


async def test_get_origin_access_control_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="get_origin_access_control failed"
    ):
        await get_origin_access_control("OAC1")


# ---------------------------------------------------------------------------
# list_origin_access_controls
# ---------------------------------------------------------------------------


async def test_list_origin_access_controls_empty(mock_client):
    mock_client.call.return_value = {
        "OriginAccessControlList": {"Items": []},
    }
    result = await list_origin_access_controls()
    assert result == []


async def test_list_origin_access_controls_with_items(mock_client):
    mock_client.call.return_value = {
        "OriginAccessControlList": {
            "Items": [
                {
                    "Id": "OAC1",
                    "Name": "my-oac",
                    "SigningProtocol": "sigv4",
                    "SigningBehavior": "always",
                    "OriginAccessControlOriginType": "s3",
                }
            ],
        },
    }
    result = await list_origin_access_controls()
    assert len(result) == 1
    assert result[0].name == "my-oac"


async def test_list_origin_access_controls_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_origin_access_controls()


async def test_list_origin_access_controls_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(
        RuntimeError, match="list_origin_access_controls failed"
    ):
        await list_origin_access_controls()


# ---------------------------------------------------------------------------
# delete_origin_access_control
# ---------------------------------------------------------------------------


async def test_delete_origin_access_control_success(mock_client):
    mock_client.call.return_value = {}
    await delete_origin_access_control("OAC1", if_match="E1")
    mock_client.call.assert_called_once()


async def test_delete_origin_access_control_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_origin_access_control("OAC1", if_match="E1")


async def test_delete_origin_access_control_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(
        RuntimeError, match="delete_origin_access_control failed"
    ):
        await delete_origin_access_control("OAC1", if_match="E1")


# ---------------------------------------------------------------------------
# wait_for_distribution
# ---------------------------------------------------------------------------


async def test_wait_for_distribution_already_deployed(monkeypatch):
    deployed = DistributionResult(
        id="DIST1",
        arn="arn:...",
        domain_name="d1.cloudfront.net",
        status="Deployed",
    )
    monkeypatch.setattr(
        cf_mod,
        "get_distribution",
        AsyncMock(return_value=deployed),
    )
    result = await wait_for_distribution("DIST1")
    assert result.status == "Deployed"


async def test_wait_for_distribution_timeout(monkeypatch):
    in_progress = DistributionResult(
        id="DIST1",
        arn="arn:...",
        domain_name="d1.cloudfront.net",
        status="InProgress",
    )
    monkeypatch.setattr(
        cf_mod,
        "get_distribution",
        AsyncMock(return_value=in_progress),
    )
    monkeypatch.setattr("aws_util.aio.cloudfront.asyncio.sleep", AsyncMock())
    counter = {"val": 0.0}

    def fake_monotonic():
        counter["val"] += 1000.0
        return counter["val"]

    monkeypatch.setattr(time, "monotonic", fake_monotonic)
    with pytest.raises(RuntimeError, match="did not reach"):
        await wait_for_distribution("DIST1", timeout=1.0)


async def test_wait_for_distribution_polls_then_deployed(monkeypatch):
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
    monkeypatch.setattr(
        cf_mod,
        "get_distribution",
        AsyncMock(side_effect=[in_progress, deployed]),
    )
    monkeypatch.setattr("aws_util.aio.cloudfront.asyncio.sleep", AsyncMock())
    result = await wait_for_distribution("DIST1", timeout=9999.0)
    assert result.status == "Deployed"


# ---------------------------------------------------------------------------
# invalidate_and_wait
# ---------------------------------------------------------------------------


async def test_invalidate_and_wait_completed_immediately(monkeypatch):
    inv = InvalidationResult(
        id="INV1",
        distribution_id="DIST1",
        status="Completed",
        paths=["/*"],
    )
    monkeypatch.setattr(
        cf_mod,
        "create_invalidation",
        AsyncMock(return_value=inv),
    )
    monkeypatch.setattr(
        cf_mod,
        "get_invalidation",
        AsyncMock(return_value=inv),
    )
    result = await invalidate_and_wait("DIST1", paths=["/*"])
    assert result.status == "Completed"


async def test_invalidate_and_wait_timeout(monkeypatch):
    in_progress = InvalidationResult(
        id="INV1",
        distribution_id="DIST1",
        status="InProgress",
        paths=["/*"],
    )
    monkeypatch.setattr(
        cf_mod,
        "create_invalidation",
        AsyncMock(return_value=in_progress),
    )
    monkeypatch.setattr(
        cf_mod,
        "get_invalidation",
        AsyncMock(return_value=in_progress),
    )
    monkeypatch.setattr("aws_util.aio.cloudfront.asyncio.sleep", AsyncMock())
    counter = {"val": 0.0}

    def fake_monotonic():
        counter["val"] += 1000.0
        return counter["val"]

    monkeypatch.setattr(time, "monotonic", fake_monotonic)
    with pytest.raises(RuntimeError, match="did not complete"):
        await invalidate_and_wait("DIST1", paths=["/*"], timeout=1.0)


async def test_invalidate_and_wait_polls_then_completed(monkeypatch):
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
        AsyncMock(return_value=in_progress),
    )
    monkeypatch.setattr(
        cf_mod,
        "get_invalidation",
        AsyncMock(side_effect=[in_progress, completed]),
    )
    monkeypatch.setattr("aws_util.aio.cloudfront.asyncio.sleep", AsyncMock())
    result = await invalidate_and_wait("DIST1", paths=["/*"], timeout=9999.0)
    assert result.status == "Completed"


# ---------------------------------------------------------------------------
# __all__ re-exports
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


# ---------------------------------------------------------------------------
# _parse helper edge cases
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


async def test_associate_alias(mock_client):
    mock_client.call.return_value = {}
    await associate_alias("test-target_distribution_id", "test-alias", )
    mock_client.call.assert_called_once()


async def test_associate_alias_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await associate_alias("test-target_distribution_id", "test-alias", )


async def test_associate_alias_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to associate alias"):
        await associate_alias("test-target_distribution_id", "test-alias", )


async def test_associate_distribution_tenant_web_acl(mock_client):
    mock_client.call.return_value = {}
    await associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", )
    mock_client.call.assert_called_once()


async def test_associate_distribution_tenant_web_acl_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", )


async def test_associate_distribution_tenant_web_acl_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to associate distribution tenant web acl"):
        await associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", )


async def test_associate_distribution_web_acl(mock_client):
    mock_client.call.return_value = {}
    await associate_distribution_web_acl("test-id", "test-web_acl_arn", )
    mock_client.call.assert_called_once()


async def test_associate_distribution_web_acl_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await associate_distribution_web_acl("test-id", "test-web_acl_arn", )


async def test_associate_distribution_web_acl_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to associate distribution web acl"):
        await associate_distribution_web_acl("test-id", "test-web_acl_arn", )


async def test_copy_distribution(mock_client):
    mock_client.call.return_value = {}
    await copy_distribution("test-primary_distribution_id", "test-caller_reference", )
    mock_client.call.assert_called_once()


async def test_copy_distribution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await copy_distribution("test-primary_distribution_id", "test-caller_reference", )


async def test_copy_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to copy distribution"):
        await copy_distribution("test-primary_distribution_id", "test-caller_reference", )


async def test_create_anycast_ip_list(mock_client):
    mock_client.call.return_value = {}
    await create_anycast_ip_list("test-name", 1, )
    mock_client.call.assert_called_once()


async def test_create_anycast_ip_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_anycast_ip_list("test-name", 1, )


async def test_create_anycast_ip_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create anycast ip list"):
        await create_anycast_ip_list("test-name", 1, )


async def test_create_cache_policy(mock_client):
    mock_client.call.return_value = {}
    await create_cache_policy({}, )
    mock_client.call.assert_called_once()


async def test_create_cache_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_cache_policy({}, )


async def test_create_cache_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create cache policy"):
        await create_cache_policy({}, )


async def test_create_cloud_front_origin_access_identity(mock_client):
    mock_client.call.return_value = {}
    await create_cloud_front_origin_access_identity({}, )
    mock_client.call.assert_called_once()


async def test_create_cloud_front_origin_access_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_cloud_front_origin_access_identity({}, )


async def test_create_cloud_front_origin_access_identity_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create cloud front origin access identity"):
        await create_cloud_front_origin_access_identity({}, )


async def test_create_connection_group(mock_client):
    mock_client.call.return_value = {}
    await create_connection_group("test-name", )
    mock_client.call.assert_called_once()


async def test_create_connection_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_connection_group("test-name", )


async def test_create_connection_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create connection group"):
        await create_connection_group("test-name", )


async def test_create_continuous_deployment_policy(mock_client):
    mock_client.call.return_value = {}
    await create_continuous_deployment_policy({}, )
    mock_client.call.assert_called_once()


async def test_create_continuous_deployment_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_continuous_deployment_policy({}, )


async def test_create_continuous_deployment_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create continuous deployment policy"):
        await create_continuous_deployment_policy({}, )


async def test_create_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await create_distribution_tenant("test-distribution_id", "test-name", [], )
    mock_client.call.assert_called_once()


async def test_create_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_distribution_tenant("test-distribution_id", "test-name", [], )


async def test_create_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create distribution tenant"):
        await create_distribution_tenant("test-distribution_id", "test-name", [], )


async def test_create_distribution_with_tags(mock_client):
    mock_client.call.return_value = {}
    await create_distribution_with_tags({}, )
    mock_client.call.assert_called_once()


async def test_create_distribution_with_tags_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_distribution_with_tags({}, )


async def test_create_distribution_with_tags_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create distribution with tags"):
        await create_distribution_with_tags({}, )


async def test_create_field_level_encryption_config(mock_client):
    mock_client.call.return_value = {}
    await create_field_level_encryption_config({}, )
    mock_client.call.assert_called_once()


async def test_create_field_level_encryption_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_field_level_encryption_config({}, )


async def test_create_field_level_encryption_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create field level encryption config"):
        await create_field_level_encryption_config({}, )


async def test_create_field_level_encryption_profile(mock_client):
    mock_client.call.return_value = {}
    await create_field_level_encryption_profile({}, )
    mock_client.call.assert_called_once()


async def test_create_field_level_encryption_profile_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_field_level_encryption_profile({}, )


async def test_create_field_level_encryption_profile_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create field level encryption profile"):
        await create_field_level_encryption_profile({}, )


async def test_create_function(mock_client):
    mock_client.call.return_value = {}
    await create_function("test-name", {}, "test-function_code", )
    mock_client.call.assert_called_once()


async def test_create_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_function("test-name", {}, "test-function_code", )


async def test_create_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create function"):
        await create_function("test-name", {}, "test-function_code", )


async def test_create_invalidation_for_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await create_invalidation_for_distribution_tenant("test-id", {}, )
    mock_client.call.assert_called_once()


async def test_create_invalidation_for_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_invalidation_for_distribution_tenant("test-id", {}, )


async def test_create_invalidation_for_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create invalidation for distribution tenant"):
        await create_invalidation_for_distribution_tenant("test-id", {}, )


async def test_create_key_group(mock_client):
    mock_client.call.return_value = {}
    await create_key_group({}, )
    mock_client.call.assert_called_once()


async def test_create_key_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_key_group({}, )


async def test_create_key_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create key group"):
        await create_key_group({}, )


async def test_create_key_value_store(mock_client):
    mock_client.call.return_value = {}
    await create_key_value_store("test-name", )
    mock_client.call.assert_called_once()


async def test_create_key_value_store_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_key_value_store("test-name", )


async def test_create_key_value_store_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create key value store"):
        await create_key_value_store("test-name", )


async def test_create_monitoring_subscription(mock_client):
    mock_client.call.return_value = {}
    await create_monitoring_subscription("test-distribution_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_monitoring_subscription_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_monitoring_subscription("test-distribution_id", {}, )


async def test_create_monitoring_subscription_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create monitoring subscription"):
        await create_monitoring_subscription("test-distribution_id", {}, )


async def test_create_origin_request_policy(mock_client):
    mock_client.call.return_value = {}
    await create_origin_request_policy({}, )
    mock_client.call.assert_called_once()


async def test_create_origin_request_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_origin_request_policy({}, )


async def test_create_origin_request_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create origin request policy"):
        await create_origin_request_policy({}, )


async def test_create_public_key(mock_client):
    mock_client.call.return_value = {}
    await create_public_key({}, )
    mock_client.call.assert_called_once()


async def test_create_public_key_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_public_key({}, )


async def test_create_public_key_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create public key"):
        await create_public_key({}, )


async def test_create_realtime_log_config(mock_client):
    mock_client.call.return_value = {}
    await create_realtime_log_config([], [], "test-name", 1, )
    mock_client.call.assert_called_once()


async def test_create_realtime_log_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_realtime_log_config([], [], "test-name", 1, )


async def test_create_realtime_log_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create realtime log config"):
        await create_realtime_log_config([], [], "test-name", 1, )


async def test_create_response_headers_policy(mock_client):
    mock_client.call.return_value = {}
    await create_response_headers_policy({}, )
    mock_client.call.assert_called_once()


async def test_create_response_headers_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_response_headers_policy({}, )


async def test_create_response_headers_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create response headers policy"):
        await create_response_headers_policy({}, )


async def test_create_streaming_distribution(mock_client):
    mock_client.call.return_value = {}
    await create_streaming_distribution({}, )
    mock_client.call.assert_called_once()


async def test_create_streaming_distribution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_streaming_distribution({}, )


async def test_create_streaming_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create streaming distribution"):
        await create_streaming_distribution({}, )


async def test_create_streaming_distribution_with_tags(mock_client):
    mock_client.call.return_value = {}
    await create_streaming_distribution_with_tags({}, )
    mock_client.call.assert_called_once()


async def test_create_streaming_distribution_with_tags_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_streaming_distribution_with_tags({}, )


async def test_create_streaming_distribution_with_tags_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create streaming distribution with tags"):
        await create_streaming_distribution_with_tags({}, )


async def test_create_vpc_origin(mock_client):
    mock_client.call.return_value = {}
    await create_vpc_origin({}, )
    mock_client.call.assert_called_once()


async def test_create_vpc_origin_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_origin({}, )


async def test_create_vpc_origin_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create vpc origin"):
        await create_vpc_origin({}, )


async def test_delete_anycast_ip_list(mock_client):
    mock_client.call.return_value = {}
    await delete_anycast_ip_list("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_anycast_ip_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_anycast_ip_list("test-id", "test-if_match", )


async def test_delete_anycast_ip_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete anycast ip list"):
        await delete_anycast_ip_list("test-id", "test-if_match", )


async def test_delete_cache_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_cache_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_cache_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_policy("test-id", )


async def test_delete_cache_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete cache policy"):
        await delete_cache_policy("test-id", )


async def test_delete_cloud_front_origin_access_identity(mock_client):
    mock_client.call.return_value = {}
    await delete_cloud_front_origin_access_identity("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_cloud_front_origin_access_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cloud_front_origin_access_identity("test-id", )


async def test_delete_cloud_front_origin_access_identity_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete cloud front origin access identity"):
        await delete_cloud_front_origin_access_identity("test-id", )


async def test_delete_connection_group(mock_client):
    mock_client.call.return_value = {}
    await delete_connection_group("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_connection_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection_group("test-id", "test-if_match", )


async def test_delete_connection_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete connection group"):
        await delete_connection_group("test-id", "test-if_match", )


async def test_delete_continuous_deployment_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_continuous_deployment_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_continuous_deployment_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_continuous_deployment_policy("test-id", )


async def test_delete_continuous_deployment_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete continuous deployment policy"):
        await delete_continuous_deployment_policy("test-id", )


async def test_delete_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await delete_distribution_tenant("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_distribution_tenant("test-id", "test-if_match", )


async def test_delete_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete distribution tenant"):
        await delete_distribution_tenant("test-id", "test-if_match", )


async def test_delete_field_level_encryption_config(mock_client):
    mock_client.call.return_value = {}
    await delete_field_level_encryption_config("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_field_level_encryption_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_field_level_encryption_config("test-id", )


async def test_delete_field_level_encryption_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete field level encryption config"):
        await delete_field_level_encryption_config("test-id", )


async def test_delete_field_level_encryption_profile(mock_client):
    mock_client.call.return_value = {}
    await delete_field_level_encryption_profile("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_field_level_encryption_profile_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_field_level_encryption_profile("test-id", )


async def test_delete_field_level_encryption_profile_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete field level encryption profile"):
        await delete_field_level_encryption_profile("test-id", )


async def test_delete_function(mock_client):
    mock_client.call.return_value = {}
    await delete_function("test-name", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_function("test-name", "test-if_match", )


async def test_delete_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete function"):
        await delete_function("test-name", "test-if_match", )


async def test_delete_key_group(mock_client):
    mock_client.call.return_value = {}
    await delete_key_group("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_key_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_key_group("test-id", )


async def test_delete_key_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete key group"):
        await delete_key_group("test-id", )


async def test_delete_key_value_store(mock_client):
    mock_client.call.return_value = {}
    await delete_key_value_store("test-name", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_key_value_store_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_key_value_store("test-name", "test-if_match", )


async def test_delete_key_value_store_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete key value store"):
        await delete_key_value_store("test-name", "test-if_match", )


async def test_delete_monitoring_subscription(mock_client):
    mock_client.call.return_value = {}
    await delete_monitoring_subscription("test-distribution_id", )
    mock_client.call.assert_called_once()


async def test_delete_monitoring_subscription_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_monitoring_subscription("test-distribution_id", )


async def test_delete_monitoring_subscription_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete monitoring subscription"):
        await delete_monitoring_subscription("test-distribution_id", )


async def test_delete_origin_request_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_origin_request_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_origin_request_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_origin_request_policy("test-id", )


async def test_delete_origin_request_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete origin request policy"):
        await delete_origin_request_policy("test-id", )


async def test_delete_public_key(mock_client):
    mock_client.call.return_value = {}
    await delete_public_key("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_public_key_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_public_key("test-id", )


async def test_delete_public_key_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete public key"):
        await delete_public_key("test-id", )


async def test_delete_realtime_log_config(mock_client):
    mock_client.call.return_value = {}
    await delete_realtime_log_config()
    mock_client.call.assert_called_once()


async def test_delete_realtime_log_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_realtime_log_config()


async def test_delete_realtime_log_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete realtime log config"):
        await delete_realtime_log_config()


async def test_delete_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_response_headers_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_response_headers_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_response_headers_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_response_headers_policy("test-id", )


async def test_delete_response_headers_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete response headers policy"):
        await delete_response_headers_policy("test-id", )


async def test_delete_streaming_distribution(mock_client):
    mock_client.call.return_value = {}
    await delete_streaming_distribution("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_streaming_distribution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_streaming_distribution("test-id", )


async def test_delete_streaming_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete streaming distribution"):
        await delete_streaming_distribution("test-id", )


async def test_delete_vpc_origin(mock_client):
    mock_client.call.return_value = {}
    await delete_vpc_origin("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_origin_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_origin("test-id", "test-if_match", )


async def test_delete_vpc_origin_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete vpc origin"):
        await delete_vpc_origin("test-id", "test-if_match", )


async def test_describe_function(mock_client):
    mock_client.call.return_value = {}
    await describe_function("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_function("test-name", )


async def test_describe_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe function"):
        await describe_function("test-name", )


async def test_describe_key_value_store(mock_client):
    mock_client.call.return_value = {}
    await describe_key_value_store("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_key_value_store_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_key_value_store("test-name", )


async def test_describe_key_value_store_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe key value store"):
        await describe_key_value_store("test-name", )


async def test_disassociate_distribution_tenant_web_acl(mock_client):
    mock_client.call.return_value = {}
    await disassociate_distribution_tenant_web_acl("test-id", )
    mock_client.call.assert_called_once()


async def test_disassociate_distribution_tenant_web_acl_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_distribution_tenant_web_acl("test-id", )


async def test_disassociate_distribution_tenant_web_acl_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate distribution tenant web acl"):
        await disassociate_distribution_tenant_web_acl("test-id", )


async def test_disassociate_distribution_web_acl(mock_client):
    mock_client.call.return_value = {}
    await disassociate_distribution_web_acl("test-id", )
    mock_client.call.assert_called_once()


async def test_disassociate_distribution_web_acl_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_distribution_web_acl("test-id", )


async def test_disassociate_distribution_web_acl_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate distribution web acl"):
        await disassociate_distribution_web_acl("test-id", )


async def test_get_anycast_ip_list(mock_client):
    mock_client.call.return_value = {}
    await get_anycast_ip_list("test-id", )
    mock_client.call.assert_called_once()


async def test_get_anycast_ip_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_anycast_ip_list("test-id", )


async def test_get_anycast_ip_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get anycast ip list"):
        await get_anycast_ip_list("test-id", )


async def test_get_cache_policy(mock_client):
    mock_client.call.return_value = {}
    await get_cache_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_get_cache_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_cache_policy("test-id", )


async def test_get_cache_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get cache policy"):
        await get_cache_policy("test-id", )


async def test_get_cache_policy_config(mock_client):
    mock_client.call.return_value = {}
    await get_cache_policy_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_cache_policy_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_cache_policy_config("test-id", )


async def test_get_cache_policy_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get cache policy config"):
        await get_cache_policy_config("test-id", )


async def test_get_cloud_front_origin_access_identity(mock_client):
    mock_client.call.return_value = {}
    await get_cloud_front_origin_access_identity("test-id", )
    mock_client.call.assert_called_once()


async def test_get_cloud_front_origin_access_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_cloud_front_origin_access_identity("test-id", )


async def test_get_cloud_front_origin_access_identity_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get cloud front origin access identity"):
        await get_cloud_front_origin_access_identity("test-id", )


async def test_get_cloud_front_origin_access_identity_config(mock_client):
    mock_client.call.return_value = {}
    await get_cloud_front_origin_access_identity_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_cloud_front_origin_access_identity_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_cloud_front_origin_access_identity_config("test-id", )


async def test_get_cloud_front_origin_access_identity_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get cloud front origin access identity config"):
        await get_cloud_front_origin_access_identity_config("test-id", )


async def test_get_connection_group(mock_client):
    mock_client.call.return_value = {}
    await get_connection_group("test-identifier", )
    mock_client.call.assert_called_once()


async def test_get_connection_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_connection_group("test-identifier", )


async def test_get_connection_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get connection group"):
        await get_connection_group("test-identifier", )


async def test_get_connection_group_by_routing_endpoint(mock_client):
    mock_client.call.return_value = {}
    await get_connection_group_by_routing_endpoint("test-routing_endpoint", )
    mock_client.call.assert_called_once()


async def test_get_connection_group_by_routing_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_connection_group_by_routing_endpoint("test-routing_endpoint", )


async def test_get_connection_group_by_routing_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get connection group by routing endpoint"):
        await get_connection_group_by_routing_endpoint("test-routing_endpoint", )


async def test_get_continuous_deployment_policy(mock_client):
    mock_client.call.return_value = {}
    await get_continuous_deployment_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_get_continuous_deployment_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_continuous_deployment_policy("test-id", )


async def test_get_continuous_deployment_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get continuous deployment policy"):
        await get_continuous_deployment_policy("test-id", )


async def test_get_continuous_deployment_policy_config(mock_client):
    mock_client.call.return_value = {}
    await get_continuous_deployment_policy_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_continuous_deployment_policy_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_continuous_deployment_policy_config("test-id", )


async def test_get_continuous_deployment_policy_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get continuous deployment policy config"):
        await get_continuous_deployment_policy_config("test-id", )


async def test_get_distribution_config(mock_client):
    mock_client.call.return_value = {}
    await get_distribution_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_distribution_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_config("test-id", )


async def test_get_distribution_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get distribution config"):
        await get_distribution_config("test-id", )


async def test_get_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await get_distribution_tenant("test-identifier", )
    mock_client.call.assert_called_once()


async def test_get_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_tenant("test-identifier", )


async def test_get_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get distribution tenant"):
        await get_distribution_tenant("test-identifier", )


async def test_get_distribution_tenant_by_domain(mock_client):
    mock_client.call.return_value = {}
    await get_distribution_tenant_by_domain("test-domain", )
    mock_client.call.assert_called_once()


async def test_get_distribution_tenant_by_domain_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_tenant_by_domain("test-domain", )


async def test_get_distribution_tenant_by_domain_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get distribution tenant by domain"):
        await get_distribution_tenant_by_domain("test-domain", )


async def test_get_field_level_encryption(mock_client):
    mock_client.call.return_value = {}
    await get_field_level_encryption("test-id", )
    mock_client.call.assert_called_once()


async def test_get_field_level_encryption_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_field_level_encryption("test-id", )


async def test_get_field_level_encryption_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get field level encryption"):
        await get_field_level_encryption("test-id", )


async def test_get_field_level_encryption_config(mock_client):
    mock_client.call.return_value = {}
    await get_field_level_encryption_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_field_level_encryption_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_field_level_encryption_config("test-id", )


async def test_get_field_level_encryption_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get field level encryption config"):
        await get_field_level_encryption_config("test-id", )


async def test_get_field_level_encryption_profile(mock_client):
    mock_client.call.return_value = {}
    await get_field_level_encryption_profile("test-id", )
    mock_client.call.assert_called_once()


async def test_get_field_level_encryption_profile_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_field_level_encryption_profile("test-id", )


async def test_get_field_level_encryption_profile_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get field level encryption profile"):
        await get_field_level_encryption_profile("test-id", )


async def test_get_field_level_encryption_profile_config(mock_client):
    mock_client.call.return_value = {}
    await get_field_level_encryption_profile_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_field_level_encryption_profile_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_field_level_encryption_profile_config("test-id", )


async def test_get_field_level_encryption_profile_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get field level encryption profile config"):
        await get_field_level_encryption_profile_config("test-id", )


async def test_get_function(mock_client):
    mock_client.call.return_value = {}
    await get_function("test-name", )
    mock_client.call.assert_called_once()


async def test_get_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_function("test-name", )


async def test_get_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get function"):
        await get_function("test-name", )


async def test_get_invalidation_for_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await get_invalidation_for_distribution_tenant("test-distribution_tenant_id", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_invalidation_for_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_invalidation_for_distribution_tenant("test-distribution_tenant_id", "test-id", )


async def test_get_invalidation_for_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get invalidation for distribution tenant"):
        await get_invalidation_for_distribution_tenant("test-distribution_tenant_id", "test-id", )


async def test_get_key_group(mock_client):
    mock_client.call.return_value = {}
    await get_key_group("test-id", )
    mock_client.call.assert_called_once()


async def test_get_key_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_group("test-id", )


async def test_get_key_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get key group"):
        await get_key_group("test-id", )


async def test_get_key_group_config(mock_client):
    mock_client.call.return_value = {}
    await get_key_group_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_key_group_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_group_config("test-id", )


async def test_get_key_group_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get key group config"):
        await get_key_group_config("test-id", )


async def test_get_managed_certificate_details(mock_client):
    mock_client.call.return_value = {}
    await get_managed_certificate_details("test-identifier", )
    mock_client.call.assert_called_once()


async def test_get_managed_certificate_details_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_managed_certificate_details("test-identifier", )


async def test_get_managed_certificate_details_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get managed certificate details"):
        await get_managed_certificate_details("test-identifier", )


async def test_get_monitoring_subscription(mock_client):
    mock_client.call.return_value = {}
    await get_monitoring_subscription("test-distribution_id", )
    mock_client.call.assert_called_once()


async def test_get_monitoring_subscription_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_monitoring_subscription("test-distribution_id", )


async def test_get_monitoring_subscription_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get monitoring subscription"):
        await get_monitoring_subscription("test-distribution_id", )


async def test_get_origin_access_control_config(mock_client):
    mock_client.call.return_value = {}
    await get_origin_access_control_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_origin_access_control_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_origin_access_control_config("test-id", )


async def test_get_origin_access_control_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get origin access control config"):
        await get_origin_access_control_config("test-id", )


async def test_get_origin_request_policy(mock_client):
    mock_client.call.return_value = {}
    await get_origin_request_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_get_origin_request_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_origin_request_policy("test-id", )


async def test_get_origin_request_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get origin request policy"):
        await get_origin_request_policy("test-id", )


async def test_get_origin_request_policy_config(mock_client):
    mock_client.call.return_value = {}
    await get_origin_request_policy_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_origin_request_policy_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_origin_request_policy_config("test-id", )


async def test_get_origin_request_policy_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get origin request policy config"):
        await get_origin_request_policy_config("test-id", )


async def test_get_public_key(mock_client):
    mock_client.call.return_value = {}
    await get_public_key("test-id", )
    mock_client.call.assert_called_once()


async def test_get_public_key_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_public_key("test-id", )


async def test_get_public_key_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get public key"):
        await get_public_key("test-id", )


async def test_get_public_key_config(mock_client):
    mock_client.call.return_value = {}
    await get_public_key_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_public_key_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_public_key_config("test-id", )


async def test_get_public_key_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get public key config"):
        await get_public_key_config("test-id", )


async def test_get_realtime_log_config(mock_client):
    mock_client.call.return_value = {}
    await get_realtime_log_config()
    mock_client.call.assert_called_once()


async def test_get_realtime_log_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_realtime_log_config()


async def test_get_realtime_log_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get realtime log config"):
        await get_realtime_log_config()


async def test_get_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_get_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        await get_resource_policy("test-resource_arn", )


async def test_get_response_headers_policy(mock_client):
    mock_client.call.return_value = {}
    await get_response_headers_policy("test-id", )
    mock_client.call.assert_called_once()


async def test_get_response_headers_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_response_headers_policy("test-id", )


async def test_get_response_headers_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get response headers policy"):
        await get_response_headers_policy("test-id", )


async def test_get_response_headers_policy_config(mock_client):
    mock_client.call.return_value = {}
    await get_response_headers_policy_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_response_headers_policy_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_response_headers_policy_config("test-id", )


async def test_get_response_headers_policy_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get response headers policy config"):
        await get_response_headers_policy_config("test-id", )


async def test_get_streaming_distribution(mock_client):
    mock_client.call.return_value = {}
    await get_streaming_distribution("test-id", )
    mock_client.call.assert_called_once()


async def test_get_streaming_distribution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_streaming_distribution("test-id", )


async def test_get_streaming_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get streaming distribution"):
        await get_streaming_distribution("test-id", )


async def test_get_streaming_distribution_config(mock_client):
    mock_client.call.return_value = {}
    await get_streaming_distribution_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_streaming_distribution_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_streaming_distribution_config("test-id", )


async def test_get_streaming_distribution_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get streaming distribution config"):
        await get_streaming_distribution_config("test-id", )


async def test_get_vpc_origin(mock_client):
    mock_client.call.return_value = {}
    await get_vpc_origin("test-id", )
    mock_client.call.assert_called_once()


async def test_get_vpc_origin_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_vpc_origin("test-id", )


async def test_get_vpc_origin_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get vpc origin"):
        await get_vpc_origin("test-id", )


async def test_list_anycast_ip_lists(mock_client):
    mock_client.call.return_value = {}
    await list_anycast_ip_lists()
    mock_client.call.assert_called_once()


async def test_list_anycast_ip_lists_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_anycast_ip_lists()


async def test_list_anycast_ip_lists_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list anycast ip lists"):
        await list_anycast_ip_lists()


async def test_list_cache_policies(mock_client):
    mock_client.call.return_value = {}
    await list_cache_policies()
    mock_client.call.assert_called_once()


async def test_list_cache_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_cache_policies()


async def test_list_cache_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list cache policies"):
        await list_cache_policies()


async def test_list_cloud_front_origin_access_identities(mock_client):
    mock_client.call.return_value = {}
    await list_cloud_front_origin_access_identities()
    mock_client.call.assert_called_once()


async def test_list_cloud_front_origin_access_identities_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_cloud_front_origin_access_identities()


async def test_list_cloud_front_origin_access_identities_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list cloud front origin access identities"):
        await list_cloud_front_origin_access_identities()


async def test_list_conflicting_aliases(mock_client):
    mock_client.call.return_value = {}
    await list_conflicting_aliases("test-distribution_id", "test-alias", )
    mock_client.call.assert_called_once()


async def test_list_conflicting_aliases_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_conflicting_aliases("test-distribution_id", "test-alias", )


async def test_list_conflicting_aliases_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list conflicting aliases"):
        await list_conflicting_aliases("test-distribution_id", "test-alias", )


async def test_list_connection_groups(mock_client):
    mock_client.call.return_value = {}
    await list_connection_groups()
    mock_client.call.assert_called_once()


async def test_list_connection_groups_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_connection_groups()


async def test_list_connection_groups_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list connection groups"):
        await list_connection_groups()


async def test_list_continuous_deployment_policies(mock_client):
    mock_client.call.return_value = {}
    await list_continuous_deployment_policies()
    mock_client.call.assert_called_once()


async def test_list_continuous_deployment_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_continuous_deployment_policies()


async def test_list_continuous_deployment_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list continuous deployment policies"):
        await list_continuous_deployment_policies()


async def test_list_distribution_tenants(mock_client):
    mock_client.call.return_value = {}
    await list_distribution_tenants()
    mock_client.call.assert_called_once()


async def test_list_distribution_tenants_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distribution_tenants()


async def test_list_distribution_tenants_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distribution tenants"):
        await list_distribution_tenants()


async def test_list_distribution_tenants_by_customization(mock_client):
    mock_client.call.return_value = {}
    await list_distribution_tenants_by_customization()
    mock_client.call.assert_called_once()


async def test_list_distribution_tenants_by_customization_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distribution_tenants_by_customization()


async def test_list_distribution_tenants_by_customization_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distribution tenants by customization"):
        await list_distribution_tenants_by_customization()


async def test_list_distributions_by_anycast_ip_list_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_anycast_ip_list_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", )


async def test_list_distributions_by_anycast_ip_list_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by anycast ip list id"):
        await list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", )


async def test_list_distributions_by_cache_policy_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_cache_policy_id("test-cache_policy_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_cache_policy_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_cache_policy_id("test-cache_policy_id", )


async def test_list_distributions_by_cache_policy_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by cache policy id"):
        await list_distributions_by_cache_policy_id("test-cache_policy_id", )


async def test_list_distributions_by_connection_mode(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_connection_mode("test-connection_mode", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_connection_mode_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_connection_mode("test-connection_mode", )


async def test_list_distributions_by_connection_mode_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by connection mode"):
        await list_distributions_by_connection_mode("test-connection_mode", )


async def test_list_distributions_by_key_group(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_key_group("test-key_group_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_key_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_key_group("test-key_group_id", )


async def test_list_distributions_by_key_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by key group"):
        await list_distributions_by_key_group("test-key_group_id", )


async def test_list_distributions_by_origin_request_policy_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_origin_request_policy_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", )


async def test_list_distributions_by_origin_request_policy_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by origin request policy id"):
        await list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", )


async def test_list_distributions_by_owned_resource(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_owned_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_owned_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_owned_resource("test-resource_arn", )


async def test_list_distributions_by_owned_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by owned resource"):
        await list_distributions_by_owned_resource("test-resource_arn", )


async def test_list_distributions_by_realtime_log_config(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_realtime_log_config()
    mock_client.call.assert_called_once()


async def test_list_distributions_by_realtime_log_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_realtime_log_config()


async def test_list_distributions_by_realtime_log_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by realtime log config"):
        await list_distributions_by_realtime_log_config()


async def test_list_distributions_by_response_headers_policy_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_response_headers_policy_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", )


async def test_list_distributions_by_response_headers_policy_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by response headers policy id"):
        await list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", )


async def test_list_distributions_by_vpc_origin_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_vpc_origin_id("test-vpc_origin_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_vpc_origin_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_vpc_origin_id("test-vpc_origin_id", )


async def test_list_distributions_by_vpc_origin_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by vpc origin id"):
        await list_distributions_by_vpc_origin_id("test-vpc_origin_id", )


async def test_list_distributions_by_web_acl_id(mock_client):
    mock_client.call.return_value = {}
    await list_distributions_by_web_acl_id("test-web_acl_id", )
    mock_client.call.assert_called_once()


async def test_list_distributions_by_web_acl_id_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_distributions_by_web_acl_id("test-web_acl_id", )


async def test_list_distributions_by_web_acl_id_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list distributions by web acl id"):
        await list_distributions_by_web_acl_id("test-web_acl_id", )


async def test_list_domain_conflicts(mock_client):
    mock_client.call.return_value = {}
    await list_domain_conflicts("test-domain", {}, )
    mock_client.call.assert_called_once()


async def test_list_domain_conflicts_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_domain_conflicts("test-domain", {}, )


async def test_list_domain_conflicts_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list domain conflicts"):
        await list_domain_conflicts("test-domain", {}, )


async def test_list_field_level_encryption_configs(mock_client):
    mock_client.call.return_value = {}
    await list_field_level_encryption_configs()
    mock_client.call.assert_called_once()


async def test_list_field_level_encryption_configs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_field_level_encryption_configs()


async def test_list_field_level_encryption_configs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list field level encryption configs"):
        await list_field_level_encryption_configs()


async def test_list_field_level_encryption_profiles(mock_client):
    mock_client.call.return_value = {}
    await list_field_level_encryption_profiles()
    mock_client.call.assert_called_once()


async def test_list_field_level_encryption_profiles_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_field_level_encryption_profiles()


async def test_list_field_level_encryption_profiles_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list field level encryption profiles"):
        await list_field_level_encryption_profiles()


async def test_list_functions(mock_client):
    mock_client.call.return_value = {}
    await list_functions()
    mock_client.call.assert_called_once()


async def test_list_functions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_functions()


async def test_list_functions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list functions"):
        await list_functions()


async def test_list_invalidations_for_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await list_invalidations_for_distribution_tenant("test-id", )
    mock_client.call.assert_called_once()


async def test_list_invalidations_for_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_invalidations_for_distribution_tenant("test-id", )


async def test_list_invalidations_for_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list invalidations for distribution tenant"):
        await list_invalidations_for_distribution_tenant("test-id", )


async def test_list_key_groups(mock_client):
    mock_client.call.return_value = {}
    await list_key_groups()
    mock_client.call.assert_called_once()


async def test_list_key_groups_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_key_groups()


async def test_list_key_groups_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list key groups"):
        await list_key_groups()


async def test_list_key_value_stores(mock_client):
    mock_client.call.return_value = {}
    await list_key_value_stores()
    mock_client.call.assert_called_once()


async def test_list_key_value_stores_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_key_value_stores()


async def test_list_key_value_stores_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list key value stores"):
        await list_key_value_stores()


async def test_list_origin_request_policies(mock_client):
    mock_client.call.return_value = {}
    await list_origin_request_policies()
    mock_client.call.assert_called_once()


async def test_list_origin_request_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_origin_request_policies()


async def test_list_origin_request_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list origin request policies"):
        await list_origin_request_policies()


async def test_list_public_keys(mock_client):
    mock_client.call.return_value = {}
    await list_public_keys()
    mock_client.call.assert_called_once()


async def test_list_public_keys_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_public_keys()


async def test_list_public_keys_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list public keys"):
        await list_public_keys()


async def test_list_realtime_log_configs(mock_client):
    mock_client.call.return_value = {}
    await list_realtime_log_configs()
    mock_client.call.assert_called_once()


async def test_list_realtime_log_configs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_realtime_log_configs()


async def test_list_realtime_log_configs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list realtime log configs"):
        await list_realtime_log_configs()


async def test_list_response_headers_policies(mock_client):
    mock_client.call.return_value = {}
    await list_response_headers_policies()
    mock_client.call.assert_called_once()


async def test_list_response_headers_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_response_headers_policies()


async def test_list_response_headers_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list response headers policies"):
        await list_response_headers_policies()


async def test_list_streaming_distributions(mock_client):
    mock_client.call.return_value = {}
    await list_streaming_distributions()
    mock_client.call.assert_called_once()


async def test_list_streaming_distributions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_streaming_distributions()


async def test_list_streaming_distributions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list streaming distributions"):
        await list_streaming_distributions()


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource", )


async def test_list_vpc_origins(mock_client):
    mock_client.call.return_value = {}
    await list_vpc_origins()
    mock_client.call.assert_called_once()


async def test_list_vpc_origins_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_origins()


async def test_list_vpc_origins_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list vpc origins"):
        await list_vpc_origins()


async def test_publish_function(mock_client):
    mock_client.call.return_value = {}
    await publish_function("test-name", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_publish_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await publish_function("test-name", "test-if_match", )


async def test_publish_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to publish function"):
        await publish_function("test-name", "test-if_match", )


async def test_put_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await put_resource_policy("test-resource_arn", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy_document", )


async def test_put_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        await put_resource_policy("test-resource_arn", "test-policy_document", )


async def test_run_function(mock_client):
    mock_client.call.return_value = {}
    await run_function("test-name", "test-if_match", "test-event_object", )
    mock_client.call.assert_called_once()


async def test_run_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await run_function("test-name", "test-if_match", "test-event_object", )


async def test_run_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to run function"):
        await run_function("test-name", "test-if_match", "test-event_object", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource", {}, )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource", {}, )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource", {}, )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource", {}, )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource", {}, )


async def test_update_anycast_ip_list(mock_client):
    mock_client.call.return_value = {}
    await update_anycast_ip_list("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_update_anycast_ip_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_anycast_ip_list("test-id", "test-if_match", )


async def test_update_anycast_ip_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update anycast ip list"):
        await update_anycast_ip_list("test-id", "test-if_match", )


async def test_update_cache_policy(mock_client):
    mock_client.call.return_value = {}
    await update_cache_policy({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_cache_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_cache_policy({}, "test-id", )


async def test_update_cache_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update cache policy"):
        await update_cache_policy({}, "test-id", )


async def test_update_cloud_front_origin_access_identity(mock_client):
    mock_client.call.return_value = {}
    await update_cloud_front_origin_access_identity({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_cloud_front_origin_access_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_cloud_front_origin_access_identity({}, "test-id", )


async def test_update_cloud_front_origin_access_identity_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update cloud front origin access identity"):
        await update_cloud_front_origin_access_identity({}, "test-id", )


async def test_update_connection_group(mock_client):
    mock_client.call.return_value = {}
    await update_connection_group("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_update_connection_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_connection_group("test-id", "test-if_match", )


async def test_update_connection_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update connection group"):
        await update_connection_group("test-id", "test-if_match", )


async def test_update_continuous_deployment_policy(mock_client):
    mock_client.call.return_value = {}
    await update_continuous_deployment_policy({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_continuous_deployment_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_continuous_deployment_policy({}, "test-id", )


async def test_update_continuous_deployment_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update continuous deployment policy"):
        await update_continuous_deployment_policy({}, "test-id", )


async def test_update_distribution_tenant(mock_client):
    mock_client.call.return_value = {}
    await update_distribution_tenant("test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_update_distribution_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_distribution_tenant("test-id", "test-if_match", )


async def test_update_distribution_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update distribution tenant"):
        await update_distribution_tenant("test-id", "test-if_match", )


async def test_update_distribution_with_staging_config(mock_client):
    mock_client.call.return_value = {}
    await update_distribution_with_staging_config("test-id", )
    mock_client.call.assert_called_once()


async def test_update_distribution_with_staging_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_distribution_with_staging_config("test-id", )


async def test_update_distribution_with_staging_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update distribution with staging config"):
        await update_distribution_with_staging_config("test-id", )


async def test_update_domain_association(mock_client):
    mock_client.call.return_value = {}
    await update_domain_association("test-domain", {}, )
    mock_client.call.assert_called_once()


async def test_update_domain_association_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_domain_association("test-domain", {}, )


async def test_update_domain_association_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update domain association"):
        await update_domain_association("test-domain", {}, )


async def test_update_field_level_encryption_config(mock_client):
    mock_client.call.return_value = {}
    await update_field_level_encryption_config({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_field_level_encryption_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_field_level_encryption_config({}, "test-id", )


async def test_update_field_level_encryption_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update field level encryption config"):
        await update_field_level_encryption_config({}, "test-id", )


async def test_update_field_level_encryption_profile(mock_client):
    mock_client.call.return_value = {}
    await update_field_level_encryption_profile({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_field_level_encryption_profile_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_field_level_encryption_profile({}, "test-id", )


async def test_update_field_level_encryption_profile_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update field level encryption profile"):
        await update_field_level_encryption_profile({}, "test-id", )


async def test_update_function(mock_client):
    mock_client.call.return_value = {}
    await update_function("test-name", "test-if_match", {}, "test-function_code", )
    mock_client.call.assert_called_once()


async def test_update_function_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_function("test-name", "test-if_match", {}, "test-function_code", )


async def test_update_function_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update function"):
        await update_function("test-name", "test-if_match", {}, "test-function_code", )


async def test_update_key_group(mock_client):
    mock_client.call.return_value = {}
    await update_key_group({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_key_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_key_group({}, "test-id", )


async def test_update_key_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update key group"):
        await update_key_group({}, "test-id", )


async def test_update_key_value_store(mock_client):
    mock_client.call.return_value = {}
    await update_key_value_store("test-name", "test-comment", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_update_key_value_store_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_key_value_store("test-name", "test-comment", "test-if_match", )


async def test_update_key_value_store_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update key value store"):
        await update_key_value_store("test-name", "test-comment", "test-if_match", )


async def test_update_origin_access_control(mock_client):
    mock_client.call.return_value = {}
    await update_origin_access_control({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_origin_access_control_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_origin_access_control({}, "test-id", )


async def test_update_origin_access_control_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update origin access control"):
        await update_origin_access_control({}, "test-id", )


async def test_update_origin_request_policy(mock_client):
    mock_client.call.return_value = {}
    await update_origin_request_policy({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_origin_request_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_origin_request_policy({}, "test-id", )


async def test_update_origin_request_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update origin request policy"):
        await update_origin_request_policy({}, "test-id", )


async def test_update_public_key(mock_client):
    mock_client.call.return_value = {}
    await update_public_key({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_public_key_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_public_key({}, "test-id", )


async def test_update_public_key_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update public key"):
        await update_public_key({}, "test-id", )


async def test_update_realtime_log_config(mock_client):
    mock_client.call.return_value = {}
    await update_realtime_log_config()
    mock_client.call.assert_called_once()


async def test_update_realtime_log_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_realtime_log_config()


async def test_update_realtime_log_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update realtime log config"):
        await update_realtime_log_config()


async def test_update_response_headers_policy(mock_client):
    mock_client.call.return_value = {}
    await update_response_headers_policy({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_response_headers_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_response_headers_policy({}, "test-id", )


async def test_update_response_headers_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update response headers policy"):
        await update_response_headers_policy({}, "test-id", )


async def test_update_streaming_distribution(mock_client):
    mock_client.call.return_value = {}
    await update_streaming_distribution({}, "test-id", )
    mock_client.call.assert_called_once()


async def test_update_streaming_distribution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_streaming_distribution({}, "test-id", )


async def test_update_streaming_distribution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update streaming distribution"):
        await update_streaming_distribution({}, "test-id", )


async def test_update_vpc_origin(mock_client):
    mock_client.call.return_value = {}
    await update_vpc_origin({}, "test-id", "test-if_match", )
    mock_client.call.assert_called_once()


async def test_update_vpc_origin_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_vpc_origin({}, "test-id", "test-if_match", )


async def test_update_vpc_origin_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update vpc origin"):
        await update_vpc_origin({}, "test-id", "test-if_match", )


async def test_verify_dns_configuration(mock_client):
    mock_client.call.return_value = {}
    await verify_dns_configuration("test-identifier", )
    mock_client.call.assert_called_once()


async def test_verify_dns_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await verify_dns_configuration("test-identifier", )


async def test_verify_dns_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to verify dns configuration"):
        await verify_dns_configuration("test-identifier", )


@pytest.mark.asyncio
async def test_associate_distribution_tenant_web_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import associate_distribution_tenant_web_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await associate_distribution_tenant_web_acl("test-id", "test-web_acl_arn", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_distribution_web_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import associate_distribution_web_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await associate_distribution_web_acl("test-id", "test-web_acl_arn", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import copy_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await copy_distribution("test-primary_distribution_id", "test-caller_reference", staging="test-staging", if_match="test-if_match", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_anycast_ip_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import create_anycast_ip_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await create_anycast_ip_list("test-name", 1, tags=[{"Key": "k", "Value": "v"}], ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_connection_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import create_connection_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await create_connection_group("test-name", ipv6_enabled="test-ipv6_enabled", tags=[{"Key": "k", "Value": "v"}], anycast_ip_list_id="test-anycast_ip_list_id", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import create_distribution_tenant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await create_distribution_tenant("test-distribution_id", "test-name", "test-domains", tags=[{"Key": "k", "Value": "v"}], customizations="test-customizations", parameters="test-parameters", connection_group_id="test-connection_group_id", managed_certificate_request="test-managed_certificate_request", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_key_value_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import create_key_value_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await create_key_value_store("test-name", comment="test-comment", import_source=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_origin_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import create_vpc_origin
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await create_vpc_origin({}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_cache_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_cache_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_cache_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_cloud_front_origin_access_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_cloud_front_origin_access_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_cloud_front_origin_access_identity("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_continuous_deployment_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_continuous_deployment_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_continuous_deployment_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_field_level_encryption_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_field_level_encryption_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_field_level_encryption_config("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_field_level_encryption_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_field_level_encryption_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_field_level_encryption_profile("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_key_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_key_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_key_group("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_origin_request_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_origin_request_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_origin_request_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_public_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_public_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_public_key("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_realtime_log_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_realtime_log_config(name="test-name", arn="test-arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_response_headers_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_response_headers_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_response_headers_policy("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_streaming_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import delete_streaming_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await delete_streaming_distribution("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import describe_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await describe_function("test-name", stage="test-stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_distribution_tenant_web_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import disassociate_distribution_tenant_web_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await disassociate_distribution_tenant_web_acl("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_distribution_web_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import disassociate_distribution_web_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await disassociate_distribution_web_acl("test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import get_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await get_function("test-name", stage="test-stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import get_realtime_log_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await get_realtime_log_config(name="test-name", arn="test-arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_anycast_ip_lists_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_anycast_ip_lists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_anycast_ip_lists(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cache_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_cache_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_cache_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cloud_front_origin_access_identities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_cloud_front_origin_access_identities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_cloud_front_origin_access_identities(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_conflicting_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_conflicting_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_conflicting_aliases("test-distribution_id", "test-alias", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_connection_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_connection_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_connection_groups(association_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_continuous_deployment_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_continuous_deployment_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_continuous_deployment_policies(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distribution_tenants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distribution_tenants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distribution_tenants(association_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distribution_tenants_by_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distribution_tenants_by_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distribution_tenants_by_customization(web_acl_arn="test-web_acl_arn", certificate_arn="test-certificate_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_anycast_ip_list_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_anycast_ip_list_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_anycast_ip_list_id("test-anycast_ip_list_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_cache_policy_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_cache_policy_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_cache_policy_id("test-cache_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_connection_mode_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_connection_mode
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_connection_mode("test-connection_mode", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_key_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_key_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_key_group("test-key_group_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_origin_request_policy_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_origin_request_policy_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_origin_request_policy_id("test-origin_request_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_owned_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_owned_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_owned_resource("test-resource_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_realtime_log_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_realtime_log_config(marker="test-marker", max_items=1, realtime_log_config_name={}, realtime_log_config_arn={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_response_headers_policy_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_response_headers_policy_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_response_headers_policy_id("test-response_headers_policy_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_vpc_origin_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_vpc_origin_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_vpc_origin_id("test-vpc_origin_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_distributions_by_web_acl_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_distributions_by_web_acl_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_distributions_by_web_acl_id("test-web_acl_id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_domain_conflicts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_domain_conflicts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_domain_conflicts("test-domain", "test-domain_control_validation_resource", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_field_level_encryption_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_field_level_encryption_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_field_level_encryption_configs(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_field_level_encryption_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_field_level_encryption_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_field_level_encryption_profiles(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_functions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_functions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_functions(marker="test-marker", max_items=1, stage="test-stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invalidations_for_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_invalidations_for_distribution_tenant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_invalidations_for_distribution_tenant("test-id", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_key_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_key_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_key_groups(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_key_value_stores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_key_value_stores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_key_value_stores(marker="test-marker", max_items=1, status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_origin_request_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_origin_request_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_origin_request_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_public_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_public_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_public_keys(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_realtime_log_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_realtime_log_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_realtime_log_configs(max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_response_headers_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_response_headers_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_response_headers_policies(type_value="test-type_value", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_streaming_distributions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_streaming_distributions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_streaming_distributions(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_origins_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import list_vpc_origins
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await list_vpc_origins(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import run_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await run_function("test-name", "test-if_match", "test-event_object", stage="test-stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_anycast_ip_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_anycast_ip_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_anycast_ip_list("test-id", "test-if_match", ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_cache_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_cache_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_cache_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_cloud_front_origin_access_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_cloud_front_origin_access_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_cloud_front_origin_access_identity({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_connection_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_connection_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_connection_group("test-id", "test-if_match", ipv6_enabled="test-ipv6_enabled", anycast_ip_list_id="test-anycast_ip_list_id", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_continuous_deployment_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_continuous_deployment_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_continuous_deployment_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_distribution_tenant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_distribution_tenant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_distribution_tenant("test-id", "test-if_match", distribution_id="test-distribution_id", domains="test-domains", customizations="test-customizations", parameters="test-parameters", connection_group_id="test-connection_group_id", managed_certificate_request="test-managed_certificate_request", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_distribution_with_staging_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_distribution_with_staging_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_distribution_with_staging_config("test-id", staging_distribution_id="test-staging_distribution_id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_domain_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_domain_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_domain_association("test-domain", "test-target_resource", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_field_level_encryption_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_field_level_encryption_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_field_level_encryption_config({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_field_level_encryption_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_field_level_encryption_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_field_level_encryption_profile({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_key_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_key_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_key_group({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_origin_access_control_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_origin_access_control
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_origin_access_control({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_origin_request_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_origin_request_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_origin_request_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_public_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_public_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_public_key({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_realtime_log_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_realtime_log_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_realtime_log_config(end_points="test-end_points", fields="test-fields", name="test-name", arn="test-arn", sampling_rate="test-sampling_rate", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_response_headers_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_response_headers_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_response_headers_policy({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_streaming_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import update_streaming_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await update_streaming_distribution({}, "test-id", if_match="test-if_match", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_verify_dns_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudfront import verify_dns_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudfront.async_client", lambda *a, **kw: mock_client)
    await verify_dns_configuration("test-identifier", domain="test-domain", region_name="us-east-1")
    mock_client.call.assert_called_once()
