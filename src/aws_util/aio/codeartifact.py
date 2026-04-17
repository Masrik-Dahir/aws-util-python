"""Native async CodeArtifact utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.codeartifact import (
    AuthorizationTokenResult,
    CopyPackageVersionsResult,
    CreatePackageGroupResult,
    DeleteDomainPermissionsPolicyResult,
    DeletePackageGroupResult,
    DeletePackageResult,
    DeletePackageVersionsResult,
    DeleteRepositoryPermissionsPolicyResult,
    DescribePackageGroupResult,
    DisposePackageVersionsResult,
    DomainResult,
    EndpointResult,
    ExternalConnectionResult,
    GetAssociatedPackageGroupResult,
    GetDomainPermissionsPolicyResult,
    GetPackageVersionAssetResult,
    GetPackageVersionReadmeResult,
    GetRepositoryPermissionsPolicyResult,
    ListAllowedRepositoriesForGroupResult,
    ListAssociatedPackagesResult,
    ListPackageGroupsResult,
    ListPackageVersionAssetsResult,
    ListPackageVersionDependenciesResult,
    ListRepositoriesInDomainResult,
    ListSubPackageGroupsResult,
    ListTagsForResourceResult,
    PackageResult,
    PackageVersionResult,
    PublishPackageVersionResult,
    PutDomainPermissionsPolicyResult,
    PutPackageOriginConfigurationResult,
    PutRepositoryPermissionsPolicyResult,
    RepositoryResult,
    UpdatePackageGroupOriginConfigurationResult,
    UpdatePackageGroupResult,
    UpdatePackageVersionsStatusResult,
    UpdateRepositoryResult,
    _parse_domain,
    _parse_package,
    _parse_package_version,
    _parse_repository,
)
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AuthorizationTokenResult",
    "CopyPackageVersionsResult",
    "CreatePackageGroupResult",
    "DeleteDomainPermissionsPolicyResult",
    "DeletePackageGroupResult",
    "DeletePackageResult",
    "DeletePackageVersionsResult",
    "DeleteRepositoryPermissionsPolicyResult",
    "DescribePackageGroupResult",
    "DisposePackageVersionsResult",
    "DomainResult",
    "EndpointResult",
    "ExternalConnectionResult",
    "GetAssociatedPackageGroupResult",
    "GetDomainPermissionsPolicyResult",
    "GetPackageVersionAssetResult",
    "GetPackageVersionReadmeResult",
    "GetRepositoryPermissionsPolicyResult",
    "ListAllowedRepositoriesForGroupResult",
    "ListAssociatedPackagesResult",
    "ListPackageGroupsResult",
    "ListPackageVersionAssetsResult",
    "ListPackageVersionDependenciesResult",
    "ListRepositoriesInDomainResult",
    "ListSubPackageGroupsResult",
    "ListTagsForResourceResult",
    "PackageResult",
    "PackageVersionResult",
    "PublishPackageVersionResult",
    "PutDomainPermissionsPolicyResult",
    "PutPackageOriginConfigurationResult",
    "PutRepositoryPermissionsPolicyResult",
    "RepositoryResult",
    "UpdatePackageGroupOriginConfigurationResult",
    "UpdatePackageGroupResult",
    "UpdatePackageVersionsStatusResult",
    "UpdateRepositoryResult",
    "associate_external_connection",
    "copy_package_versions",
    "create_domain",
    "create_package_group",
    "create_repository",
    "delete_domain",
    "delete_domain_permissions_policy",
    "delete_package",
    "delete_package_group",
    "delete_package_versions",
    "delete_repository",
    "delete_repository_permissions_policy",
    "describe_domain",
    "describe_package",
    "describe_package_group",
    "describe_package_version",
    "describe_repository",
    "disassociate_external_connection",
    "dispose_package_versions",
    "get_associated_package_group",
    "get_authorization_token",
    "get_domain_permissions_policy",
    "get_package_version_asset",
    "get_package_version_readme",
    "get_repository_endpoint",
    "get_repository_permissions_policy",
    "list_allowed_repositories_for_group",
    "list_associated_packages",
    "list_domains",
    "list_package_groups",
    "list_package_version_assets",
    "list_package_version_dependencies",
    "list_package_versions",
    "list_packages",
    "list_repositories",
    "list_repositories_in_domain",
    "list_sub_package_groups",
    "list_tags_for_resource",
    "publish_package_version",
    "put_domain_permissions_policy",
    "put_package_origin_configuration",
    "put_repository_permissions_policy",
    "tag_resource",
    "untag_resource",
    "update_package_group",
    "update_package_group_origin_configuration",
    "update_package_versions_status",
    "update_repository",
]


# ---------------------------------------------------------------------------
# Domain operations
# ---------------------------------------------------------------------------


async def create_domain(
    domain: str,
    *,
    encryption_key: str | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> DomainResult:
    """Create a CodeArtifact domain.

    Args:
        domain: The domain name.
        encryption_key: Optional KMS key ARN for encryption.
        tags: Optional list of tag dicts with ``key`` and ``value``.
        region_name: AWS region override.

    Returns:
        A :class:`DomainResult` for the created domain.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain}
    if encryption_key is not None:
        kwargs["encryptionKey"] = encryption_key
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_domain failed for {domain!r}") from exc
    return _parse_domain(resp["domain"])


