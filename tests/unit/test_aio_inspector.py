"""Tests for aws_util.aio.inspector -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.inspector import (
    AccountStatusResult,
    ConfigurationResult,
    CoverageResult,
    FindingResult,
    MemberResult,
    ReportStatusResult,
    SbomExportResult,
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


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


async def test_enable(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"accounts": [{"accountId": "111"}], "failedAccounts": []}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await enable(["EC2"])
    assert len(result["accounts"]) == 1

async def test_enable_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="enable failed"):
        await enable(["EC2"])


async def test_disable(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"accounts": [], "failedAccounts": []}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await disable(["EC2"])
    assert result["failedAccounts"] == []


async def test_disable_with_account_ids(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"accounts": [], "failedAccounts": []}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    await disable(["EC2"], account_ids=["111"])
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["accountIds"] == ["111"]


async def test_disable_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await disable(["EC2"])


# ---------------------------------------------------------------------------
# get_configuration / update_configuration
# ---------------------------------------------------------------------------


async def test_get_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ecrConfiguration": {"x": "y"},
        "ec2Configuration": {"a": "b"},
        "ResponseMetadata": {},
    }
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await get_configuration()
    assert isinstance(result, ConfigurationResult)


async def test_get_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_configuration()


async def test_update_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    await update_configuration(ecr_configuration={"a": "b"}, ec2_configuration={"c": "d"})
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["ecrConfiguration"] == {"a": "b"}


async def test_update_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await update_configuration()


# ---------------------------------------------------------------------------
# batch_get_account_status
# ---------------------------------------------------------------------------


async def test_batch_get_account_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "accounts": [{"accountId": "111", "state": {}, "resourceState": {}}],
    }
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await batch_get_account_status(["111"])
    assert len(result) == 1


async def test_batch_get_account_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await batch_get_account_status(["111"])


# ---------------------------------------------------------------------------
# list_findings
# ---------------------------------------------------------------------------


async def test_list_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"findings": [{"findingArn": "arn:f"}]}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_findings()
    assert len(result) == 1

async def test_list_findings_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"findings": [{"findingArn": "a1"}], "nextToken": "tok"},
        {"findings": [{"findingArn": "a2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_findings()
    assert len(result) == 2


async def test_list_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_findings()


# ---------------------------------------------------------------------------
# list_finding_aggregations
# ---------------------------------------------------------------------------


async def test_list_finding_aggregations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"responses": [{"key": "val"}]}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_finding_aggregations("FINDING_TYPE")
    assert len(result) == 1

async def test_list_finding_aggregations_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"responses": [{"a": 1}], "nextToken": "tok"},
        {"responses": [{"a": 2}]},
    ]
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_finding_aggregations("FINDING_TYPE")
    assert len(result) == 2


async def test_list_finding_aggregations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_finding_aggregations("FINDING_TYPE")


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


async def test_get_findings_report_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "reportId": "r1", "status": "COMPLETE", "errorCode": "",
        "errorMessage": "", "destination": {}, "ResponseMetadata": {},
    }
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await get_findings_report_status("r1")
    assert isinstance(result, ReportStatusResult)


async def test_get_findings_report_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_findings_report_status("r1")


async def test_create_findings_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"reportId": "r1"}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await create_findings_report(report_format="JSON", s3_destination={"bucketName": "b"})
    assert result == "r1"


async def test_create_findings_report_with_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"reportId": "r1"}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    await create_findings_report(
        report_format="CSV", s3_destination={"bucketName": "b"}, filter_criteria={"f": "v"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "filterCriteria" in call_kwargs


async def test_create_findings_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await create_findings_report(report_format="JSON", s3_destination={"bucketName": "b"})


# ---------------------------------------------------------------------------
# SBOM exports
# ---------------------------------------------------------------------------


async def test_get_sbom_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "reportId": "r1", "status": "COMPLETE", "errorCode": "",
        "errorMessage": "", "s3Destination": {}, "ResponseMetadata": {},
    }
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await get_sbom_export("r1")
    assert isinstance(result, SbomExportResult)


async def test_get_sbom_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_sbom_export("r1")


async def test_create_sbom_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"reportId": "r1"}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await create_sbom_export(report_format="CYCLONEDX_1_4", s3_destination={"bucketName": "b"})
    assert result == "r1"


async def test_create_sbom_export_with_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"reportId": "r1"}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    await create_sbom_export(
        report_format="SPDX_2_3", s3_destination={"bucketName": "b"},
        resource_filter_criteria={"f": "v"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "resourceFilterCriteria" in call_kwargs


async def test_create_sbom_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await create_sbom_export(report_format="CYCLONEDX_1_4", s3_destination={"bucketName": "b"})


# ---------------------------------------------------------------------------
# list_coverage
# ---------------------------------------------------------------------------


async def test_list_coverage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"coveredResources": [{"resourceId": "r1"}]}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_coverage()
    assert len(result) == 1

async def test_list_coverage_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"coveredResources": [{"resourceId": "r1"}], "nextToken": "tok"},
        {"coveredResources": [{"resourceId": "r2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_coverage()
    assert len(result) == 2


async def test_list_coverage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_coverage()


# ---------------------------------------------------------------------------
# list_members / get_member
# ---------------------------------------------------------------------------


async def test_list_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"members": [{"accountId": "111"}]}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_members()
    assert len(result) == 1

async def test_list_members_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"members": [{"accountId": "1"}], "nextToken": "tok"},
        {"members": [{"accountId": "2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await list_members()
    assert len(result) == 2


async def test_list_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_members()


async def test_get_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"member": {"accountId": "111", "relationshipStatus": "ASSOCIATED"}}
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    result = await get_member("111")
    assert isinstance(result, MemberResult)


async def test_get_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.inspector.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_member("111")


async def test_associate_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_member("test-account_id", )
    mock_client.call.assert_called_once()


async def test_associate_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_member("test-account_id", )


async def test_batch_associate_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_code_security_scan_configuration([], )
    mock_client.call.assert_called_once()


async def test_batch_associate_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_code_security_scan_configuration([], )


async def test_batch_disassociate_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_code_security_scan_configuration([], )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_code_security_scan_configuration([], )


async def test_batch_get_code_snippet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_code_snippet([], )
    mock_client.call.assert_called_once()


async def test_batch_get_code_snippet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_code_snippet([], )


async def test_batch_get_finding_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_finding_details([], )
    mock_client.call.assert_called_once()


async def test_batch_get_finding_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_finding_details([], )


async def test_batch_get_free_trial_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_free_trial_info([], )
    mock_client.call.assert_called_once()


async def test_batch_get_free_trial_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_free_trial_info([], )


async def test_batch_get_member_ec2_deep_inspection_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_member_ec2_deep_inspection_status()
    mock_client.call.assert_called_once()


async def test_batch_get_member_ec2_deep_inspection_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_member_ec2_deep_inspection_status()


async def test_batch_update_member_ec2_deep_inspection_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_member_ec2_deep_inspection_status([], )
    mock_client.call.assert_called_once()


async def test_batch_update_member_ec2_deep_inspection_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_member_ec2_deep_inspection_status([], )


async def test_cancel_findings_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_findings_report("test-report_id", )
    mock_client.call.assert_called_once()


async def test_cancel_findings_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_findings_report("test-report_id", )


async def test_cancel_sbom_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_sbom_export("test-report_id", )
    mock_client.call.assert_called_once()


async def test_cancel_sbom_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_sbom_export("test-report_id", )


async def test_create_cis_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cis_scan_configuration("test-scan_name", "test-security_level", {}, {}, )
    mock_client.call.assert_called_once()


async def test_create_cis_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cis_scan_configuration("test-scan_name", "test-security_level", {}, {}, )


async def test_create_code_security_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_code_security_integration("test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_code_security_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_code_security_integration("test-name", "test-type_value", )


async def test_create_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_code_security_scan_configuration("test-name", "test-level", {}, )
    mock_client.call.assert_called_once()


async def test_create_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_code_security_scan_configuration("test-name", "test-level", {}, )


async def test_create_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_filter("test-action", {}, "test-name", )
    mock_client.call.assert_called_once()


async def test_create_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_filter("test-action", {}, "test-name", )


async def test_delete_cis_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cis_scan_configuration("test-scan_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_cis_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cis_scan_configuration("test-scan_configuration_arn", )


async def test_delete_code_security_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_code_security_integration("test-integration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_code_security_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_code_security_integration("test-integration_arn", )


async def test_delete_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_code_security_scan_configuration("test-scan_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_delete_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_code_security_scan_configuration("test-scan_configuration_arn", )


async def test_delete_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_filter("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_filter("test-arn", )


async def test_describe_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_organization_configuration()
    mock_client.call.assert_called_once()


async def test_describe_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_configuration()


async def test_disable_delegated_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_delegated_admin_account("test-delegated_admin_account_id", )
    mock_client.call.assert_called_once()


async def test_disable_delegated_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_delegated_admin_account("test-delegated_admin_account_id", )


async def test_disassociate_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_member("test-account_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_member("test-account_id", )


async def test_enable_delegated_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_delegated_admin_account("test-delegated_admin_account_id", )
    mock_client.call.assert_called_once()


async def test_enable_delegated_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_delegated_admin_account("test-delegated_admin_account_id", )


async def test_get_cis_scan_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cis_scan_report("test-scan_arn", )
    mock_client.call.assert_called_once()


async def test_get_cis_scan_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cis_scan_report("test-scan_arn", )


async def test_get_cis_scan_result_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", "test-account_id", )
    mock_client.call.assert_called_once()


async def test_get_cis_scan_result_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", "test-account_id", )


async def test_get_clusters_for_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_clusters_for_image({}, )
    mock_client.call.assert_called_once()


async def test_get_clusters_for_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_clusters_for_image({}, )


async def test_get_code_security_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_code_security_integration("test-integration_arn", )
    mock_client.call.assert_called_once()


async def test_get_code_security_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_code_security_integration("test-integration_arn", )


async def test_get_code_security_scan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_code_security_scan({}, "test-scan_id", )
    mock_client.call.assert_called_once()


async def test_get_code_security_scan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_code_security_scan({}, "test-scan_id", )


async def test_get_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_code_security_scan_configuration("test-scan_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_get_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_code_security_scan_configuration("test-scan_configuration_arn", )


async def test_get_delegated_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_delegated_admin_account()
    mock_client.call.assert_called_once()


async def test_get_delegated_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_delegated_admin_account()


async def test_get_ec2_deep_inspection_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ec2_deep_inspection_configuration()
    mock_client.call.assert_called_once()


async def test_get_ec2_deep_inspection_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ec2_deep_inspection_configuration()


async def test_get_encryption_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_encryption_key("test-scan_type", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_get_encryption_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_encryption_key("test-scan_type", "test-resource_type", )


async def test_list_account_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_permissions()
    mock_client.call.assert_called_once()


async def test_list_account_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_permissions()


async def test_list_cis_scan_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cis_scan_configurations()
    mock_client.call.assert_called_once()


async def test_list_cis_scan_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cis_scan_configurations()


async def test_list_cis_scan_results_aggregated_by_checks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cis_scan_results_aggregated_by_checks("test-scan_arn", )
    mock_client.call.assert_called_once()


async def test_list_cis_scan_results_aggregated_by_checks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cis_scan_results_aggregated_by_checks("test-scan_arn", )


async def test_list_cis_scan_results_aggregated_by_target_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", )
    mock_client.call.assert_called_once()


async def test_list_cis_scan_results_aggregated_by_target_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", )


async def test_list_cis_scans(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cis_scans()
    mock_client.call.assert_called_once()


async def test_list_cis_scans_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cis_scans()


async def test_list_code_security_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_code_security_integrations()
    mock_client.call.assert_called_once()


async def test_list_code_security_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_code_security_integrations()


async def test_list_code_security_scan_configuration_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_code_security_scan_configuration_associations("test-scan_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_list_code_security_scan_configuration_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_code_security_scan_configuration_associations("test-scan_configuration_arn", )


async def test_list_code_security_scan_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_code_security_scan_configurations()
    mock_client.call.assert_called_once()


async def test_list_code_security_scan_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_code_security_scan_configurations()


async def test_list_coverage_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_coverage_statistics()
    mock_client.call.assert_called_once()


async def test_list_coverage_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_coverage_statistics()


async def test_list_delegated_admin_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_delegated_admin_accounts()
    mock_client.call.assert_called_once()


async def test_list_delegated_admin_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_delegated_admin_accounts()


async def test_list_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_filters()
    mock_client.call.assert_called_once()


async def test_list_filters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_filters()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_usage_totals(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_usage_totals()
    mock_client.call.assert_called_once()


async def test_list_usage_totals_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_usage_totals()


async def test_reset_encryption_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_encryption_key("test-scan_type", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_reset_encryption_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_encryption_key("test-scan_type", "test-resource_type", )


async def test_search_vulnerabilities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_vulnerabilities({}, )
    mock_client.call.assert_called_once()


async def test_search_vulnerabilities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_vulnerabilities({}, )


async def test_send_cis_session_health(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_cis_session_health("test-scan_job_id", "test-session_token", )
    mock_client.call.assert_called_once()


async def test_send_cis_session_health_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_cis_session_health("test-scan_job_id", "test-session_token", )


async def test_send_cis_session_telemetry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_cis_session_telemetry("test-scan_job_id", "test-session_token", [], )
    mock_client.call.assert_called_once()


async def test_send_cis_session_telemetry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_cis_session_telemetry("test-scan_job_id", "test-session_token", [], )


async def test_start_cis_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_cis_session("test-scan_job_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_cis_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_cis_session("test-scan_job_id", {}, )


async def test_start_code_security_scan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_code_security_scan({}, )
    mock_client.call.assert_called_once()


async def test_start_code_security_scan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_code_security_scan({}, )


async def test_stop_cis_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_cis_session("test-scan_job_id", "test-session_token", {}, )
    mock_client.call.assert_called_once()


async def test_stop_cis_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_cis_session("test-scan_job_id", "test-session_token", {}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_cis_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_cis_scan_configuration("test-scan_configuration_arn", )
    mock_client.call.assert_called_once()


async def test_update_cis_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_cis_scan_configuration("test-scan_configuration_arn", )


async def test_update_code_security_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_code_security_integration("test-integration_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_code_security_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_code_security_integration("test-integration_arn", {}, )


async def test_update_code_security_scan_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_code_security_scan_configuration("test-scan_configuration_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_code_security_scan_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_code_security_scan_configuration("test-scan_configuration_arn", {}, )


async def test_update_ec2_deep_inspection_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ec2_deep_inspection_configuration()
    mock_client.call.assert_called_once()


async def test_update_ec2_deep_inspection_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ec2_deep_inspection_configuration()


async def test_update_encryption_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_encryption_key("test-kms_key_id", "test-scan_type", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_update_encryption_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_encryption_key("test-kms_key_id", "test-scan_type", "test-resource_type", )


async def test_update_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_filter("test-filter_arn", )
    mock_client.call.assert_called_once()


async def test_update_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_filter("test-filter_arn", )


async def test_update_org_ec2_deep_inspection_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_org_ec2_deep_inspection_configuration([], )
    mock_client.call.assert_called_once()


async def test_update_org_ec2_deep_inspection_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_org_ec2_deep_inspection_configuration([], )


async def test_update_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_organization_configuration({}, )
    mock_client.call.assert_called_once()


async def test_update_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.inspector.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_organization_configuration({}, )


@pytest.mark.asyncio
async def test_update_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import update_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await update_configuration(ecr_configuration={}, ec2_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_findings(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_finding_aggregations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_finding_aggregations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_finding_aggregations("test-aggregation_type", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_coverage_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_coverage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_coverage(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_members(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_member_ec2_deep_inspection_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import batch_get_member_ec2_deep_inspection_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await batch_get_member_ec2_deep_inspection_status(account_ids=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cis_scan_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import create_cis_scan_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await create_cis_scan_configuration("test-scan_name", "test-security_level", "test-schedule", "test-targets", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_code_security_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import create_code_security_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await create_code_security_integration("test-name", "test-type_value", details="test-details", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_code_security_scan_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import create_code_security_scan_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await create_code_security_scan_configuration("test-name", "test-level", {}, scope_settings={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import create_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await create_filter("test-action", "test-filter_criteria", "test-name", description="test-description", tags=[{"Key": "k", "Value": "v"}], reason="test-reason", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_delegated_admin_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import enable_delegated_admin_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await enable_delegated_admin_account(1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cis_scan_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import get_cis_scan_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await get_cis_scan_report("test-scan_arn", target_accounts=1, report_format=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cis_scan_result_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import get_cis_scan_result_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await get_cis_scan_result_details("test-scan_arn", "test-target_resource_id", 1, filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_clusters_for_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import get_clusters_for_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await get_clusters_for_image("test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_code_security_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import get_code_security_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await get_code_security_integration("test-integration_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_account_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_account_permissions(service="test-service", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cis_scan_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_cis_scan_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_cis_scan_configurations(filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cis_scan_results_aggregated_by_checks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_cis_scan_results_aggregated_by_checks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_cis_scan_results_aggregated_by_checks("test-scan_arn", filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cis_scan_results_aggregated_by_target_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_cis_scan_results_aggregated_by_target_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_cis_scan_results_aggregated_by_target_resource("test-scan_arn", filter_criteria="test-filter_criteria", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cis_scans_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_cis_scans
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_cis_scans(filter_criteria="test-filter_criteria", detail_level="test-detail_level", sort_by="test-sort_by", sort_order="test-sort_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_code_security_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_code_security_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_code_security_integrations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_code_security_scan_configuration_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_code_security_scan_configuration_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_code_security_scan_configuration_associations({}, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_code_security_scan_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_code_security_scan_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_code_security_scan_configurations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_coverage_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_coverage_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_coverage_statistics(filter_criteria="test-filter_criteria", group_by="test-group_by", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_delegated_admin_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_delegated_admin_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_delegated_admin_accounts(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_filters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_filters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_filters(arns="test-arns", action="test-action", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_usage_totals_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_usage_totals
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_usage_totals(max_results=1, next_token="test-next_token", account_ids=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_vulnerabilities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import search_vulnerabilities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await search_vulnerabilities("test-filter_criteria", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_code_security_scan_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import start_code_security_scan
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await start_code_security_scan("test-resource", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_cis_scan_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import update_cis_scan_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await update_cis_scan_configuration({}, scan_name="test-scan_name", security_level="test-security_level", schedule="test-schedule", targets="test-targets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ec2_deep_inspection_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import update_ec2_deep_inspection_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await update_ec2_deep_inspection_configuration(activate_deep_inspection=True, package_paths="test-package_paths", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import update_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await update_filter("test-filter_arn", action="test-action", description="test-description", filter_criteria="test-filter_criteria", name="test-name", reason="test-reason", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_list_coverage_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_coverage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: mock_client)
    await list_coverage(filter_criteria="test-filter_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import enable
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: m)
    await enable(["EC2"], account_ids=["123"], client_token="tok", region_name="us-east-1")

@pytest.mark.asyncio
async def test_list_findings_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_findings
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: m)
    await list_findings(filter_criteria={"severity": "HIGH"}, sort_criteria={"field": "SEVERITY"}, region_name="us-east-1")

@pytest.mark.asyncio
async def test_list_finding_aggregations_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.inspector import list_finding_aggregations
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.inspector.async_client", lambda *a, **kw: m)
    await list_finding_aggregations("FINDING_TYPE", aggregation_request={"findingTypeAggregation": {}}, region_name="us-east-1")
