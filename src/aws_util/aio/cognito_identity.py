"""Native async Cognito Identity utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.cognito_identity import (
    CredentialsResult,
    GetIdentityPoolRolesResult,
    GetOpenIdTokenForDeveloperIdentityResult,
    GetPrincipalTagAttributeMapResult,
    IdentityPoolResult,
    IdentityResult,
    ListTagsForResourceResult,
    LookupDeveloperIdentityResult,
    MergeDeveloperIdentitiesResult,
    OpenIdTokenResult,
    SetPrincipalTagAttributeMapResult,
    _parse_identity,
    _parse_identity_pool,
)
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CredentialsResult",
    "GetIdentityPoolRolesResult",
    "GetOpenIdTokenForDeveloperIdentityResult",
    "GetPrincipalTagAttributeMapResult",
    "IdentityPoolResult",
    "IdentityResult",
    "ListTagsForResourceResult",
    "LookupDeveloperIdentityResult",
    "MergeDeveloperIdentitiesResult",
    "OpenIdTokenResult",
    "SetPrincipalTagAttributeMapResult",
    "create_identity_pool",
    "delete_identities",
    "delete_identity_pool",
    "describe_identity",
    "describe_identity_pool",
    "get_credentials_for_identity",
    "get_id",
    "get_identity_pool_roles",
    "get_open_id_token",
    "get_open_id_token_for_developer_identity",
    "get_principal_tag_attribute_map",
    "list_identities",
    "list_identity_pools",
    "list_tags_for_resource",
    "lookup_developer_identity",
    "merge_developer_identities",
    "set_identity_pool_roles",
    "set_principal_tag_attribute_map",
    "tag_resource",
    "unlink_developer_identity",
    "unlink_identity",
    "untag_resource",
    "update_identity_pool",
]


# ---------------------------------------------------------------------------
# Identity Pool CRUD
# ---------------------------------------------------------------------------


async def create_identity_pool(
    identity_pool_name: str,
    allow_unauthenticated_identities: bool = False,
    *,
    supported_login_providers: dict[str, str] | None = None,
    developer_provider_name: str | None = None,
    open_id_connect_provider_arns: list[str] | None = None,
    cognito_identity_providers: list[dict[str, Any]] | None = None,
    saml_provider_arns: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> IdentityPoolResult:
    """Create a new Cognito Identity pool.

    Args:
        identity_pool_name: Name of the identity pool.
        allow_unauthenticated_identities: Whether to allow
            unauthenticated identities.
        supported_login_providers: Login providers mapping.
        developer_provider_name: Developer provider name.
        open_id_connect_provider_arns: OIDC provider ARNs.
        cognito_identity_providers: Cognito identity provider configs.
        saml_provider_arns: SAML provider ARNs.
        tags: Tags to attach to the pool.
        region_name: AWS region override.

    Returns:
        The newly created :class:`IdentityPoolResult`.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {
        "IdentityPoolName": identity_pool_name,
        "AllowUnauthenticatedIdentities": allow_unauthenticated_identities,
    }
    if supported_login_providers is not None:
        kwargs["SupportedLoginProviders"] = supported_login_providers
    if developer_provider_name is not None:
        kwargs["DeveloperProviderName"] = developer_provider_name
    if open_id_connect_provider_arns is not None:
        kwargs["OpenIdConnectProviderARNs"] = open_id_connect_provider_arns
    if cognito_identity_providers is not None:
        kwargs["CognitoIdentityProviders"] = cognito_identity_providers
    if saml_provider_arns is not None:
        kwargs["SamlProviderARNs"] = saml_provider_arns
    if tags is not None:
        kwargs["IdentityPoolTags"] = tags
    try:
        resp = await client.call("CreateIdentityPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create identity pool {identity_pool_name!r}",
        ) from exc
    return _parse_identity_pool(resp)


async def describe_identity_pool(
    identity_pool_id: str,
    *,
    region_name: str | None = None,
) -> IdentityPoolResult | None:
    """Describe a Cognito Identity pool.

    Args:
        identity_pool_id: ID of the identity pool.
        region_name: AWS region override.

    Returns:
        An :class:`IdentityPoolResult`, or ``None`` if not found.
    """
    client = async_client("cognito-identity", region_name)
    try:
        resp = await client.call("DescribeIdentityPool", IdentityPoolId=identity_pool_id)
        return _parse_identity_pool(resp)
    except Exception as exc:
        err_str = str(exc)
        if "ResourceNotFoundException" in err_str:
            return None
        raise wrap_aws_error(
            exc,
            f"describe_identity_pool failed for {identity_pool_id!r}",
        ) from exc


