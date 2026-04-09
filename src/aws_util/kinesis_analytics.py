"""aws_util.kinesis_analytics -- AWS Kinesis Analytics V2 utilities.

Provides helpers for managing Kinesis Data Analytics applications
(also known as Amazon Managed Service for Apache Flink), including
application CRUD, start/stop, input/output management, and updates.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AddApplicationCloudWatchLoggingOptionResult",
    "AddApplicationInputProcessingConfigurationResult",
    "AddApplicationReferenceDataSourceResult",
    "AddApplicationVpcConfigurationResult",
    "ApplicationDetail",
    "ApplicationInputResult",
    "ApplicationOutputResult",
    "ApplicationSummary",
    "CreateApplicationPresignedUrlResult",
    "DeleteApplicationCloudWatchLoggingOptionResult",
    "DeleteApplicationInputProcessingConfigurationResult",
    "DeleteApplicationOutputResult",
    "DeleteApplicationReferenceDataSourceResult",
    "DeleteApplicationVpcConfigurationResult",
    "DescribeApplicationOperationResult",
    "DescribeApplicationSnapshotResult",
    "DescribeApplicationVersionResult",
    "DiscoverInputSchemaResult",
    "ListApplicationOperationsResult",
    "ListApplicationSnapshotsResult",
    "ListApplicationVersionsResult",
    "ListTagsForResourceResult",
    "RollbackApplicationResult",
    "UpdateApplicationMaintenanceConfigurationResult",
    "add_application_cloud_watch_logging_option",
    "add_application_input",
    "add_application_input_processing_configuration",
    "add_application_output",
    "add_application_reference_data_source",
    "add_application_vpc_configuration",
    "create_application",
    "create_application_presigned_url",
    "create_application_snapshot",
    "delete_application",
    "delete_application_cloud_watch_logging_option",
    "delete_application_input_processing_configuration",
    "delete_application_output",
    "delete_application_reference_data_source",
    "delete_application_snapshot",
    "delete_application_vpc_configuration",
    "describe_application",
    "describe_application_operation",
    "describe_application_snapshot",
    "describe_application_version",
    "discover_input_schema",
    "list_application_operations",
    "list_application_snapshots",
    "list_application_versions",
    "list_applications",
    "list_tags_for_resource",
    "rollback_application",
    "start_application",
    "stop_application",
    "tag_resource",
    "untag_resource",
    "update_application",
    "update_application_maintenance_configuration",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ApplicationSummary(BaseModel):
    """Summary metadata for a Kinesis Analytics V2 application."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_name: str
    application_arn: str
    application_status: str
    application_version_id: int | None = None
    runtime_environment: str | None = None


class ApplicationDetail(BaseModel):
    """Detailed metadata for a Kinesis Analytics V2 application."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_name: str
    application_arn: str
    application_status: str
    application_version_id: int
    application_description: str | None = None
    runtime_environment: str | None = None
    service_execution_role: str | None = None
    create_timestamp: Any = None
    last_update_timestamp: Any = None
    application_configuration_description: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


class ApplicationInputResult(BaseModel):
    """Result of adding an application input."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_arn: str
    application_version_id: int
    input_descriptions: list[dict[str, Any]] = []


