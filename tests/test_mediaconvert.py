"""Tests for aws_util.mediaconvert -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.exceptions import AwsTimeoutError
from aws_util.mediaconvert import (
    EndpointResult,
    JobResult,
    JobTemplateResult,
    QueueResult,
    _parse_job,
    _parse_job_template,
    _parse_queue,
    cancel_job,
    create_job,
    create_job_template,
    create_queue,
    delete_job_template,
    delete_queue,
    describe_endpoints,
    get_job,
    get_job_template,
    get_queue,
    list_job_templates,
    list_jobs,
    list_queues,
    wait_for_job,
    associate_certificate,
    create_preset,
    create_resource_share,
    delete_policy,
    delete_preset,
    disassociate_certificate,
    get_jobs_query_results,
    get_policy,
    get_preset,
    list_presets,
    list_tags_for_resource,
    list_versions,
    probe,
    put_policy,
    search_jobs,
    start_jobs_query,
    tag_resource,
    untag_resource,
    update_job_template,
    update_preset,
    update_queue,
)

_ERR = ClientError({"Error": {"Code": "X", "Message": "fail"}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_job_result_minimal():
    m = JobResult(id="j1")
    assert m.status is None
    assert m.settings == {}


def test_job_result_full():
    m = JobResult(
        id="j1", arn="arn:1", status="COMPLETE", queue="q1",
        role="r1", settings={"k": "v"}, created_at="2024-01-01",
        error_code=1234, error_message="msg", extra={"x": 1},
    )
    assert m.error_code == 1234


def test_job_template_result_minimal():
    m = JobTemplateResult(name="t1")
    assert m.arn is None


def test_job_template_result_full():
    m = JobTemplateResult(
        name="t1", arn="arn:1", description="d",
        category="c", queue="q", settings={"k": "v"},
        extra={"x": 1},
    )
    assert m.category == "c"


def test_queue_result_minimal():
    m = QueueResult(name="q1")
    assert m.status is None


def test_queue_result_full():
    m = QueueResult(
        name="q1", arn="arn:1", status="ACTIVE",
        description="d", pricing_plan="ON_DEMAND", extra={"x": 1},
    )
    assert m.pricing_plan == "ON_DEMAND"


def test_endpoint_result():
    m = EndpointResult(url="https://endpoint.amazonaws.com")
    assert m.url.startswith("https")


# ---------------------------------------------------------------------------
# _parse helpers
# ---------------------------------------------------------------------------


def test_parse_job():
    data = {
        "Id": "j1", "Arn": "arn:1", "Status": "COMPLETE",
        "Queue": "q1", "Role": "r1", "Settings": {"k": "v"},
        "CreatedAt": "2024-01-01", "ErrorCode": 1234,
        "ErrorMessage": "msg",
    }
    r = _parse_job(data)
    assert r.id == "j1"
    assert r.error_code == 1234


def test_parse_job_template():
    data = {
        "Name": "t1", "Arn": "arn:1", "Description": "d",
        "Category": "c", "Queue": "q", "Settings": {"k": "v"},
    }
    r = _parse_job_template(data)
    assert r.name == "t1"


def test_parse_queue():
    data = {
        "Name": "q1", "Arn": "arn:1", "Status": "ACTIVE",
        "Description": "d", "PricingPlan": "ON_DEMAND",
    }
    r = _parse_queue(data)
    assert r.name == "q1"


# ---------------------------------------------------------------------------
# create_job
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_create_job_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.return_value = {"Job": {"Id": "j1"}}
    r = create_job("role", {"k": "v"})
    assert r.id == "j1"


@patch("aws_util.mediaconvert.get_client")
def test_create_job_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.return_value = {"Job": {"Id": "j1"}}
    r = create_job("role", {"k": "v"}, queue="q1", job_template="t1")
    assert r.id == "j1"


@patch("aws_util.mediaconvert.get_client")
def test_create_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_job failed"):
        create_job("role", {})


# ---------------------------------------------------------------------------
# get_job
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_get_job_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_job.return_value = {"Job": {"Id": "j1", "Status": "COMPLETE"}}
    r = get_job("j1")
    assert r.id == "j1"


@patch("aws_util.mediaconvert.get_client")
def test_get_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_job.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_job failed"):
        get_job("j1")


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_list_jobs_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_jobs.return_value = {"Jobs": [{"Id": "j1"}]}
    r = list_jobs()
    assert len(r) == 1


@patch("aws_util.mediaconvert.get_client")
def test_list_jobs_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_jobs.return_value = {"Jobs": [{"Id": "j1"}]}
    r = list_jobs(queue="q1", status="COMPLETE", max_results=10)
    assert len(r) == 1


@patch("aws_util.mediaconvert.get_client")
def test_list_jobs_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_jobs.side_effect = [
        {"Jobs": [{"Id": "j1"}], "NextToken": "tok"},
        {"Jobs": [{"Id": "j2"}]},
    ]
    r = list_jobs()
    assert len(r) == 2


@patch("aws_util.mediaconvert.get_client")
def test_list_jobs_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_jobs.side_effect = _ERR
    with pytest.raises(RuntimeError, match="list_jobs failed"):
        list_jobs()


# ---------------------------------------------------------------------------
# cancel_job
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_cancel_job_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    cancel_job("j1")
    client.cancel_job.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_cancel_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_job.side_effect = _ERR
    with pytest.raises(RuntimeError, match="cancel_job failed"):
        cancel_job("j1")


# ---------------------------------------------------------------------------
# create_job_template
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_create_job_template_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job_template.return_value = {
        "JobTemplate": {"Name": "t1"},
    }
    r = create_job_template("t1", {"k": "v"})
    assert r.name == "t1"


@patch("aws_util.mediaconvert.get_client")
def test_create_job_template_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job_template.return_value = {
        "JobTemplate": {"Name": "t1"},
    }
    r = create_job_template(
        "t1", {"k": "v"},
        description="d", category="c", queue="q1",
    )
    assert r.name == "t1"


@patch("aws_util.mediaconvert.get_client")
def test_create_job_template_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job_template.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_job_template failed"):
        create_job_template("t1", {})


# ---------------------------------------------------------------------------
# get_job_template
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_get_job_template_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_job_template.return_value = {
        "JobTemplate": {"Name": "t1"},
    }
    r = get_job_template("t1")
    assert r.name == "t1"


@patch("aws_util.mediaconvert.get_client")
def test_get_job_template_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_job_template.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_job_template failed"):
        get_job_template("t1")


# ---------------------------------------------------------------------------
# list_job_templates
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_list_job_templates_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_job_templates.return_value = {
        "JobTemplates": [{"Name": "t1"}],
    }
    r = list_job_templates()
    assert len(r) == 1


@patch("aws_util.mediaconvert.get_client")
def test_list_job_templates_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_job_templates.return_value = {
        "JobTemplates": [{"Name": "t1"}],
    }
    r = list_job_templates(category="c", max_results=5)
    assert len(r) == 1


@patch("aws_util.mediaconvert.get_client")
def test_list_job_templates_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_job_templates.side_effect = [
        {"JobTemplates": [{"Name": "t1"}], "NextToken": "tok"},
        {"JobTemplates": [{"Name": "t2"}]},
    ]
    r = list_job_templates()
    assert len(r) == 2


@patch("aws_util.mediaconvert.get_client")
def test_list_job_templates_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_job_templates.side_effect = _ERR
    with pytest.raises(RuntimeError, match="list_job_templates failed"):
        list_job_templates()


# ---------------------------------------------------------------------------
# delete_job_template
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_delete_job_template_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_job_template("t1")


@patch("aws_util.mediaconvert.get_client")
def test_delete_job_template_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_job_template.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_job_template failed"):
        delete_job_template("t1")


# ---------------------------------------------------------------------------
# Queue operations
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_create_queue_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_queue.return_value = {"Queue": {"Name": "q1"}}
    r = create_queue("q1")
    assert r.name == "q1"


@patch("aws_util.mediaconvert.get_client")
def test_create_queue_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_queue.return_value = {"Queue": {"Name": "q1"}}
    r = create_queue("q1", description="d", pricing_plan="ON_DEMAND")
    assert r.name == "q1"


@patch("aws_util.mediaconvert.get_client")
def test_create_queue_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_queue.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_queue failed"):
        create_queue("q1")


@patch("aws_util.mediaconvert.get_client")
def test_get_queue_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_queue.return_value = {"Queue": {"Name": "q1"}}
    r = get_queue("q1")
    assert r.name == "q1"


@patch("aws_util.mediaconvert.get_client")
def test_get_queue_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_queue.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_queue failed"):
        get_queue("q1")


@patch("aws_util.mediaconvert.get_client")
def test_list_queues_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_queues.return_value = {"Queues": [{"Name": "q1"}]}
    r = list_queues()
    assert len(r) == 1


@patch("aws_util.mediaconvert.get_client")
def test_list_queues_with_max(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_queues.return_value = {"Queues": []}
    r = list_queues(max_results=5)
    assert r == []


@patch("aws_util.mediaconvert.get_client")
def test_list_queues_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_queues.side_effect = [
        {"Queues": [{"Name": "q1"}], "NextToken": "tok"},
        {"Queues": [{"Name": "q2"}]},
    ]
    r = list_queues()
    assert len(r) == 2


@patch("aws_util.mediaconvert.get_client")
def test_list_queues_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_queues.side_effect = _ERR
    with pytest.raises(RuntimeError, match="list_queues failed"):
        list_queues()


@patch("aws_util.mediaconvert.get_client")
def test_delete_queue_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_queue("q1")


@patch("aws_util.mediaconvert.get_client")
def test_delete_queue_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_queue.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_queue failed"):
        delete_queue("q1")


# ---------------------------------------------------------------------------
# describe_endpoints
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_client")
def test_describe_endpoints_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.return_value = {
        "Endpoints": [{"Url": "https://ep.amazonaws.com"}],
    }
    r = describe_endpoints()
    assert len(r) == 1
    assert r[0].url == "https://ep.amazonaws.com"


@patch("aws_util.mediaconvert.get_client")
def test_describe_endpoints_with_max(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.return_value = {"Endpoints": []}
    r = describe_endpoints(max_results=5)
    assert r == []


@patch("aws_util.mediaconvert.get_client")
def test_describe_endpoints_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.side_effect = [
        {"Endpoints": [{"Url": "u1"}], "NextToken": "tok"},
        {"Endpoints": [{"Url": "u2"}]},
    ]
    r = describe_endpoints()
    assert len(r) == 2


@patch("aws_util.mediaconvert.get_client")
def test_describe_endpoints_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_endpoints.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_endpoints failed"):
        describe_endpoints()


# ---------------------------------------------------------------------------
# wait_for_job
# ---------------------------------------------------------------------------


@patch("aws_util.mediaconvert.get_job")
def test_wait_for_job_ok(mock_gj):
    mock_gj.return_value = JobResult(id="j1", status="COMPLETE")
    r = wait_for_job("j1")
    assert r.status == "COMPLETE"


@patch("aws_util.mediaconvert.get_job")
def test_wait_for_job_custom_statuses(mock_gj):
    mock_gj.return_value = JobResult(id="j1", status="DONE")
    r = wait_for_job("j1", target_statuses=["DONE"])
    assert r.status == "DONE"


@patch("aws_util.mediaconvert.time")
@patch("aws_util.mediaconvert.get_job")
def test_wait_for_job_timeout(mock_gj, mock_time):
    mock_time.monotonic.side_effect = [0.0, 999.0]
    mock_time.sleep = MagicMock()
    mock_gj.return_value = JobResult(id="j1", status="PROGRESSING")
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        wait_for_job("j1", timeout=1.0)


REGION = "us-east-1"


@patch("aws_util.mediaconvert.get_client")
def test_associate_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_certificate.return_value = {}
    associate_certificate("test-arn", region_name=REGION)
    mock_client.associate_certificate.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_associate_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to associate certificate"):
        associate_certificate("test-arn", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_create_preset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_preset.return_value = {}
    create_preset("test-name", {}, region_name=REGION)
    mock_client.create_preset.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_create_preset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_preset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_preset",
    )
    with pytest.raises(RuntimeError, match="Failed to create preset"):
        create_preset("test-name", {}, region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_create_resource_share(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_share.return_value = {}
    create_resource_share("test-job_id", "test-support_case_id", region_name=REGION)
    mock_client.create_resource_share.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_create_resource_share_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_resource_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_share",
    )
    with pytest.raises(RuntimeError, match="Failed to create resource share"):
        create_resource_share("test-job_id", "test-support_case_id", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_delete_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_policy.return_value = {}
    delete_policy(region_name=REGION)
    mock_client.delete_policy.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_delete_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete policy"):
        delete_policy(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_delete_preset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_preset.return_value = {}
    delete_preset("test-name", region_name=REGION)
    mock_client.delete_preset.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_delete_preset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_preset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_preset",
    )
    with pytest.raises(RuntimeError, match="Failed to delete preset"):
        delete_preset("test-name", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_disassociate_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_certificate.return_value = {}
    disassociate_certificate("test-arn", region_name=REGION)
    mock_client.disassociate_certificate.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_disassociate_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate certificate"):
        disassociate_certificate("test-arn", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_get_jobs_query_results(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_jobs_query_results.return_value = {}
    get_jobs_query_results("test-id", region_name=REGION)
    mock_client.get_jobs_query_results.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_get_jobs_query_results_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_jobs_query_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_jobs_query_results",
    )
    with pytest.raises(RuntimeError, match="Failed to get jobs query results"):
        get_jobs_query_results("test-id", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_get_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_policy.return_value = {}
    get_policy(region_name=REGION)
    mock_client.get_policy.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_get_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to get policy"):
        get_policy(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_get_preset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_preset.return_value = {}
    get_preset("test-name", region_name=REGION)
    mock_client.get_preset.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_get_preset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_preset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_preset",
    )
    with pytest.raises(RuntimeError, match="Failed to get preset"):
        get_preset("test-name", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_list_presets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_presets.return_value = {}
    list_presets(region_name=REGION)
    mock_client.list_presets.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_list_presets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_presets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_presets",
    )
    with pytest.raises(RuntimeError, match="Failed to list presets"):
        list_presets(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-arn", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_list_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_versions.return_value = {}
    list_versions(region_name=REGION)
    mock_client.list_versions.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_list_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list versions"):
        list_versions(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_probe(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.probe.return_value = {}
    probe(region_name=REGION)
    mock_client.probe.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_probe_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.probe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "probe",
    )
    with pytest.raises(RuntimeError, match="Failed to probe"):
        probe(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_put_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_policy.return_value = {}
    put_policy({}, region_name=REGION)
    mock_client.put_policy.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_put_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to put policy"):
        put_policy({}, region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_search_jobs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_jobs.return_value = {}
    search_jobs(region_name=REGION)
    mock_client.search_jobs.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_search_jobs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_jobs",
    )
    with pytest.raises(RuntimeError, match="Failed to search jobs"):
        search_jobs(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_start_jobs_query(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_jobs_query.return_value = {}
    start_jobs_query(region_name=REGION)
    mock_client.start_jobs_query.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_start_jobs_query_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_jobs_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_jobs_query",
    )
    with pytest.raises(RuntimeError, match="Failed to start jobs query"):
        start_jobs_query(region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-arn", {}, region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-arn", region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-arn", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_update_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_job_template.return_value = {}
    update_job_template("test-name", region_name=REGION)
    mock_client.update_job_template.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_update_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to update job template"):
        update_job_template("test-name", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_update_preset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_preset.return_value = {}
    update_preset("test-name", region_name=REGION)
    mock_client.update_preset.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_update_preset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_preset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_preset",
    )
    with pytest.raises(RuntimeError, match="Failed to update preset"):
        update_preset("test-name", region_name=REGION)


@patch("aws_util.mediaconvert.get_client")
def test_update_queue(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_queue.return_value = {}
    update_queue("test-name", region_name=REGION)
    mock_client.update_queue.assert_called_once()


@patch("aws_util.mediaconvert.get_client")
def test_update_queue_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_queue.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue",
    )
    with pytest.raises(RuntimeError, match="Failed to update queue"):
        update_queue("test-name", region_name=REGION)


def test_create_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import create_job
    mock_client = MagicMock()
    mock_client.create_job.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    create_job("test-role", {}, queue="test-queue", job_template="test-job_template", region_name="us-east-1")
    mock_client.create_job.assert_called_once()

def test_list_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import list_jobs
    mock_client = MagicMock()
    mock_client.list_jobs.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    list_jobs(queue="test-queue", status="test-status", max_results=1, region_name="us-east-1")
    mock_client.list_jobs.assert_called_once()

def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import create_job_template
    mock_client = MagicMock()
    mock_client.create_job_template.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    create_job_template("test-name", {}, description="test-description", category="test-category", queue="test-queue", region_name="us-east-1")
    mock_client.create_job_template.assert_called_once()

def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import list_job_templates
    mock_client = MagicMock()
    mock_client.list_job_templates.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    list_job_templates(category="test-category", max_results=1, region_name="us-east-1")
    mock_client.list_job_templates.assert_called_once()

def test_create_queue_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import create_queue
    mock_client = MagicMock()
    mock_client.create_queue.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    create_queue("test-name", description="test-description", pricing_plan="test-pricing_plan", region_name="us-east-1")
    mock_client.create_queue.assert_called_once()

def test_list_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import list_queues
    mock_client = MagicMock()
    mock_client.list_queues.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    list_queues(max_results=1, region_name="us-east-1")
    mock_client.list_queues.assert_called_once()

def test_describe_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import describe_endpoints
    mock_client = MagicMock()
    mock_client.describe_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    describe_endpoints(max_results=1, region_name="us-east-1")
    mock_client.describe_endpoints.assert_called_once()

def test_create_preset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import create_preset
    mock_client = MagicMock()
    mock_client.create_preset.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    create_preset("test-name", {}, category="test-category", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_preset.assert_called_once()

def test_list_presets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import list_presets
    mock_client = MagicMock()
    mock_client.list_presets.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    list_presets(category="test-category", list_by="test-list_by", max_results=1, next_token="test-next_token", order="test-order", region_name="us-east-1")
    mock_client.list_presets.assert_called_once()

def test_list_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import list_versions
    mock_client = MagicMock()
    mock_client.list_versions.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    list_versions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_versions.assert_called_once()

def test_probe_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import probe
    mock_client = MagicMock()
    mock_client.probe.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    probe(input_files="test-input_files", region_name="us-east-1")
    mock_client.probe.assert_called_once()

def test_search_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import search_jobs
    mock_client = MagicMock()
    mock_client.search_jobs.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    search_jobs(input_file="test-input_file", max_results=1, next_token="test-next_token", order="test-order", queue="test-queue", status="test-status", region_name="us-east-1")
    mock_client.search_jobs.assert_called_once()

def test_start_jobs_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import start_jobs_query
    mock_client = MagicMock()
    mock_client.start_jobs_query.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    start_jobs_query(filter_list="test-filter_list", max_results=1, next_token="test-next_token", order="test-order", region_name="us-east-1")
    mock_client.start_jobs_query.assert_called_once()

def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import untag_resource
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-arn", tag_keys="test-tag_keys", region_name="us-east-1")
    mock_client.untag_resource.assert_called_once()

def test_update_job_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import update_job_template
    mock_client = MagicMock()
    mock_client.update_job_template.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    update_job_template("test-name", acceleration_settings={}, category="test-category", description="test-description", hop_destinations="test-hop_destinations", priority="test-priority", queue="test-queue", settings={}, status_update_interval="test-status_update_interval", region_name="us-east-1")
    mock_client.update_job_template.assert_called_once()

def test_update_preset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import update_preset
    mock_client = MagicMock()
    mock_client.update_preset.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    update_preset("test-name", category="test-category", description="test-description", settings={}, region_name="us-east-1")
    mock_client.update_preset.assert_called_once()

def test_update_queue_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.mediaconvert import update_queue
    mock_client = MagicMock()
    mock_client.update_queue.return_value = {}
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    update_queue("test-name", concurrent_jobs="test-concurrent_jobs", description="test-description", reservation_plan_settings={}, status="test-status", region_name="us-east-1")
    mock_client.update_queue.assert_called_once()


def test_wait_for_job_polls(monkeypatch):
    from unittest.mock import MagicMock, patch
    from aws_util.mediaconvert import wait_for_job
    import time as _time
    mock_client = MagicMock()
    mock_client.get_job.side_effect = [
        {"Job": {"Id": "j-1", "Status": "PROGRESSING"}},
        {"Job": {"Id": "j-1", "Status": "COMPLETE"}},
    ]
    monkeypatch.setattr("aws_util.mediaconvert.get_client", lambda *a, **kw: mock_client)
    monkeypatch.setattr(_time, "sleep", lambda s: None)
    result = wait_for_job("j-1", region_name="us-east-1")
