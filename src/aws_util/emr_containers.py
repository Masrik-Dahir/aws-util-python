"""aws_util.emr_containers — Amazon EMR on EKS (EMR Containers) utilities.

Provides convenience wrappers around EMR Containers virtual cluster and job
run management operations with Pydantic-modelled results.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CreateJobTemplateResult",
    "CreateManagedEndpointResult",
    "CreateSecurityConfigurationResult",
    "DeleteJobTemplateResult",
    "DeleteManagedEndpointResult",
    "DescribeJobTemplateResult",
    "DescribeManagedEndpointResult",
    "DescribeSecurityConfigurationResult",
    "GetManagedEndpointSessionCredentialsResult",
    "JobRunResult",
    "ListJobTemplatesResult",
    "ListManagedEndpointsResult",
    "ListSecurityConfigurationsResult",
    "ListTagsForResourceResult",
    "VirtualClusterResult",
    "cancel_job_run",
    "create_job_template",
    "create_managed_endpoint",
    "create_security_configuration",
    "create_virtual_cluster",
    "delete_job_template",
    "delete_managed_endpoint",
    "delete_virtual_cluster",
    "describe_job_run",
    "describe_job_template",
    "describe_managed_endpoint",
    "describe_security_configuration",
    "describe_virtual_cluster",
    "get_managed_endpoint_session_credentials",
    "list_job_runs",
    "list_job_templates",
    "list_managed_endpoints",
    "list_security_configurations",
    "list_tags_for_resource",
    "list_virtual_clusters",
    "start_job_run",
    "tag_resource",
    "untag_resource",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class VirtualClusterResult(BaseModel):
    """Metadata for an EMR Containers virtual cluster."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    id: str
    name: str
    arn: str = ""
    state: str = ""
    container_provider: dict[str, Any] = {}
    created_at: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class JobRunResult(BaseModel):
    """Metadata for an EMR Containers job run."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    id: str
    name: str = ""
    virtual_cluster_id: str = ""
    arn: str = ""
    state: str = ""
    state_details: str | None = None
    execution_role_arn: str | None = None
    release_label: str | None = None
    created_at: str | None = None
    finished_at: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_VC_FIELDS = {
    "id",
    "name",
    "arn",
    "state",
    "containerProvider",
    "createdAt",
    "tags",
}

_JR_FIELDS = {
    "id",
    "name",
    "virtualClusterId",
    "arn",
    "state",
    "stateDetails",
    "executionRoleArn",
    "releaseLabel",
    "createdAt",
    "finishedAt",
}


def _parse_virtual_cluster(data: dict[str, Any]) -> VirtualClusterResult:
    """Parse a raw EMR Containers virtual cluster dict."""
    created = data.get("createdAt")
    return VirtualClusterResult(
        id=data.get("id", ""),
        name=data.get("name", ""),
        arn=data.get("arn", ""),
        state=data.get("state", ""),
        container_provider=data.get("containerProvider", {}),
        created_at=str(created) if created is not None else None,
        tags=data.get("tags", {}),
        extra={k: v for k, v in data.items() if k not in _VC_FIELDS},
    )


def _parse_job_run(data: dict[str, Any]) -> JobRunResult:
    """Parse a raw EMR Containers job run dict."""
    created = data.get("createdAt")
    finished = data.get("finishedAt")
    return JobRunResult(
        id=data.get("id", ""),
        name=data.get("name", ""),
        virtual_cluster_id=data.get("virtualClusterId", ""),
        arn=data.get("arn", ""),
        state=data.get("state", ""),
        state_details=data.get("stateDetails"),
        execution_role_arn=data.get("executionRoleArn"),
        release_label=data.get("releaseLabel"),
        created_at=str(created) if created is not None else None,
        finished_at=str(finished) if finished is not None else None,
        extra={k: v for k, v in data.items() if k not in _JR_FIELDS},
    )


# ---------------------------------------------------------------------------
# Virtual cluster operations
# ---------------------------------------------------------------------------


def create_virtual_cluster(
    name: str,
    *,
    container_provider: dict[str, Any],
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> VirtualClusterResult:
    """Create an EMR Containers virtual cluster.

    Args:
        name: Name for the virtual cluster.
        container_provider: Container provider configuration (EKS info).
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`VirtualClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "containerProvider": container_provider,
    }
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_virtual_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_virtual_cluster failed for {name!r}") from exc
    return VirtualClusterResult(
        id=resp.get("id", ""),
        name=resp.get("name", name),
        arn=resp.get("arn", ""),
    )


def describe_virtual_cluster(
    virtual_cluster_id: str,
    *,
    region_name: str | None = None,
) -> VirtualClusterResult:
    """Describe an EMR Containers virtual cluster.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        region_name: AWS region override.

    Returns:
        A :class:`VirtualClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    try:
        resp = client.describe_virtual_cluster(id=virtual_cluster_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"describe_virtual_cluster failed for {virtual_cluster_id!r}"
        ) from exc
    return _parse_virtual_cluster(resp.get("virtualCluster", {}))


