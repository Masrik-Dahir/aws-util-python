"""aws_util.codestar_connections -- AWS CodeStar Connections utilities.

Provides helpers for managing CodeStar Connections, hosts, and tags.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ConnectionResult",
    "CreateRepositoryLinkResult",
    "CreateSyncConfigurationResult",
    "GetRepositoryLinkResult",
    "GetRepositorySyncStatusResult",
    "GetResourceSyncStatusResult",
    "GetSyncBlockerSummaryResult",
    "GetSyncConfigurationResult",
    "HostResult",
    "ListRepositoryLinksResult",
    "ListRepositorySyncDefinitionsResult",
    "ListSyncConfigurationsResult",
    "TagResult",
    "UpdateRepositoryLinkResult",
    "UpdateSyncBlockerResult",
    "UpdateSyncConfigurationResult",
    "create_connection",
    "create_host",
    "create_repository_link",
    "create_sync_configuration",
    "delete_connection",
    "delete_host",
    "delete_repository_link",
    "delete_sync_configuration",
    "get_connection",
    "get_host",
    "get_repository_link",
    "get_repository_sync_status",
    "get_resource_sync_status",
    "get_sync_blocker_summary",
    "get_sync_configuration",
    "list_connections",
    "list_hosts",
    "list_repository_links",
    "list_repository_sync_definitions",
    "list_sync_configurations",
    "list_tags_for_resource",
    "tag_resource",
    "untag_resource",
    "update_host",
    "update_repository_link",
    "update_sync_blocker",
    "update_sync_configuration",
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ConnectionResult(BaseModel):
    """A CodeStar connection."""

    model_config = ConfigDict(frozen=True)

    connection_name: str | None = None
    connection_arn: str
    provider_type: str | None = None
    owner_account_id: str | None = None
    connection_status: str | None = None
    host_arn: str | None = None
    extra: dict[str, Any] = {}


class HostResult(BaseModel):
    """A CodeStar host."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    host_arn: str
    provider_type: str | None = None
    provider_endpoint: str | None = None
    status: str | None = None
    vpc_configuration: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


class TagResult(BaseModel):
    """A resource tag."""

    model_config = ConfigDict(frozen=True)

    key: str
    value: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_connection(data: dict[str, Any]) -> ConnectionResult:
    """Convert a raw connection dict into a ``ConnectionResult``."""
    _known = {
        "ConnectionName",
        "ConnectionArn",
        "ProviderType",
        "OwnerAccountId",
        "ConnectionStatus",
        "HostArn",
    }
    return ConnectionResult(
        connection_name=data.get("ConnectionName"),
        connection_arn=data["ConnectionArn"],
        provider_type=data.get("ProviderType"),
        owner_account_id=data.get("OwnerAccountId"),
        connection_status=data.get("ConnectionStatus"),
        host_arn=data.get("HostArn"),
        extra={k: v for k, v in data.items() if k not in _known},
    )


def _parse_host(data: dict[str, Any]) -> HostResult:
    """Convert a raw host dict into a ``HostResult``."""
    _known = {
        "Name",
        "HostArn",
        "ProviderType",
        "ProviderEndpoint",
        "Status",
        "VpcConfiguration",
    }
    return HostResult(
        name=data.get("Name"),
        host_arn=data["HostArn"],
        provider_type=data.get("ProviderType"),
        provider_endpoint=data.get("ProviderEndpoint"),
        status=data.get("Status"),
        vpc_configuration=data.get("VpcConfiguration"),
        extra={k: v for k, v in data.items() if k not in _known},
    )


# ---------------------------------------------------------------------------
# Connection operations
# ---------------------------------------------------------------------------


