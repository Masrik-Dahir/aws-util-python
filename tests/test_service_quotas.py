"""Tests for aws_util.service_quotas module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.service_quotas as mod
from aws_util.service_quotas import (
    QuotaChangeResult,
    QuotaResult,
    ServiceResult,
    _parse_quota,
    _parse_quota_change,
    _parse_service,
    get_aws_default_service_quota,
    get_requested_service_quota_change,
    get_service_quota,
    list_requested_service_quota_changes,
    list_service_quotas,
    list_services,
    request_service_quota_increase,
    associate_service_quota_template,
    create_support_case,
    delete_service_quota_increase_request_from_template,
    disassociate_service_quota_template,
    get_association_for_service_quota_template,
    get_auto_management_configuration,
    get_service_quota_increase_request_from_template,
    list_aws_default_service_quotas,
    list_requested_service_quota_change_history,
    list_requested_service_quota_change_history_by_quota,
    list_service_quota_increase_requests_in_template,
    list_tags_for_resource,
    put_service_quota_increase_request_into_template,
    start_auto_management,
    stop_auto_management,
    tag_resource,
    untag_resource,
    update_auto_management,
)

REGION = "us-east-1"

_SVC = {"ServiceCode": "ec2", "ServiceName": "Amazon EC2", "extra": "x"}
_QUOTA = {
    "ServiceCode": "ec2", "ServiceName": "Amazon EC2",
    "QuotaCode": "L-1234", "QuotaName": "Instances",
    "Value": 100.0, "Unit": "None",
    "Adjustable": True, "GlobalQuota": False,
    "extraQ": "y",
}
_CHANGE = {
    "Id": "ch-1", "ServiceCode": "ec2", "QuotaCode": "L-1234",
    "Status": "PENDING", "DesiredValue": 200.0,
    "CaseId": "case-1", "Created": "2025-01-01", "LastUpdated": "2025-01-02",
    "extraC": "z",
}


def _ce(code: str = "ServiceException", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_service_result_model():
    r = ServiceResult(service_code="ec2", service_name="Amazon EC2")
    assert r.service_code == "ec2"


def test_quota_result_model():
    r = QuotaResult(service_code="ec2", quota_code="L-1")
    assert r.adjustable is False
    assert r.global_quota is False


def test_quota_change_result_model():
    r = QuotaChangeResult(id="ch-1")
    assert r.status is None


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def test_parse_service():
    r = _parse_service(_SVC)
    assert r.service_code == "ec2"
    assert "extra" in r.extra


def test_parse_quota():
    r = _parse_quota(_QUOTA)
    assert r.quota_code == "L-1234"
    assert r.adjustable is True
    assert "extraQ" in r.extra


def test_parse_quota_change():
    r = _parse_quota_change(_CHANGE)
    assert r.id == "ch-1"
    assert r.created == "2025-01-01"
    assert r.last_updated == "2025-01-02"
    assert "extraC" in r.extra


def test_parse_quota_change_no_dates():
    data = {**_CHANGE, "Created": None, "LastUpdated": None}
    r = _parse_quota_change(data)
    assert r.created is None
    assert r.last_updated is None


# ---------------------------------------------------------------------------
# list_services
# ---------------------------------------------------------------------------


def test_list_services_success(monkeypatch):
    client = MagicMock()
    client.list_services.return_value = {"Services": [_SVC]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_services(region_name=REGION)
    assert len(r) == 1


def test_list_services_error(monkeypatch):
    client = MagicMock()
    client.list_services.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_services failed"):
        list_services(region_name=REGION)


# ---------------------------------------------------------------------------
# list_service_quotas
# ---------------------------------------------------------------------------


def test_list_service_quotas_success(monkeypatch):
    client = MagicMock()
    client.list_service_quotas.return_value = {"Quotas": [_QUOTA]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_service_quotas("ec2", region_name=REGION)
    assert len(r) == 1


def test_list_service_quotas_error(monkeypatch):
    client = MagicMock()
    client.list_service_quotas.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_service_quotas failed"):
        list_service_quotas("ec2", region_name=REGION)


# ---------------------------------------------------------------------------
# get_service_quota
# ---------------------------------------------------------------------------


def test_get_service_quota_success(monkeypatch):
    client = MagicMock()
    client.get_service_quota.return_value = {"Quota": _QUOTA}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_service_quota("ec2", "L-1234", region_name=REGION)
    assert r.quota_code == "L-1234"


def test_get_service_quota_error(monkeypatch):
    client = MagicMock()
    client.get_service_quota.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_service_quota failed"):
        get_service_quota("ec2", "L-1234", region_name=REGION)


# ---------------------------------------------------------------------------
# get_aws_default_service_quota
# ---------------------------------------------------------------------------


def test_get_aws_default_service_quota_success(monkeypatch):
    client = MagicMock()
    client.get_aws_default_service_quota.return_value = {"Quota": _QUOTA}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_aws_default_service_quota("ec2", "L-1234", region_name=REGION)
    assert r.value == 100.0


def test_get_aws_default_service_quota_error(monkeypatch):
    client = MagicMock()
    client.get_aws_default_service_quota.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_aws_default_service_quota failed"):
        get_aws_default_service_quota("ec2", "L-1234", region_name=REGION)


# ---------------------------------------------------------------------------
# request_service_quota_increase
# ---------------------------------------------------------------------------


def test_request_service_quota_increase_success(monkeypatch):
    client = MagicMock()
    client.request_service_quota_increase.return_value = {"RequestedQuota": _CHANGE}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = request_service_quota_increase("ec2", "L-1234", 200.0, region_name=REGION)
    assert r.id == "ch-1"


def test_request_service_quota_increase_error(monkeypatch):
    client = MagicMock()
    client.request_service_quota_increase.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="request_service_quota_increase failed"):
        request_service_quota_increase("ec2", "L-1234", 200.0, region_name=REGION)


# ---------------------------------------------------------------------------
# list_requested_service_quota_changes
# ---------------------------------------------------------------------------


def test_list_requested_changes_success(monkeypatch):
    client = MagicMock()
    client.list_requested_service_quota_changes.return_value = {"RequestedQuotas": [_CHANGE]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_requested_service_quota_changes(region_name=REGION)
    assert len(r) == 1


def test_list_requested_changes_with_filters(monkeypatch):
    client = MagicMock()
    client.list_requested_service_quota_changes.return_value = {"RequestedQuotas": []}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    list_requested_service_quota_changes(
        service_code="ec2", status="PENDING", region_name=REGION
    )
    kw = client.list_requested_service_quota_changes.call_args[1]
    assert kw["ServiceCode"] == "ec2"
    assert kw["Status"] == "PENDING"


def test_list_requested_changes_error(monkeypatch):
    client = MagicMock()
    client.list_requested_service_quota_changes.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_requested_service_quota_changes failed"):
        list_requested_service_quota_changes(region_name=REGION)


# ---------------------------------------------------------------------------
# get_requested_service_quota_change
# ---------------------------------------------------------------------------


def test_get_requested_change_success(monkeypatch):
    client = MagicMock()
    client.get_requested_service_quota_change.return_value = {"RequestedQuota": _CHANGE}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_requested_service_quota_change("ch-1", region_name=REGION)
    assert r.id == "ch-1"


def test_get_requested_change_error(monkeypatch):
    client = MagicMock()
    client.get_requested_service_quota_change.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_requested_service_quota_change failed"):
        get_requested_service_quota_change("ch-1", region_name=REGION)


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_associate_service_quota_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_service_quota_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    associate_service_quota_template(region_name=REGION)
    mock_client.associate_service_quota_template.assert_called_once()


def test_associate_service_quota_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_service_quota_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_service_quota_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate service quota template"):
        associate_service_quota_template(region_name=REGION)


def test_create_support_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_support_case.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    create_support_case("test-request_id", region_name=REGION)
    mock_client.create_support_case.assert_called_once()


def test_create_support_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_support_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_support_case",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create support case"):
        create_support_case("test-request_id", region_name=REGION)


def test_delete_service_quota_increase_request_from_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_quota_increase_request_from_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    delete_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", region_name=REGION)
    mock_client.delete_service_quota_increase_request_from_template.assert_called_once()


def test_delete_service_quota_increase_request_from_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_quota_increase_request_from_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_quota_increase_request_from_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service quota increase request from template"):
        delete_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", region_name=REGION)


def test_disassociate_service_quota_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_service_quota_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    disassociate_service_quota_template(region_name=REGION)
    mock_client.disassociate_service_quota_template.assert_called_once()


def test_disassociate_service_quota_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_service_quota_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_service_quota_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate service quota template"):
        disassociate_service_quota_template(region_name=REGION)


def test_get_association_for_service_quota_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_association_for_service_quota_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    get_association_for_service_quota_template(region_name=REGION)
    mock_client.get_association_for_service_quota_template.assert_called_once()


def test_get_association_for_service_quota_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_association_for_service_quota_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_association_for_service_quota_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get association for service quota template"):
        get_association_for_service_quota_template(region_name=REGION)


def test_get_auto_management_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auto_management_configuration.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    get_auto_management_configuration(region_name=REGION)
    mock_client.get_auto_management_configuration.assert_called_once()


def test_get_auto_management_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auto_management_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_auto_management_configuration",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get auto management configuration"):
        get_auto_management_configuration(region_name=REGION)


def test_get_service_quota_increase_request_from_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_quota_increase_request_from_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    get_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", region_name=REGION)
    mock_client.get_service_quota_increase_request_from_template.assert_called_once()


def test_get_service_quota_increase_request_from_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_quota_increase_request_from_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_quota_increase_request_from_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service quota increase request from template"):
        get_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", region_name=REGION)


def test_list_aws_default_service_quotas(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aws_default_service_quotas.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_aws_default_service_quotas("test-service_code", region_name=REGION)
    mock_client.list_aws_default_service_quotas.assert_called_once()


def test_list_aws_default_service_quotas_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aws_default_service_quotas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aws_default_service_quotas",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aws default service quotas"):
        list_aws_default_service_quotas("test-service_code", region_name=REGION)


def test_list_requested_service_quota_change_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_requested_service_quota_change_history(region_name=REGION)
    mock_client.list_requested_service_quota_change_history.assert_called_once()


def test_list_requested_service_quota_change_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_requested_service_quota_change_history",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list requested service quota change history"):
        list_requested_service_quota_change_history(region_name=REGION)


def test_list_requested_service_quota_change_history_by_quota(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history_by_quota.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", region_name=REGION)
    mock_client.list_requested_service_quota_change_history_by_quota.assert_called_once()


def test_list_requested_service_quota_change_history_by_quota_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history_by_quota.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_requested_service_quota_change_history_by_quota",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list requested service quota change history by quota"):
        list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", region_name=REGION)


def test_list_service_quota_increase_requests_in_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_quota_increase_requests_in_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_service_quota_increase_requests_in_template(region_name=REGION)
    mock_client.list_service_quota_increase_requests_in_template.assert_called_once()


def test_list_service_quota_increase_requests_in_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_quota_increase_requests_in_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_quota_increase_requests_in_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service quota increase requests in template"):
        list_service_quota_increase_requests_in_template(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_put_service_quota_increase_request_into_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_service_quota_increase_request_into_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    put_service_quota_increase_request_into_template("test-quota_code", "test-service_code", "test-aws_region", "test-desired_value", region_name=REGION)
    mock_client.put_service_quota_increase_request_into_template.assert_called_once()


def test_put_service_quota_increase_request_into_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_service_quota_increase_request_into_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_service_quota_increase_request_into_template",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put service quota increase request into template"):
        put_service_quota_increase_request_into_template("test-quota_code", "test-service_code", "test-aws_region", "test-desired_value", region_name=REGION)


def test_start_auto_management(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_auto_management.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    start_auto_management("test-opt_in_level", "test-opt_in_type", region_name=REGION)
    mock_client.start_auto_management.assert_called_once()


def test_start_auto_management_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_auto_management.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_auto_management",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start auto management"):
        start_auto_management("test-opt_in_level", "test-opt_in_type", region_name=REGION)


def test_stop_auto_management(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_auto_management.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    stop_auto_management(region_name=REGION)
    mock_client.stop_auto_management.assert_called_once()


def test_stop_auto_management_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_auto_management.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_auto_management",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop auto management"):
        stop_auto_management(region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_auto_management(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_auto_management.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    update_auto_management(region_name=REGION)
    mock_client.update_auto_management.assert_called_once()


def test_update_auto_management_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_auto_management.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_auto_management",
    )
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update auto management"):
        update_auto_management(region_name=REGION)


def test_list_requested_service_quota_changes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import list_requested_service_quota_changes
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_changes.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_requested_service_quota_changes(service_code="test-service_code", status="test-status", region_name="us-east-1")
    mock_client.list_requested_service_quota_changes.assert_called_once()

def test_list_aws_default_service_quotas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import list_aws_default_service_quotas
    mock_client = MagicMock()
    mock_client.list_aws_default_service_quotas.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_aws_default_service_quotas("test-service_code", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_aws_default_service_quotas.assert_called_once()

def test_list_requested_service_quota_change_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import list_requested_service_quota_change_history
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_requested_service_quota_change_history(service_code="test-service_code", status="test-status", next_token="test-next_token", max_results=1, quota_requested_at_level="test-quota_requested_at_level", region_name="us-east-1")
    mock_client.list_requested_service_quota_change_history.assert_called_once()

def test_list_requested_service_quota_change_history_by_quota_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import list_requested_service_quota_change_history_by_quota
    mock_client = MagicMock()
    mock_client.list_requested_service_quota_change_history_by_quota.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", status="test-status", next_token="test-next_token", max_results=1, quota_requested_at_level="test-quota_requested_at_level", region_name="us-east-1")
    mock_client.list_requested_service_quota_change_history_by_quota.assert_called_once()

def test_list_service_quota_increase_requests_in_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import list_service_quota_increase_requests_in_template
    mock_client = MagicMock()
    mock_client.list_service_quota_increase_requests_in_template.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    list_service_quota_increase_requests_in_template(service_code="test-service_code", aws_region="test-aws_region", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_service_quota_increase_requests_in_template.assert_called_once()

def test_start_auto_management_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import start_auto_management
    mock_client = MagicMock()
    mock_client.start_auto_management.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    start_auto_management("test-opt_in_level", "test-opt_in_type", notification_arn="test-notification_arn", exclusion_list="test-exclusion_list", region_name="us-east-1")
    mock_client.start_auto_management.assert_called_once()

def test_update_auto_management_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.service_quotas import update_auto_management
    mock_client = MagicMock()
    mock_client.update_auto_management.return_value = {}
    monkeypatch.setattr("aws_util.service_quotas.get_client", lambda *a, **kw: mock_client)
    update_auto_management(opt_in_type="test-opt_in_type", notification_arn="test-notification_arn", exclusion_list="test-exclusion_list", region_name="us-east-1")
    mock_client.update_auto_management.assert_called_once()
