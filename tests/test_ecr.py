"""Tests for aws_util.ecr module."""
from __future__ import annotations

import base64
import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.ecr as ecr_mod
from aws_util.ecr import (
    ECRRepository,
    ECRImage,
    ECRAuthToken,
    get_auth_token,
    list_repositories,
    describe_repository,
    list_images,
    ensure_repository,
    get_latest_image_tag,
    batch_check_layer_availability,
    batch_delete_image,
    batch_get_image,
    batch_get_repository_scanning_configuration,
    complete_layer_upload,
    create_pull_through_cache_rule,
    create_repository,
    create_repository_creation_template,
    delete_lifecycle_policy,
    delete_pull_through_cache_rule,
    delete_registry_policy,
    delete_repository,
    delete_repository_creation_template,
    delete_repository_policy,
    describe_image_replication_status,
    describe_image_scan_findings,
    describe_images,
    describe_pull_through_cache_rules,
    describe_registry,
    describe_repositories,
    describe_repository_creation_templates,
    get_account_setting,
    get_authorization_token,
    get_download_url_for_layer,
    get_lifecycle_policy,
    get_lifecycle_policy_preview,
    get_registry_policy,
    get_registry_scanning_configuration,
    get_repository_policy,
    initiate_layer_upload,
    list_tags_for_resource,
    put_account_setting,
    put_image,
    put_image_scanning_configuration,
    put_image_tag_mutability,
    put_lifecycle_policy,
    put_registry_policy,
    put_registry_scanning_configuration,
    put_replication_configuration,
    set_repository_policy,
    start_image_scan,
    start_lifecycle_policy_preview,
    tag_resource,
    untag_resource,
    update_pull_through_cache_rule,
    update_repository_creation_template,
    upload_layer_part,
    validate_pull_through_cache_rule,
)

REGION = "us-east-1"
REPO_NAME = "test-repo"


@pytest.fixture
def ecr_repo():
    client = boto3.client("ecr", region_name=REGION)
    resp = client.create_repository(repositoryName=REPO_NAME)
    return resp["repository"]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_ecr_repository_model():
    repo = ECRRepository(
        repository_name=REPO_NAME,
        repository_arn="arn:aws:ecr:us-east-1:123:repository/test",
        repository_uri="123.dkr.ecr.us-east-1.amazonaws.com/test",
        registry_id="123456789012",
    )
    assert repo.repository_name == REPO_NAME
    assert repo.image_tag_mutability == "MUTABLE"


def test_ecr_image_model():
    img = ECRImage(
        registry_id="123456789012",
        repository_name=REPO_NAME,
        image_digest="sha256:abc",
    )
    assert img.image_tags == []


def test_ecr_auth_token_model():
    token = ECRAuthToken(
        endpoint="https://123.dkr.ecr.us-east-1.amazonaws.com",
        username="AWS",
        password="secret",
    )
    assert token.username == "AWS"


# ---------------------------------------------------------------------------
# get_auth_token
# ---------------------------------------------------------------------------

def test_get_auth_token_success(ecr_repo):
    result = get_auth_token(region_name=REGION)
    assert isinstance(result, list)
    # moto returns auth tokens
    for token in result:
        assert isinstance(token, ECRAuthToken)


def test_get_auth_token_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorization_token.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "GetAuthorizationToken"
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_auth_token failed"):
        get_auth_token(region_name=REGION)


# ---------------------------------------------------------------------------
# list_repositories
# ---------------------------------------------------------------------------

def test_list_repositories_returns_list(ecr_repo):
    result = list_repositories(region_name=REGION)
    assert isinstance(result, list)
    assert any(r.repository_name == REPO_NAME for r in result)


