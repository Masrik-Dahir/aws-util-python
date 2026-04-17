"""Tests for aws_util.aio.bedrock_agent module."""
from __future__ import annotations

import asyncio
import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.bedrock_agent import (
    AgentResult,
    DataSourceResult,
    IngestionJobResult,
    KnowledgeBaseResult,
    associate_agent_knowledge_base,
    create_agent,
    create_data_source,
    create_knowledge_base,
    delete_agent,
    delete_knowledge_base,
    get_agent,
    get_data_source,
    get_ingestion_job,
    get_knowledge_base,
    list_agents,
    list_data_sources,
    list_knowledge_bases,
    prepare_agent,
    start_ingestion_job,
    update_agent,
    wait_for_agent,
    wait_for_ingestion_job,
    associate_agent_collaborator,
    create_agent_action_group,
    create_agent_alias,
    create_flow,
    create_flow_alias,
    create_flow_version,
    create_prompt,
    create_prompt_version,
    delete_agent_action_group,
    delete_agent_alias,
    delete_agent_version,
    delete_data_source,
    delete_flow,
    delete_flow_alias,
    delete_flow_version,
    delete_knowledge_base_documents,
    delete_prompt,
    disassociate_agent_collaborator,
    disassociate_agent_knowledge_base,
    get_agent_action_group,
    get_agent_alias,
    get_agent_collaborator,
    get_agent_knowledge_base,
    get_agent_version,
    get_flow,
    get_flow_alias,
    get_flow_version,
    get_knowledge_base_documents,
    get_prompt,
    ingest_knowledge_base_documents,
    list_agent_action_groups,
    list_agent_aliases,
    list_agent_collaborators,
    list_agent_knowledge_bases,
    list_agent_versions,
    list_flow_aliases,
    list_flow_versions,
    list_flows,
    list_ingestion_jobs,
    list_knowledge_base_documents,
    list_prompts,
    list_tags_for_resource,
    prepare_flow,
    stop_ingestion_job,
    tag_resource,
    untag_resource,
    update_agent_action_group,
    update_agent_alias,
    update_agent_collaborator,
    update_agent_knowledge_base,
    update_data_source,
    update_flow,
    update_flow_alias,
    update_knowledge_base,
    update_prompt,
    validate_flow_definition,
)
from aws_util.exceptions import AwsTimeoutError


REGION = "us-east-1"
AGENT_ID = "agent-123"
AGENT_NAME = "my-agent"
ROLE_ARN = "arn:aws:iam::123456789012:role/testrole"
KB_ID = "kb-123"
DS_ID = "ds-123"
IJ_ID = "ij-123"


def _mf(mc):
    return lambda *a, **kw: mc


def _agent_dict(**ov):
    d = {
        "agentId": AGENT_ID,
        "agentName": AGENT_NAME,
        "agentArn": "arn:agent",
        "agentStatus": "PREPARED",
        "agentVersion": "1",
        "description": "desc",
        "foundationModel": "anthropic.claude-v2",
        "instruction": "help",
        "idleSessionTTLInSeconds": 600,
        "agentResourceRoleArn": ROLE_ARN,
    }
    d.update(ov)
    return d


def _kb_dict(**ov):
    d = {
        "knowledgeBaseId": KB_ID,
        "name": "my-kb",
        "knowledgeBaseArn": "arn:kb",
        "status": "ACTIVE",
        "description": "kb desc",
        "roleArn": ROLE_ARN,
    }
    d.update(ov)
    return d


def _ds_dict(**ov):
    d = {
        "dataSourceId": DS_ID,
        "knowledgeBaseId": KB_ID,
        "name": "my-ds",
        "status": "AVAILABLE",
        "description": "ds desc",
    }
    d.update(ov)
    return d


def _ij_dict(**ov):
    d = {
        "ingestionJobId": IJ_ID,
        "knowledgeBaseId": KB_ID,
        "dataSourceId": DS_ID,
        "status": "COMPLETE",
        "description": "ij desc",
        "statistics": {"docs": 10},
        "failureReasons": [],
    }
    d.update(ov)
    return d


# ---------------------------------------------------------------------------
# Agent CRUD
# ---------------------------------------------------------------------------


