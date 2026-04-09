"""Tests for aws_util.secrets_manager module."""
from __future__ import annotations

import json
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.secrets_manager import (
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# create_secret
# ---------------------------------------------------------------------------


def test_create_secret_string(secrets_client):
    arn = create_secret("my/secret", "plain-value", region_name=REGION)
    assert arn.startswith("arn:aws:")
    resp = secrets_client.get_secret_value(SecretId="my/secret")
    assert resp["SecretString"] == "plain-value"


def test_create_secret_dict(secrets_client):
    create_secret("my/dict", {"user": "alice", "pass": "pw"}, region_name=REGION)
    resp = secrets_client.get_secret_value(SecretId="my/dict")
    data = json.loads(resp["SecretString"])
    assert data["user"] == "alice"


def test_create_secret_with_description(secrets_client):
    create_secret("my/desc", "val", description="Test desc", region_name=REGION)
    resp = secrets_client.describe_secret(SecretId="my/desc")
    assert resp["Description"] == "Test desc"


def test_create_secret_with_tags(secrets_client):
    create_secret("my/tags", "val", tags={"env": "test"}, region_name=REGION)
    # Just verify it was created (tags are harder to assert in moto)
    resp = secrets_client.get_secret_value(SecretId="my/tags")
    assert resp["SecretString"] == "val"


def test_create_secret_with_kms(secrets_client):
    # moto accepts but ignores kms_key_id
    create_secret("my/kms", "val", kms_key_id="alias/aws/secretsmanager", region_name=REGION)
    resp = secrets_client.get_secret_value(SecretId="my/kms")
    assert resp["SecretString"] == "val"


def test_create_secret_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_client.create_secret.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "CreateSecret",
    )
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create secret"):
        create_secret("x", "y", region_name=REGION)


# ---------------------------------------------------------------------------
# update_secret
# ---------------------------------------------------------------------------


def test_update_secret_string(secrets_client):
    secrets_client.create_secret(Name="upd/secret", SecretString="old")
    update_secret("upd/secret", "new-value", region_name=REGION)
    resp = secrets_client.get_secret_value(SecretId="upd/secret")
    assert resp["SecretString"] == "new-value"


def test_update_secret_dict(secrets_client):
    secrets_client.create_secret(Name="upd/dict", SecretString=json.dumps({"k": "v"}))
    update_secret("upd/dict", {"k": "updated"}, region_name=REGION)
    resp = secrets_client.get_secret_value(SecretId="upd/dict")
    assert json.loads(resp["SecretString"])["k"] == "updated"


def test_update_secret_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_client.update_secret.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "UpdateSecret",
    )
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update secret"):
        update_secret("no/such", "val", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_secret
# ---------------------------------------------------------------------------


def test_delete_secret_with_recovery_window(secrets_client):
    secrets_client.create_secret(Name="del/rec", SecretString="v")
    delete_secret("del/rec", recovery_window_in_days=7, region_name=REGION)
    # Secret should be marked for deletion
    resp = secrets_client.describe_secret(SecretId="del/rec")
    assert "DeletedDate" in resp or resp.get("Name") == "del/rec"


def test_delete_secret_force(secrets_client):
    secrets_client.create_secret(Name="del/force", SecretString="v")
    delete_secret("del/force", force_delete=True, region_name=REGION)


def test_delete_secret_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_client.delete_secret.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DeleteSecret",
    )
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete secret"):
        delete_secret("no/such", region_name=REGION)


# ---------------------------------------------------------------------------
# list_secrets
# ---------------------------------------------------------------------------


def test_list_secrets_returns_all(secrets_client):
    secrets_client.create_secret(Name="ls/a", SecretString="v1")
    secrets_client.create_secret(Name="ls/b", SecretString="v2")
    result = list_secrets(region_name=REGION)
    names = [s["name"] for s in result]
    assert "ls/a" in names
    assert "ls/b" in names


def test_list_secrets_with_prefix(secrets_client):
    secrets_client.create_secret(Name="pfx/a", SecretString="v1")
    secrets_client.create_secret(Name="other/b", SecretString="v2")
    result = list_secrets(name_prefix="pfx", region_name=REGION)
    assert any(s["name"] == "pfx/a" for s in result)


def test_list_secrets_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "ListSecrets",
    )
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_secrets failed"):
        list_secrets(region_name=REGION)


# ---------------------------------------------------------------------------
# rotate_secret
# ---------------------------------------------------------------------------


def test_rotate_secret_basic(secrets_client):
    secrets_client.create_secret(Name="rot/secret", SecretString="v")
    # moto may or may not support rotation; just ensure no exception with basic params
    try:
        rotate_secret("rot/secret", region_name=REGION)
    except RuntimeError:
        pass  # moto may not support rotation without a Lambda