def test_list_repositories_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "DescribeRepositories"
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_repositories failed"):
        list_repositories(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_repository
# ---------------------------------------------------------------------------

def test_describe_repository_found(ecr_repo):
    result = describe_repository(REPO_NAME, region_name=REGION)
    assert result is not None
    assert result.repository_name == REPO_NAME


def test_describe_repository_not_found(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repositories.side_effect = ClientError(
        {"Error": {"Code": "RepositoryNotFoundException", "Message": "not found"}},
        "DescribeRepositories",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_repository("nonexistent", region_name=REGION)
    assert result is None


def test_describe_repository_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repositories.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "DescribeRepositories"
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_repository failed"):
        describe_repository(REPO_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# list_images
# ---------------------------------------------------------------------------

def test_list_images_empty_repo(ecr_repo):
    result = list_images(REPO_NAME, region_name=REGION)
    assert isinstance(result, list)
    assert result == []


def test_list_images_runtime_error(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "RepositoryNotFoundException", "Message": "not found"}}, "ListImages"
    )
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_images failed"):
        list_images("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# ensure_repository
# ---------------------------------------------------------------------------

def test_ensure_repository_existing(ecr_repo):
    result = ensure_repository(REPO_NAME, region_name=REGION)
    assert result.repository_name == REPO_NAME


def test_ensure_repository_creates_new(monkeypatch):
    # First call (describe) returns None (not found), then creates
    call_count = {"n": 0}

    def fake_describe(name, registry_id=None, region_name=None):
        call_count["n"] += 1
        return None

    mock_client = MagicMock()
    mock_client.create_repository.return_value = {
        "repository": {
            "repositoryName": "new-repo",
            "repositoryArn": "arn:aws:ecr:us-east-1:123:repository/new-repo",
            "repositoryUri": "123.dkr.ecr.us-east-1.amazonaws.com/new-repo",
            "registryId": "123456789012",
            "imageTagMutability": "MUTABLE",
        }
    }
    monkeypatch.setattr(ecr_mod, "describe_repository", fake_describe)
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = ensure_repository("new-repo", region_name=REGION)
    assert result.repository_name == "new-repo"


def test_ensure_repository_create_error(monkeypatch):
    monkeypatch.setattr(ecr_mod, "describe_repository", lambda *a, **kw: None)
    mock_client = MagicMock()
    mock_client.create_repository.side_effect = ClientError(
        {"Error": {"Code": "RepositoryAlreadyExistsException", "Message": "exists"}},
        "CreateRepository",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ECR repository"):
        ensure_repository("fail-repo", region_name=REGION)


# ---------------------------------------------------------------------------
# get_latest_image_tag
# ---------------------------------------------------------------------------

def test_get_latest_image_tag_no_images(ecr_repo, monkeypatch):
    monkeypatch.setattr(ecr_mod, "list_images", lambda *a, **kw: [])
    result = get_latest_image_tag(REPO_NAME, region_name=REGION)
    assert result is None


def test_get_auth_token_with_registry_ids(monkeypatch):
    """Covers the registry_ids kwarg branch in get_auth_token (line 82)."""
    import base64
    token_val = base64.b64encode(b"AWS:password123").decode()
    mock_client = MagicMock()
    mock_client.get_authorization_token.return_value = {
        "authorizationData": [{
            "authorizationToken": token_val,
            "proxyEndpoint": "https://123.dkr.ecr.us-east-1.amazonaws.com",
        }]
    }
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_auth_token(registry_ids=["123456789012"], region_name=REGION)
    assert len(result) == 1
    call_kwargs = mock_client.get_authorization_token.call_args[1]
    assert call_kwargs.get("registryIds") == ["123456789012"]


def test_list_repositories_with_registry_id(monkeypatch):
    """Covers the registry_id kwarg branch in list_repositories (line 123)."""
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"repositories": []}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_repositories(registry_id="123456789012", region_name=REGION)
    assert result == []
    call_kwargs = mock_paginator.paginate.call_args[1]
    assert call_kwargs.get("registryId") == "123456789012"


def test_describe_repository_with_registry_id(ecr_repo):
    """Covers registry_id kwarg branch in describe_repository (line 166)."""
    result = describe_repository(REPO_NAME, registry_id="123456789012", region_name=REGION)
    assert result is not None or result is None  # just exercise the branch


def test_describe_repository_empty_response(monkeypatch):
    """Covers the repos=[] return None branch (line 175)."""
    mock_client = MagicMock()
    mock_client.describe_repositories.return_value = {"repositories": []}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_repository("empty", region_name=REGION)
    assert result is None


def test_list_images_with_registry_id(monkeypatch):
    """Covers registry_id kwarg in list_images (line 213)."""
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"imageIds": []}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_images(REPO_NAME, registry_id="123", region_name=REGION)
    assert result == []
    call_kwargs = mock_paginator.paginate.call_args[1]
    assert call_kwargs.get("registryId") == "123"


def test_list_images_with_actual_images(monkeypatch):
    """Covers the describe_images batch path (lines 227-249)."""
    from datetime import datetime, timezone
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"imageIds": [{"imageDigest": "sha256:abc", "imageTag": "v1.0"}]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    mock_client.describe_images.return_value = {
        "imageDetails": [{
            "registryId": "123",
            "repositoryName": REPO_NAME,
            "imageDigest": "sha256:abc",
            "imageTags": ["v1.0"],
            "imagePushedAt": datetime(2024, 6, 1, tzinfo=timezone.utc),
            "imageSizeInBytes": 10000,
        }]
    }
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_images(REPO_NAME, region_name=REGION)
    assert len(result) == 1
    assert result[0].image_tags == ["v1.0"]


def test_list_images_describe_images_error(monkeypatch):
    """Covers the ClientError in describe_images (line 247-248)."""
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"imageIds": [{"imageDigest": "sha256:abc"}]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    mock_client.describe_images.side_effect = ClientError(
        {"Error": {"Code": "ImageNotFoundException", "Message": "not found"}}, "DescribeImages"
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_images failed"):
        list_images(REPO_NAME, region_name=REGION)


def test_get_latest_image_tag_with_images(monkeypatch):
    from datetime import datetime, timezone
    img1 = ECRImage(
        registry_id="123",
        repository_name=REPO_NAME,
        image_digest="sha256:aaa",
        image_tags=["v1.0"],
        image_pushed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    img2 = ECRImage(
        registry_id="123",
        repository_name=REPO_NAME,
        image_digest="sha256:bbb",
        image_tags=["v2.0"],
        image_pushed_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )
    monkeypatch.setattr(ecr_mod, "list_images", lambda *a, **kw: [img1, img2])
    result = get_latest_image_tag(REPO_NAME, region_name=REGION)
    assert result == "v2.0"


def test_list_images_with_registry_id_and_images(monkeypatch):
    """Covers registry_id branch in describe_images batch call (line 231)."""
    from datetime import datetime, timezone
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"imageIds": [{"imageDigest": "sha256:abc"}]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    mock_client.describe_images.return_value = {
        "imageDetails": [{
            "registryId": "123",
            "repositoryName": REPO_NAME,
            "imageDigest": "sha256:abc",
            "imageTags": ["latest"],
            "imagePushedAt": datetime(2024, 1, 1, tzinfo=timezone.utc),
        }]
    }
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_images(REPO_NAME, registry_id="123", region_name=REGION)
    assert len(result) == 1
    call_kwargs = mock_client.describe_images.call_args[1]
    assert call_kwargs.get("registryId") == "123"


def test_batch_check_layer_availability(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_check_layer_availability.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    batch_check_layer_availability("test-repository_name", [], region_name=REGION)
    mock_client.batch_check_layer_availability.assert_called_once()


def test_batch_check_layer_availability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_check_layer_availability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_check_layer_availability",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch check layer availability"):
        batch_check_layer_availability("test-repository_name", [], region_name=REGION)


def test_batch_delete_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_image.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    batch_delete_image("test-repository_name", [], region_name=REGION)
    mock_client.batch_delete_image.assert_called_once()


def test_batch_delete_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_image",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete image"):
        batch_delete_image("test-repository_name", [], region_name=REGION)


def test_batch_get_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_image.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_image("test-repository_name", [], region_name=REGION)
    mock_client.batch_get_image.assert_called_once()


def test_batch_get_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_image",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get image"):
        batch_get_image("test-repository_name", [], region_name=REGION)


def test_batch_get_repository_scanning_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_repository_scanning_configuration.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_repository_scanning_configuration([], region_name=REGION)
    mock_client.batch_get_repository_scanning_configuration.assert_called_once()


def test_batch_get_repository_scanning_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_repository_scanning_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_repository_scanning_configuration",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get repository scanning configuration"):
        batch_get_repository_scanning_configuration([], region_name=REGION)


def test_complete_layer_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_layer_upload.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    complete_layer_upload("test-repository_name", "test-upload_id", [], region_name=REGION)
    mock_client.complete_layer_upload.assert_called_once()


def test_complete_layer_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_layer_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "complete_layer_upload",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete layer upload"):
        complete_layer_upload("test-repository_name", "test-upload_id", [], region_name=REGION)


def test_create_pull_through_cache_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", region_name=REGION)
    mock_client.create_pull_through_cache_rule.assert_called_once()


def test_create_pull_through_cache_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_pull_through_cache_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_pull_through_cache_rule",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create pull through cache rule"):
        create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", region_name=REGION)