async def test_create_agent_minimal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN, region_name=REGION)
    assert r.agent_id == AGENT_ID


async def test_create_agent_all_opts(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_agent(
        AGENT_NAME,
        agent_resource_role_arn=ROLE_ARN,
        foundation_model="fm",
        instruction="i",
        description="d",
        idle_session_ttl_in_seconds=100,
        region_name=REGION,
    )
    assert r.agent_name == AGENT_NAME


async def test_create_agent_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN)


async def test_create_agent_no_key(monkeypatch):
    client = AsyncMock()
    client.call.return_value = _agent_dict()
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN)
    assert r.agent_id == AGENT_ID


async def test_get_agent_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await get_agent(AGENT_ID, region_name=REGION)
    assert r.agent_id == AGENT_ID


async def test_get_agent_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await get_agent(AGENT_ID)


async def test_list_agents_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agentSummaries": []}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_agents(region_name=REGION)
    assert r == []


async def test_list_agents_pagination(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"agentSummaries": [_agent_dict()], "nextToken": "tok"},
        {"agentSummaries": [_agent_dict(agentId="a2")]},
    ]
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_agents(max_results=1)
    assert len(r) == 2


async def test_list_agents_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await list_agents()


async def test_delete_agent_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    await delete_agent(AGENT_ID, region_name=REGION)


async def test_delete_agent_skip_check(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    await delete_agent(AGENT_ID, skip_resource_in_use_check=True)


async def test_delete_agent_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await delete_agent(AGENT_ID)


async def test_update_agent_minimal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await update_agent(AGENT_ID, AGENT_NAME, agent_resource_role_arn=ROLE_ARN)
    assert r.agent_id == AGENT_ID


async def test_update_agent_all_opts(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await update_agent(
        AGENT_ID,
        AGENT_NAME,
        agent_resource_role_arn=ROLE_ARN,
        foundation_model="fm",
        instruction="i",
        description="d",
        idle_session_ttl_in_seconds=100,
        region_name=REGION,
    )
    assert r.agent_name == AGENT_NAME


async def test_update_agent_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await update_agent(AGENT_ID, AGENT_NAME, agent_resource_role_arn=ROLE_ARN)


async def test_prepare_agent_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await prepare_agent(AGENT_ID, region_name=REGION)
    assert r.agent_id == AGENT_ID


async def test_prepare_agent_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await prepare_agent(AGENT_ID)


# ---------------------------------------------------------------------------
# Knowledge Base CRUD
# ---------------------------------------------------------------------------


async def test_create_knowledge_base_minimal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_knowledge_base(
        "my-kb",
        role_arn=ROLE_ARN,
        knowledge_base_configuration={},
        storage_configuration={},
    )
    assert r.knowledge_base_id == KB_ID


async def test_create_knowledge_base_with_desc(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_knowledge_base(
        "my-kb",
        role_arn=ROLE_ARN,
        knowledge_base_configuration={},
        storage_configuration={},
        description="desc",
        region_name=REGION,
    )
    assert r.name == "my-kb"


async def test_create_knowledge_base_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await create_knowledge_base(
            "kb", role_arn="r", knowledge_base_configuration={},
            storage_configuration={},
        )


async def test_get_knowledge_base_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await get_knowledge_base(KB_ID, region_name=REGION)
    assert r.knowledge_base_id == KB_ID


async def test_get_knowledge_base_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await get_knowledge_base(KB_ID)


async def test_list_knowledge_bases_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"knowledgeBaseSummaries": []}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_knowledge_bases()
    assert r == []


async def test_list_knowledge_bases_pagination(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"knowledgeBaseSummaries": [_kb_dict()], "nextToken": "tok"},
        {"knowledgeBaseSummaries": [_kb_dict(knowledgeBaseId="kb-2")]},
    ]
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_knowledge_bases(max_results=1)
    assert len(r) == 2


async def test_list_knowledge_bases_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await list_knowledge_bases()


async def test_delete_knowledge_base_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    await delete_knowledge_base(KB_ID, region_name=REGION)


async def test_delete_knowledge_base_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await delete_knowledge_base(KB_ID)


# ---------------------------------------------------------------------------
# Associate
# ---------------------------------------------------------------------------


async def test_associate_agent_knowledge_base_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ok": True}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await associate_agent_knowledge_base(AGENT_ID, "DRAFT", KB_ID, region_name=REGION)
    assert r == {"ok": True}


async def test_associate_agent_knowledge_base_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await associate_agent_knowledge_base(AGENT_ID, "DRAFT", KB_ID)


# ---------------------------------------------------------------------------
# Data Source CRUD
# ---------------------------------------------------------------------------


async def test_create_data_source_minimal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_data_source(KB_ID, "my-ds", data_source_configuration={})
    assert r.data_source_id == DS_ID


async def test_create_data_source_with_desc(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await create_data_source(
        KB_ID, "my-ds", data_source_configuration={}, description="d",
        region_name=REGION,
    )
    assert r.name == "my-ds"


async def test_create_data_source_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await create_data_source(KB_ID, "ds", data_source_configuration={})


async def test_get_data_source_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await get_data_source(KB_ID, DS_ID, region_name=REGION)
    assert r.data_source_id == DS_ID


async def test_get_data_source_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await get_data_source(KB_ID, DS_ID)


async def test_list_data_sources_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"dataSourceSummaries": []}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_data_sources(KB_ID)
    assert r == []


async def test_list_data_sources_pagination(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"dataSourceSummaries": [_ds_dict()], "nextToken": "tok"},
        {"dataSourceSummaries": [_ds_dict(dataSourceId="ds-2")]},
    ]
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await list_data_sources(KB_ID, max_results=1)
    assert len(r) == 2


