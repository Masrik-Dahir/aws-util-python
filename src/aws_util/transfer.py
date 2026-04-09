"""aws_util.transfer -- AWS Transfer Family utilities.

Create, describe, update, delete, start, and stop SFTP/FTPS/FTP servers,
manage users, SSH public keys, external access entries, and workflows.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AccessResult",
    "CreateAgreementResult",
    "CreateConnectorResult",
    "CreateProfileResult",
    "CreateWebAppResult",
    "DescribeAgreementResult",
    "DescribeCertificateResult",
    "DescribeConnectorResult",
    "DescribeExecutionResult",
    "DescribeHostKeyResult",
    "DescribeProfileResult",
    "DescribeSecurityPolicyResult",
    "DescribeWebAppCustomizationResult",
    "DescribeWebAppResult",
    "ImportCertificateResult",
    "ImportHostKeyResult",
    "ListAgreementsResult",
    "ListCertificatesResult",
    "ListConnectorsResult",
    "ListExecutionsResult",
    "ListFileTransferResultsResult",
    "ListHostKeysResult",
    "ListProfilesResult",
    "ListSecurityPoliciesResult",
    "ListTagsForResourceResult",
    "ListWebAppsResult",
    "RunConnectionResult",
    "RunIdentityProviderResult",
    "ServerResult",
    "SshPublicKeyResult",
    "StartDirectoryListingResult",
    "StartFileTransferResult",
    "StartRemoteDeleteResult",
    "StartRemoteMoveResult",
    "UpdateAgreementResult",
    "UpdateCertificateResult",
    "UpdateConnectorResult",
    "UpdateHostKeyResult",
    "UpdateProfileResult",
    "UpdateWebAppCustomizationResult",
    "UpdateWebAppResult",
    "UserResult",
    "WorkflowResult",
    "create_access",
    "create_agreement",
    "create_connector",
    "create_profile",
    "create_server",
    "create_user",
    "create_web_app",
    "create_workflow",
    "delete_access",
    "delete_agreement",
    "delete_certificate",
    "delete_connector",
    "delete_host_key",
    "delete_profile",
    "delete_server",
    "delete_ssh_public_key",
    "delete_user",
    "delete_web_app",
    "delete_web_app_customization",
    "delete_workflow",
    "describe_access",
    "describe_agreement",
    "describe_certificate",
    "describe_connector",
    "describe_execution",
    "describe_host_key",
    "describe_profile",
    "describe_security_policy",
    "describe_server",
    "describe_user",
    "describe_web_app",
    "describe_web_app_customization",
    "describe_workflow",
    "import_certificate",
    "import_host_key",
    "import_ssh_public_key",
    "list_accesses",
    "list_agreements",
    "list_certificates",
    "list_connectors",
    "list_executions",
    "list_file_transfer_results",
    "list_host_keys",
    "list_profiles",
    "list_security_policies",
    "list_servers",
    "list_tags_for_resource",
    "list_users",
    "list_web_apps",
    "list_workflows",
    "run_connection",
    "run_identity_provider",
    "send_workflow_step_state",
    "start_directory_listing",
    "start_file_transfer",
    "start_remote_delete",
    "start_remote_move",
    "start_server",
    "stop_server",
    "tag_resource",
    "untag_resource",
    "update_access",
    "update_agreement",
    "update_certificate",
    "update_connector",
    "update_host_key",
    "update_profile",
    "update_server",
    "update_user",
    "update_web_app",
    "update_web_app_customization",
    "wait_for_server",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ServerResult(BaseModel):
    """Metadata for a Transfer Family server."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    server_id: str
    arn: str | None = None
    state: str | None = None
    endpoint_type: str | None = None
    identity_provider_type: str | None = None
    domain: str | None = None
    protocols: list[str] = []
    extra: dict[str, Any] = {}


class UserResult(BaseModel):
    """Metadata for a Transfer Family user."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    server_id: str
    user_name: str
    arn: str | None = None
    home_directory: str | None = None
    home_directory_type: str | None = None
    role: str | None = None
    ssh_public_key_count: int | None = None
    extra: dict[str, Any] = {}


class SshPublicKeyResult(BaseModel):
    """Metadata for an imported SSH public key."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    server_id: str
    user_name: str
    ssh_public_key_id: str


class AccessResult(BaseModel):
    """Metadata for a Transfer Family external access entry."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    server_id: str
    external_id: str
    home_directory: str | None = None
    home_directory_type: str | None = None
    role: str | None = None
    extra: dict[str, Any] = {}


class WorkflowResult(BaseModel):
    """Metadata for a Transfer Family workflow."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    workflow_id: str
    arn: str | None = None
    description: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SERVER_KNOWN_KEYS = {
    "ServerId",
    "Arn",
    "State",
    "EndpointType",
    "IdentityProviderType",
    "Domain",
    "Protocols",
}

_USER_KNOWN_KEYS = {
    "ServerId",
    "UserName",
    "Arn",
    "HomeDirectory",
    "HomeDirectoryType",
    "Role",
    "SshPublicKeyCount",
}


def _parse_server(data: dict[str, Any]) -> ServerResult:
    """Convert a raw Transfer server dict to a :class:`ServerResult`."""
    return ServerResult(
        server_id=data["ServerId"],
        arn=data.get("Arn"),
        state=data.get("State"),
        endpoint_type=data.get("EndpointType"),
        identity_provider_type=data.get("IdentityProviderType"),
        domain=data.get("Domain"),
        protocols=data.get("Protocols", []),
        extra={k: v for k, v in data.items() if k not in _SERVER_KNOWN_KEYS},
    )


def _parse_user(data: dict[str, Any]) -> UserResult:
    """Convert a raw Transfer user dict to a :class:`UserResult`."""
    return UserResult(
        server_id=data["ServerId"],
        user_name=data["UserName"],
        arn=data.get("Arn"),
        home_directory=data.get("HomeDirectory"),
        home_directory_type=data.get("HomeDirectoryType"),
        role=data.get("Role"),
        ssh_public_key_count=data.get("SshPublicKeyCount"),
        extra={k: v for k, v in data.items() if k not in _USER_KNOWN_KEYS},
    )