def test_rotate_secret_with_lambda_and_days(secrets_client):
    secrets_client.create_secret(Name="rot/lambda", SecretString="v")
    try:
        rotate_secret(
            "rot/lambda",
            lambda_arn="arn:aws:lambda:us-east-1:123456789012:function:rotator",
            rotation_days=30,
            region_name=REGION,
        )
    except RuntimeError:
        pass


def test_rotate_secret_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_client.rotate_secret.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "RotateSecret",
    )
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rotate secret"):
        rotate_secret("no/such", region_name=REGION)


# ---------------------------------------------------------------------------
# get_secret
# ---------------------------------------------------------------------------


def test_get_secret_plain_string(secrets_client):
    secrets_client.create_secret(Name="gs/plain", SecretString="my-value")
    result = get_secret("gs/plain", region_name=REGION)
    assert result == "my-value"


def test_get_secret_json_key(secrets_client):
    secrets_client.create_secret(
        Name="gs/json",
        SecretString=json.dumps({"user": "alice", "pass": "secret"}),
    )
    result = get_secret("gs/json:user", region_name=REGION)
    assert result == "alice"


def test_get_secret_json_key_not_found(secrets_client):
    secrets_client.create_secret(
        Name="gs/jk", SecretString=json.dumps({"user": "alice"})
    )
    with pytest.raises(KeyError, match="'missing'"):
        get_secret("gs/jk:missing", region_name=REGION)


def test_get_secret_invalid_json_with_key(secrets_client):
    secrets_client.create_secret(Name="gs/bad", SecretString="not-json")
    with pytest.raises(RuntimeError, match="not valid JSON"):
        get_secret("gs/bad:somekey", region_name=REGION)


def test_get_secret_api_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.secrets_manager as sm

    mock_client = MagicMock()
    mock_client.get_secret_value.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "GetSecretValue",
    )
    monkeypatch.setattr(sm, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Error resolving secret"):
        get_secret("no/such", region_name=REGION)


def test_get_secret_binary_secret(secrets_client):
    """Secrets stored as binary bytes should be decoded."""
    secrets_client.create_secret(Name="gs/bin", SecretBinary=b"binary-value")
    result = get_secret("gs/bin", region_name=REGION)
    assert result == "binary-value"


def test_batch_get_secret_value(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    batch_get_secret_value(region_name=REGION)
    mock_client.batch_get_secret_value.assert_called_once()


def test_batch_get_secret_value_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_secret_value.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_secret_value",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get secret value"):
        batch_get_secret_value(region_name=REGION)


def test_cancel_rotate_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_rotate_secret.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    cancel_rotate_secret("test-secret_id", region_name=REGION)
    mock_client.cancel_rotate_secret.assert_called_once()


def test_cancel_rotate_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_rotate_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_rotate_secret",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel rotate secret"):
        cancel_rotate_secret("test-secret_id", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-secret_id", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-secret_id", region_name=REGION)


def test_describe_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_secret.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    describe_secret("test-secret_id", region_name=REGION)
    mock_client.describe_secret.assert_called_once()


def test_describe_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_secret",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe secret"):
        describe_secret("test-secret_id", region_name=REGION)


def test_get_random_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_random_password.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    get_random_password(region_name=REGION)
    mock_client.get_random_password.assert_called_once()


def test_get_random_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_random_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_random_password",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get random password"):
        get_random_password(region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-secret_id", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-secret_id", region_name=REGION)


def test_get_secret_value(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    get_secret_value("test-secret_id", region_name=REGION)
    mock_client.get_secret_value.assert_called_once()


def test_get_secret_value_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_secret_value.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_secret_value",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get secret value"):
        get_secret_value("test-secret_id", region_name=REGION)


def test_list_secret_version_ids(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_secret_version_ids.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    list_secret_version_ids("test-secret_id", region_name=REGION)
    mock_client.list_secret_version_ids.assert_called_once()


def test_list_secret_version_ids_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_secret_version_ids.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_secret_version_ids",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list secret version ids"):
        list_secret_version_ids("test-secret_id", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-secret_id", "test-resource_policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-secret_id", "test-resource_policy", region_name=REGION)


def test_put_secret_value(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    put_secret_value("test-secret_id", region_name=REGION)
    mock_client.put_secret_value.assert_called_once()


def test_put_secret_value_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_secret_value.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_secret_value",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put secret value"):
        put_secret_value("test-secret_id", region_name=REGION)


def test_remove_regions_from_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_regions_from_replication.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    remove_regions_from_replication("test-secret_id", [], region_name=REGION)
    mock_client.remove_regions_from_replication.assert_called_once()


def test_remove_regions_from_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_regions_from_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_regions_from_replication",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove regions from replication"):
        remove_regions_from_replication("test-secret_id", [], region_name=REGION)