async def test_list_data_sources_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await list_data_sources(KB_ID)


# ---------------------------------------------------------------------------
# Ingestion Jobs
# ---------------------------------------------------------------------------


async def test_start_ingestion_job_minimal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await start_ingestion_job(KB_ID, DS_ID)
    assert r.ingestion_job_id == IJ_ID


async def test_start_ingestion_job_with_desc(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await start_ingestion_job(KB_ID, DS_ID, description="d", region_name=REGION)
    assert r.status == "COMPLETE"


async def test_start_ingestion_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await start_ingestion_job(KB_ID, DS_ID)


async def test_get_ingestion_job_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await get_ingestion_job(KB_ID, DS_ID, IJ_ID, region_name=REGION)
    assert r.ingestion_job_id == IJ_ID


async def test_get_ingestion_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError):
        await get_ingestion_job(KB_ID, DS_ID, IJ_ID)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def test_wait_for_agent_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict(agentStatus="PREPARED")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await wait_for_agent(AGENT_ID, region_name=REGION)
    assert r.agent_status == "PREPARED"


async def test_wait_for_agent_failure(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict(agentStatus="FAILED")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError, match="failure status"):
        await wait_for_agent(AGENT_ID)


async def test_wait_for_agent_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"agent": _agent_dict(agentStatus="CREATING")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            return 100.0
        return 999.0

    monkeypatch.setattr(time, "monotonic", _mono)
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    with pytest.raises(AwsTimeoutError):
        await wait_for_agent(AGENT_ID, timeout=10)


async def test_wait_for_agent_poll_then_success(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"agent": _agent_dict(agentStatus="CREATING")},
        {"agent": _agent_dict(agentStatus="PREPARED")},
    ]
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    monkeypatch.setattr(time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    r = await wait_for_agent(AGENT_ID, timeout=300)
    assert r.agent_status == "PREPARED"


async def test_wait_for_ingestion_job_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict(status="COMPLETE")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    r = await wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, region_name=REGION)
    assert r.status == "COMPLETE"


async def test_wait_for_ingestion_job_failure(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict(status="FAILED")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    with pytest.raises(RuntimeError, match="failure"):
        await wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID)


async def test_wait_for_ingestion_job_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ingestionJob": _ij_dict(status="IN_PROGRESS")}
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            return 100.0
        return 999.0

    monkeypatch.setattr(time, "monotonic", _mono)
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    with pytest.raises(AwsTimeoutError):
        await wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, timeout=10)


