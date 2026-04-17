"""Tests for aws_util.transfer module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.transfer as transfer_mod
from aws_util.transfer import (
    AccessResult,
    ServerResult,
    SshPublicKeyResult,
    UserResult,
    WorkflowResult,
    _parse_access,
    _parse_server,
    _parse_user,
    _parse_workflow,
    create_access,
    create_server,
    create_user,
    create_workflow,
    delete_access,
    delete_server,
    delete_ssh_public_key,
    delete_user,
    delete_workflow,
    describe_access,
    describe_server,
    describe_user,
    describe_workflow,
    import_ssh_public_key,
    list_accesses,
    list_servers,
    list_users,
    list_workflows,
    send_workflow_step_state,
    start_server,
    stop_server,
    update_access,
    update_server,
    update_user,
    wait_for_server,
    create_agreement,
    create_connector,
    create_profile,
    create_web_app,
    delete_agreement,
    delete_certificate,
    delete_connector,
    delete_host_key,
    delete_profile,
    delete_web_app,
    delete_web_app_customization,
    describe_agreement,
    describe_certificate,
    describe_connector,
    describe_execution,
    describe_host_key,
    describe_profile,
    describe_security_policy,
    describe_web_app,
    describe_web_app_customization,
    import_certificate,
    import_host_key,
    list_agreements,
    list_certificates,
    list_connectors,
    list_executions,
    list_file_transfer_results,
    list_host_keys,
    list_profiles,
    list_security_policies,
    list_tags_for_resource,
    list_web_apps,
    run_connection,
    run_identity_provider,
    start_directory_listing,
    start_file_transfer,
    start_remote_delete,
    start_remote_move,
    tag_resource,
    untag_resource,
    update_agreement,
    update_certificate,
    update_connector,
    update_host_key,
    update_profile,
    update_web_app,
    update_web_app_customization,
)
from aws_util.exceptions import AwsTimeoutError

REGION = "us-east-1"
SERVER_ID = "s-1234567890abcdef0"
USER_NAME = "testuser"
EXT_ID = "S-1-2-34-567"
WF_ID = "w-1234567890abcdef0"


def _client_error(code: str = "ServiceException", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _server_dict(**overrides):
    d = {
        "ServerId": SERVER_ID,
        "Arn": "arn:aws:transfer:us-east-1:123:server/s-123",
        "State": "ONLINE",
        "EndpointType": "PUBLIC",
        "IdentityProviderType": "SERVICE_MANAGED",
        "Domain": "S3",
        "Protocols": ["SFTP"],
    }
    d.update(overrides)
    return d


def _user_dict(**overrides):
    d = {
        "ServerId": SERVER_ID,
        "UserName": USER_NAME,
        "Arn": "arn:aws:transfer:us-east-1:123:user/testuser",
        "HomeDirectory": "/bucket/home",
        "HomeDirectoryType": "PATH",
        "Role": "arn:aws:iam::123:role/transfer-role",
        "SshPublicKeyCount": 1,
    }
    d.update(overrides)
    return d


def _access_dict(**overrides):
    d = {
        "ServerId": SERVER_ID,
        "ExternalId": EXT_ID,
        "HomeDirectory": "/bucket",
        "HomeDirectoryType": "PATH",
        "Role": "arn:aws:iam::123:role/access-role",
    }
    d.update(overrides)
    return d


def _workflow_dict(**overrides):
    d = {
        "WorkflowId": WF_ID,
        "Arn": "arn:aws:transfer:us-east-1:123:workflow/w-123",
        "Description": "test wf",
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_server(monkeypatch):
    result = _parse_server(_server_dict())
    assert result.server_id == SERVER_ID
    assert result.state == "ONLINE"
    assert result.protocols == ["SFTP"]


def test_parse_user():
    result = _parse_user(_user_dict())
    assert result.user_name == USER_NAME
    assert result.home_directory == "/bucket/home"


def test_parse_access():
    result = _parse_access(_access_dict())
    assert result.external_id == EXT_ID
    assert result.role == "arn:aws:iam::123:role/access-role"


def test_parse_workflow():
    result = _parse_workflow(_workflow_dict())
    assert result.workflow_id == WF_ID
    assert result.description == "test wf"


# ---------------------------------------------------------------------------
# Server operations
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_create_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_server.return_value = {"ServerId": SERVER_ID, "Arn": "arn:..."}
    result = create_server(protocols=["SFTP"], endpoint_type="PUBLIC", region_name=REGION)
    assert result.server_id == SERVER_ID


@patch("aws_util.transfer.get_client")
def test_create_server_with_all_options(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_server.return_value = {"ServerId": SERVER_ID}
    result = create_server(
        protocols=["SFTP"],
        endpoint_type="PUBLIC",
        identity_provider_type="SERVICE_MANAGED",
        domain="S3",
        tags={"env": "test"},
        extra_kwargs={"LoggingRole": "arn:..."},
        region_name=REGION,
    )
    assert result.server_id == SERVER_ID


@patch("aws_util.transfer.get_client")
def test_create_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_server(region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_describe_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_server.return_value = {"Server": _server_dict()}
    result = describe_server(SERVER_ID, region_name=REGION)
    assert result.server_id == SERVER_ID
    assert result.state == "ONLINE"


@patch("aws_util.transfer.get_client")
def test_describe_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_server(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_list_servers_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_servers.return_value = {"Servers": [_server_dict()]}
    result = list_servers(region_name=REGION)
    assert len(result) == 1
    assert result[0].server_id == SERVER_ID


@patch("aws_util.transfer.get_client")
def test_list_servers_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_servers.side_effect = [
        {"Servers": [_server_dict()], "NextToken": "tok"},
        {"Servers": [_server_dict(ServerId="s-other")]},
    ]
    result = list_servers(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.transfer.get_client")
def test_list_servers_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_servers.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_servers(region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_update_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_server.return_value = {"ServerId": SERVER_ID}
    result = update_server(
        SERVER_ID, protocols=["SFTP", "FTPS"], endpoint_type="VPC",
        extra_kwargs={"LoggingRole": "arn:..."}, region_name=REGION,
    )
    assert result == SERVER_ID


@patch("aws_util.transfer.get_client")
def test_update_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_server(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_delete_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_server(SERVER_ID, region_name=REGION)
    client.delete_server.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_delete_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_server(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_start_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    start_server(SERVER_ID, region_name=REGION)
    client.start_server.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_start_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.start_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        start_server(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_stop_server_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    stop_server(SERVER_ID, region_name=REGION)
    client.stop_server.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_stop_server_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.stop_server.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        stop_server(SERVER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_create_user_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_user.return_value = {
        "ServerId": SERVER_ID, "UserName": USER_NAME, "Arn": "arn:...",
    }
    result = create_user(SERVER_ID, USER_NAME, "arn:role", region_name=REGION)
    assert result.user_name == USER_NAME


@patch("aws_util.transfer.get_client")
def test_create_user_with_all_options(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_user.return_value = {
        "ServerId": SERVER_ID, "UserName": USER_NAME,
    }
    result = create_user(
        SERVER_ID, USER_NAME, "arn:role",
        home_directory="/bucket",
        home_directory_type="PATH",
        home_directory_mappings=[{"Entry": "/", "Target": "/bucket"}],
        extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result.server_id == SERVER_ID


@patch("aws_util.transfer.get_client")
def test_create_user_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_user.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_user(SERVER_ID, USER_NAME, "arn:role", region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_describe_user_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_user.return_value = {
        "ServerId": SERVER_ID,
        "User": _user_dict(),
    }
    result = describe_user(SERVER_ID, USER_NAME, region_name=REGION)
    assert result.user_name == USER_NAME


@patch("aws_util.transfer.get_client")
def test_describe_user_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_user.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_user(SERVER_ID, USER_NAME, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_list_users_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_users.return_value = {
        "ServerId": SERVER_ID,
        "Users": [_user_dict()],
    }
    result = list_users(SERVER_ID, region_name=REGION)
    assert len(result) == 1


@patch("aws_util.transfer.get_client")
def test_list_users_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_users.side_effect = [
        {"ServerId": SERVER_ID, "Users": [_user_dict()], "NextToken": "tok"},
        {"ServerId": SERVER_ID, "Users": [_user_dict(UserName="user2")]},
    ]
    result = list_users(SERVER_ID, region_name=REGION)
    assert len(result) == 2


@patch("aws_util.transfer.get_client")
def test_list_users_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_users.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_users(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_update_user_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_user.return_value = {"UserName": USER_NAME}
    result = update_user(
        SERVER_ID, USER_NAME, home_directory="/new",
        role="arn:new-role", extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result == USER_NAME


@patch("aws_util.transfer.get_client")
def test_update_user_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_user.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_user(SERVER_ID, USER_NAME, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_delete_user_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_user(SERVER_ID, USER_NAME, region_name=REGION)
    client.delete_user.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_delete_user_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_user.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_user(SERVER_ID, USER_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# SSH public key operations
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_import_ssh_public_key_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.import_ssh_public_key.return_value = {
        "ServerId": SERVER_ID,
        "UserName": USER_NAME,
        "SshPublicKeyId": "key-123",
    }
    result = import_ssh_public_key(
        SERVER_ID, USER_NAME, "ssh-rsa AAA...", region_name=REGION,
    )
    assert result.ssh_public_key_id == "key-123"


@patch("aws_util.transfer.get_client")
def test_import_ssh_public_key_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.import_ssh_public_key.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        import_ssh_public_key(SERVER_ID, USER_NAME, "ssh-rsa", region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_delete_ssh_public_key_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_ssh_public_key(SERVER_ID, USER_NAME, "key-123", region_name=REGION)
    client.delete_ssh_public_key.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_delete_ssh_public_key_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_ssh_public_key.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_ssh_public_key(SERVER_ID, USER_NAME, "key-123", region_name=REGION)


# ---------------------------------------------------------------------------
# Access operations
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_create_access_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_access.return_value = {
        "ServerId": SERVER_ID, "ExternalId": EXT_ID,
    }
    result = create_access(SERVER_ID, EXT_ID, "arn:role", region_name=REGION)
    assert result.external_id == EXT_ID


@patch("aws_util.transfer.get_client")
def test_create_access_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_access.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_access(SERVER_ID, EXT_ID, "arn:role", region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_describe_access_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_access.return_value = {
        "ServerId": SERVER_ID,
        "ExternalId": EXT_ID,
        "Access": _access_dict(),
    }
    result = describe_access(SERVER_ID, EXT_ID, region_name=REGION)
    assert result.external_id == EXT_ID


@patch("aws_util.transfer.get_client")
def test_describe_access_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_access.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_access(SERVER_ID, EXT_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_list_accesses_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_accesses.return_value = {
        "ServerId": SERVER_ID,
        "Accesses": [_access_dict()],
    }
    result = list_accesses(SERVER_ID, region_name=REGION)
    assert len(result) == 1


@patch("aws_util.transfer.get_client")
def test_list_accesses_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_accesses.side_effect = [
        {"ServerId": SERVER_ID, "Accesses": [_access_dict()], "NextToken": "tok"},
        {"ServerId": SERVER_ID, "Accesses": [_access_dict(ExternalId="S-9-9")]},
    ]
    result = list_accesses(SERVER_ID, region_name=REGION)
    assert len(result) == 2


@patch("aws_util.transfer.get_client")
def test_list_accesses_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_accesses.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_accesses(SERVER_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_update_access_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_access.return_value = {"ExternalId": EXT_ID}
    result = update_access(
        SERVER_ID, EXT_ID,
        home_directory="/new", role="arn:new",
        extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result == EXT_ID


@patch("aws_util.transfer.get_client")
def test_update_access_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_access.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_access(SERVER_ID, EXT_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_delete_access_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_access(SERVER_ID, EXT_ID, region_name=REGION)
    client.delete_access.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_delete_access_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_access.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_access(SERVER_ID, EXT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Workflow operations
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_create_workflow_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_workflow.return_value = {"WorkflowId": WF_ID, "Arn": "arn:..."}
    result = create_workflow(
        [{"Type": "COPY"}],
        description="test",
        on_exception_steps=[{"Type": "TAG"}],
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.workflow_id == WF_ID


@patch("aws_util.transfer.get_client")
def test_create_workflow_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_workflow.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_workflow([{"Type": "COPY"}], region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_describe_workflow_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_workflow.return_value = {"Workflow": _workflow_dict()}
    result = describe_workflow(WF_ID, region_name=REGION)
    assert result.workflow_id == WF_ID


@patch("aws_util.transfer.get_client")
def test_describe_workflow_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_workflow.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_workflow(WF_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_list_workflows_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_workflows.return_value = {"Workflows": [_workflow_dict()]}
    result = list_workflows(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.transfer.get_client")
def test_list_workflows_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_workflows.side_effect = [
        {"Workflows": [_workflow_dict()], "NextToken": "tok"},
        {"Workflows": [_workflow_dict(WorkflowId="w-other")]},
    ]
    result = list_workflows(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.transfer.get_client")
def test_list_workflows_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_workflows.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_workflows(region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_delete_workflow_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_workflow(WF_ID, region_name=REGION)
    client.delete_workflow.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_delete_workflow_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_workflow.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_workflow(WF_ID, region_name=REGION)


@patch("aws_util.transfer.get_client")
def test_send_workflow_step_state_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    send_workflow_step_state(WF_ID, "exec-1", "tok-1", "SUCCESS", region_name=REGION)
    client.send_workflow_step_state.assert_called_once()


@patch("aws_util.transfer.get_client")
def test_send_workflow_step_state_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.send_workflow_step_state.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        send_workflow_step_state(WF_ID, "exec-1", "tok-1", "SUCCESS", region_name=REGION)


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


@patch("aws_util.transfer.get_client")
def test_wait_for_server_immediate(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_server.return_value = {"Server": _server_dict(State="ONLINE")}
    result = wait_for_server(SERVER_ID, timeout=5, region_name=REGION)
    assert result.state == "ONLINE"


@patch("aws_util.transfer.get_client")
def test_wait_for_server_timeout(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_server.return_value = {
        "Server": _server_dict(State="STARTING"),
    }
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    with patch.object(time, "monotonic", _mono), \
         patch.object(time, "sleep"):
        with pytest.raises(AwsTimeoutError):
            wait_for_server(
                SERVER_ID, timeout=1, poll_interval=0.1, region_name=REGION,
            )


@patch("aws_util.transfer.get_client")
def test_wait_for_server_poll_then_ready(mock_gc):
    """Cover the sleep branch: first poll STARTING, second ONLINE."""
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_server.side_effect = [
        {"Server": _server_dict(State="STARTING")},
        {"Server": _server_dict(State="ONLINE")},
    ]
    with patch.object(time, "sleep"):
        result = wait_for_server(
            SERVER_ID, timeout=600, poll_interval=1.0, region_name=REGION,
        )
    assert result.state == "ONLINE"


def test_create_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agreement.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", region_name=REGION)
    mock_client.create_agreement.assert_called_once()


def test_create_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_agreement",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create agreement"):
        create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", region_name=REGION)


def test_create_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connector.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    create_connector("test-access_role", region_name=REGION)
    mock_client.create_connector.assert_called_once()


def test_create_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_connector",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create connector"):
        create_connector("test-access_role", region_name=REGION)


def test_create_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_profile.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    create_profile("test-as2_id", "test-profile_type", region_name=REGION)
    mock_client.create_profile.assert_called_once()


def test_create_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_profile",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create profile"):
        create_profile("test-as2_id", "test-profile_type", region_name=REGION)


def test_create_web_app(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_web_app.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    create_web_app({}, region_name=REGION)
    mock_client.create_web_app.assert_called_once()


def test_create_web_app_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_web_app.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_web_app",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create web app"):
        create_web_app({}, region_name=REGION)


def test_delete_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agreement.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_agreement("test-agreement_id", "test-server_id", region_name=REGION)
    mock_client.delete_agreement.assert_called_once()


def test_delete_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_agreement",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete agreement"):
        delete_agreement("test-agreement_id", "test-server_id", region_name=REGION)


def test_delete_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_certificate.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_certificate("test-certificate_id", region_name=REGION)
    mock_client.delete_certificate.assert_called_once()


def test_delete_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_certificate",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete certificate"):
        delete_certificate("test-certificate_id", region_name=REGION)


def test_delete_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connector.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_connector("test-connector_id", region_name=REGION)
    mock_client.delete_connector.assert_called_once()


def test_delete_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connector",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connector"):
        delete_connector("test-connector_id", region_name=REGION)


def test_delete_host_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_host_key.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_host_key("test-server_id", "test-host_key_id", region_name=REGION)
    mock_client.delete_host_key.assert_called_once()


def test_delete_host_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_host_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_host_key",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete host key"):
        delete_host_key("test-server_id", "test-host_key_id", region_name=REGION)


def test_delete_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_profile.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_profile("test-profile_id", region_name=REGION)
    mock_client.delete_profile.assert_called_once()


def test_delete_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_profile",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete profile"):
        delete_profile("test-profile_id", region_name=REGION)


def test_delete_web_app(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_app.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_web_app("test-web_app_id", region_name=REGION)
    mock_client.delete_web_app.assert_called_once()


def test_delete_web_app_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_app.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_web_app",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete web app"):
        delete_web_app("test-web_app_id", region_name=REGION)


def test_delete_web_app_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_app_customization.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    delete_web_app_customization("test-web_app_id", region_name=REGION)
    mock_client.delete_web_app_customization.assert_called_once()


def test_delete_web_app_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_app_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_web_app_customization",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete web app customization"):
        delete_web_app_customization("test-web_app_id", region_name=REGION)


def test_describe_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_agreement.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_agreement("test-agreement_id", "test-server_id", region_name=REGION)
    mock_client.describe_agreement.assert_called_once()


def test_describe_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_agreement",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe agreement"):
        describe_agreement("test-agreement_id", "test-server_id", region_name=REGION)


def test_describe_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificate.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_certificate("test-certificate_id", region_name=REGION)
    mock_client.describe_certificate.assert_called_once()


def test_describe_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificate",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe certificate"):
        describe_certificate("test-certificate_id", region_name=REGION)


def test_describe_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connector.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_connector("test-connector_id", region_name=REGION)
    mock_client.describe_connector.assert_called_once()


def test_describe_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_connector",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe connector"):
        describe_connector("test-connector_id", region_name=REGION)


def test_describe_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_execution.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_execution("test-execution_id", "test-workflow_id", region_name=REGION)
    mock_client.describe_execution.assert_called_once()


def test_describe_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_execution",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe execution"):
        describe_execution("test-execution_id", "test-workflow_id", region_name=REGION)


def test_describe_host_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_key.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_host_key("test-server_id", "test-host_key_id", region_name=REGION)
    mock_client.describe_host_key.assert_called_once()


def test_describe_host_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_host_key",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe host key"):
        describe_host_key("test-server_id", "test-host_key_id", region_name=REGION)


def test_describe_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_profile.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_profile("test-profile_id", region_name=REGION)
    mock_client.describe_profile.assert_called_once()


def test_describe_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_profile",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe profile"):
        describe_profile("test-profile_id", region_name=REGION)


def test_describe_security_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_policy.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_security_policy("test-security_policy_name", region_name=REGION)
    mock_client.describe_security_policy.assert_called_once()


def test_describe_security_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_policy",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security policy"):
        describe_security_policy("test-security_policy_name", region_name=REGION)


def test_describe_web_app(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_web_app.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_web_app("test-web_app_id", region_name=REGION)
    mock_client.describe_web_app.assert_called_once()


def test_describe_web_app_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_web_app.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_web_app",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe web app"):
        describe_web_app("test-web_app_id", region_name=REGION)


def test_describe_web_app_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_web_app_customization.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    describe_web_app_customization("test-web_app_id", region_name=REGION)
    mock_client.describe_web_app_customization.assert_called_once()


def test_describe_web_app_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_web_app_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_web_app_customization",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe web app customization"):
        describe_web_app_customization("test-web_app_id", region_name=REGION)


def test_import_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_certificate.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    import_certificate("test-usage", "test-certificate", region_name=REGION)
    mock_client.import_certificate.assert_called_once()


def test_import_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_certificate",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import certificate"):
        import_certificate("test-usage", "test-certificate", region_name=REGION)


def test_import_host_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_host_key.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    import_host_key("test-server_id", "test-host_key_body", region_name=REGION)
    mock_client.import_host_key.assert_called_once()


def test_import_host_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_host_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_host_key",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import host key"):
        import_host_key("test-server_id", "test-host_key_body", region_name=REGION)


def test_list_agreements(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agreements.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_agreements("test-server_id", region_name=REGION)
    mock_client.list_agreements.assert_called_once()


def test_list_agreements_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agreements.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agreements",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agreements"):
        list_agreements("test-server_id", region_name=REGION)


def test_list_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_certificates.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_certificates(region_name=REGION)
    mock_client.list_certificates.assert_called_once()


def test_list_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_certificates",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list certificates"):
        list_certificates(region_name=REGION)


def test_list_connectors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connectors.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_connectors(region_name=REGION)
    mock_client.list_connectors.assert_called_once()


def test_list_connectors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connectors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_connectors",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list connectors"):
        list_connectors(region_name=REGION)


def test_list_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_executions.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_executions("test-workflow_id", region_name=REGION)
    mock_client.list_executions.assert_called_once()


def test_list_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_executions",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list executions"):
        list_executions("test-workflow_id", region_name=REGION)


def test_list_file_transfer_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_file_transfer_results.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_file_transfer_results("test-connector_id", "test-transfer_id", region_name=REGION)
    mock_client.list_file_transfer_results.assert_called_once()


def test_list_file_transfer_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_file_transfer_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_file_transfer_results",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list file transfer results"):
        list_file_transfer_results("test-connector_id", "test-transfer_id", region_name=REGION)


def test_list_host_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_host_keys.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_host_keys("test-server_id", region_name=REGION)
    mock_client.list_host_keys.assert_called_once()


def test_list_host_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_host_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_host_keys",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list host keys"):
        list_host_keys("test-server_id", region_name=REGION)


def test_list_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_profiles.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_profiles(region_name=REGION)
    mock_client.list_profiles.assert_called_once()


def test_list_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_profiles",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list profiles"):
        list_profiles(region_name=REGION)


def test_list_security_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_policies.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_security_policies(region_name=REGION)
    mock_client.list_security_policies.assert_called_once()


def test_list_security_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_policies",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security policies"):
        list_security_policies(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-arn", region_name=REGION)


def test_list_web_apps(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_web_apps.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    list_web_apps(region_name=REGION)
    mock_client.list_web_apps.assert_called_once()


def test_list_web_apps_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_web_apps.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_web_apps",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list web apps"):
        list_web_apps(region_name=REGION)


def test_run_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_connection.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    run_connection("test-connector_id", region_name=REGION)
    mock_client.test_connection.assert_called_once()


def test_run_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_connection",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run connection"):
        run_connection("test-connector_id", region_name=REGION)


def test_run_identity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_identity_provider.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    run_identity_provider("test-server_id", "test-user_name", region_name=REGION)
    mock_client.test_identity_provider.assert_called_once()


def test_run_identity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_identity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_identity_provider",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run identity provider"):
        run_identity_provider("test-server_id", "test-user_name", region_name=REGION)


def test_start_directory_listing(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_directory_listing.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", region_name=REGION)
    mock_client.start_directory_listing.assert_called_once()


def test_start_directory_listing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_directory_listing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_directory_listing",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start directory listing"):
        start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", region_name=REGION)


def test_start_file_transfer(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_file_transfer.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    start_file_transfer("test-connector_id", region_name=REGION)
    mock_client.start_file_transfer.assert_called_once()


def test_start_file_transfer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_file_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_file_transfer",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start file transfer"):
        start_file_transfer("test-connector_id", region_name=REGION)


def test_start_remote_delete(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_remote_delete.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    start_remote_delete("test-connector_id", "test-delete_path", region_name=REGION)
    mock_client.start_remote_delete.assert_called_once()


def test_start_remote_delete_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_remote_delete.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_remote_delete",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start remote delete"):
        start_remote_delete("test-connector_id", "test-delete_path", region_name=REGION)


def test_start_remote_move(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_remote_move.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    start_remote_move("test-connector_id", "test-source_path", "test-target_path", region_name=REGION)
    mock_client.start_remote_move.assert_called_once()


def test_start_remote_move_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_remote_move.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_remote_move",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start remote move"):
        start_remote_move("test-connector_id", "test-source_path", "test-target_path", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-arn", [], region_name=REGION)


def test_update_agreement(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agreement.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_agreement("test-agreement_id", "test-server_id", region_name=REGION)
    mock_client.update_agreement.assert_called_once()


def test_update_agreement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agreement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agreement",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agreement"):
        update_agreement("test-agreement_id", "test-server_id", region_name=REGION)


def test_update_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_certificate.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_certificate("test-certificate_id", region_name=REGION)
    mock_client.update_certificate.assert_called_once()


def test_update_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_certificate",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update certificate"):
        update_certificate("test-certificate_id", region_name=REGION)


def test_update_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connector.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_connector("test-connector_id", region_name=REGION)
    mock_client.update_connector.assert_called_once()


def test_update_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connector",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connector"):
        update_connector("test-connector_id", region_name=REGION)


def test_update_host_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_host_key.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_host_key("test-server_id", "test-host_key_id", "test-description", region_name=REGION)
    mock_client.update_host_key.assert_called_once()


def test_update_host_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_host_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_host_key",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update host key"):
        update_host_key("test-server_id", "test-host_key_id", "test-description", region_name=REGION)


def test_update_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_profile.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_profile("test-profile_id", region_name=REGION)
    mock_client.update_profile.assert_called_once()


def test_update_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_profile",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update profile"):
        update_profile("test-profile_id", region_name=REGION)


def test_update_web_app(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_web_app.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_web_app("test-web_app_id", region_name=REGION)
    mock_client.update_web_app.assert_called_once()


def test_update_web_app_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_web_app.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_web_app",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update web app"):
        update_web_app("test-web_app_id", region_name=REGION)


def test_update_web_app_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_web_app_customization.return_value = {}
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    update_web_app_customization("test-web_app_id", region_name=REGION)
    mock_client.update_web_app_customization.assert_called_once()


def test_update_web_app_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_web_app_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_web_app_customization",
    )
    monkeypatch.setattr(transfer_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update web app customization"):
        update_web_app_customization("test-web_app_id", region_name=REGION)


def test_create_agreement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_agreement
    mock_client = MagicMock()
    mock_client.create_agreement.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", description="test-description", base_directory="test-base_directory", status="test-status", tags=[{"Key": "k", "Value": "v"}], preserve_filename="test-preserve_filename", enforce_message_signing="test-enforce_message_signing", custom_directories="test-custom_directories", region_name="us-east-1")
    mock_client.create_agreement.assert_called_once()

def test_create_connector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_connector
    mock_client = MagicMock()
    mock_client.create_connector.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    create_connector("test-access_role", url="test-url", as2_config={}, logging_role="test-logging_role", tags=[{"Key": "k", "Value": "v"}], sftp_config={}, security_policy_name="test-security_policy_name", egress_config={}, region_name="us-east-1")
    mock_client.create_connector.assert_called_once()

def test_create_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_profile
    mock_client = MagicMock()
    mock_client.create_profile.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    create_profile("test-as2_id", "test-profile_type", certificate_ids="test-certificate_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_profile.assert_called_once()

def test_create_web_app_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_web_app
    mock_client = MagicMock()
    mock_client.create_web_app.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    create_web_app("test-identity_provider_details", access_endpoint="test-access_endpoint", web_app_units="test-web_app_units", tags=[{"Key": "k", "Value": "v"}], web_app_endpoint_policy="{}", region_name="us-east-1")
    mock_client.create_web_app.assert_called_once()

def test_import_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import import_certificate
    mock_client = MagicMock()
    mock_client.import_certificate.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    import_certificate("test-usage", "test-certificate", certificate_chain="test-certificate_chain", private_key="test-private_key", active_date="test-active_date", inactive_date="test-inactive_date", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_certificate.assert_called_once()

def test_import_host_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import import_host_key
    mock_client = MagicMock()
    mock_client.import_host_key.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    import_host_key("test-server_id", "test-host_key_body", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_host_key.assert_called_once()

def test_list_agreements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_agreements
    mock_client = MagicMock()
    mock_client.list_agreements.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_agreements("test-server_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agreements.assert_called_once()

def test_list_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_certificates
    mock_client = MagicMock()
    mock_client.list_certificates.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_certificates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_certificates.assert_called_once()

def test_list_connectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_connectors
    mock_client = MagicMock()
    mock_client.list_connectors.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_connectors(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_connectors.assert_called_once()

def test_list_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_executions
    mock_client = MagicMock()
    mock_client.list_executions.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_executions("test-workflow_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_executions.assert_called_once()

def test_list_file_transfer_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_file_transfer_results
    mock_client = MagicMock()
    mock_client.list_file_transfer_results.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_file_transfer_results("test-connector_id", "test-transfer_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_file_transfer_results.assert_called_once()

def test_list_host_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_host_keys
    mock_client = MagicMock()
    mock_client.list_host_keys.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_host_keys("test-server_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_host_keys.assert_called_once()

def test_list_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_profiles
    mock_client = MagicMock()
    mock_client.list_profiles.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_profiles(max_results=1, next_token="test-next_token", profile_type="test-profile_type", region_name="us-east-1")
    mock_client.list_profiles.assert_called_once()

def test_list_security_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_security_policies
    mock_client = MagicMock()
    mock_client.list_security_policies.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_security_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_security_policies.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_web_apps_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import list_web_apps
    mock_client = MagicMock()
    mock_client.list_web_apps.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    list_web_apps(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_web_apps.assert_called_once()

def test_run_identity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import run_identity_provider
    mock_client = MagicMock()
    mock_client.test_identity_provider.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    run_identity_provider("test-server_id", "test-user_name", server_protocol="test-server_protocol", source_ip="test-source_ip", user_password="test-user_password", region_name="us-east-1")
    mock_client.test_identity_provider.assert_called_once()

def test_start_directory_listing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import start_directory_listing
    mock_client = MagicMock()
    mock_client.start_directory_listing.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", max_items=1, region_name="us-east-1")
    mock_client.start_directory_listing.assert_called_once()

def test_start_file_transfer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import start_file_transfer
    mock_client = MagicMock()
    mock_client.start_file_transfer.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    start_file_transfer("test-connector_id", send_file_paths="test-send_file_paths", retrieve_file_paths="test-retrieve_file_paths", local_directory_path="test-local_directory_path", remote_directory_path="test-remote_directory_path", region_name="us-east-1")
    mock_client.start_file_transfer.assert_called_once()

def test_update_agreement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_agreement
    mock_client = MagicMock()
    mock_client.update_agreement.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_agreement("test-agreement_id", "test-server_id", description="test-description", status="test-status", local_profile_id="test-local_profile_id", partner_profile_id="test-partner_profile_id", base_directory="test-base_directory", access_role="test-access_role", preserve_filename="test-preserve_filename", enforce_message_signing="test-enforce_message_signing", custom_directories="test-custom_directories", region_name="us-east-1")
    mock_client.update_agreement.assert_called_once()

def test_update_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_certificate
    mock_client = MagicMock()
    mock_client.update_certificate.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_certificate("test-certificate_id", active_date="test-active_date", inactive_date="test-inactive_date", description="test-description", region_name="us-east-1")
    mock_client.update_certificate.assert_called_once()

def test_update_connector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_connector
    mock_client = MagicMock()
    mock_client.update_connector.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_connector("test-connector_id", url="test-url", as2_config={}, access_role="test-access_role", logging_role="test-logging_role", sftp_config={}, security_policy_name="test-security_policy_name", egress_config={}, region_name="us-east-1")
    mock_client.update_connector.assert_called_once()

def test_update_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_profile
    mock_client = MagicMock()
    mock_client.update_profile.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_profile("test-profile_id", certificate_ids="test-certificate_ids", region_name="us-east-1")
    mock_client.update_profile.assert_called_once()

def test_update_web_app_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_web_app
    mock_client = MagicMock()
    mock_client.update_web_app.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_web_app("test-web_app_id", identity_provider_details="test-identity_provider_details", access_endpoint="test-access_endpoint", web_app_units="test-web_app_units", region_name="us-east-1")
    mock_client.update_web_app.assert_called_once()

def test_update_web_app_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import update_web_app_customization
    mock_client = MagicMock()
    mock_client.update_web_app_customization.return_value = {}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    update_web_app_customization("test-web_app_id", title="test-title", logo_file="test-logo_file", favicon_file="test-favicon_file", region_name="us-east-1")
    mock_client.update_web_app_customization.assert_called_once()


def test_create_access_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_access
    mock_client = MagicMock()
    mock_client.create_access.return_value = {"ServerId": "s-1", "ExternalId": "e-1"}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: mock_client)
    create_access("s-1", "e-1", "role-arn", extra_kwargs={"HomeDirectory": "/"}, region_name="us-east-1")
    mock_client.create_access.assert_called_once()


def test_create_access_all_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transfer import create_access
    m = MagicMock(); m.create_access.return_value = {"ServerId": "s", "ExternalId": "e"}
    monkeypatch.setattr("aws_util.transfer.get_client", lambda *a, **kw: m)
    create_access("s", "e", "role", home_directory="/", home_directory_type="PATH", extra_kwargs={}, region_name="us-east-1")
