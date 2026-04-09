"""Tests for aws_util.inspector -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.inspector import (
    AccountStatusResult,
    ConfigurationResult,
    CoverageResult,
    FindingResult,
    MemberResult,
    ReportStatusResult,
    SbomExportResult,
    _parse_account_status,
    _parse_coverage,
    _parse_finding,
    _parse_member,
    batch_get_account_status,
    create_findings_report,
    create_sbom_export,
    disable,
    enable,
    get_configuration,
    get_findings_report_status,
    get_member,
    get_sbom_export,
    list_coverage,
    list_finding_aggregations,
    list_findings,
    list_members,
    update_configuration,
    associate_member,
    batch_associate_code_security_scan_configuration,
    batch_disassociate_code_security_scan_configuration,
    batch_get_code_snippet,
    batch_get_finding_details,
    batch_get_free_trial_info,
    batch_get_member_ec2_deep_inspection_status,
    batch_update_member_ec2_deep_inspection_status,
    cancel_findings_report,
    cancel_sbom_export,
    create_cis_scan_configuration,
    create_code_security_integration,
    create_code_security_scan_configuration,
    create_filter,
    delete_cis_scan_configuration,
    delete_code_security_integration,
    delete_code_security_scan_configuration,
    delete_filter,
    describe_organization_configuration,
    disable_delegated_admin_account,
    disassociate_member,
    enable_delegated_admin_account,
    get_cis_scan_report,
    get_cis_scan_result_details,
    get_clusters_for_image,
    get_code_security_integration,
    get_code_security_scan,
    get_code_security_scan_configuration,
    get_delegated_admin_account,
    get_ec2_deep_inspection_configuration,
    get_encryption_key,
    list_account_permissions,
    list_cis_scan_configurations,
    list_cis_scan_results_aggregated_by_checks,
    list_cis_scan_results_aggregated_by_target_resource,
    list_cis_scans,
    list_code_security_integrations,
    list_code_security_scan_configuration_associations,
    list_code_security_scan_configurations,
    list_coverage_statistics,
    list_delegated_admin_accounts,
    list_filters,
    list_tags_for_resource,
    list_usage_totals,
    reset_encryption_key,
    search_vulnerabilities,
    send_cis_session_health,
    send_cis_session_telemetry,
    start_cis_session,
    start_code_security_scan,
    stop_cis_session,
    tag_resource,
    untag_resource,
    update_cis_scan_configuration,
    update_code_security_integration,
    update_code_security_scan_configuration,
    update_ec2_deep_inspection_configuration,
    update_encryption_key,
    update_filter,
    update_org_ec2_deep_inspection_configuration,
    update_organization_configuration,
)


def _client_error(code: str = "ValidationException") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": "boom"}}, "Op"
    )


# ---------------------------------------------------------------------------
# Parser unit tests
# ---------------------------------------------------------------------------


def test_parse_account_status(monkeypatch):
    a = _parse_account_status({
        "accountId": "111",
        "state": {"status": "ENABLED"},
        "resourceState": {"ec2": {}},
        "extra_field": 1,
    })
    assert isinstance(a, AccountStatusResult)
    assert a.account_id == "111"
    assert a.extra == {"extra_field": 1}


def test_parse_finding():
    f = _parse_finding({
        "findingArn": "arn:f",
        "awsAccountId": "111",
        "type": "VULNERABILITY",
        "severity": "HIGH",
        "status": "ACTIVE",
        "title": "t",
        "description": "d",
        "extra": 1,
    })
    assert isinstance(f, FindingResult)
    assert f.finding_arn == "arn:f"
    assert f.extra == {"extra": 1}


def test_parse_coverage():
    c = _parse_coverage({
        "resourceId": "r1",
        "resourceType": "EC2",
        "accountId": "111",
        "scanStatus": {"reason": "ok"},
        "extra": True,
    })
    assert isinstance(c, CoverageResult)
    assert c.resource_id == "r1"
    assert c.extra == {"extra": True}


def test_parse_member():
    m = _parse_member({
        "accountId": "111",
        "relationshipStatus": "ASSOCIATED",
        "delegatedAdminAccountId": "222",
        "updatedAt": "2024-01-01",
        "extra": "x",
    })
    assert isinstance(m, MemberResult)
    assert m.updated_at == "2024-01-01"
    assert m.extra == {"extra": "x"}


def test_parse_member_minimal():
    m = _parse_member({})
    assert m.updated_at is None


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_enable(mock_gc):
    client = MagicMock()
    client.enable.return_value = {"accounts": [{"accountId": "111"}], "failedAccounts": []}
    mock_gc.return_value = client
    result = enable(["EC2"])
    assert len(result["accounts"]) == 1


@patch("aws_util.inspector.get_client")
def test_enable_error(mock_gc):
    client = MagicMock()
    client.enable.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="enable failed"):
        enable(["EC2"])


@patch("aws_util.inspector.get_client")
def test_disable(mock_gc):
    client = MagicMock()
    client.disable.return_value = {"accounts": [], "failedAccounts": []}
    mock_gc.return_value = client
    result = disable(["EC2"])
    assert result["failedAccounts"] == []


@patch("aws_util.inspector.get_client")
def test_disable_with_account_ids(mock_gc):
    client = MagicMock()
    client.disable.return_value = {"accounts": [], "failedAccounts": []}
    mock_gc.return_value = client
    disable(["EC2"], account_ids=["111"])
    call_kwargs = client.disable.call_args[1]
    assert call_kwargs["accountIds"] == ["111"]


@patch("aws_util.inspector.get_client")
def test_disable_error(mock_gc):
    client = MagicMock()
    client.disable.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        disable(["EC2"])


# ---------------------------------------------------------------------------
# get_configuration / update_configuration
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_get_configuration(mock_gc):
    client = MagicMock()
    client.get_configuration.return_value = {
        "ecrConfiguration": {"pullDateRescanDuration": "180"},
        "ec2Configuration": {"scanMode": "EC2_SSM_AGENT_BASED"},
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_configuration()
    assert isinstance(result, ConfigurationResult)
    assert "pullDateRescanDuration" in result.ecr_configuration


@patch("aws_util.inspector.get_client")
def test_get_configuration_error(mock_gc):
    client = MagicMock()
    client.get_configuration.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_configuration()


@patch("aws_util.inspector.get_client")
def test_update_configuration(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    update_configuration(
        ecr_configuration={"a": "b"},
        ec2_configuration={"c": "d"},
    )
    call_kwargs = client.update_configuration.call_args[1]
    assert call_kwargs["ecrConfiguration"] == {"a": "b"}
    assert call_kwargs["ec2Configuration"] == {"c": "d"}


@patch("aws_util.inspector.get_client")
def test_update_configuration_error(mock_gc):
    client = MagicMock()
    client.update_configuration.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_configuration()


# ---------------------------------------------------------------------------
# batch_get_account_status
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_batch_get_account_status(mock_gc):
    client = MagicMock()
    client.batch_get_account_status.return_value = {
        "accounts": [{"accountId": "111", "state": {}, "resourceState": {}}],
    }
    mock_gc.return_value = client
    result = batch_get_account_status(["111"])
    assert len(result) == 1
    assert isinstance(result[0], AccountStatusResult)


@patch("aws_util.inspector.get_client")
def test_batch_get_account_status_error(mock_gc):
    client = MagicMock()
    client.batch_get_account_status.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        batch_get_account_status(["111"])


# ---------------------------------------------------------------------------
# list_findings
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_list_findings(mock_gc):
    client = MagicMock()
    client.list_findings.return_value = {
        "findings": [{"findingArn": "arn:f"}],
    }
    mock_gc.return_value = client
    result = list_findings()
    assert len(result) == 1
    assert isinstance(result[0], FindingResult)


@patch("aws_util.inspector.get_client")
def test_list_findings_pagination(mock_gc):
    client = MagicMock()
    client.list_findings.side_effect = [
        {"findings": [{"findingArn": "a1"}], "nextToken": "tok"},
        {"findings": [{"findingArn": "a2"}]},
    ]
    mock_gc.return_value = client
    result = list_findings()
    assert len(result) == 2


@patch("aws_util.inspector.get_client")
def test_list_findings_error(mock_gc):
    client = MagicMock()
    client.list_findings.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_findings()


# ---------------------------------------------------------------------------
# list_finding_aggregations
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_list_finding_aggregations(mock_gc):
    client = MagicMock()
    client.list_finding_aggregations.return_value = {
        "responses": [{"key": "val"}],
    }
    mock_gc.return_value = client
    result = list_finding_aggregations("FINDING_TYPE")
    assert len(result) == 1


@patch("aws_util.inspector.get_client")
def test_list_finding_aggregations_pagination(mock_gc):
    client = MagicMock()
    client.list_finding_aggregations.side_effect = [
        {"responses": [{"a": 1}], "nextToken": "tok"},
        {"responses": [{"a": 2}]},
    ]
    mock_gc.return_value = client
    result = list_finding_aggregations("FINDING_TYPE")
    assert len(result) == 2


@patch("aws_util.inspector.get_client")
def test_list_finding_aggregations_error(mock_gc):
    client = MagicMock()
    client.list_finding_aggregations.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_finding_aggregations("FINDING_TYPE")


# ---------------------------------------------------------------------------
# get_findings_report_status / create_findings_report
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_get_findings_report_status(mock_gc):
    client = MagicMock()
    client.get_findings_report_status.return_value = {
        "reportId": "r1",
        "status": "COMPLETE",
        "errorCode": "",
        "errorMessage": "",
        "destination": {"bucketName": "b"},
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_findings_report_status("r1")
    assert isinstance(result, ReportStatusResult)
    assert result.report_id == "r1"


@patch("aws_util.inspector.get_client")
def test_get_findings_report_status_error(mock_gc):
    client = MagicMock()
    client.get_findings_report_status.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_findings_report_status("r1")


@patch("aws_util.inspector.get_client")
def test_create_findings_report(mock_gc):
    client = MagicMock()
    client.create_findings_report.return_value = {"reportId": "r1"}
    mock_gc.return_value = client
    result = create_findings_report(
        report_format="JSON",
        s3_destination={"bucketName": "b", "kmsKeyArn": "k"},
    )
    assert result == "r1"


@patch("aws_util.inspector.get_client")
def test_create_findings_report_with_filter(mock_gc):
    client = MagicMock()
    client.create_findings_report.return_value = {"reportId": "r1"}
    mock_gc.return_value = client
    create_findings_report(
        report_format="CSV",
        s3_destination={"bucketName": "b"},
        filter_criteria={"f": "v"},
    )
    call_kwargs = client.create_findings_report.call_args[1]
    assert "filterCriteria" in call_kwargs


@patch("aws_util.inspector.get_client")
def test_create_findings_report_error(mock_gc):
    client = MagicMock()
    client.create_findings_report.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_findings_report(
            report_format="JSON",
            s3_destination={"bucketName": "b"},
        )


# ---------------------------------------------------------------------------
# get_sbom_export / create_sbom_export
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_get_sbom_export(mock_gc):
    client = MagicMock()
    client.get_sbom_export.return_value = {
        "reportId": "r1",
        "status": "COMPLETE",
        "errorCode": "",
        "errorMessage": "",
        "s3Destination": {"bucketName": "b"},
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_sbom_export("r1")
    assert isinstance(result, SbomExportResult)
    assert result.report_id == "r1"


@patch("aws_util.inspector.get_client")
def test_get_sbom_export_error(mock_gc):
    client = MagicMock()
    client.get_sbom_export.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_sbom_export("r1")


@patch("aws_util.inspector.get_client")
def test_create_sbom_export(mock_gc):
    client = MagicMock()
    client.create_sbom_export.return_value = {"reportId": "r1"}
    mock_gc.return_value = client
    result = create_sbom_export(
        report_format="CYCLONEDX_1_4",
        s3_destination={"bucketName": "b"},
    )
    assert result == "r1"


@patch("aws_util.inspector.get_client")
def test_create_sbom_export_with_filter(mock_gc):
    client = MagicMock()
    client.create_sbom_export.return_value = {"reportId": "r1"}
    mock_gc.return_value = client
    create_sbom_export(
        report_format="SPDX_2_3",
        s3_destination={"bucketName": "b"},
        resource_filter_criteria={"f": "v"},
    )
    call_kwargs = client.create_sbom_export.call_args[1]
    assert "resourceFilterCriteria" in call_kwargs


@patch("aws_util.inspector.get_client")
def test_create_sbom_export_error(mock_gc):
    client = MagicMock()
    client.create_sbom_export.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_sbom_export(
            report_format="CYCLONEDX_1_4",
            s3_destination={"bucketName": "b"},
        )


# ---------------------------------------------------------------------------
# list_coverage
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_list_coverage(mock_gc):
    client = MagicMock()
    client.list_coverage.return_value = {
        "coveredResources": [{"resourceId": "r1", "resourceType": "EC2"}],
    }
    mock_gc.return_value = client
    result = list_coverage()
    assert len(result) == 1
    assert isinstance(result[0], CoverageResult)


@patch("aws_util.inspector.get_client")
def test_list_coverage_pagination(mock_gc):
    client = MagicMock()
    client.list_coverage.side_effect = [
        {"coveredResources": [{"resourceId": "r1"}], "nextToken": "tok"},
        {"coveredResources": [{"resourceId": "r2"}]},
    ]
    mock_gc.return_value = client
    result = list_coverage()
    assert len(result) == 2


@patch("aws_util.inspector.get_client")
def test_list_coverage_error(mock_gc):
    client = MagicMock()
    client.list_coverage.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_coverage()


# ---------------------------------------------------------------------------
# list_members / get_member
# ---------------------------------------------------------------------------


@patch("aws_util.inspector.get_client")
def test_list_members(mock_gc):
    client = MagicMock()
    client.list_members.return_value = {
        "members": [{"accountId": "111", "relationshipStatus": "ASSOCIATED"}],
    }
    mock_gc.return_value = client
    result = list_members()
    assert len(result) == 1


@patch("aws_util.inspector.get_client")
def test_list_members_pagination(mock_gc):
    client = MagicMock()
    client.list_members.side_effect = [
        {"members": [{"accountId": "1"}], "nextToken": "tok"},
        {"members": [{"accountId": "2"}]},
    ]
    mock_gc.return_value = client
    result = list_members()
    assert len(result) == 2


@patch("aws_util.inspector.get_client")
def test_list_members_error(mock_gc):
    client = MagicMock()
    client.list_members.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_members()


@patch("aws_util.inspector.get_client")
def test_get_member(mock_gc):
    client = MagicMock()
    client.get_member.return_value = {
        "member": {"accountId": "111", "relationshipStatus": "ASSOCIATED"},
    }
    mock_gc.return_value = client
    result = get_member("111")
    assert isinstance(result, MemberResult)
    assert result.account_id == "111"


@patch("aws_util.inspector.get_client")
def test_get_member_error(mock_gc):
    client = MagicMock()
    client.get_member.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_member("111")


REGION = "us-east-1"


@patch("aws_util.inspector.get_client")
def test_associate_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_member.return_value = {}
    associate_member("test-account_id", region_name=REGION)
    mock_client.associate_member.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_associate_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_member",
    )
    with pytest.raises(RuntimeError, match="Failed to associate member"):
        associate_member("test-account_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_associate_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_code_security_scan_configuration.return_value = {}
    batch_associate_code_security_scan_configuration([], region_name=REGION)
    mock_client.batch_associate_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_associate_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to batch associate code security scan configuration"):
        batch_associate_code_security_scan_configuration([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_disassociate_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_code_security_scan_configuration.return_value = {}
    batch_disassociate_code_security_scan_configuration([], region_name=REGION)
    mock_client.batch_disassociate_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_disassociate_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to batch disassociate code security scan configuration"):
        batch_disassociate_code_security_scan_configuration([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_get_code_snippet(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_code_snippet.return_value = {}
    batch_get_code_snippet([], region_name=REGION)
    mock_client.batch_get_code_snippet.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_get_code_snippet_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_code_snippet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_code_snippet",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get code snippet"):
        batch_get_code_snippet([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_get_finding_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_finding_details.return_value = {}
    batch_get_finding_details([], region_name=REGION)
    mock_client.batch_get_finding_details.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_get_finding_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_finding_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_finding_details",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get finding details"):
        batch_get_finding_details([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_get_free_trial_info(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_free_trial_info.return_value = {}
    batch_get_free_trial_info([], region_name=REGION)
    mock_client.batch_get_free_trial_info.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_get_free_trial_info_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_free_trial_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_free_trial_info",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get free trial info"):
        batch_get_free_trial_info([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_get_member_ec2_deep_inspection_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_member_ec2_deep_inspection_status.return_value = {}
    batch_get_member_ec2_deep_inspection_status(region_name=REGION)
    mock_client.batch_get_member_ec2_deep_inspection_status.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_get_member_ec2_deep_inspection_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_member_ec2_deep_inspection_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_member_ec2_deep_inspection_status",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get member ec2 deep inspection status"):
        batch_get_member_ec2_deep_inspection_status(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_batch_update_member_ec2_deep_inspection_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_member_ec2_deep_inspection_status.return_value = {}
    batch_update_member_ec2_deep_inspection_status([], region_name=REGION)
    mock_client.batch_update_member_ec2_deep_inspection_status.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_batch_update_member_ec2_deep_inspection_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_member_ec2_deep_inspection_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_member_ec2_deep_inspection_status",
    )
    with pytest.raises(RuntimeError, match="Failed to batch update member ec2 deep inspection status"):
        batch_update_member_ec2_deep_inspection_status([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_cancel_findings_report(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_findings_report.return_value = {}
    cancel_findings_report("test-report_id", region_name=REGION)
    mock_client.cancel_findings_report.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_cancel_findings_report_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_findings_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_findings_report",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel findings report"):
        cancel_findings_report("test-report_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_cancel_sbom_export(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_sbom_export.return_value = {}
    cancel_sbom_export("test-report_id", region_name=REGION)
    mock_client.cancel_sbom_export.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_cancel_sbom_export_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_sbom_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_sbom_export",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel sbom export"):
        cancel_sbom_export("test-report_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_create_cis_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_cis_scan_configuration.return_value = {}
    create_cis_scan_configuration("test-scan_name", "test-security_level", {}, {}, region_name=REGION)
    mock_client.create_cis_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_create_cis_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_cis_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cis_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to create cis scan configuration"):
        create_cis_scan_configuration("test-scan_name", "test-security_level", {}, {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_create_code_security_integration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_code_security_integration.return_value = {}
    create_code_security_integration("test-name", "test-type_value", region_name=REGION)
    mock_client.create_code_security_integration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_create_code_security_integration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_code_security_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_code_security_integration",
    )
    with pytest.raises(RuntimeError, match="Failed to create code security integration"):
        create_code_security_integration("test-name", "test-type_value", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_create_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_code_security_scan_configuration.return_value = {}
    create_code_security_scan_configuration("test-name", "test-level", {}, region_name=REGION)
    mock_client.create_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_create_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to create code security scan configuration"):
        create_code_security_scan_configuration("test-name", "test-level", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_create_filter(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_filter.return_value = {}
    create_filter("test-action", {}, "test-name", region_name=REGION)
    mock_client.create_filter.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_create_filter_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_filter",
    )
    with pytest.raises(RuntimeError, match="Failed to create filter"):
        create_filter("test-action", {}, "test-name", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_delete_cis_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_cis_scan_configuration.return_value = {}
    delete_cis_scan_configuration("test-scan_configuration_arn", region_name=REGION)
    mock_client.delete_cis_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_delete_cis_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_cis_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cis_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete cis scan configuration"):
        delete_cis_scan_configuration("test-scan_configuration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_delete_code_security_integration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_code_security_integration.return_value = {}
    delete_code_security_integration("test-integration_arn", region_name=REGION)
    mock_client.delete_code_security_integration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_delete_code_security_integration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_code_security_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_code_security_integration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete code security integration"):
        delete_code_security_integration("test-integration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_delete_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_code_security_scan_configuration.return_value = {}
    delete_code_security_scan_configuration("test-scan_configuration_arn", region_name=REGION)
    mock_client.delete_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_delete_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete code security scan configuration"):
        delete_code_security_scan_configuration("test-scan_configuration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_delete_filter(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_filter.return_value = {}
    delete_filter("test-arn", region_name=REGION)
    mock_client.delete_filter.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_delete_filter_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_filter",
    )
    with pytest.raises(RuntimeError, match="Failed to delete filter"):
        delete_filter("test-arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_describe_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.return_value = {}
    describe_organization_configuration(region_name=REGION)
    mock_client.describe_organization_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_describe_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe organization configuration"):
        describe_organization_configuration(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_disable_delegated_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_delegated_admin_account.return_value = {}
    disable_delegated_admin_account("test-delegated_admin_account_id", region_name=REGION)
    mock_client.disable_delegated_admin_account.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_disable_delegated_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_delegated_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_delegated_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disable delegated admin account"):
        disable_delegated_admin_account("test-delegated_admin_account_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_disassociate_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_member.return_value = {}
    disassociate_member("test-account_id", region_name=REGION)
    mock_client.disassociate_member.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_disassociate_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_member",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate member"):
        disassociate_member("test-account_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_enable_delegated_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_delegated_admin_account.return_value = {}
    enable_delegated_admin_account("test-delegated_admin_account_id", region_name=REGION)
    mock_client.enable_delegated_admin_account.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_enable_delegated_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_delegated_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_delegated_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to enable delegated admin account"):
        enable_delegated_admin_account("test-delegated_admin_account_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_cis_scan_report(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cis_scan_report.return_value = {}
    get_cis_scan_report("test-scan_arn", region_name=REGION)
    mock_client.get_cis_scan_report.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_cis_scan_report_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cis_scan_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cis_scan_report",
    )
    with pytest.raises(RuntimeError, match="Failed to get cis scan report"):
        get_cis_scan_report("test-scan_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_cis_scan_result_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cis_scan_result_details.return_value = {}
    get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", "test-account_id", region_name=REGION)
    mock_client.get_cis_scan_result_details.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_cis_scan_result_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cis_scan_result_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cis_scan_result_details",
    )
    with pytest.raises(RuntimeError, match="Failed to get cis scan result details"):
        get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", "test-account_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_clusters_for_image(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_clusters_for_image.return_value = {}
    get_clusters_for_image({}, region_name=REGION)
    mock_client.get_clusters_for_image.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_clusters_for_image_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_clusters_for_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_clusters_for_image",
    )
    with pytest.raises(RuntimeError, match="Failed to get clusters for image"):
        get_clusters_for_image({}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_code_security_integration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_integration.return_value = {}
    get_code_security_integration("test-integration_arn", region_name=REGION)
    mock_client.get_code_security_integration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_code_security_integration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_code_security_integration",
    )
    with pytest.raises(RuntimeError, match="Failed to get code security integration"):
        get_code_security_integration("test-integration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_code_security_scan(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_scan.return_value = {}
    get_code_security_scan({}, "test-scan_id", region_name=REGION)
    mock_client.get_code_security_scan.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_code_security_scan_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_scan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_code_security_scan",
    )
    with pytest.raises(RuntimeError, match="Failed to get code security scan"):
        get_code_security_scan({}, "test-scan_id", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_scan_configuration.return_value = {}
    get_code_security_scan_configuration("test-scan_configuration_arn", region_name=REGION)
    mock_client.get_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get code security scan configuration"):
        get_code_security_scan_configuration("test-scan_configuration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_delegated_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_delegated_admin_account.return_value = {}
    get_delegated_admin_account(region_name=REGION)
    mock_client.get_delegated_admin_account.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_delegated_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_delegated_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_delegated_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to get delegated admin account"):
        get_delegated_admin_account(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_ec2_deep_inspection_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_ec2_deep_inspection_configuration.return_value = {}
    get_ec2_deep_inspection_configuration(region_name=REGION)
    mock_client.get_ec2_deep_inspection_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_ec2_deep_inspection_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_ec2_deep_inspection_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ec2_deep_inspection_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get ec2 deep inspection configuration"):
        get_ec2_deep_inspection_configuration(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_get_encryption_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_encryption_key.return_value = {}
    get_encryption_key("test-scan_type", "test-resource_type", region_name=REGION)
    mock_client.get_encryption_key.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_get_encryption_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_encryption_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_encryption_key",
    )
    with pytest.raises(RuntimeError, match="Failed to get encryption key"):
        get_encryption_key("test-scan_type", "test-resource_type", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_account_permissions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_account_permissions.return_value = {}
    list_account_permissions(region_name=REGION)
    mock_client.list_account_permissions.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_account_permissions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_account_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_permissions",
    )
    with pytest.raises(RuntimeError, match="Failed to list account permissions"):
        list_account_permissions(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_configurations.return_value = {}
    list_cis_scan_configurations(region_name=REGION)
    mock_client.list_cis_scan_configurations.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cis_scan_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to list cis scan configurations"):
        list_cis_scan_configurations(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_results_aggregated_by_checks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_results_aggregated_by_checks.return_value = {}
    list_cis_scan_results_aggregated_by_checks("test-scan_arn", region_name=REGION)
    mock_client.list_cis_scan_results_aggregated_by_checks.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_results_aggregated_by_checks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_results_aggregated_by_checks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cis_scan_results_aggregated_by_checks",
    )
    with pytest.raises(RuntimeError, match="Failed to list cis scan results aggregated by checks"):
        list_cis_scan_results_aggregated_by_checks("test-scan_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_results_aggregated_by_target_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_results_aggregated_by_target_resource.return_value = {}
    list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", region_name=REGION)
    mock_client.list_cis_scan_results_aggregated_by_target_resource.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_cis_scan_results_aggregated_by_target_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scan_results_aggregated_by_target_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cis_scan_results_aggregated_by_target_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list cis scan results aggregated by target resource"):
        list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_cis_scans(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scans.return_value = {}
    list_cis_scans(region_name=REGION)
    mock_client.list_cis_scans.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_cis_scans_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_cis_scans.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cis_scans",
    )
    with pytest.raises(RuntimeError, match="Failed to list cis scans"):
        list_cis_scans(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_code_security_integrations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_integrations.return_value = {}
    list_code_security_integrations(region_name=REGION)
    mock_client.list_code_security_integrations.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_code_security_integrations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_code_security_integrations",
    )
    with pytest.raises(RuntimeError, match="Failed to list code security integrations"):
        list_code_security_integrations(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_code_security_scan_configuration_associations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_scan_configuration_associations.return_value = {}
    list_code_security_scan_configuration_associations("test-scan_configuration_arn", region_name=REGION)
    mock_client.list_code_security_scan_configuration_associations.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_code_security_scan_configuration_associations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_scan_configuration_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_code_security_scan_configuration_associations",
    )
    with pytest.raises(RuntimeError, match="Failed to list code security scan configuration associations"):
        list_code_security_scan_configuration_associations("test-scan_configuration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_code_security_scan_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_scan_configurations.return_value = {}
    list_code_security_scan_configurations(region_name=REGION)
    mock_client.list_code_security_scan_configurations.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_code_security_scan_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_code_security_scan_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_code_security_scan_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to list code security scan configurations"):
        list_code_security_scan_configurations(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_coverage_statistics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_coverage_statistics.return_value = {}
    list_coverage_statistics(region_name=REGION)
    mock_client.list_coverage_statistics.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_coverage_statistics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_coverage_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_coverage_statistics",
    )
    with pytest.raises(RuntimeError, match="Failed to list coverage statistics"):
        list_coverage_statistics(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_delegated_admin_accounts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_delegated_admin_accounts.return_value = {}
    list_delegated_admin_accounts(region_name=REGION)
    mock_client.list_delegated_admin_accounts.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_delegated_admin_accounts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_delegated_admin_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_delegated_admin_accounts",
    )
    with pytest.raises(RuntimeError, match="Failed to list delegated admin accounts"):
        list_delegated_admin_accounts(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_filters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_filters.return_value = {}
    list_filters(region_name=REGION)
    mock_client.list_filters.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_filters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_filters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_filters",
    )
    with pytest.raises(RuntimeError, match="Failed to list filters"):
        list_filters(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_list_usage_totals(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_usage_totals.return_value = {}
    list_usage_totals(region_name=REGION)
    mock_client.list_usage_totals.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_list_usage_totals_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_usage_totals.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_usage_totals",
    )
    with pytest.raises(RuntimeError, match="Failed to list usage totals"):
        list_usage_totals(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_reset_encryption_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_encryption_key.return_value = {}
    reset_encryption_key("test-scan_type", "test-resource_type", region_name=REGION)
    mock_client.reset_encryption_key.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_reset_encryption_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_encryption_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_encryption_key",
    )
    with pytest.raises(RuntimeError, match="Failed to reset encryption key"):
        reset_encryption_key("test-scan_type", "test-resource_type", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_search_vulnerabilities(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_vulnerabilities.return_value = {}
    search_vulnerabilities({}, region_name=REGION)
    mock_client.search_vulnerabilities.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_search_vulnerabilities_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_vulnerabilities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_vulnerabilities",
    )
    with pytest.raises(RuntimeError, match="Failed to search vulnerabilities"):
        search_vulnerabilities({}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_send_cis_session_health(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_cis_session_health.return_value = {}
    send_cis_session_health("test-scan_job_id", "test-session_token", region_name=REGION)
    mock_client.send_cis_session_health.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_send_cis_session_health_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_cis_session_health.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_cis_session_health",
    )
    with pytest.raises(RuntimeError, match="Failed to send cis session health"):
        send_cis_session_health("test-scan_job_id", "test-session_token", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_send_cis_session_telemetry(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_cis_session_telemetry.return_value = {}
    send_cis_session_telemetry("test-scan_job_id", "test-session_token", [], region_name=REGION)
    mock_client.send_cis_session_telemetry.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_send_cis_session_telemetry_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_cis_session_telemetry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_cis_session_telemetry",
    )
    with pytest.raises(RuntimeError, match="Failed to send cis session telemetry"):
        send_cis_session_telemetry("test-scan_job_id", "test-session_token", [], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_start_cis_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_cis_session.return_value = {}
    start_cis_session("test-scan_job_id", {}, region_name=REGION)
    mock_client.start_cis_session.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_start_cis_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_cis_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_cis_session",
    )
    with pytest.raises(RuntimeError, match="Failed to start cis session"):
        start_cis_session("test-scan_job_id", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_start_code_security_scan(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_code_security_scan.return_value = {}
    start_code_security_scan({}, region_name=REGION)
    mock_client.start_code_security_scan.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_start_code_security_scan_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_code_security_scan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_code_security_scan",
    )
    with pytest.raises(RuntimeError, match="Failed to start code security scan"):
        start_code_security_scan({}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_stop_cis_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_cis_session.return_value = {}
    stop_cis_session("test-scan_job_id", "test-session_token", {}, region_name=REGION)
    mock_client.stop_cis_session.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_stop_cis_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_cis_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_cis_session",
    )
    with pytest.raises(RuntimeError, match="Failed to stop cis session"):
        stop_cis_session("test-scan_job_id", "test-session_token", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_cis_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_cis_scan_configuration.return_value = {}
    update_cis_scan_configuration("test-scan_configuration_arn", region_name=REGION)
    mock_client.update_cis_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_cis_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_cis_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cis_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update cis scan configuration"):
        update_cis_scan_configuration("test-scan_configuration_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_code_security_integration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_code_security_integration.return_value = {}
    update_code_security_integration("test-integration_arn", {}, region_name=REGION)
    mock_client.update_code_security_integration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_code_security_integration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_code_security_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_code_security_integration",
    )
    with pytest.raises(RuntimeError, match="Failed to update code security integration"):
        update_code_security_integration("test-integration_arn", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_code_security_scan_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_code_security_scan_configuration.return_value = {}
    update_code_security_scan_configuration("test-scan_configuration_arn", {}, region_name=REGION)
    mock_client.update_code_security_scan_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_code_security_scan_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_code_security_scan_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_code_security_scan_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update code security scan configuration"):
        update_code_security_scan_configuration("test-scan_configuration_arn", {}, region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_ec2_deep_inspection_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ec2_deep_inspection_configuration.return_value = {}
    update_ec2_deep_inspection_configuration(region_name=REGION)
    mock_client.update_ec2_deep_inspection_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_ec2_deep_inspection_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ec2_deep_inspection_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ec2_deep_inspection_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update ec2 deep inspection configuration"):
        update_ec2_deep_inspection_configuration(region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_encryption_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_encryption_key.return_value = {}
    update_encryption_key("test-kms_key_id", "test-scan_type", "test-resource_type", region_name=REGION)
    mock_client.update_encryption_key.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_encryption_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_encryption_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_encryption_key",
    )
    with pytest.raises(RuntimeError, match="Failed to update encryption key"):
        update_encryption_key("test-kms_key_id", "test-scan_type", "test-resource_type", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_filter(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_filter.return_value = {}
    update_filter("test-filter_arn", region_name=REGION)
    mock_client.update_filter.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_filter_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_filter",
    )
    with pytest.raises(RuntimeError, match="Failed to update filter"):
        update_filter("test-filter_arn", region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_org_ec2_deep_inspection_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_org_ec2_deep_inspection_configuration.return_value = {}
    update_org_ec2_deep_inspection_configuration([], region_name=REGION)
    mock_client.update_org_ec2_deep_inspection_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_org_ec2_deep_inspection_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_org_ec2_deep_inspection_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_org_ec2_deep_inspection_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update org ec2 deep inspection configuration"):
        update_org_ec2_deep_inspection_configuration([], region_name=REGION)


@patch("aws_util.inspector.get_client")
def test_update_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.return_value = {}
    update_organization_configuration({}, region_name=REGION)
    mock_client.update_organization_configuration.assert_called_once()


@patch("aws_util.inspector.get_client")
def test_update_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update organization configuration"):
        update_organization_configuration({}, region_name=REGION)


def test_update_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import update_configuration
    mock_client = MagicMock()
    mock_client.update_configuration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    update_configuration(ecr_configuration={}, ec2_configuration={}, region_name="us-east-1")
    mock_client.update_configuration.assert_called_once()

def test_list_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_findings
    mock_client = MagicMock()
    mock_client.list_findings.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_findings(max_results=1, region_name="us-east-1")
    mock_client.list_findings.assert_called_once()

def test_list_finding_aggregations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_finding_aggregations
    mock_client = MagicMock()
    mock_client.list_finding_aggregations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_finding_aggregations("test-aggregation_type", max_results=1, region_name="us-east-1")
    mock_client.list_finding_aggregations.assert_called_once()

def test_list_coverage_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_coverage
    mock_client = MagicMock()
    mock_client.list_coverage.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_coverage(max_results=1, region_name="us-east-1")
    mock_client.list_coverage.assert_called_once()

def test_list_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_members
    mock_client = MagicMock()
    mock_client.list_members.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_members(max_results=1, region_name="us-east-1")
    mock_client.list_members.assert_called_once()

def test_batch_get_member_ec2_deep_inspection_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import batch_get_member_ec2_deep_inspection_status
    mock_client = MagicMock()
    mock_client.batch_get_member_ec2_deep_inspection_status.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    batch_get_member_ec2_deep_inspection_status(account_ids=1, region_name="us-east-1")
    mock_client.batch_get_member_ec2_deep_inspection_status.assert_called_once()

def test_create_cis_scan_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import create_cis_scan_configuration
    mock_client = MagicMock()
    mock_client.create_cis_scan_configuration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    create_cis_scan_configuration("test-scan_name", "test-security_level", "test-schedule", "test-targets", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_cis_scan_configuration.assert_called_once()

def test_create_code_security_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import create_code_security_integration
    mock_client = MagicMock()
    mock_client.create_code_security_integration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    create_code_security_integration("test-name", "test-type_value", details="test-details", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_code_security_integration.assert_called_once()

def test_create_code_security_scan_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import create_code_security_scan_configuration
    mock_client = MagicMock()
    mock_client.create_code_security_scan_configuration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    create_code_security_scan_configuration("test-name", "test-level", {}, scope_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_code_security_scan_configuration.assert_called_once()

def test_create_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import create_filter
    mock_client = MagicMock()
    mock_client.create_filter.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    create_filter("test-action", "test-filter_criteria", "test-name", description="test-description", tags=[{"Key": "k", "Value": "v"}], reason="test-reason", region_name="us-east-1")
    mock_client.create_filter.assert_called_once()

def test_enable_delegated_admin_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import enable_delegated_admin_account
    mock_client = MagicMock()
    mock_client.enable_delegated_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    enable_delegated_admin_account(1, client_token="test-client_token", region_name="us-east-1")
    mock_client.enable_delegated_admin_account.assert_called_once()

def test_get_cis_scan_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import get_cis_scan_report
    mock_client = MagicMock()
    mock_client.get_cis_scan_report.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    get_cis_scan_report("test-scan_arn", target_accounts=1, report_format=1, region_name="us-east-1")
    mock_client.get_cis_scan_report.assert_called_once()

def test_get_cis_scan_result_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import get_cis_scan_result_details
    mock_client = MagicMock()
    mock_client.get_cis_scan_result_details.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", 1, filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_cis_scan_result_details.assert_called_once()

def test_get_clusters_for_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import get_clusters_for_image
    mock_client = MagicMock()
    mock_client.get_clusters_for_image.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    get_clusters_for_image("test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_clusters_for_image.assert_called_once()

def test_get_code_security_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import get_code_security_integration
    mock_client = MagicMock()
    mock_client.get_code_security_integration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    get_code_security_integration("test-integration_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.get_code_security_integration.assert_called_once()

def test_list_account_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_account_permissions
    mock_client = MagicMock()
    mock_client.list_account_permissions.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_account_permissions(service="test-service", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_account_permissions.assert_called_once()

def test_list_cis_scan_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_cis_scan_configurations
    mock_client = MagicMock()
    mock_client.list_cis_scan_configurations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_cis_scan_configurations(filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cis_scan_configurations.assert_called_once()

def test_list_cis_scan_results_aggregated_by_checks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_cis_scan_results_aggregated_by_checks
    mock_client = MagicMock()
    mock_client.list_cis_scan_results_aggregated_by_checks.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_cis_scan_results_aggregated_by_checks("test-scan_arn", filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cis_scan_results_aggregated_by_checks.assert_called_once()

def test_list_cis_scan_results_aggregated_by_target_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_cis_scan_results_aggregated_by_target_resource
    mock_client = MagicMock()
    mock_client.list_cis_scan_results_aggregated_by_target_resource.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cis_scan_results_aggregated_by_target_resource.assert_called_once()

def test_list_cis_scans_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_cis_scans
    mock_client = MagicMock()
    mock_client.list_cis_scans.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_cis_scans(filter_criteria="test-filter_criteria", detail_level="test-detail_level", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cis_scans.assert_called_once()

def test_list_code_security_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_code_security_integrations
    mock_client = MagicMock()
    mock_client.list_code_security_integrations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_code_security_integrations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_code_security_integrations.assert_called_once()

def test_list_code_security_scan_configuration_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_code_security_scan_configuration_associations
    mock_client = MagicMock()
    mock_client.list_code_security_scan_configuration_associations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_code_security_scan_configuration_associations({}, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_code_security_scan_configuration_associations.assert_called_once()

def test_list_code_security_scan_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_code_security_scan_configurations
    mock_client = MagicMock()
    mock_client.list_code_security_scan_configurations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_code_security_scan_configurations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_code_security_scan_configurations.assert_called_once()

def test_list_coverage_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_coverage_statistics
    mock_client = MagicMock()
    mock_client.list_coverage_statistics.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_coverage_statistics(filter_criteria="test-filter_criteria", group_by="test-group_by", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_coverage_statistics.assert_called_once()

def test_list_delegated_admin_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_delegated_admin_accounts
    mock_client = MagicMock()
    mock_client.list_delegated_admin_accounts.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_delegated_admin_accounts(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_delegated_admin_accounts.assert_called_once()

def test_list_filters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_filters
    mock_client = MagicMock()
    mock_client.list_filters.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_filters(arns="test-arns", action="test-action", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_filters.assert_called_once()

def test_list_usage_totals_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_usage_totals
    mock_client = MagicMock()
    mock_client.list_usage_totals.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_usage_totals(max_results=1, next_token="test-next_token", account_ids=1, region_name="us-east-1")
    mock_client.list_usage_totals.assert_called_once()

def test_search_vulnerabilities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import search_vulnerabilities
    mock_client = MagicMock()
    mock_client.search_vulnerabilities.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    search_vulnerabilities("test-filter_criteria", next_token="test-next_token", region_name="us-east-1")
    mock_client.search_vulnerabilities.assert_called_once()

def test_start_code_security_scan_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import start_code_security_scan
    mock_client = MagicMock()
    mock_client.start_code_security_scan.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    start_code_security_scan("test-resource", client_token="test-client_token", region_name="us-east-1")
    mock_client.start_code_security_scan.assert_called_once()

def test_update_cis_scan_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import update_cis_scan_configuration
    mock_client = MagicMock()
    mock_client.update_cis_scan_configuration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    update_cis_scan_configuration({}, scan_name="test-scan_name", security_level="test-security_level", schedule="test-schedule", targets="test-targets", region_name="us-east-1")
    mock_client.update_cis_scan_configuration.assert_called_once()

def test_update_ec2_deep_inspection_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import update_ec2_deep_inspection_configuration
    mock_client = MagicMock()
    mock_client.update_ec2_deep_inspection_configuration.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    update_ec2_deep_inspection_configuration(activate_deep_inspection=True, package_paths="test-package_paths", region_name="us-east-1")
    mock_client.update_ec2_deep_inspection_configuration.assert_called_once()

def test_update_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import update_filter
    mock_client = MagicMock()
    mock_client.update_filter.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    update_filter("test-filter_arn", action="test-action", description="test-description", filter_criteria="test-filter_criteria", name="test-name", reason="test-reason", region_name="us-east-1")
    mock_client.update_filter.assert_called_once()


def test_list_coverage_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_coverage
    mock_client = MagicMock()
    mock_client.list_coverage.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: mock_client)
    list_coverage(filter_criteria="test-filter_criteria", region_name="us-east-1")
    mock_client.list_coverage.assert_called_once()

def test_enable_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import enable
    m = MagicMock(); m.enable.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: m)
    enable(["EC2"], account_ids=["123"], client_token="tok", region_name="us-east-1")

def test_list_findings_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_findings
    m = MagicMock(); m.list_findings.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: m)
    list_findings(filter_criteria={"severity": "HIGH"}, sort_criteria={"field": "SEVERITY"}, region_name="us-east-1")

def test_list_finding_aggregations_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.inspector import list_finding_aggregations
    m = MagicMock(); m.list_finding_aggregations.return_value = {}
    monkeypatch.setattr("aws_util.inspector.get_client", lambda *a, **kw: m)
    list_finding_aggregations("FINDING_TYPE", aggregation_request={"findingTypeAggregation": {}}, region_name="us-east-1")
