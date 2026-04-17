"""Tests for aws_util.aio.codeartifact -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codeartifact import (
    AuthorizationTokenResult,
    DomainResult,
    EndpointResult,
    ExternalConnectionResult,
    PackageResult,
    PackageVersionResult,
    RepositoryResult,
    associate_external_connection,
    create_domain,
    create_repository,
    delete_domain,
    delete_repository,
    describe_domain,
    describe_package,
    describe_package_version,
    describe_repository,
    disassociate_external_connection,
    get_authorization_token,
    get_repository_endpoint,
    list_domains,
    list_package_versions,
    list_packages,
    list_repositories,
    copy_package_versions,
    create_package_group,
    delete_domain_permissions_policy,
    delete_package,
    delete_package_group,
    delete_package_versions,
    delete_repository_permissions_policy,
    describe_package_group,
    dispose_package_versions,
    get_associated_package_group,
    get_domain_permissions_policy,
    get_package_version_asset,
    get_package_version_readme,
    get_repository_permissions_policy,
    list_allowed_repositories_for_group,
    list_associated_packages,
    list_package_groups,
    list_package_version_assets,
    list_package_version_dependencies,
    list_repositories_in_domain,
    list_sub_package_groups,
    list_tags_for_resource,
    publish_package_version,
    put_domain_permissions_policy,
    put_package_origin_configuration,
    put_repository_permissions_policy,
    tag_resource,
    untag_resource,
    update_package_group,
    update_package_group_origin_configuration,
    update_package_versions_status,
    update_repository,
)

DOMAIN = "test-domain"
REPO = "test-repo"
OWNER = "123456789012"
PKG = "my-package"


def _domain_dict(**kw):
    d = {"name": "d1", "arn": "arn:aws:codeartifact:us-east-1:123:domain/d1"}
    d.update(kw)
    return d


def _repo_dict(**kw):
    d = {"name": "r1", "arn": "arn:aws:codeartifact:us-east-1:123:repository/r1"}
    d.update(kw)
    return d


def _pkg_dict(**kw):
    d = {"format": "pypi", "package": "pkg1"}
    d.update(kw)
    return d


def _pkg_version_dict(**kw):
    d = {"format": "pypi", "package": "pkg1", "version": "1.0.0"}
    d.update(kw)
    return d


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# Domain operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_domain_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await create_domain(DOMAIN)
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_create_domain_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await create_domain(DOMAIN, encryption_key="k", tags=[{"key": "v"}])
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_create_domain_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_domain(DOMAIN)


@pytest.mark.asyncio
async def test_describe_domain_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_domain(DOMAIN)
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_describe_domain_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_domain(DOMAIN, domain_owner=OWNER)
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_describe_domain_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_domain(DOMAIN)


@pytest.mark.asyncio
async def test_list_domains_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domains": [_domain_dict()]}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_domains()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_domains_with_max(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domains": []}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_domains(max_results=10)
    assert r == []


@pytest.mark.asyncio
async def test_list_domains_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"domains": [_domain_dict()], "nextToken": "tok"},
        {"domains": [_domain_dict(name="d2", arn="arn:d2")]},
    ]
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_domains()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_domains_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_domains()


@pytest.mark.asyncio
async def test_delete_domain_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await delete_domain(DOMAIN)
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_delete_domain_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"domain": _domain_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await delete_domain(DOMAIN, domain_owner=OWNER)
    assert isinstance(r, DomainResult)


@pytest.mark.asyncio
async def test_delete_domain_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_domain(DOMAIN)


# ---------------------------------------------------------------------------
# Repository operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_repository_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await create_repository(DOMAIN, REPO)
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_create_repository_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await create_repository(
        DOMAIN, REPO,
        domain_owner=OWNER, description="d",
        upstreams=[{"repositoryName": "u"}],
        tags=[{"key": "v"}],
    )
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_create_repository_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_repository(DOMAIN, REPO)


@pytest.mark.asyncio
async def test_describe_repository_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_repository(DOMAIN, REPO)
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_describe_repository_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_repository(DOMAIN, REPO, domain_owner=OWNER)
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_describe_repository_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_repository(DOMAIN, REPO)


@pytest.mark.asyncio
async def test_list_repositories_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repositories": [_repo_dict()]}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_repositories()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_repositories_with_prefix(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repositories": []}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_repositories(repository_prefix="pre")
    assert r == []


@pytest.mark.asyncio
async def test_list_repositories_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"repositories": [_repo_dict()], "nextToken": "tok"},
        {"repositories": [_repo_dict(name="r2", arn="arn:r2")]},
    ]
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_repositories()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_repositories_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_repositories()


@pytest.mark.asyncio
async def test_delete_repository_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await delete_repository(DOMAIN, REPO)
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_delete_repository_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await delete_repository(DOMAIN, REPO, domain_owner=OWNER)
    assert isinstance(r, RepositoryResult)


@pytest.mark.asyncio
async def test_delete_repository_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_repository(DOMAIN, REPO)


# ---------------------------------------------------------------------------
# Package operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_packages_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"packages": [_pkg_dict()]}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_packages(DOMAIN, REPO)
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_packages_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"packages": []}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_packages(
        DOMAIN, REPO,
        domain_owner=OWNER, format="npm",
        namespace="ns", package_prefix="pre",
    )
    assert r == []


@pytest.mark.asyncio
async def test_list_packages_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"packages": [_pkg_dict()], "nextToken": "tok"},
        {"packages": [_pkg_dict(package="pkg2")]},
    ]
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_packages(DOMAIN, REPO)
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_packages_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_packages(DOMAIN, REPO)


@pytest.mark.asyncio
async def test_describe_package_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"package": _pkg_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_package(DOMAIN, REPO, "pypi", PKG)
    assert isinstance(r, PackageResult)


@pytest.mark.asyncio
async def test_describe_package_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"package": _pkg_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_package(
        DOMAIN, REPO, "pypi", PKG,
        domain_owner=OWNER, namespace="ns",
    )
    assert isinstance(r, PackageResult)


@pytest.mark.asyncio
async def test_describe_package_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_package(DOMAIN, REPO, "pypi", PKG)


@pytest.mark.asyncio
async def test_list_package_versions_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "versions": [{"version": "1.0", "status": "Published"}],
    }
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_package_versions(DOMAIN, REPO, "pypi", PKG)
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_package_versions_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"versions": []}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_package_versions(
        DOMAIN, REPO, "pypi", PKG,
        domain_owner=OWNER, namespace="ns",
        status="Published", sort_by="PUBLISHED_TIME",
    )
    assert r == []


@pytest.mark.asyncio
async def test_list_package_versions_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"versions": [{"version": "1.0"}], "nextToken": "tok"},
        {"versions": [{"version": "2.0"}]},
    ]
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await list_package_versions(DOMAIN, REPO, "pypi", PKG)
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_package_versions_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_package_versions(DOMAIN, REPO, "pypi", PKG)


@pytest.mark.asyncio
async def test_describe_package_version_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"packageVersion": _pkg_version_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_package_version(DOMAIN, REPO, "pypi", PKG, "1.0.0")
    assert isinstance(r, PackageVersionResult)


@pytest.mark.asyncio
async def test_describe_package_version_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"packageVersion": _pkg_version_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await describe_package_version(
        DOMAIN, REPO, "pypi", PKG, "1.0.0",
        domain_owner=OWNER, namespace="ns",
    )
    assert isinstance(r, PackageVersionResult)


@pytest.mark.asyncio
async def test_describe_package_version_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_package_version(DOMAIN, REPO, "pypi", PKG, "1.0.0")


# ---------------------------------------------------------------------------
# Authorization & endpoint
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_authorization_token_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "authorizationToken": "tok123",
        "expiration": "2025-01-01",
    }
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await get_authorization_token(DOMAIN)
    assert r.authorization_token == "tok123"
    assert r.expiration == "2025-01-01"


@pytest.mark.asyncio
async def test_get_authorization_token_no_expiration(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"authorizationToken": "tok123"}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await get_authorization_token(DOMAIN)
    assert r.expiration is None


@pytest.mark.asyncio
async def test_get_authorization_token_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"authorizationToken": "tok"}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await get_authorization_token(
        DOMAIN, domain_owner=OWNER, duration_seconds=3600,
    )
    assert isinstance(r, AuthorizationTokenResult)


@pytest.mark.asyncio
async def test_get_authorization_token_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_authorization_token(DOMAIN)


@pytest.mark.asyncio
async def test_get_repository_endpoint_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repositoryEndpoint": "https://ep.example.com"}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await get_repository_endpoint(DOMAIN, REPO, "pypi")
    assert r.repository_endpoint == "https://ep.example.com"


@pytest.mark.asyncio
async def test_get_repository_endpoint_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repositoryEndpoint": "https://ep"}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await get_repository_endpoint(DOMAIN, REPO, "pypi", domain_owner=OWNER)
    assert isinstance(r, EndpointResult)


@pytest.mark.asyncio
async def test_get_repository_endpoint_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_repository_endpoint(DOMAIN, REPO, "pypi")


# ---------------------------------------------------------------------------
# External connections
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_associate_external_connection_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await associate_external_connection(DOMAIN, REPO, "public:npmjs")
    assert isinstance(r, ExternalConnectionResult)


@pytest.mark.asyncio
async def test_associate_external_connection_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await associate_external_connection(
        DOMAIN, REPO, "public:npmjs", domain_owner=OWNER,
    )
    assert isinstance(r, ExternalConnectionResult)


@pytest.mark.asyncio
async def test_associate_external_connection_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await associate_external_connection(DOMAIN, REPO, "public:npmjs")


@pytest.mark.asyncio
async def test_disassociate_external_connection_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await disassociate_external_connection(DOMAIN, REPO, "public:npmjs")
    assert isinstance(r, ExternalConnectionResult)


@pytest.mark.asyncio
async def test_disassociate_external_connection_with_owner(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"repository": _repo_dict()}
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    r = await disassociate_external_connection(
        DOMAIN, REPO, "public:npmjs", domain_owner=OWNER,
    )
    assert isinstance(r, ExternalConnectionResult)


@pytest.mark.asyncio
async def test_disassociate_external_connection_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await disassociate_external_connection(DOMAIN, REPO, "public:npmjs")


async def test_copy_package_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", )
    mock_client.call.assert_called_once()


async def test_copy_package_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", )


async def test_create_package_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_package_group("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_create_package_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_package_group("test-domain", "test-package_group", )


async def test_delete_domain_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_domain_permissions_policy("test-domain", )
    mock_client.call.assert_called_once()


async def test_delete_domain_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_domain_permissions_policy("test-domain", )


async def test_delete_package(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_package("test-domain", "test-repository", "test-format", "test-package", )
    mock_client.call.assert_called_once()


async def test_delete_package_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_package("test-domain", "test-repository", "test-format", "test-package", )


async def test_delete_package_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_package_group("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_delete_package_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_package_group("test-domain", "test-package_group", )


async def test_delete_package_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_package_versions("test-domain", "test-repository", "test-format", "test-package", [], )
    mock_client.call.assert_called_once()


async def test_delete_package_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_package_versions("test-domain", "test-repository", "test-format", "test-package", [], )


async def test_delete_repository_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_repository_permissions_policy("test-domain", "test-repository", )
    mock_client.call.assert_called_once()


async def test_delete_repository_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository_permissions_policy("test-domain", "test-repository", )


async def test_describe_package_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_package_group("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_describe_package_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_package_group("test-domain", "test-package_group", )


async def test_dispose_package_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", [], )
    mock_client.call.assert_called_once()


async def test_dispose_package_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", [], )


async def test_get_associated_package_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_associated_package_group("test-domain", "test-format", "test-package", )
    mock_client.call.assert_called_once()


async def test_get_associated_package_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_associated_package_group("test-domain", "test-format", "test-package", )


async def test_get_domain_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_domain_permissions_policy("test-domain", )
    mock_client.call.assert_called_once()


async def test_get_domain_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_domain_permissions_policy("test-domain", )


async def test_get_package_version_asset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", )
    mock_client.call.assert_called_once()


async def test_get_package_version_asset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", )


async def test_get_package_version_readme(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )
    mock_client.call.assert_called_once()


async def test_get_package_version_readme_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )


async def test_get_repository_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_repository_permissions_policy("test-domain", "test-repository", )
    mock_client.call.assert_called_once()


async def test_get_repository_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository_permissions_policy("test-domain", "test-repository", )


async def test_list_allowed_repositories_for_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", )
    mock_client.call.assert_called_once()


async def test_list_allowed_repositories_for_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", )


async def test_list_associated_packages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associated_packages("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_list_associated_packages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associated_packages("test-domain", "test-package_group", )


async def test_list_package_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_package_groups("test-domain", )
    mock_client.call.assert_called_once()


async def test_list_package_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_package_groups("test-domain", )


async def test_list_package_version_assets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )
    mock_client.call.assert_called_once()


async def test_list_package_version_assets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )


async def test_list_package_version_dependencies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )
    mock_client.call.assert_called_once()


async def test_list_package_version_dependencies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", )


async def test_list_repositories_in_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_repositories_in_domain("test-domain", )
    mock_client.call.assert_called_once()


async def test_list_repositories_in_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_repositories_in_domain("test-domain", )


async def test_list_sub_package_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sub_package_groups("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_list_sub_package_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sub_package_groups("test-domain", "test-package_group", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_publish_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", )
    mock_client.call.assert_called_once()


async def test_publish_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", )


async def test_put_domain_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_domain_permissions_policy("test-domain", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_domain_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_domain_permissions_policy("test-domain", "test-policy_document", )


async def test_put_package_origin_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", {}, )
    mock_client.call.assert_called_once()


async def test_put_package_origin_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", {}, )


async def test_put_repository_permissions_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_repository_permissions_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_package_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package_group("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_update_package_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package_group("test-domain", "test-package_group", )


async def test_update_package_group_origin_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package_group_origin_configuration("test-domain", "test-package_group", )
    mock_client.call.assert_called_once()


async def test_update_package_group_origin_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package_group_origin_configuration("test-domain", "test-package_group", )


async def test_update_package_versions_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", [], "test-target_status", )
    mock_client.call.assert_called_once()


async def test_update_package_versions_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", [], "test-target_status", )


async def test_update_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_repository("test-domain", "test-repository", )
    mock_client.call.assert_called_once()


async def test_update_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codeartifact.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository("test-domain", "test-repository", )


@pytest.mark.asyncio
async def test_list_domains_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_domains
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_domains(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_repositories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_repositories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_repositories(repository_prefix="test-repository_prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_packages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_packages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_packages("test-domain", "test-repository", domain_owner="test-domain_owner", format="test-format", namespace="test-namespace", package_prefix="test-package_prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_package_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_package_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_package_versions("test-domain", "test-repository", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", status="test-status", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_package_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import copy_package_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", versions="test-versions", version_revisions="test-version_revisions", allow_overwrite=True, include_from_upstream=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_package_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import create_package_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await create_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", contact_info="test-contact_info", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import delete_domain_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await delete_domain_permissions_policy("test-domain", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_package_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import delete_package
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await delete_package("test-domain", "test-repository", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_package_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import delete_package_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await delete_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_package_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import delete_package_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await delete_package_versions("test-domain", "test-repository", "test-format", "test-package", "test-versions", domain_owner="test-domain_owner", namespace="test-namespace", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import delete_repository_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await delete_repository_permissions_policy("test-domain", "test-repository", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_package_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import describe_package_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await describe_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_dispose_package_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import dispose_package_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", "test-versions", domain_owner="test-domain_owner", namespace="test-namespace", version_revisions="test-version_revisions", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_associated_package_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import get_associated_package_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await get_associated_package_group("test-domain", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import get_domain_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await get_domain_permissions_policy("test-domain", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_package_version_asset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import get_package_version_asset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", domain_owner="test-domain_owner", namespace="test-namespace", package_version_revision="test-package_version_revision", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_package_version_readme_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import get_package_version_readme
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import get_repository_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await get_repository_permissions_policy("test-domain", "test-repository", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_allowed_repositories_for_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_allowed_repositories_for_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associated_packages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_associated_packages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_associated_packages("test-domain", "test-package_group", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", preview="test-preview", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_package_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_package_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_package_groups("test-domain", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", prefix="test-prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_package_version_assets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_package_version_assets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_package_version_dependencies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_package_version_dependencies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_repositories_in_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_repositories_in_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_repositories_in_domain("test-domain", domain_owner="test-domain_owner", administrator_account=1, repository_prefix="test-repository_prefix", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sub_package_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import list_sub_package_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await list_sub_package_groups("test-domain", "test-package_group", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import publish_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", domain_owner="test-domain_owner", namespace="test-namespace", unfinished="test-unfinished", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import put_domain_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await put_domain_permissions_policy("test-domain", "test-policy_document", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_package_origin_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import put_package_origin_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", "test-restrictions", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import put_repository_permissions_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import update_package_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await update_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", contact_info="test-contact_info", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_group_origin_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import update_package_group_origin_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await update_package_group_origin_configuration("test-domain", "test-package_group", domain_owner="test-domain_owner", restrictions="test-restrictions", add_allowed_repositories="test-add_allowed_repositories", remove_allowed_repositories="test-remove_allowed_repositories", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_versions_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import update_package_versions_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", "test-versions", "test-target_status", domain_owner="test-domain_owner", namespace="test-namespace", version_revisions="test-version_revisions", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_repository_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codeartifact import update_repository
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codeartifact.async_client", lambda *a, **kw: mock_client)
    await update_repository("test-domain", "test-repository", domain_owner="test-domain_owner", description="test-description", upstreams="test-upstreams", region_name="us-east-1")
    mock_client.call.assert_called_once()
