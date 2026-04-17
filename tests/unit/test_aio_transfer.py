"""Tests for aws_util.aio.transfer module."""
from __future__ import annotations

import time as _time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.transfer import (
    AccessResult,
    ServerResult,
    SshPublicKeyResult,
    UserResult,
    WorkflowResult,
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


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


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
        "Arn": "arn:...",
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
        "Arn": "arn:...",
        "Description": "test wf",
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Server operations
# ---------------------------------------------------------------------------


async def test_create_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ServerId": SERVER_ID, "Arn": "arn:..."}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_server(protocols=["SFTP"], region_name=REGION)
    assert result.server_id == SERVER_ID


async def test_create_server_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ServerId": SERVER_ID}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_server(
        protocols=["SFTP"],
        endpoint_type="PUBLIC",
        identity_provider_type="SERVICE_MANAGED",
        domain="S3",
        tags={"env": "test"},
        extra_kwargs={"LoggingRole": "arn:..."},
        region_name=REGION,
    )
    assert result.server_id == SERVER_ID


async def test_create_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_server(region_name=REGION)


async def test_describe_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Server": _server_dict()}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await describe_server(SERVER_ID, region_name=REGION)
    assert result.server_id == SERVER_ID
    assert result.state == "ONLINE"


async def test_describe_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_server(SERVER_ID, region_name=REGION)


async def test_list_servers_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Servers": [_server_dict()]}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_servers(region_name=REGION)
    assert len(result) == 1


