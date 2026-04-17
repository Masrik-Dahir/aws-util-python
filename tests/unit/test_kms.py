"""Tests for aws_util.kms module."""
from __future__ import annotations

import boto3
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.kms import (
    DataKey,
    EncryptResult,
    decrypt,
    decrypt_data_key,
    encrypt,
    envelope_decrypt,
    envelope_encrypt,
    generate_data_key,
    re_encrypt,
    cancel_key_deletion,
    connect_custom_key_store,
    create_alias,
    create_custom_key_store,
    create_grant,
    create_key,
    delete_alias,
    delete_custom_key_store,
    delete_imported_key_material,
    derive_shared_secret,
    describe_custom_key_stores,
    describe_key,
    disable_key,
    disable_key_rotation,
    disconnect_custom_key_store,
    enable_key,
    enable_key_rotation,
    generate_data_key_pair,
    generate_data_key_pair_without_plaintext,
    generate_data_key_without_plaintext,
    generate_mac,
    generate_random,
    get_key_policy,
    get_key_rotation_status,
    get_parameters_for_import,
    get_public_key,
    import_key_material,
    list_aliases,
    list_grants,
    list_key_policies,
    list_key_rotations,
    list_keys,
    list_resource_tags,
    list_retirable_grants,
    put_key_policy,
    replicate_key,
    retire_grant,
    revoke_grant,
    rotate_key_on_demand,
    schedule_key_deletion,
    sign,
    tag_resource,
    untag_resource,
    update_alias,
    update_custom_key_store,
    update_key_description,
    update_primary_region,
    verify,
    verify_mac,
)

REGION = "us-east-1"


@pytest.fixture
def kms_key_id(kms_key):
    _, key_id = kms_key
    return key_id


@pytest.fixture
def kms_key_id_2():
    client = boto3.client("kms", region_name=REGION)
    resp = client.create_key(Description="second-key")
    return resp["KeyMetadata"]["KeyId"]


# ---------------------------------------------------------------------------
# encrypt / decrypt
# ---------------------------------------------------------------------------


def test_encrypt_bytes(kms_key_id):
    result = encrypt(kms_key_id, b"hello bytes", region_name=REGION)
    assert isinstance(result, EncryptResult)
    assert result.ciphertext_blob
    assert result.key_id


def test_encrypt_string(kms_key_id):
    result = encrypt(kms_key_id, "hello string", region_name=REGION)
    assert result.ciphertext_blob


def test_encrypt_decrypt_roundtrip(kms_key_id):
    plaintext = b"secret data"
    enc = encrypt(kms_key_id, plaintext, region_name=REGION)
    dec = decrypt(enc.ciphertext_blob, region_name=REGION)
    assert dec == plaintext


def test_encrypt_decrypt_string_roundtrip(kms_key_id):
    enc = encrypt(kms_key_id, "my-secret", region_name=REGION)
    dec = decrypt(enc.ciphertext_blob, region_name=REGION)
    assert dec == b"my-secret"


def test_decrypt_with_key_id(kms_key_id):
    enc = encrypt(kms_key_id, b"data", region_name=REGION)
    dec = decrypt(enc.ciphertext_blob, key_id=kms_key_id, region_name=REGION)
    assert dec == b"data"