class ApplicationOutputResult(BaseModel):
    """Result of adding an application output."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_arn: str
    application_version_id: int
    output_descriptions: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_summary(data: dict[str, Any]) -> ApplicationSummary:
    """Convert a raw application summary dict into an ``ApplicationSummary``."""
    return ApplicationSummary(
        application_name=data["ApplicationName"],
        application_arn=data["ApplicationARN"],
        application_status=data.get("ApplicationStatus", "UNKNOWN"),
        application_version_id=data.get("ApplicationVersionId"),
        runtime_environment=data.get("RuntimeEnvironment"),
    )


def _parse_detail(data: dict[str, Any]) -> ApplicationDetail:
    """Convert a raw application detail dict into an ``ApplicationDetail``."""
    known_keys = {
        "ApplicationName",
        "ApplicationARN",
        "ApplicationStatus",
        "ApplicationVersionId",
        "ApplicationDescription",
        "RuntimeEnvironment",
        "ServiceExecutionRole",
        "CreateTimestamp",
        "LastUpdateTimestamp",
        "ApplicationConfigurationDescription",
    }
    return ApplicationDetail(
        application_name=data["ApplicationName"],
        application_arn=data["ApplicationARN"],
        application_status=data.get("ApplicationStatus", "UNKNOWN"),
        application_version_id=data.get("ApplicationVersionId", 0),
        application_description=data.get("ApplicationDescription"),
        runtime_environment=data.get("RuntimeEnvironment"),
        service_execution_role=data.get("ServiceExecutionRole"),
        create_timestamp=data.get("CreateTimestamp"),
        last_update_timestamp=data.get("LastUpdateTimestamp"),
        application_configuration_description=data.get("ApplicationConfigurationDescription"),
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


# ---------------------------------------------------------------------------
# Application CRUD
# ---------------------------------------------------------------------------


def create_application(
    application_name: str,
    *,
    runtime_environment: str,
    service_execution_role: str,
    application_configuration: dict[str, Any] | None = None,
    application_description: str | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ApplicationDetail:
    """Create a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        runtime_environment: Runtime environment (e.g. ``"SQL-1_0"``,
            ``"FLINK-1_15"``, ``"FLINK-1_18"``).
        service_execution_role: IAM role ARN for the application.
        application_configuration: Optional application configuration dict.
        application_description: Optional description.
        tags: Optional list of ``{"Key": ..., "Value": ...}`` tag dicts.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationDetail` for the created application.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {
        "ApplicationName": application_name,
        "RuntimeEnvironment": runtime_environment,
        "ServiceExecutionRole": service_execution_role,
    }
    if application_configuration is not None:
        kwargs["ApplicationConfiguration"] = application_configuration
    if application_description is not None:
        kwargs["ApplicationDescription"] = application_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_application failed for {application_name!r}") from exc
    return _parse_detail(resp["ApplicationDetail"])


def describe_application(
    application_name: str,
    *,
    include_additional_details: bool = False,
    region_name: str | None = None,
) -> ApplicationDetail:
    """Describe a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        include_additional_details: Whether to include additional details
            such as the current application snapshot.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationDetail` with current metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {"ApplicationName": application_name}
    if include_additional_details:
        kwargs["IncludeAdditionalDetails"] = True
    try:
        resp = client.describe_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_application failed for {application_name!r}",
        ) from exc
    return _parse_detail(resp["ApplicationDetail"])


