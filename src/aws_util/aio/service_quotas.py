"""Native async service_quotas utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.service_quotas import (
    GetAssociationForServiceQuotaTemplateResult,
    GetAutoManagementConfigurationResult,
    GetServiceQuotaIncreaseRequestFromTemplateResult,
    ListAwsDefaultServiceQuotasResult,
    ListRequestedServiceQuotaChangeHistoryByQuotaResult,
    ListRequestedServiceQuotaChangeHistoryResult,
    ListServiceQuotaIncreaseRequestsInTemplateResult,
    ListTagsForResourceResult,
    PutServiceQuotaIncreaseRequestIntoTemplateResult,
    QuotaChangeResult,
    QuotaResult,
    ServiceResult,
    _parse_quota,
    _parse_quota_change,
    _parse_service,
)

__all__ = [
    "GetAssociationForServiceQuotaTemplateResult",
    "GetAutoManagementConfigurationResult",
    "GetServiceQuotaIncreaseRequestFromTemplateResult",
    "ListAwsDefaultServiceQuotasResult",
    "ListRequestedServiceQuotaChangeHistoryByQuotaResult",
    "ListRequestedServiceQuotaChangeHistoryResult",
    "ListServiceQuotaIncreaseRequestsInTemplateResult",
    "ListTagsForResourceResult",
    "PutServiceQuotaIncreaseRequestIntoTemplateResult",
    "QuotaChangeResult",
    "QuotaResult",
    "ServiceResult",
    "associate_service_quota_template",
    "create_support_case",
    "delete_service_quota_increase_request_from_template",
    "disassociate_service_quota_template",
    "get_association_for_service_quota_template",
    "get_auto_management_configuration",
    "get_aws_default_service_quota",
    "get_requested_service_quota_change",
    "get_service_quota",
    "get_service_quota_increase_request_from_template",
    "list_aws_default_service_quotas",
    "list_requested_service_quota_change_history",
    "list_requested_service_quota_change_history_by_quota",
    "list_requested_service_quota_changes",
    "list_service_quota_increase_requests_in_template",
    "list_service_quotas",
    "list_services",
    "list_tags_for_resource",
    "put_service_quota_increase_request_into_template",
    "request_service_quota_increase",
    "start_auto_management",
    "stop_auto_management",
    "tag_resource",
    "untag_resource",
    "update_auto_management",
]


async def list_services(
    *,
    region_name: str | None = None,
) -> list[ServiceResult]:
    """List AWS services available in Service Quotas.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ServiceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call("ListServices")
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_services failed") from exc
    return [_parse_service(s) for s in resp.get("Services", [])]


async def list_service_quotas(
    service_code: str,
    *,
    region_name: str | None = None,
) -> list[QuotaResult]:
    """List quotas for a specific AWS service.

    Args:
        service_code: The service code (e.g. ``"ec2"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`QuotaResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call(
            "ListServiceQuotas",
            ServiceCode=service_code,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_service_quotas failed") from exc
    return [_parse_quota(q) for q in resp.get("Quotas", [])]


async def get_service_quota(
    service_code: str,
    quota_code: str,
    *,
    region_name: str | None = None,
) -> QuotaResult:
    """Get a specific service quota.

    Args:
        service_code: The service code.
        quota_code: The quota code.
        region_name: AWS region override.

    Returns:
        A :class:`QuotaResult` object.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call(
            "GetServiceQuota",
            ServiceCode=service_code,
            QuotaCode=quota_code,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "get_service_quota failed") from exc
    return _parse_quota(resp["Quota"])


async def get_aws_default_service_quota(
    service_code: str,
    quota_code: str,
    *,
    region_name: str | None = None,
) -> QuotaResult:
    """Get the AWS default value for a service quota.

    Args:
        service_code: The service code.
        quota_code: The quota code.
        region_name: AWS region override.

    Returns:
        A :class:`QuotaResult` object.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call(
            "GetAWSDefaultServiceQuota",
            ServiceCode=service_code,
            QuotaCode=quota_code,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "get_aws_default_service_quota failed") from exc
    return _parse_quota(resp["Quota"])


async def request_service_quota_increase(
    service_code: str,
    quota_code: str,
    desired_value: float,
    *,
    region_name: str | None = None,
) -> QuotaChangeResult:
    """Request an increase for a service quota.

    Args:
        service_code: The service code.
        quota_code: The quota code.
        desired_value: The desired quota value.
        region_name: AWS region override.

    Returns:
        A :class:`QuotaChangeResult` object.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call(
            "RequestServiceQuotaIncrease",
            ServiceCode=service_code,
            QuotaCode=quota_code,
            DesiredValue=desired_value,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "request_service_quota_increase failed") from exc
    return _parse_quota_change(resp["RequestedQuota"])


