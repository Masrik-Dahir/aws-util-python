"""aws_util.bedrock_agent --- AWS Bedrock Agent management utilities.

Provides high-level helpers for creating, managing, and monitoring
AWS Bedrock Agents, knowledge bases, data sources, and ingestion jobs.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AgentResult",
    "AssociateAgentCollaboratorResult",
    "CreateAgentActionGroupResult",
    "CreateAgentAliasResult",
    "CreateFlowAliasResult",
    "CreateFlowResult",
    "CreateFlowVersionResult",
    "CreatePromptResult",
    "CreatePromptVersionResult",
    "DataSourceResult",
    "DeleteAgentAliasResult",
    "DeleteAgentVersionResult",
    "DeleteDataSourceResult",
    "DeleteFlowAliasResult",
    "DeleteFlowResult",
    "DeleteFlowVersionResult",
    "DeleteKnowledgeBaseDocumentsResult",
    "DeletePromptResult",
    "GetAgentActionGroupResult",
    "GetAgentAliasResult",
    "GetAgentCollaboratorResult",
    "GetAgentKnowledgeBaseResult",
    "GetAgentVersionResult",
    "GetFlowAliasResult",
    "GetFlowResult",
    "GetFlowVersionResult",
    "GetKnowledgeBaseDocumentsResult",
    "GetPromptResult",
    "IngestKnowledgeBaseDocumentsResult",
    "IngestionJobResult",
    "KnowledgeBaseResult",
    "ListAgentActionGroupsResult",
    "ListAgentAliasesResult",
    "ListAgentCollaboratorsResult",
    "ListAgentKnowledgeBasesResult",
    "ListAgentVersionsResult",
    "ListFlowAliasesResult",
    "ListFlowVersionsResult",
    "ListFlowsResult",
    "ListIngestionJobsResult",
    "ListKnowledgeBaseDocumentsResult",
    "ListPromptsResult",
    "ListTagsForResourceResult",
    "PrepareFlowResult",
    "StopIngestionJobResult",
    "UpdateAgentActionGroupResult",
    "UpdateAgentAliasResult",
    "UpdateAgentCollaboratorResult",
    "UpdateAgentKnowledgeBaseResult",
    "UpdateDataSourceResult",
    "UpdateFlowAliasResult",
    "UpdateFlowResult",
    "UpdateKnowledgeBaseResult",
    "UpdatePromptResult",
    "ValidateFlowDefinitionResult",
    "associate_agent_collaborator",
    "associate_agent_knowledge_base",
    "create_agent",
    "create_agent_action_group",
    "create_agent_alias",
    "create_data_source",
    "create_flow",
    "create_flow_alias",
    "create_flow_version",
    "create_knowledge_base",
    "create_prompt",
    "create_prompt_version",
    "delete_agent",
    "delete_agent_action_group",
    "delete_agent_alias",
    "delete_agent_version",
    "delete_data_source",
    "delete_flow",
    "delete_flow_alias",
    "delete_flow_version",
    "delete_knowledge_base",
    "delete_knowledge_base_documents",
    "delete_prompt",
    "disassociate_agent_collaborator",
    "disassociate_agent_knowledge_base",
    "get_agent",
    "get_agent_action_group",
    "get_agent_alias",
    "get_agent_collaborator",
    "get_agent_knowledge_base",
    "get_agent_version",
    "get_data_source",
    "get_flow",
    "get_flow_alias",
    "get_flow_version",
    "get_ingestion_job",
    "get_knowledge_base",
    "get_knowledge_base_documents",
    "get_prompt",
    "ingest_knowledge_base_documents",
    "list_agent_action_groups",
    "list_agent_aliases",
    "list_agent_collaborators",
    "list_agent_knowledge_bases",
    "list_agent_versions",
    "list_agents",
    "list_data_sources",
    "list_flow_aliases",
    "list_flow_versions",
    "list_flows",
    "list_ingestion_jobs",
    "list_knowledge_base_documents",
    "list_knowledge_bases",
    "list_prompts",
    "list_tags_for_resource",
    "prepare_agent",
    "prepare_flow",
    "start_ingestion_job",
    "stop_ingestion_job",
    "tag_resource",
    "untag_resource",
    "update_agent",
    "update_agent_action_group",
    "update_agent_alias",
    "update_agent_collaborator",
    "update_agent_knowledge_base",
    "update_data_source",
    "update_flow",
    "update_flow_alias",
    "update_knowledge_base",
    "update_prompt",
    "validate_flow_definition",
    "wait_for_agent",
    "wait_for_ingestion_job",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AgentResult(BaseModel):
    """Metadata for a Bedrock Agent."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    agent_id: str
    agent_name: str
    agent_arn: str = ""
    agent_status: str = ""
    agent_version: str = ""
    description: str = ""
    foundation_model: str = ""
    instruction: str = ""
    idle_session_ttl_in_seconds: int = 0
    agent_resource_role_arn: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class KnowledgeBaseResult(BaseModel):
    """Metadata for a Bedrock Knowledge Base."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    knowledge_base_id: str
    name: str
    knowledge_base_arn: str = ""
    status: str = ""
    description: str = ""
    role_arn: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class DataSourceResult(BaseModel):
    """Metadata for a Bedrock data source."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    data_source_id: str
    knowledge_base_id: str
    name: str
    status: str = ""
    description: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class IngestionJobResult(BaseModel):
    """Metadata for a Bedrock ingestion job."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    ingestion_job_id: str
    knowledge_base_id: str
    data_source_id: str
    status: str = ""
    description: str = ""
    statistics: dict[str, Any] = Field(default_factory=dict)
    failure_reasons: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_AGENT_FIELDS = frozenset(
    {
        "agentId",
        "agentName",
        "agentArn",
        "agentStatus",
        "agentVersion",
        "description",
        "foundationModel",
        "instruction",
        "idleSessionTTLInSeconds",
        "agentResourceRoleArn",
    }
)


def _parse_agent(data: dict[str, Any]) -> AgentResult:
    """Build an :class:`AgentResult` from an AWS response dict."""
    return AgentResult(
        agent_id=data.get("agentId", ""),
        agent_name=data.get("agentName", ""),
        agent_arn=data.get("agentArn", ""),
        agent_status=data.get("agentStatus", ""),
        agent_version=data.get("agentVersion", ""),
        description=data.get("description", ""),
        foundation_model=data.get("foundationModel", ""),
        instruction=data.get("instruction", ""),
        idle_session_ttl_in_seconds=data.get("idleSessionTTLInSeconds", 0),
        agent_resource_role_arn=data.get("agentResourceRoleArn", ""),
        extra={k: v for k, v in data.items() if k not in _AGENT_FIELDS},
    )


_KB_FIELDS = frozenset(
    {
        "knowledgeBaseId",
        "name",
        "knowledgeBaseArn",
        "status",
        "description",
        "roleArn",
    }
)


def _parse_knowledge_base(data: dict[str, Any]) -> KnowledgeBaseResult:
    """Build a :class:`KnowledgeBaseResult` from an AWS response dict."""
    return KnowledgeBaseResult(
        knowledge_base_id=data.get("knowledgeBaseId", ""),
        name=data.get("name", ""),
        knowledge_base_arn=data.get("knowledgeBaseArn", ""),
        status=data.get("status", ""),
        description=data.get("description", ""),
        role_arn=data.get("roleArn", ""),
        extra={k: v for k, v in data.items() if k not in _KB_FIELDS},
    )


_DS_FIELDS = frozenset(
    {
        "dataSourceId",
        "knowledgeBaseId",
        "name",
        "status",
        "description",
    }
)


def _parse_data_source(data: dict[str, Any]) -> DataSourceResult:
    """Build a :class:`DataSourceResult` from an AWS response dict."""
    return DataSourceResult(
        data_source_id=data.get("dataSourceId", ""),
        knowledge_base_id=data.get("knowledgeBaseId", ""),
        name=data.get("name", ""),
        status=data.get("status", ""),
        description=data.get("description", ""),
        extra={k: v for k, v in data.items() if k not in _DS_FIELDS},
    )


_IJ_FIELDS = frozenset(
    {
        "ingestionJobId",
        "knowledgeBaseId",
        "dataSourceId",
        "status",
        "description",
        "statistics",
        "failureReasons",
    }
)


def _parse_ingestion_job(data: dict[str, Any]) -> IngestionJobResult:
    """Build an :class:`IngestionJobResult` from an AWS response dict."""
    return IngestionJobResult(
        ingestion_job_id=data.get("ingestionJobId", ""),
        knowledge_base_id=data.get("knowledgeBaseId", ""),
        data_source_id=data.get("dataSourceId", ""),
        status=data.get("status", ""),
        description=data.get("description", ""),
        statistics=data.get("statistics", {}),
        failure_reasons=data.get("failureReasons", []),
        extra={k: v for k, v in data.items() if k not in _IJ_FIELDS},
    )


# ---------------------------------------------------------------------------
# Agent CRUD
# ---------------------------------------------------------------------------


def create_agent(
    agent_name: str,
    *,
    agent_resource_role_arn: str,
    foundation_model: str | None = None,
    instruction: str | None = None,
    description: str | None = None,
    idle_session_ttl_in_seconds: int | None = None,
    region_name: str | None = None,
) -> AgentResult:
    """Create a new Bedrock Agent.

    Args:
        agent_name: Name for the agent.
        agent_resource_role_arn: IAM role ARN the agent will assume.
        foundation_model: Foundation model ID for the agent.
        instruction: Natural language instruction for the agent.
        description: Optional human-readable description.
        idle_session_ttl_in_seconds: Session TTL in seconds.
        region_name: AWS region override.

    Returns:
        An :class:`AgentResult` describing the created agent.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {
        "agentName": agent_name,
        "agentResourceRoleArn": agent_resource_role_arn,
    }
    if foundation_model is not None:
        kwargs["foundationModel"] = foundation_model
    if instruction is not None:
        kwargs["instruction"] = instruction
    if description is not None:
        kwargs["description"] = description
    if idle_session_ttl_in_seconds is not None:
        kwargs["idleSessionTTLInSeconds"] = idle_session_ttl_in_seconds
    try:
        resp = client.create_agent(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_agent failed for {agent_name!r}") from exc
    return _parse_agent(resp.get("agent", resp))


def get_agent(
    agent_id: str,
    *,
    region_name: str | None = None,
) -> AgentResult:
    """Retrieve details of a Bedrock Agent.

    Args:
        agent_id: The agent identifier.
        region_name: AWS region override.

    Returns:
        An :class:`AgentResult` with the agent configuration.

    Raises:
        RuntimeError: If the agent does not exist or the call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.get_agent(agentId=agent_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_agent failed for {agent_id!r}") from exc
    return _parse_agent(resp.get("agent", resp))


def list_agents(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[AgentResult]:
    """List Bedrock Agents in the account.

    Args:
        max_results: Maximum number of agents to return per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`AgentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    agents: list[AgentResult] = []
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        while True:
            resp = client.list_agents(**kwargs)
            for summary in resp.get("agentSummaries", []):
                agents.append(_parse_agent(summary))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_agents failed") from exc
    return agents


def delete_agent(
    agent_id: str,
    *,
    skip_resource_in_use_check: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete a Bedrock Agent.

    Args:
        agent_id: The agent identifier.
        skip_resource_in_use_check: If ``True``, delete even if the
            agent is in use.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        client.delete_agent(
            agentId=agent_id,
            skipResourceInUseCheck=skip_resource_in_use_check,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_agent failed for {agent_id!r}") from exc


def update_agent(
    agent_id: str,
    agent_name: str,
    *,
    agent_resource_role_arn: str,
    foundation_model: str | None = None,
    instruction: str | None = None,
    description: str | None = None,
    idle_session_ttl_in_seconds: int | None = None,
    region_name: str | None = None,
) -> AgentResult:
    """Update an existing Bedrock Agent.

    Args:
        agent_id: The agent identifier.
        agent_name: Updated agent name.
        agent_resource_role_arn: IAM role ARN the agent will assume.
        foundation_model: Foundation model ID for the agent.
        instruction: Natural language instruction for the agent.
        description: Optional human-readable description.
        idle_session_ttl_in_seconds: Session TTL in seconds.
        region_name: AWS region override.

    Returns:
        An :class:`AgentResult` with the updated agent configuration.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {
        "agentId": agent_id,
        "agentName": agent_name,
        "agentResourceRoleArn": agent_resource_role_arn,
    }
    if foundation_model is not None:
        kwargs["foundationModel"] = foundation_model
    if instruction is not None:
        kwargs["instruction"] = instruction
    if description is not None:
        kwargs["description"] = description
    if idle_session_ttl_in_seconds is not None:
        kwargs["idleSessionTTLInSeconds"] = idle_session_ttl_in_seconds
    try:
        resp = client.update_agent(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_agent failed for {agent_id!r}") from exc
    return _parse_agent(resp.get("agent", resp))


def prepare_agent(
    agent_id: str,
    *,
    region_name: str | None = None,
) -> AgentResult:
    """Prepare a Bedrock Agent for use.

    Args:
        agent_id: The agent identifier.
        region_name: AWS region override.

    Returns:
        An :class:`AgentResult` with the agent status after preparation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.prepare_agent(agentId=agent_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"prepare_agent failed for {agent_id!r}") from exc
    return _parse_agent(resp.get("agent", resp))


# ---------------------------------------------------------------------------
# Knowledge Base CRUD
# ---------------------------------------------------------------------------


def create_knowledge_base(
    name: str,
    *,
    role_arn: str,
    knowledge_base_configuration: dict[str, Any],
    storage_configuration: dict[str, Any],
    description: str | None = None,
    region_name: str | None = None,
) -> KnowledgeBaseResult:
    """Create a Bedrock Knowledge Base.

    Args:
        name: Knowledge base name.
        role_arn: IAM role ARN for the knowledge base.
        knowledge_base_configuration: Configuration for the knowledge
            base type (e.g. vector search settings).
        storage_configuration: Storage backend configuration
            (e.g. OpenSearch, Pinecone).
        description: Optional human-readable description.
        region_name: AWS region override.

    Returns:
        A :class:`KnowledgeBaseResult` describing the created knowledge base.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "roleArn": role_arn,
        "knowledgeBaseConfiguration": knowledge_base_configuration,
        "storageConfiguration": storage_configuration,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_knowledge_base(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_knowledge_base failed for {name!r}") from exc
    return _parse_knowledge_base(resp.get("knowledgeBase", resp))


def get_knowledge_base(
    knowledge_base_id: str,
    *,
    region_name: str | None = None,
) -> KnowledgeBaseResult:
    """Retrieve details of a Bedrock Knowledge Base.

    Args:
        knowledge_base_id: The knowledge base identifier.
        region_name: AWS region override.

    Returns:
        A :class:`KnowledgeBaseResult` with the knowledge base details.

    Raises:
        RuntimeError: If the knowledge base does not exist or the call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.get_knowledge_base(knowledgeBaseId=knowledge_base_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_knowledge_base failed for {knowledge_base_id!r}") from exc
    return _parse_knowledge_base(resp.get("knowledgeBase", resp))


def list_knowledge_bases(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[KnowledgeBaseResult]:
    """List Bedrock Knowledge Bases in the account.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`KnowledgeBaseResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kbs: list[KnowledgeBaseResult] = []
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        while True:
            resp = client.list_knowledge_bases(**kwargs)
            for summary in resp.get("knowledgeBaseSummaries", []):
                kbs.append(_parse_knowledge_base(summary))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_knowledge_bases failed") from exc
    return kbs


def delete_knowledge_base(
    knowledge_base_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Bedrock Knowledge Base.

    Args:
        knowledge_base_id: The knowledge base identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        client.delete_knowledge_base(knowledgeBaseId=knowledge_base_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"delete_knowledge_base failed for {knowledge_base_id!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Agent-Knowledge Base association
# ---------------------------------------------------------------------------


def associate_agent_knowledge_base(
    agent_id: str,
    agent_version: str,
    knowledge_base_id: str,
    *,
    description: str = "",
    knowledge_base_state: str = "ENABLED",
    region_name: str | None = None,
) -> dict[str, Any]:
    """Associate a Knowledge Base with a Bedrock Agent.

    Args:
        agent_id: The agent identifier.
        agent_version: The agent version (e.g. ``"DRAFT"``).
        knowledge_base_id: The knowledge base identifier.
        description: Description of how the agent should use the
            knowledge base.
        knowledge_base_state: State of the association
            (``"ENABLED"`` or ``"DISABLED"``).
        region_name: AWS region override.

    Returns:
        The raw AWS response dict for the association.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.associate_agent_knowledge_base(
            agentId=agent_id,
            agentVersion=agent_version,
            knowledgeBaseId=knowledge_base_id,
            description=description,
            knowledgeBaseState=knowledge_base_state,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"associate_agent_knowledge_base failed for "
            f"agent {agent_id!r} / kb {knowledge_base_id!r}",
        ) from exc
    return resp


# ---------------------------------------------------------------------------
# Data Source CRUD
# ---------------------------------------------------------------------------


def create_data_source(
    knowledge_base_id: str,
    name: str,
    *,
    data_source_configuration: dict[str, Any],
    description: str | None = None,
    region_name: str | None = None,
) -> DataSourceResult:
    """Create a data source for a Bedrock Knowledge Base.

    Args:
        knowledge_base_id: The knowledge base identifier.
        name: Data source name.
        data_source_configuration: Configuration specifying the data
            source type and location (e.g. S3 bucket).
        description: Optional human-readable description.
        region_name: AWS region override.

    Returns:
        A :class:`DataSourceResult` describing the created data source.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {
        "knowledgeBaseId": knowledge_base_id,
        "name": name,
        "dataSourceConfiguration": data_source_configuration,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_data_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_data_source failed for kb {knowledge_base_id!r}",
        ) from exc
    return _parse_data_source(resp.get("dataSource", resp))


def get_data_source(
    knowledge_base_id: str,
    data_source_id: str,
    *,
    region_name: str | None = None,
) -> DataSourceResult:
    """Retrieve details of a Bedrock data source.

    Args:
        knowledge_base_id: The knowledge base identifier.
        data_source_id: The data source identifier.
        region_name: AWS region override.

    Returns:
        A :class:`DataSourceResult` with the data source details.

    Raises:
        RuntimeError: If the data source does not exist or the call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.get_data_source(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_data_source failed for kb {knowledge_base_id!r} / ds {data_source_id!r}",
        ) from exc
    return _parse_data_source(resp.get("dataSource", resp))


def list_data_sources(
    knowledge_base_id: str,
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[DataSourceResult]:
    """List data sources for a Bedrock Knowledge Base.

    Args:
        knowledge_base_id: The knowledge base identifier.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`DataSourceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    sources: list[DataSourceResult] = []
    kwargs: dict[str, Any] = {"knowledgeBaseId": knowledge_base_id}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        while True:
            resp = client.list_data_sources(**kwargs)
            for summary in resp.get("dataSourceSummaries", []):
                sources.append(_parse_data_source(summary))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"list_data_sources failed for kb {knowledge_base_id!r}",
        ) from exc
    return sources


# ---------------------------------------------------------------------------
# Ingestion Jobs
# ---------------------------------------------------------------------------


def start_ingestion_job(
    knowledge_base_id: str,
    data_source_id: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> IngestionJobResult:
    """Start an ingestion job for a Bedrock data source.

    Args:
        knowledge_base_id: The knowledge base identifier.
        data_source_id: The data source identifier.
        description: Optional human-readable description.
        region_name: AWS region override.

    Returns:
        An :class:`IngestionJobResult` for the started job.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {
        "knowledgeBaseId": knowledge_base_id,
        "dataSourceId": data_source_id,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.start_ingestion_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"start_ingestion_job failed for kb {knowledge_base_id!r} / ds {data_source_id!r}",
        ) from exc
    return _parse_ingestion_job(resp.get("ingestionJob", resp))


def get_ingestion_job(
    knowledge_base_id: str,
    data_source_id: str,
    ingestion_job_id: str,
    *,
    region_name: str | None = None,
) -> IngestionJobResult:
    """Retrieve details of a Bedrock ingestion job.

    Args:
        knowledge_base_id: The knowledge base identifier.
        data_source_id: The data source identifier.
        ingestion_job_id: The ingestion job identifier.
        region_name: AWS region override.

    Returns:
        An :class:`IngestionJobResult` with the job details.

    Raises:
        RuntimeError: If the job does not exist or the call fails.
    """
    client = get_client("bedrock-agent", region_name)
    try:
        resp = client.get_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
            ingestionJobId=ingestion_job_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_ingestion_job failed for "
            f"kb {knowledge_base_id!r} / ds {data_source_id!r} "
            f"/ job {ingestion_job_id!r}",
        ) from exc
    return _parse_ingestion_job(resp.get("ingestionJob", resp))


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


def wait_for_agent(
    agent_id: str,
    *,
    target_statuses: tuple[str, ...] = ("PREPARED",),
    failure_statuses: tuple[str, ...] = ("FAILED",),
    timeout: float = 300,
    poll_interval: float = 5,
    region_name: str | None = None,
) -> AgentResult:
    """Poll until a Bedrock Agent reaches a target or failure status.

    Args:
        agent_id: The agent identifier.
        target_statuses: Statuses considered successful
            (default ``("PREPARED",)``).
        failure_statuses: Statuses considered failed (raises immediately,
            default ``("FAILED",)``).
        timeout: Maximum seconds to wait (default ``300``).
        poll_interval: Seconds between polls (default ``5``).
        region_name: AWS region override.

    Returns:
        An :class:`AgentResult` in one of the *target_statuses*.

    Raises:
        AwsTimeoutError: If the agent does not reach a target status
            within *timeout*.
        RuntimeError: If the agent enters a *failure_statuses* status
            or the describe call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        agent = get_agent(agent_id, region_name=region_name)
        if agent.agent_status in target_statuses:
            return agent
        if agent.agent_status in failure_statuses:
            raise RuntimeError(f"Agent {agent_id!r} entered failure status: {agent.agent_status}")
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Agent {agent_id!r} did not reach {target_statuses} "
                f"within {timeout}s (last status: {agent.agent_status})"
            )
        time.sleep(poll_interval)


def wait_for_ingestion_job(
    knowledge_base_id: str,
    data_source_id: str,
    ingestion_job_id: str,
    *,
    target_statuses: tuple[str, ...] = ("COMPLETE",),
    failure_statuses: tuple[str, ...] = ("FAILED",),
    timeout: float = 600,
    poll_interval: float = 10,
    region_name: str | None = None,
) -> IngestionJobResult:
    """Poll until an ingestion job reaches a target or failure status.

    Args:
        knowledge_base_id: The knowledge base identifier.
        data_source_id: The data source identifier.
        ingestion_job_id: The ingestion job identifier.
        target_statuses: Statuses considered successful
            (default ``("COMPLETE",)``).
        failure_statuses: Statuses considered failed (raises immediately,
            default ``("FAILED",)``).
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between polls (default ``10``).
        region_name: AWS region override.

    Returns:
        An :class:`IngestionJobResult` in one of the *target_statuses*.

    Raises:
        AwsTimeoutError: If the job does not reach a target status
            within *timeout*.
        RuntimeError: If the job enters a *failure_statuses* status
            or the describe call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        job = get_ingestion_job(
            knowledge_base_id,
            data_source_id,
            ingestion_job_id,
            region_name=region_name,
        )
        if job.status in target_statuses:
            return job
        if job.status in failure_statuses:
            raise RuntimeError(
                f"Ingestion job {ingestion_job_id!r} entered failure status: {job.status}"
            )
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Ingestion job {ingestion_job_id!r} did not reach "
                f"{target_statuses} within {timeout}s "
                f"(last status: {job.status})"
            )
        time.sleep(poll_interval)


class AssociateAgentCollaboratorResult(BaseModel):
    """Result of associate_agent_collaborator."""

    model_config = ConfigDict(frozen=True)

    agent_collaborator: dict[str, Any] | None = None


class CreateAgentActionGroupResult(BaseModel):
    """Result of create_agent_action_group."""

    model_config = ConfigDict(frozen=True)

    agent_action_group: dict[str, Any] | None = None


class CreateAgentAliasResult(BaseModel):
    """Result of create_agent_alias."""

    model_config = ConfigDict(frozen=True)

    agent_alias: dict[str, Any] | None = None


class CreateFlowResult(BaseModel):
    """Result of create_flow."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    execution_role_arn: str | None = None
    customer_encryption_key_arn: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    version: str | None = None
    definition: dict[str, Any] | None = None


class CreateFlowAliasResult(BaseModel):
    """Result of create_flow_alias."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    routing_configuration: list[dict[str, Any]] | None = None
    concurrency_configuration: dict[str, Any] | None = None
    flow_id: str | None = None
    id: str | None = None
    arn: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateFlowVersionResult(BaseModel):
    """Result of create_flow_version."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    execution_role_arn: str | None = None
    customer_encryption_key_arn: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_at: str | None = None
    version: str | None = None
    definition: dict[str, Any] | None = None


class CreatePromptResult(BaseModel):
    """Result of create_prompt."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    customer_encryption_key_arn: str | None = None
    default_variant: str | None = None
    variants: list[dict[str, Any]] | None = None
    id: str | None = None
    arn: str | None = None
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreatePromptVersionResult(BaseModel):
    """Result of create_prompt_version."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    customer_encryption_key_arn: str | None = None
    default_variant: str | None = None
    variants: list[dict[str, Any]] | None = None
    id: str | None = None
    arn: str | None = None
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class DeleteAgentAliasResult(BaseModel):
    """Result of delete_agent_alias."""

    model_config = ConfigDict(frozen=True)

    agent_id: str | None = None
    agent_alias_id: str | None = None
    agent_alias_status: str | None = None


class DeleteAgentVersionResult(BaseModel):
    """Result of delete_agent_version."""

    model_config = ConfigDict(frozen=True)

    agent_id: str | None = None
    agent_version: str | None = None
    agent_status: str | None = None


class DeleteDataSourceResult(BaseModel):
    """Result of delete_data_source."""

    model_config = ConfigDict(frozen=True)

    knowledge_base_id: str | None = None
    data_source_id: str | None = None
    status: str | None = None


class DeleteFlowResult(BaseModel):
    """Result of delete_flow."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None


class DeleteFlowAliasResult(BaseModel):
    """Result of delete_flow_alias."""

    model_config = ConfigDict(frozen=True)

    flow_id: str | None = None
    id: str | None = None


class DeleteFlowVersionResult(BaseModel):
    """Result of delete_flow_version."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    version: str | None = None


class DeleteKnowledgeBaseDocumentsResult(BaseModel):
    """Result of delete_knowledge_base_documents."""

    model_config = ConfigDict(frozen=True)

    document_details: list[dict[str, Any]] | None = None


class DeletePromptResult(BaseModel):
    """Result of delete_prompt."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    version: str | None = None


class GetAgentActionGroupResult(BaseModel):
    """Result of get_agent_action_group."""

    model_config = ConfigDict(frozen=True)

    agent_action_group: dict[str, Any] | None = None


class GetAgentAliasResult(BaseModel):
    """Result of get_agent_alias."""

    model_config = ConfigDict(frozen=True)

    agent_alias: dict[str, Any] | None = None


class GetAgentCollaboratorResult(BaseModel):
    """Result of get_agent_collaborator."""

    model_config = ConfigDict(frozen=True)

    agent_collaborator: dict[str, Any] | None = None


class GetAgentKnowledgeBaseResult(BaseModel):
    """Result of get_agent_knowledge_base."""

    model_config = ConfigDict(frozen=True)

    agent_knowledge_base: dict[str, Any] | None = None


class GetAgentVersionResult(BaseModel):
    """Result of get_agent_version."""

    model_config = ConfigDict(frozen=True)

    agent_version: dict[str, Any] | None = None


class GetFlowResult(BaseModel):
    """Result of get_flow."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    execution_role_arn: str | None = None
    customer_encryption_key_arn: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    version: str | None = None
    definition: dict[str, Any] | None = None
    validations: list[dict[str, Any]] | None = None


class GetFlowAliasResult(BaseModel):
    """Result of get_flow_alias."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    routing_configuration: list[dict[str, Any]] | None = None
    concurrency_configuration: dict[str, Any] | None = None
    flow_id: str | None = None
    id: str | None = None
    arn: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class GetFlowVersionResult(BaseModel):
    """Result of get_flow_version."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    execution_role_arn: str | None = None
    customer_encryption_key_arn: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_at: str | None = None
    version: str | None = None
    definition: dict[str, Any] | None = None


class GetKnowledgeBaseDocumentsResult(BaseModel):
    """Result of get_knowledge_base_documents."""

    model_config = ConfigDict(frozen=True)

    document_details: list[dict[str, Any]] | None = None


class GetPromptResult(BaseModel):
    """Result of get_prompt."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    customer_encryption_key_arn: str | None = None
    default_variant: str | None = None
    variants: list[dict[str, Any]] | None = None
    id: str | None = None
    arn: str | None = None
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class IngestKnowledgeBaseDocumentsResult(BaseModel):
    """Result of ingest_knowledge_base_documents."""

    model_config = ConfigDict(frozen=True)

    document_details: list[dict[str, Any]] | None = None


class ListAgentActionGroupsResult(BaseModel):
    """Result of list_agent_action_groups."""

    model_config = ConfigDict(frozen=True)

    action_group_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAgentAliasesResult(BaseModel):
    """Result of list_agent_aliases."""

    model_config = ConfigDict(frozen=True)

    agent_alias_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAgentCollaboratorsResult(BaseModel):
    """Result of list_agent_collaborators."""

    model_config = ConfigDict(frozen=True)

    agent_collaborator_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAgentKnowledgeBasesResult(BaseModel):
    """Result of list_agent_knowledge_bases."""

    model_config = ConfigDict(frozen=True)

    agent_knowledge_base_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAgentVersionsResult(BaseModel):
    """Result of list_agent_versions."""

    model_config = ConfigDict(frozen=True)

    agent_version_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlowAliasesResult(BaseModel):
    """Result of list_flow_aliases."""

    model_config = ConfigDict(frozen=True)

    flow_alias_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlowVersionsResult(BaseModel):
    """Result of list_flow_versions."""

    model_config = ConfigDict(frozen=True)

    flow_version_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlowsResult(BaseModel):
    """Result of list_flows."""

    model_config = ConfigDict(frozen=True)

    flow_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListIngestionJobsResult(BaseModel):
    """Result of list_ingestion_jobs."""

    model_config = ConfigDict(frozen=True)

    ingestion_job_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListKnowledgeBaseDocumentsResult(BaseModel):
    """Result of list_knowledge_base_documents."""

    model_config = ConfigDict(frozen=True)

    document_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPromptsResult(BaseModel):
    """Result of list_prompts."""

    model_config = ConfigDict(frozen=True)

    prompt_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class PrepareFlowResult(BaseModel):
    """Result of prepare_flow."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None


class StopIngestionJobResult(BaseModel):
    """Result of stop_ingestion_job."""

    model_config = ConfigDict(frozen=True)

    ingestion_job: dict[str, Any] | None = None


class UpdateAgentActionGroupResult(BaseModel):
    """Result of update_agent_action_group."""

    model_config = ConfigDict(frozen=True)

    agent_action_group: dict[str, Any] | None = None


class UpdateAgentAliasResult(BaseModel):
    """Result of update_agent_alias."""

    model_config = ConfigDict(frozen=True)

    agent_alias: dict[str, Any] | None = None


class UpdateAgentCollaboratorResult(BaseModel):
    """Result of update_agent_collaborator."""

    model_config = ConfigDict(frozen=True)

    agent_collaborator: dict[str, Any] | None = None


class UpdateAgentKnowledgeBaseResult(BaseModel):
    """Result of update_agent_knowledge_base."""

    model_config = ConfigDict(frozen=True)

    agent_knowledge_base: dict[str, Any] | None = None


class UpdateDataSourceResult(BaseModel):
    """Result of update_data_source."""

    model_config = ConfigDict(frozen=True)

    data_source: dict[str, Any] | None = None


class UpdateFlowResult(BaseModel):
    """Result of update_flow."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    execution_role_arn: str | None = None
    customer_encryption_key_arn: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    version: str | None = None
    definition: dict[str, Any] | None = None


class UpdateFlowAliasResult(BaseModel):
    """Result of update_flow_alias."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    routing_configuration: list[dict[str, Any]] | None = None
    concurrency_configuration: dict[str, Any] | None = None
    flow_id: str | None = None
    id: str | None = None
    arn: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class UpdateKnowledgeBaseResult(BaseModel):
    """Result of update_knowledge_base."""

    model_config = ConfigDict(frozen=True)

    knowledge_base: dict[str, Any] | None = None


class UpdatePromptResult(BaseModel):
    """Result of update_prompt."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    customer_encryption_key_arn: str | None = None
    default_variant: str | None = None
    variants: list[dict[str, Any]] | None = None
    id: str | None = None
    arn: str | None = None
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ValidateFlowDefinitionResult(BaseModel):
    """Result of validate_flow_definition."""

    model_config = ConfigDict(frozen=True)

    validations: list[dict[str, Any]] | None = None


def associate_agent_collaborator(
    agent_id: str,
    agent_version: str,
    agent_descriptor: dict[str, Any],
    collaborator_name: str,
    collaboration_instruction: str,
    *,
    relay_conversation_history: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> AssociateAgentCollaboratorResult:
    """Associate agent collaborator.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        agent_descriptor: Agent descriptor.
        collaborator_name: Collaborator name.
        collaboration_instruction: Collaboration instruction.
        relay_conversation_history: Relay conversation history.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["agentDescriptor"] = agent_descriptor
    kwargs["collaboratorName"] = collaborator_name
    kwargs["collaborationInstruction"] = collaboration_instruction
    if relay_conversation_history is not None:
        kwargs["relayConversationHistory"] = relay_conversation_history
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.associate_agent_collaborator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate agent collaborator") from exc
    return AssociateAgentCollaboratorResult(
        agent_collaborator=resp.get("agentCollaborator"),
    )


def create_agent_action_group(
    agent_id: str,
    agent_version: str,
    action_group_name: str,
    *,
    client_token: str | None = None,
    description: str | None = None,
    parent_action_group_signature: str | None = None,
    parent_action_group_signature_params: dict[str, Any] | None = None,
    action_group_executor: dict[str, Any] | None = None,
    api_schema: dict[str, Any] | None = None,
    action_group_state: str | None = None,
    function_schema: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAgentActionGroupResult:
    """Create agent action group.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        action_group_name: Action group name.
        client_token: Client token.
        description: Description.
        parent_action_group_signature: Parent action group signature.
        parent_action_group_signature_params: Parent action group signature params.
        action_group_executor: Action group executor.
        api_schema: Api schema.
        action_group_state: Action group state.
        function_schema: Function schema.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["actionGroupName"] = action_group_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if description is not None:
        kwargs["description"] = description
    if parent_action_group_signature is not None:
        kwargs["parentActionGroupSignature"] = parent_action_group_signature
    if parent_action_group_signature_params is not None:
        kwargs["parentActionGroupSignatureParams"] = parent_action_group_signature_params
    if action_group_executor is not None:
        kwargs["actionGroupExecutor"] = action_group_executor
    if api_schema is not None:
        kwargs["apiSchema"] = api_schema
    if action_group_state is not None:
        kwargs["actionGroupState"] = action_group_state
    if function_schema is not None:
        kwargs["functionSchema"] = function_schema
    try:
        resp = client.create_agent_action_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create agent action group") from exc
    return CreateAgentActionGroupResult(
        agent_action_group=resp.get("agentActionGroup"),
    )


def create_agent_alias(
    agent_id: str,
    agent_alias_name: str,
    *,
    client_token: str | None = None,
    description: str | None = None,
    routing_configuration: list[dict[str, Any]] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAgentAliasResult:
    """Create agent alias.

    Args:
        agent_id: Agent id.
        agent_alias_name: Agent alias name.
        client_token: Client token.
        description: Description.
        routing_configuration: Routing configuration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasName"] = agent_alias_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if description is not None:
        kwargs["description"] = description
    if routing_configuration is not None:
        kwargs["routingConfiguration"] = routing_configuration
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_agent_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create agent alias") from exc
    return CreateAgentAliasResult(
        agent_alias=resp.get("agentAlias"),
    )


def create_flow(
    name: str,
    execution_role_arn: str,
    *,
    description: str | None = None,
    customer_encryption_key_arn: str | None = None,
    definition: dict[str, Any] | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateFlowResult:
    """Create flow.

    Args:
        name: Name.
        execution_role_arn: Execution role arn.
        description: Description.
        customer_encryption_key_arn: Customer encryption key arn.
        definition: Definition.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["executionRoleArn"] = execution_role_arn
    if description is not None:
        kwargs["description"] = description
    if customer_encryption_key_arn is not None:
        kwargs["customerEncryptionKeyArn"] = customer_encryption_key_arn
    if definition is not None:
        kwargs["definition"] = definition
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create flow") from exc
    return CreateFlowResult(
        name=resp.get("name"),
        description=resp.get("description"),
        execution_role_arn=resp.get("executionRoleArn"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        version=resp.get("version"),
        definition=resp.get("definition"),
    )


def create_flow_alias(
    name: str,
    routing_configuration: list[dict[str, Any]],
    flow_identifier: str,
    *,
    description: str | None = None,
    concurrency_configuration: dict[str, Any] | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateFlowAliasResult:
    """Create flow alias.

    Args:
        name: Name.
        routing_configuration: Routing configuration.
        flow_identifier: Flow identifier.
        description: Description.
        concurrency_configuration: Concurrency configuration.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["routingConfiguration"] = routing_configuration
    kwargs["flowIdentifier"] = flow_identifier
    if description is not None:
        kwargs["description"] = description
    if concurrency_configuration is not None:
        kwargs["concurrencyConfiguration"] = concurrency_configuration
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_flow_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create flow alias") from exc
    return CreateFlowAliasResult(
        name=resp.get("name"),
        description=resp.get("description"),
        routing_configuration=resp.get("routingConfiguration"),
        concurrency_configuration=resp.get("concurrencyConfiguration"),
        flow_id=resp.get("flowId"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def create_flow_version(
    flow_identifier: str,
    *,
    description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateFlowVersionResult:
    """Create flow version.

    Args:
        flow_identifier: Flow identifier.
        description: Description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if description is not None:
        kwargs["description"] = description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.create_flow_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create flow version") from exc
    return CreateFlowVersionResult(
        name=resp.get("name"),
        description=resp.get("description"),
        execution_role_arn=resp.get("executionRoleArn"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_at=resp.get("createdAt"),
        version=resp.get("version"),
        definition=resp.get("definition"),
    )


def create_prompt(
    name: str,
    *,
    description: str | None = None,
    customer_encryption_key_arn: str | None = None,
    default_variant: str | None = None,
    variants: list[dict[str, Any]] | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePromptResult:
    """Create prompt.

    Args:
        name: Name.
        description: Description.
        customer_encryption_key_arn: Customer encryption key arn.
        default_variant: Default variant.
        variants: Variants.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if customer_encryption_key_arn is not None:
        kwargs["customerEncryptionKeyArn"] = customer_encryption_key_arn
    if default_variant is not None:
        kwargs["defaultVariant"] = default_variant
    if variants is not None:
        kwargs["variants"] = variants
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create prompt") from exc
    return CreatePromptResult(
        name=resp.get("name"),
        description=resp.get("description"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        default_variant=resp.get("defaultVariant"),
        variants=resp.get("variants"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        version=resp.get("version"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def create_prompt_version(
    prompt_identifier: str,
    *,
    description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePromptVersionResult:
    """Create prompt version.

    Args:
        prompt_identifier: Prompt identifier.
        description: Description.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptIdentifier"] = prompt_identifier
    if description is not None:
        kwargs["description"] = description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_prompt_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create prompt version") from exc
    return CreatePromptVersionResult(
        name=resp.get("name"),
        description=resp.get("description"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        default_variant=resp.get("defaultVariant"),
        variants=resp.get("variants"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        version=resp.get("version"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def delete_agent_action_group(
    agent_id: str,
    agent_version: str,
    action_group_id: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete agent action group.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        action_group_id: Action group id.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["actionGroupId"] = action_group_id
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        client.delete_agent_action_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete agent action group") from exc
    return None


def delete_agent_alias(
    agent_id: str,
    agent_alias_id: str,
    region_name: str | None = None,
) -> DeleteAgentAliasResult:
    """Delete agent alias.

    Args:
        agent_id: Agent id.
        agent_alias_id: Agent alias id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    try:
        resp = client.delete_agent_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete agent alias") from exc
    return DeleteAgentAliasResult(
        agent_id=resp.get("agentId"),
        agent_alias_id=resp.get("agentAliasId"),
        agent_alias_status=resp.get("agentAliasStatus"),
    )


def delete_agent_version(
    agent_id: str,
    agent_version: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> DeleteAgentVersionResult:
    """Delete agent version.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        resp = client.delete_agent_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete agent version") from exc
    return DeleteAgentVersionResult(
        agent_id=resp.get("agentId"),
        agent_version=resp.get("agentVersion"),
        agent_status=resp.get("agentStatus"),
    )


def delete_data_source(
    knowledge_base_id: str,
    data_source_id: str,
    region_name: str | None = None,
) -> DeleteDataSourceResult:
    """Delete data source.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    try:
        resp = client.delete_data_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete data source") from exc
    return DeleteDataSourceResult(
        knowledge_base_id=resp.get("knowledgeBaseId"),
        data_source_id=resp.get("dataSourceId"),
        status=resp.get("status"),
    )


def delete_flow(
    flow_identifier: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> DeleteFlowResult:
    """Delete flow.

    Args:
        flow_identifier: Flow identifier.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        resp = client.delete_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete flow") from exc
    return DeleteFlowResult(
        id=resp.get("id"),
    )


def delete_flow_alias(
    flow_identifier: str,
    alias_identifier: str,
    region_name: str | None = None,
) -> DeleteFlowAliasResult:
    """Delete flow alias.

    Args:
        flow_identifier: Flow identifier.
        alias_identifier: Alias identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["aliasIdentifier"] = alias_identifier
    try:
        resp = client.delete_flow_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete flow alias") from exc
    return DeleteFlowAliasResult(
        flow_id=resp.get("flowId"),
        id=resp.get("id"),
    )


def delete_flow_version(
    flow_identifier: str,
    flow_version: str,
    *,
    skip_resource_in_use_check: bool | None = None,
    region_name: str | None = None,
) -> DeleteFlowVersionResult:
    """Delete flow version.

    Args:
        flow_identifier: Flow identifier.
        flow_version: Flow version.
        skip_resource_in_use_check: Skip resource in use check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowVersion"] = flow_version
    if skip_resource_in_use_check is not None:
        kwargs["skipResourceInUseCheck"] = skip_resource_in_use_check
    try:
        resp = client.delete_flow_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete flow version") from exc
    return DeleteFlowVersionResult(
        id=resp.get("id"),
        version=resp.get("version"),
    )


def delete_knowledge_base_documents(
    knowledge_base_id: str,
    data_source_id: str,
    document_identifiers: list[dict[str, Any]],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> DeleteKnowledgeBaseDocumentsResult:
    """Delete knowledge base documents.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        document_identifiers: Document identifiers.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    kwargs["documentIdentifiers"] = document_identifiers
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.delete_knowledge_base_documents(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete knowledge base documents") from exc
    return DeleteKnowledgeBaseDocumentsResult(
        document_details=resp.get("documentDetails"),
    )


def delete_prompt(
    prompt_identifier: str,
    *,
    prompt_version: str | None = None,
    region_name: str | None = None,
) -> DeletePromptResult:
    """Delete prompt.

    Args:
        prompt_identifier: Prompt identifier.
        prompt_version: Prompt version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptIdentifier"] = prompt_identifier
    if prompt_version is not None:
        kwargs["promptVersion"] = prompt_version
    try:
        resp = client.delete_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete prompt") from exc
    return DeletePromptResult(
        id=resp.get("id"),
        version=resp.get("version"),
    )


def disassociate_agent_collaborator(
    agent_id: str,
    agent_version: str,
    collaborator_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate agent collaborator.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        collaborator_id: Collaborator id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["collaboratorId"] = collaborator_id
    try:
        client.disassociate_agent_collaborator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate agent collaborator") from exc
    return None


def disassociate_agent_knowledge_base(
    agent_id: str,
    agent_version: str,
    knowledge_base_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate agent knowledge base.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        knowledge_base_id: Knowledge base id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["knowledgeBaseId"] = knowledge_base_id
    try:
        client.disassociate_agent_knowledge_base(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate agent knowledge base") from exc
    return None


def get_agent_action_group(
    agent_id: str,
    agent_version: str,
    action_group_id: str,
    region_name: str | None = None,
) -> GetAgentActionGroupResult:
    """Get agent action group.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        action_group_id: Action group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["actionGroupId"] = action_group_id
    try:
        resp = client.get_agent_action_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent action group") from exc
    return GetAgentActionGroupResult(
        agent_action_group=resp.get("agentActionGroup"),
    )


def get_agent_alias(
    agent_id: str,
    agent_alias_id: str,
    region_name: str | None = None,
) -> GetAgentAliasResult:
    """Get agent alias.

    Args:
        agent_id: Agent id.
        agent_alias_id: Agent alias id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    try:
        resp = client.get_agent_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent alias") from exc
    return GetAgentAliasResult(
        agent_alias=resp.get("agentAlias"),
    )


def get_agent_collaborator(
    agent_id: str,
    agent_version: str,
    collaborator_id: str,
    region_name: str | None = None,
) -> GetAgentCollaboratorResult:
    """Get agent collaborator.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        collaborator_id: Collaborator id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["collaboratorId"] = collaborator_id
    try:
        resp = client.get_agent_collaborator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent collaborator") from exc
    return GetAgentCollaboratorResult(
        agent_collaborator=resp.get("agentCollaborator"),
    )


def get_agent_knowledge_base(
    agent_id: str,
    agent_version: str,
    knowledge_base_id: str,
    region_name: str | None = None,
) -> GetAgentKnowledgeBaseResult:
    """Get agent knowledge base.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        knowledge_base_id: Knowledge base id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["knowledgeBaseId"] = knowledge_base_id
    try:
        resp = client.get_agent_knowledge_base(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent knowledge base") from exc
    return GetAgentKnowledgeBaseResult(
        agent_knowledge_base=resp.get("agentKnowledgeBase"),
    )


def get_agent_version(
    agent_id: str,
    agent_version: str,
    region_name: str | None = None,
) -> GetAgentVersionResult:
    """Get agent version.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    try:
        resp = client.get_agent_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get agent version") from exc
    return GetAgentVersionResult(
        agent_version=resp.get("agentVersion"),
    )


def get_flow(
    flow_identifier: str,
    region_name: str | None = None,
) -> GetFlowResult:
    """Get flow.

    Args:
        flow_identifier: Flow identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    try:
        resp = client.get_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get flow") from exc
    return GetFlowResult(
        name=resp.get("name"),
        description=resp.get("description"),
        execution_role_arn=resp.get("executionRoleArn"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        version=resp.get("version"),
        definition=resp.get("definition"),
        validations=resp.get("validations"),
    )


def get_flow_alias(
    flow_identifier: str,
    alias_identifier: str,
    region_name: str | None = None,
) -> GetFlowAliasResult:
    """Get flow alias.

    Args:
        flow_identifier: Flow identifier.
        alias_identifier: Alias identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["aliasIdentifier"] = alias_identifier
    try:
        resp = client.get_flow_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get flow alias") from exc
    return GetFlowAliasResult(
        name=resp.get("name"),
        description=resp.get("description"),
        routing_configuration=resp.get("routingConfiguration"),
        concurrency_configuration=resp.get("concurrencyConfiguration"),
        flow_id=resp.get("flowId"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def get_flow_version(
    flow_identifier: str,
    flow_version: str,
    region_name: str | None = None,
) -> GetFlowVersionResult:
    """Get flow version.

    Args:
        flow_identifier: Flow identifier.
        flow_version: Flow version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["flowVersion"] = flow_version
    try:
        resp = client.get_flow_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get flow version") from exc
    return GetFlowVersionResult(
        name=resp.get("name"),
        description=resp.get("description"),
        execution_role_arn=resp.get("executionRoleArn"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_at=resp.get("createdAt"),
        version=resp.get("version"),
        definition=resp.get("definition"),
    )


def get_knowledge_base_documents(
    knowledge_base_id: str,
    data_source_id: str,
    document_identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> GetKnowledgeBaseDocumentsResult:
    """Get knowledge base documents.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        document_identifiers: Document identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    kwargs["documentIdentifiers"] = document_identifiers
    try:
        resp = client.get_knowledge_base_documents(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get knowledge base documents") from exc
    return GetKnowledgeBaseDocumentsResult(
        document_details=resp.get("documentDetails"),
    )


def get_prompt(
    prompt_identifier: str,
    *,
    prompt_version: str | None = None,
    region_name: str | None = None,
) -> GetPromptResult:
    """Get prompt.

    Args:
        prompt_identifier: Prompt identifier.
        prompt_version: Prompt version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["promptIdentifier"] = prompt_identifier
    if prompt_version is not None:
        kwargs["promptVersion"] = prompt_version
    try:
        resp = client.get_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get prompt") from exc
    return GetPromptResult(
        name=resp.get("name"),
        description=resp.get("description"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        default_variant=resp.get("defaultVariant"),
        variants=resp.get("variants"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        version=resp.get("version"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def ingest_knowledge_base_documents(
    knowledge_base_id: str,
    data_source_id: str,
    documents: list[dict[str, Any]],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> IngestKnowledgeBaseDocumentsResult:
    """Ingest knowledge base documents.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        documents: Documents.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    kwargs["documents"] = documents
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.ingest_knowledge_base_documents(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to ingest knowledge base documents") from exc
    return IngestKnowledgeBaseDocumentsResult(
        document_details=resp.get("documentDetails"),
    )


def list_agent_action_groups(
    agent_id: str,
    agent_version: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgentActionGroupsResult:
    """List agent action groups.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_agent_action_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent action groups") from exc
    return ListAgentActionGroupsResult(
        action_group_summaries=resp.get("actionGroupSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_agent_aliases(
    agent_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgentAliasesResult:
    """List agent aliases.

    Args:
        agent_id: Agent id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_agent_aliases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent aliases") from exc
    return ListAgentAliasesResult(
        agent_alias_summaries=resp.get("agentAliasSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_agent_collaborators(
    agent_id: str,
    agent_version: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgentCollaboratorsResult:
    """List agent collaborators.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_agent_collaborators(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent collaborators") from exc
    return ListAgentCollaboratorsResult(
        agent_collaborator_summaries=resp.get("agentCollaboratorSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_agent_knowledge_bases(
    agent_id: str,
    agent_version: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgentKnowledgeBasesResult:
    """List agent knowledge bases.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_agent_knowledge_bases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent knowledge bases") from exc
    return ListAgentKnowledgeBasesResult(
        agent_knowledge_base_summaries=resp.get("agentKnowledgeBaseSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_agent_versions(
    agent_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgentVersionsResult:
    """List agent versions.

    Args:
        agent_id: Agent id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_agent_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent versions") from exc
    return ListAgentVersionsResult(
        agent_version_summaries=resp.get("agentVersionSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_flow_aliases(
    flow_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFlowAliasesResult:
    """List flow aliases.

    Args:
        flow_identifier: Flow identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_flow_aliases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flow aliases") from exc
    return ListFlowAliasesResult(
        flow_alias_summaries=resp.get("flowAliasSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_flow_versions(
    flow_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFlowVersionsResult:
    """List flow versions.

    Args:
        flow_identifier: Flow identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_flow_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flow versions") from exc
    return ListFlowVersionsResult(
        flow_version_summaries=resp.get("flowVersionSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_flows(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFlowsResult:
    """List flows.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_flows(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flows") from exc
    return ListFlowsResult(
        flow_summaries=resp.get("flowSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_ingestion_jobs(
    knowledge_base_id: str,
    data_source_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    sort_by: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIngestionJobsResult:
    """List ingestion jobs.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        filters: Filters.
        sort_by: Sort by.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    if filters is not None:
        kwargs["filters"] = filters
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_ingestion_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list ingestion jobs") from exc
    return ListIngestionJobsResult(
        ingestion_job_summaries=resp.get("ingestionJobSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_knowledge_base_documents(
    knowledge_base_id: str,
    data_source_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListKnowledgeBaseDocumentsResult:
    """List knowledge base documents.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_knowledge_base_documents(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list knowledge base documents") from exc
    return ListKnowledgeBaseDocumentsResult(
        document_details=resp.get("documentDetails"),
        next_token=resp.get("nextToken"),
    )


def list_prompts(
    *,
    prompt_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPromptsResult:
    """List prompts.

    Args:
        prompt_identifier: Prompt identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    if prompt_identifier is not None:
        kwargs["promptIdentifier"] = prompt_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_prompts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list prompts") from exc
    return ListPromptsResult(
        prompt_summaries=resp.get("promptSummaries"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def prepare_flow(
    flow_identifier: str,
    region_name: str | None = None,
) -> PrepareFlowResult:
    """Prepare flow.

    Args:
        flow_identifier: Flow identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["flowIdentifier"] = flow_identifier
    try:
        resp = client.prepare_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to prepare flow") from exc
    return PrepareFlowResult(
        id=resp.get("id"),
        status=resp.get("status"),
    )


def stop_ingestion_job(
    knowledge_base_id: str,
    data_source_id: str,
    ingestion_job_id: str,
    region_name: str | None = None,
) -> StopIngestionJobResult:
    """Stop ingestion job.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        ingestion_job_id: Ingestion job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    kwargs["ingestionJobId"] = ingestion_job_id
    try:
        resp = client.stop_ingestion_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop ingestion job") from exc
    return StopIngestionJobResult(
        ingestion_job=resp.get("ingestionJob"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_agent_action_group(
    agent_id: str,
    agent_version: str,
    action_group_id: str,
    action_group_name: str,
    *,
    description: str | None = None,
    parent_action_group_signature: str | None = None,
    parent_action_group_signature_params: dict[str, Any] | None = None,
    action_group_executor: dict[str, Any] | None = None,
    action_group_state: str | None = None,
    api_schema: dict[str, Any] | None = None,
    function_schema: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateAgentActionGroupResult:
    """Update agent action group.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        action_group_id: Action group id.
        action_group_name: Action group name.
        description: Description.
        parent_action_group_signature: Parent action group signature.
        parent_action_group_signature_params: Parent action group signature params.
        action_group_executor: Action group executor.
        action_group_state: Action group state.
        api_schema: Api schema.
        function_schema: Function schema.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["actionGroupId"] = action_group_id
    kwargs["actionGroupName"] = action_group_name
    if description is not None:
        kwargs["description"] = description
    if parent_action_group_signature is not None:
        kwargs["parentActionGroupSignature"] = parent_action_group_signature
    if parent_action_group_signature_params is not None:
        kwargs["parentActionGroupSignatureParams"] = parent_action_group_signature_params
    if action_group_executor is not None:
        kwargs["actionGroupExecutor"] = action_group_executor
    if action_group_state is not None:
        kwargs["actionGroupState"] = action_group_state
    if api_schema is not None:
        kwargs["apiSchema"] = api_schema
    if function_schema is not None:
        kwargs["functionSchema"] = function_schema
    try:
        resp = client.update_agent_action_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agent action group") from exc
    return UpdateAgentActionGroupResult(
        agent_action_group=resp.get("agentActionGroup"),
    )


def update_agent_alias(
    agent_id: str,
    agent_alias_id: str,
    agent_alias_name: str,
    *,
    description: str | None = None,
    routing_configuration: list[dict[str, Any]] | None = None,
    alias_invocation_state: str | None = None,
    region_name: str | None = None,
) -> UpdateAgentAliasResult:
    """Update agent alias.

    Args:
        agent_id: Agent id.
        agent_alias_id: Agent alias id.
        agent_alias_name: Agent alias name.
        description: Description.
        routing_configuration: Routing configuration.
        alias_invocation_state: Alias invocation state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentAliasId"] = agent_alias_id
    kwargs["agentAliasName"] = agent_alias_name
    if description is not None:
        kwargs["description"] = description
    if routing_configuration is not None:
        kwargs["routingConfiguration"] = routing_configuration
    if alias_invocation_state is not None:
        kwargs["aliasInvocationState"] = alias_invocation_state
    try:
        resp = client.update_agent_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agent alias") from exc
    return UpdateAgentAliasResult(
        agent_alias=resp.get("agentAlias"),
    )


def update_agent_collaborator(
    agent_id: str,
    agent_version: str,
    collaborator_id: str,
    agent_descriptor: dict[str, Any],
    collaborator_name: str,
    collaboration_instruction: str,
    *,
    relay_conversation_history: str | None = None,
    region_name: str | None = None,
) -> UpdateAgentCollaboratorResult:
    """Update agent collaborator.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        collaborator_id: Collaborator id.
        agent_descriptor: Agent descriptor.
        collaborator_name: Collaborator name.
        collaboration_instruction: Collaboration instruction.
        relay_conversation_history: Relay conversation history.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["collaboratorId"] = collaborator_id
    kwargs["agentDescriptor"] = agent_descriptor
    kwargs["collaboratorName"] = collaborator_name
    kwargs["collaborationInstruction"] = collaboration_instruction
    if relay_conversation_history is not None:
        kwargs["relayConversationHistory"] = relay_conversation_history
    try:
        resp = client.update_agent_collaborator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agent collaborator") from exc
    return UpdateAgentCollaboratorResult(
        agent_collaborator=resp.get("agentCollaborator"),
    )


def update_agent_knowledge_base(
    agent_id: str,
    agent_version: str,
    knowledge_base_id: str,
    *,
    description: str | None = None,
    knowledge_base_state: str | None = None,
    region_name: str | None = None,
) -> UpdateAgentKnowledgeBaseResult:
    """Update agent knowledge base.

    Args:
        agent_id: Agent id.
        agent_version: Agent version.
        knowledge_base_id: Knowledge base id.
        description: Description.
        knowledge_base_state: Knowledge base state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["agentId"] = agent_id
    kwargs["agentVersion"] = agent_version
    kwargs["knowledgeBaseId"] = knowledge_base_id
    if description is not None:
        kwargs["description"] = description
    if knowledge_base_state is not None:
        kwargs["knowledgeBaseState"] = knowledge_base_state
    try:
        resp = client.update_agent_knowledge_base(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agent knowledge base") from exc
    return UpdateAgentKnowledgeBaseResult(
        agent_knowledge_base=resp.get("agentKnowledgeBase"),
    )


def update_data_source(
    knowledge_base_id: str,
    data_source_id: str,
    name: str,
    data_source_configuration: dict[str, Any],
    *,
    description: str | None = None,
    data_deletion_policy: str | None = None,
    server_side_encryption_configuration: dict[str, Any] | None = None,
    vector_ingestion_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDataSourceResult:
    """Update data source.

    Args:
        knowledge_base_id: Knowledge base id.
        data_source_id: Data source id.
        name: Name.
        data_source_configuration: Data source configuration.
        description: Description.
        data_deletion_policy: Data deletion policy.
        server_side_encryption_configuration: Server side encryption configuration.
        vector_ingestion_configuration: Vector ingestion configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["dataSourceId"] = data_source_id
    kwargs["name"] = name
    kwargs["dataSourceConfiguration"] = data_source_configuration
    if description is not None:
        kwargs["description"] = description
    if data_deletion_policy is not None:
        kwargs["dataDeletionPolicy"] = data_deletion_policy
    if server_side_encryption_configuration is not None:
        kwargs["serverSideEncryptionConfiguration"] = server_side_encryption_configuration
    if vector_ingestion_configuration is not None:
        kwargs["vectorIngestionConfiguration"] = vector_ingestion_configuration
    try:
        resp = client.update_data_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update data source") from exc
    return UpdateDataSourceResult(
        data_source=resp.get("dataSource"),
    )


def update_flow(
    name: str,
    execution_role_arn: str,
    flow_identifier: str,
    *,
    description: str | None = None,
    customer_encryption_key_arn: str | None = None,
    definition: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFlowResult:
    """Update flow.

    Args:
        name: Name.
        execution_role_arn: Execution role arn.
        flow_identifier: Flow identifier.
        description: Description.
        customer_encryption_key_arn: Customer encryption key arn.
        definition: Definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["executionRoleArn"] = execution_role_arn
    kwargs["flowIdentifier"] = flow_identifier
    if description is not None:
        kwargs["description"] = description
    if customer_encryption_key_arn is not None:
        kwargs["customerEncryptionKeyArn"] = customer_encryption_key_arn
    if definition is not None:
        kwargs["definition"] = definition
    try:
        resp = client.update_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update flow") from exc
    return UpdateFlowResult(
        name=resp.get("name"),
        description=resp.get("description"),
        execution_role_arn=resp.get("executionRoleArn"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        version=resp.get("version"),
        definition=resp.get("definition"),
    )


def update_flow_alias(
    name: str,
    routing_configuration: list[dict[str, Any]],
    flow_identifier: str,
    alias_identifier: str,
    *,
    description: str | None = None,
    concurrency_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFlowAliasResult:
    """Update flow alias.

    Args:
        name: Name.
        routing_configuration: Routing configuration.
        flow_identifier: Flow identifier.
        alias_identifier: Alias identifier.
        description: Description.
        concurrency_configuration: Concurrency configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["routingConfiguration"] = routing_configuration
    kwargs["flowIdentifier"] = flow_identifier
    kwargs["aliasIdentifier"] = alias_identifier
    if description is not None:
        kwargs["description"] = description
    if concurrency_configuration is not None:
        kwargs["concurrencyConfiguration"] = concurrency_configuration
    try:
        resp = client.update_flow_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update flow alias") from exc
    return UpdateFlowAliasResult(
        name=resp.get("name"),
        description=resp.get("description"),
        routing_configuration=resp.get("routingConfiguration"),
        concurrency_configuration=resp.get("concurrencyConfiguration"),
        flow_id=resp.get("flowId"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def update_knowledge_base(
    knowledge_base_id: str,
    name: str,
    role_arn: str,
    knowledge_base_configuration: dict[str, Any],
    *,
    description: str | None = None,
    storage_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateKnowledgeBaseResult:
    """Update knowledge base.

    Args:
        knowledge_base_id: Knowledge base id.
        name: Name.
        role_arn: Role arn.
        knowledge_base_configuration: Knowledge base configuration.
        description: Description.
        storage_configuration: Storage configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["knowledgeBaseId"] = knowledge_base_id
    kwargs["name"] = name
    kwargs["roleArn"] = role_arn
    kwargs["knowledgeBaseConfiguration"] = knowledge_base_configuration
    if description is not None:
        kwargs["description"] = description
    if storage_configuration is not None:
        kwargs["storageConfiguration"] = storage_configuration
    try:
        resp = client.update_knowledge_base(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update knowledge base") from exc
    return UpdateKnowledgeBaseResult(
        knowledge_base=resp.get("knowledgeBase"),
    )


def update_prompt(
    name: str,
    prompt_identifier: str,
    *,
    description: str | None = None,
    customer_encryption_key_arn: str | None = None,
    default_variant: str | None = None,
    variants: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdatePromptResult:
    """Update prompt.

    Args:
        name: Name.
        prompt_identifier: Prompt identifier.
        description: Description.
        customer_encryption_key_arn: Customer encryption key arn.
        default_variant: Default variant.
        variants: Variants.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["promptIdentifier"] = prompt_identifier
    if description is not None:
        kwargs["description"] = description
    if customer_encryption_key_arn is not None:
        kwargs["customerEncryptionKeyArn"] = customer_encryption_key_arn
    if default_variant is not None:
        kwargs["defaultVariant"] = default_variant
    if variants is not None:
        kwargs["variants"] = variants
    try:
        resp = client.update_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update prompt") from exc
    return UpdatePromptResult(
        name=resp.get("name"),
        description=resp.get("description"),
        customer_encryption_key_arn=resp.get("customerEncryptionKeyArn"),
        default_variant=resp.get("defaultVariant"),
        variants=resp.get("variants"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        version=resp.get("version"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
    )


def validate_flow_definition(
    definition: dict[str, Any],
    region_name: str | None = None,
) -> ValidateFlowDefinitionResult:
    """Validate flow definition.

    Args:
        definition: Definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("bedrock-agent", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["definition"] = definition
    try:
        resp = client.validate_flow_definition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to validate flow definition") from exc
    return ValidateFlowDefinitionResult(
        validations=resp.get("validations"),
    )