def list_applications(
    *,
    limit: int | None = None,
    region_name: str | None = None,
) -> list[ApplicationSummary]:
    """List Kinesis Analytics V2 applications.

    Args:
        limit: Maximum number of applications to return per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`ApplicationSummary` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    summaries: list[ApplicationSummary] = []
    kwargs: dict[str, Any] = {}
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        while True:
            resp = client.list_applications(**kwargs)
            for app in resp.get("ApplicationSummaries", []):
                summaries.append(_parse_summary(app))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_applications failed") from exc
    return summaries


def delete_application(
    application_name: str,
    *,
    create_timestamp: Any,
    region_name: str | None = None,
) -> None:
    """Delete a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        create_timestamp: The creation timestamp of the application
            (required by the API to prevent accidental deletion).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    try:
        client.delete_application(
            ApplicationName=application_name,
            CreateTimestamp=create_timestamp,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_application failed for {application_name!r}") from exc


# ---------------------------------------------------------------------------
# Start / Stop
# ---------------------------------------------------------------------------


def start_application(
    application_name: str,
    *,
    run_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Start a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        run_configuration: Optional run configuration dict specifying
            input starting positions or Flink run configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {"ApplicationName": application_name}
    if run_configuration is not None:
        kwargs["RunConfiguration"] = run_configuration
    try:
        client.start_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_application failed for {application_name!r}") from exc


def stop_application(
    application_name: str,
    *,
    force: bool = False,
    region_name: str | None = None,
) -> None:
    """Stop a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        force: If ``True``, force-stop the application.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {"ApplicationName": application_name}
    if force:
        kwargs["Force"] = True
    try:
        client.stop_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_application failed for {application_name!r}") from exc


# ---------------------------------------------------------------------------
# Input / Output management
# ---------------------------------------------------------------------------


def add_application_input(
    application_name: str,
    *,
    current_application_version_id: int,
    input_config: dict[str, Any],
    region_name: str | None = None,
) -> ApplicationInputResult:
    """Add a streaming input to a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        current_application_version_id: Current version ID of the application.
        input_config: Input configuration dict describing the streaming
            source and schema.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationInputResult` with the updated input descriptions.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    try:
        resp = client.add_application_input(
            ApplicationName=application_name,
            CurrentApplicationVersionId=current_application_version_id,
            Input=input_config,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"add_application_input failed for {application_name!r}",
        ) from exc
    return ApplicationInputResult(
        application_arn=resp.get("ApplicationARN", ""),
        application_version_id=resp.get("ApplicationVersionId", 0),
        input_descriptions=resp.get("InputDescriptions", []),
    )


def add_application_output(
    application_name: str,
    *,
    current_application_version_id: int,
    output_config: dict[str, Any],
    region_name: str | None = None,
) -> ApplicationOutputResult:
    """Add an output destination to a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        current_application_version_id: Current version ID of the application.
        output_config: Output configuration dict describing the destination
            and schema.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationOutputResult` with the updated output descriptions.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    try:
        resp = client.add_application_output(
            ApplicationName=application_name,
            CurrentApplicationVersionId=current_application_version_id,
            Output=output_config,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"add_application_output failed for {application_name!r}",
        ) from exc
    return ApplicationOutputResult(
        application_arn=resp.get("ApplicationARN", ""),
        application_version_id=resp.get("ApplicationVersionId", 0),
        output_descriptions=resp.get("OutputDescriptions", []),
    )


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


def update_application(
    application_name: str,
    *,
    current_application_version_id: int,
    application_configuration_update: dict[str, Any] | None = None,
    service_execution_role_update: str | None = None,
    run_configuration_update: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ApplicationDetail:
    """Update a Kinesis Analytics V2 application.

    Args:
        application_name: Name of the application.
        current_application_version_id: Current version ID of the application.
        application_configuration_update: Optional configuration update dict.
        service_execution_role_update: Optional new service execution role ARN.
        run_configuration_update: Optional run configuration update dict.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationDetail` for the updated application.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {
        "ApplicationName": application_name,
        "CurrentApplicationVersionId": current_application_version_id,
    }
    if application_configuration_update is not None:
        kwargs["ApplicationConfigurationUpdate"] = application_configuration_update
    if service_execution_role_update is not None:
        kwargs["ServiceExecutionRoleUpdate"] = service_execution_role_update
    if run_configuration_update is not None:
        kwargs["RunConfigurationUpdate"] = run_configuration_update
    try:
        resp = client.update_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_application failed for {application_name!r}") from exc
    return _parse_detail(resp["ApplicationDetail"])


class AddApplicationCloudWatchLoggingOptionResult(BaseModel):
    """Result of add_application_cloud_watch_logging_option."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    cloud_watch_logging_option_descriptions: list[dict[str, Any]] | None = None
    operation_id: str | None = None


class AddApplicationInputProcessingConfigurationResult(BaseModel):
    """Result of add_application_input_processing_configuration."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    input_id: str | None = None
    input_processing_configuration_description: dict[str, Any] | None = None


class AddApplicationReferenceDataSourceResult(BaseModel):
    """Result of add_application_reference_data_source."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    reference_data_source_descriptions: list[dict[str, Any]] | None = None


class AddApplicationVpcConfigurationResult(BaseModel):
    """Result of add_application_vpc_configuration."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    vpc_configuration_description: dict[str, Any] | None = None
    operation_id: str | None = None


class CreateApplicationPresignedUrlResult(BaseModel):
    """Result of create_application_presigned_url."""

    model_config = ConfigDict(frozen=True)

    authorized_url: str | None = None


class DeleteApplicationCloudWatchLoggingOptionResult(BaseModel):
    """Result of delete_application_cloud_watch_logging_option."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    cloud_watch_logging_option_descriptions: list[dict[str, Any]] | None = None
    operation_id: str | None = None


class DeleteApplicationInputProcessingConfigurationResult(BaseModel):
    """Result of delete_application_input_processing_configuration."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None


class DeleteApplicationOutputResult(BaseModel):
    """Result of delete_application_output."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None


class DeleteApplicationReferenceDataSourceResult(BaseModel):
    """Result of delete_application_reference_data_source."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None


class DeleteApplicationVpcConfigurationResult(BaseModel):
    """Result of delete_application_vpc_configuration."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_version_id: int | None = None
    operation_id: str | None = None


class DescribeApplicationOperationResult(BaseModel):
    """Result of describe_application_operation."""

    model_config = ConfigDict(frozen=True)

    application_operation_info_details: dict[str, Any] | None = None


class DescribeApplicationSnapshotResult(BaseModel):
    """Result of describe_application_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_details: dict[str, Any] | None = None


class DescribeApplicationVersionResult(BaseModel):
    """Result of describe_application_version."""

    model_config = ConfigDict(frozen=True)

    application_version_detail: dict[str, Any] | None = None


class DiscoverInputSchemaResult(BaseModel):
    """Result of discover_input_schema."""

    model_config = ConfigDict(frozen=True)

    input_schema: dict[str, Any] | None = None
    parsed_input_records: list[list[str]] | None = None
    processed_input_records: list[str] | None = None
    raw_input_records: list[str] | None = None


class ListApplicationOperationsResult(BaseModel):
    """Result of list_application_operations."""

    model_config = ConfigDict(frozen=True)

    application_operation_info_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationSnapshotsResult(BaseModel):
    """Result of list_application_snapshots."""

    model_config = ConfigDict(frozen=True)

    snapshot_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationVersionsResult(BaseModel):
    """Result of list_application_versions."""

    model_config = ConfigDict(frozen=True)

    application_version_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class RollbackApplicationResult(BaseModel):
    """Result of rollback_application."""

    model_config = ConfigDict(frozen=True)

    application_detail: dict[str, Any] | None = None
    operation_id: str | None = None


class UpdateApplicationMaintenanceConfigurationResult(BaseModel):
    """Result of update_application_maintenance_configuration."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_maintenance_configuration_description: dict[str, Any] | None = None


def add_application_cloud_watch_logging_option(
    application_name: str,
    cloud_watch_logging_option: dict[str, Any],
    *,
    current_application_version_id: int | None = None,
    conditional_token: str | None = None,
    region_name: str | None = None,
) -> AddApplicationCloudWatchLoggingOptionResult:
    """Add application cloud watch logging option.

    Args:
        application_name: Application name.
        cloud_watch_logging_option: Cloud watch logging option.
        current_application_version_id: Current application version id.
        conditional_token: Conditional token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CloudWatchLoggingOption"] = cloud_watch_logging_option
    if current_application_version_id is not None:
        kwargs["CurrentApplicationVersionId"] = current_application_version_id
    if conditional_token is not None:
        kwargs["ConditionalToken"] = conditional_token
    try:
        resp = client.add_application_cloud_watch_logging_option(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add application cloud watch logging option") from exc
    return AddApplicationCloudWatchLoggingOptionResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        cloud_watch_logging_option_descriptions=resp.get("CloudWatchLoggingOptionDescriptions"),
        operation_id=resp.get("OperationId"),
    )


def add_application_input_processing_configuration(
    application_name: str,
    current_application_version_id: int,
    input_id: str,
    input_processing_configuration: dict[str, Any],
    region_name: str | None = None,
) -> AddApplicationInputProcessingConfigurationResult:
    """Add application input processing configuration.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        input_id: Input id.
        input_processing_configuration: Input processing configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    kwargs["InputId"] = input_id
    kwargs["InputProcessingConfiguration"] = input_processing_configuration
    try:
        resp = client.add_application_input_processing_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to add application input processing configuration"
        ) from exc
    return AddApplicationInputProcessingConfigurationResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        input_id=resp.get("InputId"),
        input_processing_configuration_description=resp.get(
            "InputProcessingConfigurationDescription"
        ),
    )


def add_application_reference_data_source(
    application_name: str,
    current_application_version_id: int,
    reference_data_source: dict[str, Any],
    region_name: str | None = None,
) -> AddApplicationReferenceDataSourceResult:
    """Add application reference data source.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        reference_data_source: Reference data source.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    kwargs["ReferenceDataSource"] = reference_data_source
    try:
        resp = client.add_application_reference_data_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add application reference data source") from exc
    return AddApplicationReferenceDataSourceResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        reference_data_source_descriptions=resp.get("ReferenceDataSourceDescriptions"),
    )


def add_application_vpc_configuration(
    application_name: str,
    vpc_configuration: dict[str, Any],
    *,
    current_application_version_id: int | None = None,
    conditional_token: str | None = None,
    region_name: str | None = None,
) -> AddApplicationVpcConfigurationResult:
    """Add application vpc configuration.

    Args:
        application_name: Application name.
        vpc_configuration: Vpc configuration.
        current_application_version_id: Current application version id.
        conditional_token: Conditional token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["VpcConfiguration"] = vpc_configuration
    if current_application_version_id is not None:
        kwargs["CurrentApplicationVersionId"] = current_application_version_id
    if conditional_token is not None:
        kwargs["ConditionalToken"] = conditional_token
    try:
        resp = client.add_application_vpc_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add application vpc configuration") from exc
    return AddApplicationVpcConfigurationResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        vpc_configuration_description=resp.get("VpcConfigurationDescription"),
        operation_id=resp.get("OperationId"),
    )


