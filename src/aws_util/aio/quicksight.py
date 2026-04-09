"""Native async QuickSight utilities using the async engine."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.quicksight import (
    AnalysisResult,
    BatchCreateTopicReviewedAnswerResult,
    BatchDeleteTopicReviewedAnswerResult,
    CancelIngestionResult,
    CreateAccountCustomizationResult,
    CreateAccountSubscriptionResult,
    CreateActionConnectorResult,
    CreateBrandResult,
    CreateCustomPermissionsResult,
    CreateDataSetResult,
    CreateFolderMembershipResult,
    CreateFolderResult,
    CreateGroupMembershipResult,
    CreateGroupResult,
    CreateIamPolicyAssignmentResult,
    CreateIngestionResult,
    CreateNamespaceResult,
    CreateRefreshScheduleResult,
    CreateRoleMembershipResult,
    CreateTemplateAliasResult,
    CreateTemplateResult,
    CreateThemeAliasResult,
    CreateThemeResult,
    CreateTopicRefreshScheduleResult,
    CreateTopicResult,
    CreateVpcConnectionResult,
    DashboardResult,
    DataSetResult,
    DataSourceResult,
    DeleteAccountCustomizationResult,
    DeleteAccountCustomPermissionResult,
    DeleteAccountSubscriptionResult,
    DeleteActionConnectorResult,
    DeleteAnalysisResult,
    DeleteBrandAssignmentResult,
    DeleteBrandResult,
    DeleteCustomPermissionsResult,
    DeleteDataSetRefreshPropertiesResult,
    DeleteDataSetResult,
    DeleteDataSourceResult,
    DeleteDefaultQBusinessApplicationResult,
    DeleteFolderMembershipResult,
    DeleteFolderResult,
    DeleteGroupMembershipResult,
    DeleteGroupResult,
    DeleteIamPolicyAssignmentResult,
    DeleteIdentityPropagationConfigResult,
    DeleteNamespaceResult,
    DeleteRefreshScheduleResult,
    DeleteRoleCustomPermissionResult,
    DeleteRoleMembershipResult,
    DeleteTemplateAliasResult,
    DeleteTemplateResult,
    DeleteThemeAliasResult,
    DeleteThemeResult,
    DeleteTopicRefreshScheduleResult,
    DeleteTopicResult,
    DeleteUserByPrincipalIdResult,
    DeleteUserCustomPermissionResult,
    DeleteVpcConnectionResult,
    DescribeAccountCustomizationResult,
    DescribeAccountCustomPermissionResult,
    DescribeAccountSettingsResult,
    DescribeAccountSubscriptionResult,
    DescribeActionConnectorPermissionsResult,
    DescribeActionConnectorResult,
    DescribeAnalysisDefinitionResult,
    DescribeAnalysisPermissionsResult,
    DescribeAnalysisResult,
    DescribeAssetBundleExportJobResult,
    DescribeAssetBundleImportJobResult,
    DescribeBrandAssignmentResult,
    DescribeBrandPublishedVersionResult,
    DescribeBrandResult,
    DescribeCustomPermissionsResult,
    DescribeDashboardDefinitionResult,
    DescribeDashboardPermissionsResult,
    DescribeDashboardSnapshotJobResult,
    DescribeDashboardSnapshotJobResultResult,
    DescribeDashboardsQaConfigurationResult,
    DescribeDataSetPermissionsResult,
    DescribeDataSetRefreshPropertiesResult,
    DescribeDataSetResult,
    DescribeDataSourcePermissionsResult,
    DescribeDataSourceResult,
    DescribeDefaultQBusinessApplicationResult,
    DescribeFolderPermissionsResult,
    DescribeFolderResolvedPermissionsResult,
    DescribeFolderResult,
    DescribeGroupMembershipResult,
    DescribeGroupResult,
    DescribeIamPolicyAssignmentResult,
    DescribeIngestionResult,
    DescribeIpRestrictionResult,
    DescribeKeyRegistrationResult,
    DescribeNamespaceResult,
    DescribeQPersonalizationConfigurationResult,
    DescribeQuickSightQSearchConfigurationResult,
    DescribeRefreshScheduleResult,
    DescribeRoleCustomPermissionResult,
    DescribeTemplateAliasResult,
    DescribeTemplateDefinitionResult,
    DescribeTemplatePermissionsResult,
    DescribeTemplateResult,
    DescribeThemeAliasResult,
    DescribeThemePermissionsResult,
    DescribeThemeResult,
    DescribeTopicPermissionsResult,
    DescribeTopicRefreshResult,
    DescribeTopicRefreshScheduleResult,
    DescribeTopicResult,
    DescribeVpcConnectionResult,
    GenerateEmbedUrlForAnonymousUserResult,
    GenerateEmbedUrlForRegisteredUserResult,
    GenerateEmbedUrlForRegisteredUserWithIdentityResult,
    GetDashboardEmbedUrlResult,
    GetFlowMetadataResult,
    GetFlowPermissionsResult,
    GetSessionEmbedUrlResult,
    ListActionConnectorsResult,
    ListAssetBundleExportJobsResult,
    ListAssetBundleImportJobsResult,
    ListBrandsResult,
    ListCustomPermissionsResult,
    ListDashboardVersionsResult,
    ListDataSetsResult,
    ListFlowsResult,
    ListFolderMembersResult,
    ListFoldersForResourceResult,
    ListFoldersResult,
    ListGroupMembershipsResult,
    ListGroupsResult,
    ListIamPolicyAssignmentsForUserResult,
    ListIamPolicyAssignmentsResult,
    ListIdentityPropagationConfigsResult,
    ListIngestionsResult,
    ListNamespacesResult,
    ListRefreshSchedulesResult,
    ListRoleMembershipsResult,
    ListTagsForResourceResult,
    ListTemplateAliasesResult,
    ListTemplatesResult,
    ListTemplateVersionsResult,
    ListThemeAliasesResult,
    ListThemesResult,
    ListThemeVersionsResult,
    ListTopicRefreshSchedulesResult,
    ListTopicReviewedAnswersResult,
    ListTopicsResult,
    ListUserGroupsResult,
    ListVpcConnectionsResult,
    PredictQaResultsResult,
    PutDataSetRefreshPropertiesResult,
    QuickSightUser,
    RestoreAnalysisResult,
    SearchActionConnectorsResult,
    SearchAnalysesResult,
    SearchDashboardsResult,
    SearchDataSetsResult,
    SearchDataSourcesResult,
    SearchFlowsResult,
    SearchFoldersResult,
    SearchGroupsResult,
    SearchTopicsResult,
    StartAssetBundleExportJobResult,
    StartAssetBundleImportJobResult,
    StartDashboardSnapshotJobResult,
    StartDashboardSnapshotJobScheduleResult,
    TagResourceResult,
    UntagResourceResult,
    UpdateAccountCustomizationResult,
    UpdateAccountCustomPermissionResult,
    UpdateAccountSettingsResult,
    UpdateActionConnectorPermissionsResult,
    UpdateActionConnectorResult,
    UpdateAnalysisPermissionsResult,
    UpdateAnalysisResult,
    UpdateApplicationWithTokenExchangeGrantResult,
    UpdateBrandAssignmentResult,
    UpdateBrandPublishedVersionResult,
    UpdateBrandResult,
    UpdateCustomPermissionsResult,
    UpdateDashboardLinksResult,
    UpdateDashboardPermissionsResult,
    UpdateDashboardPublishedVersionResult,
    UpdateDashboardResult,
    UpdateDashboardsQaConfigurationResult,
    UpdateDataSetPermissionsResult,
    UpdateDataSetResult,
    UpdateDataSourcePermissionsResult,
    UpdateDataSourceResult,
    UpdateDefaultQBusinessApplicationResult,
    UpdateFlowPermissionsResult,
    UpdateFolderPermissionsResult,
    UpdateFolderResult,
    UpdateGroupResult,
    UpdateIamPolicyAssignmentResult,
    UpdateIdentityPropagationConfigResult,
    UpdateIpRestrictionResult,
    UpdateKeyRegistrationResult,
    UpdatePublicSharingSettingsResult,
    UpdateQPersonalizationConfigurationResult,
    UpdateQuickSightQSearchConfigurationResult,
    UpdateRefreshScheduleResult,
    UpdateRoleCustomPermissionResult,
    UpdateSpiceCapacityConfigurationResult,
    UpdateTemplateAliasResult,
    UpdateTemplatePermissionsResult,
    UpdateTemplateResult,
    UpdateThemeAliasResult,
    UpdateThemePermissionsResult,
    UpdateThemeResult,
    UpdateTopicPermissionsResult,
    UpdateTopicRefreshScheduleResult,
    UpdateTopicResult,
    UpdateUserCustomPermissionResult,
    UpdateUserResult,
    UpdateVpcConnectionResult,
)

__all__ = [
    "AnalysisResult",
    "BatchCreateTopicReviewedAnswerResult",
    "BatchDeleteTopicReviewedAnswerResult",
    "CancelIngestionResult",
    "CreateAccountCustomizationResult",
    "CreateAccountSubscriptionResult",
    "CreateActionConnectorResult",
    "CreateBrandResult",
    "CreateCustomPermissionsResult",
    "CreateDataSetResult",
    "CreateFolderMembershipResult",
    "CreateFolderResult",
    "CreateGroupMembershipResult",
    "CreateGroupResult",
    "CreateIamPolicyAssignmentResult",
    "CreateIngestionResult",
    "CreateNamespaceResult",
    "CreateRefreshScheduleResult",
    "CreateRoleMembershipResult",
    "CreateTemplateAliasResult",
    "CreateTemplateResult",
    "CreateThemeAliasResult",
    "CreateThemeResult",
    "CreateTopicRefreshScheduleResult",
    "CreateTopicResult",
    "CreateVpcConnectionResult",
    "DashboardResult",
    "DataSetResult",
    "DataSourceResult",
    "DeleteAccountCustomPermissionResult",
    "DeleteAccountCustomizationResult",
    "DeleteAccountSubscriptionResult",
    "DeleteActionConnectorResult",
    "DeleteAnalysisResult",
    "DeleteBrandAssignmentResult",
    "DeleteBrandResult",
    "DeleteCustomPermissionsResult",
    "DeleteDataSetRefreshPropertiesResult",
    "DeleteDataSetResult",
    "DeleteDataSourceResult",
    "DeleteDefaultQBusinessApplicationResult",
    "DeleteFolderMembershipResult",
    "DeleteFolderResult",
    "DeleteGroupMembershipResult",
    "DeleteGroupResult",
    "DeleteIamPolicyAssignmentResult",
    "DeleteIdentityPropagationConfigResult",
    "DeleteNamespaceResult",
    "DeleteRefreshScheduleResult",
    "DeleteRoleCustomPermissionResult",
    "DeleteRoleMembershipResult",
    "DeleteTemplateAliasResult",
    "DeleteTemplateResult",
    "DeleteThemeAliasResult",
    "DeleteThemeResult",
    "DeleteTopicRefreshScheduleResult",
    "DeleteTopicResult",
    "DeleteUserByPrincipalIdResult",
    "DeleteUserCustomPermissionResult",
    "DeleteVpcConnectionResult",
    "DescribeAccountCustomPermissionResult",
    "DescribeAccountCustomizationResult",
    "DescribeAccountSettingsResult",
    "DescribeAccountSubscriptionResult",
    "DescribeActionConnectorPermissionsResult",
    "DescribeActionConnectorResult",
    "DescribeAnalysisDefinitionResult",
    "DescribeAnalysisPermissionsResult",
    "DescribeAnalysisResult",
    "DescribeAssetBundleExportJobResult",
    "DescribeAssetBundleImportJobResult",
    "DescribeBrandAssignmentResult",
    "DescribeBrandPublishedVersionResult",
    "DescribeBrandResult",
    "DescribeCustomPermissionsResult",
    "DescribeDashboardDefinitionResult",
    "DescribeDashboardPermissionsResult",
    "DescribeDashboardSnapshotJobResult",
    "DescribeDashboardSnapshotJobResultResult",
    "DescribeDashboardsQaConfigurationResult",
    "DescribeDataSetPermissionsResult",
    "DescribeDataSetRefreshPropertiesResult",
    "DescribeDataSetResult",
    "DescribeDataSourcePermissionsResult",
    "DescribeDataSourceResult",
    "DescribeDefaultQBusinessApplicationResult",
    "DescribeFolderPermissionsResult",
    "DescribeFolderResolvedPermissionsResult",
    "DescribeFolderResult",
    "DescribeGroupMembershipResult",
    "DescribeGroupResult",
    "DescribeIamPolicyAssignmentResult",
    "DescribeIngestionResult",
    "DescribeIpRestrictionResult",
    "DescribeKeyRegistrationResult",
    "DescribeNamespaceResult",
    "DescribeQPersonalizationConfigurationResult",
    "DescribeQuickSightQSearchConfigurationResult",
    "DescribeRefreshScheduleResult",
    "DescribeRoleCustomPermissionResult",
    "DescribeTemplateAliasResult",
    "DescribeTemplateDefinitionResult",
    "DescribeTemplatePermissionsResult",
    "DescribeTemplateResult",
    "DescribeThemeAliasResult",
    "DescribeThemePermissionsResult",
    "DescribeThemeResult",
    "DescribeTopicPermissionsResult",
    "DescribeTopicRefreshResult",
    "DescribeTopicRefreshScheduleResult",
    "DescribeTopicResult",
    "DescribeVpcConnectionResult",
    "GenerateEmbedUrlForAnonymousUserResult",
    "GenerateEmbedUrlForRegisteredUserResult",
    "GenerateEmbedUrlForRegisteredUserWithIdentityResult",
    "GetDashboardEmbedUrlResult",
    "GetFlowMetadataResult",
    "GetFlowPermissionsResult",
    "GetSessionEmbedUrlResult",
    "ListActionConnectorsResult",
    "ListAssetBundleExportJobsResult",
    "ListAssetBundleImportJobsResult",
    "ListBrandsResult",
    "ListCustomPermissionsResult",
    "ListDashboardVersionsResult",
    "ListDataSetsResult",
    "ListFlowsResult",
    "ListFolderMembersResult",
    "ListFoldersForResourceResult",
    "ListFoldersResult",
    "ListGroupMembershipsResult",
    "ListGroupsResult",
    "ListIamPolicyAssignmentsForUserResult",
    "ListIamPolicyAssignmentsResult",
    "ListIdentityPropagationConfigsResult",
    "ListIngestionsResult",
    "ListNamespacesResult",
    "ListRefreshSchedulesResult",
    "ListRoleMembershipsResult",
    "ListTagsForResourceResult",
    "ListTemplateAliasesResult",
    "ListTemplateVersionsResult",
    "ListTemplatesResult",
    "ListThemeAliasesResult",
    "ListThemeVersionsResult",
    "ListThemesResult",
    "ListTopicRefreshSchedulesResult",
    "ListTopicReviewedAnswersResult",
    "ListTopicsResult",
    "ListUserGroupsResult",
    "ListVpcConnectionsResult",
    "PredictQaResultsResult",
    "PutDataSetRefreshPropertiesResult",
    "QuickSightUser",
    "RestoreAnalysisResult",
    "SearchActionConnectorsResult",
    "SearchAnalysesResult",
    "SearchDashboardsResult",
    "SearchDataSetsResult",
    "SearchDataSourcesResult",
    "SearchFlowsResult",
    "SearchFoldersResult",
    "SearchGroupsResult",
    "SearchTopicsResult",
    "StartAssetBundleExportJobResult",
    "StartAssetBundleImportJobResult",
    "StartDashboardSnapshotJobResult",
    "StartDashboardSnapshotJobScheduleResult",
    "TagResourceResult",
    "UntagResourceResult",
    "UpdateAccountCustomPermissionResult",
    "UpdateAccountCustomizationResult",
    "UpdateAccountSettingsResult",
    "UpdateActionConnectorPermissionsResult",
    "UpdateActionConnectorResult",
    "UpdateAnalysisPermissionsResult",
    "UpdateAnalysisResult",
    "UpdateApplicationWithTokenExchangeGrantResult",
    "UpdateBrandAssignmentResult",
    "UpdateBrandPublishedVersionResult",
    "UpdateBrandResult",
    "UpdateCustomPermissionsResult",
    "UpdateDashboardLinksResult",
    "UpdateDashboardPermissionsResult",
    "UpdateDashboardPublishedVersionResult",
    "UpdateDashboardResult",
    "UpdateDashboardsQaConfigurationResult",
    "UpdateDataSetPermissionsResult",
    "UpdateDataSetResult",
    "UpdateDataSourcePermissionsResult",
    "UpdateDataSourceResult",
    "UpdateDefaultQBusinessApplicationResult",
    "UpdateFlowPermissionsResult",
    "UpdateFolderPermissionsResult",
    "UpdateFolderResult",
    "UpdateGroupResult",
    "UpdateIamPolicyAssignmentResult",
    "UpdateIdentityPropagationConfigResult",
    "UpdateIpRestrictionResult",
    "UpdateKeyRegistrationResult",
    "UpdatePublicSharingSettingsResult",
    "UpdateQPersonalizationConfigurationResult",
    "UpdateQuickSightQSearchConfigurationResult",
    "UpdateRefreshScheduleResult",
    "UpdateRoleCustomPermissionResult",
    "UpdateSpiceCapacityConfigurationResult",
    "UpdateTemplateAliasResult",
    "UpdateTemplatePermissionsResult",
    "UpdateTemplateResult",
    "UpdateThemeAliasResult",
    "UpdateThemePermissionsResult",
    "UpdateThemeResult",
    "UpdateTopicPermissionsResult",
    "UpdateTopicRefreshScheduleResult",
    "UpdateTopicResult",
    "UpdateUserCustomPermissionResult",
    "UpdateUserResult",
    "UpdateVpcConnectionResult",
    "batch_create_topic_reviewed_answer",
    "batch_delete_topic_reviewed_answer",
    "cancel_ingestion",
    "create_account_customization",
    "create_account_subscription",
    "create_action_connector",
    "create_analysis",
    "create_brand",
    "create_custom_permissions",
    "create_dashboard",
    "create_data_set",
    "create_data_source",
    "create_dataset",
    "create_folder",
    "create_folder_membership",
    "create_group",
    "create_group_membership",
    "create_iam_policy_assignment",
    "create_ingestion",
    "create_namespace",
    "create_refresh_schedule",
    "create_role_membership",
    "create_template",
    "create_template_alias",
    "create_theme",
    "create_theme_alias",
    "create_topic",
    "create_topic_refresh_schedule",
    "create_vpc_connection",
    "delete_account_custom_permission",
    "delete_account_customization",
    "delete_account_subscription",
    "delete_action_connector",
    "delete_analysis",
    "delete_brand",
    "delete_brand_assignment",
    "delete_custom_permissions",
    "delete_dashboard",
    "delete_data_set",
    "delete_data_set_refresh_properties",
    "delete_data_source",
    "delete_dataset",
    "delete_default_q_business_application",
    "delete_folder",
    "delete_folder_membership",
    "delete_group",
    "delete_group_membership",
    "delete_iam_policy_assignment",
    "delete_identity_propagation_config",
    "delete_namespace",
    "delete_refresh_schedule",
    "delete_role_custom_permission",
    "delete_role_membership",
    "delete_template",
    "delete_template_alias",
    "delete_theme",
    "delete_theme_alias",
    "delete_topic",
    "delete_topic_refresh_schedule",
    "delete_user",
    "delete_user_by_principal_id",
    "delete_user_custom_permission",
    "delete_vpc_connection",
    "describe_account_custom_permission",
    "describe_account_customization",
    "describe_account_settings",
    "describe_account_subscription",
    "describe_action_connector",
    "describe_action_connector_permissions",
    "describe_analysis",
    "describe_analysis_definition",
    "describe_analysis_permissions",
    "describe_asset_bundle_export_job",
    "describe_asset_bundle_import_job",
    "describe_brand",
    "describe_brand_assignment",
    "describe_brand_published_version",
    "describe_custom_permissions",
    "describe_dashboard",
    "describe_dashboard_definition",
    "describe_dashboard_permissions",
    "describe_dashboard_snapshot_job",
    "describe_dashboard_snapshot_job_result",
    "describe_dashboards_qa_configuration",
    "describe_data_set",
    "describe_data_set_permissions",
    "describe_data_set_refresh_properties",
    "describe_data_source",
    "describe_data_source_permissions",
    "describe_dataset",
    "describe_default_q_business_application",
    "describe_folder",
    "describe_folder_permissions",
    "describe_folder_resolved_permissions",
    "describe_group",
    "describe_group_membership",
    "describe_iam_policy_assignment",
    "describe_ingestion",
    "describe_ip_restriction",
    "describe_key_registration",
    "describe_namespace",
    "describe_q_personalization_configuration",
    "describe_quick_sight_q_search_configuration",
    "describe_refresh_schedule",
    "describe_role_custom_permission",
    "describe_template",
    "describe_template_alias",
    "describe_template_definition",
    "describe_template_permissions",
    "describe_theme",
    "describe_theme_alias",
    "describe_theme_permissions",
    "describe_topic",
    "describe_topic_permissions",
    "describe_topic_refresh",
    "describe_topic_refresh_schedule",
    "describe_user",
    "describe_vpc_connection",
    "generate_embed_url_for_anonymous_user",
    "generate_embed_url_for_registered_user",
    "generate_embed_url_for_registered_user_with_identity",
    "get_dashboard_embed_url",
    "get_flow_metadata",
    "get_flow_permissions",
    "get_session_embed_url",
    "list_action_connectors",
    "list_analyses",
    "list_asset_bundle_export_jobs",
    "list_asset_bundle_import_jobs",
    "list_brands",
    "list_custom_permissions",
    "list_dashboard_versions",
    "list_dashboards",
    "list_data_sets",
    "list_data_sources",
    "list_datasets",
    "list_flows",
    "list_folder_members",
    "list_folders",
    "list_folders_for_resource",
    "list_group_memberships",
    "list_groups",
    "list_iam_policy_assignments",
    "list_iam_policy_assignments_for_user",
    "list_identity_propagation_configs",
    "list_ingestions",
    "list_namespaces",
    "list_refresh_schedules",
    "list_role_memberships",
    "list_tags_for_resource",
    "list_template_aliases",
    "list_template_versions",
    "list_templates",
    "list_theme_aliases",
    "list_theme_versions",
    "list_themes",
    "list_topic_refresh_schedules",
    "list_topic_reviewed_answers",
    "list_topics",
    "list_user_groups",
    "list_users",
    "list_vpc_connections",
    "predict_qa_results",
    "put_data_set_refresh_properties",
    "register_user",
    "restore_analysis",
    "search_action_connectors",
    "search_analyses",
    "search_dashboards",
    "search_data_sets",
    "search_data_sources",
    "search_flows",
    "search_folders",
    "search_groups",
    "search_topics",
    "start_asset_bundle_export_job",
    "start_asset_bundle_import_job",
    "start_dashboard_snapshot_job",
    "start_dashboard_snapshot_job_schedule",
    "tag_resource",
    "untag_resource",
    "update_account_custom_permission",
    "update_account_customization",
    "update_account_settings",
    "update_action_connector",
    "update_action_connector_permissions",
    "update_analysis",
    "update_analysis_permissions",
    "update_application_with_token_exchange_grant",
    "update_brand",
    "update_brand_assignment",
    "update_brand_published_version",
    "update_custom_permissions",
    "update_dashboard",
    "update_dashboard_links",
    "update_dashboard_permissions",
    "update_dashboard_published_version",
    "update_dashboards_qa_configuration",
    "update_data_set",
    "update_data_set_permissions",
    "update_data_source",
    "update_data_source_permissions",
    "update_default_q_business_application",
    "update_flow_permissions",
    "update_folder",
    "update_folder_permissions",
    "update_group",
    "update_iam_policy_assignment",
    "update_identity_propagation_config",
    "update_ip_restriction",
    "update_key_registration",
    "update_public_sharing_settings",
    "update_q_personalization_configuration",
    "update_quick_sight_q_search_configuration",
    "update_refresh_schedule",
    "update_role_custom_permission",
    "update_spice_capacity_configuration",
    "update_template",
    "update_template_alias",
    "update_template_permissions",
    "update_theme",
    "update_theme_alias",
    "update_theme_permissions",
    "update_topic",
    "update_topic_permissions",
    "update_topic_refresh_schedule",
    "update_user",
    "update_user_custom_permission",
    "update_vpc_connection",
]


# ---------------------------------------------------------------------------
# Dashboard operations
# ---------------------------------------------------------------------------


async def create_dashboard(
    aws_account_id: str,
    dashboard_id: str,
    name: str,
    source_entity: dict[str, Any],
    *,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> DashboardResult:
    """Create a QuickSight dashboard.

    Args:
        aws_account_id: The AWS account ID.
        dashboard_id: ID for the new dashboard.
        name: Display name of the dashboard.
        source_entity: Source entity configuration dict.
        permissions: Optional permission list.
        tags: Optional tag list.
        region_name: AWS region override.

    Returns:
        A :class:`DashboardResult` with metadata.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "DashboardId": dashboard_id,
        "Name": name,
        "SourceEntity": source_entity,
    }
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateDashboard", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create dashboard {dashboard_id!r}") from exc
    return DashboardResult(
        dashboard_id=resp.get("DashboardId", dashboard_id),
        name=name,
        arn=resp.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_dashboard(
    aws_account_id: str,
    dashboard_id: str,
    *,
    region_name: str | None = None,
) -> DashboardResult:
    """Describe a QuickSight dashboard.

    Args:
        aws_account_id: The AWS account ID.
        dashboard_id: The dashboard ID.
        region_name: AWS region override.

    Returns:
        A :class:`DashboardResult` with metadata.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("quicksight", region_name)
    try:
        resp = await client.call(
            "DescribeDashboard",
            AwsAccountId=aws_account_id,
            DashboardId=dashboard_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to describe dashboard {dashboard_id!r}") from exc
    dashboard = resp.get("Dashboard", {})
    return DashboardResult(
        dashboard_id=dashboard.get("DashboardId", dashboard_id),
        name=dashboard.get("Name", ""),
        arn=dashboard.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_dashboards(
    aws_account_id: str,
    *,
    region_name: str | None = None,
) -> list[DashboardResult]:
    """List all QuickSight dashboards in the account.

    Args:
        aws_account_id: The AWS account ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`DashboardResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    dashboards: list[DashboardResult] = []
    kwargs: dict[str, Any] = {"AwsAccountId": aws_account_id}
    try:
        while True:
            resp = await client.call("ListDashboards", **kwargs)
            for d in resp.get("DashboardSummaryList", []):
                dashboards.append(
                    DashboardResult(
                        dashboard_id=d.get("DashboardId", ""),
                        name=d.get("Name", ""),
                        arn=d.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_dashboards failed") from exc
    return dashboards


async def delete_dashboard(
    aws_account_id: str,
    dashboard_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a QuickSight dashboard.

    Args:
        aws_account_id: The AWS account ID.
        dashboard_id: The dashboard ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("quicksight", region_name)
    try:
        await client.call(
            "DeleteDashboard",
            AwsAccountId=aws_account_id,
            DashboardId=dashboard_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete dashboard {dashboard_id!r}") from exc


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


async def create_dataset(
    aws_account_id: str,
    dataset_id: str,
    name: str,
    physical_table_map: dict[str, Any],
    import_mode: str = "SPICE",
    *,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> DataSetResult:
    """Create a QuickSight dataset.

    Args:
        aws_account_id: The AWS account ID.
        dataset_id: ID for the new dataset.
        name: Display name.
        physical_table_map: Physical table configuration.
        import_mode: Import mode (``"SPICE"`` or ``"DIRECT_QUERY"``).
        permissions: Optional permission list.
        tags: Optional tag list.
        region_name: AWS region override.

    Returns:
        A :class:`DataSetResult` with metadata.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "DataSetId": dataset_id,
        "Name": name,
        "PhysicalTableMap": physical_table_map,
        "ImportMode": import_mode,
    }
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateDataSet", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create dataset {dataset_id!r}") from exc
    return DataSetResult(
        dataset_id=resp.get("DataSetId", dataset_id),
        name=name,
        arn=resp.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_dataset(
    aws_account_id: str,
    dataset_id: str,
    *,
    region_name: str | None = None,
) -> DataSetResult:
    """Describe a QuickSight dataset.

    Args:
        aws_account_id: The AWS account ID.
        dataset_id: The dataset ID.
        region_name: AWS region override.

    Returns:
        A :class:`DataSetResult` with metadata.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("quicksight", region_name)
    try:
        resp = await client.call(
            "DescribeDataSet",
            AwsAccountId=aws_account_id,
            DataSetId=dataset_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to describe dataset {dataset_id!r}") from exc
    ds = resp.get("DataSet", {})
    return DataSetResult(
        dataset_id=ds.get("DataSetId", dataset_id),
        name=ds.get("Name", ""),
        arn=ds.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_datasets(
    aws_account_id: str,
    *,
    region_name: str | None = None,
) -> list[DataSetResult]:
    """List all QuickSight datasets in the account.

    Args:
        aws_account_id: The AWS account ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`DataSetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    datasets: list[DataSetResult] = []
    kwargs: dict[str, Any] = {"AwsAccountId": aws_account_id}
    try:
        while True:
            resp = await client.call("ListDataSets", **kwargs)
            for ds in resp.get("DataSetSummaries", []):
                datasets.append(
                    DataSetResult(
                        dataset_id=ds.get("DataSetId", ""),
                        name=ds.get("Name", ""),
                        arn=ds.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_datasets failed") from exc
    return datasets


async def delete_dataset(
    aws_account_id: str,
    dataset_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a QuickSight dataset.

    Args:
        aws_account_id: The AWS account ID.
        dataset_id: The dataset ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("quicksight", region_name)
    try:
        await client.call(
            "DeleteDataSet",
            AwsAccountId=aws_account_id,
            DataSetId=dataset_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete dataset {dataset_id!r}") from exc


# ---------------------------------------------------------------------------
# Analysis operations
# ---------------------------------------------------------------------------


async def create_analysis(
    aws_account_id: str,
    analysis_id: str,
    name: str,
    source_entity: dict[str, Any],
    *,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> AnalysisResult:
    """Create a QuickSight analysis.

    Args:
        aws_account_id: The AWS account ID.
        analysis_id: ID for the new analysis.
        name: Display name.
        source_entity: Source entity configuration dict.
        permissions: Optional permission list.
        tags: Optional tag list.
        region_name: AWS region override.

    Returns:
        An :class:`AnalysisResult` with metadata.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "AnalysisId": analysis_id,
        "Name": name,
        "SourceEntity": source_entity,
    }
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateAnalysis", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create analysis {analysis_id!r}") from exc
    return AnalysisResult(
        analysis_id=resp.get("AnalysisId", analysis_id),
        name=name,
        arn=resp.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_analyses(
    aws_account_id: str,
    *,
    region_name: str | None = None,
) -> list[AnalysisResult]:
    """List all QuickSight analyses in the account.

    Args:
        aws_account_id: The AWS account ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`AnalysisResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    analyses: list[AnalysisResult] = []
    kwargs: dict[str, Any] = {"AwsAccountId": aws_account_id}
    try:
        while True:
            resp = await client.call("ListAnalyses", **kwargs)
            for a in resp.get("AnalysisSummaryList", []):
                analyses.append(
                    AnalysisResult(
                        analysis_id=a.get("AnalysisId", ""),
                        name=a.get("Name", ""),
                        arn=a.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_analyses failed") from exc
    return analyses


# ---------------------------------------------------------------------------
# Data source operations
# ---------------------------------------------------------------------------


async def create_data_source(
    aws_account_id: str,
    data_source_id: str,
    name: str,
    data_source_type: str,
    data_source_parameters: dict[str, Any],
    *,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> DataSourceResult:
    """Create a QuickSight data source.

    Args:
        aws_account_id: The AWS account ID.
        data_source_id: ID for the new data source.
        name: Display name.
        data_source_type: Type (e.g. ``"ATHENA"``, ``"S3"``).
        data_source_parameters: Type-specific connection parameters.
        permissions: Optional permission list.
        tags: Optional tag list.
        region_name: AWS region override.

    Returns:
        A :class:`DataSourceResult` with metadata.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "DataSourceId": data_source_id,
        "Name": name,
        "Type": data_source_type,
        "DataSourceParameters": data_source_parameters,
    }
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateDataSource", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create data source {data_source_id!r}") from exc
    return DataSourceResult(
        data_source_id=resp.get("DataSourceId", data_source_id),
        name=name,
        arn=resp.get("Arn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_data_sources(
    aws_account_id: str,
    *,
    region_name: str | None = None,
) -> list[DataSourceResult]:
    """List all QuickSight data sources in the account.

    Args:
        aws_account_id: The AWS account ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`DataSourceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    sources: list[DataSourceResult] = []
    kwargs: dict[str, Any] = {"AwsAccountId": aws_account_id}
    try:
        while True:
            resp = await client.call("ListDataSources", **kwargs)
            for s in resp.get("DataSources", []):
                sources.append(
                    DataSourceResult(
                        data_source_id=s.get("DataSourceId", ""),
                        name=s.get("Name", ""),
                        arn=s.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_data_sources failed") from exc
    return sources


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


async def describe_user(
    aws_account_id: str,
    user_name: str,
    namespace: str = "default",
    *,
    region_name: str | None = None,
) -> QuickSightUser:
    """Describe a QuickSight user.

    Args:
        aws_account_id: The AWS account ID.
        user_name: The QuickSight user name.
        namespace: The QuickSight namespace (default ``"default"``).
        region_name: AWS region override.

    Returns:
        A :class:`QuickSightUser` with metadata.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = async_client("quicksight", region_name)
    try:
        resp = await client.call(
            "DescribeUser",
            AwsAccountId=aws_account_id,
            UserName=user_name,
            Namespace=namespace,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to describe user {user_name!r}") from exc
    user = resp.get("User", {})
    return QuickSightUser(
        user_name=user.get("UserName"),
        email=user.get("Email"),
        role=user.get("Role"),
        arn=user.get("Arn"),
        identity_type=user.get("IdentityType"),
        active=user.get("Active"),
        principal_id=user.get("PrincipalId"),
    )


async def list_users(
    aws_account_id: str,
    namespace: str = "default",
    *,
    region_name: str | None = None,
) -> list[QuickSightUser]:
    """List all QuickSight users in a namespace.

    Args:
        aws_account_id: The AWS account ID.
        namespace: The QuickSight namespace (default ``"default"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`QuickSightUser` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    users: list[QuickSightUser] = []
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "Namespace": namespace,
    }
    try:
        while True:
            resp = await client.call("ListUsers", **kwargs)
            for u in resp.get("UserList", []):
                users.append(
                    QuickSightUser(
                        user_name=u.get("UserName"),
                        email=u.get("Email"),
                        role=u.get("Role"),
                        arn=u.get("Arn"),
                        identity_type=u.get("IdentityType"),
                        active=u.get("Active"),
                        principal_id=u.get("PrincipalId"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_users failed") from exc
    return users


async def register_user(
    aws_account_id: str,
    email: str,
    identity_type: str,
    user_role: str,
    namespace: str = "default",
    *,
    iam_arn: str | None = None,
    session_name: str | None = None,
    region_name: str | None = None,
) -> QuickSightUser:
    """Register a new QuickSight user.

    Args:
        aws_account_id: The AWS account ID.
        email: User email address.
        identity_type: Identity type (``"IAM"``, ``"QUICKSIGHT"``).
        user_role: User role (``"READER"``, ``"AUTHOR"``, ``"ADMIN"``).
        namespace: The QuickSight namespace (default ``"default"``).
        iam_arn: IAM ARN (required when ``identity_type`` is ``"IAM"``).
        session_name: Session name for IAM federation.
        region_name: AWS region override.

    Returns:
        A :class:`QuickSightUser` with metadata.

    Raises:
        RuntimeError: If registration fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {
        "AwsAccountId": aws_account_id,
        "Email": email,
        "IdentityType": identity_type,
        "UserRole": user_role,
        "Namespace": namespace,
    }
    if iam_arn is not None:
        kwargs["IamArn"] = iam_arn
    if session_name is not None:
        kwargs["SessionName"] = session_name

    try:
        resp = await client.call("RegisterUser", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to register user {email!r}") from exc
    user = resp.get("User", {})
    return QuickSightUser(
        user_name=user.get("UserName"),
        email=user.get("Email"),
        role=user.get("Role"),
        arn=user.get("Arn"),
        identity_type=user.get("IdentityType"),
        active=user.get("Active"),
        principal_id=user.get("PrincipalId"),
    )


async def delete_user(
    aws_account_id: str,
    user_name: str,
    namespace: str = "default",
    *,
    region_name: str | None = None,
) -> None:
    """Delete a QuickSight user.

    Args:
        aws_account_id: The AWS account ID.
        user_name: The QuickSight user name to delete.
        namespace: The QuickSight namespace (default ``"default"``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("quicksight", region_name)
    try:
        await client.call(
            "DeleteUser",
            AwsAccountId=aws_account_id,
            UserName=user_name,
            Namespace=namespace,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete user {user_name!r}") from exc


async def batch_create_topic_reviewed_answer(
    aws_account_id: str,
    topic_id: str,
    answers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchCreateTopicReviewedAnswerResult:
    """Batch create topic reviewed answer.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        answers: Answers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["Answers"] = answers
    try:
        resp = await client.call("BatchCreateTopicReviewedAnswer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch create topic reviewed answer") from exc
    return BatchCreateTopicReviewedAnswerResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        succeeded_answers=resp.get("SucceededAnswers"),
        invalid_answers=resp.get("InvalidAnswers"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def batch_delete_topic_reviewed_answer(
    aws_account_id: str,
    topic_id: str,
    *,
    answer_ids: list[str] | None = None,
    region_name: str | None = None,
) -> BatchDeleteTopicReviewedAnswerResult:
    """Batch delete topic reviewed answer.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        answer_ids: Answer ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    if answer_ids is not None:
        kwargs["AnswerIds"] = answer_ids
    try:
        resp = await client.call("BatchDeleteTopicReviewedAnswer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete topic reviewed answer") from exc
    return BatchDeleteTopicReviewedAnswerResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        succeeded_answers=resp.get("SucceededAnswers"),
        invalid_answers=resp.get("InvalidAnswers"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def cancel_ingestion(
    aws_account_id: str,
    data_set_id: str,
    ingestion_id: str,
    region_name: str | None = None,
) -> CancelIngestionResult:
    """Cancel ingestion.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        ingestion_id: Ingestion id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["IngestionId"] = ingestion_id
    try:
        resp = await client.call("CancelIngestion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel ingestion") from exc
    return CancelIngestionResult(
        arn=resp.get("Arn"),
        ingestion_id=resp.get("IngestionId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_account_customization(
    aws_account_id: str,
    account_customization: dict[str, Any],
    *,
    namespace: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateAccountCustomizationResult:
    """Create account customization.

    Args:
        aws_account_id: Aws account id.
        account_customization: Account customization.
        namespace: Namespace.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AccountCustomization"] = account_customization
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateAccountCustomization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create account customization") from exc
    return CreateAccountCustomizationResult(
        arn=resp.get("Arn"),
        aws_account_id=resp.get("AwsAccountId"),
        namespace=resp.get("Namespace"),
        account_customization=resp.get("AccountCustomization"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_account_subscription(
    authentication_method: str,
    aws_account_id: str,
    account_name: str,
    notification_email: str,
    *,
    edition: str | None = None,
    active_directory_name: str | None = None,
    realm: str | None = None,
    directory_id: str | None = None,
    admin_group: list[str] | None = None,
    author_group: list[str] | None = None,
    reader_group: list[str] | None = None,
    admin_pro_group: list[str] | None = None,
    author_pro_group: list[str] | None = None,
    reader_pro_group: list[str] | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email_address: str | None = None,
    contact_number: str | None = None,
    iam_identity_center_instance_arn: str | None = None,
    region_name: str | None = None,
) -> CreateAccountSubscriptionResult:
    """Create account subscription.

    Args:
        authentication_method: Authentication method.
        aws_account_id: Aws account id.
        account_name: Account name.
        notification_email: Notification email.
        edition: Edition.
        active_directory_name: Active directory name.
        realm: Realm.
        directory_id: Directory id.
        admin_group: Admin group.
        author_group: Author group.
        reader_group: Reader group.
        admin_pro_group: Admin pro group.
        author_pro_group: Author pro group.
        reader_pro_group: Reader pro group.
        first_name: First name.
        last_name: Last name.
        email_address: Email address.
        contact_number: Contact number.
        iam_identity_center_instance_arn: Iam identity center instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationMethod"] = authentication_method
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AccountName"] = account_name
    kwargs["NotificationEmail"] = notification_email
    if edition is not None:
        kwargs["Edition"] = edition
    if active_directory_name is not None:
        kwargs["ActiveDirectoryName"] = active_directory_name
    if realm is not None:
        kwargs["Realm"] = realm
    if directory_id is not None:
        kwargs["DirectoryId"] = directory_id
    if admin_group is not None:
        kwargs["AdminGroup"] = admin_group
    if author_group is not None:
        kwargs["AuthorGroup"] = author_group
    if reader_group is not None:
        kwargs["ReaderGroup"] = reader_group
    if admin_pro_group is not None:
        kwargs["AdminProGroup"] = admin_pro_group
    if author_pro_group is not None:
        kwargs["AuthorProGroup"] = author_pro_group
    if reader_pro_group is not None:
        kwargs["ReaderProGroup"] = reader_pro_group
    if first_name is not None:
        kwargs["FirstName"] = first_name
    if last_name is not None:
        kwargs["LastName"] = last_name
    if email_address is not None:
        kwargs["EmailAddress"] = email_address
    if contact_number is not None:
        kwargs["ContactNumber"] = contact_number
    if iam_identity_center_instance_arn is not None:
        kwargs["IAMIdentityCenterInstanceArn"] = iam_identity_center_instance_arn
    try:
        resp = await client.call("CreateAccountSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create account subscription") from exc
    return CreateAccountSubscriptionResult(
        signup_response=resp.get("SignupResponse"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_action_connector(
    aws_account_id: str,
    action_connector_id: str,
    name: str,
    type_value: str,
    authentication_config: dict[str, Any],
    *,
    description: str | None = None,
    permissions: list[dict[str, Any]] | None = None,
    vpc_connection_arn: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateActionConnectorResult:
    """Create action connector.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        name: Name.
        type_value: Type value.
        authentication_config: Authentication config.
        description: Description.
        permissions: Permissions.
        vpc_connection_arn: Vpc connection arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    kwargs["AuthenticationConfig"] = authentication_config
    if description is not None:
        kwargs["Description"] = description
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if vpc_connection_arn is not None:
        kwargs["VpcConnectionArn"] = vpc_connection_arn
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateActionConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create action connector") from exc
    return CreateActionConnectorResult(
        arn=resp.get("Arn"),
        creation_status=resp.get("CreationStatus"),
        action_connector_id=resp.get("ActionConnectorId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_brand(
    aws_account_id: str,
    brand_id: str,
    *,
    brand_definition: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateBrandResult:
    """Create brand.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        brand_definition: Brand definition.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    if brand_definition is not None:
        kwargs["BrandDefinition"] = brand_definition
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateBrand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create brand") from exc
    return CreateBrandResult(
        request_id=resp.get("RequestId"),
        brand_detail=resp.get("BrandDetail"),
        brand_definition=resp.get("BrandDefinition"),
    )


async def create_custom_permissions(
    aws_account_id: str,
    custom_permissions_name: str,
    *,
    capabilities: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCustomPermissionsResult:
    """Create custom permissions.

    Args:
        aws_account_id: Aws account id.
        custom_permissions_name: Custom permissions name.
        capabilities: Capabilities.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["CustomPermissionsName"] = custom_permissions_name
    if capabilities is not None:
        kwargs["Capabilities"] = capabilities
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateCustomPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom permissions") from exc
    return CreateCustomPermissionsResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
    )


async def create_data_set(
    aws_account_id: str,
    data_set_id: str,
    name: str,
    physical_table_map: dict[str, Any],
    import_mode: str,
    *,
    logical_table_map: dict[str, Any] | None = None,
    column_groups: list[dict[str, Any]] | None = None,
    field_folders: dict[str, Any] | None = None,
    permissions: list[dict[str, Any]] | None = None,
    row_level_permission_data_set: dict[str, Any] | None = None,
    row_level_permission_tag_configuration: dict[str, Any] | None = None,
    column_level_permission_rules: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    data_set_usage_configuration: dict[str, Any] | None = None,
    dataset_parameters: list[dict[str, Any]] | None = None,
    folder_arns: list[str] | None = None,
    performance_configuration: dict[str, Any] | None = None,
    use_as: str | None = None,
    data_prep_configuration: dict[str, Any] | None = None,
    semantic_model_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDataSetResult:
    """Create data set.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        name: Name.
        physical_table_map: Physical table map.
        import_mode: Import mode.
        logical_table_map: Logical table map.
        column_groups: Column groups.
        field_folders: Field folders.
        permissions: Permissions.
        row_level_permission_data_set: Row level permission data set.
        row_level_permission_tag_configuration: Row level permission tag configuration.
        column_level_permission_rules: Column level permission rules.
        tags: Tags.
        data_set_usage_configuration: Data set usage configuration.
        dataset_parameters: Dataset parameters.
        folder_arns: Folder arns.
        performance_configuration: Performance configuration.
        use_as: Use as.
        data_prep_configuration: Data prep configuration.
        semantic_model_configuration: Semantic model configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["Name"] = name
    kwargs["PhysicalTableMap"] = physical_table_map
    kwargs["ImportMode"] = import_mode
    if logical_table_map is not None:
        kwargs["LogicalTableMap"] = logical_table_map
    if column_groups is not None:
        kwargs["ColumnGroups"] = column_groups
    if field_folders is not None:
        kwargs["FieldFolders"] = field_folders
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if row_level_permission_data_set is not None:
        kwargs["RowLevelPermissionDataSet"] = row_level_permission_data_set
    if row_level_permission_tag_configuration is not None:
        kwargs["RowLevelPermissionTagConfiguration"] = row_level_permission_tag_configuration
    if column_level_permission_rules is not None:
        kwargs["ColumnLevelPermissionRules"] = column_level_permission_rules
    if tags is not None:
        kwargs["Tags"] = tags
    if data_set_usage_configuration is not None:
        kwargs["DataSetUsageConfiguration"] = data_set_usage_configuration
    if dataset_parameters is not None:
        kwargs["DatasetParameters"] = dataset_parameters
    if folder_arns is not None:
        kwargs["FolderArns"] = folder_arns
    if performance_configuration is not None:
        kwargs["PerformanceConfiguration"] = performance_configuration
    if use_as is not None:
        kwargs["UseAs"] = use_as
    if data_prep_configuration is not None:
        kwargs["DataPrepConfiguration"] = data_prep_configuration
    if semantic_model_configuration is not None:
        kwargs["SemanticModelConfiguration"] = semantic_model_configuration
    try:
        resp = await client.call("CreateDataSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data set") from exc
    return CreateDataSetResult(
        arn=resp.get("Arn"),
        data_set_id=resp.get("DataSetId"),
        ingestion_arn=resp.get("IngestionArn"),
        ingestion_id=resp.get("IngestionId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_folder(
    aws_account_id: str,
    folder_id: str,
    *,
    name: str | None = None,
    folder_type: str | None = None,
    parent_folder_arn: str | None = None,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    sharing_model: str | None = None,
    region_name: str | None = None,
) -> CreateFolderResult:
    """Create folder.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        name: Name.
        folder_type: Folder type.
        parent_folder_arn: Parent folder arn.
        permissions: Permissions.
        tags: Tags.
        sharing_model: Sharing model.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    if name is not None:
        kwargs["Name"] = name
    if folder_type is not None:
        kwargs["FolderType"] = folder_type
    if parent_folder_arn is not None:
        kwargs["ParentFolderArn"] = parent_folder_arn
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags
    if sharing_model is not None:
        kwargs["SharingModel"] = sharing_model
    try:
        resp = await client.call("CreateFolder", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create folder") from exc
    return CreateFolderResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        folder_id=resp.get("FolderId"),
        request_id=resp.get("RequestId"),
    )


async def create_folder_membership(
    aws_account_id: str,
    folder_id: str,
    member_id: str,
    member_type: str,
    region_name: str | None = None,
) -> CreateFolderMembershipResult:
    """Create folder membership.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        member_id: Member id.
        member_type: Member type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    kwargs["MemberId"] = member_id
    kwargs["MemberType"] = member_type
    try:
        resp = await client.call("CreateFolderMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create folder membership") from exc
    return CreateFolderMembershipResult(
        status=resp.get("Status"),
        folder_member=resp.get("FolderMember"),
        request_id=resp.get("RequestId"),
    )


async def create_group(
    group_name: str,
    aws_account_id: str,
    namespace: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateGroupResult:
    """Create group.

    Args:
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("CreateGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create group") from exc
    return CreateGroupResult(
        group=resp.get("Group"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_group_membership(
    member_name: str,
    group_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> CreateGroupMembershipResult:
    """Create group membership.

    Args:
        member_name: Member name.
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberName"] = member_name
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("CreateGroupMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create group membership") from exc
    return CreateGroupMembershipResult(
        group_member=resp.get("GroupMember"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_iam_policy_assignment(
    aws_account_id: str,
    assignment_name: str,
    assignment_status: str,
    namespace: str,
    *,
    policy_arn: str | None = None,
    identities: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateIamPolicyAssignmentResult:
    """Create iam policy assignment.

    Args:
        aws_account_id: Aws account id.
        assignment_name: Assignment name.
        assignment_status: Assignment status.
        namespace: Namespace.
        policy_arn: Policy arn.
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssignmentName"] = assignment_name
    kwargs["AssignmentStatus"] = assignment_status
    kwargs["Namespace"] = namespace
    if policy_arn is not None:
        kwargs["PolicyArn"] = policy_arn
    if identities is not None:
        kwargs["Identities"] = identities
    try:
        resp = await client.call("CreateIAMPolicyAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create iam policy assignment") from exc
    return CreateIamPolicyAssignmentResult(
        assignment_name=resp.get("AssignmentName"),
        assignment_id=resp.get("AssignmentId"),
        assignment_status=resp.get("AssignmentStatus"),
        policy_arn=resp.get("PolicyArn"),
        identities=resp.get("Identities"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_ingestion(
    data_set_id: str,
    ingestion_id: str,
    aws_account_id: str,
    *,
    ingestion_type: str | None = None,
    region_name: str | None = None,
) -> CreateIngestionResult:
    """Create ingestion.

    Args:
        data_set_id: Data set id.
        ingestion_id: Ingestion id.
        aws_account_id: Aws account id.
        ingestion_type: Ingestion type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSetId"] = data_set_id
    kwargs["IngestionId"] = ingestion_id
    kwargs["AwsAccountId"] = aws_account_id
    if ingestion_type is not None:
        kwargs["IngestionType"] = ingestion_type
    try:
        resp = await client.call("CreateIngestion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ingestion") from exc
    return CreateIngestionResult(
        arn=resp.get("Arn"),
        ingestion_id=resp.get("IngestionId"),
        ingestion_status=resp.get("IngestionStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_namespace(
    aws_account_id: str,
    namespace: str,
    identity_store: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateNamespaceResult:
    """Create namespace.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        identity_store: Identity store.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["IdentityStore"] = identity_store
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create namespace") from exc
    return CreateNamespaceResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
        capacity_region=resp.get("CapacityRegion"),
        creation_status=resp.get("CreationStatus"),
        identity_store=resp.get("IdentityStore"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_refresh_schedule(
    data_set_id: str,
    aws_account_id: str,
    schedule: dict[str, Any],
    region_name: str | None = None,
) -> CreateRefreshScheduleResult:
    """Create refresh schedule.

    Args:
        data_set_id: Data set id.
        aws_account_id: Aws account id.
        schedule: Schedule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSetId"] = data_set_id
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Schedule"] = schedule
    try:
        resp = await client.call("CreateRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create refresh schedule") from exc
    return CreateRefreshScheduleResult(
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        schedule_id=resp.get("ScheduleId"),
        arn=resp.get("Arn"),
    )


async def create_role_membership(
    member_name: str,
    aws_account_id: str,
    namespace: str,
    role: str,
    region_name: str | None = None,
) -> CreateRoleMembershipResult:
    """Create role membership.

    Args:
        member_name: Member name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        role: Role.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberName"] = member_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["Role"] = role
    try:
        resp = await client.call("CreateRoleMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create role membership") from exc
    return CreateRoleMembershipResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_template(
    aws_account_id: str,
    template_id: str,
    *,
    name: str | None = None,
    permissions: list[dict[str, Any]] | None = None,
    source_entity: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    version_description: str | None = None,
    definition: dict[str, Any] | None = None,
    validation_strategy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTemplateResult:
    """Create template.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        name: Name.
        permissions: Permissions.
        source_entity: Source entity.
        tags: Tags.
        version_description: Version description.
        definition: Definition.
        validation_strategy: Validation strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if name is not None:
        kwargs["Name"] = name
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if source_entity is not None:
        kwargs["SourceEntity"] = source_entity
    if tags is not None:
        kwargs["Tags"] = tags
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if definition is not None:
        kwargs["Definition"] = definition
    if validation_strategy is not None:
        kwargs["ValidationStrategy"] = validation_strategy
    try:
        resp = await client.call("CreateTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create template") from exc
    return CreateTemplateResult(
        arn=resp.get("Arn"),
        version_arn=resp.get("VersionArn"),
        template_id=resp.get("TemplateId"),
        creation_status=resp.get("CreationStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_template_alias(
    aws_account_id: str,
    template_id: str,
    alias_name: str,
    template_version_number: int,
    region_name: str | None = None,
) -> CreateTemplateAliasResult:
    """Create template alias.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        alias_name: Alias name.
        template_version_number: Template version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    kwargs["AliasName"] = alias_name
    kwargs["TemplateVersionNumber"] = template_version_number
    try:
        resp = await client.call("CreateTemplateAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create template alias") from exc
    return CreateTemplateAliasResult(
        template_alias=resp.get("TemplateAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_theme(
    aws_account_id: str,
    theme_id: str,
    name: str,
    base_theme_id: str,
    configuration: dict[str, Any],
    *,
    version_description: str | None = None,
    permissions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateThemeResult:
    """Create theme.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        name: Name.
        base_theme_id: Base theme id.
        configuration: Configuration.
        version_description: Version description.
        permissions: Permissions.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["Name"] = name
    kwargs["BaseThemeId"] = base_theme_id
    kwargs["Configuration"] = configuration
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateTheme", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create theme") from exc
    return CreateThemeResult(
        arn=resp.get("Arn"),
        version_arn=resp.get("VersionArn"),
        theme_id=resp.get("ThemeId"),
        creation_status=resp.get("CreationStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_theme_alias(
    aws_account_id: str,
    theme_id: str,
    alias_name: str,
    theme_version_number: int,
    region_name: str | None = None,
) -> CreateThemeAliasResult:
    """Create theme alias.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        alias_name: Alias name.
        theme_version_number: Theme version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["AliasName"] = alias_name
    kwargs["ThemeVersionNumber"] = theme_version_number
    try:
        resp = await client.call("CreateThemeAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create theme alias") from exc
    return CreateThemeAliasResult(
        theme_alias=resp.get("ThemeAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_topic(
    aws_account_id: str,
    topic_id: str,
    topic: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    folder_arns: list[str] | None = None,
    custom_instructions: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTopicResult:
    """Create topic.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        topic: Topic.
        tags: Tags.
        folder_arns: Folder arns.
        custom_instructions: Custom instructions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["Topic"] = topic
    if tags is not None:
        kwargs["Tags"] = tags
    if folder_arns is not None:
        kwargs["FolderArns"] = folder_arns
    if custom_instructions is not None:
        kwargs["CustomInstructions"] = custom_instructions
    try:
        resp = await client.call("CreateTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create topic") from exc
    return CreateTopicResult(
        arn=resp.get("Arn"),
        topic_id=resp.get("TopicId"),
        refresh_arn=resp.get("RefreshArn"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def create_topic_refresh_schedule(
    aws_account_id: str,
    topic_id: str,
    dataset_arn: str,
    refresh_schedule: dict[str, Any],
    *,
    dataset_name: str | None = None,
    region_name: str | None = None,
) -> CreateTopicRefreshScheduleResult:
    """Create topic refresh schedule.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        dataset_arn: Dataset arn.
        refresh_schedule: Refresh schedule.
        dataset_name: Dataset name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["DatasetArn"] = dataset_arn
    kwargs["RefreshSchedule"] = refresh_schedule
    if dataset_name is not None:
        kwargs["DatasetName"] = dataset_name
    try:
        resp = await client.call("CreateTopicRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create topic refresh schedule") from exc
    return CreateTopicRefreshScheduleResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        dataset_arn=resp.get("DatasetArn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def create_vpc_connection(
    aws_account_id: str,
    vpc_connection_id: str,
    name: str,
    subnet_ids: list[str],
    security_group_ids: list[str],
    role_arn: str,
    *,
    dns_resolvers: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateVpcConnectionResult:
    """Create vpc connection.

    Args:
        aws_account_id: Aws account id.
        vpc_connection_id: Vpc connection id.
        name: Name.
        subnet_ids: Subnet ids.
        security_group_ids: Security group ids.
        role_arn: Role arn.
        dns_resolvers: Dns resolvers.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["VPCConnectionId"] = vpc_connection_id
    kwargs["Name"] = name
    kwargs["SubnetIds"] = subnet_ids
    kwargs["SecurityGroupIds"] = security_group_ids
    kwargs["RoleArn"] = role_arn
    if dns_resolvers is not None:
        kwargs["DnsResolvers"] = dns_resolvers
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVPCConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc connection") from exc
    return CreateVpcConnectionResult(
        arn=resp.get("Arn"),
        vpc_connection_id=resp.get("VPCConnectionId"),
        creation_status=resp.get("CreationStatus"),
        availability_status=resp.get("AvailabilityStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_account_custom_permission(
    aws_account_id: str,
    region_name: str | None = None,
) -> DeleteAccountCustomPermissionResult:
    """Delete account custom permission.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DeleteAccountCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account custom permission") from exc
    return DeleteAccountCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_account_customization(
    aws_account_id: str,
    *,
    namespace: str | None = None,
    region_name: str | None = None,
) -> DeleteAccountCustomizationResult:
    """Delete account customization.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteAccountCustomization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account customization") from exc
    return DeleteAccountCustomizationResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_account_subscription(
    aws_account_id: str,
    region_name: str | None = None,
) -> DeleteAccountSubscriptionResult:
    """Delete account subscription.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DeleteAccountSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account subscription") from exc
    return DeleteAccountSubscriptionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_action_connector(
    aws_account_id: str,
    action_connector_id: str,
    region_name: str | None = None,
) -> DeleteActionConnectorResult:
    """Delete action connector.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    try:
        resp = await client.call("DeleteActionConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete action connector") from exc
    return DeleteActionConnectorResult(
        arn=resp.get("Arn"),
        action_connector_id=resp.get("ActionConnectorId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_analysis(
    aws_account_id: str,
    analysis_id: str,
    *,
    recovery_window_in_days: int | None = None,
    force_delete_without_recovery: bool | None = None,
    region_name: str | None = None,
) -> DeleteAnalysisResult:
    """Delete analysis.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        recovery_window_in_days: Recovery window in days.
        force_delete_without_recovery: Force delete without recovery.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    if recovery_window_in_days is not None:
        kwargs["RecoveryWindowInDays"] = recovery_window_in_days
    if force_delete_without_recovery is not None:
        kwargs["ForceDeleteWithoutRecovery"] = force_delete_without_recovery
    try:
        resp = await client.call("DeleteAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete analysis") from exc
    return DeleteAnalysisResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        analysis_id=resp.get("AnalysisId"),
        deletion_time=resp.get("DeletionTime"),
        request_id=resp.get("RequestId"),
    )


async def delete_brand(
    aws_account_id: str,
    brand_id: str,
    region_name: str | None = None,
) -> DeleteBrandResult:
    """Delete brand.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    try:
        resp = await client.call("DeleteBrand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete brand") from exc
    return DeleteBrandResult(
        request_id=resp.get("RequestId"),
    )


async def delete_brand_assignment(
    aws_account_id: str,
    region_name: str | None = None,
) -> DeleteBrandAssignmentResult:
    """Delete brand assignment.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DeleteBrandAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete brand assignment") from exc
    return DeleteBrandAssignmentResult(
        request_id=resp.get("RequestId"),
    )


async def delete_custom_permissions(
    aws_account_id: str,
    custom_permissions_name: str,
    region_name: str | None = None,
) -> DeleteCustomPermissionsResult:
    """Delete custom permissions.

    Args:
        aws_account_id: Aws account id.
        custom_permissions_name: Custom permissions name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["CustomPermissionsName"] = custom_permissions_name
    try:
        resp = await client.call("DeleteCustomPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom permissions") from exc
    return DeleteCustomPermissionsResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
    )


async def delete_data_set(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> DeleteDataSetResult:
    """Delete data set.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("DeleteDataSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data set") from exc
    return DeleteDataSetResult(
        arn=resp.get("Arn"),
        data_set_id=resp.get("DataSetId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_data_set_refresh_properties(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> DeleteDataSetRefreshPropertiesResult:
    """Delete data set refresh properties.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("DeleteDataSetRefreshProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data set refresh properties") from exc
    return DeleteDataSetRefreshPropertiesResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_data_source(
    aws_account_id: str,
    data_source_id: str,
    region_name: str | None = None,
) -> DeleteDataSourceResult:
    """Delete data source.

    Args:
        aws_account_id: Aws account id.
        data_source_id: Data source id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSourceId"] = data_source_id
    try:
        resp = await client.call("DeleteDataSource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data source") from exc
    return DeleteDataSourceResult(
        arn=resp.get("Arn"),
        data_source_id=resp.get("DataSourceId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_default_q_business_application(
    aws_account_id: str,
    *,
    namespace: str | None = None,
    region_name: str | None = None,
) -> DeleteDefaultQBusinessApplicationResult:
    """Delete default q business application.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteDefaultQBusinessApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete default q business application") from exc
    return DeleteDefaultQBusinessApplicationResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_folder(
    aws_account_id: str,
    folder_id: str,
    region_name: str | None = None,
) -> DeleteFolderResult:
    """Delete folder.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    try:
        resp = await client.call("DeleteFolder", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete folder") from exc
    return DeleteFolderResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        folder_id=resp.get("FolderId"),
        request_id=resp.get("RequestId"),
    )


async def delete_folder_membership(
    aws_account_id: str,
    folder_id: str,
    member_id: str,
    member_type: str,
    region_name: str | None = None,
) -> DeleteFolderMembershipResult:
    """Delete folder membership.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        member_id: Member id.
        member_type: Member type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    kwargs["MemberId"] = member_id
    kwargs["MemberType"] = member_type
    try:
        resp = await client.call("DeleteFolderMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete folder membership") from exc
    return DeleteFolderMembershipResult(
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def delete_group(
    group_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteGroupResult:
    """Delete group.

    Args:
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete group") from exc
    return DeleteGroupResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_group_membership(
    member_name: str,
    group_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteGroupMembershipResult:
    """Delete group membership.

    Args:
        member_name: Member name.
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberName"] = member_name
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteGroupMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete group membership") from exc
    return DeleteGroupMembershipResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_iam_policy_assignment(
    aws_account_id: str,
    assignment_name: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteIamPolicyAssignmentResult:
    """Delete iam policy assignment.

    Args:
        aws_account_id: Aws account id.
        assignment_name: Assignment name.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssignmentName"] = assignment_name
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteIAMPolicyAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete iam policy assignment") from exc
    return DeleteIamPolicyAssignmentResult(
        assignment_name=resp.get("AssignmentName"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_identity_propagation_config(
    aws_account_id: str,
    service: str,
    region_name: str | None = None,
) -> DeleteIdentityPropagationConfigResult:
    """Delete identity propagation config.

    Args:
        aws_account_id: Aws account id.
        service: Service.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Service"] = service
    try:
        resp = await client.call("DeleteIdentityPropagationConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete identity propagation config") from exc
    return DeleteIdentityPropagationConfigResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_namespace(
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteNamespaceResult:
    """Delete namespace.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete namespace") from exc
    return DeleteNamespaceResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_refresh_schedule(
    data_set_id: str,
    aws_account_id: str,
    schedule_id: str,
    region_name: str | None = None,
) -> DeleteRefreshScheduleResult:
    """Delete refresh schedule.

    Args:
        data_set_id: Data set id.
        aws_account_id: Aws account id.
        schedule_id: Schedule id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSetId"] = data_set_id
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ScheduleId"] = schedule_id
    try:
        resp = await client.call("DeleteRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete refresh schedule") from exc
    return DeleteRefreshScheduleResult(
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        schedule_id=resp.get("ScheduleId"),
        arn=resp.get("Arn"),
    )


async def delete_role_custom_permission(
    role: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteRoleCustomPermissionResult:
    """Delete role custom permission.

    Args:
        role: Role.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Role"] = role
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteRoleCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete role custom permission") from exc
    return DeleteRoleCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_role_membership(
    member_name: str,
    role: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteRoleMembershipResult:
    """Delete role membership.

    Args:
        member_name: Member name.
        role: Role.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberName"] = member_name
    kwargs["Role"] = role
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteRoleMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete role membership") from exc
    return DeleteRoleMembershipResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_template(
    aws_account_id: str,
    template_id: str,
    *,
    version_number: int | None = None,
    region_name: str | None = None,
) -> DeleteTemplateResult:
    """Delete template.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    try:
        resp = await client.call("DeleteTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete template") from exc
    return DeleteTemplateResult(
        request_id=resp.get("RequestId"),
        arn=resp.get("Arn"),
        template_id=resp.get("TemplateId"),
        status=resp.get("Status"),
    )


async def delete_template_alias(
    aws_account_id: str,
    template_id: str,
    alias_name: str,
    region_name: str | None = None,
) -> DeleteTemplateAliasResult:
    """Delete template alias.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DeleteTemplateAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete template alias") from exc
    return DeleteTemplateAliasResult(
        status=resp.get("Status"),
        template_id=resp.get("TemplateId"),
        alias_name=resp.get("AliasName"),
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
    )


async def delete_theme(
    aws_account_id: str,
    theme_id: str,
    *,
    version_number: int | None = None,
    region_name: str | None = None,
) -> DeleteThemeResult:
    """Delete theme.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    try:
        resp = await client.call("DeleteTheme", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete theme") from exc
    return DeleteThemeResult(
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        theme_id=resp.get("ThemeId"),
    )


async def delete_theme_alias(
    aws_account_id: str,
    theme_id: str,
    alias_name: str,
    region_name: str | None = None,
) -> DeleteThemeAliasResult:
    """Delete theme alias.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DeleteThemeAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete theme alias") from exc
    return DeleteThemeAliasResult(
        alias_name=resp.get("AliasName"),
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        theme_id=resp.get("ThemeId"),
    )


async def delete_topic(
    aws_account_id: str,
    topic_id: str,
    region_name: str | None = None,
) -> DeleteTopicResult:
    """Delete topic.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    try:
        resp = await client.call("DeleteTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete topic") from exc
    return DeleteTopicResult(
        arn=resp.get("Arn"),
        topic_id=resp.get("TopicId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_topic_refresh_schedule(
    aws_account_id: str,
    topic_id: str,
    dataset_id: str,
    region_name: str | None = None,
) -> DeleteTopicRefreshScheduleResult:
    """Delete topic refresh schedule.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        dataset_id: Dataset id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["DatasetId"] = dataset_id
    try:
        resp = await client.call("DeleteTopicRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete topic refresh schedule") from exc
    return DeleteTopicRefreshScheduleResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        dataset_arn=resp.get("DatasetArn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def delete_user_by_principal_id(
    principal_id: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteUserByPrincipalIdResult:
    """Delete user by principal id.

    Args:
        principal_id: Principal id.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PrincipalId"] = principal_id
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteUserByPrincipalId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user by principal id") from exc
    return DeleteUserByPrincipalIdResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_user_custom_permission(
    user_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DeleteUserCustomPermissionResult:
    """Delete user custom permission.

    Args:
        user_name: User name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DeleteUserCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user custom permission") from exc
    return DeleteUserCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def delete_vpc_connection(
    aws_account_id: str,
    vpc_connection_id: str,
    region_name: str | None = None,
) -> DeleteVpcConnectionResult:
    """Delete vpc connection.

    Args:
        aws_account_id: Aws account id.
        vpc_connection_id: Vpc connection id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["VPCConnectionId"] = vpc_connection_id
    try:
        resp = await client.call("DeleteVPCConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc connection") from exc
    return DeleteVpcConnectionResult(
        arn=resp.get("Arn"),
        vpc_connection_id=resp.get("VPCConnectionId"),
        deletion_status=resp.get("DeletionStatus"),
        availability_status=resp.get("AvailabilityStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_account_custom_permission(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeAccountCustomPermissionResult:
    """Describe account custom permission.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeAccountCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account custom permission") from exc
    return DescribeAccountCustomPermissionResult(
        custom_permissions_name=resp.get("CustomPermissionsName"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_account_customization(
    aws_account_id: str,
    *,
    namespace: str | None = None,
    resolved: bool | None = None,
    region_name: str | None = None,
) -> DescribeAccountCustomizationResult:
    """Describe account customization.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        resolved: Resolved.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if resolved is not None:
        kwargs["Resolved"] = resolved
    try:
        resp = await client.call("DescribeAccountCustomization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account customization") from exc
    return DescribeAccountCustomizationResult(
        arn=resp.get("Arn"),
        aws_account_id=resp.get("AwsAccountId"),
        namespace=resp.get("Namespace"),
        account_customization=resp.get("AccountCustomization"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_account_settings(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeAccountSettingsResult:
    """Describe account settings.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account settings") from exc
    return DescribeAccountSettingsResult(
        account_settings=resp.get("AccountSettings"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_account_subscription(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeAccountSubscriptionResult:
    """Describe account subscription.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeAccountSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account subscription") from exc
    return DescribeAccountSubscriptionResult(
        account_info=resp.get("AccountInfo"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_action_connector(
    aws_account_id: str,
    action_connector_id: str,
    region_name: str | None = None,
) -> DescribeActionConnectorResult:
    """Describe action connector.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    try:
        resp = await client.call("DescribeActionConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe action connector") from exc
    return DescribeActionConnectorResult(
        action_connector=resp.get("ActionConnector"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_action_connector_permissions(
    aws_account_id: str,
    action_connector_id: str,
    region_name: str | None = None,
) -> DescribeActionConnectorPermissionsResult:
    """Describe action connector permissions.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    try:
        resp = await client.call("DescribeActionConnectorPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe action connector permissions") from exc
    return DescribeActionConnectorPermissionsResult(
        arn=resp.get("Arn"),
        action_connector_id=resp.get("ActionConnectorId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_analysis(
    aws_account_id: str,
    analysis_id: str,
    region_name: str | None = None,
) -> DescribeAnalysisResult:
    """Describe analysis.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    try:
        resp = await client.call("DescribeAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe analysis") from exc
    return DescribeAnalysisResult(
        analysis=resp.get("Analysis"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_analysis_definition(
    aws_account_id: str,
    analysis_id: str,
    region_name: str | None = None,
) -> DescribeAnalysisDefinitionResult:
    """Describe analysis definition.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    try:
        resp = await client.call("DescribeAnalysisDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe analysis definition") from exc
    return DescribeAnalysisDefinitionResult(
        analysis_id=resp.get("AnalysisId"),
        name=resp.get("Name"),
        errors=resp.get("Errors"),
        resource_status=resp.get("ResourceStatus"),
        theme_arn=resp.get("ThemeArn"),
        definition=resp.get("Definition"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_analysis_permissions(
    aws_account_id: str,
    analysis_id: str,
    region_name: str | None = None,
) -> DescribeAnalysisPermissionsResult:
    """Describe analysis permissions.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    try:
        resp = await client.call("DescribeAnalysisPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe analysis permissions") from exc
    return DescribeAnalysisPermissionsResult(
        analysis_id=resp.get("AnalysisId"),
        analysis_arn=resp.get("AnalysisArn"),
        permissions=resp.get("Permissions"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_asset_bundle_export_job(
    aws_account_id: str,
    asset_bundle_export_job_id: str,
    region_name: str | None = None,
) -> DescribeAssetBundleExportJobResult:
    """Describe asset bundle export job.

    Args:
        aws_account_id: Aws account id.
        asset_bundle_export_job_id: Asset bundle export job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssetBundleExportJobId"] = asset_bundle_export_job_id
    try:
        resp = await client.call("DescribeAssetBundleExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset bundle export job") from exc
    return DescribeAssetBundleExportJobResult(
        job_status=resp.get("JobStatus"),
        download_url=resp.get("DownloadUrl"),
        errors=resp.get("Errors"),
        arn=resp.get("Arn"),
        created_time=resp.get("CreatedTime"),
        asset_bundle_export_job_id=resp.get("AssetBundleExportJobId"),
        aws_account_id=resp.get("AwsAccountId"),
        resource_arns=resp.get("ResourceArns"),
        include_all_dependencies=resp.get("IncludeAllDependencies"),
        export_format=resp.get("ExportFormat"),
        cloud_formation_override_property_configuration=resp.get(
            "CloudFormationOverridePropertyConfiguration"
        ),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        include_permissions=resp.get("IncludePermissions"),
        include_tags=resp.get("IncludeTags"),
        validation_strategy=resp.get("ValidationStrategy"),
        warnings=resp.get("Warnings"),
        include_folder_memberships=resp.get("IncludeFolderMemberships"),
        include_folder_members=resp.get("IncludeFolderMembers"),
    )


async def describe_asset_bundle_import_job(
    aws_account_id: str,
    asset_bundle_import_job_id: str,
    region_name: str | None = None,
) -> DescribeAssetBundleImportJobResult:
    """Describe asset bundle import job.

    Args:
        aws_account_id: Aws account id.
        asset_bundle_import_job_id: Asset bundle import job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssetBundleImportJobId"] = asset_bundle_import_job_id
    try:
        resp = await client.call("DescribeAssetBundleImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset bundle import job") from exc
    return DescribeAssetBundleImportJobResult(
        job_status=resp.get("JobStatus"),
        errors=resp.get("Errors"),
        rollback_errors=resp.get("RollbackErrors"),
        arn=resp.get("Arn"),
        created_time=resp.get("CreatedTime"),
        asset_bundle_import_job_id=resp.get("AssetBundleImportJobId"),
        aws_account_id=resp.get("AwsAccountId"),
        asset_bundle_import_source=resp.get("AssetBundleImportSource"),
        override_parameters=resp.get("OverrideParameters"),
        failure_action=resp.get("FailureAction"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        override_permissions=resp.get("OverridePermissions"),
        override_tags=resp.get("OverrideTags"),
        override_validation_strategy=resp.get("OverrideValidationStrategy"),
        warnings=resp.get("Warnings"),
    )


async def describe_brand(
    aws_account_id: str,
    brand_id: str,
    *,
    version_id: str | None = None,
    region_name: str | None = None,
) -> DescribeBrandResult:
    """Describe brand.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    if version_id is not None:
        kwargs["VersionId"] = version_id
    try:
        resp = await client.call("DescribeBrand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe brand") from exc
    return DescribeBrandResult(
        request_id=resp.get("RequestId"),
        brand_detail=resp.get("BrandDetail"),
        brand_definition=resp.get("BrandDefinition"),
    )


async def describe_brand_assignment(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeBrandAssignmentResult:
    """Describe brand assignment.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeBrandAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe brand assignment") from exc
    return DescribeBrandAssignmentResult(
        request_id=resp.get("RequestId"),
        brand_arn=resp.get("BrandArn"),
    )


async def describe_brand_published_version(
    aws_account_id: str,
    brand_id: str,
    region_name: str | None = None,
) -> DescribeBrandPublishedVersionResult:
    """Describe brand published version.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    try:
        resp = await client.call("DescribeBrandPublishedVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe brand published version") from exc
    return DescribeBrandPublishedVersionResult(
        request_id=resp.get("RequestId"),
        brand_detail=resp.get("BrandDetail"),
        brand_definition=resp.get("BrandDefinition"),
    )


async def describe_custom_permissions(
    aws_account_id: str,
    custom_permissions_name: str,
    region_name: str | None = None,
) -> DescribeCustomPermissionsResult:
    """Describe custom permissions.

    Args:
        aws_account_id: Aws account id.
        custom_permissions_name: Custom permissions name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["CustomPermissionsName"] = custom_permissions_name
    try:
        resp = await client.call("DescribeCustomPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe custom permissions") from exc
    return DescribeCustomPermissionsResult(
        status=resp.get("Status"),
        custom_permissions=resp.get("CustomPermissions"),
        request_id=resp.get("RequestId"),
    )


async def describe_dashboard_definition(
    aws_account_id: str,
    dashboard_id: str,
    *,
    version_number: int | None = None,
    alias_name: str | None = None,
    region_name: str | None = None,
) -> DescribeDashboardDefinitionResult:
    """Describe dashboard definition.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        version_number: Version number.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    if alias_name is not None:
        kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeDashboardDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboard definition") from exc
    return DescribeDashboardDefinitionResult(
        dashboard_id=resp.get("DashboardId"),
        errors=resp.get("Errors"),
        name=resp.get("Name"),
        resource_status=resp.get("ResourceStatus"),
        theme_arn=resp.get("ThemeArn"),
        definition=resp.get("Definition"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        dashboard_publish_options=resp.get("DashboardPublishOptions"),
    )


async def describe_dashboard_permissions(
    aws_account_id: str,
    dashboard_id: str,
    region_name: str | None = None,
) -> DescribeDashboardPermissionsResult:
    """Describe dashboard permissions.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    try:
        resp = await client.call("DescribeDashboardPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboard permissions") from exc
    return DescribeDashboardPermissionsResult(
        dashboard_id=resp.get("DashboardId"),
        dashboard_arn=resp.get("DashboardArn"),
        permissions=resp.get("Permissions"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        link_sharing_configuration=resp.get("LinkSharingConfiguration"),
    )


async def describe_dashboard_snapshot_job(
    aws_account_id: str,
    dashboard_id: str,
    snapshot_job_id: str,
    region_name: str | None = None,
) -> DescribeDashboardSnapshotJobResult:
    """Describe dashboard snapshot job.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        snapshot_job_id: Snapshot job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["SnapshotJobId"] = snapshot_job_id
    try:
        resp = await client.call("DescribeDashboardSnapshotJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboard snapshot job") from exc
    return DescribeDashboardSnapshotJobResult(
        aws_account_id=resp.get("AwsAccountId"),
        dashboard_id=resp.get("DashboardId"),
        snapshot_job_id=resp.get("SnapshotJobId"),
        user_configuration=resp.get("UserConfiguration"),
        snapshot_configuration=resp.get("SnapshotConfiguration"),
        arn=resp.get("Arn"),
        job_status=resp.get("JobStatus"),
        created_time=resp.get("CreatedTime"),
        last_updated_time=resp.get("LastUpdatedTime"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_dashboard_snapshot_job_result(
    aws_account_id: str,
    dashboard_id: str,
    snapshot_job_id: str,
    region_name: str | None = None,
) -> DescribeDashboardSnapshotJobResultResult:
    """Describe dashboard snapshot job result.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        snapshot_job_id: Snapshot job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["SnapshotJobId"] = snapshot_job_id
    try:
        resp = await client.call("DescribeDashboardSnapshotJobResult", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboard snapshot job result") from exc
    return DescribeDashboardSnapshotJobResultResult(
        arn=resp.get("Arn"),
        job_status=resp.get("JobStatus"),
        created_time=resp.get("CreatedTime"),
        last_updated_time=resp.get("LastUpdatedTime"),
        result=resp.get("Result"),
        error_info=resp.get("ErrorInfo"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_dashboards_qa_configuration(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeDashboardsQaConfigurationResult:
    """Describe dashboards qa configuration.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeDashboardsQAConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboards qa configuration") from exc
    return DescribeDashboardsQaConfigurationResult(
        dashboards_qa_status=resp.get("DashboardsQAStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_data_set(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> DescribeDataSetResult:
    """Describe data set.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("DescribeDataSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data set") from exc
    return DescribeDataSetResult(
        data_set=resp.get("DataSet"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_data_set_permissions(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> DescribeDataSetPermissionsResult:
    """Describe data set permissions.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("DescribeDataSetPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data set permissions") from exc
    return DescribeDataSetPermissionsResult(
        data_set_arn=resp.get("DataSetArn"),
        data_set_id=resp.get("DataSetId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_data_set_refresh_properties(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> DescribeDataSetRefreshPropertiesResult:
    """Describe data set refresh properties.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("DescribeDataSetRefreshProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data set refresh properties") from exc
    return DescribeDataSetRefreshPropertiesResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        data_set_refresh_properties=resp.get("DataSetRefreshProperties"),
    )


async def describe_data_source(
    aws_account_id: str,
    data_source_id: str,
    region_name: str | None = None,
) -> DescribeDataSourceResult:
    """Describe data source.

    Args:
        aws_account_id: Aws account id.
        data_source_id: Data source id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSourceId"] = data_source_id
    try:
        resp = await client.call("DescribeDataSource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data source") from exc
    return DescribeDataSourceResult(
        data_source=resp.get("DataSource"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_data_source_permissions(
    aws_account_id: str,
    data_source_id: str,
    region_name: str | None = None,
) -> DescribeDataSourcePermissionsResult:
    """Describe data source permissions.

    Args:
        aws_account_id: Aws account id.
        data_source_id: Data source id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSourceId"] = data_source_id
    try:
        resp = await client.call("DescribeDataSourcePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data source permissions") from exc
    return DescribeDataSourcePermissionsResult(
        data_source_arn=resp.get("DataSourceArn"),
        data_source_id=resp.get("DataSourceId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_default_q_business_application(
    aws_account_id: str,
    *,
    namespace: str | None = None,
    region_name: str | None = None,
) -> DescribeDefaultQBusinessApplicationResult:
    """Describe default q business application.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeDefaultQBusinessApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe default q business application") from exc
    return DescribeDefaultQBusinessApplicationResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        application_id=resp.get("ApplicationId"),
    )


async def describe_folder(
    aws_account_id: str,
    folder_id: str,
    region_name: str | None = None,
) -> DescribeFolderResult:
    """Describe folder.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    try:
        resp = await client.call("DescribeFolder", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe folder") from exc
    return DescribeFolderResult(
        status=resp.get("Status"),
        folder=resp.get("Folder"),
        request_id=resp.get("RequestId"),
    )


async def describe_folder_permissions(
    aws_account_id: str,
    folder_id: str,
    *,
    namespace: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFolderPermissionsResult:
    """Describe folder permissions.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        namespace: Namespace.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFolderPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe folder permissions") from exc
    return DescribeFolderPermissionsResult(
        status=resp.get("Status"),
        folder_id=resp.get("FolderId"),
        arn=resp.get("Arn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        next_token=resp.get("NextToken"),
    )


async def describe_folder_resolved_permissions(
    aws_account_id: str,
    folder_id: str,
    *,
    namespace: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFolderResolvedPermissionsResult:
    """Describe folder resolved permissions.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        namespace: Namespace.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFolderResolvedPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe folder resolved permissions") from exc
    return DescribeFolderResolvedPermissionsResult(
        status=resp.get("Status"),
        folder_id=resp.get("FolderId"),
        arn=resp.get("Arn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        next_token=resp.get("NextToken"),
    )


async def describe_group(
    group_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DescribeGroupResult:
    """Describe group.

    Args:
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe group") from exc
    return DescribeGroupResult(
        group=resp.get("Group"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_group_membership(
    member_name: str,
    group_name: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DescribeGroupMembershipResult:
    """Describe group membership.

    Args:
        member_name: Member name.
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberName"] = member_name
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeGroupMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe group membership") from exc
    return DescribeGroupMembershipResult(
        group_member=resp.get("GroupMember"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_iam_policy_assignment(
    aws_account_id: str,
    assignment_name: str,
    namespace: str,
    region_name: str | None = None,
) -> DescribeIamPolicyAssignmentResult:
    """Describe iam policy assignment.

    Args:
        aws_account_id: Aws account id.
        assignment_name: Assignment name.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssignmentName"] = assignment_name
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeIAMPolicyAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe iam policy assignment") from exc
    return DescribeIamPolicyAssignmentResult(
        iam_policy_assignment=resp.get("IAMPolicyAssignment"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_ingestion(
    aws_account_id: str,
    data_set_id: str,
    ingestion_id: str,
    region_name: str | None = None,
) -> DescribeIngestionResult:
    """Describe ingestion.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        ingestion_id: Ingestion id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["IngestionId"] = ingestion_id
    try:
        resp = await client.call("DescribeIngestion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe ingestion") from exc
    return DescribeIngestionResult(
        ingestion=resp.get("Ingestion"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_ip_restriction(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeIpRestrictionResult:
    """Describe ip restriction.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeIpRestriction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe ip restriction") from exc
    return DescribeIpRestrictionResult(
        aws_account_id=resp.get("AwsAccountId"),
        ip_restriction_rule_map=resp.get("IpRestrictionRuleMap"),
        vpc_id_restriction_rule_map=resp.get("VpcIdRestrictionRuleMap"),
        vpc_endpoint_id_restriction_rule_map=resp.get("VpcEndpointIdRestrictionRuleMap"),
        enabled=resp.get("Enabled"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_key_registration(
    aws_account_id: str,
    *,
    default_key_only: bool | None = None,
    region_name: str | None = None,
) -> DescribeKeyRegistrationResult:
    """Describe key registration.

    Args:
        aws_account_id: Aws account id.
        default_key_only: Default key only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if default_key_only is not None:
        kwargs["DefaultKeyOnly"] = default_key_only
    try:
        resp = await client.call("DescribeKeyRegistration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe key registration") from exc
    return DescribeKeyRegistrationResult(
        aws_account_id=resp.get("AwsAccountId"),
        key_registration=resp.get("KeyRegistration"),
        q_data_key=resp.get("QDataKey"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_namespace(
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DescribeNamespaceResult:
    """Describe namespace.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe namespace") from exc
    return DescribeNamespaceResult(
        namespace=resp.get("Namespace"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_q_personalization_configuration(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeQPersonalizationConfigurationResult:
    """Describe q personalization configuration.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeQPersonalizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe q personalization configuration") from exc
    return DescribeQPersonalizationConfigurationResult(
        personalization_mode=resp.get("PersonalizationMode"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_quick_sight_q_search_configuration(
    aws_account_id: str,
    region_name: str | None = None,
) -> DescribeQuickSightQSearchConfigurationResult:
    """Describe quick sight q search configuration.

    Args:
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("DescribeQuickSightQSearchConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe quick sight q search configuration") from exc
    return DescribeQuickSightQSearchConfigurationResult(
        q_search_status=resp.get("QSearchStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_refresh_schedule(
    aws_account_id: str,
    data_set_id: str,
    schedule_id: str,
    region_name: str | None = None,
) -> DescribeRefreshScheduleResult:
    """Describe refresh schedule.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        schedule_id: Schedule id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["ScheduleId"] = schedule_id
    try:
        resp = await client.call("DescribeRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe refresh schedule") from exc
    return DescribeRefreshScheduleResult(
        refresh_schedule=resp.get("RefreshSchedule"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        arn=resp.get("Arn"),
    )


async def describe_role_custom_permission(
    role: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> DescribeRoleCustomPermissionResult:
    """Describe role custom permission.

    Args:
        role: Role.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Role"] = role
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("DescribeRoleCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe role custom permission") from exc
    return DescribeRoleCustomPermissionResult(
        custom_permissions_name=resp.get("CustomPermissionsName"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_template(
    aws_account_id: str,
    template_id: str,
    *,
    version_number: int | None = None,
    alias_name: str | None = None,
    region_name: str | None = None,
) -> DescribeTemplateResult:
    """Describe template.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        version_number: Version number.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    if alias_name is not None:
        kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe template") from exc
    return DescribeTemplateResult(
        template=resp.get("Template"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_template_alias(
    aws_account_id: str,
    template_id: str,
    alias_name: str,
    region_name: str | None = None,
) -> DescribeTemplateAliasResult:
    """Describe template alias.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeTemplateAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe template alias") from exc
    return DescribeTemplateAliasResult(
        template_alias=resp.get("TemplateAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_template_definition(
    aws_account_id: str,
    template_id: str,
    *,
    version_number: int | None = None,
    alias_name: str | None = None,
    region_name: str | None = None,
) -> DescribeTemplateDefinitionResult:
    """Describe template definition.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        version_number: Version number.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    if alias_name is not None:
        kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeTemplateDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe template definition") from exc
    return DescribeTemplateDefinitionResult(
        name=resp.get("Name"),
        template_id=resp.get("TemplateId"),
        errors=resp.get("Errors"),
        resource_status=resp.get("ResourceStatus"),
        theme_arn=resp.get("ThemeArn"),
        definition=resp.get("Definition"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_template_permissions(
    aws_account_id: str,
    template_id: str,
    region_name: str | None = None,
) -> DescribeTemplatePermissionsResult:
    """Describe template permissions.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    try:
        resp = await client.call("DescribeTemplatePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe template permissions") from exc
    return DescribeTemplatePermissionsResult(
        template_id=resp.get("TemplateId"),
        template_arn=resp.get("TemplateArn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_theme(
    aws_account_id: str,
    theme_id: str,
    *,
    version_number: int | None = None,
    alias_name: str | None = None,
    region_name: str | None = None,
) -> DescribeThemeResult:
    """Describe theme.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        version_number: Version number.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    if version_number is not None:
        kwargs["VersionNumber"] = version_number
    if alias_name is not None:
        kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeTheme", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe theme") from exc
    return DescribeThemeResult(
        theme=resp.get("Theme"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_theme_alias(
    aws_account_id: str,
    theme_id: str,
    alias_name: str,
    region_name: str | None = None,
) -> DescribeThemeAliasResult:
    """Describe theme alias.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        alias_name: Alias name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["AliasName"] = alias_name
    try:
        resp = await client.call("DescribeThemeAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe theme alias") from exc
    return DescribeThemeAliasResult(
        theme_alias=resp.get("ThemeAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_theme_permissions(
    aws_account_id: str,
    theme_id: str,
    region_name: str | None = None,
) -> DescribeThemePermissionsResult:
    """Describe theme permissions.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    try:
        resp = await client.call("DescribeThemePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe theme permissions") from exc
    return DescribeThemePermissionsResult(
        theme_id=resp.get("ThemeId"),
        theme_arn=resp.get("ThemeArn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_topic(
    aws_account_id: str,
    topic_id: str,
    region_name: str | None = None,
) -> DescribeTopicResult:
    """Describe topic.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    try:
        resp = await client.call("DescribeTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe topic") from exc
    return DescribeTopicResult(
        arn=resp.get("Arn"),
        topic_id=resp.get("TopicId"),
        topic=resp.get("Topic"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        custom_instructions=resp.get("CustomInstructions"),
    )


async def describe_topic_permissions(
    aws_account_id: str,
    topic_id: str,
    region_name: str | None = None,
) -> DescribeTopicPermissionsResult:
    """Describe topic permissions.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    try:
        resp = await client.call("DescribeTopicPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe topic permissions") from exc
    return DescribeTopicPermissionsResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        permissions=resp.get("Permissions"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_topic_refresh(
    aws_account_id: str,
    topic_id: str,
    refresh_id: str,
    region_name: str | None = None,
) -> DescribeTopicRefreshResult:
    """Describe topic refresh.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        refresh_id: Refresh id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["RefreshId"] = refresh_id
    try:
        resp = await client.call("DescribeTopicRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe topic refresh") from exc
    return DescribeTopicRefreshResult(
        refresh_details=resp.get("RefreshDetails"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def describe_topic_refresh_schedule(
    aws_account_id: str,
    topic_id: str,
    dataset_id: str,
    region_name: str | None = None,
) -> DescribeTopicRefreshScheduleResult:
    """Describe topic refresh schedule.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        dataset_id: Dataset id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["DatasetId"] = dataset_id
    try:
        resp = await client.call("DescribeTopicRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe topic refresh schedule") from exc
    return DescribeTopicRefreshScheduleResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        dataset_arn=resp.get("DatasetArn"),
        refresh_schedule=resp.get("RefreshSchedule"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def describe_vpc_connection(
    aws_account_id: str,
    vpc_connection_id: str,
    region_name: str | None = None,
) -> DescribeVpcConnectionResult:
    """Describe vpc connection.

    Args:
        aws_account_id: Aws account id.
        vpc_connection_id: Vpc connection id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["VPCConnectionId"] = vpc_connection_id
    try:
        resp = await client.call("DescribeVPCConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc connection") from exc
    return DescribeVpcConnectionResult(
        vpc_connection=resp.get("VPCConnection"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def generate_embed_url_for_anonymous_user(
    aws_account_id: str,
    namespace: str,
    authorized_resource_arns: list[str],
    experience_configuration: dict[str, Any],
    *,
    session_lifetime_in_minutes: int | None = None,
    session_tags: list[dict[str, Any]] | None = None,
    allowed_domains: list[str] | None = None,
    region_name: str | None = None,
) -> GenerateEmbedUrlForAnonymousUserResult:
    """Generate embed url for anonymous user.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        authorized_resource_arns: Authorized resource arns.
        experience_configuration: Experience configuration.
        session_lifetime_in_minutes: Session lifetime in minutes.
        session_tags: Session tags.
        allowed_domains: Allowed domains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["AuthorizedResourceArns"] = authorized_resource_arns
    kwargs["ExperienceConfiguration"] = experience_configuration
    if session_lifetime_in_minutes is not None:
        kwargs["SessionLifetimeInMinutes"] = session_lifetime_in_minutes
    if session_tags is not None:
        kwargs["SessionTags"] = session_tags
    if allowed_domains is not None:
        kwargs["AllowedDomains"] = allowed_domains
    try:
        resp = await client.call("GenerateEmbedUrlForAnonymousUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate embed url for anonymous user") from exc
    return GenerateEmbedUrlForAnonymousUserResult(
        embed_url=resp.get("EmbedUrl"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        anonymous_user_arn=resp.get("AnonymousUserArn"),
    )


async def generate_embed_url_for_registered_user(
    aws_account_id: str,
    user_arn: str,
    experience_configuration: dict[str, Any],
    *,
    session_lifetime_in_minutes: int | None = None,
    allowed_domains: list[str] | None = None,
    region_name: str | None = None,
) -> GenerateEmbedUrlForRegisteredUserResult:
    """Generate embed url for registered user.

    Args:
        aws_account_id: Aws account id.
        user_arn: User arn.
        experience_configuration: Experience configuration.
        session_lifetime_in_minutes: Session lifetime in minutes.
        allowed_domains: Allowed domains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["UserArn"] = user_arn
    kwargs["ExperienceConfiguration"] = experience_configuration
    if session_lifetime_in_minutes is not None:
        kwargs["SessionLifetimeInMinutes"] = session_lifetime_in_minutes
    if allowed_domains is not None:
        kwargs["AllowedDomains"] = allowed_domains
    try:
        resp = await client.call("GenerateEmbedUrlForRegisteredUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate embed url for registered user") from exc
    return GenerateEmbedUrlForRegisteredUserResult(
        embed_url=resp.get("EmbedUrl"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def generate_embed_url_for_registered_user_with_identity(
    aws_account_id: str,
    experience_configuration: dict[str, Any],
    *,
    session_lifetime_in_minutes: int | None = None,
    allowed_domains: list[str] | None = None,
    region_name: str | None = None,
) -> GenerateEmbedUrlForRegisteredUserWithIdentityResult:
    """Generate embed url for registered user with identity.

    Args:
        aws_account_id: Aws account id.
        experience_configuration: Experience configuration.
        session_lifetime_in_minutes: Session lifetime in minutes.
        allowed_domains: Allowed domains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ExperienceConfiguration"] = experience_configuration
    if session_lifetime_in_minutes is not None:
        kwargs["SessionLifetimeInMinutes"] = session_lifetime_in_minutes
    if allowed_domains is not None:
        kwargs["AllowedDomains"] = allowed_domains
    try:
        resp = await client.call("GenerateEmbedUrlForRegisteredUserWithIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to generate embed url for registered user with identity"
        ) from exc
    return GenerateEmbedUrlForRegisteredUserWithIdentityResult(
        embed_url=resp.get("EmbedUrl"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def get_dashboard_embed_url(
    aws_account_id: str,
    dashboard_id: str,
    identity_type: str,
    *,
    session_lifetime_in_minutes: int | None = None,
    undo_redo_disabled: bool | None = None,
    reset_disabled: bool | None = None,
    state_persistence_enabled: bool | None = None,
    user_arn: str | None = None,
    namespace: str | None = None,
    additional_dashboard_ids: list[str] | None = None,
    region_name: str | None = None,
) -> GetDashboardEmbedUrlResult:
    """Get dashboard embed url.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        identity_type: Identity type.
        session_lifetime_in_minutes: Session lifetime in minutes.
        undo_redo_disabled: Undo redo disabled.
        reset_disabled: Reset disabled.
        state_persistence_enabled: State persistence enabled.
        user_arn: User arn.
        namespace: Namespace.
        additional_dashboard_ids: Additional dashboard ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["IdentityType"] = identity_type
    if session_lifetime_in_minutes is not None:
        kwargs["SessionLifetimeInMinutes"] = session_lifetime_in_minutes
    if undo_redo_disabled is not None:
        kwargs["UndoRedoDisabled"] = undo_redo_disabled
    if reset_disabled is not None:
        kwargs["ResetDisabled"] = reset_disabled
    if state_persistence_enabled is not None:
        kwargs["StatePersistenceEnabled"] = state_persistence_enabled
    if user_arn is not None:
        kwargs["UserArn"] = user_arn
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if additional_dashboard_ids is not None:
        kwargs["AdditionalDashboardIds"] = additional_dashboard_ids
    try:
        resp = await client.call("GetDashboardEmbedUrl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dashboard embed url") from exc
    return GetDashboardEmbedUrlResult(
        embed_url=resp.get("EmbedUrl"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def get_flow_metadata(
    aws_account_id: str,
    flow_id: str,
    region_name: str | None = None,
) -> GetFlowMetadataResult:
    """Get flow metadata.

    Args:
        aws_account_id: Aws account id.
        flow_id: Flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FlowId"] = flow_id
    try:
        resp = await client.call("GetFlowMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get flow metadata") from exc
    return GetFlowMetadataResult(
        arn=resp.get("Arn"),
        flow_id=resp.get("FlowId"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        publish_state=resp.get("PublishState"),
        user_count=resp.get("UserCount"),
        run_count=resp.get("RunCount"),
        created_time=resp.get("CreatedTime"),
        last_updated_time=resp.get("LastUpdatedTime"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def get_flow_permissions(
    aws_account_id: str,
    flow_id: str,
    region_name: str | None = None,
) -> GetFlowPermissionsResult:
    """Get flow permissions.

    Args:
        aws_account_id: Aws account id.
        flow_id: Flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FlowId"] = flow_id
    try:
        resp = await client.call("GetFlowPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get flow permissions") from exc
    return GetFlowPermissionsResult(
        arn=resp.get("Arn"),
        flow_id=resp.get("FlowId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def get_session_embed_url(
    aws_account_id: str,
    *,
    entry_point: str | None = None,
    session_lifetime_in_minutes: int | None = None,
    user_arn: str | None = None,
    region_name: str | None = None,
) -> GetSessionEmbedUrlResult:
    """Get session embed url.

    Args:
        aws_account_id: Aws account id.
        entry_point: Entry point.
        session_lifetime_in_minutes: Session lifetime in minutes.
        user_arn: User arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if entry_point is not None:
        kwargs["EntryPoint"] = entry_point
    if session_lifetime_in_minutes is not None:
        kwargs["SessionLifetimeInMinutes"] = session_lifetime_in_minutes
    if user_arn is not None:
        kwargs["UserArn"] = user_arn
    try:
        resp = await client.call("GetSessionEmbedUrl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get session embed url") from exc
    return GetSessionEmbedUrlResult(
        embed_url=resp.get("EmbedUrl"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_action_connectors(
    aws_account_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListActionConnectorsResult:
    """List action connectors.

    Args:
        aws_account_id: Aws account id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListActionConnectors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list action connectors") from exc
    return ListActionConnectorsResult(
        action_connector_summaries=resp.get("ActionConnectorSummaries"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_asset_bundle_export_jobs(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAssetBundleExportJobsResult:
    """List asset bundle export jobs.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAssetBundleExportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset bundle export jobs") from exc
    return ListAssetBundleExportJobsResult(
        asset_bundle_export_job_summary_list=resp.get("AssetBundleExportJobSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_asset_bundle_import_jobs(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAssetBundleImportJobsResult:
    """List asset bundle import jobs.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAssetBundleImportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset bundle import jobs") from exc
    return ListAssetBundleImportJobsResult(
        asset_bundle_import_job_summary_list=resp.get("AssetBundleImportJobSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_brands(
    aws_account_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBrandsResult:
    """List brands.

    Args:
        aws_account_id: Aws account id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListBrands", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list brands") from exc
    return ListBrandsResult(
        next_token=resp.get("NextToken"),
        brands=resp.get("Brands"),
    )


async def list_custom_permissions(
    aws_account_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCustomPermissionsResult:
    """List custom permissions.

    Args:
        aws_account_id: Aws account id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListCustomPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom permissions") from exc
    return ListCustomPermissionsResult(
        status=resp.get("Status"),
        custom_permissions_list=resp.get("CustomPermissionsList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
    )


async def list_dashboard_versions(
    aws_account_id: str,
    dashboard_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDashboardVersionsResult:
    """List dashboard versions.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDashboardVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dashboard versions") from exc
    return ListDashboardVersionsResult(
        dashboard_version_summary_list=resp.get("DashboardVersionSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_data_sets(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDataSetsResult:
    """List data sets.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDataSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data sets") from exc
    return ListDataSetsResult(
        data_set_summaries=resp.get("DataSetSummaries"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_flows(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFlowsResult:
    """List flows.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListFlows", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list flows") from exc
    return ListFlowsResult(
        flow_summary_list=resp.get("FlowSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_folder_members(
    aws_account_id: str,
    folder_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFolderMembersResult:
    """List folder members.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListFolderMembers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list folder members") from exc
    return ListFolderMembersResult(
        status=resp.get("Status"),
        folder_member_list=resp.get("FolderMemberList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
    )


async def list_folders(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFoldersResult:
    """List folders.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListFolders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list folders") from exc
    return ListFoldersResult(
        status=resp.get("Status"),
        folder_summary_list=resp.get("FolderSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
    )


async def list_folders_for_resource(
    aws_account_id: str,
    resource_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFoldersForResourceResult:
    """List folders for resource.

    Args:
        aws_account_id: Aws account id.
        resource_arn: Resource arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ResourceArn"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListFoldersForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list folders for resource") from exc
    return ListFoldersForResourceResult(
        status=resp.get("Status"),
        folders=resp.get("Folders"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
    )


async def list_group_memberships(
    group_name: str,
    aws_account_id: str,
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListGroupMembershipsResult:
    """List group memberships.

    Args:
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListGroupMemberships", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list group memberships") from exc
    return ListGroupMembershipsResult(
        group_member_list=resp.get("GroupMemberList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_groups(
    aws_account_id: str,
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListGroupsResult:
    """List groups.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list groups") from exc
    return ListGroupsResult(
        group_list=resp.get("GroupList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_iam_policy_assignments(
    aws_account_id: str,
    namespace: str,
    *,
    assignment_status: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListIamPolicyAssignmentsResult:
    """List iam policy assignments.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        assignment_status: Assignment status.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if assignment_status is not None:
        kwargs["AssignmentStatus"] = assignment_status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListIAMPolicyAssignments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list iam policy assignments") from exc
    return ListIamPolicyAssignmentsResult(
        iam_policy_assignments=resp.get("IAMPolicyAssignments"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_iam_policy_assignments_for_user(
    aws_account_id: str,
    user_name: str,
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListIamPolicyAssignmentsForUserResult:
    """List iam policy assignments for user.

    Args:
        aws_account_id: Aws account id.
        user_name: User name.
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["UserName"] = user_name
    kwargs["Namespace"] = namespace
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListIAMPolicyAssignmentsForUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list iam policy assignments for user") from exc
    return ListIamPolicyAssignmentsForUserResult(
        active_assignments=resp.get("ActiveAssignments"),
        request_id=resp.get("RequestId"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
    )


async def list_identity_propagation_configs(
    aws_account_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIdentityPropagationConfigsResult:
    """List identity propagation configs.

    Args:
        aws_account_id: Aws account id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListIdentityPropagationConfigs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list identity propagation configs") from exc
    return ListIdentityPropagationConfigsResult(
        services=resp.get("Services"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_ingestions(
    data_set_id: str,
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListIngestionsResult:
    """List ingestions.

    Args:
        data_set_id: Data set id.
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSetId"] = data_set_id
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListIngestions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ingestions") from exc
    return ListIngestionsResult(
        ingestions=resp.get("Ingestions"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_namespaces(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListNamespacesResult:
    """List namespaces.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListNamespaces", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list namespaces") from exc
    return ListNamespacesResult(
        namespaces=resp.get("Namespaces"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_refresh_schedules(
    aws_account_id: str,
    data_set_id: str,
    region_name: str | None = None,
) -> ListRefreshSchedulesResult:
    """List refresh schedules.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    try:
        resp = await client.call("ListRefreshSchedules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list refresh schedules") from exc
    return ListRefreshSchedulesResult(
        refresh_schedules=resp.get("RefreshSchedules"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_role_memberships(
    role: str,
    aws_account_id: str,
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRoleMembershipsResult:
    """List role memberships.

    Args:
        role: Role.
        aws_account_id: Aws account id.
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Role"] = role
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListRoleMemberships", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list role memberships") from exc
    return ListRoleMembershipsResult(
        members_list=resp.get("MembersList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
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
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_template_aliases(
    aws_account_id: str,
    template_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTemplateAliasesResult:
    """List template aliases.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTemplateAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list template aliases") from exc
    return ListTemplateAliasesResult(
        template_alias_list=resp.get("TemplateAliasList"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        next_token=resp.get("NextToken"),
    )


async def list_template_versions(
    aws_account_id: str,
    template_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTemplateVersionsResult:
    """List template versions.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTemplateVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list template versions") from exc
    return ListTemplateVersionsResult(
        template_version_summary_list=resp.get("TemplateVersionSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_templates(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTemplatesResult:
    """List templates.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list templates") from exc
    return ListTemplatesResult(
        template_summary_list=resp.get("TemplateSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_theme_aliases(
    aws_account_id: str,
    theme_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThemeAliasesResult:
    """List theme aliases.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListThemeAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list theme aliases") from exc
    return ListThemeAliasesResult(
        theme_alias_list=resp.get("ThemeAliasList"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        next_token=resp.get("NextToken"),
    )


async def list_theme_versions(
    aws_account_id: str,
    theme_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThemeVersionsResult:
    """List theme versions.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListThemeVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list theme versions") from exc
    return ListThemeVersionsResult(
        theme_version_summary_list=resp.get("ThemeVersionSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_themes(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    type_value: str | None = None,
    region_name: str | None = None,
) -> ListThemesResult:
    """List themes.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if type_value is not None:
        kwargs["Type"] = type_value
    try:
        resp = await client.call("ListThemes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list themes") from exc
    return ListThemesResult(
        theme_summary_list=resp.get("ThemeSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_topic_refresh_schedules(
    aws_account_id: str,
    topic_id: str,
    region_name: str | None = None,
) -> ListTopicRefreshSchedulesResult:
    """List topic refresh schedules.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    try:
        resp = await client.call("ListTopicRefreshSchedules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list topic refresh schedules") from exc
    return ListTopicRefreshSchedulesResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        refresh_schedules=resp.get("RefreshSchedules"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_topic_reviewed_answers(
    aws_account_id: str,
    topic_id: str,
    region_name: str | None = None,
) -> ListTopicReviewedAnswersResult:
    """List topic reviewed answers.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    try:
        resp = await client.call("ListTopicReviewedAnswers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list topic reviewed answers") from exc
    return ListTopicReviewedAnswersResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        answers=resp.get("Answers"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def list_topics(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTopicsResult:
    """List topics.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTopics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list topics") from exc
    return ListTopicsResult(
        topics_summaries=resp.get("TopicsSummaries"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_user_groups(
    user_name: str,
    aws_account_id: str,
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUserGroupsResult:
    """List user groups.

    Args:
        user_name: User name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListUserGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list user groups") from exc
    return ListUserGroupsResult(
        group_list=resp.get("GroupList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def list_vpc_connections(
    aws_account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListVpcConnectionsResult:
    """List vpc connections.

    Args:
        aws_account_id: Aws account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListVPCConnections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list vpc connections") from exc
    return ListVpcConnectionsResult(
        vpc_connection_summaries=resp.get("VPCConnectionSummaries"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def predict_qa_results(
    aws_account_id: str,
    query_text: str,
    *,
    include_quick_sight_q_index: str | None = None,
    include_generated_answer: str | None = None,
    max_topics_to_consider: int | None = None,
    region_name: str | None = None,
) -> PredictQaResultsResult:
    """Predict qa results.

    Args:
        aws_account_id: Aws account id.
        query_text: Query text.
        include_quick_sight_q_index: Include quick sight q index.
        include_generated_answer: Include generated answer.
        max_topics_to_consider: Max topics to consider.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["QueryText"] = query_text
    if include_quick_sight_q_index is not None:
        kwargs["IncludeQuickSightQIndex"] = include_quick_sight_q_index
    if include_generated_answer is not None:
        kwargs["IncludeGeneratedAnswer"] = include_generated_answer
    if max_topics_to_consider is not None:
        kwargs["MaxTopicsToConsider"] = max_topics_to_consider
    try:
        resp = await client.call("PredictQAResults", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to predict qa results") from exc
    return PredictQaResultsResult(
        primary_result=resp.get("PrimaryResult"),
        additional_results=resp.get("AdditionalResults"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def put_data_set_refresh_properties(
    aws_account_id: str,
    data_set_id: str,
    data_set_refresh_properties: dict[str, Any],
    region_name: str | None = None,
) -> PutDataSetRefreshPropertiesResult:
    """Put data set refresh properties.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        data_set_refresh_properties: Data set refresh properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["DataSetRefreshProperties"] = data_set_refresh_properties
    try:
        resp = await client.call("PutDataSetRefreshProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put data set refresh properties") from exc
    return PutDataSetRefreshPropertiesResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def restore_analysis(
    aws_account_id: str,
    analysis_id: str,
    *,
    restore_to_folders: bool | None = None,
    region_name: str | None = None,
) -> RestoreAnalysisResult:
    """Restore analysis.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        restore_to_folders: Restore to folders.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    if restore_to_folders is not None:
        kwargs["RestoreToFolders"] = restore_to_folders
    try:
        resp = await client.call("RestoreAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore analysis") from exc
    return RestoreAnalysisResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        analysis_id=resp.get("AnalysisId"),
        request_id=resp.get("RequestId"),
        restoration_failed_folder_arns=resp.get("RestorationFailedFolderArns"),
    )


async def search_action_connectors(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SearchActionConnectorsResult:
    """Search action connectors.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("SearchActionConnectors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search action connectors") from exc
    return SearchActionConnectorsResult(
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        action_connector_summaries=resp.get("ActionConnectorSummaries"),
    )


async def search_analyses(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchAnalysesResult:
    """Search analyses.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchAnalyses", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search analyses") from exc
    return SearchAnalysesResult(
        analysis_summary_list=resp.get("AnalysisSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def search_dashboards(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchDashboardsResult:
    """Search dashboards.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchDashboards", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search dashboards") from exc
    return SearchDashboardsResult(
        dashboard_summary_list=resp.get("DashboardSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def search_data_sets(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchDataSetsResult:
    """Search data sets.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchDataSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search data sets") from exc
    return SearchDataSetsResult(
        data_set_summaries=resp.get("DataSetSummaries"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def search_data_sources(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchDataSourcesResult:
    """Search data sources.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchDataSources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search data sources") from exc
    return SearchDataSourcesResult(
        data_source_summaries=resp.get("DataSourceSummaries"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def search_flows(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchFlowsResult:
    """Search flows.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchFlows", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search flows") from exc
    return SearchFlowsResult(
        flow_summary_list=resp.get("FlowSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def search_folders(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchFoldersResult:
    """Search folders.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchFolders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search folders") from exc
    return SearchFoldersResult(
        status=resp.get("Status"),
        folder_summary_list=resp.get("FolderSummaryList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
    )


async def search_groups(
    aws_account_id: str,
    namespace: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchGroupsResult:
    """Search groups.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search groups") from exc
    return SearchGroupsResult(
        group_list=resp.get("GroupList"),
        next_token=resp.get("NextToken"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def search_topics(
    aws_account_id: str,
    filters: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> SearchTopicsResult:
    """Search topics.

    Args:
        aws_account_id: Aws account id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("SearchTopics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search topics") from exc
    return SearchTopicsResult(
        topic_summary_list=resp.get("TopicSummaryList"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def start_asset_bundle_export_job(
    aws_account_id: str,
    asset_bundle_export_job_id: str,
    resource_arns: list[str],
    export_format: str,
    *,
    include_all_dependencies: bool | None = None,
    cloud_formation_override_property_configuration: dict[str, Any] | None = None,
    include_permissions: bool | None = None,
    include_tags: bool | None = None,
    validation_strategy: dict[str, Any] | None = None,
    include_folder_memberships: bool | None = None,
    include_folder_members: str | None = None,
    region_name: str | None = None,
) -> StartAssetBundleExportJobResult:
    """Start asset bundle export job.

    Args:
        aws_account_id: Aws account id.
        asset_bundle_export_job_id: Asset bundle export job id.
        resource_arns: Resource arns.
        export_format: Export format.
        include_all_dependencies: Include all dependencies.
        cloud_formation_override_property_configuration: Cloud formation override property configuration.
        include_permissions: Include permissions.
        include_tags: Include tags.
        validation_strategy: Validation strategy.
        include_folder_memberships: Include folder memberships.
        include_folder_members: Include folder members.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssetBundleExportJobId"] = asset_bundle_export_job_id
    kwargs["ResourceArns"] = resource_arns
    kwargs["ExportFormat"] = export_format
    if include_all_dependencies is not None:
        kwargs["IncludeAllDependencies"] = include_all_dependencies
    if cloud_formation_override_property_configuration is not None:
        kwargs["CloudFormationOverridePropertyConfiguration"] = (
            cloud_formation_override_property_configuration
        )
    if include_permissions is not None:
        kwargs["IncludePermissions"] = include_permissions
    if include_tags is not None:
        kwargs["IncludeTags"] = include_tags
    if validation_strategy is not None:
        kwargs["ValidationStrategy"] = validation_strategy
    if include_folder_memberships is not None:
        kwargs["IncludeFolderMemberships"] = include_folder_memberships
    if include_folder_members is not None:
        kwargs["IncludeFolderMembers"] = include_folder_members
    try:
        resp = await client.call("StartAssetBundleExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start asset bundle export job") from exc
    return StartAssetBundleExportJobResult(
        arn=resp.get("Arn"),
        asset_bundle_export_job_id=resp.get("AssetBundleExportJobId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def start_asset_bundle_import_job(
    aws_account_id: str,
    asset_bundle_import_job_id: str,
    asset_bundle_import_source: dict[str, Any],
    *,
    override_parameters: dict[str, Any] | None = None,
    failure_action: str | None = None,
    override_permissions: dict[str, Any] | None = None,
    override_tags: dict[str, Any] | None = None,
    override_validation_strategy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartAssetBundleImportJobResult:
    """Start asset bundle import job.

    Args:
        aws_account_id: Aws account id.
        asset_bundle_import_job_id: Asset bundle import job id.
        asset_bundle_import_source: Asset bundle import source.
        override_parameters: Override parameters.
        failure_action: Failure action.
        override_permissions: Override permissions.
        override_tags: Override tags.
        override_validation_strategy: Override validation strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssetBundleImportJobId"] = asset_bundle_import_job_id
    kwargs["AssetBundleImportSource"] = asset_bundle_import_source
    if override_parameters is not None:
        kwargs["OverrideParameters"] = override_parameters
    if failure_action is not None:
        kwargs["FailureAction"] = failure_action
    if override_permissions is not None:
        kwargs["OverridePermissions"] = override_permissions
    if override_tags is not None:
        kwargs["OverrideTags"] = override_tags
    if override_validation_strategy is not None:
        kwargs["OverrideValidationStrategy"] = override_validation_strategy
    try:
        resp = await client.call("StartAssetBundleImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start asset bundle import job") from exc
    return StartAssetBundleImportJobResult(
        arn=resp.get("Arn"),
        asset_bundle_import_job_id=resp.get("AssetBundleImportJobId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def start_dashboard_snapshot_job(
    aws_account_id: str,
    dashboard_id: str,
    snapshot_job_id: str,
    user_configuration: dict[str, Any],
    snapshot_configuration: dict[str, Any],
    region_name: str | None = None,
) -> StartDashboardSnapshotJobResult:
    """Start dashboard snapshot job.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        snapshot_job_id: Snapshot job id.
        user_configuration: User configuration.
        snapshot_configuration: Snapshot configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["SnapshotJobId"] = snapshot_job_id
    kwargs["UserConfiguration"] = user_configuration
    kwargs["SnapshotConfiguration"] = snapshot_configuration
    try:
        resp = await client.call("StartDashboardSnapshotJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start dashboard snapshot job") from exc
    return StartDashboardSnapshotJobResult(
        arn=resp.get("Arn"),
        snapshot_job_id=resp.get("SnapshotJobId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def start_dashboard_snapshot_job_schedule(
    aws_account_id: str,
    dashboard_id: str,
    schedule_id: str,
    region_name: str | None = None,
) -> StartDashboardSnapshotJobScheduleResult:
    """Start dashboard snapshot job schedule.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        schedule_id: Schedule id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["ScheduleId"] = schedule_id
    try:
        resp = await client.call("StartDashboardSnapshotJobSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start dashboard snapshot job schedule") from exc
    return StartDashboardSnapshotJobScheduleResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> TagResourceResult:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        resp = await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return TagResourceResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> UntagResourceResult:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        resp = await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return UntagResourceResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_account_custom_permission(
    custom_permissions_name: str,
    aws_account_id: str,
    region_name: str | None = None,
) -> UpdateAccountCustomPermissionResult:
    """Update account custom permission.

    Args:
        custom_permissions_name: Custom permissions name.
        aws_account_id: Aws account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CustomPermissionsName"] = custom_permissions_name
    kwargs["AwsAccountId"] = aws_account_id
    try:
        resp = await client.call("UpdateAccountCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account custom permission") from exc
    return UpdateAccountCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_account_customization(
    aws_account_id: str,
    account_customization: dict[str, Any],
    *,
    namespace: str | None = None,
    region_name: str | None = None,
) -> UpdateAccountCustomizationResult:
    """Update account customization.

    Args:
        aws_account_id: Aws account id.
        account_customization: Account customization.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AccountCustomization"] = account_customization
    if namespace is not None:
        kwargs["Namespace"] = namespace
    try:
        resp = await client.call("UpdateAccountCustomization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account customization") from exc
    return UpdateAccountCustomizationResult(
        arn=resp.get("Arn"),
        aws_account_id=resp.get("AwsAccountId"),
        namespace=resp.get("Namespace"),
        account_customization=resp.get("AccountCustomization"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_account_settings(
    aws_account_id: str,
    default_namespace: str,
    *,
    notification_email: str | None = None,
    termination_protection_enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateAccountSettingsResult:
    """Update account settings.

    Args:
        aws_account_id: Aws account id.
        default_namespace: Default namespace.
        notification_email: Notification email.
        termination_protection_enabled: Termination protection enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DefaultNamespace"] = default_namespace
    if notification_email is not None:
        kwargs["NotificationEmail"] = notification_email
    if termination_protection_enabled is not None:
        kwargs["TerminationProtectionEnabled"] = termination_protection_enabled
    try:
        resp = await client.call("UpdateAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account settings") from exc
    return UpdateAccountSettingsResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_action_connector(
    aws_account_id: str,
    action_connector_id: str,
    name: str,
    authentication_config: dict[str, Any],
    *,
    description: str | None = None,
    vpc_connection_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateActionConnectorResult:
    """Update action connector.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        name: Name.
        authentication_config: Authentication config.
        description: Description.
        vpc_connection_arn: Vpc connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    kwargs["Name"] = name
    kwargs["AuthenticationConfig"] = authentication_config
    if description is not None:
        kwargs["Description"] = description
    if vpc_connection_arn is not None:
        kwargs["VpcConnectionArn"] = vpc_connection_arn
    try:
        resp = await client.call("UpdateActionConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update action connector") from exc
    return UpdateActionConnectorResult(
        arn=resp.get("Arn"),
        action_connector_id=resp.get("ActionConnectorId"),
        request_id=resp.get("RequestId"),
        update_status=resp.get("UpdateStatus"),
        status=resp.get("Status"),
    )


async def update_action_connector_permissions(
    aws_account_id: str,
    action_connector_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateActionConnectorPermissionsResult:
    """Update action connector permissions.

    Args:
        aws_account_id: Aws account id.
        action_connector_id: Action connector id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ActionConnectorId"] = action_connector_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateActionConnectorPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update action connector permissions") from exc
    return UpdateActionConnectorPermissionsResult(
        arn=resp.get("Arn"),
        action_connector_id=resp.get("ActionConnectorId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        permissions=resp.get("Permissions"),
    )


async def update_analysis(
    aws_account_id: str,
    analysis_id: str,
    name: str,
    *,
    parameters: dict[str, Any] | None = None,
    source_entity: dict[str, Any] | None = None,
    theme_arn: str | None = None,
    definition: dict[str, Any] | None = None,
    validation_strategy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateAnalysisResult:
    """Update analysis.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        name: Name.
        parameters: Parameters.
        source_entity: Source entity.
        theme_arn: Theme arn.
        definition: Definition.
        validation_strategy: Validation strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    kwargs["Name"] = name
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if source_entity is not None:
        kwargs["SourceEntity"] = source_entity
    if theme_arn is not None:
        kwargs["ThemeArn"] = theme_arn
    if definition is not None:
        kwargs["Definition"] = definition
    if validation_strategy is not None:
        kwargs["ValidationStrategy"] = validation_strategy
    try:
        resp = await client.call("UpdateAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update analysis") from exc
    return UpdateAnalysisResult(
        arn=resp.get("Arn"),
        analysis_id=resp.get("AnalysisId"),
        update_status=resp.get("UpdateStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_analysis_permissions(
    aws_account_id: str,
    analysis_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateAnalysisPermissionsResult:
    """Update analysis permissions.

    Args:
        aws_account_id: Aws account id.
        analysis_id: Analysis id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AnalysisId"] = analysis_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateAnalysisPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update analysis permissions") from exc
    return UpdateAnalysisPermissionsResult(
        analysis_arn=resp.get("AnalysisArn"),
        analysis_id=resp.get("AnalysisId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_application_with_token_exchange_grant(
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> UpdateApplicationWithTokenExchangeGrantResult:
    """Update application with token exchange grant.

    Args:
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("UpdateApplicationWithTokenExchangeGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update application with token exchange grant") from exc
    return UpdateApplicationWithTokenExchangeGrantResult(
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_brand(
    aws_account_id: str,
    brand_id: str,
    *,
    brand_definition: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateBrandResult:
    """Update brand.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        brand_definition: Brand definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    if brand_definition is not None:
        kwargs["BrandDefinition"] = brand_definition
    try:
        resp = await client.call("UpdateBrand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update brand") from exc
    return UpdateBrandResult(
        request_id=resp.get("RequestId"),
        brand_detail=resp.get("BrandDetail"),
        brand_definition=resp.get("BrandDefinition"),
    )


async def update_brand_assignment(
    aws_account_id: str,
    brand_arn: str,
    region_name: str | None = None,
) -> UpdateBrandAssignmentResult:
    """Update brand assignment.

    Args:
        aws_account_id: Aws account id.
        brand_arn: Brand arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandArn"] = brand_arn
    try:
        resp = await client.call("UpdateBrandAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update brand assignment") from exc
    return UpdateBrandAssignmentResult(
        request_id=resp.get("RequestId"),
        brand_arn=resp.get("BrandArn"),
    )


async def update_brand_published_version(
    aws_account_id: str,
    brand_id: str,
    version_id: str,
    region_name: str | None = None,
) -> UpdateBrandPublishedVersionResult:
    """Update brand published version.

    Args:
        aws_account_id: Aws account id.
        brand_id: Brand id.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["BrandId"] = brand_id
    kwargs["VersionId"] = version_id
    try:
        resp = await client.call("UpdateBrandPublishedVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update brand published version") from exc
    return UpdateBrandPublishedVersionResult(
        request_id=resp.get("RequestId"),
        version_id=resp.get("VersionId"),
    )


async def update_custom_permissions(
    aws_account_id: str,
    custom_permissions_name: str,
    *,
    capabilities: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateCustomPermissionsResult:
    """Update custom permissions.

    Args:
        aws_account_id: Aws account id.
        custom_permissions_name: Custom permissions name.
        capabilities: Capabilities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["CustomPermissionsName"] = custom_permissions_name
    if capabilities is not None:
        kwargs["Capabilities"] = capabilities
    try:
        resp = await client.call("UpdateCustomPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update custom permissions") from exc
    return UpdateCustomPermissionsResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        request_id=resp.get("RequestId"),
    )


async def update_dashboard(
    aws_account_id: str,
    dashboard_id: str,
    name: str,
    *,
    source_entity: dict[str, Any] | None = None,
    parameters: dict[str, Any] | None = None,
    version_description: str | None = None,
    dashboard_publish_options: dict[str, Any] | None = None,
    theme_arn: str | None = None,
    definition: dict[str, Any] | None = None,
    validation_strategy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDashboardResult:
    """Update dashboard.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        name: Name.
        source_entity: Source entity.
        parameters: Parameters.
        version_description: Version description.
        dashboard_publish_options: Dashboard publish options.
        theme_arn: Theme arn.
        definition: Definition.
        validation_strategy: Validation strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["Name"] = name
    if source_entity is not None:
        kwargs["SourceEntity"] = source_entity
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if dashboard_publish_options is not None:
        kwargs["DashboardPublishOptions"] = dashboard_publish_options
    if theme_arn is not None:
        kwargs["ThemeArn"] = theme_arn
    if definition is not None:
        kwargs["Definition"] = definition
    if validation_strategy is not None:
        kwargs["ValidationStrategy"] = validation_strategy
    try:
        resp = await client.call("UpdateDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard") from exc
    return UpdateDashboardResult(
        arn=resp.get("Arn"),
        version_arn=resp.get("VersionArn"),
        dashboard_id=resp.get("DashboardId"),
        creation_status=resp.get("CreationStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_dashboard_links(
    aws_account_id: str,
    dashboard_id: str,
    link_entities: list[str],
    region_name: str | None = None,
) -> UpdateDashboardLinksResult:
    """Update dashboard links.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        link_entities: Link entities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["LinkEntities"] = link_entities
    try:
        resp = await client.call("UpdateDashboardLinks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard links") from exc
    return UpdateDashboardLinksResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        dashboard_arn=resp.get("DashboardArn"),
        link_entities=resp.get("LinkEntities"),
    )


async def update_dashboard_permissions(
    aws_account_id: str,
    dashboard_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    grant_link_permissions: list[dict[str, Any]] | None = None,
    revoke_link_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateDashboardPermissionsResult:
    """Update dashboard permissions.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        grant_link_permissions: Grant link permissions.
        revoke_link_permissions: Revoke link permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    if grant_link_permissions is not None:
        kwargs["GrantLinkPermissions"] = grant_link_permissions
    if revoke_link_permissions is not None:
        kwargs["RevokeLinkPermissions"] = revoke_link_permissions
    try:
        resp = await client.call("UpdateDashboardPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard permissions") from exc
    return UpdateDashboardPermissionsResult(
        dashboard_arn=resp.get("DashboardArn"),
        dashboard_id=resp.get("DashboardId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
        link_sharing_configuration=resp.get("LinkSharingConfiguration"),
    )


async def update_dashboard_published_version(
    aws_account_id: str,
    dashboard_id: str,
    version_number: int,
    region_name: str | None = None,
) -> UpdateDashboardPublishedVersionResult:
    """Update dashboard published version.

    Args:
        aws_account_id: Aws account id.
        dashboard_id: Dashboard id.
        version_number: Version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardId"] = dashboard_id
    kwargs["VersionNumber"] = version_number
    try:
        resp = await client.call("UpdateDashboardPublishedVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard published version") from exc
    return UpdateDashboardPublishedVersionResult(
        dashboard_id=resp.get("DashboardId"),
        dashboard_arn=resp.get("DashboardArn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_dashboards_qa_configuration(
    aws_account_id: str,
    dashboards_qa_status: str,
    region_name: str | None = None,
) -> UpdateDashboardsQaConfigurationResult:
    """Update dashboards qa configuration.

    Args:
        aws_account_id: Aws account id.
        dashboards_qa_status: Dashboards qa status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DashboardsQAStatus"] = dashboards_qa_status
    try:
        resp = await client.call("UpdateDashboardsQAConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboards qa configuration") from exc
    return UpdateDashboardsQaConfigurationResult(
        dashboards_qa_status=resp.get("DashboardsQAStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_data_set(
    aws_account_id: str,
    data_set_id: str,
    name: str,
    physical_table_map: dict[str, Any],
    import_mode: str,
    *,
    logical_table_map: dict[str, Any] | None = None,
    column_groups: list[dict[str, Any]] | None = None,
    field_folders: dict[str, Any] | None = None,
    row_level_permission_data_set: dict[str, Any] | None = None,
    row_level_permission_tag_configuration: dict[str, Any] | None = None,
    column_level_permission_rules: list[dict[str, Any]] | None = None,
    data_set_usage_configuration: dict[str, Any] | None = None,
    dataset_parameters: list[dict[str, Any]] | None = None,
    performance_configuration: dict[str, Any] | None = None,
    data_prep_configuration: dict[str, Any] | None = None,
    semantic_model_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDataSetResult:
    """Update data set.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        name: Name.
        physical_table_map: Physical table map.
        import_mode: Import mode.
        logical_table_map: Logical table map.
        column_groups: Column groups.
        field_folders: Field folders.
        row_level_permission_data_set: Row level permission data set.
        row_level_permission_tag_configuration: Row level permission tag configuration.
        column_level_permission_rules: Column level permission rules.
        data_set_usage_configuration: Data set usage configuration.
        dataset_parameters: Dataset parameters.
        performance_configuration: Performance configuration.
        data_prep_configuration: Data prep configuration.
        semantic_model_configuration: Semantic model configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    kwargs["Name"] = name
    kwargs["PhysicalTableMap"] = physical_table_map
    kwargs["ImportMode"] = import_mode
    if logical_table_map is not None:
        kwargs["LogicalTableMap"] = logical_table_map
    if column_groups is not None:
        kwargs["ColumnGroups"] = column_groups
    if field_folders is not None:
        kwargs["FieldFolders"] = field_folders
    if row_level_permission_data_set is not None:
        kwargs["RowLevelPermissionDataSet"] = row_level_permission_data_set
    if row_level_permission_tag_configuration is not None:
        kwargs["RowLevelPermissionTagConfiguration"] = row_level_permission_tag_configuration
    if column_level_permission_rules is not None:
        kwargs["ColumnLevelPermissionRules"] = column_level_permission_rules
    if data_set_usage_configuration is not None:
        kwargs["DataSetUsageConfiguration"] = data_set_usage_configuration
    if dataset_parameters is not None:
        kwargs["DatasetParameters"] = dataset_parameters
    if performance_configuration is not None:
        kwargs["PerformanceConfiguration"] = performance_configuration
    if data_prep_configuration is not None:
        kwargs["DataPrepConfiguration"] = data_prep_configuration
    if semantic_model_configuration is not None:
        kwargs["SemanticModelConfiguration"] = semantic_model_configuration
    try:
        resp = await client.call("UpdateDataSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data set") from exc
    return UpdateDataSetResult(
        arn=resp.get("Arn"),
        data_set_id=resp.get("DataSetId"),
        ingestion_arn=resp.get("IngestionArn"),
        ingestion_id=resp.get("IngestionId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_data_set_permissions(
    aws_account_id: str,
    data_set_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateDataSetPermissionsResult:
    """Update data set permissions.

    Args:
        aws_account_id: Aws account id.
        data_set_id: Data set id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSetId"] = data_set_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateDataSetPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data set permissions") from exc
    return UpdateDataSetPermissionsResult(
        data_set_arn=resp.get("DataSetArn"),
        data_set_id=resp.get("DataSetId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_data_source(
    aws_account_id: str,
    data_source_id: str,
    name: str,
    *,
    data_source_parameters: dict[str, Any] | None = None,
    credentials: dict[str, Any] | None = None,
    vpc_connection_properties: dict[str, Any] | None = None,
    ssl_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDataSourceResult:
    """Update data source.

    Args:
        aws_account_id: Aws account id.
        data_source_id: Data source id.
        name: Name.
        data_source_parameters: Data source parameters.
        credentials: Credentials.
        vpc_connection_properties: Vpc connection properties.
        ssl_properties: Ssl properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSourceId"] = data_source_id
    kwargs["Name"] = name
    if data_source_parameters is not None:
        kwargs["DataSourceParameters"] = data_source_parameters
    if credentials is not None:
        kwargs["Credentials"] = credentials
    if vpc_connection_properties is not None:
        kwargs["VpcConnectionProperties"] = vpc_connection_properties
    if ssl_properties is not None:
        kwargs["SslProperties"] = ssl_properties
    try:
        resp = await client.call("UpdateDataSource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data source") from exc
    return UpdateDataSourceResult(
        arn=resp.get("Arn"),
        data_source_id=resp.get("DataSourceId"),
        update_status=resp.get("UpdateStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_data_source_permissions(
    aws_account_id: str,
    data_source_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateDataSourcePermissionsResult:
    """Update data source permissions.

    Args:
        aws_account_id: Aws account id.
        data_source_id: Data source id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["DataSourceId"] = data_source_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateDataSourcePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data source permissions") from exc
    return UpdateDataSourcePermissionsResult(
        data_source_arn=resp.get("DataSourceArn"),
        data_source_id=resp.get("DataSourceId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_default_q_business_application(
    aws_account_id: str,
    application_id: str,
    *,
    namespace: str | None = None,
    region_name: str | None = None,
) -> UpdateDefaultQBusinessApplicationResult:
    """Update default q business application.

    Args:
        aws_account_id: Aws account id.
        application_id: Application id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ApplicationId"] = application_id
    if namespace is not None:
        kwargs["Namespace"] = namespace
    try:
        resp = await client.call("UpdateDefaultQBusinessApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update default q business application") from exc
    return UpdateDefaultQBusinessApplicationResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_flow_permissions(
    aws_account_id: str,
    flow_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateFlowPermissionsResult:
    """Update flow permissions.

    Args:
        aws_account_id: Aws account id.
        flow_id: Flow id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FlowId"] = flow_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateFlowPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update flow permissions") from exc
    return UpdateFlowPermissionsResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        flow_id=resp.get("FlowId"),
    )


async def update_folder(
    aws_account_id: str,
    folder_id: str,
    name: str,
    region_name: str | None = None,
) -> UpdateFolderResult:
    """Update folder.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    kwargs["Name"] = name
    try:
        resp = await client.call("UpdateFolder", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update folder") from exc
    return UpdateFolderResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        folder_id=resp.get("FolderId"),
        request_id=resp.get("RequestId"),
    )


async def update_folder_permissions(
    aws_account_id: str,
    folder_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateFolderPermissionsResult:
    """Update folder permissions.

    Args:
        aws_account_id: Aws account id.
        folder_id: Folder id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["FolderId"] = folder_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateFolderPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update folder permissions") from exc
    return UpdateFolderPermissionsResult(
        status=resp.get("Status"),
        arn=resp.get("Arn"),
        folder_id=resp.get("FolderId"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
    )


async def update_group(
    group_name: str,
    aws_account_id: str,
    namespace: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateGroupResult:
    """Update group.

    Args:
        group_name: Group name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update group") from exc
    return UpdateGroupResult(
        group=resp.get("Group"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_iam_policy_assignment(
    aws_account_id: str,
    assignment_name: str,
    namespace: str,
    *,
    assignment_status: str | None = None,
    policy_arn: str | None = None,
    identities: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateIamPolicyAssignmentResult:
    """Update iam policy assignment.

    Args:
        aws_account_id: Aws account id.
        assignment_name: Assignment name.
        namespace: Namespace.
        assignment_status: Assignment status.
        policy_arn: Policy arn.
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["AssignmentName"] = assignment_name
    kwargs["Namespace"] = namespace
    if assignment_status is not None:
        kwargs["AssignmentStatus"] = assignment_status
    if policy_arn is not None:
        kwargs["PolicyArn"] = policy_arn
    if identities is not None:
        kwargs["Identities"] = identities
    try:
        resp = await client.call("UpdateIAMPolicyAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update iam policy assignment") from exc
    return UpdateIamPolicyAssignmentResult(
        assignment_name=resp.get("AssignmentName"),
        assignment_id=resp.get("AssignmentId"),
        policy_arn=resp.get("PolicyArn"),
        identities=resp.get("Identities"),
        assignment_status=resp.get("AssignmentStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_identity_propagation_config(
    aws_account_id: str,
    service: str,
    *,
    authorized_targets: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateIdentityPropagationConfigResult:
    """Update identity propagation config.

    Args:
        aws_account_id: Aws account id.
        service: Service.
        authorized_targets: Authorized targets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Service"] = service
    if authorized_targets is not None:
        kwargs["AuthorizedTargets"] = authorized_targets
    try:
        resp = await client.call("UpdateIdentityPropagationConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update identity propagation config") from exc
    return UpdateIdentityPropagationConfigResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_ip_restriction(
    aws_account_id: str,
    *,
    ip_restriction_rule_map: dict[str, Any] | None = None,
    vpc_id_restriction_rule_map: dict[str, Any] | None = None,
    vpc_endpoint_id_restriction_rule_map: dict[str, Any] | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateIpRestrictionResult:
    """Update ip restriction.

    Args:
        aws_account_id: Aws account id.
        ip_restriction_rule_map: Ip restriction rule map.
        vpc_id_restriction_rule_map: Vpc id restriction rule map.
        vpc_endpoint_id_restriction_rule_map: Vpc endpoint id restriction rule map.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if ip_restriction_rule_map is not None:
        kwargs["IpRestrictionRuleMap"] = ip_restriction_rule_map
    if vpc_id_restriction_rule_map is not None:
        kwargs["VpcIdRestrictionRuleMap"] = vpc_id_restriction_rule_map
    if vpc_endpoint_id_restriction_rule_map is not None:
        kwargs["VpcEndpointIdRestrictionRuleMap"] = vpc_endpoint_id_restriction_rule_map
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = await client.call("UpdateIpRestriction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ip restriction") from exc
    return UpdateIpRestrictionResult(
        aws_account_id=resp.get("AwsAccountId"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_key_registration(
    aws_account_id: str,
    key_registration: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateKeyRegistrationResult:
    """Update key registration.

    Args:
        aws_account_id: Aws account id.
        key_registration: Key registration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["KeyRegistration"] = key_registration
    try:
        resp = await client.call("UpdateKeyRegistration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update key registration") from exc
    return UpdateKeyRegistrationResult(
        failed_key_registration=resp.get("FailedKeyRegistration"),
        successful_key_registration=resp.get("SuccessfulKeyRegistration"),
        request_id=resp.get("RequestId"),
    )


async def update_public_sharing_settings(
    aws_account_id: str,
    *,
    public_sharing_enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdatePublicSharingSettingsResult:
    """Update public sharing settings.

    Args:
        aws_account_id: Aws account id.
        public_sharing_enabled: Public sharing enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    if public_sharing_enabled is not None:
        kwargs["PublicSharingEnabled"] = public_sharing_enabled
    try:
        resp = await client.call("UpdatePublicSharingSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update public sharing settings") from exc
    return UpdatePublicSharingSettingsResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_q_personalization_configuration(
    aws_account_id: str,
    personalization_mode: str,
    region_name: str | None = None,
) -> UpdateQPersonalizationConfigurationResult:
    """Update q personalization configuration.

    Args:
        aws_account_id: Aws account id.
        personalization_mode: Personalization mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["PersonalizationMode"] = personalization_mode
    try:
        resp = await client.call("UpdateQPersonalizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update q personalization configuration") from exc
    return UpdateQPersonalizationConfigurationResult(
        personalization_mode=resp.get("PersonalizationMode"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_quick_sight_q_search_configuration(
    aws_account_id: str,
    q_search_status: str,
    region_name: str | None = None,
) -> UpdateQuickSightQSearchConfigurationResult:
    """Update quick sight q search configuration.

    Args:
        aws_account_id: Aws account id.
        q_search_status: Q search status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["QSearchStatus"] = q_search_status
    try:
        resp = await client.call("UpdateQuickSightQSearchConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update quick sight q search configuration") from exc
    return UpdateQuickSightQSearchConfigurationResult(
        q_search_status=resp.get("QSearchStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_refresh_schedule(
    data_set_id: str,
    aws_account_id: str,
    schedule: dict[str, Any],
    region_name: str | None = None,
) -> UpdateRefreshScheduleResult:
    """Update refresh schedule.

    Args:
        data_set_id: Data set id.
        aws_account_id: Aws account id.
        schedule: Schedule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSetId"] = data_set_id
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Schedule"] = schedule
    try:
        resp = await client.call("UpdateRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update refresh schedule") from exc
    return UpdateRefreshScheduleResult(
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
        schedule_id=resp.get("ScheduleId"),
        arn=resp.get("Arn"),
    )


async def update_role_custom_permission(
    custom_permissions_name: str,
    role: str,
    aws_account_id: str,
    namespace: str,
    region_name: str | None = None,
) -> UpdateRoleCustomPermissionResult:
    """Update role custom permission.

    Args:
        custom_permissions_name: Custom permissions name.
        role: Role.
        aws_account_id: Aws account id.
        namespace: Namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CustomPermissionsName"] = custom_permissions_name
    kwargs["Role"] = role
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    try:
        resp = await client.call("UpdateRoleCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update role custom permission") from exc
    return UpdateRoleCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_spice_capacity_configuration(
    aws_account_id: str,
    purchase_mode: str,
    region_name: str | None = None,
) -> UpdateSpiceCapacityConfigurationResult:
    """Update spice capacity configuration.

    Args:
        aws_account_id: Aws account id.
        purchase_mode: Purchase mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["PurchaseMode"] = purchase_mode
    try:
        resp = await client.call("UpdateSPICECapacityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update spice capacity configuration") from exc
    return UpdateSpiceCapacityConfigurationResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_template(
    aws_account_id: str,
    template_id: str,
    *,
    source_entity: dict[str, Any] | None = None,
    version_description: str | None = None,
    name: str | None = None,
    definition: dict[str, Any] | None = None,
    validation_strategy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateTemplateResult:
    """Update template.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        source_entity: Source entity.
        version_description: Version description.
        name: Name.
        definition: Definition.
        validation_strategy: Validation strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if source_entity is not None:
        kwargs["SourceEntity"] = source_entity
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if name is not None:
        kwargs["Name"] = name
    if definition is not None:
        kwargs["Definition"] = definition
    if validation_strategy is not None:
        kwargs["ValidationStrategy"] = validation_strategy
    try:
        resp = await client.call("UpdateTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update template") from exc
    return UpdateTemplateResult(
        template_id=resp.get("TemplateId"),
        arn=resp.get("Arn"),
        version_arn=resp.get("VersionArn"),
        creation_status=resp.get("CreationStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_template_alias(
    aws_account_id: str,
    template_id: str,
    alias_name: str,
    template_version_number: int,
    region_name: str | None = None,
) -> UpdateTemplateAliasResult:
    """Update template alias.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        alias_name: Alias name.
        template_version_number: Template version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    kwargs["AliasName"] = alias_name
    kwargs["TemplateVersionNumber"] = template_version_number
    try:
        resp = await client.call("UpdateTemplateAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update template alias") from exc
    return UpdateTemplateAliasResult(
        template_alias=resp.get("TemplateAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_template_permissions(
    aws_account_id: str,
    template_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateTemplatePermissionsResult:
    """Update template permissions.

    Args:
        aws_account_id: Aws account id.
        template_id: Template id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TemplateId"] = template_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateTemplatePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update template permissions") from exc
    return UpdateTemplatePermissionsResult(
        template_id=resp.get("TemplateId"),
        template_arn=resp.get("TemplateArn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_theme(
    aws_account_id: str,
    theme_id: str,
    base_theme_id: str,
    *,
    name: str | None = None,
    version_description: str | None = None,
    configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateThemeResult:
    """Update theme.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        base_theme_id: Base theme id.
        name: Name.
        version_description: Version description.
        configuration: Configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["BaseThemeId"] = base_theme_id
    if name is not None:
        kwargs["Name"] = name
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if configuration is not None:
        kwargs["Configuration"] = configuration
    try:
        resp = await client.call("UpdateTheme", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update theme") from exc
    return UpdateThemeResult(
        theme_id=resp.get("ThemeId"),
        arn=resp.get("Arn"),
        version_arn=resp.get("VersionArn"),
        creation_status=resp.get("CreationStatus"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_theme_alias(
    aws_account_id: str,
    theme_id: str,
    alias_name: str,
    theme_version_number: int,
    region_name: str | None = None,
) -> UpdateThemeAliasResult:
    """Update theme alias.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        alias_name: Alias name.
        theme_version_number: Theme version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    kwargs["AliasName"] = alias_name
    kwargs["ThemeVersionNumber"] = theme_version_number
    try:
        resp = await client.call("UpdateThemeAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update theme alias") from exc
    return UpdateThemeAliasResult(
        theme_alias=resp.get("ThemeAlias"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_theme_permissions(
    aws_account_id: str,
    theme_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateThemePermissionsResult:
    """Update theme permissions.

    Args:
        aws_account_id: Aws account id.
        theme_id: Theme id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["ThemeId"] = theme_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateThemePermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update theme permissions") from exc
    return UpdateThemePermissionsResult(
        theme_id=resp.get("ThemeId"),
        theme_arn=resp.get("ThemeArn"),
        permissions=resp.get("Permissions"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_topic(
    aws_account_id: str,
    topic_id: str,
    topic: dict[str, Any],
    *,
    custom_instructions: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateTopicResult:
    """Update topic.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        topic: Topic.
        custom_instructions: Custom instructions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["Topic"] = topic
    if custom_instructions is not None:
        kwargs["CustomInstructions"] = custom_instructions
    try:
        resp = await client.call("UpdateTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update topic") from exc
    return UpdateTopicResult(
        topic_id=resp.get("TopicId"),
        arn=resp.get("Arn"),
        refresh_arn=resp.get("RefreshArn"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_topic_permissions(
    aws_account_id: str,
    topic_id: str,
    *,
    grant_permissions: list[dict[str, Any]] | None = None,
    revoke_permissions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateTopicPermissionsResult:
    """Update topic permissions.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        grant_permissions: Grant permissions.
        revoke_permissions: Revoke permissions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    if grant_permissions is not None:
        kwargs["GrantPermissions"] = grant_permissions
    if revoke_permissions is not None:
        kwargs["RevokePermissions"] = revoke_permissions
    try:
        resp = await client.call("UpdateTopicPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update topic permissions") from exc
    return UpdateTopicPermissionsResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        permissions=resp.get("Permissions"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_topic_refresh_schedule(
    aws_account_id: str,
    topic_id: str,
    dataset_id: str,
    refresh_schedule: dict[str, Any],
    region_name: str | None = None,
) -> UpdateTopicRefreshScheduleResult:
    """Update topic refresh schedule.

    Args:
        aws_account_id: Aws account id.
        topic_id: Topic id.
        dataset_id: Dataset id.
        refresh_schedule: Refresh schedule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["TopicId"] = topic_id
    kwargs["DatasetId"] = dataset_id
    kwargs["RefreshSchedule"] = refresh_schedule
    try:
        resp = await client.call("UpdateTopicRefreshSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update topic refresh schedule") from exc
    return UpdateTopicRefreshScheduleResult(
        topic_id=resp.get("TopicId"),
        topic_arn=resp.get("TopicArn"),
        dataset_arn=resp.get("DatasetArn"),
        status=resp.get("Status"),
        request_id=resp.get("RequestId"),
    )


async def update_user(
    user_name: str,
    aws_account_id: str,
    namespace: str,
    email: str,
    role: str,
    *,
    custom_permissions_name: str | None = None,
    unapply_custom_permissions: bool | None = None,
    external_login_federation_provider_type: str | None = None,
    custom_federation_provider_url: str | None = None,
    external_login_id: str | None = None,
    region_name: str | None = None,
) -> UpdateUserResult:
    """Update user.

    Args:
        user_name: User name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        email: Email.
        role: Role.
        custom_permissions_name: Custom permissions name.
        unapply_custom_permissions: Unapply custom permissions.
        external_login_federation_provider_type: External login federation provider type.
        custom_federation_provider_url: Custom federation provider url.
        external_login_id: External login id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["Email"] = email
    kwargs["Role"] = role
    if custom_permissions_name is not None:
        kwargs["CustomPermissionsName"] = custom_permissions_name
    if unapply_custom_permissions is not None:
        kwargs["UnapplyCustomPermissions"] = unapply_custom_permissions
    if external_login_federation_provider_type is not None:
        kwargs["ExternalLoginFederationProviderType"] = external_login_federation_provider_type
    if custom_federation_provider_url is not None:
        kwargs["CustomFederationProviderUrl"] = custom_federation_provider_url
    if external_login_id is not None:
        kwargs["ExternalLoginId"] = external_login_id
    try:
        resp = await client.call("UpdateUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update user") from exc
    return UpdateUserResult(
        user=resp.get("User"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_user_custom_permission(
    user_name: str,
    aws_account_id: str,
    namespace: str,
    custom_permissions_name: str,
    region_name: str | None = None,
) -> UpdateUserCustomPermissionResult:
    """Update user custom permission.

    Args:
        user_name: User name.
        aws_account_id: Aws account id.
        namespace: Namespace.
        custom_permissions_name: Custom permissions name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["Namespace"] = namespace
    kwargs["CustomPermissionsName"] = custom_permissions_name
    try:
        resp = await client.call("UpdateUserCustomPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update user custom permission") from exc
    return UpdateUserCustomPermissionResult(
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )


async def update_vpc_connection(
    aws_account_id: str,
    vpc_connection_id: str,
    name: str,
    subnet_ids: list[str],
    security_group_ids: list[str],
    role_arn: str,
    *,
    dns_resolvers: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateVpcConnectionResult:
    """Update vpc connection.

    Args:
        aws_account_id: Aws account id.
        vpc_connection_id: Vpc connection id.
        name: Name.
        subnet_ids: Subnet ids.
        security_group_ids: Security group ids.
        role_arn: Role arn.
        dns_resolvers: Dns resolvers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("quicksight", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AwsAccountId"] = aws_account_id
    kwargs["VPCConnectionId"] = vpc_connection_id
    kwargs["Name"] = name
    kwargs["SubnetIds"] = subnet_ids
    kwargs["SecurityGroupIds"] = security_group_ids
    kwargs["RoleArn"] = role_arn
    if dns_resolvers is not None:
        kwargs["DnsResolvers"] = dns_resolvers
    try:
        resp = await client.call("UpdateVPCConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update vpc connection") from exc
    return UpdateVpcConnectionResult(
        arn=resp.get("Arn"),
        vpc_connection_id=resp.get("VPCConnectionId"),
        update_status=resp.get("UpdateStatus"),
        availability_status=resp.get("AvailabilityStatus"),
        request_id=resp.get("RequestId"),
        status=resp.get("Status"),
    )
