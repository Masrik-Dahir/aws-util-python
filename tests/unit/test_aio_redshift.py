"""Tests for aws_util.aio.redshift -- 100% line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.redshift import (
    ClusterResult,
    LoggingStatus,
    ParameterGroupResult,
    SnapshotResult,
    SubnetGroupResult,
    create_cluster,
    create_cluster_parameter_group,
    create_cluster_snapshot,
    create_cluster_subnet_group,
    delete_cluster,
    delete_cluster_snapshot,
    describe_cluster_snapshots,
    describe_clusters,
    describe_logging_status,
    disable_logging,
    enable_logging,
    modify_cluster,
    reboot_cluster,
    restore_from_cluster_snapshot,
    wait_for_cluster,
    accept_reserved_node_exchange,
    add_partner,
    associate_data_share_consumer,
    authorize_cluster_security_group_ingress,
    authorize_data_share,
    authorize_endpoint_access,
    authorize_snapshot_access,
    batch_delete_cluster_snapshots,
    batch_modify_cluster_snapshots,
    cancel_resize,
    copy_cluster_snapshot,
    create_authentication_profile,
    create_cluster_security_group,
    create_custom_domain_association,
    create_endpoint_access,
    create_event_subscription,
    create_hsm_client_certificate,
    create_hsm_configuration,
    create_integration,
    create_redshift_idc_application,
    create_scheduled_action,
    create_snapshot_copy_grant,
    create_snapshot_schedule,
    create_tags,
    create_usage_limit,
    deauthorize_data_share,
    delete_authentication_profile,
    delete_cluster_parameter_group,
    delete_cluster_security_group,
    delete_cluster_subnet_group,
    delete_custom_domain_association,
    delete_endpoint_access,
    delete_event_subscription,
    delete_hsm_client_certificate,
    delete_hsm_configuration,
    delete_integration,
    delete_partner,
    delete_redshift_idc_application,
    delete_resource_policy,
    delete_scheduled_action,
    delete_snapshot_copy_grant,
    delete_snapshot_schedule,
    delete_tags,
    delete_usage_limit,
    deregister_namespace,
    describe_account_attributes,
    describe_authentication_profiles,
    describe_cluster_db_revisions,
    describe_cluster_parameter_groups,
    describe_cluster_parameters,
    describe_cluster_security_groups,
    describe_cluster_subnet_groups,
    describe_cluster_tracks,
    describe_cluster_versions,
    describe_custom_domain_associations,
    describe_data_shares,
    describe_data_shares_for_consumer,
    describe_data_shares_for_producer,
    describe_default_cluster_parameters,
    describe_endpoint_access,
    describe_endpoint_authorization,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_hsm_client_certificates,
    describe_hsm_configurations,
    describe_inbound_integrations,
    describe_integrations,
    describe_node_configuration_options,
    describe_orderable_cluster_options,
    describe_partners,
    describe_redshift_idc_applications,
    describe_reserved_node_exchange_status,
    describe_reserved_node_offerings,
    describe_reserved_nodes,
    describe_resize,
    describe_scheduled_actions,
    describe_snapshot_copy_grants,
    describe_snapshot_schedules,
    describe_storage,
    describe_table_restore_status,
    describe_tags,
    describe_usage_limits,
    disable_snapshot_copy,
    disassociate_data_share_consumer,
    enable_snapshot_copy,
    failover_primary_compute,
    get_cluster_credentials,
    get_cluster_credentials_with_iam,
    get_identity_center_auth_token,
    get_reserved_node_exchange_configuration_options,
    get_reserved_node_exchange_offerings,
    get_resource_policy,
    list_recommendations,
    modify_aqua_configuration,
    modify_authentication_profile,
    modify_cluster_db_revision,
    modify_cluster_iam_roles,
    modify_cluster_maintenance,
    modify_cluster_parameter_group,
    modify_cluster_snapshot,
    modify_cluster_snapshot_schedule,
    modify_cluster_subnet_group,
    modify_custom_domain_association,
    modify_endpoint_access,
    modify_event_subscription,
    modify_integration,
    modify_redshift_idc_application,
    modify_scheduled_action,
    modify_snapshot_copy_retention_period,
    modify_snapshot_schedule,
    modify_usage_limit,
    pause_cluster,
    purchase_reserved_node_offering,
    put_resource_policy,
    register_namespace,
    reject_data_share,
    reset_cluster_parameter_group,
    resize_cluster,
    restore_table_from_cluster_snapshot,
    resume_cluster,
    revoke_cluster_security_group_ingress,
    revoke_endpoint_access,
    revoke_snapshot_access,
    rotate_encryption_key,
    update_partner_status,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    """Build an async mock client."""
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


_CLUSTER_RAW: dict = {
    "ClusterIdentifier": "my-cluster",
    "NodeType": "dc2.large",
    "ClusterStatus": "available",
    "DBName": "dev",
    "MasterUsername": "admin",
    "Endpoint": {
        "Address": "my-cluster.abc.redshift.amazonaws.com",
        "Port": 5439,
    },
    "NumberOfNodes": 1,
    "PubliclyAccessible": False,
    "Encrypted": False,
    "VpcId": "vpc-123",
    "AvailabilityZone": "us-east-1a",
    "Tags": [{"Key": "env", "Value": "test"}],
}

_SNAPSHOT_RAW: dict = {
    "SnapshotIdentifier": "snap-1",
    "ClusterIdentifier": "my-cluster",
    "Status": "available",
    "SnapshotType": "manual",
    "NodeType": "dc2.large",
    "NumberOfNodes": 1,
    "DBName": "dev",
    "Encrypted": False,
}

_AIO = "aws_util.aio.redshift"


# ---------------------------------------------------------------------------
# Re-exported models
# ---------------------------------------------------------------------------


def test_reexported_models() -> None:
    """Verify that Pydantic models are re-exported from the async module."""
    assert ClusterResult is not None
    assert SnapshotResult is not None
    assert ParameterGroupResult is not None
    assert SubnetGroupResult is not None
    assert LoggingStatus is not None


# ---------------------------------------------------------------------------
# create_cluster
# ---------------------------------------------------------------------------


async def test_create_cluster_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster(
        "my-cluster", "dc2.large", "admin", "pass",
    )
    assert result.cluster_identifier == "my-cluster"
    mc.call.assert_awaited_once()


async def test_create_cluster_with_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster(
        "my-cluster", "dc2.large", "admin", "pass",
        tags={"env": "test"},
    )
    assert result.cluster_identifier == "my-cluster"


async def test_create_cluster_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster("c", "dc2.large", "admin", "pass")


async def test_create_cluster_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to create Redshift cluster"):
        await create_cluster("c", "dc2.large", "admin", "pass")


# ---------------------------------------------------------------------------
# describe_clusters
# ---------------------------------------------------------------------------


async def test_describe_clusters_no_id(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Clusters": [_CLUSTER_RAW]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_clusters()
    assert len(result) == 1
    assert result[0].cluster_identifier == "my-cluster"


async def test_describe_clusters_with_id(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Clusters": [_CLUSTER_RAW]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_clusters("my-cluster")
    assert len(result) == 1


async def test_describe_clusters_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    page1 = {"Clusters": [_CLUSTER_RAW], "Marker": "tok"}
    page2 = {"Clusters": [dict(_CLUSTER_RAW, ClusterIdentifier="c2")]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_clusters()
    assert len(result) == 2


async def test_describe_clusters_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Clusters": []})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_clusters()
    assert result == []


async def test_describe_clusters_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await describe_clusters()


async def test_describe_clusters_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="describe_clusters failed"):
        await describe_clusters()


# ---------------------------------------------------------------------------
# delete_cluster
# ---------------------------------------------------------------------------


async def test_delete_cluster_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await delete_cluster("my-cluster")
    assert result.cluster_identifier == "my-cluster"


async def test_delete_cluster_with_final_snapshot(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await delete_cluster(
        "my-cluster",
        skip_final_snapshot=False,
        final_snapshot_identifier="final-snap",
    )
    assert result.cluster_identifier == "my-cluster"


async def test_delete_cluster_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster("c")


async def test_delete_cluster_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to delete Redshift cluster"):
        await delete_cluster("c")


# ---------------------------------------------------------------------------
# modify_cluster
# ---------------------------------------------------------------------------


async def test_modify_cluster_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await modify_cluster("my-cluster", NodeType="dc2.8xlarge")
    assert result.cluster_identifier == "my-cluster"


async def test_modify_cluster_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster("c")


async def test_modify_cluster_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to modify Redshift cluster"):
        await modify_cluster("c")


# ---------------------------------------------------------------------------
# reboot_cluster
# ---------------------------------------------------------------------------


async def test_reboot_cluster_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await reboot_cluster("my-cluster")
    assert result.cluster_identifier == "my-cluster"


async def test_reboot_cluster_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await reboot_cluster("c")


async def test_reboot_cluster_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to reboot Redshift cluster"):
        await reboot_cluster("c")


# ---------------------------------------------------------------------------
# create_cluster_snapshot
# ---------------------------------------------------------------------------


async def test_create_cluster_snapshot_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Snapshot": _SNAPSHOT_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_snapshot("snap-1", "my-cluster")
    assert result.snapshot_identifier == "snap-1"


async def test_create_cluster_snapshot_with_tags(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Snapshot": _SNAPSHOT_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_snapshot(
        "snap-1", "my-cluster", tags={"k": "v"},
    )
    assert result.snapshot_identifier == "snap-1"


async def test_create_cluster_snapshot_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster_snapshot("s", "c")


async def test_create_cluster_snapshot_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        await create_cluster_snapshot("s", "c")


# ---------------------------------------------------------------------------
# describe_cluster_snapshots
# ---------------------------------------------------------------------------


async def test_describe_cluster_snapshots_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Snapshots": [_SNAPSHOT_RAW]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_cluster_snapshots(cluster_identifier="my-cluster")
    assert len(result) == 1


async def test_describe_cluster_snapshots_filtered(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Snapshots": [_SNAPSHOT_RAW]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_cluster_snapshots(
        cluster_identifier="my-cluster", snapshot_identifier="snap-1",
    )
    assert len(result) == 1


async def test_describe_cluster_snapshots_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    page1 = {"Snapshots": [_SNAPSHOT_RAW], "Marker": "tok"}
    page2 = {"Snapshots": [dict(_SNAPSHOT_RAW, SnapshotIdentifier="snap-2")]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_cluster_snapshots()
    assert len(result) == 2


async def test_describe_cluster_snapshots_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Snapshots": []})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_cluster_snapshots()
    assert result == []


async def test_describe_cluster_snapshots_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_snapshots()


async def test_describe_cluster_snapshots_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="describe_cluster_snapshots failed"):
        await describe_cluster_snapshots()


# ---------------------------------------------------------------------------
# delete_cluster_snapshot
# ---------------------------------------------------------------------------


async def test_delete_cluster_snapshot_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    await delete_cluster_snapshot("snap-1")
    mc.call.assert_awaited_once()


async def test_delete_cluster_snapshot_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster_snapshot("s")


async def test_delete_cluster_snapshot_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        await delete_cluster_snapshot("s")


# ---------------------------------------------------------------------------
# restore_from_cluster_snapshot
# ---------------------------------------------------------------------------


async def test_restore_from_cluster_snapshot_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await restore_from_cluster_snapshot("new-c", "snap-1")
    assert result.cluster_identifier == "my-cluster"


async def test_restore_from_cluster_snapshot_with_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc({"Cluster": _CLUSTER_RAW})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await restore_from_cluster_snapshot(
        "new-c", "snap-1", node_type="dc2.8xlarge", number_of_nodes=4,
    )
    assert result.cluster_identifier == "my-cluster"


async def test_restore_from_cluster_snapshot_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await restore_from_cluster_snapshot("c", "s")


async def test_restore_from_cluster_snapshot_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="restore_from_cluster_snapshot failed"):
        await restore_from_cluster_snapshot("c", "s")


# ---------------------------------------------------------------------------
# create_cluster_parameter_group
# ---------------------------------------------------------------------------


async def test_create_cluster_parameter_group_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({
        "ClusterParameterGroup": {
            "ParameterGroupName": "pg1",
            "ParameterGroupFamily": "redshift-1.0",
            "Description": "test",
        }
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_parameter_group(
        "pg1", "redshift-1.0", "test",
    )
    assert result.parameter_group_name == "pg1"


async def test_create_cluster_parameter_group_with_tags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc({
        "ClusterParameterGroup": {
            "ParameterGroupName": "pg1",
            "ParameterGroupFamily": "redshift-1.0",
            "Description": "test",
        }
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_parameter_group(
        "pg1", "redshift-1.0", "test", tags={"k": "v"},
    )
    assert result.parameter_group_name == "pg1"


async def test_create_cluster_parameter_group_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster_parameter_group("pg1", "redshift-1.0", "test")


async def test_create_cluster_parameter_group_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to create parameter group"):
        await create_cluster_parameter_group("pg1", "redshift-1.0", "test")


# ---------------------------------------------------------------------------
# create_cluster_subnet_group
# ---------------------------------------------------------------------------


async def test_create_cluster_subnet_group_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({
        "ClusterSubnetGroup": {
            "ClusterSubnetGroupName": "sg1",
            "Description": "test",
            "VpcId": "vpc-1",
            "Subnets": [{"SubnetIdentifier": "subnet-1"}],
            "SubnetGroupStatus": "Complete",
        }
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_subnet_group("sg1", "test", ["subnet-1"])
    assert result.cluster_subnet_group_name == "sg1"
    assert result.subnet_ids == ["subnet-1"]


async def test_create_cluster_subnet_group_with_tags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc({
        "ClusterSubnetGroup": {
            "ClusterSubnetGroupName": "sg1",
            "Description": "test",
            "Subnets": [],
        }
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await create_cluster_subnet_group(
        "sg1", "test", ["subnet-1"], tags={"k": "v"},
    )
    assert result.cluster_subnet_group_name == "sg1"


async def test_create_cluster_subnet_group_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster_subnet_group("sg1", "test", ["s"])


async def test_create_cluster_subnet_group_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to create subnet group"):
        await create_cluster_subnet_group("sg1", "test", ["s"])


# ---------------------------------------------------------------------------
# describe_logging_status
# ---------------------------------------------------------------------------


async def test_describe_logging_status_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({
        "LoggingEnabled": True,
        "BucketName": "my-bucket",
        "S3KeyPrefix": "logs/",
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_logging_status("my-cluster")
    assert result.logging_enabled is True
    assert result.bucket_name == "my-bucket"


async def test_describe_logging_status_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"LoggingEnabled": False})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await describe_logging_status("my-cluster")
    assert result.logging_enabled is False


async def test_describe_logging_status_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await describe_logging_status("c")


async def test_describe_logging_status_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to describe logging"):
        await describe_logging_status("c")


# ---------------------------------------------------------------------------
# enable_logging
# ---------------------------------------------------------------------------


async def test_enable_logging_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({
        "LoggingEnabled": True,
        "BucketName": "my-bucket",
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await enable_logging("my-cluster", "my-bucket")
    assert result.logging_enabled is True


async def test_enable_logging_with_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({
        "LoggingEnabled": True,
        "BucketName": "my-bucket",
        "S3KeyPrefix": "logs/",
    })
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await enable_logging(
        "my-cluster", "my-bucket", s3_key_prefix="logs/",
    )
    assert result.s3_key_prefix == "logs/"


async def test_enable_logging_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await enable_logging("c", "b")


async def test_enable_logging_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to enable logging"):
        await enable_logging("c", "b")


# ---------------------------------------------------------------------------
# disable_logging
# ---------------------------------------------------------------------------


async def test_disable_logging_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"LoggingEnabled": False})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    result = await disable_logging("my-cluster")
    assert result.logging_enabled is False


async def test_disable_logging_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="boom"):
        await disable_logging("c")


async def test_disable_logging_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)

    with pytest.raises(RuntimeError, match="Failed to disable logging"):
        await disable_logging("c")


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cluster_immediate(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Clusters": [_CLUSTER_RAW]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(f"{_AIO}.asyncio.sleep", AsyncMock())

    result = await wait_for_cluster("my-cluster")
    assert result.cluster_status == "available"


async def test_wait_for_cluster_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    mc = _mc({"Clusters": []})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(f"{_AIO}.asyncio.sleep", AsyncMock())

    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_cluster("ghost")


async def test_wait_for_cluster_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    creating = dict(_CLUSTER_RAW, ClusterStatus="creating")
    mc = _mc({"Clusters": [creating]})
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(f"{_AIO}.asyncio.sleep", AsyncMock())

    _real = time.monotonic
    values = [0.0, 0.0, 1300.0]
    _idx = 0

    def _fake():
        nonlocal _idx
        if _idx < len(values):
            v = values[_idx]
            _idx += 1
            return v
        return _real()

    monkeypatch.setattr(time, "monotonic", _fake)

    with pytest.raises(TimeoutError, match="did not reach status"):
        await wait_for_cluster("my-cluster", timeout=1200.0)


async def test_wait_for_cluster_poll_then_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Covers the asyncio.sleep branch in the polling loop."""
    creating = dict(_CLUSTER_RAW, ClusterStatus="creating")
    available = dict(_CLUSTER_RAW, ClusterStatus="available")

    call_count = {"n": 0}

    async def fake_call(op, **kw):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return {"Clusters": [creating]}
        return {"Clusters": [available]}

    mc = AsyncMock()
    mc.call = fake_call
    monkeypatch.setattr(f"{_AIO}.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(f"{_AIO}.asyncio.sleep", AsyncMock())

    result = await wait_for_cluster(
        "my-cluster", timeout=60.0, poll_interval=0.001,
    )
    assert result.cluster_status == "available"


async def test_accept_reserved_node_exchange(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_reserved_node_exchange("test-reserved_node_id", "test-target_reserved_node_offering_id", )
    mock_client.call.assert_called_once()


async def test_accept_reserved_node_exchange_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_reserved_node_exchange("test-reserved_node_id", "test-target_reserved_node_offering_id", )


async def test_add_partner(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", )
    mock_client.call.assert_called_once()


async def test_add_partner_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", )


async def test_associate_data_share_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_data_share_consumer("test-data_share_arn", )
    mock_client.call.assert_called_once()


async def test_associate_data_share_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_data_share_consumer("test-data_share_arn", )


async def test_authorize_cluster_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_cluster_security_group_ingress("test-cluster_security_group_name", )
    mock_client.call.assert_called_once()


async def test_authorize_cluster_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_cluster_security_group_ingress("test-cluster_security_group_name", )


async def test_authorize_data_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_data_share("test-data_share_arn", "test-consumer_identifier", )
    mock_client.call.assert_called_once()


async def test_authorize_data_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_data_share("test-data_share_arn", "test-consumer_identifier", )


async def test_authorize_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_endpoint_access("test-account", )
    mock_client.call.assert_called_once()


async def test_authorize_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_endpoint_access("test-account", )


async def test_authorize_snapshot_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_snapshot_access("test-account_with_restore_access", )
    mock_client.call.assert_called_once()


async def test_authorize_snapshot_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_snapshot_access("test-account_with_restore_access", )


async def test_batch_delete_cluster_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_cluster_snapshots([], )
    mock_client.call.assert_called_once()


async def test_batch_delete_cluster_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_cluster_snapshots([], )


async def test_batch_modify_cluster_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_modify_cluster_snapshots([], )
    mock_client.call.assert_called_once()


async def test_batch_modify_cluster_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_modify_cluster_snapshots([], )


async def test_cancel_resize(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_resize("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_resize_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_resize("test-cluster_identifier", )


async def test_copy_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_copy_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", )


async def test_create_authentication_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", )
    mock_client.call.assert_called_once()


async def test_create_authentication_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", )


async def test_create_cluster_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cluster_security_group("test-cluster_security_group_name", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_cluster_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster_security_group("test-cluster_security_group_name", "test-description", )


async def test_create_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_create_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", )


async def test_create_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_endpoint_access("test-endpoint_name", "test-subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_create_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_endpoint_access("test-endpoint_name", "test-subnet_group_name", )


async def test_create_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )


async def test_create_hsm_client_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_hsm_client_certificate("test-hsm_client_certificate_identifier", )
    mock_client.call.assert_called_once()


async def test_create_hsm_client_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_hsm_client_certificate("test-hsm_client_certificate_identifier", )


async def test_create_hsm_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_hsm_configuration("test-hsm_configuration_identifier", "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", )
    mock_client.call.assert_called_once()


async def test_create_hsm_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_hsm_configuration("test-hsm_configuration_identifier", "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", )


async def test_create_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration("test-source_arn", "test-target_arn", "test-integration_name", )
    mock_client.call.assert_called_once()


async def test_create_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration("test-source_arn", "test-target_arn", "test-integration_name", )


async def test_create_redshift_idc_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_redshift_idc_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", )


async def test_create_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_scheduled_action("test-scheduled_action_name", {}, "test-schedule", "test-iam_role", )
    mock_client.call.assert_called_once()


async def test_create_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_scheduled_action("test-scheduled_action_name", {}, "test-schedule", "test-iam_role", )


async def test_create_snapshot_copy_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot_copy_grant("test-snapshot_copy_grant_name", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_copy_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot_copy_grant("test-snapshot_copy_grant_name", )


async def test_create_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot_schedule()
    mock_client.call.assert_called_once()


async def test_create_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot_schedule()


async def test_create_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tags("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_create_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tags("test-resource_name", [], )


async def test_create_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_usage_limit("test-cluster_identifier", "test-feature_type", "test-limit_type", 1, )
    mock_client.call.assert_called_once()


async def test_create_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_usage_limit("test-cluster_identifier", "test-feature_type", "test-limit_type", 1, )


async def test_deauthorize_data_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await deauthorize_data_share("test-data_share_arn", "test-consumer_identifier", )
    mock_client.call.assert_called_once()


async def test_deauthorize_data_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deauthorize_data_share("test-data_share_arn", "test-consumer_identifier", )


async def test_delete_authentication_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_authentication_profile("test-authentication_profile_name", )
    mock_client.call.assert_called_once()


async def test_delete_authentication_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_authentication_profile("test-authentication_profile_name", )


async def test_delete_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cluster_parameter_group("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster_parameter_group("test-parameter_group_name", )


async def test_delete_cluster_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cluster_security_group("test-cluster_security_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cluster_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster_security_group("test-cluster_security_group_name", )


async def test_delete_cluster_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cluster_subnet_group("test-cluster_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cluster_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster_subnet_group("test-cluster_subnet_group_name", )


async def test_delete_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_domain_association("test-cluster_identifier", "test-custom_domain_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_domain_association("test-cluster_identifier", "test-custom_domain_name", )


async def test_delete_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_endpoint_access("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_delete_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_endpoint_access("test-endpoint_name", )


async def test_delete_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_delete_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_subscription("test-subscription_name", )


async def test_delete_hsm_client_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_hsm_client_certificate("test-hsm_client_certificate_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_hsm_client_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_hsm_client_certificate("test-hsm_client_certificate_identifier", )


async def test_delete_hsm_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_hsm_configuration("test-hsm_configuration_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_hsm_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_hsm_configuration("test-hsm_configuration_identifier", )


async def test_delete_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_integration("test-integration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_integration("test-integration_arn", )


async def test_delete_partner(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", )
    mock_client.call.assert_called_once()


async def test_delete_partner_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", )


async def test_delete_redshift_idc_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_redshift_idc_application("test-redshift_idc_application_arn", )
    mock_client.call.assert_called_once()


async def test_delete_redshift_idc_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_redshift_idc_application("test-redshift_idc_application_arn", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_scheduled_action("test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_delete_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_scheduled_action("test-scheduled_action_name", )


async def test_delete_snapshot_copy_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot_copy_grant("test-snapshot_copy_grant_name", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_copy_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot_copy_grant("test-snapshot_copy_grant_name", )


async def test_delete_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot_schedule("test-schedule_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot_schedule("test-schedule_identifier", )


async def test_delete_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tags("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_delete_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tags("test-resource_name", [], )


async def test_delete_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_usage_limit("test-usage_limit_id", )
    mock_client.call.assert_called_once()


async def test_delete_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_usage_limit("test-usage_limit_id", )


async def test_deregister_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_namespace({}, [], )
    mock_client.call.assert_called_once()


async def test_deregister_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_namespace({}, [], )


async def test_describe_account_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_attributes()
    mock_client.call.assert_called_once()


async def test_describe_account_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_attributes()


async def test_describe_authentication_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_authentication_profiles()
    mock_client.call.assert_called_once()


async def test_describe_authentication_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_authentication_profiles()


async def test_describe_cluster_db_revisions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_db_revisions()
    mock_client.call.assert_called_once()


async def test_describe_cluster_db_revisions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_db_revisions()


async def test_describe_cluster_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_cluster_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_parameter_groups()


async def test_describe_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_parameters("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_parameters("test-parameter_group_name", )


async def test_describe_cluster_security_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_security_groups()
    mock_client.call.assert_called_once()


async def test_describe_cluster_security_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_security_groups()


async def test_describe_cluster_subnet_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_subnet_groups()
    mock_client.call.assert_called_once()


async def test_describe_cluster_subnet_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_subnet_groups()


async def test_describe_cluster_tracks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_tracks()
    mock_client.call.assert_called_once()


async def test_describe_cluster_tracks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_tracks()


async def test_describe_cluster_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_versions()
    mock_client.call.assert_called_once()


async def test_describe_cluster_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_versions()


async def test_describe_custom_domain_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_domain_associations()
    mock_client.call.assert_called_once()


async def test_describe_custom_domain_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_domain_associations()


async def test_describe_data_shares(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_shares()
    mock_client.call.assert_called_once()


async def test_describe_data_shares_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_shares()


async def test_describe_data_shares_for_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_shares_for_consumer()
    mock_client.call.assert_called_once()


async def test_describe_data_shares_for_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_shares_for_consumer()


async def test_describe_data_shares_for_producer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_shares_for_producer()
    mock_client.call.assert_called_once()


async def test_describe_data_shares_for_producer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_shares_for_producer()


async def test_describe_default_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_default_cluster_parameters("test-parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_default_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_default_cluster_parameters("test-parameter_group_family", )


async def test_describe_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint_access()
    mock_client.call.assert_called_once()


async def test_describe_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint_access()


async def test_describe_endpoint_authorization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint_authorization()
    mock_client.call.assert_called_once()


async def test_describe_endpoint_authorization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint_authorization()


async def test_describe_event_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_categories()
    mock_client.call.assert_called_once()


async def test_describe_event_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_categories()


async def test_describe_event_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_subscriptions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_hsm_client_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_hsm_client_certificates()
    mock_client.call.assert_called_once()


async def test_describe_hsm_client_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_hsm_client_certificates()


async def test_describe_hsm_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_hsm_configurations()
    mock_client.call.assert_called_once()


async def test_describe_hsm_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_hsm_configurations()


async def test_describe_inbound_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_inbound_integrations()
    mock_client.call.assert_called_once()


async def test_describe_inbound_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_inbound_integrations()


async def test_describe_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_integrations()
    mock_client.call.assert_called_once()


async def test_describe_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_integrations()


async def test_describe_node_configuration_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_node_configuration_options("test-action_type", )
    mock_client.call.assert_called_once()


async def test_describe_node_configuration_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_node_configuration_options("test-action_type", )


async def test_describe_orderable_cluster_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_orderable_cluster_options()
    mock_client.call.assert_called_once()


async def test_describe_orderable_cluster_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_orderable_cluster_options()


async def test_describe_partners(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_partners("test-account_id", "test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_partners_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_partners("test-account_id", "test-cluster_identifier", )


async def test_describe_redshift_idc_applications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_redshift_idc_applications()
    mock_client.call.assert_called_once()


async def test_describe_redshift_idc_applications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_redshift_idc_applications()


async def test_describe_reserved_node_exchange_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_node_exchange_status()
    mock_client.call.assert_called_once()


async def test_describe_reserved_node_exchange_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_node_exchange_status()


async def test_describe_reserved_node_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_node_offerings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_node_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_node_offerings()


async def test_describe_reserved_nodes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_nodes()
    mock_client.call.assert_called_once()


async def test_describe_reserved_nodes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_nodes()


async def test_describe_resize(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_resize("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_resize_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resize("test-cluster_identifier", )


async def test_describe_scheduled_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_actions()
    mock_client.call.assert_called_once()


async def test_describe_scheduled_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_actions()


async def test_describe_snapshot_copy_grants(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshot_copy_grants()
    mock_client.call.assert_called_once()


async def test_describe_snapshot_copy_grants_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshot_copy_grants()


async def test_describe_snapshot_schedules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshot_schedules()
    mock_client.call.assert_called_once()


async def test_describe_snapshot_schedules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshot_schedules()


async def test_describe_storage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_storage()
    mock_client.call.assert_called_once()


async def test_describe_storage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_storage()


async def test_describe_table_restore_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_table_restore_status()
    mock_client.call.assert_called_once()


async def test_describe_table_restore_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_table_restore_status()


async def test_describe_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tags()
    mock_client.call.assert_called_once()


async def test_describe_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tags()


async def test_describe_usage_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_usage_limits()
    mock_client.call.assert_called_once()


async def test_describe_usage_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_usage_limits()


async def test_disable_snapshot_copy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_snapshot_copy("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_disable_snapshot_copy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_snapshot_copy("test-cluster_identifier", )


async def test_disassociate_data_share_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_data_share_consumer("test-data_share_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_data_share_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_data_share_consumer("test-data_share_arn", )


async def test_enable_snapshot_copy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_snapshot_copy("test-cluster_identifier", "test-destination_region", )
    mock_client.call.assert_called_once()


async def test_enable_snapshot_copy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_snapshot_copy("test-cluster_identifier", "test-destination_region", )


async def test_failover_primary_compute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_primary_compute("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_failover_primary_compute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_primary_compute("test-cluster_identifier", )


async def test_get_cluster_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cluster_credentials("test-db_user", )
    mock_client.call.assert_called_once()


async def test_get_cluster_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cluster_credentials("test-db_user", )


async def test_get_cluster_credentials_with_iam(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cluster_credentials_with_iam()
    mock_client.call.assert_called_once()


async def test_get_cluster_credentials_with_iam_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cluster_credentials_with_iam()


async def test_get_identity_center_auth_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_center_auth_token([], )
    mock_client.call.assert_called_once()


async def test_get_identity_center_auth_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_center_auth_token([], )


async def test_get_reserved_node_exchange_configuration_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reserved_node_exchange_configuration_options("test-action_type", )
    mock_client.call.assert_called_once()


async def test_get_reserved_node_exchange_configuration_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reserved_node_exchange_configuration_options("test-action_type", )


async def test_get_reserved_node_exchange_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reserved_node_exchange_offerings("test-reserved_node_id", )
    mock_client.call.assert_called_once()


async def test_get_reserved_node_exchange_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reserved_node_exchange_offerings("test-reserved_node_id", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_list_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recommendations()
    mock_client.call.assert_called_once()


async def test_list_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recommendations()


async def test_modify_aqua_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_aqua_configuration("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_aqua_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_aqua_configuration("test-cluster_identifier", )


async def test_modify_authentication_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", )
    mock_client.call.assert_called_once()


async def test_modify_authentication_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", )


async def test_modify_cluster_db_revision(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_db_revision("test-cluster_identifier", "test-revision_target", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_db_revision_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_db_revision("test-cluster_identifier", "test-revision_target", )


async def test_modify_cluster_iam_roles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_iam_roles("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_iam_roles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_iam_roles("test-cluster_identifier", )


async def test_modify_cluster_maintenance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_maintenance("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_maintenance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_maintenance("test-cluster_identifier", )


async def test_modify_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_parameter_group("test-parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_parameter_group("test-parameter_group_name", [], )


async def test_modify_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_snapshot("test-snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_snapshot("test-snapshot_identifier", )


async def test_modify_cluster_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_snapshot_schedule("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_snapshot_schedule("test-cluster_identifier", )


async def test_modify_cluster_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster_subnet_group("test-cluster_subnet_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_cluster_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster_subnet_group("test-cluster_subnet_group_name", [], )


async def test_modify_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", )


async def test_modify_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_endpoint_access("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_modify_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_endpoint_access("test-endpoint_name", )


async def test_modify_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_modify_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_event_subscription("test-subscription_name", )


async def test_modify_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_integration("test-integration_arn", )
    mock_client.call.assert_called_once()


async def test_modify_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_integration("test-integration_arn", )


async def test_modify_redshift_idc_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_redshift_idc_application("test-redshift_idc_application_arn", )
    mock_client.call.assert_called_once()


async def test_modify_redshift_idc_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_redshift_idc_application("test-redshift_idc_application_arn", )


async def test_modify_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_scheduled_action("test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_modify_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_scheduled_action("test-scheduled_action_name", )


async def test_modify_snapshot_copy_retention_period(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_snapshot_copy_retention_period("test-cluster_identifier", 1, )
    mock_client.call.assert_called_once()


async def test_modify_snapshot_copy_retention_period_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_snapshot_copy_retention_period("test-cluster_identifier", 1, )


async def test_modify_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_snapshot_schedule("test-schedule_identifier", [], )
    mock_client.call.assert_called_once()


async def test_modify_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_snapshot_schedule("test-schedule_identifier", [], )


async def test_modify_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_usage_limit("test-usage_limit_id", )
    mock_client.call.assert_called_once()


async def test_modify_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_usage_limit("test-usage_limit_id", )


async def test_pause_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await pause_cluster("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_pause_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await pause_cluster("test-cluster_identifier", )


async def test_purchase_reserved_node_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_reserved_node_offering("test-reserved_node_offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_reserved_node_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_reserved_node_offering("test-reserved_node_offering_id", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy", )


async def test_register_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_namespace({}, [], )
    mock_client.call.assert_called_once()


async def test_register_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_namespace({}, [], )


async def test_reject_data_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_data_share("test-data_share_arn", )
    mock_client.call.assert_called_once()


async def test_reject_data_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_data_share("test-data_share_arn", )


async def test_reset_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_cluster_parameter_group("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_cluster_parameter_group("test-parameter_group_name", )


async def test_resize_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await resize_cluster("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_resize_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resize_cluster("test-cluster_identifier", )


async def test_restore_table_from_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", )
    mock_client.call.assert_called_once()


async def test_restore_table_from_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", )


async def test_resume_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_cluster("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_resume_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_cluster("test-cluster_identifier", )


async def test_revoke_cluster_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_cluster_security_group_ingress("test-cluster_security_group_name", )
    mock_client.call.assert_called_once()


async def test_revoke_cluster_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_cluster_security_group_ingress("test-cluster_security_group_name", )


async def test_revoke_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_endpoint_access()
    mock_client.call.assert_called_once()


async def test_revoke_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_endpoint_access()


async def test_revoke_snapshot_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_snapshot_access("test-account_with_restore_access", )
    mock_client.call.assert_called_once()


async def test_revoke_snapshot_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_snapshot_access("test-account_with_restore_access", )


async def test_rotate_encryption_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await rotate_encryption_key("test-cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_rotate_encryption_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rotate_encryption_key("test-cluster_identifier", )


async def test_update_partner_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_partner_status("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_partner_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_partner_status("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", )


@pytest.mark.asyncio
async def test_associate_data_share_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import associate_data_share_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await associate_data_share_consumer("test-data_share_arn", associate_entire_account=1, consumer_arn="test-consumer_arn", consumer_region="test-consumer_region", allow_writes=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_cluster_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import authorize_cluster_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await authorize_cluster_security_group_ingress("test-cluster_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_data_share_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import authorize_data_share
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await authorize_data_share("test-data_share_arn", "test-consumer_identifier", allow_writes=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import authorize_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await authorize_endpoint_access(1, cluster_identifier="test-cluster_identifier", vpc_ids="test-vpc_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_snapshot_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import authorize_snapshot_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await authorize_snapshot_access(1, snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", snapshot_cluster_identifier="test-snapshot_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_modify_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import batch_modify_cluster_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await batch_modify_cluster_snapshots("test-snapshot_identifier_list", manual_snapshot_retention_period="test-manual_snapshot_retention_period", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import copy_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", source_snapshot_cluster_identifier="test-source_snapshot_cluster_identifier", manual_snapshot_retention_period="test-manual_snapshot_retention_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cluster_security_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_cluster_security_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_cluster_security_group("test-cluster_security_group_name", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_endpoint_access("test-endpoint_name", "test-subnet_group_name", cluster_identifier="test-cluster_identifier", resource_owner="test-resource_owner", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", source_ids="test-source_ids", event_categories="test-event_categories", severity="test-severity", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_hsm_client_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_hsm_client_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_hsm_client_certificate("test-hsm_client_certificate_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_hsm_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_hsm_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_hsm_configuration({}, "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_integration("test-source_arn", "test-target_arn", "test-integration_name", kms_key_id="test-kms_key_id", tag_list="test-tag_list", additional_encryption_context={}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_redshift_idc_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_redshift_idc_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", identity_namespace="test-identity_namespace", authorized_token_issuer_list="test-authorized_token_issuer_list", service_integrations="test-service_integrations", tags=[{"Key": "k", "Value": "v"}], sso_tag_keys="test-sso_tag_keys", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_scheduled_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_scheduled_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_scheduled_action("test-scheduled_action_name", "test-target_action", "test-schedule", "test-iam_role", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", end_time="test-end_time", enable=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_copy_grant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_snapshot_copy_grant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_snapshot_copy_grant("test-snapshot_copy_grant_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_snapshot_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_snapshot_schedule(schedule_definitions={}, schedule_identifier="test-schedule_identifier", schedule_description="test-schedule_description", tags=[{"Key": "k", "Value": "v"}], next_invocations="test-next_invocations", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_usage_limit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import create_usage_limit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await create_usage_limit("test-cluster_identifier", "test-feature_type", 1, "test-amount", period="test-period", breach_action="test-breach_action", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_account_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_account_attributes(attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_authentication_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_authentication_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_authentication_profiles(authentication_profile_name="test-authentication_profile_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_db_revisions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_db_revisions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_db_revisions(cluster_identifier="test-cluster_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_parameter_groups(parameter_group_name="test-parameter_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_parameters("test-parameter_group_name", source="test-source", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_security_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_security_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_security_groups(cluster_security_group_name="test-cluster_security_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_subnet_groups(cluster_subnet_group_name="test-cluster_subnet_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_tracks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_tracks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_tracks(maintenance_track_name="test-maintenance_track_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_cluster_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_versions(cluster_version="test-cluster_version", cluster_parameter_group_family="test-cluster_parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_custom_domain_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_custom_domain_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_custom_domain_associations(custom_domain_name="test-custom_domain_name", custom_domain_certificate_arn="test-custom_domain_certificate_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_data_shares_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_data_shares
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_data_shares(data_share_arn="test-data_share_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_data_shares_for_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_data_shares_for_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_data_shares_for_consumer(consumer_arn="test-consumer_arn", status="test-status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_data_shares_for_producer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_data_shares_for_producer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_data_shares_for_producer(producer_arn="test-producer_arn", status="test-status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_default_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_default_cluster_parameters("test-parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint_access(cluster_identifier="test-cluster_identifier", resource_owner="test-resource_owner", endpoint_name="test-endpoint_name", vpc_id="test-vpc_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_authorization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_endpoint_authorization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint_authorization(cluster_identifier="test-cluster_identifier", account=1, grantee="test-grantee", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_event_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_event_categories(source_type="test-source_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_event_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_event_subscriptions(subscription_name="test-subscription_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_hsm_client_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_hsm_client_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_hsm_client_certificates(hsm_client_certificate_identifier="test-hsm_client_certificate_identifier", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_hsm_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_hsm_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_hsm_configurations(hsm_configuration_identifier={}, max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_inbound_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_inbound_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_inbound_integrations(integration_arn="test-integration_arn", target_arn="test-target_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_integrations(integration_arn="test-integration_arn", max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_node_configuration_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_node_configuration_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_node_configuration_options("test-action_type", cluster_identifier="test-cluster_identifier", snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", owner_account=1, filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_orderable_cluster_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_orderable_cluster_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_orderable_cluster_options(cluster_version="test-cluster_version", node_type="test-node_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_partners_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_partners
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_partners(1, "test-cluster_identifier", database_name="test-database_name", partner_name="test-partner_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_redshift_idc_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_redshift_idc_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_redshift_idc_applications(redshift_idc_application_arn="test-redshift_idc_application_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_node_exchange_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_reserved_node_exchange_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_node_exchange_status(reserved_node_id="test-reserved_node_id", reserved_node_exchange_request_id="test-reserved_node_exchange_request_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_node_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_reserved_node_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_node_offerings(reserved_node_offering_id="test-reserved_node_offering_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_nodes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_reserved_nodes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_nodes(reserved_node_id="test-reserved_node_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_scheduled_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_scheduled_actions(scheduled_action_name="test-scheduled_action_name", target_action_type="test-target_action_type", start_time="test-start_time", end_time="test-end_time", active="test-active", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshot_copy_grants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_snapshot_copy_grants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_snapshot_copy_grants(snapshot_copy_grant_name="test-snapshot_copy_grant_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshot_schedules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_snapshot_schedules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_snapshot_schedules(cluster_identifier="test-cluster_identifier", schedule_identifier="test-schedule_identifier", tag_keys="test-tag_keys", tag_values="test-tag_values", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_table_restore_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_table_restore_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_table_restore_status(cluster_identifier="test-cluster_identifier", table_restore_request_id="test-table_restore_request_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_tags(resource_name="test-resource_name", resource_type="test-resource_type", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_usage_limits_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import describe_usage_limits
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await describe_usage_limits(usage_limit_id=1, cluster_identifier="test-cluster_identifier", feature_type="test-feature_type", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_data_share_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import disassociate_data_share_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await disassociate_data_share_consumer("test-data_share_arn", disassociate_entire_account=1, consumer_arn="test-consumer_arn", consumer_region="test-consumer_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_snapshot_copy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import enable_snapshot_copy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await enable_snapshot_copy("test-cluster_identifier", "test-destination_region", retention_period="test-retention_period", snapshot_copy_grant_name="test-snapshot_copy_grant_name", manual_snapshot_retention_period="test-manual_snapshot_retention_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cluster_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import get_cluster_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await get_cluster_credentials("test-db_user", db_name="test-db_name", cluster_identifier="test-cluster_identifier", duration_seconds=1, auto_create=True, db_groups="test-db_groups", custom_domain_name="test-custom_domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cluster_credentials_with_iam_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import get_cluster_credentials_with_iam
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await get_cluster_credentials_with_iam(db_name="test-db_name", cluster_identifier="test-cluster_identifier", duration_seconds=1, custom_domain_name="test-custom_domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_reserved_node_exchange_configuration_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import get_reserved_node_exchange_configuration_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await get_reserved_node_exchange_configuration_options("test-action_type", cluster_identifier="test-cluster_identifier", snapshot_identifier="test-snapshot_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_reserved_node_exchange_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import get_reserved_node_exchange_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await get_reserved_node_exchange_offerings("test-reserved_node_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import list_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await list_recommendations(cluster_identifier="test-cluster_identifier", namespace_arn="test-namespace_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_aqua_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_aqua_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_aqua_configuration("test-cluster_identifier", aqua_configuration_status={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_iam_roles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_cluster_iam_roles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_cluster_iam_roles("test-cluster_identifier", add_iam_roles="test-add_iam_roles", remove_iam_roles="test-remove_iam_roles", default_iam_role_arn="test-default_iam_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_maintenance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_cluster_maintenance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_cluster_maintenance("test-cluster_identifier", defer_maintenance="test-defer_maintenance", defer_maintenance_identifier="test-defer_maintenance_identifier", defer_maintenance_start_time="test-defer_maintenance_start_time", defer_maintenance_end_time="test-defer_maintenance_end_time", defer_maintenance_duration=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_cluster_snapshot("test-snapshot_identifier", manual_snapshot_retention_period="test-manual_snapshot_retention_period", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_cluster_snapshot_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_cluster_snapshot_schedule("test-cluster_identifier", schedule_identifier="test-schedule_identifier", disassociate_schedule="test-disassociate_schedule", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_cluster_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_cluster_subnet_group("test-cluster_subnet_group_name", "test-subnet_ids", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_endpoint_access("test-endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", source_ids="test-source_ids", event_categories="test-event_categories", severity="test-severity", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_integration("test-integration_arn", description="test-description", integration_name="test-integration_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_redshift_idc_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_redshift_idc_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_redshift_idc_application("test-redshift_idc_application_arn", identity_namespace="test-identity_namespace", iam_role_arn="test-iam_role_arn", idc_display_name="test-idc_display_name", authorized_token_issuer_list="test-authorized_token_issuer_list", service_integrations="test-service_integrations", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_scheduled_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_scheduled_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_scheduled_action("test-scheduled_action_name", target_action="test-target_action", schedule="test-schedule", iam_role="test-iam_role", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", end_time="test-end_time", enable=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_snapshot_copy_retention_period_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_snapshot_copy_retention_period
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_snapshot_copy_retention_period("test-cluster_identifier", "test-retention_period", manual="test-manual", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_usage_limit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import modify_usage_limit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await modify_usage_limit(1, amount="test-amount", breach_action="test-breach_action", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_reserved_node_offering_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import purchase_reserved_node_offering
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await purchase_reserved_node_offering("test-reserved_node_offering_id", node_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import reset_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await reset_cluster_parameter_group("test-parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resize_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import resize_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await resize_cluster("test-cluster_identifier", cluster_type="test-cluster_type", node_type="test-node_type", number_of_nodes="test-number_of_nodes", classic="test-classic", reserved_node_id="test-reserved_node_id", target_reserved_node_offering_id="test-target_reserved_node_offering_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_table_from_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import restore_table_from_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", enable_case_sensitive_identifier=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_cluster_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import revoke_cluster_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await revoke_cluster_security_group_ingress("test-cluster_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import revoke_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await revoke_endpoint_access(cluster_identifier="test-cluster_identifier", account=1, vpc_ids="test-vpc_ids", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_snapshot_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import revoke_snapshot_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await revoke_snapshot_access(1, snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", snapshot_cluster_identifier="test-snapshot_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_partner_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift import update_partner_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift.async_client", lambda *a, **kw: mock_client)
    await update_partner_status(1, "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", status_message="test-status_message", region_name="us-east-1")
    mock_client.call.assert_called_once()
