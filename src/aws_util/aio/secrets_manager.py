"""Native async Secrets Manager utilities — real non-blocking I/O via :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.secrets_manager import (
    BatchGetSecretValueResult,
    CancelRotateSecretResult,
    DeleteResourcePolicyResult,
    DescribeSecretResult,
    GetRandomPasswordResult,
    GetResourcePolicyResult,
    GetSecretValueResult,
    ListSecretVersionIdsResult,
    PutResourcePolicyResult,
    PutSecretValueResult,
    RemoveRegionsFromReplicationResult,
    ReplicateSecretToRegionsResult,
    RestoreSecretResult,
    StopReplicationToReplicaResult,
    UpdateSecretVersionStageResult,
    ValidateResourcePolicyResult,
)

__all__ = [
    "BatchGetSecretValueResult",
    "CancelRotateSecretResult",
    "DeleteResourcePolicyResult",
    "DescribeSecretResult",
    "GetRandomPasswordResult",
    "GetResourcePolicyResult",
    "GetSecretValueResult",
    "ListSecretVersionIdsResult",
    "PutResourcePolicyResult",
    "PutSecretValueResult",
    "RemoveRegionsFromReplicationResult",
    "ReplicateSecretToRegionsResult",
    "RestoreSecretResult",
    "StopReplicationToReplicaResult",
    "UpdateSecretVersionStageResult",
    "ValidateResourcePolicyResult",
    "batch_get_secret_value",
    "cancel_rotate_secret",
    "create_secret",
    "delete_resource_policy",
    "delete_secret",
    "describe_secret",
    "get_random_password",
    "get_resource_policy",
    "get_secret",
    "get_secret_value",
    "list_secret_version_ids",
    "list_secrets",
    "put_resource_policy",
    "put_secret_value",
    "remove_regions_from_replication",
    "replicate_secret_to_regions",
    "restore_secret",
    "rotate_secret",
    "stop_replication_to_replica",
    "tag_resource",
    "untag_resource",
    "update_secret",
    "update_secret_version_stage",
    "validate_resource_policy",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def create_secret(
    name: str,
    value: str | dict[str, Any],
    description: str = "",
    kms_key_id: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a new secret in AWS Secrets Manager.

    Args:
        name: Unique secret name or path, e.g. ``"myapp/db-credentials"``.
        value: Secret value.  Dicts are serialised to JSON automatically.
        description: Human-readable description of the secret.
        kms_key_id: KMS key ID, alias, or ARN used to encrypt the secret.
            Defaults to the AWS-managed ``secretsmanager`` key.
        tags: Resource tags as ``{key: value}``.
        region_name: AWS region override.

    Returns:
        The ARN of the newly created secret.

    Raises:
        RuntimeError: If creation fails.
    """
    raw = json.dumps(value) if isinstance(value, dict) else value
    kwargs: dict[str, Any] = {"Name": name, "SecretString": raw}
    if description:
        kwargs["Description"] = description
    if kms_key_id:
        kwargs["KmsKeyId"] = kms_key_id
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        client = async_client("secretsmanager", region_name)
        resp = await client.call("CreateSecret", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create secret {name!r}") from exc
    return resp["ARN"]


async def update_secret(
    name: str,
    value: str | dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update the value of an existing Secrets Manager secret.

    Args:
        name: Secret name, path, or ARN.
        value: New secret value.  Dicts are serialised to JSON.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    raw = json.dumps(value) if isinstance(value, dict) else value
    try:
        client = async_client("secretsmanager", region_name)
        await client.call("UpdateSecret", SecretId=name, SecretString=raw)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to update secret {name!r}") from exc


async def delete_secret(
    name: str,
    recovery_window_in_days: int = 30,
    force_delete: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete a Secrets Manager secret.

    Args:
        name: Secret name, path, or ARN.
        recovery_window_in_days: Days before permanent deletion (7-30).
            Ignored when *force_delete* is ``True``.
        force_delete: If ``True``, delete immediately without a recovery
            window.  Use with caution -- this is irreversible.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    kwargs: dict[str, Any] = {"SecretId": name}
    if force_delete:
        kwargs["ForceDeleteWithoutRecovery"] = True
    else:
        kwargs["RecoveryWindowInDays"] = recovery_window_in_days
    try:
        client = async_client("secretsmanager", region_name)
        await client.call("DeleteSecret", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete secret {name!r}") from exc


async def list_secrets(
    name_prefix: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List secrets in Secrets Manager, optionally filtered by name prefix.

    Args:
        name_prefix: Only return secrets whose name starts with this string.
        region_name: AWS region override.

    Returns:
        A list of secret metadata dicts with ``name``, ``arn``,
        ``description``, and ``last_changed_date`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    kwargs: dict[str, Any] = {}
    if name_prefix:
        kwargs["Filters"] = [{"Key": "name", "Values": [name_prefix]}]
    try:
        client = async_client("secretsmanager", region_name)
        raw_items = await client.paginate(
            "ListSecrets",
            result_key="SecretList",
            **kwargs,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_secrets failed") from exc
    return [
        {
            "name": s["Name"],
            "arn": s["ARN"],
            "description": s.get("Description", ""),
            "last_changed_date": s.get("LastChangedDate"),
            "last_accessed_date": s.get("LastAccessedDate"),
            "rotation_enabled": s.get("RotationEnabled", False),
        }
        for s in raw_items
    ]


async def rotate_secret(
    name: str,
    lambda_arn: str | None = None,
    rotation_days: int | None = None,
    region_name: str | None = None,
) -> None:
    """Trigger an immediate rotation of a Secrets Manager secret.

    If the secret already has a rotation Lambda configured, calling this
    without *lambda_arn* triggers an immediate rotation using the existing
    Lambda.

    Args:
        name: Secret name, path, or ARN.
        lambda_arn: ARN of the Lambda rotation function.  Required if
            rotation has not been previously configured.
        rotation_days: Automatic rotation interval in days.  Only applied
            when *lambda_arn* is provided.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the rotation fails.
    """
    kwargs: dict[str, Any] = {
        "SecretId": name,
        "RotateImmediately": True,
    }
    if lambda_arn:
        kwargs["RotationLambdaARN"] = lambda_arn
        if rotation_days is not None:
            kwargs["RotationRules"] = {"AutomaticallyAfterDays": rotation_days}
    try:
        client = async_client("secretsmanager", region_name)
        await client.call("RotateSecret", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to rotate secret {name!r}") from exc


async def get_secret(
    inner: str,
    region_name: str | None = None,
) -> str:
    """Fetch a secret value from AWS Secrets Manager.

    The *inner* string may reference either the full secret or a single JSON
    key within the secret:

    * ``"myapp/db-credentials"`` -- returns the entire secret string.
    * ``"myapp/db-credentials:password"`` -- parses the secret as JSON and
      returns only the ``password`` field.
    * ``"arn:aws:secretsmanager:...:secret:myapp/db:password"`` -- ARN form;
      the split is performed on the **last** ``:`` so the ARN itself is
      preserved.

    Caching is intentionally omitted here; use
    :func:`aws_util.placeholder.retrieve` (which wraps this with
    ``lru_cache``) when you need cache-aware resolution.

    Args:
        inner: Secret identifier with an optional ``:json-key`` suffix.
        region_name: AWS region override.  Defaults to the boto3-resolved
            region.

    Returns:
        The secret value (or extracted JSON field) as a string.

    Raises:
        RuntimeError: If the Secrets Manager API call fails.
        RuntimeError: If a JSON key was specified but the secret is not valid
            JSON.
        KeyError: If the specified JSON key is absent from the secret.
    """
    json_key: str | None = None
    if ":" in inner:
        secret_id, json_key = inner.rsplit(":", 1)
    else:
        secret_id = inner

    try:
        client = async_client("secretsmanager", region_name)
        resp = await client.call("GetSecretValue", SecretId=secret_id)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Error resolving secret {secret_id!r}") from exc

    secret_str: str = (
        resp["SecretString"] if "SecretString" in resp else resp["SecretBinary"].decode("utf-8")
    )

    if json_key is None:
        return secret_str

    try:
        data: dict[str, Any] = json.loads(secret_str)
    except json.JSONDecodeError as exc:
        raise wrap_aws_error(
            exc, f"Secret {secret_id!r} is not valid JSON; cannot extract key {json_key!r}"
        ) from exc

    if json_key not in data:
        raise KeyError(f"Key {json_key!r} not found in secret {secret_id!r}")

    return str(data[json_key])


async def batch_get_secret_value(
    *,
    secret_id_list: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> BatchGetSecretValueResult:
    """Batch get secret value.

    Args:
        secret_id_list: Secret id list.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    if secret_id_list is not None:
        kwargs["SecretIdList"] = secret_id_list
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("BatchGetSecretValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get secret value") from exc
    return BatchGetSecretValueResult(
        secret_values=resp.get("SecretValues"),
        next_token=resp.get("NextToken"),
        errors=resp.get("Errors"),
    )


async def cancel_rotate_secret(
    secret_id: str,
    region_name: str | None = None,
) -> CancelRotateSecretResult:
    """Cancel rotate secret.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("CancelRotateSecret", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel rotate secret") from exc
    return CancelRotateSecretResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
        version_id=resp.get("VersionId"),
    )


async def delete_resource_policy(
    secret_id: str,
    region_name: str | None = None,
) -> DeleteResourcePolicyResult:
    """Delete resource policy.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return DeleteResourcePolicyResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
    )


async def describe_secret(
    secret_id: str,
    region_name: str | None = None,
) -> DescribeSecretResult:
    """Describe secret.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("DescribeSecret", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe secret") from exc
    return DescribeSecretResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        kms_key_id=resp.get("KmsKeyId"),
        rotation_enabled=resp.get("RotationEnabled"),
        rotation_lambda_arn=resp.get("RotationLambdaARN"),
        rotation_rules=resp.get("RotationRules"),
        last_rotated_date=resp.get("LastRotatedDate"),
        last_changed_date=resp.get("LastChangedDate"),
        last_accessed_date=resp.get("LastAccessedDate"),
        deleted_date=resp.get("DeletedDate"),
        next_rotation_date=resp.get("NextRotationDate"),
        tags=resp.get("Tags"),
        version_ids_to_stages=resp.get("VersionIdsToStages"),
        owning_service=resp.get("OwningService"),
        created_date=resp.get("CreatedDate"),
        primary_region=resp.get("PrimaryRegion"),
        replication_status=resp.get("ReplicationStatus"),
    )


async def get_random_password(
    *,
    password_length: int | None = None,
    exclude_characters: str | None = None,
    exclude_numbers: bool | None = None,
    exclude_punctuation: bool | None = None,
    exclude_uppercase: bool | None = None,
    exclude_lowercase: bool | None = None,
    include_space: bool | None = None,
    require_each_included_type: bool | None = None,
    region_name: str | None = None,
) -> GetRandomPasswordResult:
    """Get random password.

    Args:
        password_length: Password length.
        exclude_characters: Exclude characters.
        exclude_numbers: Exclude numbers.
        exclude_punctuation: Exclude punctuation.
        exclude_uppercase: Exclude uppercase.
        exclude_lowercase: Exclude lowercase.
        include_space: Include space.
        require_each_included_type: Require each included type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    if password_length is not None:
        kwargs["PasswordLength"] = password_length
    if exclude_characters is not None:
        kwargs["ExcludeCharacters"] = exclude_characters
    if exclude_numbers is not None:
        kwargs["ExcludeNumbers"] = exclude_numbers
    if exclude_punctuation is not None:
        kwargs["ExcludePunctuation"] = exclude_punctuation
    if exclude_uppercase is not None:
        kwargs["ExcludeUppercase"] = exclude_uppercase
    if exclude_lowercase is not None:
        kwargs["ExcludeLowercase"] = exclude_lowercase
    if include_space is not None:
        kwargs["IncludeSpace"] = include_space
    if require_each_included_type is not None:
        kwargs["RequireEachIncludedType"] = require_each_included_type
    try:
        resp = await client.call("GetRandomPassword", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get random password") from exc
    return GetRandomPasswordResult(
        random_password=resp.get("RandomPassword"),
    )


async def get_resource_policy(
    secret_id: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
        resource_policy=resp.get("ResourcePolicy"),
    )


async def get_secret_value(
    secret_id: str,
    *,
    version_id: str | None = None,
    version_stage: str | None = None,
    region_name: str | None = None,
) -> GetSecretValueResult:
    """Get secret value.

    Args:
        secret_id: Secret id.
        version_id: Version id.
        version_stage: Version stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if version_stage is not None:
        kwargs["VersionStage"] = version_stage
    try:
        resp = await client.call("GetSecretValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get secret value") from exc
    return GetSecretValueResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
        version_id=resp.get("VersionId"),
        secret_binary=resp.get("SecretBinary"),
        secret_string=resp.get("SecretString"),
        version_stages=resp.get("VersionStages"),
        created_date=resp.get("CreatedDate"),
    )


async def list_secret_version_ids(
    secret_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    include_deprecated: bool | None = None,
    region_name: str | None = None,
) -> ListSecretVersionIdsResult:
    """List secret version ids.

    Args:
        secret_id: Secret id.
        max_results: Max results.
        next_token: Next token.
        include_deprecated: Include deprecated.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if include_deprecated is not None:
        kwargs["IncludeDeprecated"] = include_deprecated
    try:
        resp = await client.call("ListSecretVersionIds", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list secret version ids") from exc
    return ListSecretVersionIdsResult(
        versions=resp.get("Versions"),
        next_token=resp.get("NextToken"),
        arn=resp.get("ARN"),
        name=resp.get("Name"),
    )


async def put_resource_policy(
    secret_id: str,
    resource_policy: str,
    *,
    block_public_policy: bool | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        secret_id: Secret id.
        resource_policy: Resource policy.
        block_public_policy: Block public policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["ResourcePolicy"] = resource_policy
    if block_public_policy is not None:
        kwargs["BlockPublicPolicy"] = block_public_policy
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
    )


async def put_secret_value(
    secret_id: str,
    *,
    client_request_token: str | None = None,
    secret_binary: bytes | None = None,
    secret_string: str | None = None,
    version_stages: list[str] | None = None,
    rotation_token: str | None = None,
    region_name: str | None = None,
) -> PutSecretValueResult:
    """Put secret value.

    Args:
        secret_id: Secret id.
        client_request_token: Client request token.
        secret_binary: Secret binary.
        secret_string: Secret string.
        version_stages: Version stages.
        rotation_token: Rotation token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if secret_binary is not None:
        kwargs["SecretBinary"] = secret_binary
    if secret_string is not None:
        kwargs["SecretString"] = secret_string
    if version_stages is not None:
        kwargs["VersionStages"] = version_stages
    if rotation_token is not None:
        kwargs["RotationToken"] = rotation_token
    try:
        resp = await client.call("PutSecretValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put secret value") from exc
    return PutSecretValueResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
        version_id=resp.get("VersionId"),
        version_stages=resp.get("VersionStages"),
    )


async def remove_regions_from_replication(
    secret_id: str,
    remove_replica_regions: list[str],
    region_name: str | None = None,
) -> RemoveRegionsFromReplicationResult:
    """Remove regions from replication.

    Args:
        secret_id: Secret id.
        remove_replica_regions: Remove replica regions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["RemoveReplicaRegions"] = remove_replica_regions
    try:
        resp = await client.call("RemoveRegionsFromReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove regions from replication") from exc
    return RemoveRegionsFromReplicationResult(
        arn=resp.get("ARN"),
        replication_status=resp.get("ReplicationStatus"),
    )


async def replicate_secret_to_regions(
    secret_id: str,
    add_replica_regions: list[dict[str, Any]],
    *,
    force_overwrite_replica_secret: bool | None = None,
    region_name: str | None = None,
) -> ReplicateSecretToRegionsResult:
    """Replicate secret to regions.

    Args:
        secret_id: Secret id.
        add_replica_regions: Add replica regions.
        force_overwrite_replica_secret: Force overwrite replica secret.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["AddReplicaRegions"] = add_replica_regions
    if force_overwrite_replica_secret is not None:
        kwargs["ForceOverwriteReplicaSecret"] = force_overwrite_replica_secret
    try:
        resp = await client.call("ReplicateSecretToRegions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to replicate secret to regions") from exc
    return ReplicateSecretToRegionsResult(
        arn=resp.get("ARN"),
        replication_status=resp.get("ReplicationStatus"),
    )


async def restore_secret(
    secret_id: str,
    region_name: str | None = None,
) -> RestoreSecretResult:
    """Restore secret.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("RestoreSecret", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore secret") from exc
    return RestoreSecretResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
    )


async def stop_replication_to_replica(
    secret_id: str,
    region_name: str | None = None,
) -> StopReplicationToReplicaResult:
    """Stop replication to replica.

    Args:
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("StopReplicationToReplica", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop replication to replica") from exc
    return StopReplicationToReplicaResult(
        arn=resp.get("ARN"),
    )


async def tag_resource(
    secret_id: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        secret_id: Secret id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    secret_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        secret_id: Secret id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_secret_version_stage(
    secret_id: str,
    version_stage: str,
    *,
    remove_from_version_id: str | None = None,
    move_to_version_id: str | None = None,
    region_name: str | None = None,
) -> UpdateSecretVersionStageResult:
    """Update secret version stage.

    Args:
        secret_id: Secret id.
        version_stage: Version stage.
        remove_from_version_id: Remove from version id.
        move_to_version_id: Move to version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecretId"] = secret_id
    kwargs["VersionStage"] = version_stage
    if remove_from_version_id is not None:
        kwargs["RemoveFromVersionId"] = remove_from_version_id
    if move_to_version_id is not None:
        kwargs["MoveToVersionId"] = move_to_version_id
    try:
        resp = await client.call("UpdateSecretVersionStage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update secret version stage") from exc
    return UpdateSecretVersionStageResult(
        arn=resp.get("ARN"),
        name=resp.get("Name"),
    )


async def validate_resource_policy(
    resource_policy: str,
    *,
    secret_id: str | None = None,
    region_name: str | None = None,
) -> ValidateResourcePolicyResult:
    """Validate resource policy.

    Args:
        resource_policy: Resource policy.
        secret_id: Secret id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("secretsmanager", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourcePolicy"] = resource_policy
    if secret_id is not None:
        kwargs["SecretId"] = secret_id
    try:
        resp = await client.call("ValidateResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to validate resource policy") from exc
    return ValidateResourcePolicyResult(
        policy_validation_passed=resp.get("PolicyValidationPassed"),
        validation_errors=resp.get("ValidationErrors"),
    )