def test_encrypt_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.kms as kmsmod

    mock_client = MagicMock()
    mock_client.encrypt.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "key not found"}},
        "Encrypt",
    )
    monkeypatch.setattr(kmsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to encrypt"):
        encrypt("nonexistent-key", "data", region_name=REGION)


def test_decrypt_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.kms as kmsmod

    mock_client = MagicMock()
    mock_client.decrypt.side_effect = ClientError(
        {"Error": {"Code": "InvalidCiphertextException", "Message": "bad ciphertext"}},
        "Decrypt",
    )
    monkeypatch.setattr(kmsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="KMS decryption failed"):
        decrypt(b"bad-ciphertext", region_name=REGION)


# ---------------------------------------------------------------------------
# generate_data_key
# ---------------------------------------------------------------------------


def test_generate_data_key(kms_key_id):
    result = generate_data_key(kms_key_id, region_name=REGION)
    assert isinstance(result, DataKey)
    assert result.plaintext
    assert result.ciphertext_blob
    assert result.key_id


def test_generate_data_key_aes128(kms_key_id):
    result = generate_data_key(kms_key_id, key_spec="AES_128", region_name=REGION)
    assert result.plaintext


def test_generate_data_key_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.kms as kmsmod

    mock_client = MagicMock()
    mock_client.generate_data_key.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "key not found"}},
        "GenerateDataKey",
    )
    monkeypatch.setattr(kmsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate data key"):
        generate_data_key("nonexistent-key", region_name=REGION)


# ---------------------------------------------------------------------------
# envelope_encrypt / envelope_decrypt
# ---------------------------------------------------------------------------


def test_envelope_encrypt_returns_ciphertext_and_key(kms_key_id):
    result = envelope_encrypt(kms_key_id, b"sensitive data", region_name=REGION)
    assert "ciphertext" in result
    assert "encrypted_data_key" in result
    assert len(result["ciphertext"]) > 12  # nonce + data


def test_envelope_encrypt_string_input(kms_key_id):
    result = envelope_encrypt(kms_key_id, "string data", region_name=REGION)
    assert result["ciphertext"]


def test_envelope_encrypt_decrypt_roundtrip(kms_key_id):
    plaintext = b"top secret message"
    enc = envelope_encrypt(kms_key_id, plaintext, region_name=REGION)
    dec = envelope_decrypt(
        enc["ciphertext"],
        enc["encrypted_data_key"],
        region_name=REGION,
    )
    assert dec == plaintext


def test_envelope_decrypt_bad_ciphertext(kms_key_id):
    enc = envelope_encrypt(kms_key_id, b"data", region_name=REGION)
    # Corrupt the ciphertext (keep nonce, corrupt data)
    corrupted = enc["ciphertext"][:12] + b"\x00" * 100
    with pytest.raises(RuntimeError, match="envelope_decrypt failed"):
        envelope_decrypt(corrupted, enc["encrypted_data_key"], region_name=REGION)


# ---------------------------------------------------------------------------
# re_encrypt
# ---------------------------------------------------------------------------


def test_re_encrypt(kms_key_id, kms_key_id_2):
    enc = encrypt(kms_key_id, b"data-to-reencrypt", region_name=REGION)
    result = re_encrypt(
        enc.ciphertext_blob,
        destination_key_id=kms_key_id_2,
        region_name=REGION,
    )
    assert isinstance(result, EncryptResult)
    assert result.ciphertext_blob


def test_re_encrypt_with_source_key(kms_key_id, kms_key_id_2):
    enc = encrypt(kms_key_id, b"data", region_name=REGION)
    result = re_encrypt(
        enc.ciphertext_blob,
        destination_key_id=kms_key_id_2,
        source_key_id=kms_key_id,
        region_name=REGION,
    )
    assert result.ciphertext_blob


def test_re_encrypt_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.kms as kmsmod

    mock_client = MagicMock()
    mock_client.re_encrypt.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "key not found"}},
        "ReEncrypt",
    )
    monkeypatch.setattr(kmsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to re-encrypt"):
        re_encrypt(b"ciphertext", "dest-key-id", region_name=REGION)


# ---------------------------------------------------------------------------
# decrypt_data_key (convenience wrapper)
# ---------------------------------------------------------------------------


def test_decrypt_data_key(kms_key_id):
    data_key = generate_data_key(kms_key_id, region_name=REGION)
    result = decrypt_data_key(data_key.ciphertext_blob, region_name=REGION)
    assert result == data_key.plaintext


def test_cancel_key_deletion(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_key_deletion.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    cancel_key_deletion("test-key_id", region_name=REGION)
    mock_client.cancel_key_deletion.assert_called_once()


def test_cancel_key_deletion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_key_deletion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_key_deletion",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel key deletion"):
        cancel_key_deletion("test-key_id", region_name=REGION)


def test_connect_custom_key_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.connect_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    connect_custom_key_store("test-custom_key_store_id", region_name=REGION)
    mock_client.connect_custom_key_store.assert_called_once()


def test_connect_custom_key_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.connect_custom_key_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "connect_custom_key_store",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to connect custom key store"):
        connect_custom_key_store("test-custom_key_store_id", region_name=REGION)


def test_create_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_alias.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_alias("test-alias_name", "test-target_key_id", region_name=REGION)
    mock_client.create_alias.assert_called_once()


def test_create_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_alias",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create alias"):
        create_alias("test-alias_name", "test-target_key_id", region_name=REGION)