async def list_requested_service_quota_changes(
    *,
    service_code: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> list[QuotaChangeResult]:
    """List service quota change requests.

    Args:
        service_code: Optional service code filter.
        status: Optional status filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`QuotaChangeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    if service_code is not None:
        kwargs["ServiceCode"] = service_code
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = await client.call("ListRequestedServiceQuotaChangeHistory", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_requested_service_quota_changes failed") from exc
    return [_parse_quota_change(c) for c in resp.get("RequestedQuotas", [])]


async def get_requested_service_quota_change(
    request_id: str,
    *,
    region_name: str | None = None,
) -> QuotaChangeResult:
    """Get a specific service quota change request.

    Args:
        request_id: The quota change request ID.
        region_name: AWS region override.

    Returns:
        A :class:`QuotaChangeResult` object.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    try:
        resp = await client.call(
            "GetRequestedServiceQuotaChange",
            RequestId=request_id,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "get_requested_service_quota_change failed") from exc
    return _parse_quota_change(resp["RequestedQuota"])


async def associate_service_quota_template(
    region_name: str | None = None,
) -> None:
    """Associate service quota template.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("AssociateServiceQuotaTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate service quota template") from exc
    return None


async def create_support_case(
    request_id: str,
    region_name: str | None = None,
) -> None:
    """Create support case.

    Args:
        request_id: Request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RequestId"] = request_id
    try:
        await client.call("CreateSupportCase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create support case") from exc
    return None


async def delete_service_quota_increase_request_from_template(
    service_code: str,
    quota_code: str,
    aws_region: str,
    region_name: str | None = None,
) -> None:
    """Delete service quota increase request from template.

    Args:
        service_code: Service code.
        quota_code: Quota code.
        aws_region: Aws region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceCode"] = service_code
    kwargs["QuotaCode"] = quota_code
    kwargs["AwsRegion"] = aws_region
    try:
        await client.call("DeleteServiceQuotaIncreaseRequestFromTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to delete service quota increase request from template"
        ) from exc
    return None


async def disassociate_service_quota_template(
    region_name: str | None = None,
) -> None:
    """Disassociate service quota template.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisassociateServiceQuotaTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate service quota template") from exc
    return None


async def get_association_for_service_quota_template(
    region_name: str | None = None,
) -> GetAssociationForServiceQuotaTemplateResult:
    """Get association for service quota template.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAssociationForServiceQuotaTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get association for service quota template") from exc
    return GetAssociationForServiceQuotaTemplateResult(
        service_quota_template_association_status=resp.get("ServiceQuotaTemplateAssociationStatus"),
    )


async def get_auto_management_configuration(
    region_name: str | None = None,
) -> GetAutoManagementConfigurationResult:
    """Get auto management configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAutoManagementConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get auto management configuration") from exc
    return GetAutoManagementConfigurationResult(
        opt_in_level=resp.get("OptInLevel"),
        opt_in_type=resp.get("OptInType"),
        notification_arn=resp.get("NotificationArn"),
        opt_in_status=resp.get("OptInStatus"),
        exclusion_list=resp.get("ExclusionList"),
    )


async def get_service_quota_increase_request_from_template(
    service_code: str,
    quota_code: str,
    aws_region: str,
    region_name: str | None = None,
) -> GetServiceQuotaIncreaseRequestFromTemplateResult:
    """Get service quota increase request from template.

    Args:
        service_code: Service code.
        quota_code: Quota code.
        aws_region: Aws region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceCode"] = service_code
    kwargs["QuotaCode"] = quota_code
    kwargs["AwsRegion"] = aws_region
    try:
        resp = await client.call("GetServiceQuotaIncreaseRequestFromTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to get service quota increase request from template"
        ) from exc
    return GetServiceQuotaIncreaseRequestFromTemplateResult(
        service_quota_increase_request_in_template=resp.get(
            "ServiceQuotaIncreaseRequestInTemplate"
        ),
    )


async def list_aws_default_service_quotas(
    service_code: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAwsDefaultServiceQuotasResult:
    """List aws default service quotas.

    Args:
        service_code: Service code.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceCode"] = service_code
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAWSDefaultServiceQuotas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list aws default service quotas") from exc
    return ListAwsDefaultServiceQuotasResult(
        next_token=resp.get("NextToken"),
        quotas=resp.get("Quotas"),
    )


async def list_requested_service_quota_change_history(
    *,
    service_code: str | None = None,
    status: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    quota_requested_at_level: str | None = None,
    region_name: str | None = None,
) -> ListRequestedServiceQuotaChangeHistoryResult:
    """List requested service quota change history.

    Args:
        service_code: Service code.
        status: Status.
        next_token: Next token.
        max_results: Max results.
        quota_requested_at_level: Quota requested at level.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    if service_code is not None:
        kwargs["ServiceCode"] = service_code
    if status is not None:
        kwargs["Status"] = status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if quota_requested_at_level is not None:
        kwargs["QuotaRequestedAtLevel"] = quota_requested_at_level
    try:
        resp = await client.call("ListRequestedServiceQuotaChangeHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list requested service quota change history") from exc
    return ListRequestedServiceQuotaChangeHistoryResult(
        next_token=resp.get("NextToken"),
        requested_quotas=resp.get("RequestedQuotas"),
    )


async def list_requested_service_quota_change_history_by_quota(
    service_code: str,
    quota_code: str,
    *,
    status: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    quota_requested_at_level: str | None = None,
    region_name: str | None = None,
) -> ListRequestedServiceQuotaChangeHistoryByQuotaResult:
    """List requested service quota change history by quota.

    Args:
        service_code: Service code.
        quota_code: Quota code.
        status: Status.
        next_token: Next token.
        max_results: Max results.
        quota_requested_at_level: Quota requested at level.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceCode"] = service_code
    kwargs["QuotaCode"] = quota_code
    if status is not None:
        kwargs["Status"] = status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if quota_requested_at_level is not None:
        kwargs["QuotaRequestedAtLevel"] = quota_requested_at_level
    try:
        resp = await client.call("ListRequestedServiceQuotaChangeHistoryByQuota", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list requested service quota change history by quota"
        ) from exc
    return ListRequestedServiceQuotaChangeHistoryByQuotaResult(
        next_token=resp.get("NextToken"),
        requested_quotas=resp.get("RequestedQuotas"),
    )


async def list_service_quota_increase_requests_in_template(
    *,
    service_code: str | None = None,
    aws_region: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListServiceQuotaIncreaseRequestsInTemplateResult:
    """List service quota increase requests in template.

    Args:
        service_code: Service code.
        aws_region: Aws region.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    if service_code is not None:
        kwargs["ServiceCode"] = service_code
    if aws_region is not None:
        kwargs["AwsRegion"] = aws_region
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListServiceQuotaIncreaseRequestsInTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list service quota increase requests in template"
        ) from exc
    return ListServiceQuotaIncreaseRequestsInTemplateResult(
        service_quota_increase_request_in_template_list=resp.get(
            "ServiceQuotaIncreaseRequestInTemplateList"
        ),
        next_token=resp.get("NextToken"),
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
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def put_service_quota_increase_request_into_template(
    quota_code: str,
    service_code: str,
    aws_region: str,
    desired_value: float,
    region_name: str | None = None,
) -> PutServiceQuotaIncreaseRequestIntoTemplateResult:
    """Put service quota increase request into template.

    Args:
        quota_code: Quota code.
        service_code: Service code.
        aws_region: Aws region.
        desired_value: Desired value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QuotaCode"] = quota_code
    kwargs["ServiceCode"] = service_code
    kwargs["AwsRegion"] = aws_region
    kwargs["DesiredValue"] = desired_value
    try:
        resp = await client.call("PutServiceQuotaIncreaseRequestIntoTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to put service quota increase request into template"
        ) from exc
    return PutServiceQuotaIncreaseRequestIntoTemplateResult(
        service_quota_increase_request_in_template=resp.get(
            "ServiceQuotaIncreaseRequestInTemplate"
        ),
    )


async def start_auto_management(
    opt_in_level: str,
    opt_in_type: str,
    *,
    notification_arn: str | None = None,
    exclusion_list: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Start auto management.

    Args:
        opt_in_level: Opt in level.
        opt_in_type: Opt in type.
        notification_arn: Notification arn.
        exclusion_list: Exclusion list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OptInLevel"] = opt_in_level
    kwargs["OptInType"] = opt_in_type
    if notification_arn is not None:
        kwargs["NotificationArn"] = notification_arn
    if exclusion_list is not None:
        kwargs["ExclusionList"] = exclusion_list
    try:
        await client.call("StartAutoManagement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start auto management") from exc
    return None


async def stop_auto_management(
    region_name: str | None = None,
) -> None:
    """Stop auto management.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("StopAutoManagement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop auto management") from exc
    return None


async def tag_resource(
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
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
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
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_auto_management(
    *,
    opt_in_type: str | None = None,
    notification_arn: str | None = None,
    exclusion_list: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update auto management.

    Args:
        opt_in_type: Opt in type.
        notification_arn: Notification arn.
        exclusion_list: Exclusion list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("service-quotas", region_name)
    kwargs: dict[str, Any] = {}
    if opt_in_type is not None:
        kwargs["OptInType"] = opt_in_type
    if notification_arn is not None:
        kwargs["NotificationArn"] = notification_arn
    if exclusion_list is not None:
        kwargs["ExclusionList"] = exclusion_list
    try:
        await client.call("UpdateAutoManagement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update auto management") from exc
    return None
