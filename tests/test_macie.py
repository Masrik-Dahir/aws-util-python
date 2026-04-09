"""Tests for aws_util.macie -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.macie import (
    BucketInfo,
    BucketStatistics,
    ClassificationJobResult,
    FindingResult,
    FindingsFilterResult,
    MacieSessionResult,
    _parse_bucket_info,
    _parse_classification_job,
    _parse_finding,
    _parse_session,
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


def _client_error(code: str = "ValidationException") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": "boom"}}, "Op"
    )


# ---------------------------------------------------------------------------
# Parser unit tests
# ---------------------------------------------------------------------------


def test_parse_session(monkeypatch):
    s = _parse_session({
        "createdAt": "2024-01-01",
        "findingPublishingFrequency": "ONE_HOUR",
        "serviceRole": "arn:role",
        "status": "ENABLED",
        "updatedAt": "2024-06-01",
        "ResponseMetadata": {},
        "extra": 1,
    })
    assert isinstance(s, MacieSessionResult)
    assert s.status == "ENABLED"
    assert s.extra == {"extra": 1}


def test_parse_classification_job():
    j = _parse_classification_job({
        "jobId": "j1",
        "name": "my-job",
        "jobType": "ONE_TIME",
        "jobStatus": "RUNNING",
        "createdAt": "2024-01-01",
        "bucketDefinitions": [{"accountId": "111"}],
        "ResponseMetadata": {},
        "extra": 1,
    })
    assert isinstance(j, ClassificationJobResult)
    assert j.job_id == "j1"
    assert j.extra == {"extra": 1}


def test_parse_classification_job_no_created_at():
    j = _parse_classification_job({"jobId": "j1"})
    assert j.created_at is None


def test_parse_finding():
    f = _parse_finding({
        "id": "f1",
        "type": "SensitiveData",
        "severity": {"score": 3},
        "title": "title",
        "description": "desc",
        "accountId": "111",
        "region": "us-east-1",
        "extra": True,
    })
    assert isinstance(f, FindingResult)
    assert f.finding_id == "f1"
    assert f.severity_score == 3
    assert f.extra == {"extra": True}


def test_parse_finding_no_severity():
    f = _parse_finding({"id": "f1"})
    assert f.severity_score == 0


def test_parse_bucket_info():
    b = _parse_bucket_info({
        "bucketName": "my-bucket",
        "accountId": "111",
        "classifiableObjectCount": 10,
        "classifiableSizeInBytes": 1024,
        "extra": "x",
    })
    assert isinstance(b, BucketInfo)
    assert b.bucket_name == "my-bucket"
    assert b.extra == {"extra": "x"}


# ---------------------------------------------------------------------------
# enable_macie / disable_macie
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_enable_macie(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    enable_macie()
    client.enable_macie.assert_called_once()


@patch("aws_util.macie.get_client")
def test_enable_macie_error(mock_gc):
    client = MagicMock()
    client.enable_macie.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="enable_macie failed"):
        enable_macie()


@patch("aws_util.macie.get_client")
def test_disable_macie(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    disable_macie()
    client.disable_macie.assert_called_once()


@patch("aws_util.macie.get_client")
def test_disable_macie_error(mock_gc):
    client = MagicMock()
    client.disable_macie.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        disable_macie()


# ---------------------------------------------------------------------------
# get_macie_session / update_macie_session
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_get_macie_session(mock_gc):
    client = MagicMock()
    client.get_macie_session.return_value = {
        "status": "ENABLED",
        "findingPublishingFrequency": "FIFTEEN_MINUTES",
        "serviceRole": "arn:role",
    }
    mock_gc.return_value = client
    result = get_macie_session()
    assert isinstance(result, MacieSessionResult)
    assert result.status == "ENABLED"


@patch("aws_util.macie.get_client")
def test_get_macie_session_error(mock_gc):
    client = MagicMock()
    client.get_macie_session.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_macie_session()


@patch("aws_util.macie.get_client")
def test_update_macie_session(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    update_macie_session(
        finding_publishing_frequency="ONE_HOUR",
        status="PAUSED",
    )
    call_kwargs = client.update_macie_session.call_args[1]
    assert call_kwargs["findingPublishingFrequency"] == "ONE_HOUR"
    assert call_kwargs["status"] == "PAUSED"


@patch("aws_util.macie.get_client")
def test_update_macie_session_error(mock_gc):
    client = MagicMock()
    client.update_macie_session.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_macie_session()


# ---------------------------------------------------------------------------
# Classification jobs
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_create_classification_job(mock_gc):
    client = MagicMock()
    client.create_classification_job.return_value = {
        "jobId": "j1",
        "jobArn": "arn:job",
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = create_classification_job(
        "my-job", "ONE_TIME", s3_job_definition={"bucketDefinitions": []},
    )
    assert isinstance(result, ClassificationJobResult)
    assert result.job_id == "j1"


@patch("aws_util.macie.get_client")
def test_create_classification_job_error(mock_gc):
    client = MagicMock()
    client.create_classification_job.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_classification_job("j", "ONE_TIME", s3_job_definition={})


@patch("aws_util.macie.get_client")
def test_describe_classification_job(mock_gc):
    client = MagicMock()
    client.describe_classification_job.return_value = {
        "jobId": "j1",
        "name": "my-job",
        "jobType": "ONE_TIME",
        "jobStatus": "RUNNING",
    }
    mock_gc.return_value = client
    result = describe_classification_job("j1")
    assert isinstance(result, ClassificationJobResult)
    assert result.job_id == "j1"


@patch("aws_util.macie.get_client")
def test_describe_classification_job_error(mock_gc):
    client = MagicMock()
    client.describe_classification_job.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_classification_job("j1")


@patch("aws_util.macie.get_client")
def test_list_classification_jobs(mock_gc):
    client = MagicMock()
    client.list_classification_jobs.return_value = {
        "items": [{"jobId": "j1", "name": "job", "jobType": "ONE_TIME", "jobStatus": "COMPLETE"}],
    }
    mock_gc.return_value = client
    result = list_classification_jobs()
    assert len(result) == 1


@patch("aws_util.macie.get_client")
def test_list_classification_jobs_pagination(mock_gc):
    client = MagicMock()
    client.list_classification_jobs.side_effect = [
        {"items": [{"jobId": "j1"}], "nextToken": "tok"},
        {"items": [{"jobId": "j2"}]},
    ]
    mock_gc.return_value = client
    result = list_classification_jobs()
    assert len(result) == 2


@patch("aws_util.macie.get_client")
def test_list_classification_jobs_error(mock_gc):
    client = MagicMock()
    client.list_classification_jobs.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_classification_jobs()


@patch("aws_util.macie.get_client")
def test_update_classification_job(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    update_classification_job("j1", job_status="USER_PAUSED")
    client.update_classification_job.assert_called_once_with(
        jobId="j1", jobStatus="USER_PAUSED"
    )


@patch("aws_util.macie.get_client")
def test_update_classification_job_error(mock_gc):
    client = MagicMock()
    client.update_classification_job.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_classification_job("j1", job_status="USER_PAUSED")


@patch("aws_util.macie.get_client")
def test_cancel_classification_job(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    cancel_classification_job("j1")
    client.update_classification_job.assert_called_once_with(
        jobId="j1", jobStatus="CANCELLED"
    )


@patch("aws_util.macie.get_client")
def test_cancel_classification_job_error(mock_gc):
    client = MagicMock()
    client.update_classification_job.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        cancel_classification_job("j1")


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_list_findings(mock_gc):
    client = MagicMock()
    client.list_findings.return_value = {"findingIds": ["f1", "f2"]}
    mock_gc.return_value = client
    result = list_findings()
    assert result == ["f1", "f2"]


@patch("aws_util.macie.get_client")
def test_list_findings_pagination(mock_gc):
    client = MagicMock()
    client.list_findings.side_effect = [
        {"findingIds": ["f1"], "nextToken": "tok"},
        {"findingIds": ["f2"]},
    ]
    mock_gc.return_value = client
    result = list_findings()
    assert result == ["f1", "f2"]


@patch("aws_util.macie.get_client")
def test_list_findings_error(mock_gc):
    client = MagicMock()
    client.list_findings.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_findings()


@patch("aws_util.macie.get_client")
def test_get_findings(mock_gc):
    client = MagicMock()
    client.get_findings.return_value = {
        "findings": [{"id": "f1", "type": "t", "severity": {"score": 2}, "title": "t", "description": "d", "accountId": "111", "region": "us-east-1"}],
    }
    mock_gc.return_value = client
    result = get_findings(["f1"])
    assert len(result) == 1
    assert isinstance(result[0], FindingResult)


@patch("aws_util.macie.get_client")
def test_get_findings_with_sort(mock_gc):
    client = MagicMock()
    client.get_findings.return_value = {"findings": []}
    mock_gc.return_value = client
    get_findings(["f1"], sort_criteria={"attributeName": "severity"})
    call_kwargs = client.get_findings.call_args[1]
    assert "sortCriteria" in call_kwargs


@patch("aws_util.macie.get_client")
def test_get_findings_error(mock_gc):
    client = MagicMock()
    client.get_findings.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_findings(["f1"])


# ---------------------------------------------------------------------------
# Findings filters
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_list_findings_filters(mock_gc):
    client = MagicMock()
    client.list_findings_filters.return_value = {
        "findingsFilterListItems": [
            {"id": "ff1", "name": "filter1", "action": "ARCHIVE", "arn": "arn:ff1"},
        ],
    }
    mock_gc.return_value = client
    result = list_findings_filters()
    assert len(result) == 1
    assert isinstance(result[0], FindingsFilterResult)


@patch("aws_util.macie.get_client")
def test_list_findings_filters_pagination(mock_gc):
    client = MagicMock()
    client.list_findings_filters.side_effect = [
        {"findingsFilterListItems": [{"id": "ff1", "name": "f1", "action": "ARCHIVE", "arn": "a1"}], "nextToken": "tok"},
        {"findingsFilterListItems": [{"id": "ff2", "name": "f2", "action": "NOOP", "arn": "a2"}]},
    ]
    mock_gc.return_value = client
    result = list_findings_filters(max_results=1)
    assert len(result) == 2


@patch("aws_util.macie.get_client")
def test_list_findings_filters_error(mock_gc):
    client = MagicMock()
    client.list_findings_filters.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_findings_filters()


@patch("aws_util.macie.get_client")
def test_create_findings_filter(mock_gc):
    client = MagicMock()
    client.create_findings_filter.return_value = {
        "id": "ff1",
        "arn": "arn:ff1",
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = create_findings_filter(
        "my-filter", "ARCHIVE", finding_criteria={"criterion": {}},
    )
    assert isinstance(result, FindingsFilterResult)
    assert result.filter_id == "ff1"


@patch("aws_util.macie.get_client")
def test_create_findings_filter_error(mock_gc):
    client = MagicMock()
    client.create_findings_filter.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_findings_filter("f", "ARCHIVE", finding_criteria={})


@patch("aws_util.macie.get_client")
def test_get_findings_filter(mock_gc):
    client = MagicMock()
    client.get_findings_filter.return_value = {
        "id": "ff1",
        "name": "my-filter",
        "action": "ARCHIVE",
        "arn": "arn:ff1",
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_findings_filter("ff1")
    assert isinstance(result, FindingsFilterResult)
    assert result.name == "my-filter"


@patch("aws_util.macie.get_client")
def test_get_findings_filter_error(mock_gc):
    client = MagicMock()
    client.get_findings_filter.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_findings_filter("ff1")


@patch("aws_util.macie.get_client")
def test_update_findings_filter(mock_gc):
    client = MagicMock()
    client.update_findings_filter.return_value = {
        "id": "ff1",
        "arn": "arn:ff1",
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = update_findings_filter(
        "ff1",
        name="new-name",
        action="NOOP",
        finding_criteria={"criterion": {}},
        description="desc",
    )
    assert isinstance(result, FindingsFilterResult)


@patch("aws_util.macie.get_client")
def test_update_findings_filter_error(mock_gc):
    client = MagicMock()
    client.update_findings_filter.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_findings_filter("ff1")


@patch("aws_util.macie.get_client")
def test_delete_findings_filter(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_findings_filter("ff1")
    client.delete_findings_filter.assert_called_once_with(id="ff1")


@patch("aws_util.macie.get_client")
def test_delete_findings_filter_error(mock_gc):
    client = MagicMock()
    client.delete_findings_filter.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_findings_filter("ff1")


# ---------------------------------------------------------------------------
# describe_buckets / get_bucket_statistics
# ---------------------------------------------------------------------------


@patch("aws_util.macie.get_client")
def test_describe_buckets(mock_gc):
    client = MagicMock()
    client.describe_buckets.return_value = {
        "buckets": [{"bucketName": "b1", "accountId": "111"}],
    }
    mock_gc.return_value = client
    result = describe_buckets()
    assert len(result) == 1
    assert isinstance(result[0], BucketInfo)


@patch("aws_util.macie.get_client")
def test_describe_buckets_pagination(mock_gc):
    client = MagicMock()
    client.describe_buckets.side_effect = [
        {"buckets": [{"bucketName": "b1"}], "nextToken": "tok"},
        {"buckets": [{"bucketName": "b2"}]},
    ]
    mock_gc.return_value = client
    result = describe_buckets()
    assert len(result) == 2


@patch("aws_util.macie.get_client")
def test_describe_buckets_error(mock_gc):
    client = MagicMock()
    client.describe_buckets.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_buckets()


@patch("aws_util.macie.get_client")
def test_get_bucket_statistics(mock_gc):
    client = MagicMock()
    client.get_bucket_statistics.return_value = {
        "bucketsCount": 5,
        "classifiableObjectCount": 100,
        "classifiableSizeInBytes": 4096,
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_bucket_statistics()
    assert isinstance(result, BucketStatistics)
    assert result.buckets_count == 5


@patch("aws_util.macie.get_client")
def test_get_bucket_statistics_with_account(mock_gc):
    client = MagicMock()
    client.get_bucket_statistics.return_value = {
        "bucketsCount": 1,
        "classifiableObjectCount": 0,
        "classifiableSizeInBytes": 0,
    }
    mock_gc.return_value = client
    get_bucket_statistics(account_id="111")
    call_kwargs = client.get_bucket_statistics.call_args[1]
    assert call_kwargs["accountId"] == "111"


@patch("aws_util.macie.get_client")
def test_get_bucket_statistics_error(mock_gc):
    client = MagicMock()
    client.get_bucket_statistics.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_bucket_statistics()


REGION = "us-east-1"


@patch("aws_util.macie.get_client")
def test_accept_invitation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.accept_invitation.return_value = {}
    accept_invitation("test-invitation_id", region_name=REGION)
    mock_client.accept_invitation.assert_called_once()


@patch("aws_util.macie.get_client")
def test_accept_invitation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.accept_invitation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_invitation",
    )
    with pytest.raises(RuntimeError, match="Failed to accept invitation"):
        accept_invitation("test-invitation_id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_batch_get_custom_data_identifiers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_custom_data_identifiers.return_value = {}
    batch_get_custom_data_identifiers(region_name=REGION)
    mock_client.batch_get_custom_data_identifiers.assert_called_once()


@patch("aws_util.macie.get_client")
def test_batch_get_custom_data_identifiers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_custom_data_identifiers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_custom_data_identifiers",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get custom data identifiers"):
        batch_get_custom_data_identifiers(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_batch_update_automated_discovery_accounts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_automated_discovery_accounts.return_value = {}
    batch_update_automated_discovery_accounts(region_name=REGION)
    mock_client.batch_update_automated_discovery_accounts.assert_called_once()


@patch("aws_util.macie.get_client")
def test_batch_update_automated_discovery_accounts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_automated_discovery_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_automated_discovery_accounts",
    )
    with pytest.raises(RuntimeError, match="Failed to batch update automated discovery accounts"):
        batch_update_automated_discovery_accounts(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_create_allow_list(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_allow_list.return_value = {}
    create_allow_list("test-client_token", {}, "test-name", region_name=REGION)
    mock_client.create_allow_list.assert_called_once()


@patch("aws_util.macie.get_client")
def test_create_allow_list_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_allow_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_allow_list",
    )
    with pytest.raises(RuntimeError, match="Failed to create allow list"):
        create_allow_list("test-client_token", {}, "test-name", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_create_custom_data_identifier(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_data_identifier.return_value = {}
    create_custom_data_identifier("test-name", "test-regex", region_name=REGION)
    mock_client.create_custom_data_identifier.assert_called_once()


@patch("aws_util.macie.get_client")
def test_create_custom_data_identifier_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_data_identifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_data_identifier",
    )
    with pytest.raises(RuntimeError, match="Failed to create custom data identifier"):
        create_custom_data_identifier("test-name", "test-regex", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_create_invitations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_invitations.return_value = {}
    create_invitations([], region_name=REGION)
    mock_client.create_invitations.assert_called_once()


@patch("aws_util.macie.get_client")
def test_create_invitations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_invitations",
    )
    with pytest.raises(RuntimeError, match="Failed to create invitations"):
        create_invitations([], region_name=REGION)


@patch("aws_util.macie.get_client")
def test_create_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_member.return_value = {}
    create_member({}, region_name=REGION)
    mock_client.create_member.assert_called_once()


@patch("aws_util.macie.get_client")
def test_create_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_member",
    )
    with pytest.raises(RuntimeError, match="Failed to create member"):
        create_member({}, region_name=REGION)


@patch("aws_util.macie.get_client")
def test_create_sample_findings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_sample_findings.return_value = {}
    create_sample_findings(region_name=REGION)
    mock_client.create_sample_findings.assert_called_once()


@patch("aws_util.macie.get_client")
def test_create_sample_findings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_sample_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_sample_findings",
    )
    with pytest.raises(RuntimeError, match="Failed to create sample findings"):
        create_sample_findings(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_decline_invitations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.decline_invitations.return_value = {}
    decline_invitations([], region_name=REGION)
    mock_client.decline_invitations.assert_called_once()


@patch("aws_util.macie.get_client")
def test_decline_invitations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.decline_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decline_invitations",
    )
    with pytest.raises(RuntimeError, match="Failed to decline invitations"):
        decline_invitations([], region_name=REGION)


@patch("aws_util.macie.get_client")
def test_delete_allow_list(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_allow_list.return_value = {}
    delete_allow_list("test-id", region_name=REGION)
    mock_client.delete_allow_list.assert_called_once()


@patch("aws_util.macie.get_client")
def test_delete_allow_list_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_allow_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_allow_list",
    )
    with pytest.raises(RuntimeError, match="Failed to delete allow list"):
        delete_allow_list("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_delete_custom_data_identifier(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_data_identifier.return_value = {}
    delete_custom_data_identifier("test-id", region_name=REGION)
    mock_client.delete_custom_data_identifier.assert_called_once()


@patch("aws_util.macie.get_client")
def test_delete_custom_data_identifier_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_data_identifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_data_identifier",
    )
    with pytest.raises(RuntimeError, match="Failed to delete custom data identifier"):
        delete_custom_data_identifier("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_delete_invitations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_invitations.return_value = {}
    delete_invitations([], region_name=REGION)
    mock_client.delete_invitations.assert_called_once()


@patch("aws_util.macie.get_client")
def test_delete_invitations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_invitations",
    )
    with pytest.raises(RuntimeError, match="Failed to delete invitations"):
        delete_invitations([], region_name=REGION)


@patch("aws_util.macie.get_client")
def test_delete_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_member.return_value = {}
    delete_member("test-id", region_name=REGION)
    mock_client.delete_member.assert_called_once()


@patch("aws_util.macie.get_client")
def test_delete_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_member",
    )
    with pytest.raises(RuntimeError, match="Failed to delete member"):
        delete_member("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_describe_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.return_value = {}
    describe_organization_configuration(region_name=REGION)
    mock_client.describe_organization_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_describe_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe organization configuration"):
        describe_organization_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_disable_organization_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_organization_admin_account.return_value = {}
    disable_organization_admin_account("test-admin_account_id", region_name=REGION)
    mock_client.disable_organization_admin_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_disable_organization_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_organization_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disable organization admin account"):
        disable_organization_admin_account("test-admin_account_id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_disassociate_from_administrator_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_from_administrator_account.return_value = {}
    disassociate_from_administrator_account(region_name=REGION)
    mock_client.disassociate_from_administrator_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_disassociate_from_administrator_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_from_administrator_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_from_administrator_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate from administrator account"):
        disassociate_from_administrator_account(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_disassociate_from_master_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_from_master_account.return_value = {}
    disassociate_from_master_account(region_name=REGION)
    mock_client.disassociate_from_master_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_disassociate_from_master_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_from_master_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_from_master_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate from master account"):
        disassociate_from_master_account(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_disassociate_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_member.return_value = {}
    disassociate_member("test-id", region_name=REGION)
    mock_client.disassociate_member.assert_called_once()


@patch("aws_util.macie.get_client")
def test_disassociate_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_member",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate member"):
        disassociate_member("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_enable_organization_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_organization_admin_account.return_value = {}
    enable_organization_admin_account("test-admin_account_id", region_name=REGION)
    mock_client.enable_organization_admin_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_enable_organization_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_organization_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to enable organization admin account"):
        enable_organization_admin_account("test-admin_account_id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_administrator_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_administrator_account.return_value = {}
    get_administrator_account(region_name=REGION)
    mock_client.get_administrator_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_administrator_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_administrator_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_administrator_account",
    )
    with pytest.raises(RuntimeError, match="Failed to get administrator account"):
        get_administrator_account(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_allow_list(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_allow_list.return_value = {}
    get_allow_list("test-id", region_name=REGION)
    mock_client.get_allow_list.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_allow_list_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_allow_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_allow_list",
    )
    with pytest.raises(RuntimeError, match="Failed to get allow list"):
        get_allow_list("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_automated_discovery_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_automated_discovery_configuration.return_value = {}
    get_automated_discovery_configuration(region_name=REGION)
    mock_client.get_automated_discovery_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_automated_discovery_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_automated_discovery_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automated_discovery_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get automated discovery configuration"):
        get_automated_discovery_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_classification_export_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_classification_export_configuration.return_value = {}
    get_classification_export_configuration(region_name=REGION)
    mock_client.get_classification_export_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_classification_export_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_classification_export_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_classification_export_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get classification export configuration"):
        get_classification_export_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_classification_scope(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_classification_scope.return_value = {}
    get_classification_scope("test-id", region_name=REGION)
    mock_client.get_classification_scope.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_classification_scope_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_classification_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_classification_scope",
    )
    with pytest.raises(RuntimeError, match="Failed to get classification scope"):
        get_classification_scope("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_custom_data_identifier(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_custom_data_identifier.return_value = {}
    get_custom_data_identifier("test-id", region_name=REGION)
    mock_client.get_custom_data_identifier.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_custom_data_identifier_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_custom_data_identifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_data_identifier",
    )
    with pytest.raises(RuntimeError, match="Failed to get custom data identifier"):
        get_custom_data_identifier("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_finding_statistics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_finding_statistics.return_value = {}
    get_finding_statistics("test-group_by", region_name=REGION)
    mock_client.get_finding_statistics.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_finding_statistics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_finding_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_statistics",
    )
    with pytest.raises(RuntimeError, match="Failed to get finding statistics"):
        get_finding_statistics("test-group_by", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_findings_publication_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_findings_publication_configuration.return_value = {}
    get_findings_publication_configuration(region_name=REGION)
    mock_client.get_findings_publication_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_findings_publication_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_findings_publication_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_findings_publication_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get findings publication configuration"):
        get_findings_publication_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_invitations_count(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_invitations_count.return_value = {}
    get_invitations_count(region_name=REGION)
    mock_client.get_invitations_count.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_invitations_count_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_invitations_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_invitations_count",
    )
    with pytest.raises(RuntimeError, match="Failed to get invitations count"):
        get_invitations_count(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_master_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_master_account.return_value = {}
    get_master_account(region_name=REGION)
    mock_client.get_master_account.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_master_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_master_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_master_account",
    )
    with pytest.raises(RuntimeError, match="Failed to get master account"):
        get_master_account(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_member.return_value = {}
    get_member("test-id", region_name=REGION)
    mock_client.get_member.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_member",
    )
    with pytest.raises(RuntimeError, match="Failed to get member"):
        get_member("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_resource_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_profile.return_value = {}
    get_resource_profile("test-resource_arn", region_name=REGION)
    mock_client.get_resource_profile.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_resource_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to get resource profile"):
        get_resource_profile("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_reveal_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_reveal_configuration.return_value = {}
    get_reveal_configuration(region_name=REGION)
    mock_client.get_reveal_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_reveal_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_reveal_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reveal_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get reveal configuration"):
        get_reveal_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_sensitive_data_occurrences(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitive_data_occurrences.return_value = {}
    get_sensitive_data_occurrences("test-finding_id", region_name=REGION)
    mock_client.get_sensitive_data_occurrences.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_sensitive_data_occurrences_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitive_data_occurrences.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sensitive_data_occurrences",
    )
    with pytest.raises(RuntimeError, match="Failed to get sensitive data occurrences"):
        get_sensitive_data_occurrences("test-finding_id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_sensitive_data_occurrences_availability(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitive_data_occurrences_availability.return_value = {}
    get_sensitive_data_occurrences_availability("test-finding_id", region_name=REGION)
    mock_client.get_sensitive_data_occurrences_availability.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_sensitive_data_occurrences_availability_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitive_data_occurrences_availability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sensitive_data_occurrences_availability",
    )
    with pytest.raises(RuntimeError, match="Failed to get sensitive data occurrences availability"):
        get_sensitive_data_occurrences_availability("test-finding_id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_sensitivity_inspection_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitivity_inspection_template.return_value = {}
    get_sensitivity_inspection_template("test-id", region_name=REGION)
    mock_client.get_sensitivity_inspection_template.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_sensitivity_inspection_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sensitivity_inspection_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sensitivity_inspection_template",
    )
    with pytest.raises(RuntimeError, match="Failed to get sensitivity inspection template"):
        get_sensitivity_inspection_template("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_usage_statistics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_usage_statistics.return_value = {}
    get_usage_statistics(region_name=REGION)
    mock_client.get_usage_statistics.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_usage_statistics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_usage_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_statistics",
    )
    with pytest.raises(RuntimeError, match="Failed to get usage statistics"):
        get_usage_statistics(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_get_usage_totals(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_usage_totals.return_value = {}
    get_usage_totals(region_name=REGION)
    mock_client.get_usage_totals.assert_called_once()


@patch("aws_util.macie.get_client")
def test_get_usage_totals_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_usage_totals.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_totals",
    )
    with pytest.raises(RuntimeError, match="Failed to get usage totals"):
        get_usage_totals(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_allow_lists(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allow_lists.return_value = {}
    list_allow_lists(region_name=REGION)
    mock_client.list_allow_lists.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_allow_lists_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allow_lists.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_allow_lists",
    )
    with pytest.raises(RuntimeError, match="Failed to list allow lists"):
        list_allow_lists(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_automated_discovery_accounts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_automated_discovery_accounts.return_value = {}
    list_automated_discovery_accounts(region_name=REGION)
    mock_client.list_automated_discovery_accounts.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_automated_discovery_accounts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_automated_discovery_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automated_discovery_accounts",
    )
    with pytest.raises(RuntimeError, match="Failed to list automated discovery accounts"):
        list_automated_discovery_accounts(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_classification_scopes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_classification_scopes.return_value = {}
    list_classification_scopes(region_name=REGION)
    mock_client.list_classification_scopes.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_classification_scopes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_classification_scopes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_classification_scopes",
    )
    with pytest.raises(RuntimeError, match="Failed to list classification scopes"):
        list_classification_scopes(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_custom_data_identifiers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_data_identifiers.return_value = {}
    list_custom_data_identifiers(region_name=REGION)
    mock_client.list_custom_data_identifiers.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_custom_data_identifiers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_data_identifiers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_data_identifiers",
    )
    with pytest.raises(RuntimeError, match="Failed to list custom data identifiers"):
        list_custom_data_identifiers(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_invitations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_invitations.return_value = {}
    list_invitations(region_name=REGION)
    mock_client.list_invitations.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_invitations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_invitations",
    )
    with pytest.raises(RuntimeError, match="Failed to list invitations"):
        list_invitations(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_managed_data_identifiers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_data_identifiers.return_value = {}
    list_managed_data_identifiers(region_name=REGION)
    mock_client.list_managed_data_identifiers.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_managed_data_identifiers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_data_identifiers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_managed_data_identifiers",
    )
    with pytest.raises(RuntimeError, match="Failed to list managed data identifiers"):
        list_managed_data_identifiers(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_members(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_members.return_value = {}
    list_members(region_name=REGION)
    mock_client.list_members.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_members_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_members.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_members",
    )
    with pytest.raises(RuntimeError, match="Failed to list members"):
        list_members(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_organization_admin_accounts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_organization_admin_accounts.return_value = {}
    list_organization_admin_accounts(region_name=REGION)
    mock_client.list_organization_admin_accounts.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_organization_admin_accounts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_organization_admin_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_organization_admin_accounts",
    )
    with pytest.raises(RuntimeError, match="Failed to list organization admin accounts"):
        list_organization_admin_accounts(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_resource_profile_artifacts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_resource_profile_artifacts.return_value = {}
    list_resource_profile_artifacts("test-resource_arn", region_name=REGION)
    mock_client.list_resource_profile_artifacts.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_resource_profile_artifacts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_resource_profile_artifacts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_profile_artifacts",
    )
    with pytest.raises(RuntimeError, match="Failed to list resource profile artifacts"):
        list_resource_profile_artifacts("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_resource_profile_detections(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_resource_profile_detections.return_value = {}
    list_resource_profile_detections("test-resource_arn", region_name=REGION)
    mock_client.list_resource_profile_detections.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_resource_profile_detections_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_resource_profile_detections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_profile_detections",
    )
    with pytest.raises(RuntimeError, match="Failed to list resource profile detections"):
        list_resource_profile_detections("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_sensitivity_inspection_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sensitivity_inspection_templates.return_value = {}
    list_sensitivity_inspection_templates(region_name=REGION)
    mock_client.list_sensitivity_inspection_templates.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_sensitivity_inspection_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sensitivity_inspection_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sensitivity_inspection_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list sensitivity inspection templates"):
        list_sensitivity_inspection_templates(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.macie.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_put_classification_export_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_classification_export_configuration.return_value = {}
    put_classification_export_configuration({}, region_name=REGION)
    mock_client.put_classification_export_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_put_classification_export_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_classification_export_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_classification_export_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to put classification export configuration"):
        put_classification_export_configuration({}, region_name=REGION)


@patch("aws_util.macie.get_client")
def test_put_findings_publication_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_findings_publication_configuration.return_value = {}
    put_findings_publication_configuration(region_name=REGION)
    mock_client.put_findings_publication_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_put_findings_publication_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_findings_publication_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_findings_publication_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to put findings publication configuration"):
        put_findings_publication_configuration(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_run_custom_data_identifier(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_custom_data_identifier.return_value = {}
    run_custom_data_identifier("test-regex", "test-sample_text", region_name=REGION)
    mock_client.test_custom_data_identifier.assert_called_once()


@patch("aws_util.macie.get_client")
def test_run_custom_data_identifier_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_custom_data_identifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_custom_data_identifier",
    )
    with pytest.raises(RuntimeError, match="Failed to run custom data identifier"):
        run_custom_data_identifier("test-regex", "test-sample_text", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_search_resources(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_resources.return_value = {}
    search_resources(region_name=REGION)
    mock_client.search_resources.assert_called_once()


@patch("aws_util.macie.get_client")
def test_search_resources_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_resources",
    )
    with pytest.raises(RuntimeError, match="Failed to search resources"):
        search_resources(region_name=REGION)


@patch("aws_util.macie.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.macie.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.macie.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.macie.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_allow_list(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_allow_list.return_value = {}
    update_allow_list({}, "test-id", "test-name", region_name=REGION)
    mock_client.update_allow_list.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_allow_list_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_allow_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_allow_list",
    )
    with pytest.raises(RuntimeError, match="Failed to update allow list"):
        update_allow_list({}, "test-id", "test-name", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_automated_discovery_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_automated_discovery_configuration.return_value = {}
    update_automated_discovery_configuration("test-status", region_name=REGION)
    mock_client.update_automated_discovery_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_automated_discovery_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_automated_discovery_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automated_discovery_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update automated discovery configuration"):
        update_automated_discovery_configuration("test-status", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_classification_scope(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_classification_scope.return_value = {}
    update_classification_scope("test-id", region_name=REGION)
    mock_client.update_classification_scope.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_classification_scope_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_classification_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_classification_scope",
    )
    with pytest.raises(RuntimeError, match="Failed to update classification scope"):
        update_classification_scope("test-id", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_member_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_member_session.return_value = {}
    update_member_session("test-id", "test-status", region_name=REGION)
    mock_client.update_member_session.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_member_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_member_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_member_session",
    )
    with pytest.raises(RuntimeError, match="Failed to update member session"):
        update_member_session("test-id", "test-status", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.return_value = {}
    update_organization_configuration(True, region_name=REGION)
    mock_client.update_organization_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update organization configuration"):
        update_organization_configuration(True, region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_resource_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_profile.return_value = {}
    update_resource_profile("test-resource_arn", region_name=REGION)
    mock_client.update_resource_profile.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_resource_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to update resource profile"):
        update_resource_profile("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_resource_profile_detections(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_profile_detections.return_value = {}
    update_resource_profile_detections("test-resource_arn", region_name=REGION)
    mock_client.update_resource_profile_detections.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_resource_profile_detections_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_resource_profile_detections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_profile_detections",
    )
    with pytest.raises(RuntimeError, match="Failed to update resource profile detections"):
        update_resource_profile_detections("test-resource_arn", region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_reveal_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_reveal_configuration.return_value = {}
    update_reveal_configuration({}, region_name=REGION)
    mock_client.update_reveal_configuration.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_reveal_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_reveal_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_reveal_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update reveal configuration"):
        update_reveal_configuration({}, region_name=REGION)


@patch("aws_util.macie.get_client")
def test_update_sensitivity_inspection_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sensitivity_inspection_template.return_value = {}
    update_sensitivity_inspection_template("test-id", region_name=REGION)
    mock_client.update_sensitivity_inspection_template.assert_called_once()


@patch("aws_util.macie.get_client")
def test_update_sensitivity_inspection_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sensitivity_inspection_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_sensitivity_inspection_template",
    )
    with pytest.raises(RuntimeError, match="Failed to update sensitivity inspection template"):
        update_sensitivity_inspection_template("test-id", region_name=REGION)


def test_update_macie_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_macie_session
    mock_client = MagicMock()
    mock_client.update_macie_session.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_macie_session(finding_publishing_frequency="test-finding_publishing_frequency", status="test-status", region_name="us-east-1")
    mock_client.update_macie_session.assert_called_once()

def test_list_classification_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_classification_jobs
    mock_client = MagicMock()
    mock_client.list_classification_jobs.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_classification_jobs(max_results=1, region_name="us-east-1")
    mock_client.list_classification_jobs.assert_called_once()

def test_list_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_findings
    mock_client = MagicMock()
    mock_client.list_findings.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_findings(max_results=1, region_name="us-east-1")
    mock_client.list_findings.assert_called_once()

def test_list_findings_filters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_findings_filters
    mock_client = MagicMock()
    mock_client.list_findings_filters.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_findings_filters(max_results=1, region_name="us-east-1")
    mock_client.list_findings_filters.assert_called_once()

def test_update_findings_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_findings_filter
    mock_client = MagicMock()
    mock_client.update_findings_filter.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_findings_filter("test-filter_id", name="test-name", action="test-action", finding_criteria="test-finding_criteria", description="test-description", region_name="us-east-1")
    mock_client.update_findings_filter.assert_called_once()

def test_describe_buckets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import describe_buckets
    mock_client = MagicMock()
    mock_client.describe_buckets.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    describe_buckets(max_results=1, region_name="us-east-1")
    mock_client.describe_buckets.assert_called_once()

def test_accept_invitation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import accept_invitation
    mock_client = MagicMock()
    mock_client.accept_invitation.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    accept_invitation("test-invitation_id", administrator_account_id=1, master_account=1, region_name="us-east-1")
    mock_client.accept_invitation.assert_called_once()

def test_batch_get_custom_data_identifiers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import batch_get_custom_data_identifiers
    mock_client = MagicMock()
    mock_client.batch_get_custom_data_identifiers.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    batch_get_custom_data_identifiers(ids="test-ids", region_name="us-east-1")
    mock_client.batch_get_custom_data_identifiers.assert_called_once()

def test_batch_update_automated_discovery_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import batch_update_automated_discovery_accounts
    mock_client = MagicMock()
    mock_client.batch_update_automated_discovery_accounts.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    batch_update_automated_discovery_accounts(accounts=1, region_name="us-east-1")
    mock_client.batch_update_automated_discovery_accounts.assert_called_once()

def test_create_allow_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_allow_list
    mock_client = MagicMock()
    mock_client.create_allow_list.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    create_allow_list("test-client_token", "test-criteria", "test-name", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_allow_list.assert_called_once()

def test_create_custom_data_identifier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_custom_data_identifier
    mock_client = MagicMock()
    mock_client.create_custom_data_identifier.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    create_custom_data_identifier("test-name", "test-regex", client_token="test-client_token", description="test-description", ignore_words="test-ignore_words", keywords="test-keywords", maximum_match_distance=1, severity_levels="test-severity_levels", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_data_identifier.assert_called_once()

def test_create_invitations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_invitations
    mock_client = MagicMock()
    mock_client.create_invitations.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    create_invitations(1, disable_email_notification=True, message="test-message", region_name="us-east-1")
    mock_client.create_invitations.assert_called_once()

def test_create_member_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_member
    mock_client = MagicMock()
    mock_client.create_member.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    create_member(1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_member.assert_called_once()

def test_create_sample_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_sample_findings
    mock_client = MagicMock()
    mock_client.create_sample_findings.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    create_sample_findings(finding_types="test-finding_types", region_name="us-east-1")
    mock_client.create_sample_findings.assert_called_once()

def test_delete_allow_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import delete_allow_list
    mock_client = MagicMock()
    mock_client.delete_allow_list.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    delete_allow_list("test-id", ignore_job_checks="test-ignore_job_checks", region_name="us-east-1")
    mock_client.delete_allow_list.assert_called_once()

def test_enable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import enable_organization_admin_account
    mock_client = MagicMock()
    mock_client.enable_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    enable_organization_admin_account(1, client_token="test-client_token", region_name="us-east-1")
    mock_client.enable_organization_admin_account.assert_called_once()

def test_get_finding_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import get_finding_statistics
    mock_client = MagicMock()
    mock_client.get_finding_statistics.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    get_finding_statistics("test-group_by", finding_criteria="test-finding_criteria", size=1, sort_criteria="test-sort_criteria", region_name="us-east-1")
    mock_client.get_finding_statistics.assert_called_once()

def test_get_usage_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import get_usage_statistics
    mock_client = MagicMock()
    mock_client.get_usage_statistics.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    get_usage_statistics(filter_by="test-filter_by", max_results=1, next_token="test-next_token", sort_by="test-sort_by", time_range="test-time_range", region_name="us-east-1")
    mock_client.get_usage_statistics.assert_called_once()

def test_get_usage_totals_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import get_usage_totals
    mock_client = MagicMock()
    mock_client.get_usage_totals.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    get_usage_totals(time_range="test-time_range", region_name="us-east-1")
    mock_client.get_usage_totals.assert_called_once()

def test_list_allow_lists_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_allow_lists
    mock_client = MagicMock()
    mock_client.list_allow_lists.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_allow_lists(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_allow_lists.assert_called_once()

def test_list_automated_discovery_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_automated_discovery_accounts
    mock_client = MagicMock()
    mock_client.list_automated_discovery_accounts.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_automated_discovery_accounts(account_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_automated_discovery_accounts.assert_called_once()

def test_list_classification_scopes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_classification_scopes
    mock_client = MagicMock()
    mock_client.list_classification_scopes.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_classification_scopes(name="test-name", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_classification_scopes.assert_called_once()

def test_list_custom_data_identifiers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_custom_data_identifiers
    mock_client = MagicMock()
    mock_client.list_custom_data_identifiers.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_custom_data_identifiers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_custom_data_identifiers.assert_called_once()

def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_invitations
    mock_client = MagicMock()
    mock_client.list_invitations.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_invitations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_invitations.assert_called_once()

def test_list_managed_data_identifiers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_managed_data_identifiers
    mock_client = MagicMock()
    mock_client.list_managed_data_identifiers.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_managed_data_identifiers(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_managed_data_identifiers.assert_called_once()

def test_list_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_members
    mock_client = MagicMock()
    mock_client.list_members.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_members(max_results=1, next_token="test-next_token", only_associated="test-only_associated", region_name="us-east-1")
    mock_client.list_members.assert_called_once()

def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_organization_admin_accounts
    mock_client = MagicMock()
    mock_client.list_organization_admin_accounts.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_organization_admin_accounts(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_organization_admin_accounts.assert_called_once()

def test_list_resource_profile_artifacts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_resource_profile_artifacts
    mock_client = MagicMock()
    mock_client.list_resource_profile_artifacts.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_resource_profile_artifacts("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_profile_artifacts.assert_called_once()

def test_list_resource_profile_detections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_resource_profile_detections
    mock_client = MagicMock()
    mock_client.list_resource_profile_detections.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_resource_profile_detections("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_profile_detections.assert_called_once()

def test_list_sensitivity_inspection_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_sensitivity_inspection_templates
    mock_client = MagicMock()
    mock_client.list_sensitivity_inspection_templates.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    list_sensitivity_inspection_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sensitivity_inspection_templates.assert_called_once()

def test_put_findings_publication_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import put_findings_publication_configuration
    mock_client = MagicMock()
    mock_client.put_findings_publication_configuration.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    put_findings_publication_configuration(client_token="test-client_token", security_hub_configuration={}, region_name="us-east-1")
    mock_client.put_findings_publication_configuration.assert_called_once()

def test_run_custom_data_identifier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import run_custom_data_identifier
    mock_client = MagicMock()
    mock_client.test_custom_data_identifier.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    run_custom_data_identifier("test-regex", "test-sample_text", ignore_words="test-ignore_words", keywords="test-keywords", maximum_match_distance=1, region_name="us-east-1")
    mock_client.test_custom_data_identifier.assert_called_once()

def test_search_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import search_resources
    mock_client = MagicMock()
    mock_client.search_resources.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    search_resources(bucket_criteria="test-bucket_criteria", max_results=1, next_token="test-next_token", sort_criteria="test-sort_criteria", region_name="us-east-1")
    mock_client.search_resources.assert_called_once()

def test_update_allow_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_allow_list
    mock_client = MagicMock()
    mock_client.update_allow_list.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_allow_list("test-criteria", "test-id", "test-name", description="test-description", region_name="us-east-1")
    mock_client.update_allow_list.assert_called_once()

def test_update_automated_discovery_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_automated_discovery_configuration
    mock_client = MagicMock()
    mock_client.update_automated_discovery_configuration.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_automated_discovery_configuration("test-status", auto_enable_organization_members=True, region_name="us-east-1")
    mock_client.update_automated_discovery_configuration.assert_called_once()

def test_update_classification_scope_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_classification_scope
    mock_client = MagicMock()
    mock_client.update_classification_scope.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_classification_scope("test-id", s3="test-s3", region_name="us-east-1")
    mock_client.update_classification_scope.assert_called_once()

def test_update_resource_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_resource_profile
    mock_client = MagicMock()
    mock_client.update_resource_profile.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_resource_profile("test-resource_arn", sensitivity_score_override="test-sensitivity_score_override", region_name="us-east-1")
    mock_client.update_resource_profile.assert_called_once()

def test_update_resource_profile_detections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_resource_profile_detections
    mock_client = MagicMock()
    mock_client.update_resource_profile_detections.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_resource_profile_detections("test-resource_arn", suppress_data_identifiers="test-suppress_data_identifiers", region_name="us-east-1")
    mock_client.update_resource_profile_detections.assert_called_once()

def test_update_reveal_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_reveal_configuration
    mock_client = MagicMock()
    mock_client.update_reveal_configuration.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_reveal_configuration({}, retrieval_configuration={}, region_name="us-east-1")
    mock_client.update_reveal_configuration.assert_called_once()

def test_update_sensitivity_inspection_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import update_sensitivity_inspection_template
    mock_client = MagicMock()
    mock_client.update_sensitivity_inspection_template.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    update_sensitivity_inspection_template("test-id", description="test-description", excludes="test-excludes", includes=True, region_name="us-east-1")
    mock_client.update_sensitivity_inspection_template.assert_called_once()


def test_describe_buckets_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import describe_buckets
    mock_client = MagicMock()
    mock_client.describe_buckets.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: mock_client)
    describe_buckets(sort_criteria="test-sort_criteria", region_name="us-east-1")
    mock_client.describe_buckets.assert_called_once()

def test_enable_macie_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import enable_macie
    m = MagicMock(); m.enable_macie.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    enable_macie(client_token="tok", region_name="us-east-1")

def test_create_classification_job_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_classification_job
    m = MagicMock(); m.create_classification_job.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    create_classification_job("name", "ONE_TIME", s3_job_definition={}, client_token="tok", description="d", tags={"k": "v"}, region_name="us-east-1")

def test_list_classification_jobs_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_classification_jobs
    m = MagicMock(); m.list_classification_jobs.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    list_classification_jobs(filter_criteria={"includes": []}, sort_criteria={"attributeName": "name"}, region_name="us-east-1")

def test_list_findings_macie_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import list_findings
    m = MagicMock(); m.list_findings.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    list_findings(finding_criteria={"criterion": {}}, sort_criteria={"attributeName": "severity"}, region_name="us-east-1")

def test_create_findings_filter_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import create_findings_filter
    m = MagicMock(); m.create_findings_filter.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    create_findings_filter("name", "ARCHIVE", finding_criteria={}, description="d", client_token="tok", tags={"k": "v"}, region_name="us-east-1")

def test_describe_buckets_criteria(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.macie import describe_buckets
    m = MagicMock(); m.describe_buckets.return_value = {}
    monkeypatch.setattr("aws_util.macie.get_client", lambda *a, **kw: m)
    describe_buckets(criteria={"accountId": {}}, sort_criteria={"attributeName": "accountId"}, region_name="us-east-1")