def test_create_custom_key_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_custom_key_store("test-custom_key_store_name", region_name=REGION)
    mock_client.create_custom_key_store.assert_called_once()


def test_create_custom_key_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_key_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_key_store",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom key store"):
        create_custom_key_store("test-custom_key_store_name", region_name=REGION)


def test_create_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_grant.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_grant("test-key_id", "test-grantee_principal", [], region_name=REGION)
    mock_client.create_grant.assert_called_once()


def test_create_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_grant",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create grant"):
        create_grant("test-key_id", "test-grantee_principal", [], region_name=REGION)


def test_create_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_key(region_name=REGION)
    mock_client.create_key.assert_called_once()


def test_create_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create key"):
        create_key(region_name=REGION)


def test_delete_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_alias.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    delete_alias("test-alias_name", region_name=REGION)
    mock_client.delete_alias.assert_called_once()


def test_delete_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_alias",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete alias"):
        delete_alias("test-alias_name", region_name=REGION)


def test_delete_custom_key_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    delete_custom_key_store("test-custom_key_store_id", region_name=REGION)
    mock_client.delete_custom_key_store.assert_called_once()


def test_delete_custom_key_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_key_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_key_store",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom key store"):
        delete_custom_key_store("test-custom_key_store_id", region_name=REGION)


def test_delete_imported_key_material(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_imported_key_material.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    delete_imported_key_material("test-key_id", region_name=REGION)
    mock_client.delete_imported_key_material.assert_called_once()


def test_delete_imported_key_material_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_imported_key_material.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_imported_key_material",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete imported key material"):
        delete_imported_key_material("test-key_id", region_name=REGION)


def test_derive_shared_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.derive_shared_secret.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", region_name=REGION)
    mock_client.derive_shared_secret.assert_called_once()


def test_derive_shared_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.derive_shared_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "derive_shared_secret",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to derive shared secret"):
        derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", region_name=REGION)


def test_describe_custom_key_stores(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_key_stores.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    describe_custom_key_stores(region_name=REGION)
    mock_client.describe_custom_key_stores.assert_called_once()


def test_describe_custom_key_stores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_key_stores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_key_stores",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe custom key stores"):
        describe_custom_key_stores(region_name=REGION)


def test_describe_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    describe_key("test-key_id", region_name=REGION)
    mock_client.describe_key.assert_called_once()


def test_describe_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe key"):
        describe_key("test-key_id", region_name=REGION)


def test_disable_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    disable_key("test-key_id", region_name=REGION)
    mock_client.disable_key.assert_called_once()


def test_disable_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable key"):
        disable_key("test-key_id", region_name=REGION)


def test_disable_key_rotation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_key_rotation.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    disable_key_rotation("test-key_id", region_name=REGION)
    mock_client.disable_key_rotation.assert_called_once()


def test_disable_key_rotation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_key_rotation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_key_rotation",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable key rotation"):
        disable_key_rotation("test-key_id", region_name=REGION)


def test_disconnect_custom_key_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.disconnect_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    disconnect_custom_key_store("test-custom_key_store_id", region_name=REGION)
    mock_client.disconnect_custom_key_store.assert_called_once()