async def test_list_servers_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Servers": [_server_dict()], "NextToken": "tok"},
        {"Servers": [_server_dict(ServerId="s-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_servers(region_name=REGION)
    assert len(result) == 2


async def test_list_servers_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_servers(region_name=REGION)


async def test_update_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ServerId": SERVER_ID}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await update_server(
        SERVER_ID, protocols=["SFTP"], endpoint_type="VPC",
        extra_kwargs={"LoggingRole": "arn:..."}, region_name=REGION,
    )
    assert result == SERVER_ID


async def test_update_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await update_server(SERVER_ID, region_name=REGION)


async def test_delete_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await delete_server(SERVER_ID, region_name=REGION)


async def test_delete_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_server(SERVER_ID, region_name=REGION)


async def test_start_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await start_server(SERVER_ID, region_name=REGION)


async def test_start_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await start_server(SERVER_ID, region_name=REGION)


async def test_stop_server_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await stop_server(SERVER_ID, region_name=REGION)


async def test_stop_server_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await stop_server(SERVER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


async def test_create_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID, "UserName": USER_NAME, "Arn": "arn:...",
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_user(SERVER_ID, USER_NAME, "arn:role", region_name=REGION)
    assert result.user_name == USER_NAME


async def test_create_user_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID, "UserName": USER_NAME,
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_user(
        SERVER_ID, USER_NAME, "arn:role",
        home_directory="/bucket",
        home_directory_type="PATH",
        home_directory_mappings=[{"Entry": "/", "Target": "/bucket"}],
        extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result.server_id == SERVER_ID


async def test_create_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_user(SERVER_ID, USER_NAME, "arn:role", region_name=REGION)


async def test_describe_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID,
        "User": _user_dict(),
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await describe_user(SERVER_ID, USER_NAME, region_name=REGION)
    assert result.user_name == USER_NAME


async def test_describe_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_user(SERVER_ID, USER_NAME, region_name=REGION)


async def test_list_users_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID,
        "Users": [_user_dict()],
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_users(SERVER_ID, region_name=REGION)
    assert len(result) == 1


async def test_list_users_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"ServerId": SERVER_ID, "Users": [_user_dict()], "NextToken": "tok"},
        {"ServerId": SERVER_ID, "Users": [_user_dict(UserName="user2")]},
    ]
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_users(SERVER_ID, region_name=REGION)
    assert len(result) == 2


async def test_list_users_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_users(SERVER_ID, region_name=REGION)


async def test_update_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"UserName": USER_NAME}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await update_user(
        SERVER_ID, USER_NAME, home_directory="/new",
        role="arn:new", extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result == USER_NAME


async def test_update_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await update_user(SERVER_ID, USER_NAME, region_name=REGION)


async def test_delete_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await delete_user(SERVER_ID, USER_NAME, region_name=REGION)


async def test_delete_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_user(SERVER_ID, USER_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# SSH public key operations
# ---------------------------------------------------------------------------


async def test_import_ssh_public_key_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID, "UserName": USER_NAME, "SshPublicKeyId": "key-123",
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await import_ssh_public_key(
        SERVER_ID, USER_NAME, "ssh-rsa AAA...", region_name=REGION,
    )
    assert result.ssh_public_key_id == "key-123"


async def test_import_ssh_public_key_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await import_ssh_public_key(SERVER_ID, USER_NAME, "ssh-rsa", region_name=REGION)


async def test_delete_ssh_public_key_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await delete_ssh_public_key(SERVER_ID, USER_NAME, "key-123", region_name=REGION)


async def test_delete_ssh_public_key_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_ssh_public_key(SERVER_ID, USER_NAME, "key-123", region_name=REGION)


# ---------------------------------------------------------------------------
# Access operations
# ---------------------------------------------------------------------------


async def test_create_access_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ServerId": SERVER_ID, "ExternalId": EXT_ID}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_access(SERVER_ID, EXT_ID, "arn:role", region_name=REGION)
    assert result.external_id == EXT_ID


async def test_create_access_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ServerId": SERVER_ID, "ExternalId": EXT_ID}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_access(
        SERVER_ID, EXT_ID, "arn:role",
        home_directory="/bucket",
        home_directory_type="PATH",
        extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result.server_id == SERVER_ID


async def test_create_access_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_access(SERVER_ID, EXT_ID, "arn:role", region_name=REGION)


async def test_describe_access_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID,
        "ExternalId": EXT_ID,
        "Access": _access_dict(),
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await describe_access(SERVER_ID, EXT_ID, region_name=REGION)
    assert result.external_id == EXT_ID


async def test_describe_access_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_access(SERVER_ID, EXT_ID, region_name=REGION)


async def test_list_accesses_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ServerId": SERVER_ID,
        "Accesses": [_access_dict()],
    }
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_accesses(SERVER_ID, region_name=REGION)
    assert len(result) == 1


async def test_list_accesses_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"ServerId": SERVER_ID, "Accesses": [_access_dict()], "NextToken": "tok"},
        {"ServerId": SERVER_ID, "Accesses": [_access_dict(ExternalId="S-9-9")]},
    ]
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_accesses(SERVER_ID, region_name=REGION)
    assert len(result) == 2


async def test_list_accesses_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_accesses(SERVER_ID, region_name=REGION)


async def test_update_access_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ExternalId": EXT_ID}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await update_access(
        SERVER_ID, EXT_ID,
        home_directory="/new", role="arn:new",
        extra_kwargs={"Policy": "{}"},
        region_name=REGION,
    )
    assert result == EXT_ID


async def test_update_access_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await update_access(SERVER_ID, EXT_ID, region_name=REGION)


async def test_delete_access_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await delete_access(SERVER_ID, EXT_ID, region_name=REGION)