async def describe_domain(
    domain: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> DomainResult:
    """Describe a CodeArtifact domain.

    Args:
        domain: The domain name.
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        A :class:`DomainResult` for the domain.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DescribeDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_domain failed for {domain!r}") from exc
    return _parse_domain(resp["domain"])


async def list_domains(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[DomainResult]:
    """List CodeArtifact domains.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`DomainResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    domains: list[DomainResult] = []
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        while True:
            resp = await client.call("ListDomains", **kwargs)
            for d in resp.get("domains", []):
                domains.append(_parse_domain(d))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_domains failed") from exc
    return domains


async def delete_domain(
    domain: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> DomainResult:
    """Delete a CodeArtifact domain.

    Args:
        domain: The domain name.
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        A :class:`DomainResult` for the deleted domain.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DeleteDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_domain failed for {domain!r}") from exc
    return _parse_domain(resp["domain"])


# ---------------------------------------------------------------------------
# Repository operations
# ---------------------------------------------------------------------------


async def create_repository(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    description: str | None = None,
    upstreams: list[dict[str, str]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> RepositoryResult:
    """Create a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        domain_owner: Optional AWS account ID of the domain owner.
        description: Optional repository description.
        upstreams: Optional list of upstream repository dicts.
        tags: Optional list of tag dicts.
        region_name: AWS region override.

    Returns:
        A :class:`RepositoryResult` for the created repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain, "repository": repository}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if description is not None:
        kwargs["description"] = description
    if upstreams is not None:
        kwargs["upstreams"] = upstreams
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_repository failed for {repository!r}") from exc
    return _parse_repository(resp["repository"])


async def describe_repository(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> RepositoryResult:
    """Describe a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        A :class:`RepositoryResult` for the repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain, "repository": repository}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DescribeRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_repository failed for {repository!r}") from exc
    return _parse_repository(resp["repository"])


async def list_repositories(
    *,
    repository_prefix: str | None = None,
    region_name: str | None = None,
) -> list[RepositoryResult]:
    """List CodeArtifact repositories.

    Args:
        repository_prefix: Optional prefix filter for repository names.
        region_name: AWS region override.

    Returns:
        A list of :class:`RepositoryResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    repos: list[RepositoryResult] = []
    kwargs: dict[str, Any] = {}
    if repository_prefix is not None:
        kwargs["repositoryPrefix"] = repository_prefix
    try:
        while True:
            resp = await client.call("ListRepositories", **kwargs)
            for r in resp.get("repositories", []):
                repos.append(_parse_repository(r))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_repositories failed") from exc
    return repos


async def delete_repository(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> RepositoryResult:
    """Delete a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        A :class:`RepositoryResult` for the deleted repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain, "repository": repository}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DeleteRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_repository failed for {repository!r}") from exc
    return _parse_repository(resp["repository"])


# ---------------------------------------------------------------------------
# Package operations
# ---------------------------------------------------------------------------


async def list_packages(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    format: str | None = None,
    namespace: str | None = None,
    package_prefix: str | None = None,
    region_name: str | None = None,
) -> list[PackageResult]:
    """List packages in a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        domain_owner: Optional AWS account ID of the domain owner.
        format: Optional package format filter (e.g. ``"npm"``, ``"pypi"``).
        namespace: Optional namespace filter.
        package_prefix: Optional package name prefix filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`PackageResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    packages: list[PackageResult] = []
    kwargs: dict[str, Any] = {"domain": domain, "repository": repository}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if format is not None:
        kwargs["format"] = format
    if namespace is not None:
        kwargs["namespace"] = namespace
    if package_prefix is not None:
        kwargs["packagePrefix"] = package_prefix
    try:
        while True:
            resp = await client.call("ListPackages", **kwargs)
            for p in resp.get("packages", []):
                packages.append(_parse_package(p))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_packages failed") from exc
    return packages


async def describe_package(
    domain: str,
    repository: str,
    format: str,
    package: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> PackageResult:
    """Describe a package in a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        format: The package format (e.g. ``"npm"``, ``"pypi"``).
        package: The package name.
        domain_owner: Optional AWS account ID of the domain owner.
        namespace: Optional package namespace.
        region_name: AWS region override.

    Returns:
        A :class:`PackageResult` for the package.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "format": format,
        "package": package,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("DescribePackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_package failed for {package!r}") from exc
    return _parse_package(resp["package"])


async def list_package_versions(
    domain: str,
    repository: str,
    format: str,
    package: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    status: str | None = None,
    sort_by: str | None = None,
    region_name: str | None = None,
) -> list[PackageVersionResult]:
    """List versions of a package in a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        format: The package format (e.g. ``"npm"``, ``"pypi"``).
        package: The package name.
        domain_owner: Optional AWS account ID of the domain owner.
        namespace: Optional package namespace.
        status: Optional status filter (e.g. ``"Published"``).
        sort_by: Optional sort field (e.g. ``"PUBLISHED_TIME"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`PackageVersionResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    versions: list[PackageVersionResult] = []
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "format": format,
        "package": package,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if status is not None:
        kwargs["status"] = status
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    try:
        while True:
            resp = await client.call("ListPackageVersions", **kwargs)
            for v in resp.get("versions", []):
                versions.append(_parse_package_version({**v, "format": format, "package": package}))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_package_versions failed") from exc
    return versions


async def describe_package_version(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> PackageVersionResult:
    """Describe a specific package version.

    Args:
        domain: The domain name.
        repository: The repository name.
        format: The package format.
        package: The package name.
        package_version: The package version string.
        domain_owner: Optional AWS account ID of the domain owner.
        namespace: Optional package namespace.
        region_name: AWS region override.

    Returns:
        A :class:`PackageVersionResult` for the version.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "format": format,
        "package": package,
        "packageVersion": package_version,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("DescribePackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_package_version failed for {package!r}@{package_version!r}",
        ) from exc
    return _parse_package_version(resp["packageVersion"])


# ---------------------------------------------------------------------------
# Authorization & endpoint operations
# ---------------------------------------------------------------------------


async def get_authorization_token(
    domain: str,
    *,
    domain_owner: str | None = None,
    duration_seconds: int | None = None,
    region_name: str | None = None,
) -> AuthorizationTokenResult:
    """Get an authorization token for a CodeArtifact domain.

    Args:
        domain: The domain name.
        domain_owner: Optional AWS account ID of the domain owner.
        duration_seconds: Optional token validity duration in seconds.
        region_name: AWS region override.

    Returns:
        An :class:`AuthorizationTokenResult` with the token and expiration.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {"domain": domain}
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if duration_seconds is not None:
        kwargs["durationSeconds"] = duration_seconds
    try:
        resp = await client.call("GetAuthorizationToken", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_authorization_token failed for {domain!r}") from exc
    return AuthorizationTokenResult(
        authorization_token=resp["authorizationToken"],
        expiration=(str(resp["expiration"]) if resp.get("expiration") else None),
    )


async def get_repository_endpoint(
    domain: str,
    repository: str,
    format: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> EndpointResult:
    """Get the endpoint URL for a CodeArtifact repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        format: The package format (e.g. ``"npm"``, ``"pypi"``).
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        An :class:`EndpointResult` with the repository endpoint URL.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "format": format,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("GetRepositoryEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_repository_endpoint failed for {repository!r}") from exc
    return EndpointResult(repository_endpoint=resp["repositoryEndpoint"])


# ---------------------------------------------------------------------------
# External connection operations
# ---------------------------------------------------------------------------


async def associate_external_connection(
    domain: str,
    repository: str,
    external_connection: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> ExternalConnectionResult:
    """Associate an external connection with a repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        external_connection: The external connection name
            (e.g. ``"public:npmjs"``).
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        An :class:`ExternalConnectionResult` containing the updated
        repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "externalConnection": external_connection,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("AssociateExternalConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"associate_external_connection failed for {repository!r}"
        ) from exc
    return ExternalConnectionResult(
        repository=_parse_repository(resp["repository"]),
    )


async def disassociate_external_connection(
    domain: str,
    repository: str,
    external_connection: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> ExternalConnectionResult:
    """Disassociate an external connection from a repository.

    Args:
        domain: The domain name.
        repository: The repository name.
        external_connection: The external connection name.
        domain_owner: Optional AWS account ID of the domain owner.
        region_name: AWS region override.

    Returns:
        An :class:`ExternalConnectionResult` containing the updated
        repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {
        "domain": domain,
        "repository": repository,
        "externalConnection": external_connection,
    }
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DisassociateExternalConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"disassociate_external_connection failed for {repository!r}",
        ) from exc
    return ExternalConnectionResult(
        repository=_parse_repository(resp["repository"]),
    )


async def copy_package_versions(
    domain: str,
    source_repository: str,
    destination_repository: str,
    format: str,
    package: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    versions: list[str] | None = None,
    version_revisions: dict[str, Any] | None = None,
    allow_overwrite: bool | None = None,
    include_from_upstream: bool | None = None,
    region_name: str | None = None,
) -> CopyPackageVersionsResult:
    """Copy package versions.

    Args:
        domain: Domain.
        source_repository: Source repository.
        destination_repository: Destination repository.
        format: Format.
        package: Package.
        domain_owner: Domain owner.
        namespace: Namespace.
        versions: Versions.
        version_revisions: Version revisions.
        allow_overwrite: Allow overwrite.
        include_from_upstream: Include from upstream.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["sourceRepository"] = source_repository
    kwargs["destinationRepository"] = destination_repository
    kwargs["format"] = format
    kwargs["package"] = package
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if versions is not None:
        kwargs["versions"] = versions
    if version_revisions is not None:
        kwargs["versionRevisions"] = version_revisions
    if allow_overwrite is not None:
        kwargs["allowOverwrite"] = allow_overwrite
    if include_from_upstream is not None:
        kwargs["includeFromUpstream"] = include_from_upstream
    try:
        resp = await client.call("CopyPackageVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy package versions") from exc
    return CopyPackageVersionsResult(
        successful_versions=resp.get("successfulVersions"),
        failed_versions=resp.get("failedVersions"),
    )


async def create_package_group(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    contact_info: str | None = None,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreatePackageGroupResult:
    """Create package group.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        contact_info: Contact info.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if contact_info is not None:
        kwargs["contactInfo"] = contact_info
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreatePackageGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create package group") from exc
    return CreatePackageGroupResult(
        package_group=resp.get("packageGroup"),
    )


async def delete_domain_permissions_policy(
    domain: str,
    *,
    domain_owner: str | None = None,
    policy_revision: str | None = None,
    region_name: str | None = None,
) -> DeleteDomainPermissionsPolicyResult:
    """Delete domain permissions policy.

    Args:
        domain: Domain.
        domain_owner: Domain owner.
        policy_revision: Policy revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if policy_revision is not None:
        kwargs["policyRevision"] = policy_revision
    try:
        resp = await client.call("DeleteDomainPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain permissions policy") from exc
    return DeleteDomainPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def delete_package(
    domain: str,
    repository: str,
    format: str,
    package: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> DeletePackageResult:
    """Delete package.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        domain_owner: Domain owner.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("DeletePackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete package") from exc
    return DeletePackageResult(
        deleted_package=resp.get("deletedPackage"),
    )


async def delete_package_group(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> DeletePackageGroupResult:
    """Delete package group.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DeletePackageGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete package group") from exc
    return DeletePackageGroupResult(
        package_group=resp.get("packageGroup"),
    )


async def delete_package_versions(
    domain: str,
    repository: str,
    format: str,
    package: str,
    versions: list[str],
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    expected_status: str | None = None,
    region_name: str | None = None,
) -> DeletePackageVersionsResult:
    """Delete package versions.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        versions: Versions.
        domain_owner: Domain owner.
        namespace: Namespace.
        expected_status: Expected status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["versions"] = versions
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if expected_status is not None:
        kwargs["expectedStatus"] = expected_status
    try:
        resp = await client.call("DeletePackageVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete package versions") from exc
    return DeletePackageVersionsResult(
        successful_versions=resp.get("successfulVersions"),
        failed_versions=resp.get("failedVersions"),
    )


async def delete_repository_permissions_policy(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    policy_revision: str | None = None,
    region_name: str | None = None,
) -> DeleteRepositoryPermissionsPolicyResult:
    """Delete repository permissions policy.

    Args:
        domain: Domain.
        repository: Repository.
        domain_owner: Domain owner.
        policy_revision: Policy revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if policy_revision is not None:
        kwargs["policyRevision"] = policy_revision
    try:
        resp = await client.call("DeleteRepositoryPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete repository permissions policy") from exc
    return DeleteRepositoryPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def describe_package_group(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> DescribePackageGroupResult:
    """Describe package group.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("DescribePackageGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe package group") from exc
    return DescribePackageGroupResult(
        package_group=resp.get("packageGroup"),
    )


async def dispose_package_versions(
    domain: str,
    repository: str,
    format: str,
    package: str,
    versions: list[str],
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    version_revisions: dict[str, Any] | None = None,
    expected_status: str | None = None,
    region_name: str | None = None,
) -> DisposePackageVersionsResult:
    """Dispose package versions.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        versions: Versions.
        domain_owner: Domain owner.
        namespace: Namespace.
        version_revisions: Version revisions.
        expected_status: Expected status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["versions"] = versions
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if version_revisions is not None:
        kwargs["versionRevisions"] = version_revisions
    if expected_status is not None:
        kwargs["expectedStatus"] = expected_status
    try:
        resp = await client.call("DisposePackageVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to dispose package versions") from exc
    return DisposePackageVersionsResult(
        successful_versions=resp.get("successfulVersions"),
        failed_versions=resp.get("failedVersions"),
    )


async def get_associated_package_group(
    domain: str,
    format: str,
    package: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> GetAssociatedPackageGroupResult:
    """Get associated package group.

    Args:
        domain: Domain.
        format: Format.
        package: Package.
        domain_owner: Domain owner.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["format"] = format
    kwargs["package"] = package
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("GetAssociatedPackageGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get associated package group") from exc
    return GetAssociatedPackageGroupResult(
        package_group=resp.get("packageGroup"),
        association_type=resp.get("associationType"),
    )


async def get_domain_permissions_policy(
    domain: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> GetDomainPermissionsPolicyResult:
    """Get domain permissions policy.

    Args:
        domain: Domain.
        domain_owner: Domain owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("GetDomainPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain permissions policy") from exc
    return GetDomainPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def get_package_version_asset(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    asset: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    package_version_revision: str | None = None,
    region_name: str | None = None,
) -> GetPackageVersionAssetResult:
    """Get package version asset.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        package_version: Package version.
        asset: Asset.
        domain_owner: Domain owner.
        namespace: Namespace.
        package_version_revision: Package version revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["packageVersion"] = package_version
    kwargs["asset"] = asset
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if package_version_revision is not None:
        kwargs["packageVersionRevision"] = package_version_revision
    try:
        resp = await client.call("GetPackageVersionAsset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get package version asset") from exc
    return GetPackageVersionAssetResult(
        asset=resp.get("asset"),
        asset_name=resp.get("assetName"),
        package_version=resp.get("packageVersion"),
        package_version_revision=resp.get("packageVersionRevision"),
    )


async def get_package_version_readme(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> GetPackageVersionReadmeResult:
    """Get package version readme.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        package_version: Package version.
        domain_owner: Domain owner.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["packageVersion"] = package_version
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("GetPackageVersionReadme", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get package version readme") from exc
    return GetPackageVersionReadmeResult(
        format=resp.get("format"),
        namespace=resp.get("namespace"),
        package=resp.get("package"),
        version=resp.get("version"),
        version_revision=resp.get("versionRevision"),
        readme=resp.get("readme"),
    )


async def get_repository_permissions_policy(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    region_name: str | None = None,
) -> GetRepositoryPermissionsPolicyResult:
    """Get repository permissions policy.

    Args:
        domain: Domain.
        repository: Repository.
        domain_owner: Domain owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    try:
        resp = await client.call("GetRepositoryPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get repository permissions policy") from exc
    return GetRepositoryPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def list_allowed_repositories_for_group(
    domain: str,
    package_group: str,
    origin_restriction_type: str,
    *,
    domain_owner: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAllowedRepositoriesForGroupResult:
    """List allowed repositories for group.

    Args:
        domain: Domain.
        package_group: Package group.
        origin_restriction_type: Origin restriction type.
        domain_owner: Domain owner.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    kwargs["originRestrictionType"] = origin_restriction_type
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAllowedRepositoriesForGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list allowed repositories for group") from exc
    return ListAllowedRepositoriesForGroupResult(
        allowed_repositories=resp.get("allowedRepositories"),
        next_token=resp.get("nextToken"),
    )


async def list_associated_packages(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    preview: bool | None = None,
    region_name: str | None = None,
) -> ListAssociatedPackagesResult:
    """List associated packages.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        max_results: Max results.
        next_token: Next token.
        preview: Preview.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if preview is not None:
        kwargs["preview"] = preview
    try:
        resp = await client.call("ListAssociatedPackages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list associated packages") from exc
    return ListAssociatedPackagesResult(
        packages=resp.get("packages"),
        next_token=resp.get("nextToken"),
    )


async def list_package_groups(
    domain: str,
    *,
    domain_owner: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    prefix: str | None = None,
    region_name: str | None = None,
) -> ListPackageGroupsResult:
    """List package groups.

    Args:
        domain: Domain.
        domain_owner: Domain owner.
        max_results: Max results.
        next_token: Next token.
        prefix: Prefix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if prefix is not None:
        kwargs["prefix"] = prefix
    try:
        resp = await client.call("ListPackageGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list package groups") from exc
    return ListPackageGroupsResult(
        package_groups=resp.get("packageGroups"),
        next_token=resp.get("nextToken"),
    )


async def list_package_version_assets(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPackageVersionAssetsResult:
    """List package version assets.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        package_version: Package version.
        domain_owner: Domain owner.
        namespace: Namespace.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["packageVersion"] = package_version
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPackageVersionAssets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list package version assets") from exc
    return ListPackageVersionAssetsResult(
        format=resp.get("format"),
        namespace=resp.get("namespace"),
        package=resp.get("package"),
        version=resp.get("version"),
        version_revision=resp.get("versionRevision"),
        next_token=resp.get("nextToken"),
        assets=resp.get("assets"),
    )


async def list_package_version_dependencies(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPackageVersionDependenciesResult:
    """List package version dependencies.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        package_version: Package version.
        domain_owner: Domain owner.
        namespace: Namespace.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["packageVersion"] = package_version
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPackageVersionDependencies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list package version dependencies") from exc
    return ListPackageVersionDependenciesResult(
        format=resp.get("format"),
        namespace=resp.get("namespace"),
        package=resp.get("package"),
        version=resp.get("version"),
        version_revision=resp.get("versionRevision"),
        next_token=resp.get("nextToken"),
        dependencies=resp.get("dependencies"),
    )


async def list_repositories_in_domain(
    domain: str,
    *,
    domain_owner: str | None = None,
    administrator_account: str | None = None,
    repository_prefix: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRepositoriesInDomainResult:
    """List repositories in domain.

    Args:
        domain: Domain.
        domain_owner: Domain owner.
        administrator_account: Administrator account.
        repository_prefix: Repository prefix.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if administrator_account is not None:
        kwargs["administratorAccount"] = administrator_account
    if repository_prefix is not None:
        kwargs["repositoryPrefix"] = repository_prefix
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListRepositoriesInDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list repositories in domain") from exc
    return ListRepositoriesInDomainResult(
        repositories=resp.get("repositories"),
        next_token=resp.get("nextToken"),
    )


async def list_sub_package_groups(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSubPackageGroupsResult:
    """List sub package groups.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSubPackageGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sub package groups") from exc
    return ListSubPackageGroupsResult(
        package_groups=resp.get("packageGroups"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def publish_package_version(
    domain: str,
    repository: str,
    format: str,
    package: str,
    package_version: str,
    asset_content: bytes,
    asset_name: str,
    asset_sha256: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    unfinished: bool | None = None,
    region_name: str | None = None,
) -> PublishPackageVersionResult:
    """Publish package version.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        package_version: Package version.
        asset_content: Asset content.
        asset_name: Asset name.
        asset_sha256: Asset sha256.
        domain_owner: Domain owner.
        namespace: Namespace.
        unfinished: Unfinished.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["packageVersion"] = package_version
    kwargs["assetContent"] = asset_content
    kwargs["assetName"] = asset_name
    kwargs["assetSHA256"] = asset_sha256
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if unfinished is not None:
        kwargs["unfinished"] = unfinished
    try:
        resp = await client.call("PublishPackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to publish package version") from exc
    return PublishPackageVersionResult(
        format=resp.get("format"),
        namespace=resp.get("namespace"),
        package=resp.get("package"),
        version=resp.get("version"),
        version_revision=resp.get("versionRevision"),
        status=resp.get("status"),
        asset=resp.get("asset"),
    )


async def put_domain_permissions_policy(
    domain: str,
    policy_document: str,
    *,
    domain_owner: str | None = None,
    policy_revision: str | None = None,
    region_name: str | None = None,
) -> PutDomainPermissionsPolicyResult:
    """Put domain permissions policy.

    Args:
        domain: Domain.
        policy_document: Policy document.
        domain_owner: Domain owner.
        policy_revision: Policy revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["policyDocument"] = policy_document
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if policy_revision is not None:
        kwargs["policyRevision"] = policy_revision
    try:
        resp = await client.call("PutDomainPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put domain permissions policy") from exc
    return PutDomainPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def put_package_origin_configuration(
    domain: str,
    repository: str,
    format: str,
    package: str,
    restrictions: dict[str, Any],
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    region_name: str | None = None,
) -> PutPackageOriginConfigurationResult:
    """Put package origin configuration.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        restrictions: Restrictions.
        domain_owner: Domain owner.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["restrictions"] = restrictions
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    try:
        resp = await client.call("PutPackageOriginConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put package origin configuration") from exc
    return PutPackageOriginConfigurationResult(
        origin_configuration=resp.get("originConfiguration"),
    )


async def put_repository_permissions_policy(
    domain: str,
    repository: str,
    policy_document: str,
    *,
    domain_owner: str | None = None,
    policy_revision: str | None = None,
    region_name: str | None = None,
) -> PutRepositoryPermissionsPolicyResult:
    """Put repository permissions policy.

    Args:
        domain: Domain.
        repository: Repository.
        policy_document: Policy document.
        domain_owner: Domain owner.
        policy_revision: Policy revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["policyDocument"] = policy_document
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if policy_revision is not None:
        kwargs["policyRevision"] = policy_revision
    try:
        resp = await client.call("PutRepositoryPermissionsPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put repository permissions policy") from exc
    return PutRepositoryPermissionsPolicyResult(
        policy=resp.get("policy"),
    )


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
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
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_package_group(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    contact_info: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdatePackageGroupResult:
    """Update package group.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        contact_info: Contact info.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if contact_info is not None:
        kwargs["contactInfo"] = contact_info
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("UpdatePackageGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package group") from exc
    return UpdatePackageGroupResult(
        package_group=resp.get("packageGroup"),
    )


async def update_package_group_origin_configuration(
    domain: str,
    package_group: str,
    *,
    domain_owner: str | None = None,
    restrictions: dict[str, Any] | None = None,
    add_allowed_repositories: list[dict[str, Any]] | None = None,
    remove_allowed_repositories: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdatePackageGroupOriginConfigurationResult:
    """Update package group origin configuration.

    Args:
        domain: Domain.
        package_group: Package group.
        domain_owner: Domain owner.
        restrictions: Restrictions.
        add_allowed_repositories: Add allowed repositories.
        remove_allowed_repositories: Remove allowed repositories.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["packageGroup"] = package_group
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if restrictions is not None:
        kwargs["restrictions"] = restrictions
    if add_allowed_repositories is not None:
        kwargs["addAllowedRepositories"] = add_allowed_repositories
    if remove_allowed_repositories is not None:
        kwargs["removeAllowedRepositories"] = remove_allowed_repositories
    try:
        resp = await client.call("UpdatePackageGroupOriginConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package group origin configuration") from exc
    return UpdatePackageGroupOriginConfigurationResult(
        package_group=resp.get("packageGroup"),
        allowed_repository_updates=resp.get("allowedRepositoryUpdates"),
    )


async def update_package_versions_status(
    domain: str,
    repository: str,
    format: str,
    package: str,
    versions: list[str],
    target_status: str,
    *,
    domain_owner: str | None = None,
    namespace: str | None = None,
    version_revisions: dict[str, Any] | None = None,
    expected_status: str | None = None,
    region_name: str | None = None,
) -> UpdatePackageVersionsStatusResult:
    """Update package versions status.

    Args:
        domain: Domain.
        repository: Repository.
        format: Format.
        package: Package.
        versions: Versions.
        target_status: Target status.
        domain_owner: Domain owner.
        namespace: Namespace.
        version_revisions: Version revisions.
        expected_status: Expected status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    kwargs["format"] = format
    kwargs["package"] = package
    kwargs["versions"] = versions
    kwargs["targetStatus"] = target_status
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if namespace is not None:
        kwargs["namespace"] = namespace
    if version_revisions is not None:
        kwargs["versionRevisions"] = version_revisions
    if expected_status is not None:
        kwargs["expectedStatus"] = expected_status
    try:
        resp = await client.call("UpdatePackageVersionsStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package versions status") from exc
    return UpdatePackageVersionsStatusResult(
        successful_versions=resp.get("successfulVersions"),
        failed_versions=resp.get("failedVersions"),
    )


async def update_repository(
    domain: str,
    repository: str,
    *,
    domain_owner: str | None = None,
    description: str | None = None,
    upstreams: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateRepositoryResult:
    """Update repository.

    Args:
        domain: Domain.
        repository: Repository.
        domain_owner: Domain owner.
        description: Description.
        upstreams: Upstreams.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codeartifact", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domain"] = domain
    kwargs["repository"] = repository
    if domain_owner is not None:
        kwargs["domainOwner"] = domain_owner
    if description is not None:
        kwargs["description"] = description
    if upstreams is not None:
        kwargs["upstreams"] = upstreams
    try:
        resp = await client.call("UpdateRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update repository") from exc
    return UpdateRepositoryResult(
        repository=resp.get("repository"),
    )