def test_disconnect_custom_key_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disconnect_custom_key_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disconnect_custom_key_store",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disconnect custom key store"):
        disconnect_custom_key_store("test-custom_key_store_id", region_name=REGION)


def test_enable_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    enable_key("test-key_id", region_name=REGION)
    mock_client.enable_key.assert_called_once()


def test_enable_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable key"):
        enable_key("test-key_id", region_name=REGION)


def test_enable_key_rotation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_key_rotation.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    enable_key_rotation("test-key_id", region_name=REGION)
    mock_client.enable_key_rotation.assert_called_once()


def test_enable_key_rotation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_key_rotation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_key_rotation",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable key rotation"):
        enable_key_rotation("test-key_id", region_name=REGION)


def test_generate_data_key_pair(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_pair("test-key_id", "test-key_pair_spec", region_name=REGION)
    mock_client.generate_data_key_pair.assert_called_once()


def test_generate_data_key_pair_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_data_key_pair",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate data key pair"):
        generate_data_key_pair("test-key_id", "test-key_pair_spec", region_name=REGION)


def test_generate_data_key_pair_without_plaintext(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_pair_without_plaintext.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", region_name=REGION)
    mock_client.generate_data_key_pair_without_plaintext.assert_called_once()


def test_generate_data_key_pair_without_plaintext_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_pair_without_plaintext.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_data_key_pair_without_plaintext",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate data key pair without plaintext"):
        generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", region_name=REGION)


def test_generate_data_key_without_plaintext(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_without_plaintext.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_without_plaintext("test-key_id", region_name=REGION)
    mock_client.generate_data_key_without_plaintext.assert_called_once()


def test_generate_data_key_without_plaintext_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_data_key_without_plaintext.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_data_key_without_plaintext",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate data key without plaintext"):
        generate_data_key_without_plaintext("test-key_id", region_name=REGION)


def test_generate_mac(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_mac.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_mac("test-message", "test-key_id", "test-mac_algorithm", region_name=REGION)
    mock_client.generate_mac.assert_called_once()


def test_generate_mac_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_mac.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_mac",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate mac"):
        generate_mac("test-message", "test-key_id", "test-mac_algorithm", region_name=REGION)


def test_generate_random(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_random.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_random(region_name=REGION)
    mock_client.generate_random.assert_called_once()


def test_generate_random_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_random.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_random",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate random"):
        generate_random(region_name=REGION)


def test_get_key_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_policy.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_key_policy("test-key_id", region_name=REGION)
    mock_client.get_key_policy.assert_called_once()


def test_get_key_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_policy",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get key policy"):
        get_key_policy("test-key_id", region_name=REGION)


def test_get_key_rotation_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_rotation_status.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_key_rotation_status("test-key_id", region_name=REGION)
    mock_client.get_key_rotation_status.assert_called_once()


def test_get_key_rotation_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_key_rotation_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_rotation_status",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get key rotation status"):
        get_key_rotation_status("test-key_id", region_name=REGION)


def test_get_parameters_for_import(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameters_for_import.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_parameters_for_import("test-key_id", "test-wrapping_algorithm", "test-wrapping_key_spec", region_name=REGION)
    mock_client.get_parameters_for_import.assert_called_once()


def test_get_parameters_for_import_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameters_for_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_parameters_for_import",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get parameters for import"):
        get_parameters_for_import("test-key_id", "test-wrapping_algorithm", "test-wrapping_key_spec", region_name=REGION)


def test_get_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_public_key("test-key_id", region_name=REGION)
    mock_client.get_public_key.assert_called_once()


def test_get_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_public_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get public key"):
        get_public_key("test-key_id", region_name=REGION)