async def list_identity_pools(
    max_results: int = 60,
    *,
    region_name: str | None = None,
) -> list[IdentityPoolResult]:
    """List Cognito Identity pools.

    Args:
        max_results: Maximum results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`IdentityPoolResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    results: list[IdentityPoolResult] = []
    try:
        kwargs: dict[str, Any] = {"MaxResults": max_results}
        while True:
            resp = await client.call("ListIdentityPools", **kwargs)
            for pool in resp.get("IdentityPools", []):
                results.append(
                    IdentityPoolResult(
                        identity_pool_id=pool.get("IdentityPoolId", ""),
                        identity_pool_name=pool.get("IdentityPoolName", ""),
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_identity_pools failed") from exc
    return results


async def update_identity_pool(
    identity_pool_id: str,
    identity_pool_name: str,
    allow_unauthenticated_identities: bool = False,
    *,
    supported_login_providers: dict[str, str] | None = None,
    developer_provider_name: str | None = None,
    open_id_connect_provider_arns: list[str] | None = None,
    cognito_identity_providers: list[dict[str, Any]] | None = None,
    saml_provider_arns: list[str] | None = None,
    region_name: str | None = None,
) -> IdentityPoolResult:
    """Update a Cognito Identity pool.

    Args:
        identity_pool_id: ID of the identity pool.
        identity_pool_name: Updated name of the pool.
        allow_unauthenticated_identities: Whether to allow
            unauthenticated identities.
        supported_login_providers: Login providers mapping.
        developer_provider_name: Developer provider name.
        open_id_connect_provider_arns: OIDC provider ARNs.
        cognito_identity_providers: Cognito identity provider configs.
        saml_provider_arns: SAML provider ARNs.
        region_name: AWS region override.

    Returns:
        The updated :class:`IdentityPoolResult`.

    Raises:
        RuntimeError: If the update fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {
        "IdentityPoolId": identity_pool_id,
        "IdentityPoolName": identity_pool_name,
        "AllowUnauthenticatedIdentities": allow_unauthenticated_identities,
    }
    if supported_login_providers is not None:
        kwargs["SupportedLoginProviders"] = supported_login_providers
    if developer_provider_name is not None:
        kwargs["DeveloperProviderName"] = developer_provider_name
    if open_id_connect_provider_arns is not None:
        kwargs["OpenIdConnectProviderARNs"] = open_id_connect_provider_arns
    if cognito_identity_providers is not None:
        kwargs["CognitoIdentityProviders"] = cognito_identity_providers
    if saml_provider_arns is not None:
        kwargs["SamlProviderARNs"] = saml_provider_arns
    try:
        resp = await client.call("UpdateIdentityPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to update identity pool {identity_pool_id!r}",
        ) from exc
    return _parse_identity_pool(resp)


