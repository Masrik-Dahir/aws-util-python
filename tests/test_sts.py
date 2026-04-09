"""Tests for aws_util.sts module."""
from __future__ import annotations

import boto3
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.sts import (
    AssumedRoleCredentials,
    CallerIdentity,
    assume_role,
    assume_role_session,
    get_account_id,
    get_caller_identity,
    is_valid_account_id,
    assume_role_with_saml,
    assume_role_with_web_identity,
    assume_root,
    decode_authorization_message,
    get_access_key_info,
    get_delegated_access_token,
    get_federation_token,
    get_session_token,
)

REGION = "us-east-1"
ROLE_ARN = "arn:aws:iam::123456789012:role/TestRole"


@pytest.fixture
def iam_role():
    import json
    iam = boto3.client("iam", region_name=REGION)
    role = iam.create_role(
        RoleName="TestRole",
        AssumeRolePolicyDocument=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}],
        }),
    )
    return role["Role"]["Arn"]


# ---------------------------------------------------------------------------
# get_caller_identity
# ---------------------------------------------------------------------------


def test_get_caller_identity_returns_identity():
    identity = get_caller_identity(region_name=REGION)
    assert isinstance(identity, CallerIdentity)
    assert identity.account_id
    assert identity.arn
    assert identity.user_id


def test_get_caller_identity_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.sts as stsmod

    mock_client = MagicMock()
    mock_client.get_caller_identity.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "GetCallerIdentity",
    )
    monkeypatch.setattr(stsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_caller_identity failed"):
        get_caller_identity(region_name=REGION)


# ---------------------------------------------------------------------------
# get_account_id
# ---------------------------------------------------------------------------


def test_get_account_id_returns_12_digit_string():
    account_id = get_account_id(region_name=REGION)
    assert account_id.isdigit()
    assert len(account_id) == 12


# ---------------------------------------------------------------------------
# assume_role
# ---------------------------------------------------------------------------


def test_assume_role_returns_credentials(iam_role):
    creds = assume_role(iam_role, "test-session", region_name=REGION)
    assert isinstance(creds, AssumedRoleCredentials)
    assert creds.access_key_id
    assert creds.secret_access_key
    assert creds.session_token


def test_assume_role_with_duration(iam_role):
    creds = assume_role(
        iam_role,
        "test-session",
        duration_seconds=900,
        region_name=REGION,
    )
    assert creds.access_key_id


def test_assume_role_with_external_id(iam_role):
    creds = assume_role(
        iam_role,
        "ext-session",
        external_id="ext-123",
        region_name=REGION,
    )
    assert creds.access_key_id


def test_assume_role_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.sts as stsmod

    mock_client = MagicMock()
    mock_client.assume_role.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "role not found"}},
        "AssumeRole",
    )
    monkeypatch.setattr(stsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assume role"):
        assume_role("arn:aws:iam::123:role/nonexistent", "session", region_name=REGION)


# ---------------------------------------------------------------------------
# assume_role_session
# ---------------------------------------------------------------------------


def test_assume_role_session_returns_boto3_session(iam_role):
    import boto3 as _boto3

    session = assume_role_session(iam_role, "session-name", region_name=REGION)
    assert isinstance(session, _boto3.Session)


def test_assume_role_session_with_region(iam_role):
    import boto3 as _boto3

    session = assume_role_session(
        iam_role,
        "session-name",
        region_name=REGION,
    )
    assert isinstance(session, _boto3.Session)


def test_assume_role_session_no_region(iam_role):
    """When region_name is None, boto3.Session should still be created."""
    import boto3 as _boto3

    session = assume_role_session(
        iam_role,
        "session-name",
        region_name=None,
    )
    assert isinstance(session, _boto3.Session)


# ---------------------------------------------------------------------------
# is_valid_account_id
# ---------------------------------------------------------------------------


def test_is_valid_account_id_valid():
    assert is_valid_account_id("123456789012") is True


def test_is_valid_account_id_too_short():
    assert is_valid_account_id("12345678901") is False


def test_is_valid_account_id_too_long():
    assert is_valid_account_id("1234567890123") is False


def test_is_valid_account_id_non_digit():
    assert is_valid_account_id("12345678901a") is False


def test_is_valid_account_id_empty():
    assert is_valid_account_id("") is False


def test_assume_role_with_saml(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_role_with_saml.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_role_with_saml("test-role_arn", "test-principal_arn", "test-saml_assertion", region_name=REGION)
    mock_client.assume_role_with_saml.assert_called_once()


def test_assume_role_with_saml_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_role_with_saml.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assume_role_with_saml",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assume role with saml"):
        assume_role_with_saml("test-role_arn", "test-principal_arn", "test-saml_assertion", region_name=REGION)


def test_assume_role_with_web_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_role_with_web_identity.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_role_with_web_identity("test-role_arn", "test-role_session_name", "test-web_identity_token", region_name=REGION)
    mock_client.assume_role_with_web_identity.assert_called_once()


def test_assume_role_with_web_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_role_with_web_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assume_role_with_web_identity",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assume role with web identity"):
        assume_role_with_web_identity("test-role_arn", "test-role_session_name", "test-web_identity_token", region_name=REGION)


