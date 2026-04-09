from __future__ import annotations

from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchCheckLayerAvailabilityResult",
    "BatchDeleteImageResult",
    "BatchGetImageResult",
    "BatchGetRepositoryScanningConfigurationResult",
    "CompleteLayerUploadResult",
    "CreatePullThroughCacheRuleResult",
    "CreateRepositoryCreationTemplateResult",
    "CreateRepositoryResult",
    "DeleteLifecyclePolicyResult",
    "DeletePullThroughCacheRuleResult",
    "DeleteRegistryPolicyResult",
    "DeleteRepositoryCreationTemplateResult",
    "DeleteRepositoryPolicyResult",
    "DeleteRepositoryResult",
    "DescribeImageReplicationStatusResult",
    "DescribeImageScanFindingsResult",
    "DescribeImagesResult",
    "DescribePullThroughCacheRulesResult",
    "DescribeRegistryResult",
    "DescribeRepositoriesResult",
    "DescribeRepositoryCreationTemplatesResult",
    "ECRAuthToken",
    "ECRImage",
    "ECRRepository",
    "GetAccountSettingResult",
    "GetAuthorizationTokenResult",
    "GetDownloadUrlForLayerResult",
    "GetLifecyclePolicyPreviewResult",
    "GetLifecyclePolicyResult",
    "GetRegistryPolicyResult",
    "GetRegistryScanningConfigurationResult",
    "GetRepositoryPolicyResult",
    "InitiateLayerUploadResult",
    "ListTagsForResourceResult",
    "PutAccountSettingResult",
    "PutImageResult",
    "PutImageScanningConfigurationResult",
    "PutImageTagMutabilityResult",
    "PutLifecyclePolicyResult",
    "PutRegistryPolicyResult",
    "PutRegistryScanningConfigurationResult",
    "PutReplicationConfigurationResult",
    "SetRepositoryPolicyResult",
    "StartImageScanResult",
    "StartLifecyclePolicyPreviewResult",
    "UpdatePullThroughCacheRuleResult",
    "UpdateRepositoryCreationTemplateResult",
    "UploadLayerPartResult",
    "ValidatePullThroughCacheRuleResult",
    "batch_check_layer_availability",
    "batch_delete_image",
    "batch_get_image",
    "batch_get_repository_scanning_configuration",
    "complete_layer_upload",
    "create_pull_through_cache_rule",
    "create_repository",
    "create_repository_creation_template",
    "delete_lifecycle_policy",
    "delete_pull_through_cache_rule",
    "delete_registry_policy",
    "delete_repository",
    "delete_repository_creation_template",
    "delete_repository_policy",
    "describe_image_replication_status",
    "describe_image_scan_findings",
    "describe_images",
    "describe_pull_through_cache_rules",
    "describe_registry",
    "describe_repositories",
    "describe_repository",
    "describe_repository_creation_templates",
    "ensure_repository",
    "get_account_setting",
    "get_auth_token",
    "get_authorization_token",
    "get_download_url_for_layer",
    "get_latest_image_tag",
    "get_lifecycle_policy",
    "get_lifecycle_policy_preview",
    "get_registry_policy",
    "get_registry_scanning_configuration",
    "get_repository_policy",
    "initiate_layer_upload",
    "list_images",
    "list_repositories",
    "list_tags_for_resource",
    "put_account_setting",
    "put_image",
    "put_image_scanning_configuration",
    "put_image_tag_mutability",
    "put_lifecycle_policy",
    "put_registry_policy",
    "put_registry_scanning_configuration",
    "put_replication_configuration",
    "set_repository_policy",
    "start_image_scan",
    "start_lifecycle_policy_preview",
    "tag_resource",
    "untag_resource",
    "update_pull_through_cache_rule",
    "update_repository_creation_template",
    "upload_layer_part",
    "validate_pull_through_cache_rule",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ECRRepository(BaseModel):
    """Metadata for an ECR repository."""

    model_config = ConfigDict(frozen=True)

    repository_name: str
    repository_arn: str
    repository_uri: str
    registry_id: str
    created_at: datetime | None = None
    image_tag_mutability: str = "MUTABLE"


class ECRImage(BaseModel):
    """Metadata for an image stored in an ECR repository."""

    model_config = ConfigDict(frozen=True)

    registry_id: str
    repository_name: str
    image_digest: str
    image_tags: list[str] = []
    image_pushed_at: datetime | None = None
    image_size_bytes: int | None = None


class ECRAuthToken(BaseModel):
    """Docker registry authentication token from ECR."""

    model_config = ConfigDict(frozen=True)

    endpoint: str
    username: str
    password: str
    expires_at: datetime | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_auth_token(
    registry_ids: list[str] | None = None,
    region_name: str | None = None,
) -> list[ECRAuthToken]:
    """Retrieve ECR Docker authorization tokens.

    The returned credentials can be used with ``docker login`` to pull or push
    images to the registry.

    Args:
        registry_ids: Specific registry account IDs.  ``None`` returns a
            token for the caller's default registry.
        region_name: AWS region override.

    Returns:
        A list of :class:`ECRAuthToken` objects (one per registry).

    Raises:
        RuntimeError: If the API call fails.
    """
    import base64

    client = get_client("ecr", region_name)
    kwargs: dict = {}
    if registry_ids:
        kwargs["registryIds"] = registry_ids
    try:
        resp = client.get_authorization_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_auth_token failed") from exc

    tokens: list[ECRAuthToken] = []
    for auth in resp.get("authorizationData", []):
        decoded = base64.b64decode(auth["authorizationToken"]).decode("utf-8")
        username, password = decoded.split(":", 1)
        tokens.append(
            ECRAuthToken(
                endpoint=auth["proxyEndpoint"],
                username=username,
                password=password,
                expires_at=auth.get("expiresAt"),
            )
        )
    return tokens