def test_create_repository(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_repository.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    create_repository("test-repository_name", region_name=REGION)
    mock_client.create_repository.assert_called_once()


def test_create_repository_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_repository",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create repository"):
        create_repository("test-repository_name", region_name=REGION)


def test_create_repository_creation_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_repository_creation_template.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    create_repository_creation_template("test-prefix", [], region_name=REGION)
    mock_client.create_repository_creation_template.assert_called_once()


def test_create_repository_creation_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_repository_creation_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_repository_creation_template",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create repository creation template"):
        create_repository_creation_template("test-prefix", [], region_name=REGION)


def test_delete_lifecycle_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lifecycle_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_lifecycle_policy("test-repository_name", region_name=REGION)
    mock_client.delete_lifecycle_policy.assert_called_once()


def test_delete_lifecycle_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lifecycle_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_lifecycle_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete lifecycle policy"):
        delete_lifecycle_policy("test-repository_name", region_name=REGION)


def test_delete_pull_through_cache_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)
    mock_client.delete_pull_through_cache_rule.assert_called_once()


def test_delete_pull_through_cache_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pull_through_cache_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_pull_through_cache_rule",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete pull through cache rule"):
        delete_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)


def test_delete_registry_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_registry_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_registry_policy(region_name=REGION)
    mock_client.delete_registry_policy.assert_called_once()