def _parse_access(data: dict[str, Any]) -> AccessResult:
    """Convert a raw Transfer access dict to an :class:`AccessResult`."""
    known = {"ServerId", "ExternalId", "HomeDirectory", "HomeDirectoryType", "Role"}
    return AccessResult(
        server_id=data["ServerId"],
        external_id=data["ExternalId"],
        home_directory=data.get("HomeDirectory"),
        home_directory_type=data.get("HomeDirectoryType"),
        role=data.get("Role"),
        extra={k: v for k, v in data.items() if k not in known},
    )


def _parse_workflow(data: dict[str, Any]) -> WorkflowResult:
    """Convert a raw Transfer workflow dict to a :class:`WorkflowResult`."""
    known = {"WorkflowId", "Arn", "Description"}
    return WorkflowResult(
        workflow_id=data["WorkflowId"],
        arn=data.get("Arn"),
        description=data.get("Description"),
        extra={k: v for k, v in data.items() if k not in known},
    )


# ---------------------------------------------------------------------------
# Server operations
# ---------------------------------------------------------------------------


def create_server(
    *,
    protocols: list[str] | None = None,
    endpoint_type: str | None = None,
    identity_provider_type: str | None = None,
    domain: str | None = None,
    tags: dict[str, str] | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ServerResult:
    """Create a Transfer Family server.

    Args:
        protocols: List of protocols, e.g. ``["SFTP"]``.
        endpoint_type: ``"PUBLIC"`` or ``"VPC"``.
        identity_provider_type: ``"SERVICE_MANAGED"`` or ``"API_GATEWAY"``,
            etc.
        domain: ``"S3"`` or ``"EFS"``.
        tags: Key/value tags to apply.
        extra_kwargs: Additional CreateServer parameters.
        region_name: AWS region override.

    Returns:
        A :class:`ServerResult` for the newly created server.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if protocols is not None:
        kwargs["Protocols"] = protocols
    if endpoint_type is not None:
        kwargs["EndpointType"] = endpoint_type
    if identity_provider_type is not None:
        kwargs["IdentityProviderType"] = identity_provider_type
    if domain is not None:
        kwargs["Domain"] = domain
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.create_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_server failed") from exc
    return ServerResult(server_id=resp["ServerId"], arn=resp.get("Arn"))


def describe_server(
    server_id: str,
    *,
    region_name: str | None = None,
) -> ServerResult:
    """Describe a Transfer Family server.

    Args:
        server_id: The server ID.
        region_name: AWS region override.

    Returns:
        A :class:`ServerResult` with full server details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        resp = client.describe_server(ServerId=server_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_server failed") from exc
    return _parse_server(resp["Server"])


def list_servers(
    *,
    region_name: str | None = None,
) -> list[ServerResult]:
    """List all Transfer Family servers.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ServerResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    results: list[ServerResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_servers(**kwargs)
            for srv in resp.get("Servers", []):
                results.append(_parse_server(srv))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_servers failed") from exc
    return results


def update_server(
    server_id: str,
    *,
    protocols: list[str] | None = None,
    endpoint_type: str | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Update a Transfer Family server.

    Args:
        server_id: The server ID to update.
        protocols: New list of protocols.
        endpoint_type: New endpoint type.
        extra_kwargs: Additional UpdateServer parameters.
        region_name: AWS region override.

    Returns:
        The server ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {"ServerId": server_id}
    if protocols is not None:
        kwargs["Protocols"] = protocols
    if endpoint_type is not None:
        kwargs["EndpointType"] = endpoint_type
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.update_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_server failed") from exc
    return resp["ServerId"]


def delete_server(
    server_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Transfer Family server.

    Args:
        server_id: The server ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.delete_server(ServerId=server_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_server failed") from exc


def start_server(
    server_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Start a stopped Transfer Family server.

    Args:
        server_id: The server ID to start.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.start_server(ServerId=server_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_server failed") from exc


def stop_server(
    server_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Stop a running Transfer Family server.

    Args:
        server_id: The server ID to stop.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.stop_server(ServerId=server_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "stop_server failed") from exc


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


def create_user(
    server_id: str,
    user_name: str,
    role: str,
    *,
    home_directory: str | None = None,
    home_directory_type: str | None = None,
    home_directory_mappings: list[dict[str, str]] | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UserResult:
    """Create a user on a Transfer Family server.

    Args:
        server_id: The server ID.
        user_name: The username.
        role: IAM role ARN for the user.
        home_directory: Home directory path.
        home_directory_type: ``"PATH"`` or ``"LOGICAL"``.
        home_directory_mappings: Logical directory mappings.
        extra_kwargs: Additional CreateUser parameters.
        region_name: AWS region override.

    Returns:
        A :class:`UserResult` for the new user.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {
        "ServerId": server_id,
        "UserName": user_name,
        "Role": role,
    }
    if home_directory is not None:
        kwargs["HomeDirectory"] = home_directory
    if home_directory_type is not None:
        kwargs["HomeDirectoryType"] = home_directory_type
    if home_directory_mappings is not None:
        kwargs["HomeDirectoryMappings"] = home_directory_mappings
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_user failed") from exc
    return UserResult(
        server_id=resp["ServerId"],
        user_name=resp["UserName"],
        arn=resp.get("Arn"),
    )


def describe_user(
    server_id: str,
    user_name: str,
    *,
    region_name: str | None = None,
) -> UserResult:
    """Describe a Transfer Family user.

    Args:
        server_id: The server ID.
        user_name: The username.
        region_name: AWS region override.

    Returns:
        A :class:`UserResult` with full user details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        resp = client.describe_user(ServerId=server_id, UserName=user_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_user failed") from exc
    data = resp["User"]
    data["ServerId"] = resp["ServerId"]
    return _parse_user(data)


def list_users(
    server_id: str,
    *,
    region_name: str | None = None,
) -> list[UserResult]:
    """List users on a Transfer Family server.

    Args:
        server_id: The server ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`UserResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    results: list[UserResult] = []
    kwargs: dict[str, Any] = {"ServerId": server_id}
    try:
        while True:
            resp = client.list_users(**kwargs)
            for u in resp.get("Users", []):
                u["ServerId"] = resp["ServerId"]
                results.append(_parse_user(u))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_users failed") from exc
    return results


def update_user(
    server_id: str,
    user_name: str,
    *,
    home_directory: str | None = None,
    role: str | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Update a Transfer Family user.

    Args:
        server_id: The server ID.
        user_name: The username to update.
        home_directory: New home directory.
        role: New IAM role ARN.
        extra_kwargs: Additional UpdateUser parameters.
        region_name: AWS region override.

    Returns:
        The username.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {"ServerId": server_id, "UserName": user_name}
    if home_directory is not None:
        kwargs["HomeDirectory"] = home_directory
    if role is not None:
        kwargs["Role"] = role
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.update_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_user failed") from exc
    return resp["UserName"]


def delete_user(
    server_id: str,
    user_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Transfer Family user.

    Args:
        server_id: The server ID.
        user_name: The username to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.delete_user(ServerId=server_id, UserName=user_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_user failed") from exc


# ---------------------------------------------------------------------------
# SSH public key operations
# ---------------------------------------------------------------------------


def import_ssh_public_key(
    server_id: str,
    user_name: str,
    ssh_public_key_body: str,
    *,
    region_name: str | None = None,
) -> SshPublicKeyResult:
    """Import an SSH public key for a Transfer Family user.

    Args:
        server_id: The server ID.
        user_name: The username.
        ssh_public_key_body: The SSH public key string.
        region_name: AWS region override.

    Returns:
        A :class:`SshPublicKeyResult` with the key metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        resp = client.import_ssh_public_key(
            ServerId=server_id,
            UserName=user_name,
            SshPublicKeyBody=ssh_public_key_body,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "import_ssh_public_key failed") from exc
    return SshPublicKeyResult(
        server_id=resp["ServerId"],
        user_name=resp["UserName"],
        ssh_public_key_id=resp["SshPublicKeyId"],
    )


def delete_ssh_public_key(
    server_id: str,
    user_name: str,
    ssh_public_key_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an SSH public key from a Transfer Family user.

    Args:
        server_id: The server ID.
        user_name: The username.
        ssh_public_key_id: The SSH public key ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.delete_ssh_public_key(
            ServerId=server_id,
            UserName=user_name,
            SshPublicKeyId=ssh_public_key_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_ssh_public_key failed") from exc


# ---------------------------------------------------------------------------
# Access operations
# ---------------------------------------------------------------------------


def create_access(
    server_id: str,
    external_id: str,
    role: str,
    *,
    home_directory: str | None = None,
    home_directory_type: str | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> AccessResult:
    """Create an external access entry on a Transfer Family server.

    Args:
        server_id: The server ID.
        external_id: External identifier (e.g. directory group SID).
        role: IAM role ARN.
        home_directory: Home directory path.
        home_directory_type: ``"PATH"`` or ``"LOGICAL"``.
        extra_kwargs: Additional CreateAccess parameters.
        region_name: AWS region override.

    Returns:
        An :class:`AccessResult` for the new access entry.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {
        "ServerId": server_id,
        "ExternalId": external_id,
        "Role": role,
    }
    if home_directory is not None:
        kwargs["HomeDirectory"] = home_directory
    if home_directory_type is not None:
        kwargs["HomeDirectoryType"] = home_directory_type
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.create_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_access failed") from exc
    return AccessResult(
        server_id=resp["ServerId"],
        external_id=resp["ExternalId"],
    )


def describe_access(
    server_id: str,
    external_id: str,
    *,
    region_name: str | None = None,
) -> AccessResult:
    """Describe an external access entry.

    Args:
        server_id: The server ID.
        external_id: The external identifier.
        region_name: AWS region override.

    Returns:
        An :class:`AccessResult` with full access details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        resp = client.describe_access(ServerId=server_id, ExternalId=external_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_access failed") from exc
    data = resp["Access"]
    data["ServerId"] = resp["ServerId"]
    data["ExternalId"] = resp["ExternalId"]
    return _parse_access(data)


def list_accesses(
    server_id: str,
    *,
    region_name: str | None = None,
) -> list[AccessResult]:
    """List external access entries on a Transfer Family server.

    Args:
        server_id: The server ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`AccessResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    results: list[AccessResult] = []
    kwargs: dict[str, Any] = {"ServerId": server_id}
    try:
        while True:
            resp = client.list_accesses(**kwargs)
            for a in resp.get("Accesses", []):
                a["ServerId"] = resp["ServerId"]
                results.append(_parse_access(a))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_accesses failed") from exc
    return results


def update_access(
    server_id: str,
    external_id: str,
    *,
    home_directory: str | None = None,
    role: str | None = None,
    extra_kwargs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Update an external access entry.

    Args:
        server_id: The server ID.
        external_id: The external identifier.
        home_directory: New home directory.
        role: New IAM role ARN.
        extra_kwargs: Additional UpdateAccess parameters.
        region_name: AWS region override.

    Returns:
        The external ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {
        "ServerId": server_id,
        "ExternalId": external_id,
    }
    if home_directory is not None:
        kwargs["HomeDirectory"] = home_directory
    if role is not None:
        kwargs["Role"] = role
    if extra_kwargs:
        kwargs.update(extra_kwargs)
    try:
        resp = client.update_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_access failed") from exc
    return resp["ExternalId"]


def delete_access(
    server_id: str,
    external_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an external access entry.

    Args:
        server_id: The server ID.
        external_id: The external identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.delete_access(ServerId=server_id, ExternalId=external_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_access failed") from exc


# ---------------------------------------------------------------------------
# Workflow operations
# ---------------------------------------------------------------------------


def create_workflow(
    steps: list[dict[str, Any]],
    *,
    description: str | None = None,
    on_exception_steps: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> WorkflowResult:
    """Create a Transfer Family workflow.

    Args:
        steps: Workflow step definitions.
        description: Workflow description.
        on_exception_steps: Steps to run on exception.
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`WorkflowResult` for the new workflow.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {"Steps": steps}
    if description is not None:
        kwargs["Description"] = description
    if on_exception_steps is not None:
        kwargs["OnExceptionSteps"] = on_exception_steps
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_workflow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_workflow failed") from exc
    return WorkflowResult(
        workflow_id=resp["WorkflowId"],
        arn=resp.get("Arn"),
    )


def describe_workflow(
    workflow_id: str,
    *,
    region_name: str | None = None,
) -> WorkflowResult:
    """Describe a Transfer Family workflow.

    Args:
        workflow_id: The workflow ID.
        region_name: AWS region override.

    Returns:
        A :class:`WorkflowResult` with full workflow details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        resp = client.describe_workflow(WorkflowId=workflow_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_workflow failed") from exc
    return _parse_workflow(resp["Workflow"])


def list_workflows(
    *,
    region_name: str | None = None,
) -> list[WorkflowResult]:
    """List all Transfer Family workflows.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`WorkflowResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    results: list[WorkflowResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_workflows(**kwargs)
            for w in resp.get("Workflows", []):
                results.append(_parse_workflow(w))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_workflows failed") from exc
    return results


def delete_workflow(
    workflow_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Transfer Family workflow.

    Args:
        workflow_id: The workflow ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.delete_workflow(WorkflowId=workflow_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_workflow failed") from exc


def send_workflow_step_state(
    workflow_id: str,
    execution_id: str,
    token: str,
    status: str,
    *,
    region_name: str | None = None,
) -> None:
    """Send a step state for a workflow execution.

    Args:
        workflow_id: The workflow ID.
        execution_id: The execution ID.
        token: The step callback token.
        status: ``"SUCCESS"`` or ``"FAILURE"``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    try:
        client.send_workflow_step_state(
            WorkflowId=workflow_id,
            ExecutionId=execution_id,
            Token=token,
            Status=status,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "send_workflow_step_state failed") from exc


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


def wait_for_server(
    server_id: str,
    *,
    target_state: str = "ONLINE",
    timeout: float = 300.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> ServerResult:
    """Poll until a Transfer Family server reaches the desired state.

    Args:
        server_id: The server ID to monitor.
        target_state: Desired ``State`` (default ``"ONLINE"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`ServerResult` once it reaches *target_state*.

    Raises:
        AwsTimeoutError: If the server does not reach the target state
            within *timeout* seconds.
    """
    deadline = time.monotonic() + timeout
    while True:
        srv = describe_server(server_id, region_name=region_name)
        if srv.state == target_state:
            return srv
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Server {server_id!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {srv.state!r})"
            )
        time.sleep(poll_interval)


class CreateAgreementResult(BaseModel):
    """Result of create_agreement."""

    model_config = ConfigDict(frozen=True)

    agreement_id: str | None = None


class CreateConnectorResult(BaseModel):
    """Result of create_connector."""

    model_config = ConfigDict(frozen=True)

    connector_id: str | None = None


class CreateProfileResult(BaseModel):
    """Result of create_profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str | None = None


class CreateWebAppResult(BaseModel):
    """Result of create_web_app."""

    model_config = ConfigDict(frozen=True)

    web_app_id: str | None = None


class DescribeAgreementResult(BaseModel):
    """Result of describe_agreement."""

    model_config = ConfigDict(frozen=True)

    agreement: dict[str, Any] | None = None


class DescribeCertificateResult(BaseModel):
    """Result of describe_certificate."""

    model_config = ConfigDict(frozen=True)

    certificate: dict[str, Any] | None = None


class DescribeConnectorResult(BaseModel):
    """Result of describe_connector."""

    model_config = ConfigDict(frozen=True)

    connector: dict[str, Any] | None = None


class DescribeExecutionResult(BaseModel):
    """Result of describe_execution."""

    model_config = ConfigDict(frozen=True)

    workflow_id: str | None = None
    execution: dict[str, Any] | None = None


class DescribeHostKeyResult(BaseModel):
    """Result of describe_host_key."""

    model_config = ConfigDict(frozen=True)

    host_key: dict[str, Any] | None = None


class DescribeProfileResult(BaseModel):
    """Result of describe_profile."""

    model_config = ConfigDict(frozen=True)

    profile: dict[str, Any] | None = None


class DescribeSecurityPolicyResult(BaseModel):
    """Result of describe_security_policy."""

    model_config = ConfigDict(frozen=True)

    security_policy: dict[str, Any] | None = None


class DescribeWebAppResult(BaseModel):
    """Result of describe_web_app."""

    model_config = ConfigDict(frozen=True)

    web_app: dict[str, Any] | None = None


class DescribeWebAppCustomizationResult(BaseModel):
    """Result of describe_web_app_customization."""

    model_config = ConfigDict(frozen=True)

    web_app_customization: dict[str, Any] | None = None


class ImportCertificateResult(BaseModel):
    """Result of import_certificate."""

    model_config = ConfigDict(frozen=True)

    certificate_id: str | None = None


class ImportHostKeyResult(BaseModel):
    """Result of import_host_key."""

    model_config = ConfigDict(frozen=True)

    server_id: str | None = None
    host_key_id: str | None = None


class ListAgreementsResult(BaseModel):
    """Result of list_agreements."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    agreements: list[dict[str, Any]] | None = None


class ListCertificatesResult(BaseModel):
    """Result of list_certificates."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    certificates: list[dict[str, Any]] | None = None


class ListConnectorsResult(BaseModel):
    """Result of list_connectors."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    connectors: list[dict[str, Any]] | None = None


class ListExecutionsResult(BaseModel):
    """Result of list_executions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    workflow_id: str | None = None
    executions: list[dict[str, Any]] | None = None


class ListFileTransferResultsResult(BaseModel):
    """Result of list_file_transfer_results."""

    model_config = ConfigDict(frozen=True)

    file_transfer_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListHostKeysResult(BaseModel):
    """Result of list_host_keys."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    server_id: str | None = None
    host_keys: list[dict[str, Any]] | None = None


class ListProfilesResult(BaseModel):
    """Result of list_profiles."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    profiles: list[dict[str, Any]] | None = None


class ListSecurityPoliciesResult(BaseModel):
    """Result of list_security_policies."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    security_policy_names: list[str] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    next_token: str | None = None
    tags: list[dict[str, Any]] | None = None


class ListWebAppsResult(BaseModel):
    """Result of list_web_apps."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    web_apps: list[dict[str, Any]] | None = None


class RunConnectionResult(BaseModel):
    """Result of run_connection."""

    model_config = ConfigDict(frozen=True)

    connector_id: str | None = None
    status: str | None = None
    status_message: str | None = None
    sftp_connection_details: dict[str, Any] | None = None


class RunIdentityProviderResult(BaseModel):
    """Result of run_identity_provider."""

    model_config = ConfigDict(frozen=True)

    response: str | None = None
    status_code: int | None = None
    message: str | None = None
    url: str | None = None


class StartDirectoryListingResult(BaseModel):
    """Result of start_directory_listing."""

    model_config = ConfigDict(frozen=True)

    listing_id: str | None = None
    output_file_name: str | None = None


class StartFileTransferResult(BaseModel):
    """Result of start_file_transfer."""

    model_config = ConfigDict(frozen=True)

    transfer_id: str | None = None


class StartRemoteDeleteResult(BaseModel):
    """Result of start_remote_delete."""

    model_config = ConfigDict(frozen=True)

    delete_id: str | None = None


class StartRemoteMoveResult(BaseModel):
    """Result of start_remote_move."""

    model_config = ConfigDict(frozen=True)

    move_id: str | None = None


class UpdateAgreementResult(BaseModel):
    """Result of update_agreement."""

    model_config = ConfigDict(frozen=True)

    agreement_id: str | None = None


class UpdateCertificateResult(BaseModel):
    """Result of update_certificate."""

    model_config = ConfigDict(frozen=True)

    certificate_id: str | None = None


class UpdateConnectorResult(BaseModel):
    """Result of update_connector."""

    model_config = ConfigDict(frozen=True)

    connector_id: str | None = None


class UpdateHostKeyResult(BaseModel):
    """Result of update_host_key."""

    model_config = ConfigDict(frozen=True)

    server_id: str | None = None
    host_key_id: str | None = None


class UpdateProfileResult(BaseModel):
    """Result of update_profile."""

    model_config = ConfigDict(frozen=True)

    profile_id: str | None = None


class UpdateWebAppResult(BaseModel):
    """Result of update_web_app."""

    model_config = ConfigDict(frozen=True)

    web_app_id: str | None = None


class UpdateWebAppCustomizationResult(BaseModel):
    """Result of update_web_app_customization."""

    model_config = ConfigDict(frozen=True)

    web_app_id: str | None = None


def create_agreement(
    server_id: str,
    local_profile_id: str,
    partner_profile_id: str,
    access_role: str,
    *,
    description: str | None = None,
    base_directory: str | None = None,
    status: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    preserve_filename: str | None = None,
    enforce_message_signing: str | None = None,
    custom_directories: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAgreementResult:
    """Create agreement.

    Args:
        server_id: Server id.
        local_profile_id: Local profile id.
        partner_profile_id: Partner profile id.
        access_role: Access role.
        description: Description.
        base_directory: Base directory.
        status: Status.
        tags: Tags.
        preserve_filename: Preserve filename.
        enforce_message_signing: Enforce message signing.
        custom_directories: Custom directories.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["LocalProfileId"] = local_profile_id
    kwargs["PartnerProfileId"] = partner_profile_id
    kwargs["AccessRole"] = access_role
    if description is not None:
        kwargs["Description"] = description
    if base_directory is not None:
        kwargs["BaseDirectory"] = base_directory
    if status is not None:
        kwargs["Status"] = status
    if tags is not None:
        kwargs["Tags"] = tags
    if preserve_filename is not None:
        kwargs["PreserveFilename"] = preserve_filename
    if enforce_message_signing is not None:
        kwargs["EnforceMessageSigning"] = enforce_message_signing
    if custom_directories is not None:
        kwargs["CustomDirectories"] = custom_directories
    try:
        resp = client.create_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create agreement") from exc
    return CreateAgreementResult(
        agreement_id=resp.get("AgreementId"),
    )


def create_connector(
    access_role: str,
    *,
    url: str | None = None,
    as2_config: dict[str, Any] | None = None,
    logging_role: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    sftp_config: dict[str, Any] | None = None,
    security_policy_name: str | None = None,
    egress_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateConnectorResult:
    """Create connector.

    Args:
        access_role: Access role.
        url: Url.
        as2_config: As2 config.
        logging_role: Logging role.
        tags: Tags.
        sftp_config: Sftp config.
        security_policy_name: Security policy name.
        egress_config: Egress config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessRole"] = access_role
    if url is not None:
        kwargs["Url"] = url
    if as2_config is not None:
        kwargs["As2Config"] = as2_config
    if logging_role is not None:
        kwargs["LoggingRole"] = logging_role
    if tags is not None:
        kwargs["Tags"] = tags
    if sftp_config is not None:
        kwargs["SftpConfig"] = sftp_config
    if security_policy_name is not None:
        kwargs["SecurityPolicyName"] = security_policy_name
    if egress_config is not None:
        kwargs["EgressConfig"] = egress_config
    try:
        resp = client.create_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create connector") from exc
    return CreateConnectorResult(
        connector_id=resp.get("ConnectorId"),
    )


def create_profile(
    as2_id: str,
    profile_type: str,
    *,
    certificate_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateProfileResult:
    """Create profile.

    Args:
        as2_id: As2 id.
        profile_type: Profile type.
        certificate_ids: Certificate ids.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["As2Id"] = as2_id
    kwargs["ProfileType"] = profile_type
    if certificate_ids is not None:
        kwargs["CertificateIds"] = certificate_ids
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create profile") from exc
    return CreateProfileResult(
        profile_id=resp.get("ProfileId"),
    )


def create_web_app(
    identity_provider_details: dict[str, Any],
    *,
    access_endpoint: str | None = None,
    web_app_units: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    web_app_endpoint_policy: str | None = None,
    region_name: str | None = None,
) -> CreateWebAppResult:
    """Create web app.

    Args:
        identity_provider_details: Identity provider details.
        access_endpoint: Access endpoint.
        web_app_units: Web app units.
        tags: Tags.
        web_app_endpoint_policy: Web app endpoint policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityProviderDetails"] = identity_provider_details
    if access_endpoint is not None:
        kwargs["AccessEndpoint"] = access_endpoint
    if web_app_units is not None:
        kwargs["WebAppUnits"] = web_app_units
    if tags is not None:
        kwargs["Tags"] = tags
    if web_app_endpoint_policy is not None:
        kwargs["WebAppEndpointPolicy"] = web_app_endpoint_policy
    try:
        resp = client.create_web_app(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create web app") from exc
    return CreateWebAppResult(
        web_app_id=resp.get("WebAppId"),
    )


def delete_agreement(
    agreement_id: str,
    server_id: str,
    region_name: str | None = None,
) -> None:
    """Delete agreement.

    Args:
        agreement_id: Agreement id.
        server_id: Server id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AgreementId"] = agreement_id
    kwargs["ServerId"] = server_id
    try:
        client.delete_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete agreement") from exc
    return None


def delete_certificate(
    certificate_id: str,
    region_name: str | None = None,
) -> None:
    """Delete certificate.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateId"] = certificate_id
    try:
        client.delete_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete certificate") from exc
    return None


def delete_connector(
    connector_id: str,
    region_name: str | None = None,
) -> None:
    """Delete connector.

    Args:
        connector_id: Connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        client.delete_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connector") from exc
    return None


def delete_host_key(
    server_id: str,
    host_key_id: str,
    region_name: str | None = None,
) -> None:
    """Delete host key.

    Args:
        server_id: Server id.
        host_key_id: Host key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["HostKeyId"] = host_key_id
    try:
        client.delete_host_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete host key") from exc
    return None


def delete_profile(
    profile_id: str,
    region_name: str | None = None,
) -> None:
    """Delete profile.

    Args:
        profile_id: Profile id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProfileId"] = profile_id
    try:
        client.delete_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete profile") from exc
    return None


def delete_web_app(
    web_app_id: str,
    region_name: str | None = None,
) -> None:
    """Delete web app.

    Args:
        web_app_id: Web app id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    try:
        client.delete_web_app(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete web app") from exc
    return None


def delete_web_app_customization(
    web_app_id: str,
    region_name: str | None = None,
) -> None:
    """Delete web app customization.

    Args:
        web_app_id: Web app id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    try:
        client.delete_web_app_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete web app customization") from exc
    return None


def describe_agreement(
    agreement_id: str,
    server_id: str,
    region_name: str | None = None,
) -> DescribeAgreementResult:
    """Describe agreement.

    Args:
        agreement_id: Agreement id.
        server_id: Server id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AgreementId"] = agreement_id
    kwargs["ServerId"] = server_id
    try:
        resp = client.describe_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe agreement") from exc
    return DescribeAgreementResult(
        agreement=resp.get("Agreement"),
    )


def describe_certificate(
    certificate_id: str,
    region_name: str | None = None,
) -> DescribeCertificateResult:
    """Describe certificate.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateId"] = certificate_id
    try:
        resp = client.describe_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe certificate") from exc
    return DescribeCertificateResult(
        certificate=resp.get("Certificate"),
    )


def describe_connector(
    connector_id: str,
    region_name: str | None = None,
) -> DescribeConnectorResult:
    """Describe connector.

    Args:
        connector_id: Connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        resp = client.describe_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe connector") from exc
    return DescribeConnectorResult(
        connector=resp.get("Connector"),
    )


def describe_execution(
    execution_id: str,
    workflow_id: str,
    region_name: str | None = None,
) -> DescribeExecutionResult:
    """Describe execution.

    Args:
        execution_id: Execution id.
        workflow_id: Workflow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExecutionId"] = execution_id
    kwargs["WorkflowId"] = workflow_id
    try:
        resp = client.describe_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe execution") from exc
    return DescribeExecutionResult(
        workflow_id=resp.get("WorkflowId"),
        execution=resp.get("Execution"),
    )


def describe_host_key(
    server_id: str,
    host_key_id: str,
    region_name: str | None = None,
) -> DescribeHostKeyResult:
    """Describe host key.

    Args:
        server_id: Server id.
        host_key_id: Host key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["HostKeyId"] = host_key_id
    try:
        resp = client.describe_host_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe host key") from exc
    return DescribeHostKeyResult(
        host_key=resp.get("HostKey"),
    )


def describe_profile(
    profile_id: str,
    region_name: str | None = None,
) -> DescribeProfileResult:
    """Describe profile.

    Args:
        profile_id: Profile id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProfileId"] = profile_id
    try:
        resp = client.describe_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe profile") from exc
    return DescribeProfileResult(
        profile=resp.get("Profile"),
    )


def describe_security_policy(
    security_policy_name: str,
    region_name: str | None = None,
) -> DescribeSecurityPolicyResult:
    """Describe security policy.

    Args:
        security_policy_name: Security policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityPolicyName"] = security_policy_name
    try:
        resp = client.describe_security_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe security policy") from exc
    return DescribeSecurityPolicyResult(
        security_policy=resp.get("SecurityPolicy"),
    )


def describe_web_app(
    web_app_id: str,
    region_name: str | None = None,
) -> DescribeWebAppResult:
    """Describe web app.

    Args:
        web_app_id: Web app id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    try:
        resp = client.describe_web_app(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe web app") from exc
    return DescribeWebAppResult(
        web_app=resp.get("WebApp"),
    )


def describe_web_app_customization(
    web_app_id: str,
    region_name: str | None = None,
) -> DescribeWebAppCustomizationResult:
    """Describe web app customization.

    Args:
        web_app_id: Web app id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    try:
        resp = client.describe_web_app_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe web app customization") from exc
    return DescribeWebAppCustomizationResult(
        web_app_customization=resp.get("WebAppCustomization"),
    )


def import_certificate(
    usage: str,
    certificate: str,
    *,
    certificate_chain: str | None = None,
    private_key: str | None = None,
    active_date: str | None = None,
    inactive_date: str | None = None,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportCertificateResult:
    """Import certificate.

    Args:
        usage: Usage.
        certificate: Certificate.
        certificate_chain: Certificate chain.
        private_key: Private key.
        active_date: Active date.
        inactive_date: Inactive date.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Usage"] = usage
    kwargs["Certificate"] = certificate
    if certificate_chain is not None:
        kwargs["CertificateChain"] = certificate_chain
    if private_key is not None:
        kwargs["PrivateKey"] = private_key
    if active_date is not None:
        kwargs["ActiveDate"] = active_date
    if inactive_date is not None:
        kwargs["InactiveDate"] = inactive_date
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.import_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import certificate") from exc
    return ImportCertificateResult(
        certificate_id=resp.get("CertificateId"),
    )


def import_host_key(
    server_id: str,
    host_key_body: str,
    *,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportHostKeyResult:
    """Import host key.

    Args:
        server_id: Server id.
        host_key_body: Host key body.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["HostKeyBody"] = host_key_body
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.import_host_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import host key") from exc
    return ImportHostKeyResult(
        server_id=resp.get("ServerId"),
        host_key_id=resp.get("HostKeyId"),
    )


def list_agreements(
    server_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAgreementsResult:
    """List agreements.

    Args:
        server_id: Server id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_agreements(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agreements") from exc
    return ListAgreementsResult(
        next_token=resp.get("NextToken"),
        agreements=resp.get("Agreements"),
    )


def list_certificates(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCertificatesResult:
    """List certificates.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_certificates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list certificates") from exc
    return ListCertificatesResult(
        next_token=resp.get("NextToken"),
        certificates=resp.get("Certificates"),
    )


def list_connectors(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConnectorsResult:
    """List connectors.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_connectors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list connectors") from exc
    return ListConnectorsResult(
        next_token=resp.get("NextToken"),
        connectors=resp.get("Connectors"),
    )


def list_executions(
    workflow_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListExecutionsResult:
    """List executions.

    Args:
        workflow_id: Workflow id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkflowId"] = workflow_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list executions") from exc
    return ListExecutionsResult(
        next_token=resp.get("NextToken"),
        workflow_id=resp.get("WorkflowId"),
        executions=resp.get("Executions"),
    )


def list_file_transfer_results(
    connector_id: str,
    transfer_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFileTransferResultsResult:
    """List file transfer results.

    Args:
        connector_id: Connector id.
        transfer_id: Transfer id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["TransferId"] = transfer_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_file_transfer_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list file transfer results") from exc
    return ListFileTransferResultsResult(
        file_transfer_results=resp.get("FileTransferResults"),
        next_token=resp.get("NextToken"),
    )


def list_host_keys(
    server_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListHostKeysResult:
    """List host keys.

    Args:
        server_id: Server id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_host_keys(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list host keys") from exc
    return ListHostKeysResult(
        next_token=resp.get("NextToken"),
        server_id=resp.get("ServerId"),
        host_keys=resp.get("HostKeys"),
    )


def list_profiles(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    profile_type: str | None = None,
    region_name: str | None = None,
) -> ListProfilesResult:
    """List profiles.

    Args:
        max_results: Max results.
        next_token: Next token.
        profile_type: Profile type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if profile_type is not None:
        kwargs["ProfileType"] = profile_type
    try:
        resp = client.list_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list profiles") from exc
    return ListProfilesResult(
        next_token=resp.get("NextToken"),
        profiles=resp.get("Profiles"),
    )


def list_security_policies(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSecurityPoliciesResult:
    """List security policies.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_security_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security policies") from exc
    return ListSecurityPoliciesResult(
        next_token=resp.get("NextToken"),
        security_policy_names=resp.get("SecurityPolicyNames"),
    )


def list_tags_for_resource(
    arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        arn: Arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        arn=resp.get("Arn"),
        next_token=resp.get("NextToken"),
        tags=resp.get("Tags"),
    )


def list_web_apps(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListWebAppsResult:
    """List web apps.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_web_apps(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list web apps") from exc
    return ListWebAppsResult(
        next_token=resp.get("NextToken"),
        web_apps=resp.get("WebApps"),
    )


def run_connection(
    connector_id: str,
    region_name: str | None = None,
) -> RunConnectionResult:
    """Run connection.

    Args:
        connector_id: Connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        resp = client.test_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run connection") from exc
    return RunConnectionResult(
        connector_id=resp.get("ConnectorId"),
        status=resp.get("Status"),
        status_message=resp.get("StatusMessage"),
        sftp_connection_details=resp.get("SftpConnectionDetails"),
    )


def run_identity_provider(
    server_id: str,
    user_name: str,
    *,
    server_protocol: str | None = None,
    source_ip: str | None = None,
    user_password: str | None = None,
    region_name: str | None = None,
) -> RunIdentityProviderResult:
    """Run identity provider.

    Args:
        server_id: Server id.
        user_name: User name.
        server_protocol: Server protocol.
        source_ip: Source ip.
        user_password: User password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["UserName"] = user_name
    if server_protocol is not None:
        kwargs["ServerProtocol"] = server_protocol
    if source_ip is not None:
        kwargs["SourceIp"] = source_ip
    if user_password is not None:
        kwargs["UserPassword"] = user_password
    try:
        resp = client.test_identity_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run identity provider") from exc
    return RunIdentityProviderResult(
        response=resp.get("Response"),
        status_code=resp.get("StatusCode"),
        message=resp.get("Message"),
        url=resp.get("Url"),
    )


def start_directory_listing(
    connector_id: str,
    remote_directory_path: str,
    output_directory_path: str,
    *,
    max_items: int | None = None,
    region_name: str | None = None,
) -> StartDirectoryListingResult:
    """Start directory listing.

    Args:
        connector_id: Connector id.
        remote_directory_path: Remote directory path.
        output_directory_path: Output directory path.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["RemoteDirectoryPath"] = remote_directory_path
    kwargs["OutputDirectoryPath"] = output_directory_path
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.start_directory_listing(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start directory listing") from exc
    return StartDirectoryListingResult(
        listing_id=resp.get("ListingId"),
        output_file_name=resp.get("OutputFileName"),
    )


def start_file_transfer(
    connector_id: str,
    *,
    send_file_paths: list[str] | None = None,
    retrieve_file_paths: list[str] | None = None,
    local_directory_path: str | None = None,
    remote_directory_path: str | None = None,
    region_name: str | None = None,
) -> StartFileTransferResult:
    """Start file transfer.

    Args:
        connector_id: Connector id.
        send_file_paths: Send file paths.
        retrieve_file_paths: Retrieve file paths.
        local_directory_path: Local directory path.
        remote_directory_path: Remote directory path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    if send_file_paths is not None:
        kwargs["SendFilePaths"] = send_file_paths
    if retrieve_file_paths is not None:
        kwargs["RetrieveFilePaths"] = retrieve_file_paths
    if local_directory_path is not None:
        kwargs["LocalDirectoryPath"] = local_directory_path
    if remote_directory_path is not None:
        kwargs["RemoteDirectoryPath"] = remote_directory_path
    try:
        resp = client.start_file_transfer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start file transfer") from exc
    return StartFileTransferResult(
        transfer_id=resp.get("TransferId"),
    )


def start_remote_delete(
    connector_id: str,
    delete_path: str,
    region_name: str | None = None,
) -> StartRemoteDeleteResult:
    """Start remote delete.

    Args:
        connector_id: Connector id.
        delete_path: Delete path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["DeletePath"] = delete_path
    try:
        resp = client.start_remote_delete(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start remote delete") from exc
    return StartRemoteDeleteResult(
        delete_id=resp.get("DeleteId"),
    )


def start_remote_move(
    connector_id: str,
    source_path: str,
    target_path: str,
    region_name: str | None = None,
) -> StartRemoteMoveResult:
    """Start remote move.

    Args:
        connector_id: Connector id.
        source_path: Source path.
        target_path: Target path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["SourcePath"] = source_path
    kwargs["TargetPath"] = target_path
    try:
        resp = client.start_remote_move(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start remote move") from exc
    return StartRemoteMoveResult(
        move_id=resp.get("MoveId"),
    )


def tag_resource(
    arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        arn: Arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        arn: Arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_agreement(
    agreement_id: str,
    server_id: str,
    *,
    description: str | None = None,
    status: str | None = None,
    local_profile_id: str | None = None,
    partner_profile_id: str | None = None,
    base_directory: str | None = None,
    access_role: str | None = None,
    preserve_filename: str | None = None,
    enforce_message_signing: str | None = None,
    custom_directories: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateAgreementResult:
    """Update agreement.

    Args:
        agreement_id: Agreement id.
        server_id: Server id.
        description: Description.
        status: Status.
        local_profile_id: Local profile id.
        partner_profile_id: Partner profile id.
        base_directory: Base directory.
        access_role: Access role.
        preserve_filename: Preserve filename.
        enforce_message_signing: Enforce message signing.
        custom_directories: Custom directories.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AgreementId"] = agreement_id
    kwargs["ServerId"] = server_id
    if description is not None:
        kwargs["Description"] = description
    if status is not None:
        kwargs["Status"] = status
    if local_profile_id is not None:
        kwargs["LocalProfileId"] = local_profile_id
    if partner_profile_id is not None:
        kwargs["PartnerProfileId"] = partner_profile_id
    if base_directory is not None:
        kwargs["BaseDirectory"] = base_directory
    if access_role is not None:
        kwargs["AccessRole"] = access_role
    if preserve_filename is not None:
        kwargs["PreserveFilename"] = preserve_filename
    if enforce_message_signing is not None:
        kwargs["EnforceMessageSigning"] = enforce_message_signing
    if custom_directories is not None:
        kwargs["CustomDirectories"] = custom_directories
    try:
        resp = client.update_agreement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agreement") from exc
    return UpdateAgreementResult(
        agreement_id=resp.get("AgreementId"),
    )


def update_certificate(
    certificate_id: str,
    *,
    active_date: str | None = None,
    inactive_date: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateCertificateResult:
    """Update certificate.

    Args:
        certificate_id: Certificate id.
        active_date: Active date.
        inactive_date: Inactive date.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateId"] = certificate_id
    if active_date is not None:
        kwargs["ActiveDate"] = active_date
    if inactive_date is not None:
        kwargs["InactiveDate"] = inactive_date
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update certificate") from exc
    return UpdateCertificateResult(
        certificate_id=resp.get("CertificateId"),
    )


def update_connector(
    connector_id: str,
    *,
    url: str | None = None,
    as2_config: dict[str, Any] | None = None,
    access_role: str | None = None,
    logging_role: str | None = None,
    sftp_config: dict[str, Any] | None = None,
    security_policy_name: str | None = None,
    egress_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateConnectorResult:
    """Update connector.

    Args:
        connector_id: Connector id.
        url: Url.
        as2_config: As2 config.
        access_role: Access role.
        logging_role: Logging role.
        sftp_config: Sftp config.
        security_policy_name: Security policy name.
        egress_config: Egress config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    if url is not None:
        kwargs["Url"] = url
    if as2_config is not None:
        kwargs["As2Config"] = as2_config
    if access_role is not None:
        kwargs["AccessRole"] = access_role
    if logging_role is not None:
        kwargs["LoggingRole"] = logging_role
    if sftp_config is not None:
        kwargs["SftpConfig"] = sftp_config
    if security_policy_name is not None:
        kwargs["SecurityPolicyName"] = security_policy_name
    if egress_config is not None:
        kwargs["EgressConfig"] = egress_config
    try:
        resp = client.update_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update connector") from exc
    return UpdateConnectorResult(
        connector_id=resp.get("ConnectorId"),
    )


def update_host_key(
    server_id: str,
    host_key_id: str,
    description: str,
    region_name: str | None = None,
) -> UpdateHostKeyResult:
    """Update host key.

    Args:
        server_id: Server id.
        host_key_id: Host key id.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerId"] = server_id
    kwargs["HostKeyId"] = host_key_id
    kwargs["Description"] = description
    try:
        resp = client.update_host_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update host key") from exc
    return UpdateHostKeyResult(
        server_id=resp.get("ServerId"),
        host_key_id=resp.get("HostKeyId"),
    )


def update_profile(
    profile_id: str,
    *,
    certificate_ids: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateProfileResult:
    """Update profile.

    Args:
        profile_id: Profile id.
        certificate_ids: Certificate ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProfileId"] = profile_id
    if certificate_ids is not None:
        kwargs["CertificateIds"] = certificate_ids
    try:
        resp = client.update_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update profile") from exc
    return UpdateProfileResult(
        profile_id=resp.get("ProfileId"),
    )


def update_web_app(
    web_app_id: str,
    *,
    identity_provider_details: dict[str, Any] | None = None,
    access_endpoint: str | None = None,
    web_app_units: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateWebAppResult:
    """Update web app.

    Args:
        web_app_id: Web app id.
        identity_provider_details: Identity provider details.
        access_endpoint: Access endpoint.
        web_app_units: Web app units.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    if identity_provider_details is not None:
        kwargs["IdentityProviderDetails"] = identity_provider_details
    if access_endpoint is not None:
        kwargs["AccessEndpoint"] = access_endpoint
    if web_app_units is not None:
        kwargs["WebAppUnits"] = web_app_units
    try:
        resp = client.update_web_app(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update web app") from exc
    return UpdateWebAppResult(
        web_app_id=resp.get("WebAppId"),
    )


def update_web_app_customization(
    web_app_id: str,
    *,
    title: str | None = None,
    logo_file: bytes | None = None,
    favicon_file: bytes | None = None,
    region_name: str | None = None,
) -> UpdateWebAppCustomizationResult:
    """Update web app customization.

    Args:
        web_app_id: Web app id.
        title: Title.
        logo_file: Logo file.
        favicon_file: Favicon file.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transfer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebAppId"] = web_app_id
    if title is not None:
        kwargs["Title"] = title
    if logo_file is not None:
        kwargs["LogoFile"] = logo_file
    if favicon_file is not None:
        kwargs["FaviconFile"] = favicon_file
    try:
        resp = client.update_web_app_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update web app customization") from exc
    return UpdateWebAppCustomizationResult(
        web_app_id=resp.get("WebAppId"),
    )