def list_repositories(
    registry_id: str | None = None,
    region_name: str | None = None,
) -> list[ECRRepository]:
    """List ECR repositories in the account.

    Args:
        registry_id: Target registry account ID.  Defaults to the caller's
            account.
        region_name: AWS region override.

    Returns:
        A list of :class:`ECRRepository` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict = {}
    if registry_id:
        kwargs["registryId"] = registry_id

    repos: list[ECRRepository] = []
    try:
        paginator = client.get_paginator("describe_repositories")
        for page in paginator.paginate(**kwargs):
            for repo in page.get("repositories", []):
                repos.append(
                    ECRRepository(
                        repository_name=repo["repositoryName"],
                        repository_arn=repo["repositoryArn"],
                        repository_uri=repo["repositoryUri"],
                        registry_id=repo["registryId"],
                        created_at=repo.get("createdAt"),
                        image_tag_mutability=repo.get("imageTagMutability", "MUTABLE"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_repositories failed") from exc
    return repos


def describe_repository(
    repository_name: str,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> ECRRepository | None:
    """Fetch metadata for a single ECR repository.

    Args:
        repository_name: Name of the repository.
        registry_id: Registry account ID override.
        region_name: AWS region override.

    Returns:
        An :class:`ECRRepository`, or ``None`` if not found.

    Raises:
        RuntimeError: If the API call fails for a reason other than not found.
    """
    client = get_client("ecr", region_name)
    kwargs: dict = {"repositoryNames": [repository_name]}
    if registry_id:
        kwargs["registryId"] = registry_id
    try:
        resp = client.describe_repositories(**kwargs)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "RepositoryNotFoundException":
            return None
        raise wrap_aws_error(exc, f"describe_repository failed for {repository_name!r}") from exc
    repos = resp.get("repositories", [])
    if not repos:
        return None
    repo = repos[0]
    return ECRRepository(
        repository_name=repo["repositoryName"],
        repository_arn=repo["repositoryArn"],
        repository_uri=repo["repositoryUri"],
        registry_id=repo["registryId"],
        created_at=repo.get("createdAt"),
        image_tag_mutability=repo.get("imageTagMutability", "MUTABLE"),
    )


def list_images(
    repository_name: str,
    registry_id: str | None = None,
    tag_status: str = "ANY",
    region_name: str | None = None,
) -> list[ECRImage]:
    """List images in an ECR repository.

    Args:
        repository_name: Repository name.
        registry_id: Registry account ID override.
        tag_status: ``"TAGGED"``, ``"UNTAGGED"``, or ``"ANY"`` (default).
        region_name: AWS region override.

    Returns:
        A list of :class:`ECRImage` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict = {
        "repositoryName": repository_name,
        "filter": {"tagStatus": tag_status},
    }
    if registry_id:
        kwargs["registryId"] = registry_id

    image_ids: list[dict] = []
    try:
        paginator = client.get_paginator("list_images")
        for page in paginator.paginate(**kwargs):
            image_ids.extend(page.get("imageIds", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_images failed for {repository_name!r}") from exc

    if not image_ids:
        return []

    # Describe in batches of 100
    images: list[ECRImage] = []
    batch_size = 100
    desc_kwargs: dict = {"repositoryName": repository_name}
    if registry_id:
        desc_kwargs["registryId"] = registry_id
    try:
        for i in range(0, len(image_ids), batch_size):
            batch = image_ids[i : i + batch_size]
            desc_resp = client.describe_images(imageIds=batch, **desc_kwargs)
            for detail in desc_resp.get("imageDetails", []):
                images.append(
                    ECRImage(
                        registry_id=detail["registryId"],
                        repository_name=detail["repositoryName"],
                        image_digest=detail["imageDigest"],
                        image_tags=detail.get("imageTags", []),
                        image_pushed_at=detail.get("imagePushedAt"),
                        image_size_bytes=detail.get("imageSizeInBytes"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_images failed for {repository_name!r}") from exc
    return images


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def ensure_repository(
    repository_name: str,
    image_tag_mutability: str = "MUTABLE",
    scan_on_push: bool = False,
    region_name: str | None = None,
) -> ECRRepository:
    """Get an ECR repository, creating it if it does not exist.

    Args:
        repository_name: Repository name.
        image_tag_mutability: ``"MUTABLE"`` (default) or ``"IMMUTABLE"``.
        scan_on_push: Enable automated vulnerability scanning on image push.
        region_name: AWS region override.

    Returns:
        The :class:`ECRRepository` (existing or newly created).

    Raises:
        RuntimeError: If the create or describe call fails.
    """
    existing = describe_repository(repository_name, region_name=region_name)
    if existing is not None:
        return existing

    client = get_client("ecr", region_name)
    try:
        resp = client.create_repository(
            repositoryName=repository_name,
            imageTagMutability=image_tag_mutability,
            imageScanningConfiguration={"scanOnPush": scan_on_push},
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create ECR repository {repository_name!r}") from exc
    repo = resp["repository"]
    return ECRRepository(
        repository_name=repo["repositoryName"],
        repository_arn=repo["repositoryArn"],
        repository_uri=repo["repositoryUri"],
        registry_id=repo["registryId"],
        created_at=repo.get("createdAt"),
        image_tag_mutability=repo.get("imageTagMutability", image_tag_mutability),
    )


def get_latest_image_tag(
    repository_name: str,
    region_name: str | None = None,
) -> str | None:
    """Return the tag of the most recently pushed image in a repository.

    Compares ``imagePushedAt`` timestamps across all tagged images and
    returns the tag of the newest one.

    Args:
        repository_name: Repository name.
        region_name: AWS region override.

    Returns:
        The most recent image tag, or ``None`` if no tagged images exist.

    Raises:
        RuntimeError: If the image list call fails.
    """
    images = list_images(repository_name, tag_status="TAGGED", region_name=region_name)
    tagged = [img for img in images if img.image_pushed_at and img.image_tags]
    if not tagged:
        return None
    latest = max(tagged, key=lambda img: img.image_pushed_at)  # type: ignore[arg-type,return-value]
    return latest.image_tags[0] if latest.image_tags else None


class BatchCheckLayerAvailabilityResult(BaseModel):
    """Result of batch_check_layer_availability."""

    model_config = ConfigDict(frozen=True)

    layers: list[dict[str, Any]] | None = None
    failures: list[dict[str, Any]] | None = None


class BatchDeleteImageResult(BaseModel):
    """Result of batch_delete_image."""

    model_config = ConfigDict(frozen=True)

    image_ids: list[dict[str, Any]] | None = None
    failures: list[dict[str, Any]] | None = None


class BatchGetImageResult(BaseModel):
    """Result of batch_get_image."""

    model_config = ConfigDict(frozen=True)

    images: list[dict[str, Any]] | None = None
    failures: list[dict[str, Any]] | None = None


class BatchGetRepositoryScanningConfigurationResult(BaseModel):
    """Result of batch_get_repository_scanning_configuration."""

    model_config = ConfigDict(frozen=True)

    scanning_configurations: list[dict[str, Any]] | None = None
    failures: list[dict[str, Any]] | None = None


class CompleteLayerUploadResult(BaseModel):
    """Result of complete_layer_upload."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    upload_id: str | None = None
    layer_digest: str | None = None


class CreatePullThroughCacheRuleResult(BaseModel):
    """Result of create_pull_through_cache_rule."""

    model_config = ConfigDict(frozen=True)

    ecr_repository_prefix: str | None = None
    upstream_registry_url: str | None = None
    created_at: str | None = None
    registry_id: str | None = None
    upstream_registry: str | None = None
    credential_arn: str | None = None
    custom_role_arn: str | None = None
    upstream_repository_prefix: str | None = None


class CreateRepositoryResult(BaseModel):
    """Result of create_repository."""

    model_config = ConfigDict(frozen=True)

    repository: dict[str, Any] | None = None


class CreateRepositoryCreationTemplateResult(BaseModel):
    """Result of create_repository_creation_template."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_creation_template: dict[str, Any] | None = None


class DeleteLifecyclePolicyResult(BaseModel):
    """Result of delete_lifecycle_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    lifecycle_policy_text: str | None = None
    last_evaluated_at: str | None = None


class DeletePullThroughCacheRuleResult(BaseModel):
    """Result of delete_pull_through_cache_rule."""

    model_config = ConfigDict(frozen=True)

    ecr_repository_prefix: str | None = None
    upstream_registry_url: str | None = None
    created_at: str | None = None
    registry_id: str | None = None
    credential_arn: str | None = None
    custom_role_arn: str | None = None
    upstream_repository_prefix: str | None = None


class DeleteRegistryPolicyResult(BaseModel):
    """Result of delete_registry_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    policy_text: str | None = None


class DeleteRepositoryResult(BaseModel):
    """Result of delete_repository."""

    model_config = ConfigDict(frozen=True)

    repository: dict[str, Any] | None = None


class DeleteRepositoryCreationTemplateResult(BaseModel):
    """Result of delete_repository_creation_template."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_creation_template: dict[str, Any] | None = None


class DeleteRepositoryPolicyResult(BaseModel):
    """Result of delete_repository_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    policy_text: str | None = None


class DescribeImageReplicationStatusResult(BaseModel):
    """Result of describe_image_replication_status."""

    model_config = ConfigDict(frozen=True)

    repository_name: str | None = None
    image_id: dict[str, Any] | None = None
    replication_statuses: list[dict[str, Any]] | None = None


class DescribeImageScanFindingsResult(BaseModel):
    """Result of describe_image_scan_findings."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    image_id: dict[str, Any] | None = None
    image_scan_status: dict[str, Any] | None = None
    image_scan_findings: dict[str, Any] | None = None
    next_token: str | None = None


class DescribeImagesResult(BaseModel):
    """Result of describe_images."""

    model_config = ConfigDict(frozen=True)

    image_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribePullThroughCacheRulesResult(BaseModel):
    """Result of describe_pull_through_cache_rules."""

    model_config = ConfigDict(frozen=True)

    pull_through_cache_rules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeRegistryResult(BaseModel):
    """Result of describe_registry."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    replication_configuration: dict[str, Any] | None = None


class DescribeRepositoriesResult(BaseModel):
    """Result of describe_repositories."""

    model_config = ConfigDict(frozen=True)

    repositories: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeRepositoryCreationTemplatesResult(BaseModel):
    """Result of describe_repository_creation_templates."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_creation_templates: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetAccountSettingResult(BaseModel):
    """Result of get_account_setting."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    value: str | None = None


class GetAuthorizationTokenResult(BaseModel):
    """Result of get_authorization_token."""

    model_config = ConfigDict(frozen=True)

    authorization_data: list[dict[str, Any]] | None = None


class GetDownloadUrlForLayerResult(BaseModel):
    """Result of get_download_url_for_layer."""

    model_config = ConfigDict(frozen=True)

    download_url: str | None = None
    layer_digest: str | None = None


class GetLifecyclePolicyResult(BaseModel):
    """Result of get_lifecycle_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    lifecycle_policy_text: str | None = None
    last_evaluated_at: str | None = None


class GetLifecyclePolicyPreviewResult(BaseModel):
    """Result of get_lifecycle_policy_preview."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    lifecycle_policy_text: str | None = None
    status: str | None = None
    next_token: str | None = None
    preview_results: list[dict[str, Any]] | None = None
    summary: dict[str, Any] | None = None


class GetRegistryPolicyResult(BaseModel):
    """Result of get_registry_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    policy_text: str | None = None


class GetRegistryScanningConfigurationResult(BaseModel):
    """Result of get_registry_scanning_configuration."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    scanning_configuration: dict[str, Any] | None = None


class GetRepositoryPolicyResult(BaseModel):
    """Result of get_repository_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    policy_text: str | None = None


class InitiateLayerUploadResult(BaseModel):
    """Result of initiate_layer_upload."""

    model_config = ConfigDict(frozen=True)

    upload_id: str | None = None
    part_size: int | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class PutAccountSettingResult(BaseModel):
    """Result of put_account_setting."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    value: str | None = None


class PutImageResult(BaseModel):
    """Result of put_image."""

    model_config = ConfigDict(frozen=True)

    image: dict[str, Any] | None = None


class PutImageScanningConfigurationResult(BaseModel):
    """Result of put_image_scanning_configuration."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    image_scanning_configuration: dict[str, Any] | None = None


class PutImageTagMutabilityResult(BaseModel):
    """Result of put_image_tag_mutability."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    image_tag_mutability: str | None = None
    image_tag_mutability_exclusion_filters: list[dict[str, Any]] | None = None


class PutLifecyclePolicyResult(BaseModel):
    """Result of put_lifecycle_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    lifecycle_policy_text: str | None = None


class PutRegistryPolicyResult(BaseModel):
    """Result of put_registry_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    policy_text: str | None = None


class PutRegistryScanningConfigurationResult(BaseModel):
    """Result of put_registry_scanning_configuration."""

    model_config = ConfigDict(frozen=True)

    registry_scanning_configuration: dict[str, Any] | None = None


class PutReplicationConfigurationResult(BaseModel):
    """Result of put_replication_configuration."""

    model_config = ConfigDict(frozen=True)

    replication_configuration: dict[str, Any] | None = None


class SetRepositoryPolicyResult(BaseModel):
    """Result of set_repository_policy."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    policy_text: str | None = None


class StartImageScanResult(BaseModel):
    """Result of start_image_scan."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    image_id: dict[str, Any] | None = None
    image_scan_status: dict[str, Any] | None = None


class StartLifecyclePolicyPreviewResult(BaseModel):
    """Result of start_lifecycle_policy_preview."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    lifecycle_policy_text: str | None = None
    status: str | None = None


class UpdatePullThroughCacheRuleResult(BaseModel):
    """Result of update_pull_through_cache_rule."""

    model_config = ConfigDict(frozen=True)

    ecr_repository_prefix: str | None = None
    registry_id: str | None = None
    updated_at: str | None = None
    credential_arn: str | None = None
    custom_role_arn: str | None = None
    upstream_repository_prefix: str | None = None


class UpdateRepositoryCreationTemplateResult(BaseModel):
    """Result of update_repository_creation_template."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_creation_template: dict[str, Any] | None = None


class UploadLayerPartResult(BaseModel):
    """Result of upload_layer_part."""

    model_config = ConfigDict(frozen=True)

    registry_id: str | None = None
    repository_name: str | None = None
    upload_id: str | None = None
    last_byte_received: int | None = None


class ValidatePullThroughCacheRuleResult(BaseModel):
    """Result of validate_pull_through_cache_rule."""

    model_config = ConfigDict(frozen=True)

    ecr_repository_prefix: str | None = None
    registry_id: str | None = None
    upstream_registry_url: str | None = None
    credential_arn: str | None = None
    custom_role_arn: str | None = None
    upstream_repository_prefix: str | None = None
    is_valid: bool | None = None
    failure: str | None = None


def batch_check_layer_availability(
    repository_name: str,
    layer_digests: list[str],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> BatchCheckLayerAvailabilityResult:
    """Batch check layer availability.

    Args:
        repository_name: Repository name.
        layer_digests: Layer digests.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["layerDigests"] = layer_digests
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.batch_check_layer_availability(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch check layer availability") from exc
    return BatchCheckLayerAvailabilityResult(
        layers=resp.get("layers"),
        failures=resp.get("failures"),
    )


def batch_delete_image(
    repository_name: str,
    image_ids: list[dict[str, Any]],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> BatchDeleteImageResult:
    """Batch delete image.

    Args:
        repository_name: Repository name.
        image_ids: Image ids.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageIds"] = image_ids
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.batch_delete_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete image") from exc
    return BatchDeleteImageResult(
        image_ids=resp.get("imageIds"),
        failures=resp.get("failures"),
    )


def batch_get_image(
    repository_name: str,
    image_ids: list[dict[str, Any]],
    *,
    registry_id: str | None = None,
    accepted_media_types: list[str] | None = None,
    region_name: str | None = None,
) -> BatchGetImageResult:
    """Batch get image.

    Args:
        repository_name: Repository name.
        image_ids: Image ids.
        registry_id: Registry id.
        accepted_media_types: Accepted media types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageIds"] = image_ids
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if accepted_media_types is not None:
        kwargs["acceptedMediaTypes"] = accepted_media_types
    try:
        resp = client.batch_get_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get image") from exc
    return BatchGetImageResult(
        images=resp.get("images"),
        failures=resp.get("failures"),
    )


def batch_get_repository_scanning_configuration(
    repository_names: list[str],
    region_name: str | None = None,
) -> BatchGetRepositoryScanningConfigurationResult:
    """Batch get repository scanning configuration.

    Args:
        repository_names: Repository names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryNames"] = repository_names
    try:
        resp = client.batch_get_repository_scanning_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get repository scanning configuration") from exc
    return BatchGetRepositoryScanningConfigurationResult(
        scanning_configurations=resp.get("scanningConfigurations"),
        failures=resp.get("failures"),
    )


def complete_layer_upload(
    repository_name: str,
    upload_id: str,
    layer_digests: list[str],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> CompleteLayerUploadResult:
    """Complete layer upload.

    Args:
        repository_name: Repository name.
        upload_id: Upload id.
        layer_digests: Layer digests.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["uploadId"] = upload_id
    kwargs["layerDigests"] = layer_digests
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.complete_layer_upload(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to complete layer upload") from exc
    return CompleteLayerUploadResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        upload_id=resp.get("uploadId"),
        layer_digest=resp.get("layerDigest"),
    )


def create_pull_through_cache_rule(
    ecr_repository_prefix: str,
    upstream_registry_url: str,
    *,
    registry_id: str | None = None,
    upstream_registry: str | None = None,
    credential_arn: str | None = None,
    custom_role_arn: str | None = None,
    upstream_repository_prefix: str | None = None,
    region_name: str | None = None,
) -> CreatePullThroughCacheRuleResult:
    """Create pull through cache rule.

    Args:
        ecr_repository_prefix: Ecr repository prefix.
        upstream_registry_url: Upstream registry url.
        registry_id: Registry id.
        upstream_registry: Upstream registry.
        credential_arn: Credential arn.
        custom_role_arn: Custom role arn.
        upstream_repository_prefix: Upstream repository prefix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ecrRepositoryPrefix"] = ecr_repository_prefix
    kwargs["upstreamRegistryUrl"] = upstream_registry_url
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if upstream_registry is not None:
        kwargs["upstreamRegistry"] = upstream_registry
    if credential_arn is not None:
        kwargs["credentialArn"] = credential_arn
    if custom_role_arn is not None:
        kwargs["customRoleArn"] = custom_role_arn
    if upstream_repository_prefix is not None:
        kwargs["upstreamRepositoryPrefix"] = upstream_repository_prefix
    try:
        resp = client.create_pull_through_cache_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create pull through cache rule") from exc
    return CreatePullThroughCacheRuleResult(
        ecr_repository_prefix=resp.get("ecrRepositoryPrefix"),
        upstream_registry_url=resp.get("upstreamRegistryUrl"),
        created_at=resp.get("createdAt"),
        registry_id=resp.get("registryId"),
        upstream_registry=resp.get("upstreamRegistry"),
        credential_arn=resp.get("credentialArn"),
        custom_role_arn=resp.get("customRoleArn"),
        upstream_repository_prefix=resp.get("upstreamRepositoryPrefix"),
    )


def create_repository(
    repository_name: str,
    *,
    registry_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    image_tag_mutability: str | None = None,
    image_tag_mutability_exclusion_filters: list[dict[str, Any]] | None = None,
    image_scanning_configuration: dict[str, Any] | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateRepositoryResult:
    """Create repository.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        tags: Tags.
        image_tag_mutability: Image tag mutability.
        image_tag_mutability_exclusion_filters: Image tag mutability exclusion filters.
        image_scanning_configuration: Image scanning configuration.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if tags is not None:
        kwargs["tags"] = tags
    if image_tag_mutability is not None:
        kwargs["imageTagMutability"] = image_tag_mutability
    if image_tag_mutability_exclusion_filters is not None:
        kwargs["imageTagMutabilityExclusionFilters"] = image_tag_mutability_exclusion_filters
    if image_scanning_configuration is not None:
        kwargs["imageScanningConfiguration"] = image_scanning_configuration
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    try:
        resp = client.create_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create repository") from exc
    return CreateRepositoryResult(
        repository=resp.get("repository"),
    )


def create_repository_creation_template(
    prefix: str,
    applied_for: list[str],
    *,
    description: str | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    resource_tags: list[dict[str, Any]] | None = None,
    image_tag_mutability: str | None = None,
    image_tag_mutability_exclusion_filters: list[dict[str, Any]] | None = None,
    repository_policy: str | None = None,
    lifecycle_policy: str | None = None,
    custom_role_arn: str | None = None,
    region_name: str | None = None,
) -> CreateRepositoryCreationTemplateResult:
    """Create repository creation template.

    Args:
        prefix: Prefix.
        applied_for: Applied for.
        description: Description.
        encryption_configuration: Encryption configuration.
        resource_tags: Resource tags.
        image_tag_mutability: Image tag mutability.
        image_tag_mutability_exclusion_filters: Image tag mutability exclusion filters.
        repository_policy: Repository policy.
        lifecycle_policy: Lifecycle policy.
        custom_role_arn: Custom role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["prefix"] = prefix
    kwargs["appliedFor"] = applied_for
    if description is not None:
        kwargs["description"] = description
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    if resource_tags is not None:
        kwargs["resourceTags"] = resource_tags
    if image_tag_mutability is not None:
        kwargs["imageTagMutability"] = image_tag_mutability
    if image_tag_mutability_exclusion_filters is not None:
        kwargs["imageTagMutabilityExclusionFilters"] = image_tag_mutability_exclusion_filters
    if repository_policy is not None:
        kwargs["repositoryPolicy"] = repository_policy
    if lifecycle_policy is not None:
        kwargs["lifecyclePolicy"] = lifecycle_policy
    if custom_role_arn is not None:
        kwargs["customRoleArn"] = custom_role_arn
    try:
        resp = client.create_repository_creation_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create repository creation template") from exc
    return CreateRepositoryCreationTemplateResult(
        registry_id=resp.get("registryId"),
        repository_creation_template=resp.get("repositoryCreationTemplate"),
    )


def delete_lifecycle_policy(
    repository_name: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> DeleteLifecyclePolicyResult:
    """Delete lifecycle policy.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.delete_lifecycle_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete lifecycle policy") from exc
    return DeleteLifecyclePolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        lifecycle_policy_text=resp.get("lifecyclePolicyText"),
        last_evaluated_at=resp.get("lastEvaluatedAt"),
    )


def delete_pull_through_cache_rule(
    ecr_repository_prefix: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> DeletePullThroughCacheRuleResult:
    """Delete pull through cache rule.

    Args:
        ecr_repository_prefix: Ecr repository prefix.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ecrRepositoryPrefix"] = ecr_repository_prefix
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.delete_pull_through_cache_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete pull through cache rule") from exc
    return DeletePullThroughCacheRuleResult(
        ecr_repository_prefix=resp.get("ecrRepositoryPrefix"),
        upstream_registry_url=resp.get("upstreamRegistryUrl"),
        created_at=resp.get("createdAt"),
        registry_id=resp.get("registryId"),
        credential_arn=resp.get("credentialArn"),
        custom_role_arn=resp.get("customRoleArn"),
        upstream_repository_prefix=resp.get("upstreamRepositoryPrefix"),
    )


def delete_registry_policy(
    region_name: str | None = None,
) -> DeleteRegistryPolicyResult:
    """Delete registry policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.delete_registry_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete registry policy") from exc
    return DeleteRegistryPolicyResult(
        registry_id=resp.get("registryId"),
        policy_text=resp.get("policyText"),
    )


def delete_repository(
    repository_name: str,
    *,
    registry_id: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeleteRepositoryResult:
    """Delete repository.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if force is not None:
        kwargs["force"] = force
    try:
        resp = client.delete_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete repository") from exc
    return DeleteRepositoryResult(
        repository=resp.get("repository"),
    )


def delete_repository_creation_template(
    prefix: str,
    region_name: str | None = None,
) -> DeleteRepositoryCreationTemplateResult:
    """Delete repository creation template.

    Args:
        prefix: Prefix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["prefix"] = prefix
    try:
        resp = client.delete_repository_creation_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete repository creation template") from exc
    return DeleteRepositoryCreationTemplateResult(
        registry_id=resp.get("registryId"),
        repository_creation_template=resp.get("repositoryCreationTemplate"),
    )


def delete_repository_policy(
    repository_name: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> DeleteRepositoryPolicyResult:
    """Delete repository policy.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.delete_repository_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete repository policy") from exc
    return DeleteRepositoryPolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        policy_text=resp.get("policyText"),
    )


def describe_image_replication_status(
    repository_name: str,
    image_id: dict[str, Any],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> DescribeImageReplicationStatusResult:
    """Describe image replication status.

    Args:
        repository_name: Repository name.
        image_id: Image id.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageId"] = image_id
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.describe_image_replication_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe image replication status") from exc
    return DescribeImageReplicationStatusResult(
        repository_name=resp.get("repositoryName"),
        image_id=resp.get("imageId"),
        replication_statuses=resp.get("replicationStatuses"),
    )


def describe_image_scan_findings(
    repository_name: str,
    image_id: dict[str, Any],
    *,
    registry_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeImageScanFindingsResult:
    """Describe image scan findings.

    Args:
        repository_name: Repository name.
        image_id: Image id.
        registry_id: Registry id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageId"] = image_id
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.describe_image_scan_findings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe image scan findings") from exc
    return DescribeImageScanFindingsResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        image_id=resp.get("imageId"),
        image_scan_status=resp.get("imageScanStatus"),
        image_scan_findings=resp.get("imageScanFindings"),
        next_token=resp.get("nextToken"),
    )


def describe_images(
    repository_name: str,
    *,
    registry_id: str | None = None,
    image_ids: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> DescribeImagesResult:
    """Describe images.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        image_ids: Image ids.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if image_ids is not None:
        kwargs["imageIds"] = image_ids
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_images(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe images") from exc
    return DescribeImagesResult(
        image_details=resp.get("imageDetails"),
        next_token=resp.get("nextToken"),
    )


def describe_pull_through_cache_rules(
    *,
    registry_id: str | None = None,
    ecr_repository_prefixes: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribePullThroughCacheRulesResult:
    """Describe pull through cache rules.

    Args:
        registry_id: Registry id.
        ecr_repository_prefixes: Ecr repository prefixes.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if ecr_repository_prefixes is not None:
        kwargs["ecrRepositoryPrefixes"] = ecr_repository_prefixes
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.describe_pull_through_cache_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pull through cache rules") from exc
    return DescribePullThroughCacheRulesResult(
        pull_through_cache_rules=resp.get("pullThroughCacheRules"),
        next_token=resp.get("nextToken"),
    )


def describe_registry(
    region_name: str | None = None,
) -> DescribeRegistryResult:
    """Describe registry.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_registry(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe registry") from exc
    return DescribeRegistryResult(
        registry_id=resp.get("registryId"),
        replication_configuration=resp.get("replicationConfiguration"),
    )


def describe_repositories(
    *,
    registry_id: str | None = None,
    repository_names: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeRepositoriesResult:
    """Describe repositories.

    Args:
        registry_id: Registry id.
        repository_names: Repository names.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if repository_names is not None:
        kwargs["repositoryNames"] = repository_names
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.describe_repositories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe repositories") from exc
    return DescribeRepositoriesResult(
        repositories=resp.get("repositories"),
        next_token=resp.get("nextToken"),
    )


def describe_repository_creation_templates(
    *,
    prefixes: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeRepositoryCreationTemplatesResult:
    """Describe repository creation templates.

    Args:
        prefixes: Prefixes.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    if prefixes is not None:
        kwargs["prefixes"] = prefixes
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.describe_repository_creation_templates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe repository creation templates") from exc
    return DescribeRepositoryCreationTemplatesResult(
        registry_id=resp.get("registryId"),
        repository_creation_templates=resp.get("repositoryCreationTemplates"),
        next_token=resp.get("nextToken"),
    )


def get_account_setting(
    name: str,
    region_name: str | None = None,
) -> GetAccountSettingResult:
    """Get account setting.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        resp = client.get_account_setting(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get account setting") from exc
    return GetAccountSettingResult(
        name=resp.get("name"),
        value=resp.get("value"),
    )


def get_authorization_token(
    *,
    registry_ids: list[str] | None = None,
    region_name: str | None = None,
) -> GetAuthorizationTokenResult:
    """Get authorization token.

    Args:
        registry_ids: Registry ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    if registry_ids is not None:
        kwargs["registryIds"] = registry_ids
    try:
        resp = client.get_authorization_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get authorization token") from exc
    return GetAuthorizationTokenResult(
        authorization_data=resp.get("authorizationData"),
    )


def get_download_url_for_layer(
    repository_name: str,
    layer_digest: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> GetDownloadUrlForLayerResult:
    """Get download url for layer.

    Args:
        repository_name: Repository name.
        layer_digest: Layer digest.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["layerDigest"] = layer_digest
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.get_download_url_for_layer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get download url for layer") from exc
    return GetDownloadUrlForLayerResult(
        download_url=resp.get("downloadUrl"),
        layer_digest=resp.get("layerDigest"),
    )


def get_lifecycle_policy(
    repository_name: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> GetLifecyclePolicyResult:
    """Get lifecycle policy.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.get_lifecycle_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get lifecycle policy") from exc
    return GetLifecyclePolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        lifecycle_policy_text=resp.get("lifecyclePolicyText"),
        last_evaluated_at=resp.get("lastEvaluatedAt"),
    )


def get_lifecycle_policy_preview(
    repository_name: str,
    *,
    registry_id: str | None = None,
    image_ids: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetLifecyclePolicyPreviewResult:
    """Get lifecycle policy preview.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        image_ids: Image ids.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if image_ids is not None:
        kwargs["imageIds"] = image_ids
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.get_lifecycle_policy_preview(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get lifecycle policy preview") from exc
    return GetLifecyclePolicyPreviewResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        lifecycle_policy_text=resp.get("lifecyclePolicyText"),
        status=resp.get("status"),
        next_token=resp.get("nextToken"),
        preview_results=resp.get("previewResults"),
        summary=resp.get("summary"),
    )


def get_registry_policy(
    region_name: str | None = None,
) -> GetRegistryPolicyResult:
    """Get registry policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_registry_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get registry policy") from exc
    return GetRegistryPolicyResult(
        registry_id=resp.get("registryId"),
        policy_text=resp.get("policyText"),
    )


def get_registry_scanning_configuration(
    region_name: str | None = None,
) -> GetRegistryScanningConfigurationResult:
    """Get registry scanning configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_registry_scanning_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get registry scanning configuration") from exc
    return GetRegistryScanningConfigurationResult(
        registry_id=resp.get("registryId"),
        scanning_configuration=resp.get("scanningConfiguration"),
    )


def get_repository_policy(
    repository_name: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> GetRepositoryPolicyResult:
    """Get repository policy.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.get_repository_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get repository policy") from exc
    return GetRepositoryPolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        policy_text=resp.get("policyText"),
    )


def initiate_layer_upload(
    repository_name: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> InitiateLayerUploadResult:
    """Initiate layer upload.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.initiate_layer_upload(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to initiate layer upload") from exc
    return InitiateLayerUploadResult(
        upload_id=resp.get("uploadId"),
        part_size=resp.get("partSize"),
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
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def put_account_setting(
    name: str,
    value: str,
    region_name: str | None = None,
) -> PutAccountSettingResult:
    """Put account setting.

    Args:
        name: Name.
        value: Value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["value"] = value
    try:
        resp = client.put_account_setting(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put account setting") from exc
    return PutAccountSettingResult(
        name=resp.get("name"),
        value=resp.get("value"),
    )


def put_image(
    repository_name: str,
    image_manifest: str,
    *,
    registry_id: str | None = None,
    image_manifest_media_type: str | None = None,
    image_tag: str | None = None,
    image_digest: str | None = None,
    region_name: str | None = None,
) -> PutImageResult:
    """Put image.

    Args:
        repository_name: Repository name.
        image_manifest: Image manifest.
        registry_id: Registry id.
        image_manifest_media_type: Image manifest media type.
        image_tag: Image tag.
        image_digest: Image digest.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageManifest"] = image_manifest
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if image_manifest_media_type is not None:
        kwargs["imageManifestMediaType"] = image_manifest_media_type
    if image_tag is not None:
        kwargs["imageTag"] = image_tag
    if image_digest is not None:
        kwargs["imageDigest"] = image_digest
    try:
        resp = client.put_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put image") from exc
    return PutImageResult(
        image=resp.get("image"),
    )


def put_image_scanning_configuration(
    repository_name: str,
    image_scanning_configuration: dict[str, Any],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> PutImageScanningConfigurationResult:
    """Put image scanning configuration.

    Args:
        repository_name: Repository name.
        image_scanning_configuration: Image scanning configuration.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageScanningConfiguration"] = image_scanning_configuration
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.put_image_scanning_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put image scanning configuration") from exc
    return PutImageScanningConfigurationResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        image_scanning_configuration=resp.get("imageScanningConfiguration"),
    )


def put_image_tag_mutability(
    repository_name: str,
    image_tag_mutability: str,
    *,
    registry_id: str | None = None,
    image_tag_mutability_exclusion_filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutImageTagMutabilityResult:
    """Put image tag mutability.

    Args:
        repository_name: Repository name.
        image_tag_mutability: Image tag mutability.
        registry_id: Registry id.
        image_tag_mutability_exclusion_filters: Image tag mutability exclusion filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageTagMutability"] = image_tag_mutability
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if image_tag_mutability_exclusion_filters is not None:
        kwargs["imageTagMutabilityExclusionFilters"] = image_tag_mutability_exclusion_filters
    try:
        resp = client.put_image_tag_mutability(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put image tag mutability") from exc
    return PutImageTagMutabilityResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        image_tag_mutability=resp.get("imageTagMutability"),
        image_tag_mutability_exclusion_filters=resp.get("imageTagMutabilityExclusionFilters"),
    )


def put_lifecycle_policy(
    repository_name: str,
    lifecycle_policy_text: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> PutLifecyclePolicyResult:
    """Put lifecycle policy.

    Args:
        repository_name: Repository name.
        lifecycle_policy_text: Lifecycle policy text.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["lifecyclePolicyText"] = lifecycle_policy_text
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.put_lifecycle_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put lifecycle policy") from exc
    return PutLifecyclePolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        lifecycle_policy_text=resp.get("lifecyclePolicyText"),
    )


def put_registry_policy(
    policy_text: str,
    region_name: str | None = None,
) -> PutRegistryPolicyResult:
    """Put registry policy.

    Args:
        policy_text: Policy text.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyText"] = policy_text
    try:
        resp = client.put_registry_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put registry policy") from exc
    return PutRegistryPolicyResult(
        registry_id=resp.get("registryId"),
        policy_text=resp.get("policyText"),
    )


def put_registry_scanning_configuration(
    *,
    scan_type: str | None = None,
    rules: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutRegistryScanningConfigurationResult:
    """Put registry scanning configuration.

    Args:
        scan_type: Scan type.
        rules: Rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    if scan_type is not None:
        kwargs["scanType"] = scan_type
    if rules is not None:
        kwargs["rules"] = rules
    try:
        resp = client.put_registry_scanning_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put registry scanning configuration") from exc
    return PutRegistryScanningConfigurationResult(
        registry_scanning_configuration=resp.get("registryScanningConfiguration"),
    )


def put_replication_configuration(
    replication_configuration: dict[str, Any],
    region_name: str | None = None,
) -> PutReplicationConfigurationResult:
    """Put replication configuration.

    Args:
        replication_configuration: Replication configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["replicationConfiguration"] = replication_configuration
    try:
        resp = client.put_replication_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put replication configuration") from exc
    return PutReplicationConfigurationResult(
        replication_configuration=resp.get("replicationConfiguration"),
    )


def set_repository_policy(
    repository_name: str,
    policy_text: str,
    *,
    registry_id: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> SetRepositoryPolicyResult:
    """Set repository policy.

    Args:
        repository_name: Repository name.
        policy_text: Policy text.
        registry_id: Registry id.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["policyText"] = policy_text
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if force is not None:
        kwargs["force"] = force
    try:
        resp = client.set_repository_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set repository policy") from exc
    return SetRepositoryPolicyResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        policy_text=resp.get("policyText"),
    )


def start_image_scan(
    repository_name: str,
    image_id: dict[str, Any],
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> StartImageScanResult:
    """Start image scan.

    Args:
        repository_name: Repository name.
        image_id: Image id.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["imageId"] = image_id
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.start_image_scan(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start image scan") from exc
    return StartImageScanResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        image_id=resp.get("imageId"),
        image_scan_status=resp.get("imageScanStatus"),
    )


def start_lifecycle_policy_preview(
    repository_name: str,
    *,
    registry_id: str | None = None,
    lifecycle_policy_text: str | None = None,
    region_name: str | None = None,
) -> StartLifecyclePolicyPreviewResult:
    """Start lifecycle policy preview.

    Args:
        repository_name: Repository name.
        registry_id: Registry id.
        lifecycle_policy_text: Lifecycle policy text.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if lifecycle_policy_text is not None:
        kwargs["lifecyclePolicyText"] = lifecycle_policy_text
    try:
        resp = client.start_lifecycle_policy_preview(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start lifecycle policy preview") from exc
    return StartLifecyclePolicyPreviewResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        lifecycle_policy_text=resp.get("lifecyclePolicyText"),
        status=resp.get("status"),
    )


def tag_resource(
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
    client = get_client("ecr", region_name)
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
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_pull_through_cache_rule(
    ecr_repository_prefix: str,
    *,
    registry_id: str | None = None,
    credential_arn: str | None = None,
    custom_role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdatePullThroughCacheRuleResult:
    """Update pull through cache rule.

    Args:
        ecr_repository_prefix: Ecr repository prefix.
        registry_id: Registry id.
        credential_arn: Credential arn.
        custom_role_arn: Custom role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ecrRepositoryPrefix"] = ecr_repository_prefix
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    if credential_arn is not None:
        kwargs["credentialArn"] = credential_arn
    if custom_role_arn is not None:
        kwargs["customRoleArn"] = custom_role_arn
    try:
        resp = client.update_pull_through_cache_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull through cache rule") from exc
    return UpdatePullThroughCacheRuleResult(
        ecr_repository_prefix=resp.get("ecrRepositoryPrefix"),
        registry_id=resp.get("registryId"),
        updated_at=resp.get("updatedAt"),
        credential_arn=resp.get("credentialArn"),
        custom_role_arn=resp.get("customRoleArn"),
        upstream_repository_prefix=resp.get("upstreamRepositoryPrefix"),
    )


def update_repository_creation_template(
    prefix: str,
    *,
    description: str | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    resource_tags: list[dict[str, Any]] | None = None,
    image_tag_mutability: str | None = None,
    image_tag_mutability_exclusion_filters: list[dict[str, Any]] | None = None,
    repository_policy: str | None = None,
    lifecycle_policy: str | None = None,
    applied_for: list[str] | None = None,
    custom_role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateRepositoryCreationTemplateResult:
    """Update repository creation template.

    Args:
        prefix: Prefix.
        description: Description.
        encryption_configuration: Encryption configuration.
        resource_tags: Resource tags.
        image_tag_mutability: Image tag mutability.
        image_tag_mutability_exclusion_filters: Image tag mutability exclusion filters.
        repository_policy: Repository policy.
        lifecycle_policy: Lifecycle policy.
        applied_for: Applied for.
        custom_role_arn: Custom role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["prefix"] = prefix
    if description is not None:
        kwargs["description"] = description
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    if resource_tags is not None:
        kwargs["resourceTags"] = resource_tags
    if image_tag_mutability is not None:
        kwargs["imageTagMutability"] = image_tag_mutability
    if image_tag_mutability_exclusion_filters is not None:
        kwargs["imageTagMutabilityExclusionFilters"] = image_tag_mutability_exclusion_filters
    if repository_policy is not None:
        kwargs["repositoryPolicy"] = repository_policy
    if lifecycle_policy is not None:
        kwargs["lifecyclePolicy"] = lifecycle_policy
    if applied_for is not None:
        kwargs["appliedFor"] = applied_for
    if custom_role_arn is not None:
        kwargs["customRoleArn"] = custom_role_arn
    try:
        resp = client.update_repository_creation_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update repository creation template") from exc
    return UpdateRepositoryCreationTemplateResult(
        registry_id=resp.get("registryId"),
        repository_creation_template=resp.get("repositoryCreationTemplate"),
    )


def upload_layer_part(
    repository_name: str,
    upload_id: str,
    part_first_byte: int,
    part_last_byte: int,
    layer_part_blob: bytes,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> UploadLayerPartResult:
    """Upload layer part.

    Args:
        repository_name: Repository name.
        upload_id: Upload id.
        part_first_byte: Part first byte.
        part_last_byte: Part last byte.
        layer_part_blob: Layer part blob.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["uploadId"] = upload_id
    kwargs["partFirstByte"] = part_first_byte
    kwargs["partLastByte"] = part_last_byte
    kwargs["layerPartBlob"] = layer_part_blob
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.upload_layer_part(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to upload layer part") from exc
    return UploadLayerPartResult(
        registry_id=resp.get("registryId"),
        repository_name=resp.get("repositoryName"),
        upload_id=resp.get("uploadId"),
        last_byte_received=resp.get("lastByteReceived"),
    )


def validate_pull_through_cache_rule(
    ecr_repository_prefix: str,
    *,
    registry_id: str | None = None,
    region_name: str | None = None,
) -> ValidatePullThroughCacheRuleResult:
    """Validate pull through cache rule.

    Args:
        ecr_repository_prefix: Ecr repository prefix.
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ecr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ecrRepositoryPrefix"] = ecr_repository_prefix
    if registry_id is not None:
        kwargs["registryId"] = registry_id
    try:
        resp = client.validate_pull_through_cache_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to validate pull through cache rule") from exc
    return ValidatePullThroughCacheRuleResult(
        ecr_repository_prefix=resp.get("ecrRepositoryPrefix"),
        registry_id=resp.get("registryId"),
        upstream_registry_url=resp.get("upstreamRegistryUrl"),
        credential_arn=resp.get("credentialArn"),
        custom_role_arn=resp.get("customRoleArn"),
        upstream_repository_prefix=resp.get("upstreamRepositoryPrefix"),
        is_valid=resp.get("isValid"),
        failure=resp.get("failure"),
    )