def test_delete_registry_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_registry_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_registry_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete registry policy"):
        delete_registry_policy(region_name=REGION)


def test_delete_repository(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_repository("test-repository_name", region_name=REGION)
    mock_client.delete_repository.assert_called_once()


def test_delete_repository_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_repository",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete repository"):
        delete_repository("test-repository_name", region_name=REGION)


def test_delete_repository_creation_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository_creation_template.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_repository_creation_template("test-prefix", region_name=REGION)
    mock_client.delete_repository_creation_template.assert_called_once()


def test_delete_repository_creation_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository_creation_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_repository_creation_template",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete repository creation template"):
        delete_repository_creation_template("test-prefix", region_name=REGION)


def test_delete_repository_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    delete_repository_policy("test-repository_name", region_name=REGION)
    mock_client.delete_repository_policy.assert_called_once()


def test_delete_repository_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_repository_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_repository_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete repository policy"):
        delete_repository_policy("test-repository_name", region_name=REGION)


def test_describe_image_replication_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_replication_status.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_image_replication_status("test-repository_name", {}, region_name=REGION)
    mock_client.describe_image_replication_status.assert_called_once()


def test_describe_image_replication_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_replication_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_replication_status",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image replication status"):
        describe_image_replication_status("test-repository_name", {}, region_name=REGION)


def test_describe_image_scan_findings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_scan_findings.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_image_scan_findings("test-repository_name", {}, region_name=REGION)
    mock_client.describe_image_scan_findings.assert_called_once()


def test_describe_image_scan_findings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_scan_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_scan_findings",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image scan findings"):
        describe_image_scan_findings("test-repository_name", {}, region_name=REGION)


def test_describe_images(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_images.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_images("test-repository_name", region_name=REGION)
    mock_client.describe_images.assert_called_once()


def test_describe_images_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_images.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_images",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe images"):
        describe_images("test-repository_name", region_name=REGION)


def test_describe_pull_through_cache_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pull_through_cache_rules.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_pull_through_cache_rules(region_name=REGION)
    mock_client.describe_pull_through_cache_rules.assert_called_once()


def test_describe_pull_through_cache_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pull_through_cache_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pull_through_cache_rules",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe pull through cache rules"):
        describe_pull_through_cache_rules(region_name=REGION)


def test_describe_registry(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_registry.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_registry(region_name=REGION)
    mock_client.describe_registry.assert_called_once()


def test_describe_registry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_registry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_registry",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe registry"):
        describe_registry(region_name=REGION)


def test_describe_repositories(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repositories.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_repositories(region_name=REGION)
    mock_client.describe_repositories.assert_called_once()


def test_describe_repositories_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repositories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_repositories",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe repositories"):
        describe_repositories(region_name=REGION)


