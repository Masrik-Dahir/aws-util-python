"""Tests for aws_util.aio.ecr — 100 % line coverage."""
from __future__ import annotations

import base64
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.ecr import (
    ECRAuthToken,
    ECRImage,
    ECRRepository,
    describe_repository,
    ensure_repository,
    get_auth_token,
    get_latest_image_tag,
    list_images,
    list_repositories,
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _repo_dict(
    name: str = "my-repo",
    mutability: str = "MUTABLE",
) -> dict:
    return {
        "repositoryName": name,
        "repositoryArn": f"arn:aws:ecr:us-east-1:123:repository/{name}",
        "repositoryUri": f"123.dkr.ecr.us-east-1.amazonaws.com/{name}",
        "registryId": "123456789012",
        "createdAt": datetime(2024, 1, 1, tzinfo=timezone.utc),
        "imageTagMutability": mutability,
    }


def _image_detail_dict(
    digest: str = "sha256:abc123",
    tags: list[str] | None = None,
    pushed_at: datetime | None = None,
    size: int = 1024,
) -> dict:
    d: dict = {
        "registryId": "123456789012",
        "repositoryName": "my-repo",
        "imageDigest": digest,
    }
    if tags is not None:
        d["imageTags"] = tags
    if pushed_at is not None:
        d["imagePushedAt"] = pushed_at
    if size is not None:
        d["imageSizeInBytes"] = size
    return d


# ---------------------------------------------------------------------------
# get_auth_token
# ---------------------------------------------------------------------------


async def test_get_auth_token_success(monkeypatch):
    token_b64 = base64.b64encode(b"AWS:secret-password").decode()
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "authorizationData": [
            {
                "authorizationToken": token_b64,
                "proxyEndpoint": "https://123.dkr.ecr.us-east-1.amazonaws.com",
                "expiresAt": datetime(2024, 12, 31, tzinfo=timezone.utc),
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_auth_token(registry_ids=["123456789012"])
    assert len(result) == 1
    assert result[0].username == "AWS"
    assert result[0].password == "secret-password"
    assert result[0].endpoint == "https://123.dkr.ecr.us-east-1.amazonaws.com"


async def test_get_auth_token_no_registry_ids(monkeypatch):
    token_b64 = base64.b64encode(b"AWS:pw").decode()
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "authorizationData": [
            {
                "authorizationToken": token_b64,
                "proxyEndpoint": "https://endpoint",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_auth_token()
    assert len(result) == 1
    # No registryIds passed
    call_kwargs = mock_client.call.call_args[1]
    assert "registryIds" not in call_kwargs


async def test_get_auth_token_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"authorizationData": []}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_auth_token()
    assert result == []


async def test_get_auth_token_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="denied"):
        await get_auth_token()


async def test_get_auth_token_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="get_auth_token failed"):
        await get_auth_token()


# ---------------------------------------------------------------------------
# list_repositories
# ---------------------------------------------------------------------------


async def test_list_repositories_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositories": [_repo_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_repositories()
    assert len(result) == 1
    assert result[0].repository_name == "my-repo"


async def test_list_repositories_with_registry_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositories": [_repo_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_repositories(registry_id="123")
    assert len(result) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["registryId"] == "123"


async def test_list_repositories_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "repositories": [_repo_dict("repo-1")],
            "nextToken": "tok1",
        },
        {
            "repositories": [_repo_dict("repo-2")],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_repositories()
    assert len(result) == 2
    assert result[0].repository_name == "repo-1"
    assert result[1].repository_name == "repo-2"


async def test_list_repositories_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositories": []}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_repositories()
    assert result == []


async def test_list_repositories_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_repositories()


async def test_list_repositories_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_repositories failed"):
        await list_repositories()


# ---------------------------------------------------------------------------
# describe_repository
# ---------------------------------------------------------------------------


async def test_describe_repository_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositories": [_repo_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await describe_repository("my-repo")
    assert result is not None
    assert result.repository_name == "my-repo"


async def test_describe_repository_with_registry_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositories": [_repo_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await describe_repository("my-repo", registry_id="123")
    assert result is not None
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["registryId"] == "123"


async def test_describe_repository_not_found_exception(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "RepositoryNotFoundException: not found"
    )
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await describe_repository("nope")
    assert result is None


async def test_describe_repository_not_found_empty_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositories": []}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await describe_repository("nope")
    assert result is None


async def test_describe_repository_runtime_error_other(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("some other error")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="some other error"):
        await describe_repository("my-repo")


# ---------------------------------------------------------------------------
# list_images
# ---------------------------------------------------------------------------


async def test_list_images_success(monkeypatch):
    mock_client = AsyncMock()
    now = datetime(2024, 6, 1, tzinfo=timezone.utc)
    mock_client.call.side_effect = [
        # ListImages response
        {
            "imageIds": [
                {"imageDigest": "sha256:abc", "imageTag": "v1"}
            ]
        },
        # DescribeImages response
        {
            "imageDetails": [
                _image_detail_dict(
                    digest="sha256:abc",
                    tags=["v1"],
                    pushed_at=now,
                )
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo")
    assert len(result) == 1
    assert result[0].image_digest == "sha256:abc"
    assert result[0].image_tags == ["v1"]


async def test_list_images_with_registry_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:x"}]},
        {"imageDetails": [_image_detail_dict()]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo", registry_id="123")
    assert len(result) == 1


async def test_list_images_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"imageIds": []}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo")
    assert result == []


async def test_list_images_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        # First page of ListImages
        {
            "imageIds": [{"imageDigest": "sha256:a"}],
            "nextToken": "tok1",
        },
        # Second page of ListImages
        {
            "imageIds": [{"imageDigest": "sha256:b"}],
        },
        # DescribeImages batch
        {
            "imageDetails": [
                _image_detail_dict(digest="sha256:a"),
                _image_detail_dict(digest="sha256:b"),
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo")
    assert len(result) == 2


async def test_list_images_describe_batching(monkeypatch):
    """Verify images are described in batches of 100."""
    mock_client = AsyncMock()
    # ListImages returns 101 image IDs
    image_ids = [{"imageDigest": f"sha256:{i}"} for i in range(101)]
    mock_client.call.side_effect = [
        # ListImages
        {"imageIds": image_ids},
        # First DescribeImages batch (100)
        {
            "imageDetails": [
                _image_detail_dict(digest=f"sha256:{i}")
                for i in range(100)
            ]
        },
        # Second DescribeImages batch (1)
        {
            "imageDetails": [_image_detail_dict(digest="sha256:100")]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo")
    assert len(result) == 101


async def test_list_images_runtime_error_on_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("list err")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list err"):
        await list_images("my-repo")


async def test_list_images_generic_error_on_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("val")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_images failed"):
        await list_images("my-repo")


async def test_list_images_runtime_error_on_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:abc"}]},
        RuntimeError("desc err"),
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="desc err"):
        await list_images("my-repo")


async def test_list_images_generic_error_on_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:abc"}]},
        TypeError("type"),
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_images failed"):
        await list_images("my-repo")


async def test_list_images_no_tags_no_pushed_at_no_size(monkeypatch):
    """Image detail without optional fields."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:x"}]},
        {
            "imageDetails": [
                {
                    "registryId": "123",
                    "repositoryName": "my-repo",
                    "imageDigest": "sha256:x",
                }
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await list_images("my-repo")
    assert len(result) == 1
    assert result[0].image_tags == []
    assert result[0].image_pushed_at is None
    assert result[0].image_size_bytes is None


# ---------------------------------------------------------------------------
# ensure_repository
# ---------------------------------------------------------------------------


async def test_ensure_repository_existing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositories": [_repo_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await ensure_repository("my-repo")
    assert result.repository_name == "my-repo"
    # Only describe_repository called, not create
    assert mock_client.call.await_count == 1


async def test_ensure_repository_create_new(monkeypatch):
    mock_client = AsyncMock()
    # describe_repository: RepositoryNotFoundException
    # create_repository: success
    mock_client.call.side_effect = [
        RuntimeError("RepositoryNotFoundException: not found"),
        {
            "repository": _repo_dict("new-repo")
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await ensure_repository(
        "new-repo",
        image_tag_mutability="IMMUTABLE",
        scan_on_push=True,
    )
    assert result.repository_name == "new-repo"


async def test_ensure_repository_create_no_optional_fields(monkeypatch):
    """Created repo dict without createdAt/imageTagMutability."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        RuntimeError("RepositoryNotFoundException: not found"),
        {
            "repository": {
                "repositoryName": "r",
                "repositoryArn": "arn:r",
                "repositoryUri": "uri/r",
                "registryId": "123",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await ensure_repository("r")
    assert result.created_at is None
    assert result.image_tag_mutability == "MUTABLE"


async def test_ensure_repository_create_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        RuntimeError("RepositoryNotFoundException: not found"),
        RuntimeError("create failed"),
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create failed"):
        await ensure_repository("my-repo")


async def test_ensure_repository_create_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        RuntimeError("RepositoryNotFoundException: not found"),
        ValueError("val"),
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to create ECR repository"):
        await ensure_repository("my-repo")


# ---------------------------------------------------------------------------
# get_latest_image_tag
# ---------------------------------------------------------------------------


async def test_get_latest_image_tag_found(monkeypatch):
    now = datetime(2024, 6, 1, tzinfo=timezone.utc)
    older = datetime(2024, 1, 1, tzinfo=timezone.utc)
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        # ListImages
        {
            "imageIds": [
                {"imageDigest": "sha256:a", "imageTag": "v1"},
                {"imageDigest": "sha256:b", "imageTag": "v2"},
            ]
        },
        # DescribeImages
        {
            "imageDetails": [
                _image_detail_dict(
                    digest="sha256:a",
                    tags=["v1"],
                    pushed_at=older,
                ),
                _image_detail_dict(
                    digest="sha256:b",
                    tags=["v2"],
                    pushed_at=now,
                ),
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_image_tag("my-repo")
    assert result == "v2"


async def test_get_latest_image_tag_no_tagged(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"imageIds": []}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_image_tag("my-repo")
    assert result is None


async def test_get_latest_image_tag_no_pushed_at(monkeypatch):
    """Images without pushed_at are excluded from the tagged list."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:a"}]},
        {
            "imageDetails": [
                {
                    "registryId": "123",
                    "repositoryName": "my-repo",
                    "imageDigest": "sha256:a",
                    "imageTags": ["latest"],
                    # No imagePushedAt
                }
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_image_tag("my-repo")
    assert result is None


async def test_get_latest_image_tag_no_tags(monkeypatch):
    """Images without tags are excluded from the tagged list."""
    now = datetime(2024, 6, 1, tzinfo=timezone.utc)
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:a"}]},
        {
            "imageDetails": [
                {
                    "registryId": "123",
                    "repositoryName": "my-repo",
                    "imageDigest": "sha256:a",
                    "imagePushedAt": now,
                    # No imageTags
                }
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_image_tag("my-repo")
    assert result is None


async def test_get_latest_image_tag_with_region(monkeypatch):
    now = datetime(2024, 6, 1, tzinfo=timezone.utc)
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"imageIds": [{"imageDigest": "sha256:a", "imageTag": "v1"}]},
        {
            "imageDetails": [
                _image_detail_dict(
                    digest="sha256:a", tags=["v1"], pushed_at=now
                )
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_image_tag(
        "my-repo", region_name="eu-west-1"
    )
    assert result == "v1"


async def test_batch_check_layer_availability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_check_layer_availability("test-repository_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_check_layer_availability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_check_layer_availability("test-repository_name", [], )


async def test_batch_delete_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_image("test-repository_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_image("test-repository_name", [], )


async def test_batch_get_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_image("test-repository_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_image("test-repository_name", [], )


async def test_batch_get_repository_scanning_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_repository_scanning_configuration([], )
    mock_client.call.assert_called_once()


async def test_batch_get_repository_scanning_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_repository_scanning_configuration([], )


async def test_complete_layer_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await complete_layer_upload("test-repository_name", "test-upload_id", [], )
    mock_client.call.assert_called_once()


async def test_complete_layer_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await complete_layer_upload("test-repository_name", "test-upload_id", [], )


async def test_create_pull_through_cache_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", )
    mock_client.call.assert_called_once()


async def test_create_pull_through_cache_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", )


async def test_create_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_repository("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_create_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_repository("test-repository_name", )


async def test_create_repository_creation_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_repository_creation_template("test-prefix", [], )
    mock_client.call.assert_called_once()


async def test_create_repository_creation_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_repository_creation_template("test-prefix", [], )


async def test_delete_lifecycle_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_lifecycle_policy("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_delete_lifecycle_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_lifecycle_policy("test-repository_name", )


async def test_delete_pull_through_cache_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_pull_through_cache_rule("test-ecr_repository_prefix", )
    mock_client.call.assert_called_once()


async def test_delete_pull_through_cache_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_pull_through_cache_rule("test-ecr_repository_prefix", )


async def test_delete_registry_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_registry_policy()
    mock_client.call.assert_called_once()


async def test_delete_registry_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_registry_policy()


async def test_delete_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_repository("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_delete_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository("test-repository_name", )


async def test_delete_repository_creation_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_repository_creation_template("test-prefix", )
    mock_client.call.assert_called_once()


async def test_delete_repository_creation_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository_creation_template("test-prefix", )


async def test_delete_repository_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_repository_policy("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_delete_repository_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository_policy("test-repository_name", )


async def test_describe_image_replication_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_replication_status("test-repository_name", {}, )
    mock_client.call.assert_called_once()


async def test_describe_image_replication_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_replication_status("test-repository_name", {}, )


async def test_describe_image_scan_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_scan_findings("test-repository_name", {}, )
    mock_client.call.assert_called_once()


async def test_describe_image_scan_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_scan_findings("test-repository_name", {}, )


async def test_describe_images(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_images("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_describe_images_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_images("test-repository_name", )


async def test_describe_pull_through_cache_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pull_through_cache_rules()
    mock_client.call.assert_called_once()


async def test_describe_pull_through_cache_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pull_through_cache_rules()


async def test_describe_registry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_registry()
    mock_client.call.assert_called_once()


async def test_describe_registry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_registry()


async def test_describe_repositories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_repositories()
    mock_client.call.assert_called_once()


async def test_describe_repositories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_repositories()


async def test_describe_repository_creation_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_repository_creation_templates()
    mock_client.call.assert_called_once()


async def test_describe_repository_creation_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_repository_creation_templates()


async def test_get_account_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_setting("test-name", )
    mock_client.call.assert_called_once()


async def test_get_account_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_setting("test-name", )


async def test_get_authorization_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_authorization_token()
    mock_client.call.assert_called_once()


async def test_get_authorization_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_authorization_token()


async def test_get_download_url_for_layer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_download_url_for_layer("test-repository_name", "test-layer_digest", )
    mock_client.call.assert_called_once()


async def test_get_download_url_for_layer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_download_url_for_layer("test-repository_name", "test-layer_digest", )


async def test_get_lifecycle_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_lifecycle_policy("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_get_lifecycle_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_lifecycle_policy("test-repository_name", )


async def test_get_lifecycle_policy_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_lifecycle_policy_preview("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_get_lifecycle_policy_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_lifecycle_policy_preview("test-repository_name", )


async def test_get_registry_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_registry_policy()
    mock_client.call.assert_called_once()


async def test_get_registry_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_registry_policy()


async def test_get_registry_scanning_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_registry_scanning_configuration()
    mock_client.call.assert_called_once()


async def test_get_registry_scanning_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_registry_scanning_configuration()


async def test_get_repository_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_repository_policy("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_get_repository_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository_policy("test-repository_name", )


async def test_initiate_layer_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await initiate_layer_upload("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_initiate_layer_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await initiate_layer_upload("test-repository_name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_account_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_account_setting("test-name", "test-value", )
    mock_client.call.assert_called_once()


async def test_put_account_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_setting("test-name", "test-value", )


async def test_put_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_image("test-repository_name", "test-image_manifest", )
    mock_client.call.assert_called_once()


async def test_put_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_image("test-repository_name", "test-image_manifest", )


async def test_put_image_scanning_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_image_scanning_configuration("test-repository_name", {}, )
    mock_client.call.assert_called_once()


async def test_put_image_scanning_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_image_scanning_configuration("test-repository_name", {}, )


async def test_put_image_tag_mutability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", )
    mock_client.call.assert_called_once()


async def test_put_image_tag_mutability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", )


async def test_put_lifecycle_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", )
    mock_client.call.assert_called_once()


async def test_put_lifecycle_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", )


async def test_put_registry_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_registry_policy("test-policy_text", )
    mock_client.call.assert_called_once()


async def test_put_registry_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_registry_policy("test-policy_text", )


async def test_put_registry_scanning_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_registry_scanning_configuration()
    mock_client.call.assert_called_once()


async def test_put_registry_scanning_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_registry_scanning_configuration()


async def test_put_replication_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_replication_configuration({}, )
    mock_client.call.assert_called_once()


async def test_put_replication_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_replication_configuration({}, )


async def test_set_repository_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_repository_policy("test-repository_name", "test-policy_text", )
    mock_client.call.assert_called_once()


async def test_set_repository_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_repository_policy("test-repository_name", "test-policy_text", )


async def test_start_image_scan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_image_scan("test-repository_name", {}, )
    mock_client.call.assert_called_once()


async def test_start_image_scan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_image_scan("test-repository_name", {}, )


async def test_start_lifecycle_policy_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_lifecycle_policy_preview("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_start_lifecycle_policy_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_lifecycle_policy_preview("test-repository_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_pull_through_cache_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_through_cache_rule("test-ecr_repository_prefix", )
    mock_client.call.assert_called_once()


async def test_update_pull_through_cache_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_through_cache_rule("test-ecr_repository_prefix", )


async def test_update_repository_creation_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_repository_creation_template("test-prefix", )
    mock_client.call.assert_called_once()


async def test_update_repository_creation_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository_creation_template("test-prefix", )


async def test_upload_layer_part(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_layer_part("test-repository_name", "test-upload_id", 1, 1, "test-layer_part_blob", )
    mock_client.call.assert_called_once()


async def test_upload_layer_part_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_layer_part("test-repository_name", "test-upload_id", 1, 1, "test-layer_part_blob", )


async def test_validate_pull_through_cache_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_pull_through_cache_rule("test-ecr_repository_prefix", )
    mock_client.call.assert_called_once()


async def test_validate_pull_through_cache_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_pull_through_cache_rule("test-ecr_repository_prefix", )


@pytest.mark.asyncio
async def test_batch_check_layer_availability_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import batch_check_layer_availability
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await batch_check_layer_availability("test-repository_name", "test-layer_digests", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import batch_delete_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await batch_delete_image("test-repository_name", "test-image_ids", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import batch_get_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await batch_get_image("test-repository_name", "test-image_ids", registry_id="test-registry_id", accepted_media_types="test-accepted_media_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_complete_layer_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import complete_layer_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await complete_layer_upload("test-repository_name", "test-upload_id", "test-layer_digests", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import create_pull_through_cache_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await create_pull_through_cache_rule("test-ecr_repository_prefix", "test-upstream_registry_url", registry_id="test-registry_id", upstream_registry="test-upstream_registry", credential_arn="test-credential_arn", custom_role_arn="test-custom_role_arn", upstream_repository_prefix="test-upstream_repository_prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_repository_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import create_repository
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await create_repository("test-repository_name", registry_id="test-registry_id", tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", image_scanning_configuration={}, encryption_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_repository_creation_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import create_repository_creation_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await create_repository_creation_template("test-prefix", "test-applied_for", description="test-description", encryption_configuration={}, resource_tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", repository_policy="{}", lifecycle_policy="{}", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import delete_lifecycle_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await delete_lifecycle_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import delete_pull_through_cache_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await delete_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_repository_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import delete_repository
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await delete_repository("test-repository_name", registry_id="test-registry_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_repository_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import delete_repository_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await delete_repository_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_image_replication_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_image_replication_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_image_replication_status("test-repository_name", "test-image_id", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_image_scan_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_image_scan_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_image_scan_findings("test-repository_name", "test-image_id", registry_id="test-registry_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_images_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_images
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_images("test-repository_name", registry_id="test-registry_id", image_ids="test-image_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pull_through_cache_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_pull_through_cache_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_pull_through_cache_rules(registry_id="test-registry_id", ecr_repository_prefixes="test-ecr_repository_prefixes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_repositories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_repositories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_repositories(registry_id="test-registry_id", repository_names="test-repository_names", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_repository_creation_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import describe_repository_creation_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await describe_repository_creation_templates(prefixes="test-prefixes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_authorization_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import get_authorization_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await get_authorization_token(registry_ids="test-registry_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_download_url_for_layer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import get_download_url_for_layer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await get_download_url_for_layer("test-repository_name", "test-layer_digest", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import get_lifecycle_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await get_lifecycle_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_lifecycle_policy_preview_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import get_lifecycle_policy_preview
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await get_lifecycle_policy_preview("test-repository_name", registry_id="test-registry_id", image_ids="test-image_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_repository_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import get_repository_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await get_repository_policy("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_initiate_layer_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import initiate_layer_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await initiate_layer_upload("test-repository_name", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import put_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await put_image("test-repository_name", "test-image_manifest", registry_id="test-registry_id", image_manifest_media_type="test-image_manifest_media_type", image_tag="test-image_tag", image_digest="test-image_digest", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_image_scanning_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import put_image_scanning_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await put_image_scanning_configuration("test-repository_name", {}, registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_image_tag_mutability_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import put_image_tag_mutability
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await put_image_tag_mutability("test-repository_name", "test-image_tag_mutability", registry_id="test-registry_id", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_lifecycle_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import put_lifecycle_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await put_lifecycle_policy("test-repository_name", "test-lifecycle_policy_text", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_registry_scanning_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import put_registry_scanning_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await put_registry_scanning_configuration(scan_type="test-scan_type", rules="test-rules", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_repository_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import set_repository_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await set_repository_policy("test-repository_name", "test-policy_text", registry_id="test-registry_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_image_scan_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import start_image_scan
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await start_image_scan("test-repository_name", "test-image_id", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_lifecycle_policy_preview_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import start_lifecycle_policy_preview
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await start_lifecycle_policy_preview("test-repository_name", registry_id="test-registry_id", lifecycle_policy_text="test-lifecycle_policy_text", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import update_pull_through_cache_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await update_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", credential_arn="test-credential_arn", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_repository_creation_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import update_repository_creation_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await update_repository_creation_template("test-prefix", description="test-description", encryption_configuration={}, resource_tags=[{"Key": "k", "Value": "v"}], image_tag_mutability="test-image_tag_mutability", image_tag_mutability_exclusion_filters="test-image_tag_mutability_exclusion_filters", repository_policy="{}", lifecycle_policy="{}", applied_for="test-applied_for", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_upload_layer_part_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import upload_layer_part
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await upload_layer_part("test-repository_name", "test-upload_id", "test-part_first_byte", "test-part_last_byte", "test-layer_part_blob", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_pull_through_cache_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecr import validate_pull_through_cache_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecr.async_client", lambda *a, **kw: mock_client)
    await validate_pull_through_cache_rule("test-ecr_repository_prefix", registry_id="test-registry_id", region_name="us-east-1")
    mock_client.call.assert_called_once()
