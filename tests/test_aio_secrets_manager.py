"""Tests for aws_util.aio.secrets_manager — 100 % line coverage."""
from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.secrets_manager import (
    create_secret,
    delete_secret,
    get_secret,
    list_secrets,
    rotate_secret,
    update_secret,
    batch_get_secret_value,
    cancel_rotate_secret,
    delete_resource_policy,
    describe_secret,
    get_random_password,
    get_resource_policy,
    get_secret_value,
    list_secret_version_ids,
    put_resource_policy,
    put_secret_value,
    remove_regions_from_replication,
    replicate_secret_to_regions,
    restore_secret,
    stop_replication_to_replica,
    tag_resource,
    untag_resource,
    update_secret_version_stage,
    validate_resource_policy,
)


def _mc(return_value=None, side_effect=None):
    c = AsyncMock()
    if side_effect:
        c.call.side_effect = side_effect
        c.paginate.side_effect = side_effect
    else:
        c.call.return_value = return_value or {}
        c.paginate.return_value = return_value if isinstance(return_value, list) else []
    return c


# ---------------------------------------------------------------------------
# create_secret
# ---------------------------------------------------------------------------


async def test_create_secret_string(monkeypatch):
    mc = _mc({"ARN": "arn:secret"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    r = await create_secret("my-secret", "val")
    assert r == "arn:secret"


async def test_create_secret_dict(monkeypatch):
    mc = _mc({"ARN": "arn:secret"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    r = await create_secret("my-secret", {"k": "v"})
    assert r == "arn:secret"
    assert json.loads(mc.call.call_args[1]["SecretString"]) == {"k": "v"}

async def test_create_secret_no_optional(monkeypatch):
    mc = _mc({"ARN": "arn:secret"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await create_secret("s", "v")
    kw = mc.call.call_args[1]
    assert "Description" not in kw
    assert "KmsKeyId" not in kw
    assert "Tags" not in kw


async def test_create_secret_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to create secret"):
        await create_secret("s", "v")


# ---------------------------------------------------------------------------
# update_secret
# ---------------------------------------------------------------------------


async def test_update_secret_string(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await update_secret("s", "new_val")
    mc.call.assert_called_once()


async def test_update_secret_dict(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await update_secret("s", {"k": "v"})
    assert json.loads(mc.call.call_args[1]["SecretString"]) == {"k": "v"}


async def test_update_secret_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to update secret"):
        await update_secret("s", "v")


# ---------------------------------------------------------------------------
# delete_secret
# ---------------------------------------------------------------------------


async def test_delete_secret_default(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await delete_secret("s")
    kw = mc.call.call_args[1]
    assert kw["RecoveryWindowInDays"] == 30
    assert "ForceDeleteWithoutRecovery" not in kw


async def test_delete_secret_force(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await delete_secret("s", force_delete=True)
    kw = mc.call.call_args[1]
    assert kw["ForceDeleteWithoutRecovery"] is True


async def test_delete_secret_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to delete secret"):
        await delete_secret("s")


# ---------------------------------------------------------------------------
# list_secrets
# ---------------------------------------------------------------------------


async def test_list_secrets(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = [
        {"Name": "s1", "ARN": "arn:s1", "Description": "d", "LastChangedDate": "x",
         "LastAccessedDate": "y", "RotationEnabled": True},
    ]
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    r = await list_secrets()
    assert len(r) == 1
    assert r[0]["name"] == "s1"
    assert r[0]["rotation_enabled"] is True


async def test_list_secrets_with_prefix(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = []
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await list_secrets(name_prefix="app/")
    kw = mc.paginate.call_args[1]
    assert kw["Filters"] == [{"Key": "name", "Values": ["app/"]}]


async def test_list_secrets_no_optional_fields(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = [
        {"Name": "s1", "ARN": "arn:s1"},
    ]
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    r = await list_secrets()
    assert r[0]["description"] == ""
    assert r[0]["last_changed_date"] is None
    assert r[0]["last_accessed_date"] is None
    assert r[0]["rotation_enabled"] is False


async def test_list_secrets_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_secrets failed"):
        await list_secrets()


# ---------------------------------------------------------------------------
# rotate_secret
# ---------------------------------------------------------------------------


async def test_rotate_secret_basic(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await rotate_secret("s")
    kw = mc.call.call_args[1]
    assert "RotationLambdaARN" not in kw


async def test_rotate_secret_with_lambda(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await rotate_secret("s", lambda_arn="arn:lambda:fn")
    kw = mc.call.call_args[1]
    assert kw["RotationLambdaARN"] == "arn:lambda:fn"
    assert "RotationRules" not in kw


async def test_rotate_secret_with_lambda_and_days(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    await rotate_secret("s", lambda_arn="arn:fn", rotation_days=7)
    kw = mc.call.call_args[1]
    assert kw["RotationRules"] == {"AutomaticallyAfterDays": 7}


async def test_rotate_secret_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to rotate secret"):
        await rotate_secret("s")


# ---------------------------------------------------------------------------
# get_secret
# ---------------------------------------------------------------------------


async def test_get_secret_plain(monkeypatch):
    mc = _mc({"SecretString": "myval"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    assert await get_secret("my-secret") == "myval"


async def test_get_secret_with_json_key(monkeypatch):
    mc = _mc({"SecretString": '{"user": "admin", "pass": "pw"}'})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    assert await get_secret("my-secret:pass") == "pw"


async def test_get_secret_binary(monkeypatch):
    mc = _mc({"SecretBinary": b"binaryval"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    assert await get_secret("s") == "binaryval"


async def test_get_secret_json_key_not_found(monkeypatch):
    mc = _mc({"SecretString": '{"user": "admin"}'})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(KeyError, match="missing"):
        await get_secret("s:missing")


async def test_get_secret_invalid_json(monkeypatch):
    mc = _mc({"SecretString": "not-json"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="not valid JSON"):
        await get_secret("s:key")


async def test_get_secret_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Error resolving secret"):
        await get_secret("s")


async def test_batch_get_secret_value(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_secret_value()
    mock_client.call.assert_called_once()


async def test_batch_get_secret_value_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_secret_value()


async def test_cancel_rotate_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_rotate_secret("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_cancel_rotate_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_rotate_secret("test-secret_id", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-secret_id", )


async def test_describe_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_secret("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_describe_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_secret("test-secret_id", )


async def test_get_random_password(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_random_password()
    mock_client.call.assert_called_once()


async def test_get_random_password_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_random_password()


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-secret_id", )


async def test_get_secret_value(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_secret_value("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_get_secret_value_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_secret_value("test-secret_id", )


async def test_list_secret_version_ids(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_secret_version_ids("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_list_secret_version_ids_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_secret_version_ids("test-secret_id", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-secret_id", "test-resource_policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-secret_id", "test-resource_policy", )


async def test_put_secret_value(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_secret_value("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_put_secret_value_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_secret_value("test-secret_id", )


async def test_remove_regions_from_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_regions_from_replication("test-secret_id", [], )
    mock_client.call.assert_called_once()


async def test_remove_regions_from_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_regions_from_replication("test-secret_id", [], )


async def test_replicate_secret_to_regions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await replicate_secret_to_regions("test-secret_id", [], )
    mock_client.call.assert_called_once()


async def test_replicate_secret_to_regions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replicate_secret_to_regions("test-secret_id", [], )


async def test_restore_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_secret("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_restore_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_secret("test-secret_id", )


async def test_stop_replication_to_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_replication_to_replica("test-secret_id", )
    mock_client.call.assert_called_once()


async def test_stop_replication_to_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_replication_to_replica("test-secret_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-secret_id", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-secret_id", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-secret_id", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-secret_id", [], )


async def test_update_secret_version_stage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_secret_version_stage("test-secret_id", "test-version_stage", )
    mock_client.call.assert_called_once()


async def test_update_secret_version_stage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_secret_version_stage("test-secret_id", "test-version_stage", )


async def test_validate_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_resource_policy("test-resource_policy", )
    mock_client.call.assert_called_once()


async def test_validate_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.secrets_manager.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_resource_policy("test-resource_policy", )


@pytest.mark.asyncio
async def test_rotate_secret_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import rotate_secret
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await rotate_secret("test-name", rotation_days="test-rotation_days", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_secret_value_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import batch_get_secret_value
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await batch_get_secret_value(secret_id_list="test-secret_id_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_random_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import get_random_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await get_random_password(password_length="test-password_length", exclude_characters="test-exclude_characters", exclude_numbers="test-exclude_numbers", exclude_punctuation="test-exclude_punctuation", exclude_uppercase="test-exclude_uppercase", exclude_lowercase="test-exclude_lowercase", include_space=True, require_each_included_type=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_secret_value_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import get_secret_value
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await get_secret_value("test-secret_id", version_id="test-version_id", version_stage="test-version_stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_secret_version_ids_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import list_secret_version_ids
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await list_secret_version_ids("test-secret_id", max_results=1, next_token="test-next_token", include_deprecated=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-secret_id", "{}", block_public_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_secret_value_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import put_secret_value
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await put_secret_value("test-secret_id", client_request_token="test-client_request_token", secret_binary="test-secret_binary", secret_string="test-secret_string", version_stages="test-version_stages", rotation_token="test-rotation_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replicate_secret_to_regions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import replicate_secret_to_regions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await replicate_secret_to_regions("test-secret_id", "test-add_replica_regions", force_overwrite_replica_secret=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_secret_version_stage_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import update_secret_version_stage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await update_secret_version_stage("test-secret_id", "test-version_stage", remove_from_version_id="test-remove_from_version_id", move_to_version_id="test-move_to_version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import validate_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await validate_resource_policy("{}", secret_id="test-secret_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_secret_with_tags(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.secrets_manager import create_secret
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={"ARN": "arn:aws:secretsmanager:us-east-1:123:secret:test"})
    monkeypatch.setattr("aws_util.aio.secrets_manager.async_client", lambda *a, **kw: mock_client)
    await create_secret("test-secret", "value", description="desc", kms_key_id="key-1", tags={"env": "test"}, region_name="us-east-1")
    mock_client.call.assert_called_once()