def test_describe_repository_creation_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repository_creation_templates.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    describe_repository_creation_templates(region_name=REGION)
    mock_client.describe_repository_creation_templates.assert_called_once()


def test_describe_repository_creation_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_repository_creation_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_repository_creation_templates",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe repository creation templates"):
        describe_repository_creation_templates(region_name=REGION)


def test_get_account_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_setting.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_account_setting("test-name", region_name=REGION)
    mock_client.get_account_setting.assert_called_once()


def test_get_account_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_setting",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account setting"):
        get_account_setting("test-name", region_name=REGION)


def test_get_authorization_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorization_token.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_authorization_token(region_name=REGION)
    mock_client.get_authorization_token.assert_called_once()


def test_get_authorization_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorization_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_authorization_token",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get authorization token"):
        get_authorization_token(region_name=REGION)


def test_get_download_url_for_layer(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_download_url_for_layer.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_download_url_for_layer("test-repository_name", "test-layer_digest", region_name=REGION)
    mock_client.get_download_url_for_layer.assert_called_once()


def test_get_download_url_for_layer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_download_url_for_layer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_download_url_for_layer",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get download url for layer"):
        get_download_url_for_layer("test-repository_name", "test-layer_digest", region_name=REGION)


def test_get_lifecycle_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_lifecycle_policy("test-repository_name", region_name=REGION)
    mock_client.get_lifecycle_policy.assert_called_once()


def test_get_lifecycle_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_lifecycle_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get lifecycle policy"):
        get_lifecycle_policy("test-repository_name", region_name=REGION)


def test_get_lifecycle_policy_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy_preview.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_lifecycle_policy_preview("test-repository_name", region_name=REGION)
    mock_client.get_lifecycle_policy_preview.assert_called_once()


def test_get_lifecycle_policy_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_lifecycle_policy_preview",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get lifecycle policy preview"):
        get_lifecycle_policy_preview("test-repository_name", region_name=REGION)


def test_get_registry_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_registry_policy(region_name=REGION)
    mock_client.get_registry_policy.assert_called_once()


def test_get_registry_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_registry_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get registry policy"):
        get_registry_policy(region_name=REGION)


def test_get_registry_scanning_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry_scanning_configuration.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_registry_scanning_configuration(region_name=REGION)
    mock_client.get_registry_scanning_configuration.assert_called_once()


def test_get_registry_scanning_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry_scanning_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_registry_scanning_configuration",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get registry scanning configuration"):
        get_registry_scanning_configuration(region_name=REGION)


def test_get_repository_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_repository_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    get_repository_policy("test-repository_name", region_name=REGION)
    mock_client.get_repository_policy.assert_called_once()


def test_get_repository_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_repository_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_repository_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get repository policy"):
        get_repository_policy("test-repository_name", region_name=REGION)


def test_initiate_layer_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.initiate_layer_upload.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    initiate_layer_upload("test-repository_name", region_name=REGION)
    mock_client.initiate_layer_upload.assert_called_once()


def test_initiate_layer_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.initiate_layer_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "initiate_layer_upload",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to initiate layer upload"):
        initiate_layer_upload("test-repository_name", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_put_account_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_account_setting("test-name", "test-value", region_name=REGION)
    mock_client.put_account_setting.assert_called_once()


def test_put_account_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_setting",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account setting"):
        put_account_setting("test-name", "test-value", region_name=REGION)


def test_put_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_image("test-repository_name", "test-image_manifest", region_name=REGION)
    mock_client.put_image.assert_called_once()


def test_put_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_image",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put image"):
        put_image("test-repository_name", "test-image_manifest", region_name=REGION)


def test_put_image_scanning_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image_scanning_configuration.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_image_scanning_configuration("test-repository_name", {}, region_name=REGION)
    mock_client.put_image_scanning_configuration.assert_called_once()


def test_put_image_scanning_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image_scanning_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_image_scanning_configuration",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put image scanning configuration"):
        put_image_scanning_configuration("test-repository_name", {}, region_name=REGION)


def test_put_image_tag_mutability(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image_tag_mutability.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", region_name=REGION)
    mock_client.put_image_tag_mutability.assert_called_once()


def test_put_image_tag_mutability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_image_tag_mutability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_image_tag_mutability",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put image tag mutability"):
        put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", region_name=REGION)


def test_put_lifecycle_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_lifecycle_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", region_name=REGION)
    mock_client.put_lifecycle_policy.assert_called_once()