def create_application_presigned_url(
    application_name: str,
    url_type: str,
    *,
    session_expiration_duration_in_seconds: int | None = None,
    region_name: str | None = None,
) -> CreateApplicationPresignedUrlResult:
    """Create application presigned url.

    Args:
        application_name: Application name.
        url_type: Url type.
        session_expiration_duration_in_seconds: Session expiration duration in seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["UrlType"] = url_type
    if session_expiration_duration_in_seconds is not None:
        kwargs["SessionExpirationDurationInSeconds"] = session_expiration_duration_in_seconds
    try:
        resp = client.create_application_presigned_url(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create application presigned url") from exc
    return CreateApplicationPresignedUrlResult(
        authorized_url=resp.get("AuthorizedUrl"),
    )


def create_application_snapshot(
    application_name: str,
    snapshot_name: str,
    region_name: str | None = None,
) -> None:
    """Create application snapshot.

    Args:
        application_name: Application name.
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["SnapshotName"] = snapshot_name
    try:
        client.create_application_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create application snapshot") from exc
    return None


def delete_application_cloud_watch_logging_option(
    application_name: str,
    cloud_watch_logging_option_id: str,
    *,
    current_application_version_id: int | None = None,
    conditional_token: str | None = None,
    region_name: str | None = None,
) -> DeleteApplicationCloudWatchLoggingOptionResult:
    """Delete application cloud watch logging option.

    Args:
        application_name: Application name.
        cloud_watch_logging_option_id: Cloud watch logging option id.
        current_application_version_id: Current application version id.
        conditional_token: Conditional token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CloudWatchLoggingOptionId"] = cloud_watch_logging_option_id
    if current_application_version_id is not None:
        kwargs["CurrentApplicationVersionId"] = current_application_version_id
    if conditional_token is not None:
        kwargs["ConditionalToken"] = conditional_token
    try:
        resp = client.delete_application_cloud_watch_logging_option(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete application cloud watch logging option"
        ) from exc
    return DeleteApplicationCloudWatchLoggingOptionResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        cloud_watch_logging_option_descriptions=resp.get("CloudWatchLoggingOptionDescriptions"),
        operation_id=resp.get("OperationId"),
    )


def delete_application_input_processing_configuration(
    application_name: str,
    current_application_version_id: int,
    input_id: str,
    region_name: str | None = None,
) -> DeleteApplicationInputProcessingConfigurationResult:
    """Delete application input processing configuration.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        input_id: Input id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    kwargs["InputId"] = input_id
    try:
        resp = client.delete_application_input_processing_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete application input processing configuration"
        ) from exc
    return DeleteApplicationInputProcessingConfigurationResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
    )


