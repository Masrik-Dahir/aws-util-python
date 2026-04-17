"""Tests for aws_util.bedrock_agent module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.bedrock_agent as ba_mod
from aws_util.bedrock_agent import (
    AgentResult,
    DataSourceResult,
    IngestionJobResult,
    KnowledgeBaseResult,
    _parse_agent,
    _parse_data_source,
    _parse_ingestion_job,
    _parse_knowledge_base,
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


def _ce(code: str = "ValidationException", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _agent_dict(**ov):
    d = {
        "agentId": AGENT_ID,
        "agentName": AGENT_NAME,
        "agentArn": "arn:aws:bedrock:us-east-1:123:agent/agent-123",
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
# Model tests
# ---------------------------------------------------------------------------


def test_agent_result_model():
    r = AgentResult(agent_id="a1", agent_name="n1")
    assert r.agent_id == "a1"
    assert r.agent_arn == ""
    assert r.extra == {}


def test_knowledge_base_result_model():
    r = KnowledgeBaseResult(knowledge_base_id="k1", name="n1")
    assert r.knowledge_base_id == "k1"
    assert r.status == ""


def test_data_source_result_model():
    r = DataSourceResult(data_source_id="d1", knowledge_base_id="k1", name="n1")
    assert r.data_source_id == "d1"


def test_ingestion_job_result_model():
    r = IngestionJobResult(
        ingestion_job_id="i1", knowledge_base_id="k1", data_source_id="d1"
    )
    assert r.ingestion_job_id == "i1"
    assert r.failure_reasons == []
    assert r.statistics == {}


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


def test_parse_agent():
    r = _parse_agent(_agent_dict(extraField="x"))
    assert r.agent_id == AGENT_ID
    assert r.extra == {"extraField": "x"}


def test_parse_agent_empty():
    r = _parse_agent({})
    assert r.agent_id == ""
    assert r.agent_name == ""


def test_parse_knowledge_base():
    r = _parse_knowledge_base(_kb_dict(extraField="x"))
    assert r.knowledge_base_id == KB_ID
    assert r.extra == {"extraField": "x"}


def test_parse_knowledge_base_empty():
    r = _parse_knowledge_base({})
    assert r.knowledge_base_id == ""


def test_parse_data_source():
    r = _parse_data_source(_ds_dict(extraField="x"))
    assert r.data_source_id == DS_ID
    assert r.extra == {"extraField": "x"}


def test_parse_data_source_empty():
    r = _parse_data_source({})
    assert r.data_source_id == ""


def test_parse_ingestion_job():
    r = _parse_ingestion_job(_ij_dict(extraField="x"))
    assert r.ingestion_job_id == IJ_ID
    assert r.extra == {"extraField": "x"}


def test_parse_ingestion_job_empty():
    r = _parse_ingestion_job({})
    assert r.ingestion_job_id == ""
    assert r.failure_reasons == []


# ---------------------------------------------------------------------------
# Agent CRUD
# ---------------------------------------------------------------------------


def test_create_agent_minimal(monkeypatch):
    mc = MagicMock()
    mc.create_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN, region_name=REGION)
    assert r.agent_id == AGENT_ID


def test_create_agent_all_opts(monkeypatch):
    mc = MagicMock()
    mc.create_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_agent(
        AGENT_NAME,
        agent_resource_role_arn=ROLE_ARN,
        foundation_model="anthropic.claude-v2",
        instruction="help",
        description="desc",
        idle_session_ttl_in_seconds=600,
        region_name=REGION,
    )
    assert r.agent_name == AGENT_NAME
    call_kw = mc.create_agent.call_args[1]
    assert "foundationModel" in call_kw
    assert "instruction" in call_kw
    assert "description" in call_kw
    assert "idleSessionTTLInSeconds" in call_kw


def test_create_agent_error(monkeypatch):
    mc = MagicMock()
    mc.create_agent.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN)


def test_create_agent_no_agent_key(monkeypatch):
    mc = MagicMock()
    mc.create_agent.return_value = _agent_dict()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_agent(AGENT_NAME, agent_resource_role_arn=ROLE_ARN)
    assert r.agent_id == AGENT_ID


def test_get_agent_success(monkeypatch):
    mc = MagicMock()
    mc.get_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = get_agent(AGENT_ID, region_name=REGION)
    assert r.agent_id == AGENT_ID


def test_get_agent_no_key(monkeypatch):
    mc = MagicMock()
    mc.get_agent.return_value = _agent_dict()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = get_agent(AGENT_ID)
    assert r.agent_id == AGENT_ID


def test_get_agent_error(monkeypatch):
    mc = MagicMock()
    mc.get_agent.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        get_agent(AGENT_ID)


def test_list_agents_empty(monkeypatch):
    mc = MagicMock()
    mc.list_agents.return_value = {"agentSummaries": []}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_agents(region_name=REGION)
    assert r == []


def test_list_agents_pagination(monkeypatch):
    mc = MagicMock()
    mc.list_agents.side_effect = [
        {"agentSummaries": [_agent_dict()], "nextToken": "tok"},
        {"agentSummaries": [_agent_dict(agentId="agent-2")]},
    ]
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_agents(max_results=1, region_name=REGION)
    assert len(r) == 2
    assert r[1].agent_id == "agent-2"


def test_list_agents_error(monkeypatch):
    mc = MagicMock()
    mc.list_agents.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        list_agents()


def test_delete_agent_success(monkeypatch):
    mc = MagicMock()
    mc.delete_agent.return_value = {}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    delete_agent(AGENT_ID, region_name=REGION)
    mc.delete_agent.assert_called_once()


def test_delete_agent_skip_check(monkeypatch):
    mc = MagicMock()
    mc.delete_agent.return_value = {}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    delete_agent(AGENT_ID, skip_resource_in_use_check=True)
    kw = mc.delete_agent.call_args[1]
    assert kw["skipResourceInUseCheck"] is True


def test_delete_agent_error(monkeypatch):
    mc = MagicMock()
    mc.delete_agent.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        delete_agent(AGENT_ID)


def test_update_agent_minimal(monkeypatch):
    mc = MagicMock()
    mc.update_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = update_agent(AGENT_ID, AGENT_NAME, agent_resource_role_arn=ROLE_ARN)
    assert r.agent_id == AGENT_ID


def test_update_agent_all_opts(monkeypatch):
    mc = MagicMock()
    mc.update_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = update_agent(
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
    call_kw = mc.update_agent.call_args[1]
    assert "foundationModel" in call_kw
    assert "instruction" in call_kw
    assert "description" in call_kw
    assert "idleSessionTTLInSeconds" in call_kw


def test_update_agent_error(monkeypatch):
    mc = MagicMock()
    mc.update_agent.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        update_agent(AGENT_ID, AGENT_NAME, agent_resource_role_arn=ROLE_ARN)


def test_prepare_agent_success(monkeypatch):
    mc = MagicMock()
    mc.prepare_agent.return_value = {"agent": _agent_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = prepare_agent(AGENT_ID, region_name=REGION)
    assert r.agent_id == AGENT_ID


def test_prepare_agent_no_key(monkeypatch):
    mc = MagicMock()
    mc.prepare_agent.return_value = _agent_dict()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = prepare_agent(AGENT_ID)
    assert r.agent_id == AGENT_ID


def test_prepare_agent_error(monkeypatch):
    mc = MagicMock()
    mc.prepare_agent.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        prepare_agent(AGENT_ID)


# ---------------------------------------------------------------------------
# Knowledge Base CRUD
# ---------------------------------------------------------------------------


def test_create_knowledge_base_minimal(monkeypatch):
    mc = MagicMock()
    mc.create_knowledge_base.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_knowledge_base(
        "my-kb",
        role_arn=ROLE_ARN,
        knowledge_base_configuration={"type": "VECTOR"},
        storage_configuration={"type": "OPENSEARCH"},
    )
    assert r.knowledge_base_id == KB_ID


def test_create_knowledge_base_with_desc(monkeypatch):
    mc = MagicMock()
    mc.create_knowledge_base.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_knowledge_base(
        "my-kb",
        role_arn=ROLE_ARN,
        knowledge_base_configuration={"type": "VECTOR"},
        storage_configuration={"type": "OPENSEARCH"},
        description="test desc",
        region_name=REGION,
    )
    assert r.name == "my-kb"
    kw = mc.create_knowledge_base.call_args[1]
    assert kw["description"] == "test desc"


def test_create_knowledge_base_error(monkeypatch):
    mc = MagicMock()
    mc.create_knowledge_base.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        create_knowledge_base(
            "kb",
            role_arn=ROLE_ARN,
            knowledge_base_configuration={},
            storage_configuration={},
        )


def test_get_knowledge_base_success(monkeypatch):
    mc = MagicMock()
    mc.get_knowledge_base.return_value = {"knowledgeBase": _kb_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = get_knowledge_base(KB_ID, region_name=REGION)
    assert r.knowledge_base_id == KB_ID


def test_get_knowledge_base_error(monkeypatch):
    mc = MagicMock()
    mc.get_knowledge_base.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        get_knowledge_base(KB_ID)


def test_list_knowledge_bases_empty(monkeypatch):
    mc = MagicMock()
    mc.list_knowledge_bases.return_value = {"knowledgeBaseSummaries": []}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_knowledge_bases()
    assert r == []


def test_list_knowledge_bases_pagination(monkeypatch):
    mc = MagicMock()
    mc.list_knowledge_bases.side_effect = [
        {"knowledgeBaseSummaries": [_kb_dict()], "nextToken": "tok"},
        {"knowledgeBaseSummaries": [_kb_dict(knowledgeBaseId="kb-2")]},
    ]
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_knowledge_bases(max_results=1)
    assert len(r) == 2


def test_list_knowledge_bases_error(monkeypatch):
    mc = MagicMock()
    mc.list_knowledge_bases.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        list_knowledge_bases()


def test_delete_knowledge_base_success(monkeypatch):
    mc = MagicMock()
    mc.delete_knowledge_base.return_value = {}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    delete_knowledge_base(KB_ID, region_name=REGION)
    mc.delete_knowledge_base.assert_called_once()


def test_delete_knowledge_base_error(monkeypatch):
    mc = MagicMock()
    mc.delete_knowledge_base.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        delete_knowledge_base(KB_ID)


# ---------------------------------------------------------------------------
# Associate
# ---------------------------------------------------------------------------


def test_associate_agent_knowledge_base_success(monkeypatch):
    mc = MagicMock()
    mc.associate_agent_knowledge_base.return_value = {"ok": True}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = associate_agent_knowledge_base(
        AGENT_ID, "DRAFT", KB_ID, region_name=REGION
    )
    assert r == {"ok": True}


def test_associate_agent_knowledge_base_custom(monkeypatch):
    mc = MagicMock()
    mc.associate_agent_knowledge_base.return_value = {"ok": True}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = associate_agent_knowledge_base(
        AGENT_ID,
        "DRAFT",
        KB_ID,
        description="use this kb",
        knowledge_base_state="DISABLED",
    )
    assert r["ok"]


def test_associate_agent_knowledge_base_error(monkeypatch):
    mc = MagicMock()
    mc.associate_agent_knowledge_base.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        associate_agent_knowledge_base(AGENT_ID, "DRAFT", KB_ID)


# ---------------------------------------------------------------------------
# Data Source CRUD
# ---------------------------------------------------------------------------


def test_create_data_source_minimal(monkeypatch):
    mc = MagicMock()
    mc.create_data_source.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_data_source(
        KB_ID, "my-ds", data_source_configuration={"type": "S3"}
    )
    assert r.data_source_id == DS_ID


def test_create_data_source_with_desc(monkeypatch):
    mc = MagicMock()
    mc.create_data_source.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = create_data_source(
        KB_ID,
        "my-ds",
        data_source_configuration={"type": "S3"},
        description="hello",
        region_name=REGION,
    )
    assert r.name == "my-ds"
    kw = mc.create_data_source.call_args[1]
    assert kw["description"] == "hello"


def test_create_data_source_error(monkeypatch):
    mc = MagicMock()
    mc.create_data_source.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        create_data_source(KB_ID, "ds", data_source_configuration={})


def test_get_data_source_success(monkeypatch):
    mc = MagicMock()
    mc.get_data_source.return_value = {"dataSource": _ds_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = get_data_source(KB_ID, DS_ID, region_name=REGION)
    assert r.data_source_id == DS_ID


def test_get_data_source_error(monkeypatch):
    mc = MagicMock()
    mc.get_data_source.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        get_data_source(KB_ID, DS_ID)


def test_list_data_sources_empty(monkeypatch):
    mc = MagicMock()
    mc.list_data_sources.return_value = {"dataSourceSummaries": []}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_data_sources(KB_ID)
    assert r == []


def test_list_data_sources_pagination(monkeypatch):
    mc = MagicMock()
    mc.list_data_sources.side_effect = [
        {"dataSourceSummaries": [_ds_dict()], "nextToken": "tok"},
        {"dataSourceSummaries": [_ds_dict(dataSourceId="ds-2")]},
    ]
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = list_data_sources(KB_ID, max_results=1)
    assert len(r) == 2


def test_list_data_sources_error(monkeypatch):
    mc = MagicMock()
    mc.list_data_sources.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        list_data_sources(KB_ID)


# ---------------------------------------------------------------------------
# Ingestion Jobs
# ---------------------------------------------------------------------------


def test_start_ingestion_job_minimal(monkeypatch):
    mc = MagicMock()
    mc.start_ingestion_job.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = start_ingestion_job(KB_ID, DS_ID)
    assert r.ingestion_job_id == IJ_ID


def test_start_ingestion_job_with_desc(monkeypatch):
    mc = MagicMock()
    mc.start_ingestion_job.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = start_ingestion_job(KB_ID, DS_ID, description="d", region_name=REGION)
    assert r.status == "COMPLETE"
    kw = mc.start_ingestion_job.call_args[1]
    assert kw["description"] == "d"


def test_start_ingestion_job_error(monkeypatch):
    mc = MagicMock()
    mc.start_ingestion_job.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        start_ingestion_job(KB_ID, DS_ID)


def test_get_ingestion_job_success(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.return_value = {"ingestionJob": _ij_dict()}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = get_ingestion_job(KB_ID, DS_ID, IJ_ID, region_name=REGION)
    assert r.ingestion_job_id == IJ_ID


def test_get_ingestion_job_error(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.side_effect = _ce()
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError):
        get_ingestion_job(KB_ID, DS_ID, IJ_ID)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


def test_wait_for_agent_immediate(monkeypatch):
    mc = MagicMock()
    mc.get_agent.return_value = {"agent": _agent_dict(agentStatus="PREPARED")}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = wait_for_agent(AGENT_ID, region_name=REGION)
    assert r.agent_status == "PREPARED"


def test_wait_for_agent_failure_status(monkeypatch):
    mc = MagicMock()
    mc.get_agent.return_value = {"agent": _agent_dict(agentStatus="FAILED")}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="failure status"):
        wait_for_agent(AGENT_ID)


def test_wait_for_agent_timeout(monkeypatch):
    mc = MagicMock()
    mc.get_agent.return_value = {"agent": _agent_dict(agentStatus="CREATING")}
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    times = iter([100.0, 100.0, 999.0])
    monkeypatch.setattr(time, "monotonic", lambda: next(times))
    monkeypatch.setattr(time, "sleep", lambda s: None)
    with pytest.raises(AwsTimeoutError):
        wait_for_agent(AGENT_ID, timeout=10)


def test_wait_for_agent_poll_then_success(monkeypatch):
    mc = MagicMock()
    mc.get_agent.side_effect = [
        {"agent": _agent_dict(agentStatus="CREATING")},
        {"agent": _agent_dict(agentStatus="PREPARED")},
    ]
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    monkeypatch.setattr(time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    r = wait_for_agent(AGENT_ID, timeout=300)
    assert r.agent_status == "PREPARED"


def test_wait_for_ingestion_job_immediate(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.return_value = {
        "ingestionJob": _ij_dict(status="COMPLETE")
    }
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    r = wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, region_name=REGION)
    assert r.status == "COMPLETE"


def test_wait_for_ingestion_job_failure(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.return_value = {
        "ingestionJob": _ij_dict(status="FAILED")
    }
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="failure"):
        wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID)


def test_wait_for_ingestion_job_timeout(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.return_value = {
        "ingestionJob": _ij_dict(status="IN_PROGRESS")
    }
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    times = iter([100.0, 100.0, 999.0])
    monkeypatch.setattr(time, "monotonic", lambda: next(times))
    monkeypatch.setattr(time, "sleep", lambda s: None)
    with pytest.raises(AwsTimeoutError):
        wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, timeout=10)


def test_wait_for_ingestion_job_poll_then_success(monkeypatch):
    mc = MagicMock()
    mc.get_ingestion_job.side_effect = [
        {"ingestionJob": _ij_dict(status="IN_PROGRESS")},
        {"ingestionJob": _ij_dict(status="COMPLETE")},
    ]
    monkeypatch.setattr(ba_mod, "get_client", lambda *a, **kw: mc)
    monkeypatch.setattr(time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(time, "sleep", lambda s: None)
    r = wait_for_ingestion_job(KB_ID, DS_ID, IJ_ID, timeout=600)
    assert r.status == "COMPLETE"


def test_associate_agent_collaborator(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    associate_agent_collaborator("test-agent_id", "test-agent_version", {}, "test-collaborator_name", "test-collaboration_instruction", region_name=REGION)
    mock_client.associate_agent_collaborator.assert_called_once()


def test_associate_agent_collaborator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_agent_collaborator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_agent_collaborator",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate agent collaborator"):
        associate_agent_collaborator("test-agent_id", "test-agent_version", {}, "test-collaborator_name", "test-collaboration_instruction", region_name=REGION)


def test_create_agent_action_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", region_name=REGION)
    mock_client.create_agent_action_group.assert_called_once()


def test_create_agent_action_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_action_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_agent_action_group",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create agent action group"):
        create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", region_name=REGION)


def test_create_agent_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_agent_alias("test-agent_id", "test-agent_alias_name", region_name=REGION)
    mock_client.create_agent_alias.assert_called_once()


def test_create_agent_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_agent_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create agent alias"):
        create_agent_alias("test-agent_id", "test-agent_alias_name", region_name=REGION)


def test_create_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow("test-name", "test-execution_role_arn", region_name=REGION)
    mock_client.create_flow.assert_called_once()


def test_create_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create flow"):
        create_flow("test-name", "test-execution_role_arn", region_name=REGION)


def test_create_flow_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow_alias("test-name", [], "test-flow_identifier", region_name=REGION)
    mock_client.create_flow_alias.assert_called_once()


def test_create_flow_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_flow_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create flow alias"):
        create_flow_alias("test-name", [], "test-flow_identifier", region_name=REGION)


def test_create_flow_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow_version("test-flow_identifier", region_name=REGION)
    mock_client.create_flow_version.assert_called_once()


def test_create_flow_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_flow_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create flow version"):
        create_flow_version("test-flow_identifier", region_name=REGION)


def test_create_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_prompt("test-name", region_name=REGION)
    mock_client.create_prompt.assert_called_once()


def test_create_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_prompt",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create prompt"):
        create_prompt("test-name", region_name=REGION)


def test_create_prompt_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_prompt_version("test-prompt_identifier", region_name=REGION)
    mock_client.create_prompt_version.assert_called_once()


def test_create_prompt_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_prompt_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create prompt version"):
        create_prompt_version("test-prompt_identifier", region_name=REGION)


def test_delete_agent_action_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", region_name=REGION)
    mock_client.delete_agent_action_group.assert_called_once()


def test_delete_agent_action_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_action_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_agent_action_group",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete agent action group"):
        delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", region_name=REGION)


def test_delete_agent_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_agent_alias("test-agent_id", "test-agent_alias_id", region_name=REGION)
    mock_client.delete_agent_alias.assert_called_once()


def test_delete_agent_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_agent_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete agent alias"):
        delete_agent_alias("test-agent_id", "test-agent_alias_id", region_name=REGION)


def test_delete_agent_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_agent_version("test-agent_id", "test-agent_version", region_name=REGION)
    mock_client.delete_agent_version.assert_called_once()


def test_delete_agent_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_agent_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_agent_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete agent version"):
        delete_agent_version("test-agent_id", "test-agent_version", region_name=REGION)


def test_delete_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_source.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_data_source("test-knowledge_base_id", "test-data_source_id", region_name=REGION)
    mock_client.delete_data_source.assert_called_once()


def test_delete_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_source",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data source"):
        delete_data_source("test-knowledge_base_id", "test-data_source_id", region_name=REGION)


def test_delete_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_flow("test-flow_identifier", region_name=REGION)
    mock_client.delete_flow.assert_called_once()


def test_delete_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete flow"):
        delete_flow("test-flow_identifier", region_name=REGION)


def test_delete_flow_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_flow_alias("test-flow_identifier", "test-alias_identifier", region_name=REGION)
    mock_client.delete_flow_alias.assert_called_once()


def test_delete_flow_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_flow_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete flow alias"):
        delete_flow_alias("test-flow_identifier", "test-alias_identifier", region_name=REGION)


def test_delete_flow_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_flow_version("test-flow_identifier", "test-flow_version", region_name=REGION)
    mock_client.delete_flow_version.assert_called_once()


def test_delete_flow_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_flow_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete flow version"):
        delete_flow_version("test-flow_identifier", "test-flow_version", region_name=REGION)


def test_delete_knowledge_base_documents(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)
    mock_client.delete_knowledge_base_documents.assert_called_once()


def test_delete_knowledge_base_documents_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_knowledge_base_documents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_knowledge_base_documents",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete knowledge base documents"):
        delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)


def test_delete_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_prompt("test-prompt_identifier", region_name=REGION)
    mock_client.delete_prompt.assert_called_once()


def test_delete_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_prompt",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete prompt"):
        delete_prompt("test-prompt_identifier", region_name=REGION)


def test_disassociate_agent_collaborator(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    disassociate_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", region_name=REGION)
    mock_client.disassociate_agent_collaborator.assert_called_once()


def test_disassociate_agent_collaborator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_agent_collaborator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_agent_collaborator",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate agent collaborator"):
        disassociate_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", region_name=REGION)


def test_disassociate_agent_knowledge_base(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_agent_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    disassociate_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)
    mock_client.disassociate_agent_knowledge_base.assert_called_once()


def test_disassociate_agent_knowledge_base_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_agent_knowledge_base.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_agent_knowledge_base",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate agent knowledge base"):
        disassociate_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)


def test_get_agent_action_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", region_name=REGION)
    mock_client.get_agent_action_group.assert_called_once()


def test_get_agent_action_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_action_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_action_group",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent action group"):
        get_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", region_name=REGION)


def test_get_agent_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_agent_alias("test-agent_id", "test-agent_alias_id", region_name=REGION)
    mock_client.get_agent_alias.assert_called_once()


def test_get_agent_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent alias"):
        get_agent_alias("test-agent_id", "test-agent_alias_id", region_name=REGION)


def test_get_agent_collaborator(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", region_name=REGION)
    mock_client.get_agent_collaborator.assert_called_once()


def test_get_agent_collaborator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_collaborator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_collaborator",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent collaborator"):
        get_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", region_name=REGION)


def test_get_agent_knowledge_base(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)
    mock_client.get_agent_knowledge_base.assert_called_once()


def test_get_agent_knowledge_base_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_knowledge_base.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_knowledge_base",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent knowledge base"):
        get_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)


def test_get_agent_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_agent_version("test-agent_id", "test-agent_version", region_name=REGION)
    mock_client.get_agent_version.assert_called_once()


def test_get_agent_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_agent_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_agent_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get agent version"):
        get_agent_version("test-agent_id", "test-agent_version", region_name=REGION)


def test_get_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_flow("test-flow_identifier", region_name=REGION)
    mock_client.get_flow.assert_called_once()


def test_get_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow"):
        get_flow("test-flow_identifier", region_name=REGION)


def test_get_flow_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_flow_alias("test-flow_identifier", "test-alias_identifier", region_name=REGION)
    mock_client.get_flow_alias.assert_called_once()


def test_get_flow_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow alias"):
        get_flow_alias("test-flow_identifier", "test-alias_identifier", region_name=REGION)


def test_get_flow_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_flow_version("test-flow_identifier", "test-flow_version", region_name=REGION)
    mock_client.get_flow_version.assert_called_once()


def test_get_flow_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_version",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow version"):
        get_flow_version("test-flow_identifier", "test-flow_version", region_name=REGION)


def test_get_knowledge_base_documents(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)
    mock_client.get_knowledge_base_documents.assert_called_once()


def test_get_knowledge_base_documents_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_knowledge_base_documents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_knowledge_base_documents",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get knowledge base documents"):
        get_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)


def test_get_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_prompt("test-prompt_identifier", region_name=REGION)
    mock_client.get_prompt.assert_called_once()


def test_get_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_prompt",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get prompt"):
        get_prompt("test-prompt_identifier", region_name=REGION)


def test_ingest_knowledge_base_documents(monkeypatch):
    mock_client = MagicMock()
    mock_client.ingest_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)
    mock_client.ingest_knowledge_base_documents.assert_called_once()


def test_ingest_knowledge_base_documents_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.ingest_knowledge_base_documents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "ingest_knowledge_base_documents",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to ingest knowledge base documents"):
        ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", [], region_name=REGION)


def test_list_agent_action_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_action_groups.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_action_groups("test-agent_id", "test-agent_version", region_name=REGION)
    mock_client.list_agent_action_groups.assert_called_once()


def test_list_agent_action_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_action_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_action_groups",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent action groups"):
        list_agent_action_groups("test-agent_id", "test-agent_version", region_name=REGION)


def test_list_agent_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_aliases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_aliases("test-agent_id", region_name=REGION)
    mock_client.list_agent_aliases.assert_called_once()


def test_list_agent_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_aliases",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent aliases"):
        list_agent_aliases("test-agent_id", region_name=REGION)


def test_list_agent_collaborators(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_collaborators.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_collaborators("test-agent_id", "test-agent_version", region_name=REGION)
    mock_client.list_agent_collaborators.assert_called_once()


def test_list_agent_collaborators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_collaborators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_collaborators",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent collaborators"):
        list_agent_collaborators("test-agent_id", "test-agent_version", region_name=REGION)


def test_list_agent_knowledge_bases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_knowledge_bases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_knowledge_bases("test-agent_id", "test-agent_version", region_name=REGION)
    mock_client.list_agent_knowledge_bases.assert_called_once()


def test_list_agent_knowledge_bases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_knowledge_bases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_knowledge_bases",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent knowledge bases"):
        list_agent_knowledge_bases("test-agent_id", "test-agent_version", region_name=REGION)


def test_list_agent_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_versions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_versions("test-agent_id", region_name=REGION)
    mock_client.list_agent_versions.assert_called_once()


def test_list_agent_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_versions",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent versions"):
        list_agent_versions("test-agent_id", region_name=REGION)


def test_list_flow_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_aliases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flow_aliases("test-flow_identifier", region_name=REGION)
    mock_client.list_flow_aliases.assert_called_once()


def test_list_flow_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flow_aliases",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flow aliases"):
        list_flow_aliases("test-flow_identifier", region_name=REGION)


def test_list_flow_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_versions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flow_versions("test-flow_identifier", region_name=REGION)
    mock_client.list_flow_versions.assert_called_once()


def test_list_flow_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flow_versions",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flow versions"):
        list_flow_versions("test-flow_identifier", region_name=REGION)


def test_list_flows(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flows.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flows(region_name=REGION)
    mock_client.list_flows.assert_called_once()


def test_list_flows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flows",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flows"):
        list_flows(region_name=REGION)


def test_list_ingestion_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ingestion_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", region_name=REGION)
    mock_client.list_ingestion_jobs.assert_called_once()


def test_list_ingestion_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ingestion_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ingestion_jobs",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ingestion jobs"):
        list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", region_name=REGION)


def test_list_knowledge_base_documents(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", region_name=REGION)
    mock_client.list_knowledge_base_documents.assert_called_once()


def test_list_knowledge_base_documents_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_knowledge_base_documents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_knowledge_base_documents",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list knowledge base documents"):
        list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", region_name=REGION)


def test_list_prompts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompts.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_prompts(region_name=REGION)
    mock_client.list_prompts.assert_called_once()


def test_list_prompts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_prompts",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list prompts"):
        list_prompts(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_prepare_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.prepare_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    prepare_flow("test-flow_identifier", region_name=REGION)
    mock_client.prepare_flow.assert_called_once()


def test_prepare_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.prepare_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "prepare_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to prepare flow"):
        prepare_flow("test-flow_identifier", region_name=REGION)


def test_stop_ingestion_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_ingestion_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    stop_ingestion_job("test-knowledge_base_id", "test-data_source_id", "test-ingestion_job_id", region_name=REGION)
    mock_client.stop_ingestion_job.assert_called_once()


def test_stop_ingestion_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_ingestion_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_ingestion_job",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop ingestion job"):
        stop_ingestion_job("test-knowledge_base_id", "test-data_source_id", "test-ingestion_job_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_agent_action_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", region_name=REGION)
    mock_client.update_agent_action_group.assert_called_once()


def test_update_agent_action_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_action_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agent_action_group",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agent action group"):
        update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", region_name=REGION)


def test_update_agent_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", region_name=REGION)
    mock_client.update_agent_alias.assert_called_once()


def test_update_agent_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agent_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agent alias"):
        update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", region_name=REGION)


def test_update_agent_collaborator(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", {}, "test-collaborator_name", "test-collaboration_instruction", region_name=REGION)
    mock_client.update_agent_collaborator.assert_called_once()


def test_update_agent_collaborator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_collaborator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agent_collaborator",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agent collaborator"):
        update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", {}, "test-collaborator_name", "test-collaboration_instruction", region_name=REGION)


def test_update_agent_knowledge_base(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)
    mock_client.update_agent_knowledge_base.assert_called_once()


def test_update_agent_knowledge_base_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_knowledge_base.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agent_knowledge_base",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agent knowledge base"):
        update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", region_name=REGION)


def test_update_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, region_name=REGION)
    mock_client.update_data_source.assert_called_once()


def test_update_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_source",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data source"):
        update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, region_name=REGION)


def test_update_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", region_name=REGION)
    mock_client.update_flow.assert_called_once()


def test_update_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_flow",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update flow"):
        update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", region_name=REGION)


def test_update_flow_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_flow_alias("test-name", [], "test-flow_identifier", "test-alias_identifier", region_name=REGION)
    mock_client.update_flow_alias.assert_called_once()


def test_update_flow_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_flow_alias",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update flow alias"):
        update_flow_alias("test-name", [], "test-flow_identifier", "test-alias_identifier", region_name=REGION)


def test_update_knowledge_base(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, region_name=REGION)
    mock_client.update_knowledge_base.assert_called_once()


def test_update_knowledge_base_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_knowledge_base.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_knowledge_base",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update knowledge base"):
        update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, region_name=REGION)


def test_update_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_prompt("test-name", "test-prompt_identifier", region_name=REGION)
    mock_client.update_prompt.assert_called_once()


def test_update_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_prompt",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update prompt"):
        update_prompt("test-name", "test-prompt_identifier", region_name=REGION)


def test_validate_flow_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_flow_definition.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    validate_flow_definition({}, region_name=REGION)
    mock_client.validate_flow_definition.assert_called_once()


def test_validate_flow_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_flow_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_flow_definition",
    )
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to validate flow definition"):
        validate_flow_definition({}, region_name=REGION)


def test_list_agents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agents
    mock_client = MagicMock()
    mock_client.list_agents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agents(max_results=1, region_name="us-east-1")
    mock_client.list_agents.assert_called_once()

def test_list_knowledge_bases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_knowledge_bases
    mock_client = MagicMock()
    mock_client.list_knowledge_bases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_knowledge_bases(max_results=1, region_name="us-east-1")
    mock_client.list_knowledge_bases.assert_called_once()

def test_list_data_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_data_sources
    mock_client = MagicMock()
    mock_client.list_data_sources.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_data_sources("test-knowledge_base_id", max_results=1, region_name="us-east-1")
    mock_client.list_data_sources.assert_called_once()

def test_start_ingestion_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import start_ingestion_job
    mock_client = MagicMock()
    mock_client.start_ingestion_job.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    start_ingestion_job("test-knowledge_base_id", "test-data_source_id", description="test-description", region_name="us-east-1")
    mock_client.start_ingestion_job.assert_called_once()

def test_associate_agent_collaborator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import associate_agent_collaborator
    mock_client = MagicMock()
    mock_client.associate_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    associate_agent_collaborator("test-agent_id", "test-agent_version", "test-agent_descriptor", "test-collaborator_name", "test-collaboration_instruction", relay_conversation_history="test-relay_conversation_history", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_agent_collaborator.assert_called_once()

def test_create_agent_action_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_agent_action_group
    mock_client = MagicMock()
    mock_client.create_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_name", client_token="test-client_token", description="test-description", parent_action_group_signature="test-parent_action_group_signature", parent_action_group_signature_params="test-parent_action_group_signature_params", action_group_executor="test-action_group_executor", api_schema="test-api_schema", action_group_state="test-action_group_state", function_schema="test-function_schema", region_name="us-east-1")
    mock_client.create_agent_action_group.assert_called_once()

def test_create_agent_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_agent_alias
    mock_client = MagicMock()
    mock_client.create_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_agent_alias("test-agent_id", "test-agent_alias_name", client_token="test-client_token", description="test-description", routing_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_agent_alias.assert_called_once()

def test_create_flow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_flow
    mock_client = MagicMock()
    mock_client.create_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow("test-name", "test-execution_role_arn", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", definition={}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_flow.assert_called_once()

def test_create_flow_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_flow_alias
    mock_client = MagicMock()
    mock_client.create_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow_alias("test-name", {}, "test-flow_identifier", description="test-description", concurrency_configuration={}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_flow_alias.assert_called_once()

def test_create_flow_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_flow_version
    mock_client = MagicMock()
    mock_client.create_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_flow_version("test-flow_identifier", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_flow_version.assert_called_once()

def test_create_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_prompt
    mock_client = MagicMock()
    mock_client.create_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_prompt("test-name", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", default_variant="test-default_variant", variants="test-variants", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_prompt.assert_called_once()

def test_create_prompt_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import create_prompt_version
    mock_client = MagicMock()
    mock_client.create_prompt_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    create_prompt_version("test-prompt_identifier", description="test-description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_prompt_version.assert_called_once()

def test_delete_agent_action_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_agent_action_group
    mock_client = MagicMock()
    mock_client.delete_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_agent_action_group.assert_called_once()

def test_delete_agent_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_agent_version
    mock_client = MagicMock()
    mock_client.delete_agent_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_agent_version("test-agent_id", "test-agent_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_agent_version.assert_called_once()

def test_delete_flow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_flow
    mock_client = MagicMock()
    mock_client.delete_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_flow("test-flow_identifier", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_flow.assert_called_once()

def test_delete_flow_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_flow_version
    mock_client = MagicMock()
    mock_client.delete_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_flow_version("test-flow_identifier", "test-flow_version", skip_resource_in_use_check=True, region_name="us-east-1")
    mock_client.delete_flow_version.assert_called_once()

def test_delete_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_knowledge_base_documents
    mock_client = MagicMock()
    mock_client.delete_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", "test-document_identifiers", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_knowledge_base_documents.assert_called_once()

def test_delete_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import delete_prompt
    mock_client = MagicMock()
    mock_client.delete_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    delete_prompt("test-prompt_identifier", prompt_version="test-prompt_version", region_name="us-east-1")
    mock_client.delete_prompt.assert_called_once()

def test_get_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import get_prompt
    mock_client = MagicMock()
    mock_client.get_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    get_prompt("test-prompt_identifier", prompt_version="test-prompt_version", region_name="us-east-1")
    mock_client.get_prompt.assert_called_once()

def test_ingest_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import ingest_knowledge_base_documents
    mock_client = MagicMock()
    mock_client.ingest_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    ingest_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", "test-documents", client_token="test-client_token", region_name="us-east-1")
    mock_client.ingest_knowledge_base_documents.assert_called_once()

def test_list_agent_action_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agent_action_groups
    mock_client = MagicMock()
    mock_client.list_agent_action_groups.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_action_groups("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agent_action_groups.assert_called_once()

def test_list_agent_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agent_aliases
    mock_client = MagicMock()
    mock_client.list_agent_aliases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_aliases("test-agent_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agent_aliases.assert_called_once()

def test_list_agent_collaborators_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agent_collaborators
    mock_client = MagicMock()
    mock_client.list_agent_collaborators.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_collaborators("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agent_collaborators.assert_called_once()

def test_list_agent_knowledge_bases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agent_knowledge_bases
    mock_client = MagicMock()
    mock_client.list_agent_knowledge_bases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_knowledge_bases("test-agent_id", "test-agent_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agent_knowledge_bases.assert_called_once()

def test_list_agent_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_agent_versions
    mock_client = MagicMock()
    mock_client.list_agent_versions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_agent_versions("test-agent_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_agent_versions.assert_called_once()

def test_list_flow_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_flow_aliases
    mock_client = MagicMock()
    mock_client.list_flow_aliases.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flow_aliases("test-flow_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_flow_aliases.assert_called_once()

def test_list_flow_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_flow_versions
    mock_client = MagicMock()
    mock_client.list_flow_versions.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flow_versions("test-flow_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_flow_versions.assert_called_once()

def test_list_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_flows
    mock_client = MagicMock()
    mock_client.list_flows.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_flows(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_flows.assert_called_once()

def test_list_ingestion_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_ingestion_jobs
    mock_client = MagicMock()
    mock_client.list_ingestion_jobs.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_ingestion_jobs("test-knowledge_base_id", "test-data_source_id", filters=[{}], sort_by="test-sort_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_ingestion_jobs.assert_called_once()

def test_list_knowledge_base_documents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_knowledge_base_documents
    mock_client = MagicMock()
    mock_client.list_knowledge_base_documents.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_knowledge_base_documents("test-knowledge_base_id", "test-data_source_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_knowledge_base_documents.assert_called_once()

def test_list_prompts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import list_prompts
    mock_client = MagicMock()
    mock_client.list_prompts.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    list_prompts(prompt_identifier="test-prompt_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_prompts.assert_called_once()

def test_update_agent_action_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_agent_action_group
    mock_client = MagicMock()
    mock_client.update_agent_action_group.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_action_group("test-agent_id", "test-agent_version", "test-action_group_id", "test-action_group_name", description="test-description", parent_action_group_signature="test-parent_action_group_signature", parent_action_group_signature_params="test-parent_action_group_signature_params", action_group_executor="test-action_group_executor", action_group_state="test-action_group_state", api_schema="test-api_schema", function_schema="test-function_schema", region_name="us-east-1")
    mock_client.update_agent_action_group.assert_called_once()

def test_update_agent_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_agent_alias
    mock_client = MagicMock()
    mock_client.update_agent_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_alias("test-agent_id", "test-agent_alias_id", "test-agent_alias_name", description="test-description", routing_configuration={}, alias_invocation_state="test-alias_invocation_state", region_name="us-east-1")
    mock_client.update_agent_alias.assert_called_once()

def test_update_agent_collaborator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_agent_collaborator
    mock_client = MagicMock()
    mock_client.update_agent_collaborator.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_collaborator("test-agent_id", "test-agent_version", "test-collaborator_id", "test-agent_descriptor", "test-collaborator_name", "test-collaboration_instruction", relay_conversation_history="test-relay_conversation_history", region_name="us-east-1")
    mock_client.update_agent_collaborator.assert_called_once()

def test_update_agent_knowledge_base_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_agent_knowledge_base
    mock_client = MagicMock()
    mock_client.update_agent_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_agent_knowledge_base("test-agent_id", "test-agent_version", "test-knowledge_base_id", description="test-description", knowledge_base_state="test-knowledge_base_state", region_name="us-east-1")
    mock_client.update_agent_knowledge_base.assert_called_once()

def test_update_data_source_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_data_source
    mock_client = MagicMock()
    mock_client.update_data_source.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_data_source("test-knowledge_base_id", "test-data_source_id", "test-name", {}, description="test-description", data_deletion_policy="{}", server_side_encryption_configuration={}, vector_ingestion_configuration={}, region_name="us-east-1")
    mock_client.update_data_source.assert_called_once()

def test_update_flow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_flow
    mock_client = MagicMock()
    mock_client.update_flow.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_flow("test-name", "test-execution_role_arn", "test-flow_identifier", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", definition={}, region_name="us-east-1")
    mock_client.update_flow.assert_called_once()

def test_update_flow_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_flow_alias
    mock_client = MagicMock()
    mock_client.update_flow_alias.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_flow_alias("test-name", {}, "test-flow_identifier", "test-alias_identifier", description="test-description", concurrency_configuration={}, region_name="us-east-1")
    mock_client.update_flow_alias.assert_called_once()

def test_update_knowledge_base_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_knowledge_base
    mock_client = MagicMock()
    mock_client.update_knowledge_base.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_knowledge_base("test-knowledge_base_id", "test-name", "test-role_arn", {}, description="test-description", storage_configuration={}, region_name="us-east-1")
    mock_client.update_knowledge_base.assert_called_once()

def test_update_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.bedrock_agent import update_prompt
    mock_client = MagicMock()
    mock_client.update_prompt.return_value = {}
    monkeypatch.setattr("aws_util.bedrock_agent.get_client", lambda *a, **kw: mock_client)
    update_prompt("test-name", "test-prompt_identifier", description="test-description", customer_encryption_key_arn="test-customer_encryption_key_arn", default_variant="test-default_variant", variants="test-variants", region_name="us-east-1")
    mock_client.update_prompt.assert_called_once()