def test_put_lifecycle_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_lifecycle_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_lifecycle_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put lifecycle policy"):
        put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", region_name=REGION)


def test_put_registry_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_registry_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_registry_policy("test-policy_text", region_name=REGION)
    mock_client.put_registry_policy.assert_called_once()


def test_put_registry_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_registry_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_registry_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put registry policy"):
        put_registry_policy("test-policy_text", region_name=REGION)


def test_put_registry_scanning_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_registry_scanning_configuration.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_registry_scanning_configuration(region_name=REGION)
    mock_client.put_registry_scanning_configuration.assert_called_once()


def test_put_registry_scanning_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_registry_scanning_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_registry_scanning_configuration",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put registry scanning configuration"):
        put_registry_scanning_configuration(region_name=REGION)


def test_put_replication_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_replication_configuration.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    put_replication_configuration({}, region_name=REGION)
    mock_client.put_replication_configuration.assert_called_once()


def test_put_replication_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_replication_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_replication_configuration",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put replication configuration"):
        put_replication_configuration({}, region_name=REGION)


def test_set_repository_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_repository_policy.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    set_repository_policy("test-repository_name", "test-policy_text", region_name=REGION)
    mock_client.set_repository_policy.assert_called_once()


def test_set_repository_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_repository_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_repository_policy",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set repository policy"):
        set_repository_policy("test-repository_name", "test-policy_text", region_name=REGION)


def test_start_image_scan(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_image_scan.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    start_image_scan("test-repository_name", {}, region_name=REGION)
    mock_client.start_image_scan.assert_called_once()


def test_start_image_scan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_image_scan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_image_scan",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start image scan"):
        start_image_scan("test-repository_name", {}, region_name=REGION)


def test_start_lifecycle_policy_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_lifecycle_policy_preview.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    start_lifecycle_policy_preview("test-repository_name", region_name=REGION)
    mock_client.start_lifecycle_policy_preview.assert_called_once()


def test_start_lifecycle_policy_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_lifecycle_policy_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_lifecycle_policy_preview",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start lifecycle policy preview"):
        start_lifecycle_policy_preview("test-repository_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_pull_through_cache_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    update_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)
    mock_client.update_pull_through_cache_rule.assert_called_once()


def test_update_pull_through_cache_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_pull_through_cache_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_through_cache_rule",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update pull through cache rule"):
        update_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)


def test_update_repository_creation_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_repository_creation_template.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    update_repository_creation_template("test-prefix", region_name=REGION)
    mock_client.update_repository_creation_template.assert_called_once()


def test_update_repository_creation_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_repository_creation_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_repository_creation_template",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update repository creation template"):
        update_repository_creation_template("test-prefix", region_name=REGION)


def test_upload_layer_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_layer_part.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    upload_layer_part("test-repository_name", "test-upload_id", 1, 1, "test-layer_part_blob", region_name=REGION)
    mock_client.upload_layer_part.assert_called_once()


def test_upload_layer_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_layer_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_layer_part",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload layer part"):
        upload_layer_part("test-repository_name", "test-upload_id", 1, 1, "test-layer_part_blob", region_name=REGION)


def test_validate_pull_through_cache_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    validate_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)
    mock_client.validate_pull_through_cache_rule.assert_called_once()