def list_virtual_clusters(
    *,
    region_name: str | None = None,
) -> list[VirtualClusterResult]:
    """List all EMR Containers virtual clusters.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`VirtualClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    clusters: list[VirtualClusterResult] = []
    try:
        paginator = client.get_paginator("list_virtual_clusters")
        for page in paginator.paginate():
            for item in page.get("virtualClusters", []):
                clusters.append(_parse_virtual_cluster(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_virtual_clusters failed") from exc
    return clusters


def delete_virtual_cluster(
    virtual_cluster_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Delete an EMR Containers virtual cluster.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        region_name: AWS region override.

    Returns:
        A dict with the virtual cluster id.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    try:
        client.delete_virtual_cluster(id=virtual_cluster_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"delete_virtual_cluster failed for {virtual_cluster_id!r}"
        ) from exc
    return {"id": virtual_cluster_id}


# ---------------------------------------------------------------------------
# Job run operations
# ---------------------------------------------------------------------------


def start_job_run(
    virtual_cluster_id: str,
    *,
    name: str,
    execution_role_arn: str,
    release_label: str,
    job_driver: dict[str, Any],
    configuration_overrides: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> JobRunResult:
    """Start a job run on an EMR Containers virtual cluster.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        name: Name for the job run.
        execution_role_arn: IAM role ARN for execution.
        release_label: EMR release label.
        job_driver: Job driver configuration.
        configuration_overrides: Optional configuration overrides.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`JobRunResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {
        "virtualClusterId": virtual_cluster_id,
        "name": name,
        "executionRoleArn": execution_role_arn,
        "releaseLabel": release_label,
        "jobDriver": job_driver,
    }
    if configuration_overrides is not None:
        kwargs["configurationOverrides"] = configuration_overrides
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.start_job_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"start_job_run failed for cluster {virtual_cluster_id!r}"
        ) from exc
    return JobRunResult(
        id=resp.get("id", ""),
        name=resp.get("name", name),
        virtual_cluster_id=resp.get("virtualClusterId", virtual_cluster_id),
        arn=resp.get("arn", ""),
    )


def describe_job_run(
    virtual_cluster_id: str,
    job_run_id: str,
    *,
    region_name: str | None = None,
) -> JobRunResult:
    """Describe an EMR Containers job run.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        job_run_id: ID of the job run.
        region_name: AWS region override.

    Returns:
        A :class:`JobRunResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    try:
        resp = client.describe_job_run(virtualClusterId=virtual_cluster_id, id=job_run_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_job_run failed for {job_run_id!r}") from exc
    return _parse_job_run(resp.get("jobRun", {}))


def list_job_runs(
    virtual_cluster_id: str,
    *,
    region_name: str | None = None,
) -> list[JobRunResult]:
    """List job runs for an EMR Containers virtual cluster.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobRunResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    runs: list[JobRunResult] = []
    try:
        paginator = client.get_paginator("list_job_runs")
        for page in paginator.paginate(virtualClusterId=virtual_cluster_id):
            for item in page.get("jobRuns", []):
                runs.append(_parse_job_run(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_job_runs failed") from exc
    return runs


def cancel_job_run(
    virtual_cluster_id: str,
    job_run_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Cancel an EMR Containers job run.

    Args:
        virtual_cluster_id: ID of the virtual cluster.
        job_run_id: ID of the job run to cancel.
        region_name: AWS region override.

    Returns:
        A dict with virtual_cluster_id and id.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    try:
        client.cancel_job_run(virtualClusterId=virtual_cluster_id, id=job_run_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"cancel_job_run failed for {job_run_id!r}") from exc
    return {"virtual_cluster_id": virtual_cluster_id, "id": job_run_id}


class CreateJobTemplateResult(BaseModel):
    """Result of create_job_template."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    created_at: str | None = None


class CreateManagedEndpointResult(BaseModel):
    """Result of create_managed_endpoint."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    virtual_cluster_id: str | None = None


class CreateSecurityConfigurationResult(BaseModel):
    """Result of create_security_configuration."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None


class DeleteJobTemplateResult(BaseModel):
    """Result of delete_job_template."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None


class DeleteManagedEndpointResult(BaseModel):
    """Result of delete_managed_endpoint."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    virtual_cluster_id: str | None = None


class DescribeJobTemplateResult(BaseModel):
    """Result of describe_job_template."""

    model_config = ConfigDict(frozen=True)

    job_template: dict[str, Any] | None = None


class DescribeManagedEndpointResult(BaseModel):
    """Result of describe_managed_endpoint."""

    model_config = ConfigDict(frozen=True)

    endpoint: dict[str, Any] | None = None


class DescribeSecurityConfigurationResult(BaseModel):
    """Result of describe_security_configuration."""

    model_config = ConfigDict(frozen=True)

    security_configuration: dict[str, Any] | None = None


class GetManagedEndpointSessionCredentialsResult(BaseModel):
    """Result of get_managed_endpoint_session_credentials."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    credentials: dict[str, Any] | None = None
    expires_at: str | None = None


class ListJobTemplatesResult(BaseModel):
    """Result of list_job_templates."""

    model_config = ConfigDict(frozen=True)

    templates: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListManagedEndpointsResult(BaseModel):
    """Result of list_managed_endpoints."""

    model_config = ConfigDict(frozen=True)

    endpoints: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSecurityConfigurationsResult(BaseModel):
    """Result of list_security_configurations."""

    model_config = ConfigDict(frozen=True)

    security_configurations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


def create_job_template(
    name: str,
    client_token: str,
    job_template_data: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    kms_key_arn: str | None = None,
    region_name: str | None = None,
) -> CreateJobTemplateResult:
    """Create job template.

    Args:
        name: Name.
        client_token: Client token.
        job_template_data: Job template data.
        tags: Tags.
        kms_key_arn: Kms key arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["clientToken"] = client_token
    kwargs["jobTemplateData"] = job_template_data
    if tags is not None:
        kwargs["tags"] = tags
    if kms_key_arn is not None:
        kwargs["kmsKeyArn"] = kms_key_arn
    try:
        resp = client.create_job_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create job template") from exc
    return CreateJobTemplateResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
    )