def create_connection(
    connection_name: str,
    *,
    provider_type: str | None = None,
    tags: list[dict[str, str]] | None = None,
    host_arn: str | None = None,
    region_name: str | None = None,
) -> str:
    """Create a CodeStar connection.

    Args:
        connection_name: The connection name.
        provider_type: The provider type (e.g. ``"GitHub"``, ``"Bitbucket"``).
        tags: Optional list of tag dicts with ``Key`` and ``Value``.
        host_arn: Optional ARN of a host for installed providers.
        region_name: AWS region override.

    Returns:
        The ARN of the created connection.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {"ConnectionName": connection_name}
    if provider_type is not None:
        kwargs["ProviderType"] = provider_type
    if tags is not None:
        kwargs["Tags"] = tags
    if host_arn is not None:
        kwargs["HostArn"] = host_arn
    try:
        resp = client.create_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_connection failed for {connection_name!r}") from exc
    return resp["ConnectionArn"]


def get_connection(
    connection_arn: str,
    *,
    region_name: str | None = None,
) -> ConnectionResult:
    """Get details of a CodeStar connection.

    Args:
        connection_arn: The connection ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectionResult` for the connection.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        resp = client.get_connection(ConnectionArn=connection_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_connection failed for {connection_arn!r}") from exc
    return _parse_connection(resp["Connection"])


def list_connections(
    *,
    provider_type_filter: str | None = None,
    host_arn_filter: str | None = None,
    region_name: str | None = None,
) -> list[ConnectionResult]:
    """List CodeStar connections.

    Args:
        provider_type_filter: Optional provider type filter.
        host_arn_filter: Optional host ARN filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectionResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    connections: list[ConnectionResult] = []
    kwargs: dict[str, Any] = {}
    if provider_type_filter is not None:
        kwargs["ProviderTypeFilter"] = provider_type_filter
    if host_arn_filter is not None:
        kwargs["HostArnFilter"] = host_arn_filter
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_connections(**kwargs)
            for c in resp.get("Connections", []):
                connections.append(_parse_connection(c))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_connections failed") from exc
    return connections


def delete_connection(
    connection_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CodeStar connection.

    Args:
        connection_arn: The connection ARN to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        client.delete_connection(ConnectionArn=connection_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_connection failed for {connection_arn!r}") from exc


# ---------------------------------------------------------------------------
# Host operations
# ---------------------------------------------------------------------------


def create_host(
    name: str,
    provider_type: str,
    provider_endpoint: str,
    *,
    vpc_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a CodeStar host.

    Args:
        name: The host name.
        provider_type: The provider type (e.g. ``"GitHubEnterpriseServer"``).
        provider_endpoint: The URL endpoint for the provider.
        vpc_configuration: Optional VPC configuration dict.
        tags: Optional list of tag dicts.
        region_name: AWS region override.

    Returns:
        The ARN of the created host.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "ProviderType": provider_type,
        "ProviderEndpoint": provider_endpoint,
    }
    if vpc_configuration is not None:
        kwargs["VpcConfiguration"] = vpc_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_host(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_host failed for {name!r}") from exc
    return resp["HostArn"]


def get_host(
    host_arn: str,
    *,
    region_name: str | None = None,
) -> HostResult:
    """Get details of a CodeStar host.

    Args:
        host_arn: The host ARN.
        region_name: AWS region override.

    Returns:
        A :class:`HostResult` for the host.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        resp = client.get_host(HostArn=host_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_host failed for {host_arn!r}") from exc
    # get_host returns flat fields, not a nested dict
    return HostResult(
        name=resp.get("Name"),
        host_arn=host_arn,
        provider_type=resp.get("ProviderType"),
        provider_endpoint=resp.get("ProviderEndpoint"),
        status=resp.get("Status"),
        vpc_configuration=resp.get("VpcConfiguration"),
    )


def list_hosts(
    *,
    region_name: str | None = None,
) -> list[HostResult]:
    """List CodeStar hosts.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`HostResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    hosts: list[HostResult] = []
    kwargs: dict[str, Any] = {}
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_hosts(**kwargs)
            for h in resp.get("Hosts", []):
                hosts.append(_parse_host(h))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_hosts failed") from exc
    return hosts


