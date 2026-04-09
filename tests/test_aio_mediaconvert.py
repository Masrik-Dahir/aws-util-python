"""Tests for aws_util.aio.mediaconvert -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.mediaconvert import (
    EndpointResult,
    JobResult,
    JobTemplateResult,
    QueueResult,
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
from aws_util.exceptions import AwsTimeoutError

_PATCH = "aws_util.aio.mediaconvert.async_client"


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# create_job
# ---------------------------------------------------------------------------


async def test_create_job_ok(monkeypatch):
    mc = _mc({"Job": {"Id": "j1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_job("role", {"k": "v"})
    assert r.id == "j1"


async def test_create_job_with_opts(monkeypatch):
    mc = _mc({"Job": {"Id": "j1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_job("role", {"k": "v"}, queue="q1", job_template="t1")
    assert r.id == "j1"


async def test_create_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_job failed"):
        await create_job("role", {})


# ---------------------------------------------------------------------------
# get_job
# ---------------------------------------------------------------------------


async def test_get_job_ok(monkeypatch):
    mc = _mc({"Job": {"Id": "j1", "Status": "COMPLETE"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_job("j1")
    assert r.id == "j1"


async def test_get_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_job failed"):
        await get_job("j1")


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------


async def test_list_jobs_ok(monkeypatch):
    mc = _mc({"Jobs": [{"Id": "j1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_jobs()
    assert len(r) == 1


async def test_list_jobs_with_opts(monkeypatch):
    mc = _mc({"Jobs": [{"Id": "j1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_jobs(queue="q1", status="COMPLETE", max_results=10)
    assert len(r) == 1


async def test_list_jobs_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"Jobs": [{"Id": "j1"}], "NextToken": "tok"},
        {"Jobs": [{"Id": "j2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_jobs()
    assert len(r) == 2


async def test_list_jobs_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_jobs failed"):
        await list_jobs()


# ---------------------------------------------------------------------------
# cancel_job
# ---------------------------------------------------------------------------


async def test_cancel_job_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await cancel_job("j1")


async def test_cancel_job_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="cancel_job failed"):
        await cancel_job("j1")


# ---------------------------------------------------------------------------
# create_job_template
# ---------------------------------------------------------------------------


async def test_create_job_template_ok(monkeypatch):
    mc = _mc({"JobTemplate": {"Name": "t1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_job_template("t1", {"k": "v"})
    assert r.name == "t1"


async def test_create_job_template_with_opts(monkeypatch):
    mc = _mc({"JobTemplate": {"Name": "t1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_job_template(
        "t1", {"k": "v"}, description="d", category="c", queue="q1",
    )
    assert r.name == "t1"


async def test_create_job_template_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_job_template failed"):
        await create_job_template("t1", {})


# ---------------------------------------------------------------------------
# get_job_template
# ---------------------------------------------------------------------------


async def test_get_job_template_ok(monkeypatch):
    mc = _mc({"JobTemplate": {"Name": "t1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_job_template("t1")
    assert r.name == "t1"


async def test_get_job_template_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_job_template failed"):
        await get_job_template("t1")


# ---------------------------------------------------------------------------
# list_job_templates
# ---------------------------------------------------------------------------


async def test_list_job_templates_ok(monkeypatch):
    mc = _mc({"JobTemplates": [{"Name": "t1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_job_templates()
    assert len(r) == 1


async def test_list_job_templates_with_opts(monkeypatch):
    mc = _mc({"JobTemplates": [{"Name": "t1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_job_templates(category="c", max_results=5)
    assert len(r) == 1


async def test_list_job_templates_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"JobTemplates": [{"Name": "t1"}], "NextToken": "tok"},
        {"JobTemplates": [{"Name": "t2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_job_templates()
    assert len(r) == 2


async def test_list_job_templates_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_job_templates failed"):
        await list_job_templates()


# ---------------------------------------------------------------------------
# delete_job_template
# ---------------------------------------------------------------------------


async def test_delete_job_template_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_job_template("t1")


async def test_delete_job_template_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_job_template failed"):
        await delete_job_template("t1")


# ---------------------------------------------------------------------------
# Queue operations
# ---------------------------------------------------------------------------


async def test_create_queue_ok(monkeypatch):
    mc = _mc({"Queue": {"Name": "q1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_queue("q1")
    assert r.name == "q1"


async def test_create_queue_with_opts(monkeypatch):
    mc = _mc({"Queue": {"Name": "q1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_queue("q1", description="d", pricing_plan="ON_DEMAND")
    assert r.name == "q1"


async def test_create_queue_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_queue failed"):
        await create_queue("q1")


async def test_get_queue_ok(monkeypatch):
    mc = _mc({"Queue": {"Name": "q1"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_queue("q1")
    assert r.name == "q1"


async def test_get_queue_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_queue failed"):
        await get_queue("q1")


async def test_list_queues_ok(monkeypatch):
    mc = _mc({"Queues": [{"Name": "q1"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_queues()
    assert len(r) == 1


async def test_list_queues_with_max(monkeypatch):
    mc = _mc({"Queues": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_queues(max_results=5)
    assert r == []


async def test_list_queues_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"Queues": [{"Name": "q1"}], "NextToken": "tok"},
        {"Queues": [{"Name": "q2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await list_queues()
    assert len(r) == 2


async def test_list_queues_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_queues failed"):
        await list_queues()


async def test_delete_queue_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_queue("q1")


async def test_delete_queue_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_queue failed"):
        await delete_queue("q1")


# ---------------------------------------------------------------------------
# describe_endpoints
# ---------------------------------------------------------------------------


async def test_describe_endpoints_ok(monkeypatch):
    mc = _mc({"Endpoints": [{"Url": "https://ep.amazonaws.com"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_endpoints()
    assert len(r) == 1


async def test_describe_endpoints_with_max(monkeypatch):
    mc = _mc({"Endpoints": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_endpoints(max_results=5)
    assert r == []


async def test_describe_endpoints_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"Endpoints": [{"Url": "u1"}], "NextToken": "tok"},
        {"Endpoints": [{"Url": "u2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_endpoints()
    assert len(r) == 2


async def test_describe_endpoints_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_endpoints failed"):
        await describe_endpoints()


# ---------------------------------------------------------------------------
# wait_for_job
# ---------------------------------------------------------------------------


async def test_wait_for_job_ok(monkeypatch):
    mc = _mc({"Job": {"Id": "j1", "Status": "COMPLETE"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await wait_for_job("j1")
    assert r.status == "COMPLETE"


async def test_wait_for_job_custom_statuses(monkeypatch):
    mc = _mc({"Job": {"Id": "j1", "Status": "DONE"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await wait_for_job("j1", target_statuses=["DONE"])
    assert r.status == "DONE"


async def test_wait_for_job_timeout(monkeypatch):
    mc = _mc({"Job": {"Id": "j1", "Status": "PROGRESSING"}})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.mediaconvert.time.monotonic", lambda: 999.0)
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_job("j1", timeout=1.0)


async def test_associate_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_certificate("test-arn", )
    mock_client.call.assert_called_once()


async def test_associate_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_certificate("test-arn", )


async def test_create_preset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_preset("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_preset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_preset("test-name", {}, )


async def test_create_resource_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_share("test-job_id", "test-support_case_id", )
    mock_client.call.assert_called_once()


async def test_create_resource_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_share("test-job_id", "test-support_case_id", )


async def test_delete_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_policy()
    mock_client.call.assert_called_once()


async def test_delete_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_policy()


async def test_delete_preset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_preset("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_preset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_preset("test-name", )


async def test_disassociate_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_certificate("test-arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_certificate("test-arn", )


async def test_get_jobs_query_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_jobs_query_results("test-id", )
    mock_client.call.assert_called_once()


async def test_get_jobs_query_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_jobs_query_results("test-id", )


async def test_get_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_policy()
    mock_client.call.assert_called_once()


async def test_get_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_policy()


async def test_get_preset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_preset("test-name", )
    mock_client.call.assert_called_once()


async def test_get_preset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_preset("test-name", )


async def test_list_presets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_presets()
    mock_client.call.assert_called_once()


async def test_list_presets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_presets()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-arn", )


async def test_list_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_versions()
    mock_client.call.assert_called_once()


async def test_list_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_versions()


async def test_probe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await probe()
    mock_client.call.assert_called_once()


async def test_probe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await probe()


async def test_put_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_policy({}, )
    mock_client.call.assert_called_once()


async def test_put_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_policy({}, )


async def test_search_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_jobs()
    mock_client.call.assert_called_once()


async def test_search_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_jobs()


async def test_start_jobs_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_jobs_query()
    mock_client.call.assert_called_once()


async def test_start_jobs_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_jobs_query()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-arn", )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-arn", )


async def test_update_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_job_template("test-name", )
    mock_client.call.assert_called_once()


async def test_update_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_job_template("test-name", )


async def test_update_preset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_preset("test-name", )
    mock_client.call.assert_called_once()


async def test_update_preset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_preset("test-name", )


async def test_update_queue(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue("test-name", )
    mock_client.call.assert_called_once()


async def test_update_queue_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.mediaconvert.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue("test-name", )


@pytest.mark.asyncio
async def test_create_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import create_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await create_job("test-role", {}, queue="test-queue", job_template="test-job_template", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import list_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await list_jobs(queue="test-queue", status="test-status", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import create_job_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await create_job_template("test-name", {}, description="test-description", category="test-category", queue="test-queue", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import list_job_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await list_job_templates(category="test-category", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_queue_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import create_queue
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await create_queue("test-name", description="test-description", pricing_plan="test-pricing_plan", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import list_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await list_queues(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import describe_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await describe_endpoints(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_preset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import create_preset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await create_preset("test-name", {}, category="test-category", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_presets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import list_presets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await list_presets(category="test-category", list_by="test-list_by", max_results=1, next_token="test-next_token", order="test-order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import list_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await list_versions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_probe_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import probe
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await probe(input_files="test-input_files", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import search_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await search_jobs(input_file="test-input_file", max_results=1, next_token="test-next_token", order="test-order", queue="test-queue", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_jobs_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import start_jobs_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await start_jobs_query(filter_list="test-filter_list", max_results=1, next_token="test-next_token", order="test-order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import untag_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await untag_resource("test-arn", tag_keys="test-tag_keys", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_job_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import update_job_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await update_job_template("test-name", acceleration_settings={}, category="test-category", description="test-description", hop_destinations="test-hop_destinations", priority="test-priority", queue="test-queue", settings={}, status_update_interval="test-status_update_interval", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_preset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import update_preset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await update_preset("test-name", category="test-category", description="test-description", settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_queue_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.mediaconvert import update_queue
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.mediaconvert.async_client", lambda *a, **kw: mock_client)
    await update_queue("test-name", concurrent_jobs="test-concurrent_jobs", description="test-description", reservation_plan_settings={}, status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()