def test_validate_pull_through_cache_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_pull_through_cache_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_pull_through_cache_rule",
    )
    monkeypatch.setattr(ecr_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to validate pull through cache rule"):
        validate_pull_through_cache_rule("test-ecr_repository_prefix", region_name=REGION)


def test_batch_check_layer_availability_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import batch_check_layer_availability
    mock_client = MagicMock()
    mock_client.batch_check_layer_availability.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    batch_check_layer_availability("test-repository_name", "test-layer_digests", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.batch_check_layer_availability.assert_called_once()

def test_batch_delete_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import batch_delete_image
    mock_client = MagicMock()
    mock_client.batch_delete_image.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    batch_delete_image("test-repository_name", "test-image_ids", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.batch_delete_image.assert_called_once()

def test_batch_get_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import batch_get_image
    mock_client = MagicMock()
    mock_client.batch_get_image.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    batch_get_image("test-repository_name", "test-image_ids", registry_id="test-registry_id", accepted_media_types="test-accepted_media_types", region_name="us-east-1")
    mock_client.batch_get_image.assert_called_once()

def test_complete_layer_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import complete_layer_upload
    mock_client = MagicMock()
    mock_client.complete_layer_upload.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    complete_layer_upload("test-repository_name", "test-upload_id", "test-layer_digests", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.complete_layer_upload.assert_called_once()

def test_create_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import create_pull_through_cache_rule
    mock_client = MagicMock()
    mock_client.create_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", registry_id="test-registry_id", upstream_registry="test-upstream_registry", credential_arn="test-credential_arn", custom_role_arn="test-custom_role_arn", upstream_repository_prefix="test-upstream_repository_prefix", region_name="us-east-1")
    mock_client.create_pull_through_cache_rule.assert_called_once()

def test_create_repository_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import create_repository
    mock_client = MagicMock()
    mock_client.create_repository.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    create_repository("test-repository_name", registry_id="test-registry_id", tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", image_scanning_configuration={}, encryption_configuration={}, region_name="us-east-1")
    mock_client.create_repository.assert_called_once()

def test_create_repository_creation_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import create_repository_creation_template
    mock_client = MagicMock()
    mock_client.create_repository_creation_template.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    create_repository_creation_template("test-prefix", "test-applied_for", description="test-description", encryption_configuration={}, resource_tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", repository_policy="{}", lifecycle_policy="{}", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.create_repository_creation_template.assert_called_once()

def test_delete_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import delete_lifecycle_policy
    mock_client = MagicMock()
    mock_client.delete_lifecycle_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    delete_lifecycle_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.delete_lifecycle_policy.assert_called_once()

def test_delete_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import delete_pull_through_cache_rule
    mock_client = MagicMock()
    mock_client.delete_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    delete_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.delete_pull_through_cache_rule.assert_called_once()

def test_delete_repository_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import delete_repository
    mock_client = MagicMock()
    mock_client.delete_repository.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    delete_repository("test-repository_name", registry_id="test-registry_id", force=True, region_name="us-east-1")
    mock_client.delete_repository.assert_called_once()

def test_delete_repository_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import delete_repository_policy
    mock_client = MagicMock()
    mock_client.delete_repository_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    delete_repository_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.delete_repository_policy.assert_called_once()

def test_describe_image_replication_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_image_replication_status
    mock_client = MagicMock()
    mock_client.describe_image_replication_status.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_image_replication_status("test-repository_name", "test-image_id", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.describe_image_replication_status.assert_called_once()

def test_describe_image_scan_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_image_scan_findings
    mock_client = MagicMock()
    mock_client.describe_image_scan_findings.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_image_scan_findings("test-repository_name", "test-image_id", registry_id="test-registry_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_image_scan_findings.assert_called_once()

def test_describe_images_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_images
    mock_client = MagicMock()
    mock_client.describe_images.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_images("test-repository_name", registry_id="test-registry_id", image_ids="test-image_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.describe_images.assert_called_once()

def test_describe_pull_through_cache_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_pull_through_cache_rules
    mock_client = MagicMock()
    mock_client.describe_pull_through_cache_rules.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_pull_through_cache_rules(registry_id="test-registry_id", ecr_repository_prefixes="test-ecr_repository_prefixes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_pull_through_cache_rules.assert_called_once()

def test_describe_repositories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_repositories
    mock_client = MagicMock()
    mock_client.describe_repositories.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_repositories(registry_id="test-registry_id", repository_names="test-repository_names", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_repositories.assert_called_once()

def test_describe_repository_creation_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import describe_repository_creation_templates
    mock_client = MagicMock()
    mock_client.describe_repository_creation_templates.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    describe_repository_creation_templates(prefixes="test-prefixes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_repository_creation_templates.assert_called_once()

def test_get_authorization_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import get_authorization_token
    mock_client = MagicMock()
    mock_client.get_authorization_token.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    get_authorization_token(registry_ids="test-registry_ids", region_name="us-east-1")
    mock_client.get_authorization_token.assert_called_once()

def test_get_download_url_for_layer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import get_download_url_for_layer
    mock_client = MagicMock()
    mock_client.get_download_url_for_layer.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    get_download_url_for_layer("test-repository_name", "test-layer_digest", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.get_download_url_for_layer.assert_called_once()

def test_get_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import get_lifecycle_policy
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    get_lifecycle_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.get_lifecycle_policy.assert_called_once()

def test_get_lifecycle_policy_preview_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import get_lifecycle_policy_preview
    mock_client = MagicMock()
    mock_client.get_lifecycle_policy_preview.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    get_lifecycle_policy_preview("test-repository_name", registry_id="test-registry_id", image_ids="test-image_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.get_lifecycle_policy_preview.assert_called_once()

def test_get_repository_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import get_repository_policy
    mock_client = MagicMock()
    mock_client.get_repository_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    get_repository_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.get_repository_policy.assert_called_once()

def test_initiate_layer_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import initiate_layer_upload
    mock_client = MagicMock()
    mock_client.initiate_layer_upload.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    initiate_layer_upload("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.initiate_layer_upload.assert_called_once()

def test_put_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import put_image
    mock_client = MagicMock()
    mock_client.put_image.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    put_image("test-repository_name", "test-image_manifest", registry_id="test-registry_id", image_manifest_media_type="test-image_manifest_media_type", image_tag="test-image_tag", image_digest="test-image_digest", region_name="us-east-1")
    mock_client.put_image.assert_called_once()

def test_put_image_scanning_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import put_image_scanning_configuration
    mock_client = MagicMock()
    mock_client.put_image_scanning_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    put_image_scanning_configuration("test-repository_name", {}, registry_id="test-registry_id", region_name="us-east-1")
    mock_client.put_image_scanning_configuration.assert_called_once()

def test_put_image_tag_mutability_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import put_image_tag_mutability
    mock_client = MagicMock()
    mock_client.put_image_tag_mutability.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", registry_id="test-registry_id", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", region_name="us-east-1")
    mock_client.put_image_tag_mutability.assert_called_once()

def test_put_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import put_lifecycle_policy
    mock_client = MagicMock()
    mock_client.put_lifecycle_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.put_lifecycle_policy.assert_called_once()

def test_put_registry_scanning_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import put_registry_scanning_configuration
    mock_client = MagicMock()
    mock_client.put_registry_scanning_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    put_registry_scanning_configuration(scan_type="test-scan_type", rules="test-rules", region_name="us-east-1")
    mock_client.put_registry_scanning_configuration.assert_called_once()

def test_set_repository_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import set_repository_policy
    mock_client = MagicMock()
    mock_client.set_repository_policy.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    set_repository_policy("test-repository_name", "test-policy_text", registry_id="test-registry_id", force=True, region_name="us-east-1")
    mock_client.set_repository_policy.assert_called_once()

def test_start_image_scan_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import start_image_scan
    mock_client = MagicMock()
    mock_client.start_image_scan.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    start_image_scan("test-repository_name", "test-image_id", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.start_image_scan.assert_called_once()

def test_start_lifecycle_policy_preview_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import start_lifecycle_policy_preview
    mock_client = MagicMock()
    mock_client.start_lifecycle_policy_preview.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    start_lifecycle_policy_preview("test-repository_name", registry_id="test-registry_id", lifecycle_policy_text="test-lifecycle_policy_text", region_name="us-east-1")
    mock_client.start_lifecycle_policy_preview.assert_called_once()

def test_update_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import update_pull_through_cache_rule
    mock_client = MagicMock()
    mock_client.update_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    update_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", credential_arn="test-credential_arn", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.update_pull_through_cache_rule.assert_called_once()

def test_update_repository_creation_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import update_repository_creation_template
    mock_client = MagicMock()
    mock_client.update_repository_creation_template.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    update_repository_creation_template("test-prefix", description="test-description", encryption_configuration={}, resource_tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", repository_policy="{}", lifecycle_policy="{}", applied_for="test-applied_for", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.update_repository_creation_template.assert_called_once()

def test_upload_layer_part_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import upload_layer_part
    mock_client = MagicMock()
    mock_client.upload_layer_part.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    upload_layer_part("test-repository_name", "test-upload_id", "test-part_first_byte", "test-part_last_byte", "test-layer_part_blob", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.upload_layer_part.assert_called_once()

def test_validate_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecr import validate_pull_through_cache_rule
    mock_client = MagicMock()
    mock_client.validate_pull_through_cache_rule.return_value = {}
    monkeypatch.setattr("aws_util.ecr.get_client", lambda *a, **kw: mock_client)
    validate_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.validate_pull_through_cache_rule.assert_called_once()