def create_managed_endpoint(
    name: str,
    virtual_cluster_id: str,
    type_value: str,
    release_label: str,
    execution_role_arn: str,
    client_token: str,
    *,
    certificate_arn: str | None = None,
    configuration_overrides: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateManagedEndpointResult:
    """Create managed endpoint.

    Args:
        name: Name.
        virtual_cluster_id: Virtual cluster id.
        type_value: Type value.
        release_label: Release label.
        execution_role_arn: Execution role arn.
        client_token: Client token.
        certificate_arn: Certificate arn.
        configuration_overrides: Configuration overrides.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["virtualClusterId"] = virtual_cluster_id
    kwargs["type"] = type_value
    kwargs["releaseLabel"] = release_label
    kwargs["executionRoleArn"] = execution_role_arn
    kwargs["clientToken"] = client_token
    if certificate_arn is not None:
        kwargs["certificateArn"] = certificate_arn
    if configuration_overrides is not None:
        kwargs["configurationOverrides"] = configuration_overrides
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_managed_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create managed endpoint") from exc
    return CreateManagedEndpointResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        virtual_cluster_id=resp.get("virtualClusterId"),
    )


def create_security_configuration(
    client_token: str,
    name: str,
    security_configuration_data: dict[str, Any],
    *,
    container_provider: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateSecurityConfigurationResult:
    """Create security configuration.

    Args:
        client_token: Client token.
        name: Name.
        security_configuration_data: Security configuration data.
        container_provider: Container provider.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientToken"] = client_token
    kwargs["name"] = name
    kwargs["securityConfigurationData"] = security_configuration_data
    if container_provider is not None:
        kwargs["containerProvider"] = container_provider
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_security_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create security configuration") from exc
    return CreateSecurityConfigurationResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
    )


def delete_job_template(
    id: str,
    region_name: str | None = None,
) -> DeleteJobTemplateResult:
    """Delete job template.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.delete_job_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete job template") from exc
    return DeleteJobTemplateResult(
        id=resp.get("id"),
    )


def delete_managed_endpoint(
    id: str,
    virtual_cluster_id: str,
    region_name: str | None = None,
) -> DeleteManagedEndpointResult:
    """Delete managed endpoint.

    Args:
        id: Id.
        virtual_cluster_id: Virtual cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    kwargs["virtualClusterId"] = virtual_cluster_id
    try:
        resp = client.delete_managed_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete managed endpoint") from exc
    return DeleteManagedEndpointResult(
        id=resp.get("id"),
        virtual_cluster_id=resp.get("virtualClusterId"),
    )