def delete_application_output(
    application_name: str,
    current_application_version_id: int,
    output_id: str,
    region_name: str | None = None,
) -> DeleteApplicationOutputResult:
    """Delete application output.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        output_id: Output id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    kwargs["OutputId"] = output_id
    try:
        resp = client.delete_application_output(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application output") from exc
    return DeleteApplicationOutputResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
    )


def delete_application_reference_data_source(
    application_name: str,
    current_application_version_id: int,
    reference_id: str,
    region_name: str | None = None,
) -> DeleteApplicationReferenceDataSourceResult:
    """Delete application reference data source.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        reference_id: Reference id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    kwargs["ReferenceId"] = reference_id
    try:
        resp = client.delete_application_reference_data_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application reference data source") from exc
    return DeleteApplicationReferenceDataSourceResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
    )


def delete_application_snapshot(
    application_name: str,
    snapshot_name: str,
    snapshot_creation_timestamp: str,
    region_name: str | None = None,
) -> None:
    """Delete application snapshot.

    Args:
        application_name: Application name.
        snapshot_name: Snapshot name.
        snapshot_creation_timestamp: Snapshot creation timestamp.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["SnapshotName"] = snapshot_name
    kwargs["SnapshotCreationTimestamp"] = snapshot_creation_timestamp
    try:
        client.delete_application_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application snapshot") from exc
    return None


def delete_application_vpc_configuration(
    application_name: str,
    vpc_configuration_id: str,
    *,
    current_application_version_id: int | None = None,
    conditional_token: str | None = None,
    region_name: str | None = None,
) -> DeleteApplicationVpcConfigurationResult:
    """Delete application vpc configuration.

    Args:
        application_name: Application name.
        vpc_configuration_id: Vpc configuration id.
        current_application_version_id: Current application version id.
        conditional_token: Conditional token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["VpcConfigurationId"] = vpc_configuration_id
    if current_application_version_id is not None:
        kwargs["CurrentApplicationVersionId"] = current_application_version_id
    if conditional_token is not None:
        kwargs["ConditionalToken"] = conditional_token
    try:
        resp = client.delete_application_vpc_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application vpc configuration") from exc
    return DeleteApplicationVpcConfigurationResult(
        application_arn=resp.get("ApplicationARN"),
        application_version_id=resp.get("ApplicationVersionId"),
        operation_id=resp.get("OperationId"),
    )