def test_import_key_material(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_key_material.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    import_key_material("test-key_id", "test-import_token", "test-encrypted_key_material", region_name=REGION)
    mock_client.import_key_material.assert_called_once()


def test_import_key_material_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_key_material.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_key_material",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import key material"):
        import_key_material("test-key_id", "test-import_token", "test-encrypted_key_material", region_name=REGION)


def test_list_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aliases.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_aliases(region_name=REGION)
    mock_client.list_aliases.assert_called_once()


def test_list_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aliases",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aliases"):
        list_aliases(region_name=REGION)


def test_list_grants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_grants.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_grants("test-key_id", region_name=REGION)
    mock_client.list_grants.assert_called_once()


def test_list_grants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_grants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_grants",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list grants"):
        list_grants("test-key_id", region_name=REGION)


def test_list_key_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_policies.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_key_policies("test-key_id", region_name=REGION)
    mock_client.list_key_policies.assert_called_once()


def test_list_key_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_key_policies",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list key policies"):
        list_key_policies("test-key_id", region_name=REGION)


def test_list_key_rotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_rotations.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_key_rotations("test-key_id", region_name=REGION)
    mock_client.list_key_rotations.assert_called_once()


def test_list_key_rotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_rotations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_key_rotations",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list key rotations"):
        list_key_rotations("test-key_id", region_name=REGION)


def test_list_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_keys.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_keys(region_name=REGION)
    mock_client.list_keys.assert_called_once()


def test_list_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_keys",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list keys"):
        list_keys(region_name=REGION)


def test_list_resource_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_tags.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_resource_tags("test-key_id", region_name=REGION)
    mock_client.list_resource_tags.assert_called_once()


def test_list_resource_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_tags",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource tags"):
        list_resource_tags("test-key_id", region_name=REGION)


def test_list_retirable_grants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_retirable_grants.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_retirable_grants("test-retiring_principal", region_name=REGION)
    mock_client.list_retirable_grants.assert_called_once()


def test_list_retirable_grants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_retirable_grants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_retirable_grants",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list retirable grants"):
        list_retirable_grants("test-retiring_principal", region_name=REGION)


def test_put_key_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_key_policy.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    put_key_policy("test-key_id", "test-policy", region_name=REGION)
    mock_client.put_key_policy.assert_called_once()


def test_put_key_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_key_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_key_policy",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put key policy"):
        put_key_policy("test-key_id", "test-policy", region_name=REGION)


def test_replicate_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    replicate_key("test-key_id", "test-replica_region", region_name=REGION)
    mock_client.replicate_key.assert_called_once()


def test_replicate_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replicate_key",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replicate key"):
        replicate_key("test-key_id", "test-replica_region", region_name=REGION)


def test_retire_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.retire_grant.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    retire_grant(region_name=REGION)
    mock_client.retire_grant.assert_called_once()


def test_retire_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retire_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retire_grant",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to retire grant"):
        retire_grant(region_name=REGION)


def test_revoke_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_grant.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    revoke_grant("test-key_id", "test-grant_id", region_name=REGION)
    mock_client.revoke_grant.assert_called_once()


def test_revoke_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_grant",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke grant"):
        revoke_grant("test-key_id", "test-grant_id", region_name=REGION)


def test_rotate_key_on_demand(monkeypatch):
    mock_client = MagicMock()
    mock_client.rotate_key_on_demand.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    rotate_key_on_demand("test-key_id", region_name=REGION)
    mock_client.rotate_key_on_demand.assert_called_once()


def test_rotate_key_on_demand_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rotate_key_on_demand.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rotate_key_on_demand",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rotate key on demand"):
        rotate_key_on_demand("test-key_id", region_name=REGION)


def test_schedule_key_deletion(monkeypatch):
    mock_client = MagicMock()
    mock_client.schedule_key_deletion.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    schedule_key_deletion("test-key_id", region_name=REGION)
    mock_client.schedule_key_deletion.assert_called_once()


def test_schedule_key_deletion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.schedule_key_deletion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "schedule_key_deletion",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to schedule key deletion"):
        schedule_key_deletion("test-key_id", region_name=REGION)


