"""Tests for aws_util.aio.macie -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.macie import (
    BucketInfo,
    BucketStatistics,
    ClassificationJobResult,
    FindingResult,
    FindingsFilterResult,
    MacieSessionResult,
    cancel_classification_job,
    create_classification_job,
    create_findings_filter,
    delete_findings_filter,
    describe_buckets,
    describe_classification_job,
    disable_macie,
    enable_macie,
    get_bucket_statistics,
    get_findings,
    get_findings_filter,
    get_macie_session,
    list_classification_jobs,
    list_findings,
    list_findings_filters,
    update_classification_job,
    update_findings_filter,
    update_macie_session,
    accept_invitation,
    batch_get_custom_data_identifiers,
    batch_update_automated_discovery_accounts,
    create_allow_list,
    create_custom_data_identifier,
    create_invitations,
    create_member,
    create_sample_findings,
    decline_invitations,
    delete_allow_list,
    delete_custom_data_identifier,
    delete_invitations,
    delete_member,
    describe_organization_configuration,
    disable_organization_admin_account,
    disassociate_from_administrator_account,
    disassociate_from_master_account,
    disassociate_member,
    enable_organization_admin_account,
    get_administrator_account,
    get_allow_list,
    get_automated_discovery_configuration,
    get_classification_export_configuration,
    get_classification_scope,
    get_custom_data_identifier,
    get_finding_statistics,
    get_findings_publication_configuration,
    get_invitations_count,
    get_master_account,
    get_member,
    get_resource_profile,
    get_reveal_configuration,
    get_sensitive_data_occurrences,
    get_sensitive_data_occurrences_availability,
    get_sensitivity_inspection_template,
    get_usage_statistics,
    get_usage_totals,
    list_allow_lists,
    list_automated_discovery_accounts,
    list_classification_scopes,
    list_custom_data_identifiers,
    list_invitations,
    list_managed_data_identifiers,
    list_members,
    list_organization_admin_accounts,
    list_resource_profile_artifacts,
    list_resource_profile_detections,
    list_sensitivity_inspection_templates,
    list_tags_for_resource,
    put_classification_export_configuration,
    put_findings_publication_configuration,
    run_custom_data_identifier,
    search_resources,
    tag_resource,
    untag_resource,
    update_allow_list,
    update_automated_discovery_configuration,
    update_classification_scope,
    update_member_session,
    update_organization_configuration,
    update_resource_profile,
    update_resource_profile_detections,
    update_reveal_configuration,
    update_sensitivity_inspection_template,
)

_PATCH = "aws_util.aio.macie.async_client"


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------


async def test_enable_macie_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await enable_macie()
    mc.call.assert_awaited_once()


async def test_enable_macie_with_token(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await enable_macie(client_token="tok")


async def test_enable_macie_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="enable_macie failed"):
        await enable_macie()


async def test_disable_macie_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await disable_macie()


async def test_disable_macie_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="disable_macie failed"):
        await disable_macie()


async def test_get_macie_session_ok(monkeypatch):
    mc = _mc({"status": "ENABLED", "serviceRole": "arn:role"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_macie_session()
    assert r.status == "ENABLED"


async def test_get_macie_session_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_macie_session failed"):
        await get_macie_session()


async def test_update_macie_session_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await update_macie_session(
        finding_publishing_frequency="ONE_HOUR", status="PAUSED",
    )


async def test_update_macie_session_no_opts(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await update_macie_session()


async def test_update_macie_session_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="update_macie_session failed"):
        await update_macie_session()


# ---------------------------------------------------------------------------
# Classification jobs
# ---------------------------------------------------------------------------


async def test_create_classification_job_ok(monkeypatch):
    mc = _mc({"jobId": "j1", "jobArn": "arn:j1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_classification_job(
        "test", "ONE_TIME", s3_job_definition={"buckets": []},
    )
    assert r.job_id == "j1"


async def test_create_classification_job_with_opts(monkeypatch):
    mc = _mc({"jobId": "j1", "jobArn": "arn:j1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_classification_job(
        "test", "ONE_TIME", s3_job_definition={"buckets": []},
        client_token="tok", description="desc",
        tags={"env": "test"},
    )
    assert r.job_id == "j1"


async def test_create_classification_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_classification_job"):
        await create_classification_job(
            "test", "ONE_TIME", s3_job_definition={},
        )


async def test_describe_classification_job_ok(monkeypatch):
    mc = _mc({"jobId": "j1", "jobStatus": "RUNNING"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_classification_job("j1")
    assert r.job_id == "j1"


async def test_describe_classification_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_classification_job"):
        await describe_classification_job("j1")


async def test_list_classification_jobs_ok(monkeypatch):
    mc = _mc({"items": [{"jobId": "j1", "jobStatus": "RUNNING"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_classification_jobs()
    assert len(r) == 1


async def test_list_classification_jobs_with_opts(monkeypatch):
    mc = _mc({"items": [{"jobId": "j1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_classification_jobs(
        filter_criteria={"k": "v"},
        sort_criteria={"s": "ASC"},
        max_results=10,
    )
    assert len(r) == 1


async def test_list_classification_jobs_pagination(monkeypatch):
    page1 = {"items": [{"jobId": "j1"}], "nextToken": "tok"}
    page2 = {"items": [{"jobId": "j2"}]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_classification_jobs()
    assert len(r) == 2


async def test_list_classification_jobs_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_classification_jobs"):
        await list_classification_jobs()


async def test_update_classification_job_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await update_classification_job("j1", job_status="USER_PAUSED")


async def test_update_classification_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="update_classification_job"):
        await update_classification_job("j1", job_status="USER_PAUSED")


async def test_cancel_classification_job_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await cancel_classification_job("j1")


async def test_cancel_classification_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="cancel_classification_job"):
        await cancel_classification_job("j1")


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


async def test_list_findings_ok(monkeypatch):
    mc = _mc({"findingIds": ["f1", "f2"]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings()
    assert r == ["f1", "f2"]


async def test_list_findings_with_opts(monkeypatch):
    mc = _mc({"findingIds": ["f1"]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings(
        finding_criteria={"k": "v"},
        sort_criteria={"s": "ASC"},
        max_results=5,
    )
    assert r == ["f1"]


async def test_list_findings_pagination(monkeypatch):
    page1 = {"findingIds": ["f1"], "nextToken": "tok"}
    page2 = {"findingIds": ["f2"]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings()
    assert r == ["f1", "f2"]


async def test_list_findings_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_findings failed"):
        await list_findings()


async def test_get_findings_ok(monkeypatch):
    mc = _mc({
        "findings": [
            {"id": "f1", "type": "SensitiveData", "severity": {"score": 3}},
        ],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_findings(["f1"])
    assert len(r) == 1
    assert r[0].finding_id == "f1"


async def test_get_findings_with_sort(monkeypatch):
    mc = _mc({"findings": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_findings(["f1"], sort_criteria={"s": "ASC"})
    assert r == []


async def test_get_findings_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_findings failed"):
        await get_findings(["f1"])


# ---------------------------------------------------------------------------
# Findings filters
# ---------------------------------------------------------------------------


async def test_list_findings_filters_ok(monkeypatch):
    mc = _mc({
        "findingsFilterListItems": [
            {"id": "ff1", "name": "filter1", "action": "ARCHIVE", "arn": "a1"},
        ],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings_filters()
    assert len(r) == 1
    assert r[0].filter_id == "ff1"


async def test_list_findings_filters_with_max(monkeypatch):
    mc = _mc({"findingsFilterListItems": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings_filters(max_results=5)
    assert r == []


async def test_list_findings_filters_pagination(monkeypatch):
    page1 = {
        "findingsFilterListItems": [{"id": "ff1", "name": "f"}],
        "nextToken": "tok",
    }
    page2 = {"findingsFilterListItems": [{"id": "ff2", "name": "g"}]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_findings_filters()
    assert len(r) == 2


async def test_list_findings_filters_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_findings_filters"):
        await list_findings_filters()


async def test_create_findings_filter_ok(monkeypatch):
    mc = _mc({"id": "ff1", "arn": "arn:ff1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_findings_filter(
        "f1", "ARCHIVE", finding_criteria={"k": "v"},
    )
    assert r.filter_id == "ff1"


async def test_create_findings_filter_with_opts(monkeypatch):
    mc = _mc({"id": "ff1", "arn": "arn:ff1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_findings_filter(
        "f1", "ARCHIVE", finding_criteria={"k": "v"},
        description="desc", client_token="tok",
        tags={"env": "test"},
    )
    assert r.filter_id == "ff1"


async def test_create_findings_filter_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_findings_filter"):
        await create_findings_filter(
            "f1", "ARCHIVE", finding_criteria={},
        )


async def test_get_findings_filter_ok(monkeypatch):
    mc = _mc({
        "id": "ff1", "name": "f1", "action": "ARCHIVE", "arn": "a1",
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_findings_filter("ff1")
    assert r.name == "f1"


async def test_get_findings_filter_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_findings_filter"):
        await get_findings_filter("ff1")


async def test_update_findings_filter_ok(monkeypatch):
    mc = _mc({"id": "ff1", "arn": "a1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await update_findings_filter(
        "ff1", name="new", action="NOOP",
        finding_criteria={"k": "v"}, description="new desc",
    )
    assert r.filter_id == "ff1"


async def test_update_findings_filter_minimal(monkeypatch):
    mc = _mc({"id": "ff1", "arn": "a1"})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await update_findings_filter("ff1")
    assert r.filter_id == "ff1"


async def test_update_findings_filter_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="update_findings_filter"):
        await update_findings_filter("ff1")


async def test_delete_findings_filter_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_findings_filter("ff1")


async def test_delete_findings_filter_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_findings_filter"):
        await delete_findings_filter("ff1")


# ---------------------------------------------------------------------------
# S3 bucket analysis
# ---------------------------------------------------------------------------


async def test_describe_buckets_ok(monkeypatch):
    mc = _mc({
        "buckets": [{"bucketName": "b1", "accountId": "123"}],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_buckets()
    assert len(r) == 1
    assert r[0].bucket_name == "b1"


async def test_describe_buckets_with_opts(monkeypatch):
    mc = _mc({"buckets": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_buckets(
        criteria={"k": "v"},
        sort_criteria={"s": "ASC"},
        max_results=5,
    )
    assert r == []


async def test_describe_buckets_pagination(monkeypatch):
    page1 = {"buckets": [{"bucketName": "b1"}], "nextToken": "tok"}
    page2 = {"buckets": [{"bucketName": "b2"}]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_buckets()
    assert len(r) == 2


async def test_describe_buckets_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_buckets failed"):
        await describe_buckets()


async def test_get_bucket_statistics_ok(monkeypatch):
    mc = _mc({
        "bucketsCount": 5,
        "classifiableObjectCount": 100,
        "classifiableSizeInBytes": 2048,
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_bucket_statistics()
    assert r.buckets_count == 5


async def test_get_bucket_statistics_with_account(monkeypatch):
    mc = _mc({"bucketsCount": 1})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_bucket_statistics(account_id="123")
    assert r.buckets_count == 1


async def test_get_bucket_statistics_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_bucket_statistics failed"):
        await get_bucket_statistics()


async def test_accept_invitation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_invitation("test-invitation_id", )
    mock_client.call.assert_called_once()


async def test_accept_invitation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_invitation("test-invitation_id", )


async def test_batch_get_custom_data_identifiers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_custom_data_identifiers()
    mock_client.call.assert_called_once()


async def test_batch_get_custom_data_identifiers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_custom_data_identifiers()


async def test_batch_update_automated_discovery_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_automated_discovery_accounts()
    mock_client.call.assert_called_once()


async def test_batch_update_automated_discovery_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_automated_discovery_accounts()


async def test_create_allow_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_allow_list("test-client_token", {}, "test-name", )
    mock_client.call.assert_called_once()


async def test_create_allow_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_allow_list("test-client_token", {}, "test-name", )


async def test_create_custom_data_identifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_data_identifier("test-name", "test-regex", )
    mock_client.call.assert_called_once()


async def test_create_custom_data_identifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_data_identifier("test-name", "test-regex", )


async def test_create_invitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_invitations([], )
    mock_client.call.assert_called_once()


async def test_create_invitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_invitations([], )


async def test_create_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_member({}, )
    mock_client.call.assert_called_once()


async def test_create_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_member({}, )


async def test_create_sample_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_sample_findings()
    mock_client.call.assert_called_once()


async def test_create_sample_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_sample_findings()


async def test_decline_invitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await decline_invitations([], )
    mock_client.call.assert_called_once()


async def test_decline_invitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await decline_invitations([], )


async def test_delete_allow_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_allow_list("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_allow_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_allow_list("test-id", )


async def test_delete_custom_data_identifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_data_identifier("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_custom_data_identifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_data_identifier("test-id", )


async def test_delete_invitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_invitations([], )
    mock_client.call.assert_called_once()


async def test_delete_invitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_invitations([], )


async def test_delete_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_member("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_member("test-id", )


async def test_describe_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_organization_configuration()
    mock_client.call.assert_called_once()


async def test_describe_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_configuration()


async def test_disable_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_organization_admin_account("test-admin_account_id", )
    mock_client.call.assert_called_once()


async def test_disable_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_organization_admin_account("test-admin_account_id", )


async def test_disassociate_from_administrator_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_from_administrator_account()
    mock_client.call.assert_called_once()


async def test_disassociate_from_administrator_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_from_administrator_account()


async def test_disassociate_from_master_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_from_master_account()
    mock_client.call.assert_called_once()


async def test_disassociate_from_master_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_from_master_account()


async def test_disassociate_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_member("test-id", )
    mock_client.call.assert_called_once()


async def test_disassociate_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_member("test-id", )


async def test_enable_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_organization_admin_account("test-admin_account_id", )
    mock_client.call.assert_called_once()


async def test_enable_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_organization_admin_account("test-admin_account_id", )


async def test_get_administrator_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_administrator_account()
    mock_client.call.assert_called_once()


async def test_get_administrator_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_administrator_account()


async def test_get_allow_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_allow_list("test-id", )
    mock_client.call.assert_called_once()


async def test_get_allow_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_allow_list("test-id", )


async def test_get_automated_discovery_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_automated_discovery_configuration()
    mock_client.call.assert_called_once()


async def test_get_automated_discovery_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_automated_discovery_configuration()


async def test_get_classification_export_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_classification_export_configuration()
    mock_client.call.assert_called_once()


async def test_get_classification_export_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_classification_export_configuration()


async def test_get_classification_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_classification_scope("test-id", )
    mock_client.call.assert_called_once()


async def test_get_classification_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_classification_scope("test-id", )


async def test_get_custom_data_identifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_custom_data_identifier("test-id", )
    mock_client.call.assert_called_once()


async def test_get_custom_data_identifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_data_identifier("test-id", )


async def test_get_finding_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_finding_statistics("test-group_by", )
    mock_client.call.assert_called_once()


async def test_get_finding_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_statistics("test-group_by", )


async def test_get_findings_publication_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_findings_publication_configuration()
    mock_client.call.assert_called_once()


async def test_get_findings_publication_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_findings_publication_configuration()


async def test_get_invitations_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_invitations_count()
    mock_client.call.assert_called_once()


async def test_get_invitations_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_invitations_count()


async def test_get_master_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_master_account()
    mock_client.call.assert_called_once()


async def test_get_master_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_master_account()


async def test_get_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_member("test-id", )
    mock_client.call.assert_called_once()


async def test_get_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_member("test-id", )


async def test_get_resource_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_profile("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_profile("test-resource_arn", )


async def test_get_reveal_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reveal_configuration()
    mock_client.call.assert_called_once()


async def test_get_reveal_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reveal_configuration()


async def test_get_sensitive_data_occurrences(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sensitive_data_occurrences("test-finding_id", )
    mock_client.call.assert_called_once()


async def test_get_sensitive_data_occurrences_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sensitive_data_occurrences("test-finding_id", )


async def test_get_sensitive_data_occurrences_availability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sensitive_data_occurrences_availability("test-finding_id", )
    mock_client.call.assert_called_once()


async def test_get_sensitive_data_occurrences_availability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sensitive_data_occurrences_availability("test-finding_id", )


async def test_get_sensitivity_inspection_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sensitivity_inspection_template("test-id", )
    mock_client.call.assert_called_once()


async def test_get_sensitivity_inspection_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sensitivity_inspection_template("test-id", )


async def test_get_usage_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_usage_statistics()
    mock_client.call.assert_called_once()


async def test_get_usage_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_usage_statistics()


async def test_get_usage_totals(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_usage_totals()
    mock_client.call.assert_called_once()


async def test_get_usage_totals_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_usage_totals()


async def test_list_allow_lists(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_allow_lists()
    mock_client.call.assert_called_once()


async def test_list_allow_lists_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_allow_lists()


async def test_list_automated_discovery_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_automated_discovery_accounts()
    mock_client.call.assert_called_once()


async def test_list_automated_discovery_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_automated_discovery_accounts()


async def test_list_classification_scopes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_classification_scopes()
    mock_client.call.assert_called_once()


async def test_list_classification_scopes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_classification_scopes()


async def test_list_custom_data_identifiers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_data_identifiers()
    mock_client.call.assert_called_once()


async def test_list_custom_data_identifiers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_data_identifiers()


async def test_list_invitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_invitations()
    mock_client.call.assert_called_once()


async def test_list_invitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_invitations()


async def test_list_managed_data_identifiers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_managed_data_identifiers()
    mock_client.call.assert_called_once()


async def test_list_managed_data_identifiers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_managed_data_identifiers()


async def test_list_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_members()
    mock_client.call.assert_called_once()


async def test_list_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_members()


async def test_list_organization_admin_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_organization_admin_accounts()
    mock_client.call.assert_called_once()


async def test_list_organization_admin_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_organization_admin_accounts()


async def test_list_resource_profile_artifacts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_profile_artifacts("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_resource_profile_artifacts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_profile_artifacts("test-resource_arn", )


async def test_list_resource_profile_detections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_profile_detections("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_resource_profile_detections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_profile_detections("test-resource_arn", )


async def test_list_sensitivity_inspection_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sensitivity_inspection_templates()
    mock_client.call.assert_called_once()


async def test_list_sensitivity_inspection_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sensitivity_inspection_templates()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_classification_export_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_classification_export_configuration({}, )
    mock_client.call.assert_called_once()


async def test_put_classification_export_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_classification_export_configuration({}, )


async def test_put_findings_publication_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_findings_publication_configuration()
    mock_client.call.assert_called_once()


async def test_put_findings_publication_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_findings_publication_configuration()


async def test_run_custom_data_identifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_custom_data_identifier("test-regex", "test-sample_text", )
    mock_client.call.assert_called_once()


async def test_run_custom_data_identifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_custom_data_identifier("test-regex", "test-sample_text", )


async def test_search_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_resources()
    mock_client.call.assert_called_once()


async def test_search_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_resources()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_allow_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_allow_list({}, "test-id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_allow_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_allow_list({}, "test-id", "test-name", )


async def test_update_automated_discovery_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_automated_discovery_configuration("test-status", )
    mock_client.call.assert_called_once()


async def test_update_automated_discovery_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_automated_discovery_configuration("test-status", )


async def test_update_classification_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_classification_scope("test-id", )
    mock_client.call.assert_called_once()


async def test_update_classification_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_classification_scope("test-id", )


async def test_update_member_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_member_session("test-id", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_member_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_member_session("test-id", "test-status", )


async def test_update_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_organization_configuration(True, )
    mock_client.call.assert_called_once()


async def test_update_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_organization_configuration(True, )


async def test_update_resource_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_profile("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_update_resource_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_profile("test-resource_arn", )


async def test_update_resource_profile_detections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_profile_detections("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_update_resource_profile_detections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_profile_detections("test-resource_arn", )


async def test_update_reveal_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_reveal_configuration({}, )
    mock_client.call.assert_called_once()


async def test_update_reveal_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_reveal_configuration({}, )


async def test_update_sensitivity_inspection_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_sensitivity_inspection_template("test-id", )
    mock_client.call.assert_called_once()


async def test_update_sensitivity_inspection_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.macie.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_sensitivity_inspection_template("test-id", )


@pytest.mark.asyncio
async def test_update_macie_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_macie_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_macie_session(finding_publishing_frequency="test-finding_publishing_frequency", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_classification_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_classification_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_classification_jobs(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_findings(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_findings_filters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_findings_filters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_findings_filters(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_findings_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_findings_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_findings_filter("test-filter_id", name="test-name", action="test-action", finding_criteria="test-finding_criteria", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_buckets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import describe_buckets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await describe_buckets(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_accept_invitation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import accept_invitation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await accept_invitation("test-invitation_id", administrator_account_id=1, master_account=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_custom_data_identifiers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import batch_get_custom_data_identifiers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await batch_get_custom_data_identifiers(ids="test-ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_update_automated_discovery_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import batch_update_automated_discovery_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await batch_update_automated_discovery_accounts(accounts=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_allow_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import create_allow_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await create_allow_list("test-client_token", "test-criteria", "test-name", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_data_identifier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import create_custom_data_identifier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await create_custom_data_identifier("test-name", "test-regex", client_token="test-client_token", description="test-description", ignore_words="test-ignore_words", keywords="test-keywords", maximum_match_distance=1, severity_levels="test-severity_levels", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_invitations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import create_invitations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await create_invitations(1, disable_email_notification=True, message="test-message", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_member_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import create_member
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await create_member(1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_sample_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import create_sample_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await create_sample_findings(finding_types="test-finding_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_allow_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import delete_allow_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await delete_allow_list("test-id", ignore_job_checks="test-ignore_job_checks", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import enable_organization_admin_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await enable_organization_admin_account(1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_finding_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import get_finding_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await get_finding_statistics("test-group_by", finding_criteria="test-finding_criteria", size=1, sort_criteria="test-sort_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_usage_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import get_usage_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await get_usage_statistics(filter_by="test-filter_by", max_results=1, next_token="test-next_token", sort_by="test-sort_by", time_range="test-time_range", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_usage_totals_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import get_usage_totals
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await get_usage_totals(time_range="test-time_range", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_allow_lists_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_allow_lists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_allow_lists(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_automated_discovery_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_automated_discovery_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_automated_discovery_accounts(account_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_classification_scopes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_classification_scopes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_classification_scopes(name="test-name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_data_identifiers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_custom_data_identifiers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_custom_data_identifiers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_invitations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_invitations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_managed_data_identifiers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_managed_data_identifiers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_managed_data_identifiers(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_members(max_results=1, next_token="test-next_token", only_associated="test-only_associated", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_organization_admin_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_organization_admin_accounts(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_profile_artifacts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_resource_profile_artifacts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_resource_profile_artifacts("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_profile_detections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_resource_profile_detections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_resource_profile_detections("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sensitivity_inspection_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import list_sensitivity_inspection_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await list_sensitivity_inspection_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_findings_publication_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import put_findings_publication_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await put_findings_publication_configuration(client_token="test-client_token", security_hub_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_custom_data_identifier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import run_custom_data_identifier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await run_custom_data_identifier("test-regex", "test-sample_text", ignore_words="test-ignore_words", keywords="test-keywords", maximum_match_distance=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import search_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await search_resources(bucket_criteria="test-bucket_criteria", max_results=1, next_token="test-next_token", sort_criteria="test-sort_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_allow_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_allow_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_allow_list("test-criteria", "test-id", "test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_automated_discovery_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_automated_discovery_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_automated_discovery_configuration("test-status", auto_enable_organization_members=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_classification_scope_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_classification_scope
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_classification_scope("test-id", s3="test-s3", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_resource_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_resource_profile("test-resource_arn", sensitivity_score_override="test-sensitivity_score_override", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_profile_detections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_resource_profile_detections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_resource_profile_detections("test-resource_arn", suppress_data_identifiers="test-suppress_data_identifiers", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_reveal_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_reveal_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_reveal_configuration({}, retrieval_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_sensitivity_inspection_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.macie import update_sensitivity_inspection_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.macie.async_client", lambda *a, **kw: mock_client)
    await update_sensitivity_inspection_template("test-id", description="test-description", excludes="test-excludes", includes=True, region_name="us-east-1")
    mock_client.call.assert_called_once()
