"""Tests for aws_util.codeartifact -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.codeartifact import (
    AuthorizationTokenResult,
    DomainResult,
    EndpointResult,
    ExternalConnectionResult,
    PackageResult,
    PackageVersionResult,
    RepositoryResult,
    _parse_domain,
    _parse_package,
    _parse_package_version,
    _parse_repository,
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


def _ce(code: str = "SomeError", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "Op")


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


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseDomain:
    def test_minimal(self):
        r = _parse_domain(_domain_dict())
        assert isinstance(r, DomainResult)
        assert r.name == "d1"

    def test_full(self):
        r = _parse_domain(_domain_dict(
            owner="own", status="Active", createdTime="2024-01-01",
            encryptionKey="arn:kms", repositoryCount=5,
            assetSizeBytes=1000, custom="x",
        ))
        assert r.owner == "own"
        assert r.created_time == "2024-01-01"
        assert r.encryption_key == "arn:kms"
        assert r.repository_count == 5
        assert r.asset_size_bytes == 1000
        assert r.extra == {"custom": "x"}


class TestParseRepository:
    def test_minimal(self):
        r = _parse_repository(_repo_dict())
        assert isinstance(r, RepositoryResult)
        assert r.name == "r1"

    def test_full(self):
        r = _parse_repository(_repo_dict(
            domainName="d", domainOwner="own", description="desc",
            administratorAccount="admin",
            upstreams=[{"repositoryName": "up"}],
            externalConnections=[{"externalConnectionName": "ec"}],
            custom="x",
        ))
        assert r.domain_name == "d"
        assert r.domain_owner == "own"
        assert r.description == "desc"
        assert r.administrator_account == "admin"
        assert len(r.upstreams) == 1
        assert len(r.external_connections) == 1
        assert r.extra == {"custom": "x"}


class TestParsePackage:
    def test_minimal(self):
        r = _parse_package(_pkg_dict())
        assert isinstance(r, PackageResult)
        assert r.format == "pypi"

    def test_full(self):
        r = _parse_package(_pkg_dict(
            namespace="ns", originConfiguration={"cfg": True}, custom="x",
        ))
        assert r.namespace == "ns"
        assert r.origin_configuration == {"cfg": True}
        assert r.extra == {"custom": "x"}


class TestParsePackageVersion:
    def test_minimal(self):
        r = _parse_package_version(_pkg_version_dict())
        assert isinstance(r, PackageVersionResult)
        assert r.version == "1.0.0"

    def test_full(self):
        r = _parse_package_version(_pkg_version_dict(
            namespace="ns", status="Published", revision="rev1", custom="x",
        ))
        assert r.namespace == "ns"
        assert r.status == "Published"
        assert r.revision == "rev1"
        assert r.extra == {"custom": "x"}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_authorization_token_result(self):
        r = AuthorizationTokenResult(authorization_token="tok")
        assert r.authorization_token == "tok"
        assert r.expiration is None

    def test_endpoint_result(self):
        r = EndpointResult(repository_endpoint="https://ep")
        assert r.repository_endpoint == "https://ep"

    def test_external_connection_result(self):
        repo = RepositoryResult(name="r", arn="a")
        r = ExternalConnectionResult(repository=repo)
        assert r.repository.name == "r"


# ---------------------------------------------------------------------------
# Domain operations
# ---------------------------------------------------------------------------


class TestCreateDomain:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_domain.return_value = {"domain": _domain_dict()}
        r = create_domain(DOMAIN)
        assert isinstance(r, DomainResult)
        client.create_domain.assert_called_once()

    @patch("aws_util.codeartifact.get_client")
    def test_with_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_domain.return_value = {"domain": _domain_dict()}
        r = create_domain(
            DOMAIN, encryption_key="k", tags=[{"key": "v"}], region_name="eu-west-1"
        )
        assert isinstance(r, DomainResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_domain.side_effect = _ce()
        with pytest.raises(Exception):
            create_domain(DOMAIN)


class TestDescribeDomain:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_domain.return_value = {"domain": _domain_dict()}
        r = describe_domain(DOMAIN)
        assert isinstance(r, DomainResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_domain.return_value = {"domain": _domain_dict()}
        r = describe_domain(DOMAIN, domain_owner=OWNER)
        assert isinstance(r, DomainResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_domain.side_effect = _ce()
        with pytest.raises(Exception):
            describe_domain(DOMAIN)


class TestListDomains:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"domains": [_domain_dict()]}]
        r = list_domains()
        assert len(r) == 1

    @patch("aws_util.codeartifact.get_client")
    def test_with_max_results(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"domains": []}]
        r = list_domains(max_results=10)
        assert r == []

    @patch("aws_util.codeartifact.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [
            {"domains": [_domain_dict()]},
            {"domains": [_domain_dict(name="d2", arn="arn:d2")]},
        ]
        r = list_domains()
        assert len(r) == 2

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_domains()


class TestDeleteDomain:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_domain.return_value = {"domain": _domain_dict()}
        r = delete_domain(DOMAIN)
        assert isinstance(r, DomainResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_domain.return_value = {"domain": _domain_dict()}
        r = delete_domain(DOMAIN, domain_owner=OWNER)
        assert isinstance(r, DomainResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_domain.side_effect = _ce()
        with pytest.raises(Exception):
            delete_domain(DOMAIN)


# ---------------------------------------------------------------------------
# Repository operations
# ---------------------------------------------------------------------------


class TestCreateRepository:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_repository.return_value = {"repository": _repo_dict()}
        r = create_repository(DOMAIN, REPO)
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_repository.return_value = {"repository": _repo_dict()}
        r = create_repository(
            DOMAIN, REPO,
            domain_owner=OWNER, description="d",
            upstreams=[{"repositoryName": "u"}],
            tags=[{"key": "v"}],
        )
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_repository.side_effect = _ce()
        with pytest.raises(Exception):
            create_repository(DOMAIN, REPO)


class TestDescribeRepository:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_repository.return_value = {"repository": _repo_dict()}
        r = describe_repository(DOMAIN, REPO)
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_repository.return_value = {"repository": _repo_dict()}
        r = describe_repository(DOMAIN, REPO, domain_owner=OWNER)
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_repository.side_effect = _ce()
        with pytest.raises(Exception):
            describe_repository(DOMAIN, REPO)


class TestListRepositories:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"repositories": [_repo_dict()]}]
        r = list_repositories()
        assert len(r) == 1

    @patch("aws_util.codeartifact.get_client")
    def test_with_prefix(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"repositories": []}]
        r = list_repositories(repository_prefix="pre")
        assert r == []

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_repositories()


class TestDeleteRepository:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_repository.return_value = {"repository": _repo_dict()}
        r = delete_repository(DOMAIN, REPO)
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_repository.return_value = {"repository": _repo_dict()}
        r = delete_repository(DOMAIN, REPO, domain_owner=OWNER)
        assert isinstance(r, RepositoryResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_repository.side_effect = _ce()
        with pytest.raises(Exception):
            delete_repository(DOMAIN, REPO)


# ---------------------------------------------------------------------------
# Package operations
# ---------------------------------------------------------------------------


class TestListPackages:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"packages": [_pkg_dict()]}]
        r = list_packages(DOMAIN, REPO)
        assert len(r) == 1

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"packages": []}]
        r = list_packages(
            DOMAIN, REPO,
            domain_owner=OWNER, format="npm",
            namespace="ns", package_prefix="pre",
        )
        assert r == []

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_packages(DOMAIN, REPO)


class TestDescribePackage:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package.return_value = {"package": _pkg_dict()}
        r = describe_package(DOMAIN, REPO, "pypi", PKG)
        assert isinstance(r, PackageResult)

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package.return_value = {"package": _pkg_dict()}
        r = describe_package(
            DOMAIN, REPO, "pypi", PKG,
            domain_owner=OWNER, namespace="ns",
        )
        assert isinstance(r, PackageResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package.side_effect = _ce()
        with pytest.raises(Exception):
            describe_package(DOMAIN, REPO, "pypi", PKG)


class TestListPackageVersions:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [
            {"versions": [{"version": "1.0", "status": "Published"}]},
        ]
        r = list_package_versions(DOMAIN, REPO, "pypi", PKG)
        assert len(r) == 1

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"versions": []}]
        r = list_package_versions(
            DOMAIN, REPO, "pypi", PKG,
            domain_owner=OWNER, namespace="ns",
            status="Published", sort_by="PUBLISHED_TIME",
        )
        assert r == []

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_package_versions(DOMAIN, REPO, "pypi", PKG)


class TestDescribePackageVersion:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package_version.return_value = {
            "packageVersion": _pkg_version_dict(),
        }
        r = describe_package_version(DOMAIN, REPO, "pypi", PKG, "1.0.0")
        assert isinstance(r, PackageVersionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package_version.return_value = {
            "packageVersion": _pkg_version_dict(),
        }
        r = describe_package_version(
            DOMAIN, REPO, "pypi", PKG, "1.0.0",
            domain_owner=OWNER, namespace="ns",
        )
        assert isinstance(r, PackageVersionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_package_version.side_effect = _ce()
        with pytest.raises(Exception):
            describe_package_version(DOMAIN, REPO, "pypi", PKG, "1.0.0")


# ---------------------------------------------------------------------------
# Authorization & endpoint
# ---------------------------------------------------------------------------


class TestGetAuthorizationToken:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_authorization_token.return_value = {
            "authorizationToken": "tok123",
            "expiration": "2025-01-01",
        }
        r = get_authorization_token(DOMAIN)
        assert r.authorization_token == "tok123"
        assert r.expiration == "2025-01-01"

    @patch("aws_util.codeartifact.get_client")
    def test_no_expiration(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_authorization_token.return_value = {
            "authorizationToken": "tok123",
        }
        r = get_authorization_token(DOMAIN)
        assert r.expiration is None

    @patch("aws_util.codeartifact.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_authorization_token.return_value = {
            "authorizationToken": "tok",
        }
        r = get_authorization_token(
            DOMAIN, domain_owner=OWNER, duration_seconds=3600,
        )
        assert isinstance(r, AuthorizationTokenResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_authorization_token.side_effect = _ce()
        with pytest.raises(Exception):
            get_authorization_token(DOMAIN)


class TestGetRepositoryEndpoint:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_repository_endpoint.return_value = {
            "repositoryEndpoint": "https://ep.example.com",
        }
        r = get_repository_endpoint(DOMAIN, REPO, "pypi")
        assert r.repository_endpoint == "https://ep.example.com"

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_repository_endpoint.return_value = {
            "repositoryEndpoint": "https://ep",
        }
        r = get_repository_endpoint(DOMAIN, REPO, "pypi", domain_owner=OWNER)
        assert isinstance(r, EndpointResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_repository_endpoint.side_effect = _ce()
        with pytest.raises(Exception):
            get_repository_endpoint(DOMAIN, REPO, "pypi")


# ---------------------------------------------------------------------------
# External connections
# ---------------------------------------------------------------------------


class TestAssociateExternalConnection:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.associate_external_connection.return_value = {
            "repository": _repo_dict(),
        }
        r = associate_external_connection(DOMAIN, REPO, "public:npmjs")
        assert isinstance(r, ExternalConnectionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.associate_external_connection.return_value = {
            "repository": _repo_dict(),
        }
        r = associate_external_connection(
            DOMAIN, REPO, "public:npmjs", domain_owner=OWNER,
        )
        assert isinstance(r, ExternalConnectionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.associate_external_connection.side_effect = _ce()
        with pytest.raises(Exception):
            associate_external_connection(DOMAIN, REPO, "public:npmjs")


class TestDisassociateExternalConnection:
    @patch("aws_util.codeartifact.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.disassociate_external_connection.return_value = {
            "repository": _repo_dict(),
        }
        r = disassociate_external_connection(DOMAIN, REPO, "public:npmjs")
        assert isinstance(r, ExternalConnectionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_with_owner(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.disassociate_external_connection.return_value = {
            "repository": _repo_dict(),
        }
        r = disassociate_external_connection(
            DOMAIN, REPO, "public:npmjs", domain_owner=OWNER,
        )
        assert isinstance(r, ExternalConnectionResult)

    @patch("aws_util.codeartifact.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.disassociate_external_connection.side_effect = _ce()
        with pytest.raises(Exception):
            disassociate_external_connection(DOMAIN, REPO, "public:npmjs")


REGION = "us-east-1"


@patch("aws_util.codeartifact.get_client")
def test_copy_package_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_package_versions.return_value = {}
    copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", region_name=REGION)
    mock_client.copy_package_versions.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_copy_package_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_package_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_package_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to copy package versions"):
        copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_create_package_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package_group.return_value = {}
    create_package_group("test-domain", "test-package_group", region_name=REGION)
    mock_client.create_package_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_create_package_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_package_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create package group"):
        create_package_group("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_delete_domain_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_permissions_policy.return_value = {}
    delete_domain_permissions_policy("test-domain", region_name=REGION)
    mock_client.delete_domain_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_delete_domain_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete domain permissions policy"):
        delete_domain_permissions_policy("test-domain", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_delete_package(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package.return_value = {}
    delete_package("test-domain", "test-repository", "test-format", "test-package", region_name=REGION)
    mock_client.delete_package.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_delete_package_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_package",
    )
    with pytest.raises(RuntimeError, match="Failed to delete package"):
        delete_package("test-domain", "test-repository", "test-format", "test-package", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_delete_package_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_group.return_value = {}
    delete_package_group("test-domain", "test-package_group", region_name=REGION)
    mock_client.delete_package_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_delete_package_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_package_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete package group"):
        delete_package_group("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_delete_package_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_versions.return_value = {}
    delete_package_versions("test-domain", "test-repository", "test-format", "test-package", [], region_name=REGION)
    mock_client.delete_package_versions.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_delete_package_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_package_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to delete package versions"):
        delete_package_versions("test-domain", "test-repository", "test-format", "test-package", [], region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_delete_repository_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_repository_permissions_policy.return_value = {}
    delete_repository_permissions_policy("test-domain", "test-repository", region_name=REGION)
    mock_client.delete_repository_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_delete_repository_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_repository_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_repository_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete repository permissions policy"):
        delete_repository_permissions_policy("test-domain", "test-repository", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_describe_package_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_package_group.return_value = {}
    describe_package_group("test-domain", "test-package_group", region_name=REGION)
    mock_client.describe_package_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_describe_package_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_package_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_package_group",
    )
    with pytest.raises(RuntimeError, match="Failed to describe package group"):
        describe_package_group("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_dispose_package_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.dispose_package_versions.return_value = {}
    dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", [], region_name=REGION)
    mock_client.dispose_package_versions.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_dispose_package_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.dispose_package_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "dispose_package_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to dispose package versions"):
        dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", [], region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_get_associated_package_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_associated_package_group.return_value = {}
    get_associated_package_group("test-domain", "test-format", "test-package", region_name=REGION)
    mock_client.get_associated_package_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_get_associated_package_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_associated_package_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_associated_package_group",
    )
    with pytest.raises(RuntimeError, match="Failed to get associated package group"):
        get_associated_package_group("test-domain", "test-format", "test-package", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_get_domain_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domain_permissions_policy.return_value = {}
    get_domain_permissions_policy("test-domain", region_name=REGION)
    mock_client.get_domain_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_get_domain_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domain_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to get domain permissions policy"):
        get_domain_permissions_policy("test-domain", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_get_package_version_asset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version_asset.return_value = {}
    get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", region_name=REGION)
    mock_client.get_package_version_asset.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_get_package_version_asset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version_asset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_package_version_asset",
    )
    with pytest.raises(RuntimeError, match="Failed to get package version asset"):
        get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_get_package_version_readme(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version_readme.return_value = {}
    get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)
    mock_client.get_package_version_readme.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_get_package_version_readme_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version_readme.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_package_version_readme",
    )
    with pytest.raises(RuntimeError, match="Failed to get package version readme"):
        get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_get_repository_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_permissions_policy.return_value = {}
    get_repository_permissions_policy("test-domain", "test-repository", region_name=REGION)
    mock_client.get_repository_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_get_repository_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_repository_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to get repository permissions policy"):
        get_repository_permissions_policy("test-domain", "test-repository", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_allowed_repositories_for_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_repositories_for_group.return_value = {}
    list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", region_name=REGION)
    mock_client.list_allowed_repositories_for_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_allowed_repositories_for_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_repositories_for_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_allowed_repositories_for_group",
    )
    with pytest.raises(RuntimeError, match="Failed to list allowed repositories for group"):
        list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_associated_packages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_packages.return_value = {}
    list_associated_packages("test-domain", "test-package_group", region_name=REGION)
    mock_client.list_associated_packages.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_associated_packages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_packages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associated_packages",
    )
    with pytest.raises(RuntimeError, match="Failed to list associated packages"):
        list_associated_packages("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_package_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_groups.return_value = {}
    list_package_groups("test-domain", region_name=REGION)
    mock_client.list_package_groups.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_package_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_package_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to list package groups"):
        list_package_groups("test-domain", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_package_version_assets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_version_assets.return_value = {}
    list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)
    mock_client.list_package_version_assets.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_package_version_assets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_version_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_package_version_assets",
    )
    with pytest.raises(RuntimeError, match="Failed to list package version assets"):
        list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_package_version_dependencies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_version_dependencies.return_value = {}
    list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)
    mock_client.list_package_version_dependencies.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_package_version_dependencies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_version_dependencies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_package_version_dependencies",
    )
    with pytest.raises(RuntimeError, match="Failed to list package version dependencies"):
        list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_repositories_in_domain(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repositories_in_domain.return_value = {}
    list_repositories_in_domain("test-domain", region_name=REGION)
    mock_client.list_repositories_in_domain.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_repositories_in_domain_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repositories_in_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_repositories_in_domain",
    )
    with pytest.raises(RuntimeError, match="Failed to list repositories in domain"):
        list_repositories_in_domain("test-domain", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_sub_package_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sub_package_groups.return_value = {}
    list_sub_package_groups("test-domain", "test-package_group", region_name=REGION)
    mock_client.list_sub_package_groups.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_sub_package_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sub_package_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sub_package_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to list sub package groups"):
        list_sub_package_groups("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_publish_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.publish_package_version.return_value = {}
    publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", region_name=REGION)
    mock_client.publish_package_version.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_publish_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.publish_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to publish package version"):
        publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_put_domain_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_domain_permissions_policy.return_value = {}
    put_domain_permissions_policy("test-domain", "test-policy_document", region_name=REGION)
    mock_client.put_domain_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_put_domain_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_domain_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_domain_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to put domain permissions policy"):
        put_domain_permissions_policy("test-domain", "test-policy_document", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_put_package_origin_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_package_origin_configuration.return_value = {}
    put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", {}, region_name=REGION)
    mock_client.put_package_origin_configuration.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_put_package_origin_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_package_origin_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_package_origin_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to put package origin configuration"):
        put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", {}, region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_put_repository_permissions_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_repository_permissions_policy.return_value = {}
    put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", region_name=REGION)
    mock_client.put_repository_permissions_policy.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_put_repository_permissions_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_repository_permissions_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_repository_permissions_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to put repository permissions policy"):
        put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_update_package_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_group.return_value = {}
    update_package_group("test-domain", "test-package_group", region_name=REGION)
    mock_client.update_package_group.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_update_package_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update package group"):
        update_package_group("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_update_package_group_origin_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_group_origin_configuration.return_value = {}
    update_package_group_origin_configuration("test-domain", "test-package_group", region_name=REGION)
    mock_client.update_package_group_origin_configuration.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_update_package_group_origin_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_group_origin_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package_group_origin_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update package group origin configuration"):
        update_package_group_origin_configuration("test-domain", "test-package_group", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_update_package_versions_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_versions_status.return_value = {}
    update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", [], "test-target_status", region_name=REGION)
    mock_client.update_package_versions_status.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_update_package_versions_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_versions_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package_versions_status",
    )
    with pytest.raises(RuntimeError, match="Failed to update package versions status"):
        update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", [], "test-target_status", region_name=REGION)


@patch("aws_util.codeartifact.get_client")
def test_update_repository(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository.return_value = {}
    update_repository("test-domain", "test-repository", region_name=REGION)
    mock_client.update_repository.assert_called_once()


@patch("aws_util.codeartifact.get_client")
def test_update_repository_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_repository",
    )
    with pytest.raises(RuntimeError, match="Failed to update repository"):
        update_repository("test-domain", "test-repository", region_name=REGION)


def test_copy_package_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import copy_package_versions
    mock_client = MagicMock()
    mock_client.copy_package_versions.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    copy_package_versions("test-domain", "test-source_repository", "test-destination_repository", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", versions="test-versions", version_revisions="test-version_revisions", allow_overwrite=True, include_from_upstream=True, region_name="us-east-1")
    mock_client.copy_package_versions.assert_called_once()

def test_create_package_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import create_package_group
    mock_client = MagicMock()
    mock_client.create_package_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    create_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", contact_info="test-contact_info", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_package_group.assert_called_once()

def test_delete_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import delete_domain_permissions_policy
    mock_client = MagicMock()
    mock_client.delete_domain_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    delete_domain_permissions_policy("test-domain", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.delete_domain_permissions_policy.assert_called_once()

def test_delete_package_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import delete_package
    mock_client = MagicMock()
    mock_client.delete_package.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    delete_package("test-domain", "test-repository", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.delete_package.assert_called_once()

def test_delete_package_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import delete_package_group
    mock_client = MagicMock()
    mock_client.delete_package_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    delete_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.delete_package_group.assert_called_once()

def test_delete_package_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import delete_package_versions
    mock_client = MagicMock()
    mock_client.delete_package_versions.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    delete_package_versions("test-domain", "test-repository", "test-format", "test-package", "test-versions", domain_owner="test-domain_owner", namespace="test-namespace", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.delete_package_versions.assert_called_once()

def test_delete_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import delete_repository_permissions_policy
    mock_client = MagicMock()
    mock_client.delete_repository_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    delete_repository_permissions_policy("test-domain", "test-repository", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.delete_repository_permissions_policy.assert_called_once()

def test_describe_package_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import describe_package_group
    mock_client = MagicMock()
    mock_client.describe_package_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    describe_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.describe_package_group.assert_called_once()

def test_dispose_package_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import dispose_package_versions
    mock_client = MagicMock()
    mock_client.dispose_package_versions.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    dispose_package_versions("test-domain", "test-repository", "test-format", "test-package", "test-versions", domain_owner="test-domain_owner", namespace="test-namespace", version_revisions="test-version_revisions", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.dispose_package_versions.assert_called_once()

def test_get_associated_package_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import get_associated_package_group
    mock_client = MagicMock()
    mock_client.get_associated_package_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    get_associated_package_group("test-domain", "test-format", "test-package", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.get_associated_package_group.assert_called_once()

def test_get_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import get_domain_permissions_policy
    mock_client = MagicMock()
    mock_client.get_domain_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    get_domain_permissions_policy("test-domain", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.get_domain_permissions_policy.assert_called_once()

def test_get_package_version_asset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import get_package_version_asset
    mock_client = MagicMock()
    mock_client.get_package_version_asset.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    get_package_version_asset("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset", domain_owner="test-domain_owner", namespace="test-namespace", package_version_revision="test-package_version_revision", region_name="us-east-1")
    mock_client.get_package_version_asset.assert_called_once()

def test_get_package_version_readme_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import get_package_version_readme
    mock_client = MagicMock()
    mock_client.get_package_version_readme.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    get_package_version_readme("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.get_package_version_readme.assert_called_once()

def test_get_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import get_repository_permissions_policy
    mock_client = MagicMock()
    mock_client.get_repository_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    get_repository_permissions_policy("test-domain", "test-repository", domain_owner="test-domain_owner", region_name="us-east-1")
    mock_client.get_repository_permissions_policy.assert_called_once()

def test_list_allowed_repositories_for_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_allowed_repositories_for_group
    mock_client = MagicMock()
    mock_client.list_allowed_repositories_for_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_allowed_repositories_for_group("test-domain", "test-package_group", "test-origin_restriction_type", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_allowed_repositories_for_group.assert_called_once()

def test_list_associated_packages_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_associated_packages
    mock_client = MagicMock()
    mock_client.list_associated_packages.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_associated_packages("test-domain", "test-package_group", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", preview="test-preview", region_name="us-east-1")
    mock_client.list_associated_packages.assert_called_once()

def test_list_package_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_package_groups
    mock_client = MagicMock()
    mock_client.list_package_groups.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_package_groups("test-domain", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", prefix="test-prefix", region_name="us-east-1")
    mock_client.list_package_groups.assert_called_once()

def test_list_package_version_assets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_package_version_assets
    mock_client = MagicMock()
    mock_client.list_package_version_assets.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_package_version_assets("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_package_version_assets.assert_called_once()

def test_list_package_version_dependencies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_package_version_dependencies
    mock_client = MagicMock()
    mock_client.list_package_version_dependencies.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_package_version_dependencies("test-domain", "test-repository", "test-format", "test-package", "test-package_version", domain_owner="test-domain_owner", namespace="test-namespace", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_package_version_dependencies.assert_called_once()

def test_list_repositories_in_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_repositories_in_domain
    mock_client = MagicMock()
    mock_client.list_repositories_in_domain.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_repositories_in_domain("test-domain", domain_owner="test-domain_owner", administrator_account=1, repository_prefix="test-repository_prefix", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_repositories_in_domain.assert_called_once()

def test_list_sub_package_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import list_sub_package_groups
    mock_client = MagicMock()
    mock_client.list_sub_package_groups.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    list_sub_package_groups("test-domain", "test-package_group", domain_owner="test-domain_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sub_package_groups.assert_called_once()

def test_publish_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import publish_package_version
    mock_client = MagicMock()
    mock_client.publish_package_version.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    publish_package_version("test-domain", "test-repository", "test-format", "test-package", "test-package_version", "test-asset_content", "test-asset_name", "test-asset_sha256", domain_owner="test-domain_owner", namespace="test-namespace", unfinished="test-unfinished", region_name="us-east-1")
    mock_client.publish_package_version.assert_called_once()

def test_put_domain_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import put_domain_permissions_policy
    mock_client = MagicMock()
    mock_client.put_domain_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    put_domain_permissions_policy("test-domain", "test-policy_document", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.put_domain_permissions_policy.assert_called_once()

def test_put_package_origin_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import put_package_origin_configuration
    mock_client = MagicMock()
    mock_client.put_package_origin_configuration.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    put_package_origin_configuration("test-domain", "test-repository", "test-format", "test-package", "test-restrictions", domain_owner="test-domain_owner", namespace="test-namespace", region_name="us-east-1")
    mock_client.put_package_origin_configuration.assert_called_once()

def test_put_repository_permissions_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import put_repository_permissions_policy
    mock_client = MagicMock()
    mock_client.put_repository_permissions_policy.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    put_repository_permissions_policy("test-domain", "test-repository", "test-policy_document", domain_owner="test-domain_owner", policy_revision="test-policy_revision", region_name="us-east-1")
    mock_client.put_repository_permissions_policy.assert_called_once()

def test_update_package_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import update_package_group
    mock_client = MagicMock()
    mock_client.update_package_group.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    update_package_group("test-domain", "test-package_group", domain_owner="test-domain_owner", contact_info="test-contact_info", description="test-description", region_name="us-east-1")
    mock_client.update_package_group.assert_called_once()

def test_update_package_group_origin_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import update_package_group_origin_configuration
    mock_client = MagicMock()
    mock_client.update_package_group_origin_configuration.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    update_package_group_origin_configuration("test-domain", "test-package_group", domain_owner="test-domain_owner", restrictions="test-restrictions", add_allowed_repositories="test-add_allowed_repositories", remove_allowed_repositories="test-remove_allowed_repositories", region_name="us-east-1")
    mock_client.update_package_group_origin_configuration.assert_called_once()

def test_update_package_versions_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import update_package_versions_status
    mock_client = MagicMock()
    mock_client.update_package_versions_status.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    update_package_versions_status("test-domain", "test-repository", "test-format", "test-package", "test-versions", "test-target_status", domain_owner="test-domain_owner", namespace="test-namespace", version_revisions="test-version_revisions", expected_status="test-expected_status", region_name="us-east-1")
    mock_client.update_package_versions_status.assert_called_once()

def test_update_repository_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codeartifact import update_repository
    mock_client = MagicMock()
    mock_client.update_repository.return_value = {}
    monkeypatch.setattr("aws_util.codeartifact.get_client", lambda *a, **kw: mock_client)
    update_repository("test-domain", "test-repository", domain_owner="test-domain_owner", description="test-description", upstreams="test-upstreams", region_name="us-east-1")
    mock_client.update_repository.assert_called_once()