def test_sign(monkeypatch):
    mock_client = MagicMock()
    mock_client.sign.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    sign("test-key_id", "test-message", "test-signing_algorithm", region_name=REGION)
    mock_client.sign.assert_called_once()


def test_sign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.sign.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "sign",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to sign"):
        sign("test-key_id", "test-message", "test-signing_algorithm", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-key_id", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-key_id", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-key_id", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-key_id", [], region_name=REGION)


def test_update_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_alias.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    update_alias("test-alias_name", "test-target_key_id", region_name=REGION)
    mock_client.update_alias.assert_called_once()


def test_update_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_alias",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update alias"):
        update_alias("test-alias_name", "test-target_key_id", region_name=REGION)


def test_update_custom_key_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    update_custom_key_store("test-custom_key_store_id", region_name=REGION)
    mock_client.update_custom_key_store.assert_called_once()


def test_update_custom_key_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_key_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_key_store",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update custom key store"):
        update_custom_key_store("test-custom_key_store_id", region_name=REGION)


def test_update_key_description(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_description.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    update_key_description("test-key_id", "test-description", region_name=REGION)
    mock_client.update_key_description.assert_called_once()


def test_update_key_description_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_description.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_key_description",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update key description"):
        update_key_description("test-key_id", "test-description", region_name=REGION)


def test_update_primary_region(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_primary_region.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    update_primary_region("test-key_id", "test-primary_region", region_name=REGION)
    mock_client.update_primary_region.assert_called_once()


def test_update_primary_region_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_primary_region.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_primary_region",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update primary region"):
        update_primary_region("test-key_id", "test-primary_region", region_name=REGION)