async def test_delete_access_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_access(SERVER_ID, EXT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Workflow operations
# ---------------------------------------------------------------------------


async def test_create_workflow_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"WorkflowId": WF_ID, "Arn": "arn:..."}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await create_workflow(
        [{"Type": "COPY"}],
        description="test",
        on_exception_steps=[{"Type": "TAG"}],
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.workflow_id == WF_ID


async def test_create_workflow_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_workflow([{"Type": "COPY"}], region_name=REGION)


async def test_describe_workflow_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Workflow": _workflow_dict()}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await describe_workflow(WF_ID, region_name=REGION)
    assert result.workflow_id == WF_ID


async def test_describe_workflow_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_workflow(WF_ID, region_name=REGION)


async def test_list_workflows_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Workflows": [_workflow_dict()]}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_workflows(region_name=REGION)
    assert len(result) == 1


async def test_list_workflows_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Workflows": [_workflow_dict()], "NextToken": "tok"},
        {"Workflows": [_workflow_dict(WorkflowId="w-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await list_workflows(region_name=REGION)
    assert len(result) == 2


async def test_list_workflows_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_workflows(region_name=REGION)


async def test_delete_workflow_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await delete_workflow(WF_ID, region_name=REGION)


async def test_delete_workflow_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_workflow(WF_ID, region_name=REGION)


async def test_send_workflow_step_state_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    await send_workflow_step_state(WF_ID, "exec-1", "tok-1", "SUCCESS", region_name=REGION)


async def test_send_workflow_step_state_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await send_workflow_step_state(WF_ID, "exec-1", "tok-1", "SUCCESS", region_name=REGION)


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


async def test_wait_for_server_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Server": _server_dict(State="ONLINE")}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    result = await wait_for_server(SERVER_ID, timeout=5, region_name=REGION)
    assert result.state == "ONLINE"


async def test_wait_for_server_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Server": _server_dict(State="STARTING")}
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(_time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_server(
            SERVER_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_server_poll_then_ready(monkeypatch):
    """Cover the sleep branch: first poll STARTING, second ONLINE."""
    client = AsyncMock()
    client.call.side_effect = [
        {"Server": _server_dict(State="STARTING")},
        {"Server": _server_dict(State="ONLINE")},
    ]
    monkeypatch.setattr("aws_util.aio.transfer.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_server(
        SERVER_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert result.state == "ONLINE"


async def test_create_agreement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", )
    mock_client.call.assert_called_once()


async def test_create_agreement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", )


async def test_create_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_connector("test-access_role", )
    mock_client.call.assert_called_once()


async def test_create_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_connector("test-access_role", )


async def test_create_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_profile("test-as2_id", "test-profile_type", )
    mock_client.call.assert_called_once()


async def test_create_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_profile("test-as2_id", "test-profile_type", )


async def test_create_web_app(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_web_app({}, )
    mock_client.call.assert_called_once()


async def test_create_web_app_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_web_app({}, )


async def test_delete_agreement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_agreement("test-agreement_id", "test-server_id", )
    mock_client.call.assert_called_once()


async def test_delete_agreement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_agreement("test-agreement_id", "test-server_id", )


async def test_delete_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_delete_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_certificate("test-certificate_id", )


async def test_delete_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connector("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_delete_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connector("test-connector_id", )


async def test_delete_host_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_host_key("test-server_id", "test-host_key_id", )
    mock_client.call.assert_called_once()


async def test_delete_host_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_host_key("test-server_id", "test-host_key_id", )


async def test_delete_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_profile("test-profile_id", )
    mock_client.call.assert_called_once()


async def test_delete_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_profile("test-profile_id", )


async def test_delete_web_app(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_web_app("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_delete_web_app_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_web_app("test-web_app_id", )


async def test_delete_web_app_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_web_app_customization("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_delete_web_app_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_web_app_customization("test-web_app_id", )


async def test_describe_agreement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_agreement("test-agreement_id", "test-server_id", )
    mock_client.call.assert_called_once()


async def test_describe_agreement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_agreement("test-agreement_id", "test-server_id", )


async def test_describe_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_describe_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificate("test-certificate_id", )


async def test_describe_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_connector("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_describe_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_connector("test-connector_id", )


async def test_describe_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_execution("test-execution_id", "test-workflow_id", )
    mock_client.call.assert_called_once()


async def test_describe_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_execution("test-execution_id", "test-workflow_id", )


async def test_describe_host_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_host_key("test-server_id", "test-host_key_id", )
    mock_client.call.assert_called_once()


async def test_describe_host_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_host_key("test-server_id", "test-host_key_id", )


async def test_describe_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_profile("test-profile_id", )
    mock_client.call.assert_called_once()


async def test_describe_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_profile("test-profile_id", )


async def test_describe_security_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_policy("test-security_policy_name", )
    mock_client.call.assert_called_once()


async def test_describe_security_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_policy("test-security_policy_name", )


async def test_describe_web_app(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_web_app("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_describe_web_app_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_web_app("test-web_app_id", )


async def test_describe_web_app_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_web_app_customization("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_describe_web_app_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_web_app_customization("test-web_app_id", )


async def test_import_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_certificate("test-usage", "test-certificate", )
    mock_client.call.assert_called_once()


async def test_import_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_certificate("test-usage", "test-certificate", )


async def test_import_host_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_host_key("test-server_id", "test-host_key_body", )
    mock_client.call.assert_called_once()


async def test_import_host_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_host_key("test-server_id", "test-host_key_body", )


async def test_list_agreements(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agreements("test-server_id", )
    mock_client.call.assert_called_once()


async def test_list_agreements_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agreements("test-server_id", )


async def test_list_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_certificates()
    mock_client.call.assert_called_once()


async def test_list_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_certificates()


async def test_list_connectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_connectors()
    mock_client.call.assert_called_once()


async def test_list_connectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_connectors()


async def test_list_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_executions("test-workflow_id", )
    mock_client.call.assert_called_once()


async def test_list_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_executions("test-workflow_id", )


async def test_list_file_transfer_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_file_transfer_results("test-connector_id", "test-transfer_id", )
    mock_client.call.assert_called_once()


async def test_list_file_transfer_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_file_transfer_results("test-connector_id", "test-transfer_id", )


async def test_list_host_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_host_keys("test-server_id", )
    mock_client.call.assert_called_once()


async def test_list_host_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_host_keys("test-server_id", )


async def test_list_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_profiles()
    mock_client.call.assert_called_once()


async def test_list_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_profiles()


async def test_list_security_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_policies()
    mock_client.call.assert_called_once()


async def test_list_security_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_policies()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-arn", )


async def test_list_web_apps(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_web_apps()
    mock_client.call.assert_called_once()


async def test_list_web_apps_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_web_apps()


async def test_run_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_connection("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_run_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_connection("test-connector_id", )


async def test_run_identity_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_identity_provider("test-server_id", "test-user_name", )
    mock_client.call.assert_called_once()


async def test_run_identity_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_identity_provider("test-server_id", "test-user_name", )


async def test_start_directory_listing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", )
    mock_client.call.assert_called_once()


async def test_start_directory_listing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", )


async def test_start_file_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_file_transfer("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_start_file_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_file_transfer("test-connector_id", )


async def test_start_remote_delete(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_remote_delete("test-connector_id", "test-delete_path", )
    mock_client.call.assert_called_once()


async def test_start_remote_delete_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_remote_delete("test-connector_id", "test-delete_path", )


async def test_start_remote_move(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_remote_move("test-connector_id", "test-source_path", "test-target_path", )
    mock_client.call.assert_called_once()


async def test_start_remote_move_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_remote_move("test-connector_id", "test-source_path", "test-target_path", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-arn", [], )


async def test_update_agreement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agreement("test-agreement_id", "test-server_id", )
    mock_client.call.assert_called_once()


async def test_update_agreement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agreement("test-agreement_id", "test-server_id", )


async def test_update_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_update_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_certificate("test-certificate_id", )


async def test_update_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_connector("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_update_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_connector("test-connector_id", )


async def test_update_host_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_host_key("test-server_id", "test-host_key_id", "test-description", )
    mock_client.call.assert_called_once()


async def test_update_host_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_host_key("test-server_id", "test-host_key_id", "test-description", )


async def test_update_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_profile("test-profile_id", )
    mock_client.call.assert_called_once()


async def test_update_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_profile("test-profile_id", )


async def test_update_web_app(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_web_app("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_update_web_app_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_web_app("test-web_app_id", )


async def test_update_web_app_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_web_app_customization("test-web_app_id", )
    mock_client.call.assert_called_once()


async def test_update_web_app_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transfer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_web_app_customization("test-web_app_id", )


@pytest.mark.asyncio
async def test_create_agreement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import create_agreement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await create_agreement("test-server_id", "test-local_profile_id", "test-partner_profile_id", "test-access_role", description="test-description", base_directory="test-base_directory", status="test-status", tags=[{"Key": "k", "Value": "v"}], preserve_filename="test-preserve_filename", enforce_message_signing="test-enforce_message_signing", custom_directories="test-custom_directories", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_connector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import create_connector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await create_connector("test-access_role", url="test-url", as2_config={}, logging_role="test-logging_role", tags=[{"Key": "k", "Value": "v"}], sftp_config={}, security_policy_name="test-security_policy_name", egress_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import create_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await create_profile("test-as2_id", "test-profile_type", certificate_ids="test-certificate_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_web_app_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import create_web_app
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await create_web_app("test-identity_provider_details", access_endpoint="test-access_endpoint", web_app_units="test-web_app_units", tags=[{"Key": "k", "Value": "v"}], web_app_endpoint_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import import_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await import_certificate("test-usage", "test-certificate", certificate_chain="test-certificate_chain", private_key="test-private_key", active_date="test-active_date", inactive_date="test-inactive_date", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_host_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import import_host_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await import_host_key("test-server_id", "test-host_key_body", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agreements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_agreements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_agreements("test-server_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_certificates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_connectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_connectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_connectors(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_executions("test-workflow_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_file_transfer_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_file_transfer_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_file_transfer_results("test-connector_id", "test-transfer_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_host_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_host_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_host_keys("test-server_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_profiles(max_results=1, next_token="test-next_token", profile_type="test-profile_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_security_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_security_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_web_apps_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import list_web_apps
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await list_web_apps(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_identity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import run_identity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await run_identity_provider("test-server_id", "test-user_name", server_protocol="test-server_protocol", source_ip="test-source_ip", user_password="test-user_password", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_directory_listing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import start_directory_listing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await start_directory_listing("test-connector_id", "test-remote_directory_path", "test-output_directory_path", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_file_transfer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import start_file_transfer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await start_file_transfer("test-connector_id", send_file_paths="test-send_file_paths", retrieve_file_paths="test-retrieve_file_paths", local_directory_path="test-local_directory_path", remote_directory_path="test-remote_directory_path", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agreement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_agreement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_agreement("test-agreement_id", "test-server_id", description="test-description", status="test-status", local_profile_id="test-local_profile_id", partner_profile_id="test-partner_profile_id", base_directory="test-base_directory", access_role="test-access_role", preserve_filename="test-preserve_filename", enforce_message_signing="test-enforce_message_signing", custom_directories="test-custom_directories", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_certificate("test-certificate_id", active_date="test-active_date", inactive_date="test-inactive_date", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_connector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_connector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_connector("test-connector_id", url="test-url", as2_config={}, access_role="test-access_role", logging_role="test-logging_role", sftp_config={}, security_policy_name="test-security_policy_name", egress_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_profile("test-profile_id", certificate_ids="test-certificate_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_web_app_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_web_app
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_web_app("test-web_app_id", identity_provider_details="test-identity_provider_details", access_endpoint="test-access_endpoint", web_app_units="test-web_app_units", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_web_app_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transfer import update_web_app_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transfer.async_client", lambda *a, **kw: mock_client)
    await update_web_app_customization("test-web_app_id", title="test-title", logo_file="test-logo_file", favicon_file="test-favicon_file", region_name="us-east-1")
    mock_client.call.assert_called_once()