def delete_host(
    host_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CodeStar host.

    Args:
        host_arn: The host ARN to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        client.delete_host(HostArn=host_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_host failed for {host_arn!r}") from exc


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, str]],
    *,
    region_name: str | None = None,
) -> None:
    """Tag a CodeStar Connections resource.

    Args:
        resource_arn: The ARN of the resource to tag.
        tags: A list of tag dicts with ``Key`` and ``Value``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        client.tag_resource(ResourceArn=resource_arn, Tags=tags)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"tag_resource failed for {resource_arn!r}") from exc


def list_tags_for_resource(
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> list[TagResult]:
    """List tags for a CodeStar Connections resource.

    Args:
        resource_arn: The ARN of the resource.
        region_name: AWS region override.

    Returns:
        A list of :class:`TagResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    try:
        resp = client.list_tags_for_resource(ResourceArn=resource_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_tags_for_resource failed for {resource_arn!r}") from exc
    return [TagResult(key=t["Key"], value=t["Value"]) for t in resp.get("Tags", [])]


class CreateRepositoryLinkResult(BaseModel):
    """Result of create_repository_link."""

    model_config = ConfigDict(frozen=True)

    repository_link_info: dict[str, Any] | None = None


class CreateSyncConfigurationResult(BaseModel):
    """Result of create_sync_configuration."""

    model_config = ConfigDict(frozen=True)

    sync_configuration: dict[str, Any] | None = None


class GetRepositoryLinkResult(BaseModel):
    """Result of get_repository_link."""

    model_config = ConfigDict(frozen=True)

    repository_link_info: dict[str, Any] | None = None


class GetRepositorySyncStatusResult(BaseModel):
    """Result of get_repository_sync_status."""

    model_config = ConfigDict(frozen=True)

    latest_sync: dict[str, Any] | None = None


class GetResourceSyncStatusResult(BaseModel):
    """Result of get_resource_sync_status."""

    model_config = ConfigDict(frozen=True)

    desired_state: dict[str, Any] | None = None
    latest_successful_sync: dict[str, Any] | None = None
    latest_sync: dict[str, Any] | None = None


class GetSyncBlockerSummaryResult(BaseModel):
    """Result of get_sync_blocker_summary."""

    model_config = ConfigDict(frozen=True)

    sync_blocker_summary: dict[str, Any] | None = None


class GetSyncConfigurationResult(BaseModel):
    """Result of get_sync_configuration."""

    model_config = ConfigDict(frozen=True)

    sync_configuration: dict[str, Any] | None = None


class ListRepositoryLinksResult(BaseModel):
    """Result of list_repository_links."""

    model_config = ConfigDict(frozen=True)

    repository_links: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRepositorySyncDefinitionsResult(BaseModel):
    """Result of list_repository_sync_definitions."""

    model_config = ConfigDict(frozen=True)

    repository_sync_definitions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSyncConfigurationsResult(BaseModel):
    """Result of list_sync_configurations."""

    model_config = ConfigDict(frozen=True)

    sync_configurations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class UpdateRepositoryLinkResult(BaseModel):
    """Result of update_repository_link."""

    model_config = ConfigDict(frozen=True)

    repository_link_info: dict[str, Any] | None = None


class UpdateSyncBlockerResult(BaseModel):
    """Result of update_sync_blocker."""

    model_config = ConfigDict(frozen=True)

    resource_name: str | None = None
    parent_resource_name: str | None = None
    sync_blocker: dict[str, Any] | None = None


class UpdateSyncConfigurationResult(BaseModel):
    """Result of update_sync_configuration."""

    model_config = ConfigDict(frozen=True)

    sync_configuration: dict[str, Any] | None = None


def create_repository_link(
    connection_arn: str,
    owner_id: str,
    repository_name: str,
    *,
    encryption_key_arn: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRepositoryLinkResult:
    """Create repository link.

    Args:
        connection_arn: Connection arn.
        owner_id: Owner id.
        repository_name: Repository name.
        encryption_key_arn: Encryption key arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionArn"] = connection_arn
    kwargs["OwnerId"] = owner_id
    kwargs["RepositoryName"] = repository_name
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_repository_link(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create repository link") from exc
    return CreateRepositoryLinkResult(
        repository_link_info=resp.get("RepositoryLinkInfo"),
    )


def create_sync_configuration(
    branch: str,
    config_file: str,
    repository_link_id: str,
    resource_name: str,
    role_arn: str,
    sync_type: str,
    *,
    publish_deployment_status: str | None = None,
    trigger_resource_update_on: str | None = None,
    region_name: str | None = None,
) -> CreateSyncConfigurationResult:
    """Create sync configuration.

    Args:
        branch: Branch.
        config_file: Config file.
        repository_link_id: Repository link id.
        resource_name: Resource name.
        role_arn: Role arn.
        sync_type: Sync type.
        publish_deployment_status: Publish deployment status.
        trigger_resource_update_on: Trigger resource update on.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Branch"] = branch
    kwargs["ConfigFile"] = config_file
    kwargs["RepositoryLinkId"] = repository_link_id
    kwargs["ResourceName"] = resource_name
    kwargs["RoleArn"] = role_arn
    kwargs["SyncType"] = sync_type
    if publish_deployment_status is not None:
        kwargs["PublishDeploymentStatus"] = publish_deployment_status
    if trigger_resource_update_on is not None:
        kwargs["TriggerResourceUpdateOn"] = trigger_resource_update_on
    try:
        resp = client.create_sync_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create sync configuration") from exc
    return CreateSyncConfigurationResult(
        sync_configuration=resp.get("SyncConfiguration"),
    )


def delete_repository_link(
    repository_link_id: str,
    region_name: str | None = None,
) -> None:
    """Delete repository link.

    Args:
        repository_link_id: Repository link id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RepositoryLinkId"] = repository_link_id
    try:
        client.delete_repository_link(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete repository link") from exc
    return None


def delete_sync_configuration(
    sync_type: str,
    resource_name: str,
    region_name: str | None = None,
) -> None:
    """Delete sync configuration.

    Args:
        sync_type: Sync type.
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncType"] = sync_type
    kwargs["ResourceName"] = resource_name
    try:
        client.delete_sync_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete sync configuration") from exc
    return None


def get_repository_link(
    repository_link_id: str,
    region_name: str | None = None,
) -> GetRepositoryLinkResult:
    """Get repository link.

    Args:
        repository_link_id: Repository link id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RepositoryLinkId"] = repository_link_id
    try:
        resp = client.get_repository_link(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get repository link") from exc
    return GetRepositoryLinkResult(
        repository_link_info=resp.get("RepositoryLinkInfo"),
    )


def get_repository_sync_status(
    branch: str,
    repository_link_id: str,
    sync_type: str,
    region_name: str | None = None,
) -> GetRepositorySyncStatusResult:
    """Get repository sync status.

    Args:
        branch: Branch.
        repository_link_id: Repository link id.
        sync_type: Sync type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Branch"] = branch
    kwargs["RepositoryLinkId"] = repository_link_id
    kwargs["SyncType"] = sync_type
    try:
        resp = client.get_repository_sync_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get repository sync status") from exc
    return GetRepositorySyncStatusResult(
        latest_sync=resp.get("LatestSync"),
    )


def get_resource_sync_status(
    resource_name: str,
    sync_type: str,
    region_name: str | None = None,
) -> GetResourceSyncStatusResult:
    """Get resource sync status.

    Args:
        resource_name: Resource name.
        sync_type: Sync type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["SyncType"] = sync_type
    try:
        resp = client.get_resource_sync_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource sync status") from exc
    return GetResourceSyncStatusResult(
        desired_state=resp.get("DesiredState"),
        latest_successful_sync=resp.get("LatestSuccessfulSync"),
        latest_sync=resp.get("LatestSync"),
    )


def get_sync_blocker_summary(
    sync_type: str,
    resource_name: str,
    region_name: str | None = None,
) -> GetSyncBlockerSummaryResult:
    """Get sync blocker summary.

    Args:
        sync_type: Sync type.
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncType"] = sync_type
    kwargs["ResourceName"] = resource_name
    try:
        resp = client.get_sync_blocker_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get sync blocker summary") from exc
    return GetSyncBlockerSummaryResult(
        sync_blocker_summary=resp.get("SyncBlockerSummary"),
    )


def get_sync_configuration(
    sync_type: str,
    resource_name: str,
    region_name: str | None = None,
) -> GetSyncConfigurationResult:
    """Get sync configuration.

    Args:
        sync_type: Sync type.
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncType"] = sync_type
    kwargs["ResourceName"] = resource_name
    try:
        resp = client.get_sync_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get sync configuration") from exc
    return GetSyncConfigurationResult(
        sync_configuration=resp.get("SyncConfiguration"),
    )


def list_repository_links(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRepositoryLinksResult:
    """List repository links.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_repository_links(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list repository links") from exc
    return ListRepositoryLinksResult(
        repository_links=resp.get("RepositoryLinks"),
        next_token=resp.get("NextToken"),
    )


def list_repository_sync_definitions(
    repository_link_id: str,
    sync_type: str,
    region_name: str | None = None,
) -> ListRepositorySyncDefinitionsResult:
    """List repository sync definitions.

    Args:
        repository_link_id: Repository link id.
        sync_type: Sync type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RepositoryLinkId"] = repository_link_id
    kwargs["SyncType"] = sync_type
    try:
        resp = client.list_repository_sync_definitions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list repository sync definitions") from exc
    return ListRepositorySyncDefinitionsResult(
        repository_sync_definitions=resp.get("RepositorySyncDefinitions"),
        next_token=resp.get("NextToken"),
    )


def list_sync_configurations(
    repository_link_id: str,
    sync_type: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSyncConfigurationsResult:
    """List sync configurations.

    Args:
        repository_link_id: Repository link id.
        sync_type: Sync type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RepositoryLinkId"] = repository_link_id
    kwargs["SyncType"] = sync_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_sync_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list sync configurations") from exc
    return ListSyncConfigurationsResult(
        sync_configurations=resp.get("SyncConfigurations"),
        next_token=resp.get("NextToken"),
    )


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
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_host(
    host_arn: str,
    *,
    provider_endpoint: str | None = None,
    vpc_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update host.

    Args:
        host_arn: Host arn.
        provider_endpoint: Provider endpoint.
        vpc_configuration: Vpc configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostArn"] = host_arn
    if provider_endpoint is not None:
        kwargs["ProviderEndpoint"] = provider_endpoint
    if vpc_configuration is not None:
        kwargs["VpcConfiguration"] = vpc_configuration
    try:
        client.update_host(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update host") from exc
    return None


def update_repository_link(
    repository_link_id: str,
    *,
    connection_arn: str | None = None,
    encryption_key_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateRepositoryLinkResult:
    """Update repository link.

    Args:
        repository_link_id: Repository link id.
        connection_arn: Connection arn.
        encryption_key_arn: Encryption key arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RepositoryLinkId"] = repository_link_id
    if connection_arn is not None:
        kwargs["ConnectionArn"] = connection_arn
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    try:
        resp = client.update_repository_link(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update repository link") from exc
    return UpdateRepositoryLinkResult(
        repository_link_info=resp.get("RepositoryLinkInfo"),
    )


def update_sync_blocker(
    id: str,
    sync_type: str,
    resource_name: str,
    resolved_reason: str,
    region_name: str | None = None,
) -> UpdateSyncBlockerResult:
    """Update sync blocker.

    Args:
        id: Id.
        sync_type: Sync type.
        resource_name: Resource name.
        resolved_reason: Resolved reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["SyncType"] = sync_type
    kwargs["ResourceName"] = resource_name
    kwargs["ResolvedReason"] = resolved_reason
    try:
        resp = client.update_sync_blocker(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update sync blocker") from exc
    return UpdateSyncBlockerResult(
        resource_name=resp.get("ResourceName"),
        parent_resource_name=resp.get("ParentResourceName"),
        sync_blocker=resp.get("SyncBlocker"),
    )


def update_sync_configuration(
    resource_name: str,
    sync_type: str,
    *,
    branch: str | None = None,
    config_file: str | None = None,
    repository_link_id: str | None = None,
    role_arn: str | None = None,
    publish_deployment_status: str | None = None,
    trigger_resource_update_on: str | None = None,
    region_name: str | None = None,
) -> UpdateSyncConfigurationResult:
    """Update sync configuration.

    Args:
        resource_name: Resource name.
        sync_type: Sync type.
        branch: Branch.
        config_file: Config file.
        repository_link_id: Repository link id.
        role_arn: Role arn.
        publish_deployment_status: Publish deployment status.
        trigger_resource_update_on: Trigger resource update on.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codestar-connections", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["SyncType"] = sync_type
    if branch is not None:
        kwargs["Branch"] = branch
    if config_file is not None:
        kwargs["ConfigFile"] = config_file
    if repository_link_id is not None:
        kwargs["RepositoryLinkId"] = repository_link_id
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    if publish_deployment_status is not None:
        kwargs["PublishDeploymentStatus"] = publish_deployment_status
    if trigger_resource_update_on is not None:
        kwargs["TriggerResourceUpdateOn"] = trigger_resource_update_on
    try:
        resp = client.update_sync_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update sync configuration") from exc
    return UpdateSyncConfigurationResult(
        sync_configuration=resp.get("SyncConfiguration"),
    )