def test_verify(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", region_name=REGION)
    mock_client.verify.assert_called_once()


def test_verify_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify"):
        verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", region_name=REGION)


def test_verify_mac(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_mac.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", region_name=REGION)
    mock_client.verify_mac.assert_called_once()


def test_verify_mac_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_mac.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_mac",
    )
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify mac"):
        verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", region_name=REGION)


def test_create_custom_key_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import create_custom_key_store
    mock_client = MagicMock()
    mock_client.create_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_custom_key_store("test-custom_key_store_name", cloud_hsm_cluster_id="test-cloud_hsm_cluster_id", trust_anchor_certificate="test-trust_anchor_certificate", key_store_password="test-key_store_password", custom_key_store_type="test-custom_key_store_type", xks_proxy_uri_endpoint="test-xks_proxy_uri_endpoint", xks_proxy_uri_path="test-xks_proxy_uri_path", xks_proxy_vpc_endpoint_service_name="test-xks_proxy_vpc_endpoint_service_name", xks_proxy_vpc_endpoint_service_owner="test-xks_proxy_vpc_endpoint_service_owner", xks_proxy_authentication_credential="test-xks_proxy_authentication_credential", xks_proxy_connectivity="test-xks_proxy_connectivity", region_name="us-east-1")
    mock_client.create_custom_key_store.assert_called_once()

def test_create_grant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import create_grant
    mock_client = MagicMock()
    mock_client.create_grant.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_grant("test-key_id", "test-grantee_principal", "test-operations", retiring_principal="test-retiring_principal", constraints="test-constraints", grant_tokens="test-grant_tokens", name="test-name", region_name="us-east-1")
    mock_client.create_grant.assert_called_once()

def test_create_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import create_key
    mock_client = MagicMock()
    mock_client.create_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    create_key(policy="{}", description="test-description", key_usage="test-key_usage", customer_master_key_spec="test-customer_master_key_spec", key_spec="test-key_spec", origin="test-origin", custom_key_store_id="test-custom_key_store_id", bypass_policy_lockout_safety_check=True, tags=[{"Key": "k", "Value": "v"}], multi_region=True, xks_key_id="test-xks_key_id", region_name="us-east-1")
    mock_client.create_key.assert_called_once()

def test_delete_imported_key_material_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import delete_imported_key_material
    mock_client = MagicMock()
    mock_client.delete_imported_key_material.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    delete_imported_key_material("test-key_id", key_material_id="test-key_material_id", region_name="us-east-1")
    mock_client.delete_imported_key_material.assert_called_once()

def test_derive_shared_secret_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import derive_shared_secret
    mock_client = MagicMock()
    mock_client.derive_shared_secret.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", grant_tokens="test-grant_tokens", recipient="test-recipient", region_name="us-east-1")
    mock_client.derive_shared_secret.assert_called_once()

def test_describe_custom_key_stores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import describe_custom_key_stores
    mock_client = MagicMock()
    mock_client.describe_custom_key_stores.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    describe_custom_key_stores(custom_key_store_id="test-custom_key_store_id", custom_key_store_name="test-custom_key_store_name", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_custom_key_stores.assert_called_once()

def test_describe_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import describe_key
    mock_client = MagicMock()
    mock_client.describe_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    describe_key("test-key_id", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.describe_key.assert_called_once()

def test_enable_key_rotation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import enable_key_rotation
    mock_client = MagicMock()
    mock_client.enable_key_rotation.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    enable_key_rotation("test-key_id", rotation_period_in_days="test-rotation_period_in_days", region_name="us-east-1")
    mock_client.enable_key_rotation.assert_called_once()

def test_generate_data_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import generate_data_key_pair
    mock_client = MagicMock()
    mock_client.generate_data_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_pair("test-key_id", "test-key_pair_spec", encryption_context={}, grant_tokens="test-grant_tokens", recipient="test-recipient", region_name="us-east-1")
    mock_client.generate_data_key_pair.assert_called_once()

def test_generate_data_key_pair_without_plaintext_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import generate_data_key_pair_without_plaintext
    mock_client = MagicMock()
    mock_client.generate_data_key_pair_without_plaintext.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", encryption_context={}, grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.generate_data_key_pair_without_plaintext.assert_called_once()

def test_generate_data_key_without_plaintext_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import generate_data_key_without_plaintext
    mock_client = MagicMock()
    mock_client.generate_data_key_without_plaintext.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_data_key_without_plaintext("test-key_id", encryption_context={}, key_spec="test-key_spec", number_of_bytes="test-number_of_bytes", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.generate_data_key_without_plaintext.assert_called_once()

def test_generate_mac_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import generate_mac
    mock_client = MagicMock()
    mock_client.generate_mac.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_mac("test-message", "test-key_id", "test-mac_algorithm", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.generate_mac.assert_called_once()

def test_generate_random_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import generate_random
    mock_client = MagicMock()
    mock_client.generate_random.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    generate_random(number_of_bytes="test-number_of_bytes", custom_key_store_id="test-custom_key_store_id", recipient="test-recipient", region_name="us-east-1")
    mock_client.generate_random.assert_called_once()

def test_get_key_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import get_key_policy
    mock_client = MagicMock()
    mock_client.get_key_policy.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_key_policy("test-key_id", policy_name="test-policy_name", region_name="us-east-1")
    mock_client.get_key_policy.assert_called_once()

def test_get_public_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import get_public_key
    mock_client = MagicMock()
    mock_client.get_public_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    get_public_key("test-key_id", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.get_public_key.assert_called_once()

def test_import_key_material_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import import_key_material
    mock_client = MagicMock()
    mock_client.import_key_material.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    import_key_material("test-key_id", 1, True, valid_to="test-valid_to", expiration_model="test-expiration_model", import_type=1, key_material_description="test-key_material_description", key_material_id="test-key_material_id", region_name="us-east-1")
    mock_client.import_key_material.assert_called_once()

def test_list_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_aliases
    mock_client = MagicMock()
    mock_client.list_aliases.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_aliases(key_id="test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_aliases.assert_called_once()

def test_list_grants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_grants
    mock_client = MagicMock()
    mock_client.list_grants.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_grants("test-key_id", limit=1, marker="test-marker", grant_id="test-grant_id", grantee_principal="test-grantee_principal", region_name="us-east-1")
    mock_client.list_grants.assert_called_once()

def test_list_key_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_key_policies
    mock_client = MagicMock()
    mock_client.list_key_policies.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_key_policies("test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_key_policies.assert_called_once()

def test_list_key_rotations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_key_rotations
    mock_client = MagicMock()
    mock_client.list_key_rotations.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_key_rotations("test-key_id", include_key_material=True, limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_key_rotations.assert_called_once()

def test_list_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_keys
    mock_client = MagicMock()
    mock_client.list_keys.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_keys(limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_keys.assert_called_once()

def test_list_resource_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_resource_tags
    mock_client = MagicMock()
    mock_client.list_resource_tags.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_resource_tags("test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_resource_tags.assert_called_once()

def test_list_retirable_grants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import list_retirable_grants
    mock_client = MagicMock()
    mock_client.list_retirable_grants.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    list_retirable_grants("test-retiring_principal", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_retirable_grants.assert_called_once()

def test_put_key_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import put_key_policy
    mock_client = MagicMock()
    mock_client.put_key_policy.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    put_key_policy("test-key_id", "{}", policy_name="test-policy_name", bypass_policy_lockout_safety_check=True, region_name="us-east-1")
    mock_client.put_key_policy.assert_called_once()

def test_replicate_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import replicate_key
    mock_client = MagicMock()
    mock_client.replicate_key.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    replicate_key("test-key_id", "test-replica_region", policy="{}", bypass_policy_lockout_safety_check=True, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.replicate_key.assert_called_once()

def test_retire_grant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import retire_grant
    mock_client = MagicMock()
    mock_client.retire_grant.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    retire_grant(grant_token="test-grant_token", key_id="test-key_id", grant_id="test-grant_id", region_name="us-east-1")
    mock_client.retire_grant.assert_called_once()

def test_schedule_key_deletion_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import schedule_key_deletion
    mock_client = MagicMock()
    mock_client.schedule_key_deletion.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    schedule_key_deletion("test-key_id", pending_window_in_days="test-pending_window_in_days", region_name="us-east-1")
    mock_client.schedule_key_deletion.assert_called_once()

def test_sign_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import sign
    mock_client = MagicMock()
    mock_client.sign.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    sign("test-key_id", "test-message", "test-signing_algorithm", message_type="test-message_type", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.sign.assert_called_once()

def test_update_custom_key_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import update_custom_key_store
    mock_client = MagicMock()
    mock_client.update_custom_key_store.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    update_custom_key_store("test-custom_key_store_id", new_custom_key_store_name="test-new_custom_key_store_name", key_store_password="test-key_store_password", cloud_hsm_cluster_id="test-cloud_hsm_cluster_id", xks_proxy_uri_endpoint="test-xks_proxy_uri_endpoint", xks_proxy_uri_path="test-xks_proxy_uri_path", xks_proxy_vpc_endpoint_service_name="test-xks_proxy_vpc_endpoint_service_name", xks_proxy_vpc_endpoint_service_owner="test-xks_proxy_vpc_endpoint_service_owner", xks_proxy_authentication_credential="test-xks_proxy_authentication_credential", xks_proxy_connectivity="test-xks_proxy_connectivity", region_name="us-east-1")
    mock_client.update_custom_key_store.assert_called_once()

def test_verify_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import verify
    mock_client = MagicMock()
    mock_client.verify.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", message_type="test-message_type", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.verify.assert_called_once()

def test_verify_mac_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kms import verify_mac
    mock_client = MagicMock()
    mock_client.verify_mac.return_value = {}
    monkeypatch.setattr("aws_util.kms.get_client", lambda *a, **kw: mock_client)
    verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.verify_mac.assert_called_once()