def test_assume_root(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_root.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_root("test-target_principal", {}, region_name=REGION)
    mock_client.assume_root.assert_called_once()


def test_assume_root_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assume_root.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assume_root",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assume root"):
        assume_root("test-target_principal", {}, region_name=REGION)


def test_decode_authorization_message(monkeypatch):
    mock_client = MagicMock()
    mock_client.decode_authorization_message.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    decode_authorization_message("test-encoded_message", region_name=REGION)
    mock_client.decode_authorization_message.assert_called_once()


def test_decode_authorization_message_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decode_authorization_message.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decode_authorization_message",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decode authorization message"):
        decode_authorization_message("test-encoded_message", region_name=REGION)


def test_get_access_key_info(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_key_info.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_access_key_info("test-access_key_id", region_name=REGION)
    mock_client.get_access_key_info.assert_called_once()


def test_get_access_key_info_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_key_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_access_key_info",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get access key info"):
        get_access_key_info("test-access_key_id", region_name=REGION)


def test_get_delegated_access_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_delegated_access_token.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_delegated_access_token("test-trade_in_token", region_name=REGION)
    mock_client.get_delegated_access_token.assert_called_once()


def test_get_delegated_access_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_delegated_access_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_delegated_access_token",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get delegated access token"):
        get_delegated_access_token("test-trade_in_token", region_name=REGION)


def test_get_federation_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_federation_token.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_federation_token("test-name", region_name=REGION)
    mock_client.get_federation_token.assert_called_once()


def test_get_federation_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_federation_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_federation_token",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get federation token"):
        get_federation_token("test-name", region_name=REGION)


def test_get_session_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_token.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_session_token(region_name=REGION)
    mock_client.get_session_token.assert_called_once()


def test_get_session_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session_token",
    )
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session token"):
        get_session_token(region_name=REGION)


def test_assume_role_with_saml_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sts import assume_role_with_saml
    mock_client = MagicMock()
    mock_client.assume_role_with_saml.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_role_with_saml("test-role_arn", "test-principal_arn", "test-saml_assertion", policy_arns="test-policy_arns", policy="{}", duration_seconds=1, region_name="us-east-1")
    mock_client.assume_role_with_saml.assert_called_once()

def test_assume_role_with_web_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sts import assume_role_with_web_identity
    mock_client = MagicMock()
    mock_client.assume_role_with_web_identity.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_role_with_web_identity("test-role_arn", "test-role_session_name", "test-web_identity_token", provider_id="test-provider_id", policy_arns="test-policy_arns", policy="{}", duration_seconds=1, region_name="us-east-1")
    mock_client.assume_role_with_web_identity.assert_called_once()

def test_assume_root_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sts import assume_root
    mock_client = MagicMock()
    mock_client.assume_root.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    assume_root("test-target_principal", "test-task_policy_arn", duration_seconds=1, region_name="us-east-1")
    mock_client.assume_root.assert_called_once()

def test_get_federation_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sts import get_federation_token
    mock_client = MagicMock()
    mock_client.get_federation_token.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_federation_token("test-name", policy="{}", policy_arns="test-policy_arns", duration_seconds=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.get_federation_token.assert_called_once()

def test_get_session_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sts import get_session_token
    mock_client = MagicMock()
    mock_client.get_session_token.return_value = {}
    monkeypatch.setattr("aws_util.sts.get_client", lambda *a, **kw: mock_client)
    get_session_token(duration_seconds=1, serial_number="test-serial_number", token_code="test-token_code", region_name="us-east-1")
    mock_client.get_session_token.assert_called_once()