def describe_job_template(
    id: str,
    region_name: str | None = None,
) -> DescribeJobTemplateResult:
    """Describe job template.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.describe_job_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe job template") from exc
    return DescribeJobTemplateResult(
        job_template=resp.get("jobTemplate"),
    )


def describe_managed_endpoint(
    id: str,
    virtual_cluster_id: str,
    region_name: str | None = None,
) -> DescribeManagedEndpointResult:
    """Describe managed endpoint.

    Args:
        id: Id.
        virtual_cluster_id: Virtual cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    kwargs["virtualClusterId"] = virtual_cluster_id
    try:
        resp = client.describe_managed_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe managed endpoint") from exc
    return DescribeManagedEndpointResult(
        endpoint=resp.get("endpoint"),
    )


def describe_security_configuration(
    id: str,
    region_name: str | None = None,
) -> DescribeSecurityConfigurationResult:
    """Describe security configuration.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.describe_security_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe security configuration") from exc
    return DescribeSecurityConfigurationResult(
        security_configuration=resp.get("securityConfiguration"),
    )


def get_managed_endpoint_session_credentials(
    endpoint_identifier: str,
    virtual_cluster_identifier: str,
    execution_role_arn: str,
    credential_type: str,
    *,
    duration_in_seconds: int | None = None,
    log_context: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> GetManagedEndpointSessionCredentialsResult:
    """Get managed endpoint session credentials.

    Args:
        endpoint_identifier: Endpoint identifier.
        virtual_cluster_identifier: Virtual cluster identifier.
        execution_role_arn: Execution role arn.
        credential_type: Credential type.
        duration_in_seconds: Duration in seconds.
        log_context: Log context.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointIdentifier"] = endpoint_identifier
    kwargs["virtualClusterIdentifier"] = virtual_cluster_identifier
    kwargs["executionRoleArn"] = execution_role_arn
    kwargs["credentialType"] = credential_type
    if duration_in_seconds is not None:
        kwargs["durationInSeconds"] = duration_in_seconds
    if log_context is not None:
        kwargs["logContext"] = log_context
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.get_managed_endpoint_session_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get managed endpoint session credentials") from exc
    return GetManagedEndpointSessionCredentialsResult(
        id=resp.get("id"),
        credentials=resp.get("credentials"),
        expires_at=resp.get("expiresAt"),
    )


def list_job_templates(
    *,
    created_after: str | None = None,
    created_before: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListJobTemplatesResult:
    """List job templates.

    Args:
        created_after: Created after.
        created_before: Created before.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    if created_after is not None:
        kwargs["createdAfter"] = created_after
    if created_before is not None:
        kwargs["createdBefore"] = created_before
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_job_templates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list job templates") from exc
    return ListJobTemplatesResult(
        templates=resp.get("templates"),
        next_token=resp.get("nextToken"),
    )


def list_managed_endpoints(
    virtual_cluster_id: str,
    *,
    created_before: str | None = None,
    created_after: str | None = None,
    types: list[str] | None = None,
    states: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListManagedEndpointsResult:
    """List managed endpoints.

    Args:
        virtual_cluster_id: Virtual cluster id.
        created_before: Created before.
        created_after: Created after.
        types: Types.
        states: States.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["virtualClusterId"] = virtual_cluster_id
    if created_before is not None:
        kwargs["createdBefore"] = created_before
    if created_after is not None:
        kwargs["createdAfter"] = created_after
    if types is not None:
        kwargs["types"] = types
    if states is not None:
        kwargs["states"] = states
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_managed_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list managed endpoints") from exc
    return ListManagedEndpointsResult(
        endpoints=resp.get("endpoints"),
        next_token=resp.get("nextToken"),
    )


def list_security_configurations(
    *,
    created_after: str | None = None,
    created_before: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSecurityConfigurationsResult:
    """List security configurations.

    Args:
        created_after: Created after.
        created_before: Created before.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    if created_after is not None:
        kwargs["createdAfter"] = created_after
    if created_before is not None:
        kwargs["createdBefore"] = created_before
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_security_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security configurations") from exc
    return ListSecurityConfigurationsResult(
        security_configurations=resp.get("securityConfigurations"),
        next_token=resp.get("nextToken"),
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
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def tag_resource(
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
    client = get_client("emr-containers", region_name)
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
    client = get_client("emr-containers", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