async def test_wait_for_ingestion_job_poll_then_success(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"ingestionJob": _ij_dict(status="IN_PROGRESS")},
        {"ingestionJob": _ij_dict(status="COMPLETE")},
    ]
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", _mf(client))
    monkeypatch.setattr(time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())
    r = await wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, timeout=600)
    assert r.status == "COMPLETE"


async def test_associate_agent_collaborator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_agent_collaborator("test-agent_id", "test-agent_version", {}, "test-collaborator_name", "test-collaboration_instruction", )
    mock_client.call.assert_called_once()


async def test_associate_agent_collaborator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_agent_collaborator("test-agent_id", "test-agent_version", {}, "test-collaborator_name", "test-collaboration_instruction", )


async def test_create_agent_action_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", )
    mock_client.call.assert_called_once()


async def test_create_agent_action_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", )


async def test_create_agent_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_agent_alias("test-agent_id", "test-agent_alias_name", )
    mock_client.call.assert_called_once()


async def test_create_agent_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_agent_alias("test-agent_id", "test-agent_alias_name", )


async def test_create_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_flow("test-name", "test-execution_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_flow("test-name", "test-execution_role_arn", )


async def test_create_flow_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_flow_alias("test-name", [], "test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_create_flow_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_flow_alias("test-name", [], "test-flow_identifier", )


async def test_create_flow_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_flow_version("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_create_flow_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_flow_version("test-flow_identifier", )


async def test_create_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_prompt("test-name", )
    mock_client.call.assert_called_once()


async def test_create_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_prompt("test-name", )


async def test_create_prompt_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_prompt_version("test-prompt_identifier", )
    mock_client.call.assert_called_once()


async def test_create_prompt_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_prompt_version("test-prompt_identifier", )


async def test_delete_agent_action_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", )
    mock_client.call.assert_called_once()


async def test_delete_agent_action_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", )


async def test_delete_agent_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_agent_alias("test-agent_id", "test-agent_alias_id", )
    mock_client.call.assert_called_once()


async def test_delete_agent_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_agent_alias("test-agent_id", "test-agent_alias_id", )


async def test_delete_agent_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_agent_version("test-agent_id", "test-agent_version", )
    mock_client.call.assert_called_once()


async def test_delete_agent_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_agent_version("test-agent_id", "test-agent_version", )


async def test_delete_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_source("test-knowledge_base_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_delete_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_source("test-knowledge_base_id", "test-data_source_id", )


async def test_delete_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_flow("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_flow("test-flow_identifier", )


async def test_delete_flow_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_flow_alias("test-flow_identifier", "test-alias_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_flow_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_flow_alias("test-flow_identifier", "test-alias_identifier", )


async def test_delete_flow_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_flow_version("test-flow_identifier", "test-flow_version", )
    mock_client.call.assert_called_once()


async def test_delete_flow_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_flow_version("test-flow_identifier", "test-flow_version", )


async def test_delete_knowledge_base_documents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )
    mock_client.call.assert_called_once()


async def test_delete_knowledge_base_documents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )


async def test_delete_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_prompt("test-prompt_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_prompt("test-prompt_identifier", )


async def test_disassociate_agent_collaborator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_agent_collaborator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", )


async def test_disassociate_agent_knowledge_base(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_agent_knowledge_base_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )


async def test_get_agent_action_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", )
    mock_client.call.assert_called_once()


async def test_get_agent_action_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", )


async def test_get_agent_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_agent_alias("test-agent_id", "test-agent_alias_id", )
    mock_client.call.assert_called_once()


async def test_get_agent_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_alias("test-agent_id", "test-agent_alias_id", )


async def test_get_agent_collaborator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", )
    mock_client.call.assert_called_once()


async def test_get_agent_collaborator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", )


async def test_get_agent_knowledge_base(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )
    mock_client.call.assert_called_once()


async def test_get_agent_knowledge_base_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )


async def test_get_agent_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_agent_version("test-agent_id", "test-agent_version", )
    mock_client.call.assert_called_once()


async def test_get_agent_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_agent_version("test-agent_id", "test-agent_version", )


async def test_get_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_get_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow("test-flow_identifier", )


async def test_get_flow_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_alias("test-flow_identifier", "test-alias_identifier", )
    mock_client.call.assert_called_once()


async def test_get_flow_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_alias("test-flow_identifier", "test-alias_identifier", )


async def test_get_flow_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_version("test-flow_identifier", "test-flow_version", )
    mock_client.call.assert_called_once()


async def test_get_flow_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_version("test-flow_identifier", "test-flow_version", )


async def test_get_knowledge_base_documents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )
    mock_client.call.assert_called_once()


async def test_get_knowledge_base_documents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )


async def test_get_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_prompt("test-prompt_identifier", )
    mock_client.call.assert_called_once()


async def test_get_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_prompt("test-prompt_identifier", )


async def test_ingest_knowledge_base_documents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )
    mock_client.call.assert_called_once()


async def test_ingest_knowledge_base_documents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], )


