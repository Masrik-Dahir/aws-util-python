"""Tests for aws_util.aio.kms — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.kms import (
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


def _mc(return_value=None, side_effect=None):
    c = AsyncMock()
    if side_effect:
        c.call.side_effect = side_effect
    else:
        c.call.return_value = return_value or {}
    return c


# ---------------------------------------------------------------------------
# encrypt
# ---------------------------------------------------------------------------


async def test_encrypt_string(monkeypatch):
    mc = _mc({"CiphertextBlob": b"ct", "KeyId": "k1", "EncryptionAlgorithm": "SYMMETRIC_DEFAULT"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await encrypt("k1", "hello")
    assert isinstance(r, EncryptResult)
    assert r.ciphertext_blob == b"ct"
    assert r.key_id == "k1"


async def test_encrypt_bytes(monkeypatch):
    mc = _mc({"CiphertextBlob": b"ct", "KeyId": "k1"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await encrypt("k1", b"raw")
    assert r.encryption_algorithm == "SYMMETRIC_DEFAULT"  # fallback via .get


async def test_encrypt_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to encrypt"):
        await encrypt("k1", "x")


# ---------------------------------------------------------------------------
# decrypt
# ---------------------------------------------------------------------------


async def test_decrypt_basic(monkeypatch):
    mc = _mc({"Plaintext": b"plain"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    assert await decrypt(b"ct") == b"plain"


async def test_decrypt_with_key_id(monkeypatch):
    mc = _mc({"Plaintext": b"p"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    await decrypt(b"ct", key_id="k2")
    assert "KeyId" in mc.call.call_args[1]


async def test_decrypt_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("bad"))
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="KMS decryption failed"):
        await decrypt(b"ct")


# ---------------------------------------------------------------------------
# generate_data_key
# ---------------------------------------------------------------------------


async def test_generate_data_key(monkeypatch):
    mc = _mc({"Plaintext": b"dk", "CiphertextBlob": b"edk", "KeyId": "k1"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await generate_data_key("k1")
    assert isinstance(r, DataKey)
    assert r.plaintext == b"dk"


async def test_generate_data_key_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("nope"))
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to generate data key"):
        await generate_data_key("k1")


# ---------------------------------------------------------------------------
# envelope_encrypt / envelope_decrypt
# ---------------------------------------------------------------------------


async def test_envelope_encrypt(monkeypatch):
    mc = _mc({"Plaintext": b"\x00" * 32, "CiphertextBlob": b"edk", "KeyId": "k1"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await envelope_encrypt("k1", "hello")
    assert "ciphertext" in r
    assert "encrypted_data_key" in r
    assert r["encrypted_data_key"] == b"edk"


async def test_envelope_encrypt_bytes(monkeypatch):
    mc = _mc({"Plaintext": b"\x00" * 32, "CiphertextBlob": b"edk", "KeyId": "k1"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await envelope_encrypt("k1", b"raw")
    assert isinstance(r["ciphertext"], bytes)


async def test_envelope_decrypt(monkeypatch):
    # first encrypt
    key = b"\x00" * 32
    mc = _mc()
    mc.call.side_effect = [
        {"Plaintext": key, "CiphertextBlob": b"edk", "KeyId": "k1"},  # generate_data_key
    ]
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    enc = await envelope_encrypt("k1", b"test data")

    mc2 = _mc({"Plaintext": key})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc2)
    result = await envelope_decrypt(enc["ciphertext"], enc["encrypted_data_key"])
    assert result == b"test data"


async def test_envelope_decrypt_bad_data(monkeypatch):
    mc = _mc({"Plaintext": b"\x00" * 32})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="envelope_decrypt failed"):
        await envelope_decrypt(b"bad" * 10, b"edk")


# ---------------------------------------------------------------------------
# re_encrypt
# ---------------------------------------------------------------------------


async def test_re_encrypt(monkeypatch):
    mc = _mc({
        "CiphertextBlob": b"new_ct",
        "KeyId": "k2",
        "DestinationEncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    })
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await re_encrypt(b"ct", "k2")
    assert r.ciphertext_blob == b"new_ct"


async def test_re_encrypt_with_source(monkeypatch):
    mc = _mc({"CiphertextBlob": b"new_ct", "KeyId": "k2"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    r = await re_encrypt(b"ct", "k2", source_key_id="k1")
    assert r.encryption_algorithm == "SYMMETRIC_DEFAULT"  # fallback


async def test_re_encrypt_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to re-encrypt"):
        await re_encrypt(b"ct", "k2")


# ---------------------------------------------------------------------------
# decrypt_data_key
# ---------------------------------------------------------------------------


async def test_decrypt_data_key(monkeypatch):
    mc = _mc({"Plaintext": b"dk"})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mc)
    assert await decrypt_data_key(b"edk") == b"dk"


async def test_cancel_key_deletion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_key_deletion("test-key_id", )
    mock_client.call.assert_called_once()


async def test_cancel_key_deletion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_key_deletion("test-key_id", )


async def test_connect_custom_key_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await connect_custom_key_store("test-custom_key_store_id", )
    mock_client.call.assert_called_once()


async def test_connect_custom_key_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await connect_custom_key_store("test-custom_key_store_id", )


async def test_create_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_alias("test-alias_name", "test-target_key_id", )
    mock_client.call.assert_called_once()


async def test_create_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_alias("test-alias_name", "test-target_key_id", )


async def test_create_custom_key_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_key_store("test-custom_key_store_name", )
    mock_client.call.assert_called_once()


async def test_create_custom_key_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_key_store("test-custom_key_store_name", )


async def test_create_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_grant("test-key_id", "test-grantee_principal", [], )
    mock_client.call.assert_called_once()


async def test_create_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_grant("test-key_id", "test-grantee_principal", [], )


async def test_create_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_key()
    mock_client.call.assert_called_once()


async def test_create_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_key()


async def test_delete_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_alias("test-alias_name", )
    mock_client.call.assert_called_once()


async def test_delete_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_alias("test-alias_name", )


async def test_delete_custom_key_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_key_store("test-custom_key_store_id", )
    mock_client.call.assert_called_once()


async def test_delete_custom_key_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_key_store("test-custom_key_store_id", )


async def test_delete_imported_key_material(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_imported_key_material("test-key_id", )
    mock_client.call.assert_called_once()


async def test_delete_imported_key_material_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_imported_key_material("test-key_id", )


async def test_derive_shared_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", )
    mock_client.call.assert_called_once()


async def test_derive_shared_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", )


async def test_describe_custom_key_stores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_key_stores()
    mock_client.call.assert_called_once()


async def test_describe_custom_key_stores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_key_stores()


async def test_describe_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_key("test-key_id", )
    mock_client.call.assert_called_once()


async def test_describe_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_key("test-key_id", )


async def test_disable_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_key("test-key_id", )
    mock_client.call.assert_called_once()


async def test_disable_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_key("test-key_id", )


async def test_disable_key_rotation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_key_rotation("test-key_id", )
    mock_client.call.assert_called_once()


async def test_disable_key_rotation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_key_rotation("test-key_id", )


async def test_disconnect_custom_key_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await disconnect_custom_key_store("test-custom_key_store_id", )
    mock_client.call.assert_called_once()


async def test_disconnect_custom_key_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disconnect_custom_key_store("test-custom_key_store_id", )


async def test_enable_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_key("test-key_id", )
    mock_client.call.assert_called_once()


async def test_enable_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_key("test-key_id", )


async def test_enable_key_rotation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_key_rotation("test-key_id", )
    mock_client.call.assert_called_once()


async def test_enable_key_rotation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_key_rotation("test-key_id", )


async def test_generate_data_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_data_key_pair("test-key_id", "test-key_pair_spec", )
    mock_client.call.assert_called_once()


async def test_generate_data_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_data_key_pair("test-key_id", "test-key_pair_spec", )


async def test_generate_data_key_pair_without_plaintext(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", )
    mock_client.call.assert_called_once()


async def test_generate_data_key_pair_without_plaintext_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", )


async def test_generate_data_key_without_plaintext(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_data_key_without_plaintext("test-key_id", )
    mock_client.call.assert_called_once()


async def test_generate_data_key_without_plaintext_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_data_key_without_plaintext("test-key_id", )


async def test_generate_mac(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_mac("test-message", "test-key_id", "test-mac_algorithm", )
    mock_client.call.assert_called_once()


async def test_generate_mac_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_mac("test-message", "test-key_id", "test-mac_algorithm", )


async def test_generate_random(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_random()
    mock_client.call.assert_called_once()


async def test_generate_random_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_random()


async def test_get_key_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_key_policy("test-key_id", )
    mock_client.call.assert_called_once()


async def test_get_key_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_policy("test-key_id", )


async def test_get_key_rotation_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_key_rotation_status("test-key_id", )
    mock_client.call.assert_called_once()


async def test_get_key_rotation_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_rotation_status("test-key_id", )


async def test_get_parameters_for_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_parameters_for_import("test-key_id", "test-wrapping_algorithm", "test-wrapping_key_spec", )
    mock_client.call.assert_called_once()


async def test_get_parameters_for_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_parameters_for_import("test-key_id", "test-wrapping_algorithm", "test-wrapping_key_spec", )


async def test_get_public_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_public_key("test-key_id", )
    mock_client.call.assert_called_once()


async def test_get_public_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_public_key("test-key_id", )


async def test_import_key_material(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_key_material("test-key_id", "test-import_token", "test-encrypted_key_material", )
    mock_client.call.assert_called_once()


async def test_import_key_material_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_key_material("test-key_id", "test-import_token", "test-encrypted_key_material", )


async def test_list_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_aliases()
    mock_client.call.assert_called_once()


async def test_list_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_aliases()


async def test_list_grants(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_grants("test-key_id", )
    mock_client.call.assert_called_once()


async def test_list_grants_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_grants("test-key_id", )


async def test_list_key_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_key_policies("test-key_id", )
    mock_client.call.assert_called_once()


async def test_list_key_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_key_policies("test-key_id", )


async def test_list_key_rotations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_key_rotations("test-key_id", )
    mock_client.call.assert_called_once()


async def test_list_key_rotations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_key_rotations("test-key_id", )


async def test_list_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_keys()
    mock_client.call.assert_called_once()


async def test_list_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_keys()


async def test_list_resource_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_tags("test-key_id", )
    mock_client.call.assert_called_once()


async def test_list_resource_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_tags("test-key_id", )


async def test_list_retirable_grants(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_retirable_grants("test-retiring_principal", )
    mock_client.call.assert_called_once()


async def test_list_retirable_grants_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_retirable_grants("test-retiring_principal", )


async def test_put_key_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_key_policy("test-key_id", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_key_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_key_policy("test-key_id", "test-policy", )


async def test_replicate_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await replicate_key("test-key_id", "test-replica_region", )
    mock_client.call.assert_called_once()


async def test_replicate_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replicate_key("test-key_id", "test-replica_region", )


async def test_retire_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await retire_grant()
    mock_client.call.assert_called_once()


async def test_retire_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retire_grant()


async def test_revoke_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_grant("test-key_id", "test-grant_id", )
    mock_client.call.assert_called_once()


async def test_revoke_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_grant("test-key_id", "test-grant_id", )


async def test_rotate_key_on_demand(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await rotate_key_on_demand("test-key_id", )
    mock_client.call.assert_called_once()


async def test_rotate_key_on_demand_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rotate_key_on_demand("test-key_id", )


async def test_schedule_key_deletion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await schedule_key_deletion("test-key_id", )
    mock_client.call.assert_called_once()


async def test_schedule_key_deletion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await schedule_key_deletion("test-key_id", )


async def test_sign(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await sign("test-key_id", "test-message", "test-signing_algorithm", )
    mock_client.call.assert_called_once()


async def test_sign_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await sign("test-key_id", "test-message", "test-signing_algorithm", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-key_id", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-key_id", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-key_id", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-key_id", [], )


async def test_update_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_alias("test-alias_name", "test-target_key_id", )
    mock_client.call.assert_called_once()


async def test_update_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_alias("test-alias_name", "test-target_key_id", )


async def test_update_custom_key_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_custom_key_store("test-custom_key_store_id", )
    mock_client.call.assert_called_once()


async def test_update_custom_key_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_key_store("test-custom_key_store_id", )


async def test_update_key_description(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_key_description("test-key_id", "test-description", )
    mock_client.call.assert_called_once()


async def test_update_key_description_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_key_description("test-key_id", "test-description", )


async def test_update_primary_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_primary_region("test-key_id", "test-primary_region", )
    mock_client.call.assert_called_once()


async def test_update_primary_region_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_primary_region("test-key_id", "test-primary_region", )


async def test_verify(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", )
    mock_client.call.assert_called_once()


async def test_verify_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", )


async def test_verify_mac(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", )
    mock_client.call.assert_called_once()


async def test_verify_mac_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kms.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", )


@pytest.mark.asyncio
async def test_create_custom_key_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import create_custom_key_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await create_custom_key_store("test-custom_key_store_name", cloud_hsm_cluster_id="test-cloud_hsm_cluster_id", trust_anchor_certificate="test-trust_anchor_certificate", key_store_password="test-key_store_password", custom_key_store_type="test-custom_key_store_type", xks_proxy_uri_endpoint="test-xks_proxy_uri_endpoint", xks_proxy_uri_path="test-xks_proxy_uri_path", xks_proxy_vpc_endpoint_service_name="test-xks_proxy_vpc_endpoint_service_name", xks_proxy_vpc_endpoint_service_owner="test-xks_proxy_vpc_endpoint_service_owner", xks_proxy_authentication_credential="test-xks_proxy_authentication_credential", xks_proxy_connectivity="test-xks_proxy_connectivity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_grant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import create_grant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await create_grant("test-key_id", "test-grantee_principal", "test-operations", retiring_principal="test-retiring_principal", constraints="test-constraints", grant_tokens="test-grant_tokens", name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import create_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await create_key(policy="{}", description="test-description", key_usage="test-key_usage", customer_master_key_spec="test-customer_master_key_spec", key_spec="test-key_spec", origin="test-origin", custom_key_store_id="test-custom_key_store_id", bypass_policy_lockout_safety_check=True, tags=[{"Key": "k", "Value": "v"}], multi_region=True, xks_key_id="test-xks_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_imported_key_material_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import delete_imported_key_material
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await delete_imported_key_material("test-key_id", key_material_id="test-key_material_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_derive_shared_secret_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import derive_shared_secret
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await derive_shared_secret("test-key_id", "test-key_agreement_algorithm", "test-public_key", grant_tokens="test-grant_tokens", recipient="test-recipient", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_custom_key_stores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import describe_custom_key_stores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await describe_custom_key_stores(custom_key_store_id="test-custom_key_store_id", custom_key_store_name="test-custom_key_store_name", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import describe_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await describe_key("test-key_id", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_key_rotation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import enable_key_rotation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await enable_key_rotation("test-key_id", rotation_period_in_days="test-rotation_period_in_days", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_data_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import generate_data_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await generate_data_key_pair("test-key_id", "test-key_pair_spec", encryption_context={}, grant_tokens="test-grant_tokens", recipient="test-recipient", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_data_key_pair_without_plaintext_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import generate_data_key_pair_without_plaintext
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await generate_data_key_pair_without_plaintext("test-key_id", "test-key_pair_spec", encryption_context={}, grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_data_key_without_plaintext_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import generate_data_key_without_plaintext
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await generate_data_key_without_plaintext("test-key_id", encryption_context={}, key_spec="test-key_spec", number_of_bytes="test-number_of_bytes", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_mac_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import generate_mac
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await generate_mac("test-message", "test-key_id", "test-mac_algorithm", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_random_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import generate_random
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await generate_random(number_of_bytes="test-number_of_bytes", custom_key_store_id="test-custom_key_store_id", recipient="test-recipient", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_key_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import get_key_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await get_key_policy("test-key_id", policy_name="test-policy_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_public_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import get_public_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await get_public_key("test-key_id", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_key_material_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import import_key_material
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await import_key_material("test-key_id", 1, True, valid_to="test-valid_to", expiration_model="test-expiration_model", import_type=1, key_material_description="test-key_material_description", key_material_id="test-key_material_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_aliases(key_id="test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_grants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_grants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_grants("test-key_id", limit=1, marker="test-marker", grant_id="test-grant_id", grantee_principal="test-grantee_principal", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_key_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_key_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_key_policies("test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_key_rotations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_key_rotations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_key_rotations("test-key_id", include_key_material=True, limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_keys(limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_resource_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_resource_tags("test-key_id", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_retirable_grants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import list_retirable_grants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await list_retirable_grants("test-retiring_principal", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_key_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import put_key_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await put_key_policy("test-key_id", "{}", policy_name="test-policy_name", bypass_policy_lockout_safety_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replicate_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import replicate_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await replicate_key("test-key_id", "test-replica_region", policy="{}", bypass_policy_lockout_safety_check=True, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_retire_grant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import retire_grant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await retire_grant(grant_token="test-grant_token", key_id="test-key_id", grant_id="test-grant_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_schedule_key_deletion_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import schedule_key_deletion
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await schedule_key_deletion("test-key_id", pending_window_in_days="test-pending_window_in_days", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_sign_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import sign
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await sign("test-key_id", "test-message", "test-signing_algorithm", message_type="test-message_type", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_custom_key_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import update_custom_key_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await update_custom_key_store("test-custom_key_store_id", new_custom_key_store_name="test-new_custom_key_store_name", key_store_password="test-key_store_password", cloud_hsm_cluster_id="test-cloud_hsm_cluster_id", xks_proxy_uri_endpoint="test-xks_proxy_uri_endpoint", xks_proxy_uri_path="test-xks_proxy_uri_path", xks_proxy_vpc_endpoint_service_name="test-xks_proxy_vpc_endpoint_service_name", xks_proxy_vpc_endpoint_service_owner="test-xks_proxy_vpc_endpoint_service_owner", xks_proxy_authentication_credential="test-xks_proxy_authentication_credential", xks_proxy_connectivity="test-xks_proxy_connectivity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_verify_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import verify
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await verify("test-key_id", "test-message", "test-signature", "test-signing_algorithm", message_type="test-message_type", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_verify_mac_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kms import verify_mac
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kms.async_client", lambda *a, **kw: mock_client)
    await verify_mac("test-message", "test-key_id", "test-mac_algorithm", "test-mac", grant_tokens="test-grant_tokens", region_name="us-east-1")
    mock_client.call.assert_called_once()