async def delete_identity_pool(
    identity_pool_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Cognito Identity pool.

    Args:
        identity_pool_id: ID of the identity pool to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    client = async_client("cognito-identity", region_name)
    try:
        await client.call("DeleteIdentityPool", IdentityPoolId=identity_pool_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete identity pool {identity_pool_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Identity operations
# ---------------------------------------------------------------------------


async def get_id(
    identity_pool_id: str,
    *,
    account_id: str | None = None,
    logins: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Get or create an identity ID from the identity pool.

    Args:
        identity_pool_id: ID of the identity pool.
        account_id: AWS account ID.
        logins: Login provider tokens mapping.
        region_name: AWS region override.

    Returns:
        The identity ID string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {
        "IdentityPoolId": identity_pool_id,
    }
    if account_id is not None:
        kwargs["AccountId"] = account_id
    if logins is not None:
        kwargs["Logins"] = logins
    try:
        resp = await client.call("GetId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_id failed") from exc
    return resp.get("IdentityId", "")


async def get_credentials_for_identity(
    identity_id: str,
    *,
    logins: dict[str, str] | None = None,
    custom_role_arn: str | None = None,
    region_name: str | None = None,
) -> CredentialsResult:
    """Get temporary AWS credentials for an identity.

    Args:
        identity_id: The identity ID.
        logins: Login provider tokens mapping.
        custom_role_arn: Custom IAM role ARN to assume.
        region_name: AWS region override.

    Returns:
        A :class:`CredentialsResult` with temporary credentials.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {"IdentityId": identity_id}
    if logins is not None:
        kwargs["Logins"] = logins
    if custom_role_arn is not None:
        kwargs["CustomRoleArn"] = custom_role_arn
    try:
        resp = await client.call("GetCredentialsForIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_credentials_for_identity failed") from exc
    creds = resp.get("Credentials", {})
    expiration = creds.get("Expiration")
    return CredentialsResult(
        identity_id=resp.get("IdentityId", identity_id),
        access_key_id=creds.get("AccessKeyId", ""),
        secret_key=creds.get("SecretKey", ""),
        session_token=creds.get("SessionToken", ""),
        expiration=str(expiration) if expiration is not None else None,
    )


async def get_open_id_token(
    identity_id: str,
    *,
    logins: dict[str, str] | None = None,
    region_name: str | None = None,
) -> OpenIdTokenResult:
    """Get an OpenID Connect token for an identity.

    Args:
        identity_id: The identity ID.
        logins: Login provider tokens mapping.
        region_name: AWS region override.

    Returns:
        An :class:`OpenIdTokenResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {"IdentityId": identity_id}
    if logins is not None:
        kwargs["Logins"] = logins
    try:
        resp = await client.call("GetOpenIdToken", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_open_id_token failed") from exc
    return OpenIdTokenResult(
        identity_id=resp.get("IdentityId", identity_id),
        token=resp.get("Token", ""),
    )


async def list_identities(
    identity_pool_id: str,
    max_results: int = 60,
    *,
    hide_disabled: bool = False,
    region_name: str | None = None,
) -> list[IdentityResult]:
    """List identities in an identity pool.

    Args:
        identity_pool_id: ID of the identity pool.
        max_results: Maximum results per page.
        hide_disabled: Whether to hide disabled identities.
        region_name: AWS region override.

    Returns:
        A list of :class:`IdentityResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    results: list[IdentityResult] = []
    try:
        kwargs: dict[str, Any] = {
            "IdentityPoolId": identity_pool_id,
            "MaxResults": max_results,
            "HideDisabled": hide_disabled,
        }
        while True:
            resp = await client.call("ListIdentities", **kwargs)
            for identity in resp.get("Identities", []):
                results.append(_parse_identity(identity))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_identities failed") from exc
    return results


async def describe_identity(
    identity_id: str,
    *,
    region_name: str | None = None,
) -> IdentityResult | None:
    """Describe a specific identity.

    Args:
        identity_id: The identity ID.
        region_name: AWS region override.

    Returns:
        An :class:`IdentityResult`, or ``None`` if not found.
    """
    client = async_client("cognito-identity", region_name)
    try:
        resp = await client.call("DescribeIdentity", IdentityId=identity_id)
        return _parse_identity(resp)
    except Exception as exc:
        err_str = str(exc)
        if "ResourceNotFoundException" in err_str:
            return None
        raise wrap_aws_error(
            exc,
            f"describe_identity failed for {identity_id!r}",
        ) from exc


async def delete_identities(
    identity_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Delete one or more identities.

    Args:
        identity_ids: List of identity IDs to delete.
        region_name: AWS region override.

    Returns:
        A list of unprocessed identity IDs (errors).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    try:
        resp = await client.call("DeleteIdentities", IdentityIdsToDelete=identity_ids)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_identities failed") from exc
    return resp.get("UnprocessedIdentityIds", [])


async def get_identity_pool_roles(
    identity_pool_id: str,
    region_name: str | None = None,
) -> GetIdentityPoolRolesResult:
    """Get identity pool roles.

    Args:
        identity_pool_id: Identity pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    try:
        resp = await client.call("GetIdentityPoolRoles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity pool roles") from exc
    return GetIdentityPoolRolesResult(
        identity_pool_id=resp.get("IdentityPoolId"),
        roles=resp.get("Roles"),
        role_mappings=resp.get("RoleMappings"),
    )


async def get_open_id_token_for_developer_identity(
    identity_pool_id: str,
    logins: dict[str, Any],
    *,
    identity_id: str | None = None,
    principal_tags: dict[str, Any] | None = None,
    token_duration: int | None = None,
    region_name: str | None = None,
) -> GetOpenIdTokenForDeveloperIdentityResult:
    """Get open id token for developer identity.

    Args:
        identity_pool_id: Identity pool id.
        logins: Logins.
        identity_id: Identity id.
        principal_tags: Principal tags.
        token_duration: Token duration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    kwargs["Logins"] = logins
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if principal_tags is not None:
        kwargs["PrincipalTags"] = principal_tags
    if token_duration is not None:
        kwargs["TokenDuration"] = token_duration
    try:
        resp = await client.call("GetOpenIdTokenForDeveloperIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get open id token for developer identity") from exc
    return GetOpenIdTokenForDeveloperIdentityResult(
        identity_id=resp.get("IdentityId"),
        token=resp.get("Token"),
    )


async def get_principal_tag_attribute_map(
    identity_pool_id: str,
    identity_provider_name: str,
    region_name: str | None = None,
) -> GetPrincipalTagAttributeMapResult:
    """Get principal tag attribute map.

    Args:
        identity_pool_id: Identity pool id.
        identity_provider_name: Identity provider name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    kwargs["IdentityProviderName"] = identity_provider_name
    try:
        resp = await client.call("GetPrincipalTagAttributeMap", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get principal tag attribute map") from exc
    return GetPrincipalTagAttributeMapResult(
        identity_pool_id=resp.get("IdentityPoolId"),
        identity_provider_name=resp.get("IdentityProviderName"),
        use_defaults=resp.get("UseDefaults"),
        principal_tags=resp.get("PrincipalTags"),
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
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def lookup_developer_identity(
    identity_pool_id: str,
    *,
    identity_id: str | None = None,
    developer_user_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> LookupDeveloperIdentityResult:
    """Lookup developer identity.

    Args:
        identity_pool_id: Identity pool id.
        identity_id: Identity id.
        developer_user_identifier: Developer user identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if developer_user_identifier is not None:
        kwargs["DeveloperUserIdentifier"] = developer_user_identifier
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("LookupDeveloperIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to lookup developer identity") from exc
    return LookupDeveloperIdentityResult(
        identity_id=resp.get("IdentityId"),
        developer_user_identifier_list=resp.get("DeveloperUserIdentifierList"),
        next_token=resp.get("NextToken"),
    )


async def merge_developer_identities(
    source_user_identifier: str,
    destination_user_identifier: str,
    developer_provider_name: str,
    identity_pool_id: str,
    region_name: str | None = None,
) -> MergeDeveloperIdentitiesResult:
    """Merge developer identities.

    Args:
        source_user_identifier: Source user identifier.
        destination_user_identifier: Destination user identifier.
        developer_provider_name: Developer provider name.
        identity_pool_id: Identity pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceUserIdentifier"] = source_user_identifier
    kwargs["DestinationUserIdentifier"] = destination_user_identifier
    kwargs["DeveloperProviderName"] = developer_provider_name
    kwargs["IdentityPoolId"] = identity_pool_id
    try:
        resp = await client.call("MergeDeveloperIdentities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to merge developer identities") from exc
    return MergeDeveloperIdentitiesResult(
        identity_id=resp.get("IdentityId"),
    )


async def set_identity_pool_roles(
    identity_pool_id: str,
    roles: dict[str, Any],
    *,
    role_mappings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Set identity pool roles.

    Args:
        identity_pool_id: Identity pool id.
        roles: Roles.
        role_mappings: Role mappings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    kwargs["Roles"] = roles
    if role_mappings is not None:
        kwargs["RoleMappings"] = role_mappings
    try:
        await client.call("SetIdentityPoolRoles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set identity pool roles") from exc
    return None


async def set_principal_tag_attribute_map(
    identity_pool_id: str,
    identity_provider_name: str,
    *,
    use_defaults: bool | None = None,
    principal_tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SetPrincipalTagAttributeMapResult:
    """Set principal tag attribute map.

    Args:
        identity_pool_id: Identity pool id.
        identity_provider_name: Identity provider name.
        use_defaults: Use defaults.
        principal_tags: Principal tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityPoolId"] = identity_pool_id
    kwargs["IdentityProviderName"] = identity_provider_name
    if use_defaults is not None:
        kwargs["UseDefaults"] = use_defaults
    if principal_tags is not None:
        kwargs["PrincipalTags"] = principal_tags
    try:
        resp = await client.call("SetPrincipalTagAttributeMap", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set principal tag attribute map") from exc
    return SetPrincipalTagAttributeMapResult(
        identity_pool_id=resp.get("IdentityPoolId"),
        identity_provider_name=resp.get("IdentityProviderName"),
        use_defaults=resp.get("UseDefaults"),
        principal_tags=resp.get("PrincipalTags"),
    )


async def tag_resource(
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
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def unlink_developer_identity(
    identity_id: str,
    identity_pool_id: str,
    developer_provider_name: str,
    developer_user_identifier: str,
    region_name: str | None = None,
) -> None:
    """Unlink developer identity.

    Args:
        identity_id: Identity id.
        identity_pool_id: Identity pool id.
        developer_provider_name: Developer provider name.
        developer_user_identifier: Developer user identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityId"] = identity_id
    kwargs["IdentityPoolId"] = identity_pool_id
    kwargs["DeveloperProviderName"] = developer_provider_name
    kwargs["DeveloperUserIdentifier"] = developer_user_identifier
    try:
        await client.call("UnlinkDeveloperIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to unlink developer identity") from exc
    return None


async def unlink_identity(
    identity_id: str,
    logins: dict[str, Any],
    logins_to_remove: list[str],
    region_name: str | None = None,
) -> None:
    """Unlink identity.

    Args:
        identity_id: Identity id.
        logins: Logins.
        logins_to_remove: Logins to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityId"] = identity_id
    kwargs["Logins"] = logins
    kwargs["LoginsToRemove"] = logins_to_remove
    try:
        await client.call("UnlinkIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to unlink identity") from exc
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
    client = async_client("cognito-identity", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