async def test_list_agent_action_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_action_groups("test-agent_id", "test-agent_version", )
    mock_client.call.assert_called_once()


async def test_list_agent_action_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_action_groups("test-agent_id", "test-agent_version", )


async def test_list_agent_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_aliases("test-agent_id", )
    mock_client.call.assert_called_once()


async def test_list_agent_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_aliases("test-agent_id", )


async def test_list_agent_collaborators(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_collaborators("test-agent_id", "test-agent_version", )
    mock_client.call.assert_called_once()


async def test_list_agent_collaborators_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_collaborators("test-agent_id", "test-agent_version", )


async def test_list_agent_knowledge_bases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_knowledge_bases("test-agent_id", "test-agent_version", )
    mock_client.call.assert_called_once()


async def test_list_agent_knowledge_bases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_knowledge_bases("test-agent_id", "test-agent_version", )


async def test_list_agent_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_versions("test-agent_id", )
    mock_client.call.assert_called_once()


async def test_list_agent_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_versions("test-agent_id", )


async def test_list_flow_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_flow_aliases("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_list_flow_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_flow_aliases("test-flow_identifier", )


async def test_list_flow_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_flow_versions("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_list_flow_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_flow_versions("test-flow_identifier", )


async def test_list_flows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_flows()
    mock_client.call.assert_called_once()


async def test_list_flows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_flows()


async def test_list_ingestion_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_list_ingestion_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", )


async def test_list_knowledge_base_documents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_list_knowledge_base_documents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", )


async def test_list_prompts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_prompts()
    mock_client.call.assert_called_once()


async def test_list_prompts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_prompts()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_prepare_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await prepare_flow("test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_prepare_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await prepare_flow("test-flow_identifier", )


async def test_stop_ingestion_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_ingestion_job("test-knowledge_base_id", "test-data_source_id", "test-ingestion_job_id", )
    mock_client.call.assert_called_once()


async def test_stop_ingestion_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_ingestion_job("test-knowledge_base_id", "test-data_source_id", "test-ingestion_job_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_agent_action_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", )
    mock_client.call.assert_called_once()


async def test_update_agent_action_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", )


async def test_update_agent_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", )
    mock_client.call.assert_called_once()


async def test_update_agent_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", )


async def test_update_agent_collaborator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", {}, "test-collaborator_name", "test-collaboration_instruction", )
    mock_client.call.assert_called_once()


async def test_update_agent_collaborator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", {}, "test-collaborator_name", "test-collaboration_instruction", )


async def test_update_agent_knowledge_base(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )
    mock_client.call.assert_called_once()


async def test_update_agent_knowledge_base_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", )


async def test_update_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, )


async def test_update_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", )
    mock_client.call.assert_called_once()


async def test_update_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", )


async def test_update_flow_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_flow_alias("test-name", [], "test-flow_identifier", "test-alias_identifier", )
    mock_client.call.assert_called_once()


async def test_update_flow_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_flow_alias("test-name", [], "test-flow_identifier", "test-alias_identifier", )


async def test_update_knowledge_base(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_knowledge_base_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, )


async def test_update_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_prompt("test-name", "test-prompt_identifier", )
    mock_client.call.assert_called_once()


async def test_update_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_prompt("test-name", "test-prompt_identifier", )


async def test_validate_flow_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_flow_definition({}, )
    mock_client.call.assert_called_once()


async def test_validate_flow_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.bedrock_agent.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_flow_definition({}, )


@pytest.mark.asyncio
async def test_list_agents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agents(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_knowledge_bases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_knowledge_bases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_knowledge_bases(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_data_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_data_sources("test-knowledge_base_id", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_ingestion_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import start_ingestion_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await start_ingestion_job("test-knowledge_base_id", "test-data_source_id", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_agent_collaborator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import associate_agent_collaborator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await associate_agent_collaborator("test-agent_id", "test-agent_version", "test-agent_descriptor", "test-collaborator_name", "test-collaboration_instruction", relay_conversation_history="test-relay_conversation_history", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_agent_action_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_agent_action_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", client_token="test-client_token", description="test-description", parent_action_group_signature="test-parent_action_group_signature", parent_action_group_signature_params="test-parent_action_group_signature_params", action_group_executor="test-action_group_executor", api_schema="test-api_schema", action_group_state="test-action_group_state", function_schema="test-function_schema", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_agent_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_agent_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_agent_alias("test-agent_id", "test-agent_alias_name", client_token="test-client_token", description="test-description", routing_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_flow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_flow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_flow("test-name", "test-execution_role_arn", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", definition={}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_flow_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_flow_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_flow_alias("test-name", {}, "test-flow_identifier", description="test-description", concurrency_configuration={}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_flow_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_flow_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_flow_version("test-flow_identifier", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_prompt("test-name", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", default_variant="test-default_variant", variants="test-variants", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_prompt_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import create_prompt_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await create_prompt_version("test-prompt_identifier", description="test-description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_agent_action_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_agent_action_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_agent_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_agent_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_agent_version("test-agent_id", "test-agent_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_flow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_flow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_flow("test-flow_identifier", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_flow_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_flow_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_flow_version("test-flow_identifier", "test-flow_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_knowledge_base_documents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", "test-document_identifiers", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import delete_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await delete_prompt("test-prompt_identifier", prompt_version="test-prompt_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import get_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await get_prompt("test-prompt_identifier", prompt_version="test-prompt_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_ingest_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import ingest_knowledge_base_documents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", "test-documents", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_action_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agent_action_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agent_action_groups("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agent_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agent_aliases("test-agent_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_collaborators_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agent_collaborators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agent_collaborators("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_knowledge_bases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agent_knowledge_bases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agent_knowledge_bases("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_agent_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_agent_versions("test-agent_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flow_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_flow_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_flow_aliases("test-flow_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flow_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_flow_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_flow_versions("test-flow_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_flows(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ingestion_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_ingestion_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", filters=[{}], sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_knowledge_base_documents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_prompts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import list_prompts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await list_prompts(prompt_identifier="test-prompt_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agent_action_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_agent_action_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", description="test-description", parent_action_group_signature="test-parent_action_group_signature", parent_action_group_signature_params="test-parent_action_group_signature_params", action_group_executor="test-action_group_executor", action_group_state="test-action_group_state", api_schema="test-api_schema", function_schema="test-function_schema", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agent_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_agent_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", description="test-description", routing_configuration={}, alias_invocation_state="test-alias_invocation_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agent_collaborator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_agent_collaborator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", "test-agent_descriptor", "test-collaborator_name", "test-collaboration_instruction", relay_conversation_history="test-relay_conversation_history", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agent_knowledge_base_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_agent_knowledge_base
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", description="test-description", knowledge_base_state="test-knowledge_base_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_source_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_data_source
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, description="test-description", data_deletion_policy="{}", server_side_encryption_configuration={}, vector_ingestion_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_flow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_flow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", definition={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_flow_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_flow_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_flow_alias("test-name", {}, "test-flow_identifier", "test-alias_identifier", description="test-description", concurrency_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_knowledge_base_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_knowledge_base
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, description="test-description", storage_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.bedrock_agent import update_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.bedrock_agent.async_client", lambda *a, **kw: mock_client)
    await update_prompt("test-name", "test-prompt_identifier", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", default_variant="test-default_variant", variants="test-variants", region_name="us-east-1")
    mock_client.call.assert_called_once()