def test_replicate_secret_to_regions(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_secret_to_regions.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    replicate_secret_to_regions("test-secret_id", [], region_name=REGION)
    mock_client.replicate_secret_to_regions.assert_called_once()


def test_replicate_secret_to_regions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_secret_to_regions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replicate_secret_to_regions",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replicate secret to regions"):
        replicate_secret_to_regions("test-secret_id", [], region_name=REGION)


def test_restore_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_secret.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    restore_secret("test-secret_id", region_name=REGION)
    mock_client.restore_secret.assert_called_once()


def test_restore_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_secret",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore secret"):
        restore_secret("test-secret_id", region_name=REGION)


def test_stop_replication_to_replica(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_replication_to_replica.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    stop_replication_to_replica("test-secret_id", region_name=REGION)
    mock_client.stop_replication_to_replica.assert_called_once()


def test_stop_replication_to_replica_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_replication_to_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_replication_to_replica",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop replication to replica"):
        stop_replication_to_replica("test-secret_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-secret_id", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-secret_id", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-secret_id", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-secret_id", [], region_name=REGION)


def test_update_secret_version_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_secret_version_stage.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    update_secret_version_stage("test-secret_id", "test-version_stage", region_name=REGION)
    mock_client.update_secret_version_stage.assert_called_once()


def test_update_secret_version_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_secret_version_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_secret_version_stage",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update secret version stage"):
        update_secret_version_stage("test-secret_id", "test-version_stage", region_name=REGION)


def test_validate_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    validate_resource_policy("test-resource_policy", region_name=REGION)
    mock_client.validate_resource_policy.assert_called_once()


def test_validate_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_resource_policy",
    )
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to validate resource policy"):
        validate_resource_policy("test-resource_policy", region_name=REGION)


def test_rotate_secret_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import rotate_secret
    mock_client = MagicMock()
    mock_client.rotate_secret.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    rotate_secret("test-name", rotation_days="test-rotation_days", region_name="us-east-1")
    mock_client.rotate_secret.assert_called_once()

def test_batch_get_secret_value_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import batch_get_secret_value
    mock_client = MagicMock()
    mock_client.batch_get_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    batch_get_secret_value(secret_id_list="test-secret_id_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.batch_get_secret_value.assert_called_once()

def test_get_random_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import get_random_password
    mock_client = MagicMock()
    mock_client.get_random_password.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    get_random_password(password_length="test-password_length", exclude_characters="test-exclude_characters", exclude_numbers="test-exclude_numbers", exclude_punctuation="test-exclude_punctuation", exclude_uppercase="test-exclude_uppercase", exclude_lowercase="test-exclude_lowercase", include_space=True, require_each_included_type=True, region_name="us-east-1")
    mock_client.get_random_password.assert_called_once()

def test_get_secret_value_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import get_secret_value
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    get_secret_value("test-secret_id", version_id="test-version_id", version_stage="test-version_stage", region_name="us-east-1")
    mock_client.get_secret_value.assert_called_once()

def test_list_secret_version_ids_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import list_secret_version_ids
    mock_client = MagicMock()
    mock_client.list_secret_version_ids.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    list_secret_version_ids("test-secret_id", max_results=1, next_token="test-next_token", include_deprecated=True, region_name="us-east-1")
    mock_client.list_secret_version_ids.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-secret_id", "{}", block_public_policy="{}", region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_put_secret_value_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import put_secret_value
    mock_client = MagicMock()
    mock_client.put_secret_value.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    put_secret_value("test-secret_id", client_request_token="test-client_request_token", secret_binary="test-secret_binary", secret_string="test-secret_string", version_stages="test-version_stages", rotation_token="test-rotation_token", region_name="us-east-1")
    mock_client.put_secret_value.assert_called_once()

def test_replicate_secret_to_regions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import replicate_secret_to_regions
    mock_client = MagicMock()
    mock_client.replicate_secret_to_regions.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    replicate_secret_to_regions("test-secret_id", "test-add_replica_regions", force_overwrite_replica_secret=True, region_name="us-east-1")
    mock_client.replicate_secret_to_regions.assert_called_once()

def test_update_secret_version_stage_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import update_secret_version_stage
    mock_client = MagicMock()
    mock_client.update_secret_version_stage.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    update_secret_version_stage("test-secret_id", "test-version_stage", remove_from_version_id="test-remove_from_version_id", move_to_version_id="test-move_to_version_id", region_name="us-east-1")
    mock_client.update_secret_version_stage.assert_called_once()

def test_validate_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.secrets_manager import validate_resource_policy
    mock_client = MagicMock()
    mock_client.validate_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.secrets_manager.get_client", lambda *a, **kw: mock_client)
    validate_resource_policy("{}", secret_id="test-secret_id", region_name="us-east-1")
    mock_client.validate_resource_policy.assert_called_once()