def describe_application_operation(
    application_name: str,
    operation_id: str,
    region_name: str | None = None,
) -> DescribeApplicationOperationResult:
    """Describe application operation.

    Args:
        application_name: Application name.
        operation_id: Operation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["OperationId"] = operation_id
    try:
        resp = client.describe_application_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application operation") from exc
    return DescribeApplicationOperationResult(
        application_operation_info_details=resp.get("ApplicationOperationInfoDetails"),
    )


def describe_application_snapshot(
    application_name: str,
    snapshot_name: str,
    region_name: str | None = None,
) -> DescribeApplicationSnapshotResult:
    """Describe application snapshot.

    Args:
        application_name: Application name.
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["SnapshotName"] = snapshot_name
    try:
        resp = client.describe_application_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application snapshot") from exc
    return DescribeApplicationSnapshotResult(
        snapshot_details=resp.get("SnapshotDetails"),
    )


def describe_application_version(
    application_name: str,
    application_version_id: int,
    region_name: str | None = None,
) -> DescribeApplicationVersionResult:
    """Describe application version.

    Args:
        application_name: Application name.
        application_version_id: Application version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["ApplicationVersionId"] = application_version_id
    try:
        resp = client.describe_application_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application version") from exc
    return DescribeApplicationVersionResult(
        application_version_detail=resp.get("ApplicationVersionDetail"),
    )


def discover_input_schema(
    service_execution_role: str,
    *,
    resource_arn: str | None = None,
    input_starting_position_configuration: dict[str, Any] | None = None,
    s3_configuration: dict[str, Any] | None = None,
    input_processing_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> DiscoverInputSchemaResult:
    """Discover input schema.

    Args:
        service_execution_role: Service execution role.
        resource_arn: Resource arn.
        input_starting_position_configuration: Input starting position configuration.
        s3_configuration: S3 configuration.
        input_processing_configuration: Input processing configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceExecutionRole"] = service_execution_role
    if resource_arn is not None:
        kwargs["ResourceARN"] = resource_arn
    if input_starting_position_configuration is not None:
        kwargs["InputStartingPositionConfiguration"] = input_starting_position_configuration
    if s3_configuration is not None:
        kwargs["S3Configuration"] = s3_configuration
    if input_processing_configuration is not None:
        kwargs["InputProcessingConfiguration"] = input_processing_configuration
    try:
        resp = client.discover_input_schema(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to discover input schema") from exc
    return DiscoverInputSchemaResult(
        input_schema=resp.get("InputSchema"),
        parsed_input_records=resp.get("ParsedInputRecords"),
        processed_input_records=resp.get("ProcessedInputRecords"),
        raw_input_records=resp.get("RawInputRecords"),
    )


def list_application_operations(
    application_name: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    operation: str | None = None,
    operation_status: str | None = None,
    region_name: str | None = None,
) -> ListApplicationOperationsResult:
    """List application operations.

    Args:
        application_name: Application name.
        limit: Limit.
        next_token: Next token.
        operation: Operation.
        operation_status: Operation status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if operation is not None:
        kwargs["Operation"] = operation
    if operation_status is not None:
        kwargs["OperationStatus"] = operation_status
    try:
        resp = client.list_application_operations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application operations") from exc
    return ListApplicationOperationsResult(
        application_operation_info_list=resp.get("ApplicationOperationInfoList"),
        next_token=resp.get("NextToken"),
    )


def list_application_snapshots(
    application_name: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationSnapshotsResult:
    """List application snapshots.

    Args:
        application_name: Application name.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_snapshots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application snapshots") from exc
    return ListApplicationSnapshotsResult(
        snapshot_summaries=resp.get("SnapshotSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_application_versions(
    application_name: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationVersionsResult:
    """List application versions.

    Args:
        application_name: Application name.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application versions") from exc
    return ListApplicationVersionsResult(
        application_version_summaries=resp.get("ApplicationVersionSummaries"),
        next_token=resp.get("NextToken"),
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
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def rollback_application(
    application_name: str,
    current_application_version_id: int,
    region_name: str | None = None,
) -> RollbackApplicationResult:
    """Rollback application.

    Args:
        application_name: Application name.
        current_application_version_id: Current application version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["CurrentApplicationVersionId"] = current_application_version_id
    try:
        resp = client.rollback_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rollback application") from exc
    return RollbackApplicationResult(
        application_detail=resp.get("ApplicationDetail"),
        operation_id=resp.get("OperationId"),
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
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
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
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_application_maintenance_configuration(
    application_name: str,
    application_maintenance_configuration_update: dict[str, Any],
    region_name: str | None = None,
) -> UpdateApplicationMaintenanceConfigurationResult:
    """Update application maintenance configuration.

    Args:
        application_name: Application name.
        application_maintenance_configuration_update: Application maintenance configuration update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("kinesisanalyticsv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["ApplicationMaintenanceConfigurationUpdate"] = (
        application_maintenance_configuration_update
    )
    try:
        resp = client.update_application_maintenance_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application maintenance configuration") from exc
    return UpdateApplicationMaintenanceConfigurationResult(
        application_arn=resp.get("ApplicationARN"),
        application_maintenance_configuration_description=resp.get(
            "ApplicationMaintenanceConfigurationDescription"
        ),
    )
