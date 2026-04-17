"""Tests for aws_util.aio.access_analyzer module."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.access_analyzer import (
    AnalyzerResult,
    ArchiveRuleResult,
    FindingRecommendationResult,
    FindingResult,
    PolicyValidationResult,
    apply_archive_rule,
    check_access_not_granted,
    check_no_new_access,
    create_analyzer,
    create_archive_rule,
    delete_analyzer,
    delete_archive_rule,
    generate_finding_recommendation,
    get_analyzed_resource,
    get_analyzer,
    get_archive_rule,
    get_finding,
    list_analyzed_resources,
    list_analyzers,
    list_archive_rules,
    list_findings,
    start_resource_scan,
    update_analyzer,
    update_archive_rule,
    update_findings,
    validate_policy,
    cancel_policy_generation,
    check_no_public_access,
    create_access_preview,
    get_access_preview,
    get_finding_recommendation,
    get_finding_v2,
    get_findings_statistics,
    get_generated_policy,
    list_access_preview_findings,
    list_access_previews,
    list_findings_v2,
    list_policy_generations,
    list_tags_for_resource,
    start_policy_generation,
    tag_resource,
    untag_resource,
)

ANALYZER_ARN = (
    "arn:aws:access-analyzer:us-east-1:123456789012:"
    "analyzer/my-analyzer"
)

_ANALYZER_RESP = {
    "analyzer": {
        "arn": ANALYZER_ARN,
        "name": "my-analyzer",
        "type": "ACCOUNT",
        "status": "ACTIVE",
    }
}


# ---------------------------------------------------------------------------
# create_analyzer
# ---------------------------------------------------------------------------


async def test_create_analyzer_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"arn": ANALYZER_ARN}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_analyzer("my-analyzer")
    assert result.arn == ANALYZER_ARN
    assert result.name == "my-analyzer"


async def test_create_analyzer_with_tags(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"arn": ANALYZER_ARN}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_analyzer(
        "my-analyzer", tags={"env": "prod"}
    )
    assert result.tags == {"env": "prod"}


async def test_create_analyzer_with_archive_rules(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"arn": ANALYZER_ARN}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_analyzer(
        "my-analyzer",
        archive_rules=[{"ruleName": "r", "filter": {}}],
    )
    assert result.arn == ANALYZER_ARN


async def test_create_analyzer_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_analyzer("a")


async def test_create_analyzer_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to create analyzer"
    ):
        await create_analyzer("a")


# ---------------------------------------------------------------------------
# get_analyzer
# ---------------------------------------------------------------------------


async def test_get_analyzer_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _ANALYZER_RESP
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_analyzer("my-analyzer")
    assert result is not None
    assert result.name == "my-analyzer"


async def test_get_analyzer_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceNotFoundException"
    )
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_analyzer("missing")
    assert result is None


async def test_get_analyzer_other_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await get_analyzer("a")


# ---------------------------------------------------------------------------
# list_analyzers
# ---------------------------------------------------------------------------


async def test_list_analyzers_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "analyzers": [
            {
                "arn": ANALYZER_ARN,
                "name": "a1",
                "type": "ACCOUNT",
                "status": "ACTIVE",
            }
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzers()
    assert len(results) == 1


async def test_list_analyzers_with_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"analyzers": []}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzers(type="ACCOUNT")
    assert results == []


async def test_list_analyzers_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "analyzers": [
                    {
                        "arn": "arn:1",
                        "name": "a1",
                        "type": "ACCOUNT",
                        "status": "ACTIVE",
                    }
                ],
                "nextToken": "tok",
            }
        return {
            "analyzers": [
                {
                    "arn": "arn:2",
                    "name": "a2",
                    "type": "ACCOUNT",
                    "status": "ACTIVE",
                }
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzers()
    assert len(results) == 2


async def test_list_analyzers_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_analyzers()


async def test_list_analyzers_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_analyzers failed"
    ):
        await list_analyzers()


# ---------------------------------------------------------------------------
# delete_analyzer
# ---------------------------------------------------------------------------


async def test_delete_analyzer_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_analyzer("my-analyzer")
    mock_client.call.assert_awaited_once()


async def test_delete_analyzer_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_analyzer("a")


async def test_delete_analyzer_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to delete analyzer"
    ):
        await delete_analyzer("a")


# ---------------------------------------------------------------------------
# update_analyzer
# ---------------------------------------------------------------------------


async def test_update_analyzer_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_get(name, **kw):
        return AnalyzerResult(
            arn=ANALYZER_ARN,
            name=name,
            type="ACCOUNT",
            status="ACTIVE",
        )

    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.get_analyzer", _fake_get
    )
    result = await update_analyzer("my-analyzer")
    assert result is not None
    assert result.name == "my-analyzer"


async def test_update_analyzer_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_get(name, **kw):
        return None

    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.get_analyzer", _fake_get
    )
    result = await update_analyzer("missing")
    assert result is None


# ---------------------------------------------------------------------------
# get_finding
# ---------------------------------------------------------------------------


async def test_get_finding_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "finding": {
            "id": "f1",
            "analyzerArn": ANALYZER_ARN,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_finding(ANALYZER_ARN, "f1")
    assert result is not None
    assert result.id == "f1"


async def test_get_finding_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceNotFoundException"
    )
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_finding(ANALYZER_ARN, "missing")
    assert result is None


async def test_get_finding_other_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await get_finding(ANALYZER_ARN, "f1")


# ---------------------------------------------------------------------------
# list_findings
# ---------------------------------------------------------------------------


async def test_list_findings_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "findings": [{"id": "f1", "status": "ACTIVE"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_findings(ANALYZER_ARN)
    assert len(results) == 1


async def test_list_findings_with_filter_sort(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"findings": []}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_findings(
        ANALYZER_ARN,
        filter={"status": {"eq": ["ACTIVE"]}},
        sort={"attributeName": "createdAt", "orderBy": "ASC"},
    )
    assert results == []


async def test_list_findings_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "findings": [{"id": "f1", "status": "ACTIVE"}],
                "nextToken": "tok",
            }
        return {
            "findings": [{"id": "f2", "status": "ACTIVE"}],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_findings(ANALYZER_ARN)
    assert len(results) == 2


async def test_list_findings_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_findings(ANALYZER_ARN)


async def test_list_findings_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_findings failed"
    ):
        await list_findings(ANALYZER_ARN)


# ---------------------------------------------------------------------------
# update_findings
# ---------------------------------------------------------------------------


async def test_update_findings_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_findings(
        ANALYZER_ARN, ["f1", "f2"], "ARCHIVED"
    )
    mock_client.call.assert_awaited_once()


async def test_update_findings_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_findings(ANALYZER_ARN, ["f1"], "ARCHIVED")


async def test_update_findings_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="update_findings failed"
    ):
        await update_findings(ANALYZER_ARN, ["f1"], "ARCHIVED")


# ---------------------------------------------------------------------------
# get_analyzed_resource
# ---------------------------------------------------------------------------


async def test_get_analyzed_resource_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "resource": {"resourceArn": "arn:r", "isPublic": False}
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_analyzed_resource(ANALYZER_ARN, "arn:r")
    assert result is not None
    assert result["resourceArn"] == "arn:r"


async def test_get_analyzed_resource_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceNotFoundException"
    )
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_analyzed_resource(
        ANALYZER_ARN, "arn:missing"
    )
    assert result is None


async def test_get_analyzed_resource_other_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await get_analyzed_resource(ANALYZER_ARN, "arn:r")


# ---------------------------------------------------------------------------
# list_analyzed_resources
# ---------------------------------------------------------------------------


async def test_list_analyzed_resources_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "analyzedResources": [
            {"resourceArn": "arn:r1"},
            {"resourceArn": "arn:r2"},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzed_resources(ANALYZER_ARN)
    assert len(results) == 2


async def test_list_analyzed_resources_with_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"analyzedResources": []}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzed_resources(
        ANALYZER_ARN, resource_type="AWS::S3::Bucket"
    )
    assert results == []


async def test_list_analyzed_resources_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "analyzedResources": [
                    {"resourceArn": "arn:r1"}
                ],
                "nextToken": "tok",
            }
        return {
            "analyzedResources": [
                {"resourceArn": "arn:r2"}
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_analyzed_resources(ANALYZER_ARN)
    assert len(results) == 2


async def test_list_analyzed_resources_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_analyzed_resources(ANALYZER_ARN)


async def test_list_analyzed_resources_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_analyzed_resources failed"
    ):
        await list_analyzed_resources(ANALYZER_ARN)


# ---------------------------------------------------------------------------
# start_resource_scan
# ---------------------------------------------------------------------------


async def test_start_resource_scan_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_resource_scan(ANALYZER_ARN, "arn:r")
    mock_client.call.assert_awaited_once()


async def test_start_resource_scan_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_resource_scan(ANALYZER_ARN, "arn:r")


async def test_start_resource_scan_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="start_resource_scan failed"
    ):
        await start_resource_scan(ANALYZER_ARN, "arn:r")


# ---------------------------------------------------------------------------
# create_archive_rule
# ---------------------------------------------------------------------------


async def test_create_archive_rule_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_archive_rule("a", "r", {"status": {"eq": ["ACTIVE"]}})
    mock_client.call.assert_awaited_once()


async def test_create_archive_rule_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_archive_rule("a", "r", {})


async def test_create_archive_rule_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to create archive rule"
    ):
        await create_archive_rule("a", "r", {})


# ---------------------------------------------------------------------------
# get_archive_rule
# ---------------------------------------------------------------------------


async def test_get_archive_rule_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "archiveRule": {
            "ruleName": "r1",
            "filter": {"status": {"eq": ["ACTIVE"]}},
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_archive_rule("a", "r1")
    assert result is not None
    assert result.rule_name == "r1"


async def test_get_archive_rule_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceNotFoundException"
    )
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_archive_rule("a", "missing")
    assert result is None


async def test_get_archive_rule_other_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await get_archive_rule("a", "r")


# ---------------------------------------------------------------------------
# list_archive_rules
# ---------------------------------------------------------------------------


async def test_list_archive_rules_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "archiveRules": [
            {"ruleName": "r1", "filter": {}},
            {"ruleName": "r2", "filter": {}},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_archive_rules("a")
    assert len(results) == 2


async def test_list_archive_rules_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "archiveRules": [
                    {"ruleName": "r1", "filter": {}}
                ],
                "nextToken": "tok",
            }
        return {
            "archiveRules": [
                {"ruleName": "r2", "filter": {}}
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await list_archive_rules("a")
    assert len(results) == 2


async def test_list_archive_rules_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_archive_rules("a")


async def test_list_archive_rules_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_archive_rules failed"
    ):
        await list_archive_rules("a")


# ---------------------------------------------------------------------------
# update_archive_rule
# ---------------------------------------------------------------------------


async def test_update_archive_rule_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_archive_rule("a", "r", {"status": {"eq": ["ACTIVE"]}})
    mock_client.call.assert_awaited_once()


async def test_update_archive_rule_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_archive_rule("a", "r", {})


async def test_update_archive_rule_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to update archive rule"
    ):
        await update_archive_rule("a", "r", {})


# ---------------------------------------------------------------------------
# delete_archive_rule
# ---------------------------------------------------------------------------


async def test_delete_archive_rule_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_archive_rule("a", "r")
    mock_client.call.assert_awaited_once()


async def test_delete_archive_rule_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_archive_rule("a", "r")


async def test_delete_archive_rule_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to delete archive rule"
    ):
        await delete_archive_rule("a", "r")


# ---------------------------------------------------------------------------
# apply_archive_rule
# ---------------------------------------------------------------------------


async def test_apply_archive_rule_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_archive_rule(ANALYZER_ARN, "r1")
    mock_client.call.assert_awaited_once()


async def test_apply_archive_rule_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_archive_rule(ANALYZER_ARN, "r")


async def test_apply_archive_rule_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="Failed to apply archive rule"
    ):
        await apply_archive_rule(ANALYZER_ARN, "r")


# ---------------------------------------------------------------------------
# validate_policy
# ---------------------------------------------------------------------------


async def test_validate_policy_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "findings": [
            {
                "findingType": "WARNING",
                "findingDetails": "Allow with star",
                "issueCode": "W1",
            }
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await validate_policy("{}")
    assert len(results) == 1
    assert results[0].finding_type == "WARNING"

async def test_validate_policy_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "findings": [
                    {
                        "findingType": "W",
                        "findingDetails": "d1",
                    }
                ],
                "nextToken": "tok",
            }
        return {
            "findings": [
                {
                    "findingType": "E",
                    "findingDetails": "d2",
                }
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    results = await validate_policy("{}")
    assert len(results) == 2


async def test_validate_policy_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_policy("{}")


async def test_validate_policy_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="validate_policy failed"
    ):
        await validate_policy("{}")


# ---------------------------------------------------------------------------
# check_access_not_granted
# ---------------------------------------------------------------------------


async def test_check_access_not_granted_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "result": "PASS",
        "message": "No access granted",
        "reasons": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await check_access_not_granted(
        "{}", [{"actions": ["s3:GetObject"]}]
    )
    assert result["result"] == "PASS"


async def test_check_access_not_granted_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_access_not_granted("{}", [])


async def test_check_access_not_granted_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="check_access_not_granted failed"
    ):
        await check_access_not_granted("{}", [])


# ---------------------------------------------------------------------------
# check_no_new_access
# ---------------------------------------------------------------------------


async def test_check_no_new_access_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "result": "PASS",
        "message": "No new access",
        "reasons": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await check_no_new_access("{}", "{}")
    assert result["result"] == "PASS"


async def test_check_no_new_access_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_no_new_access("{}", "{}")


async def test_check_no_new_access_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="check_no_new_access failed"
    ):
        await check_no_new_access("{}", "{}")


# ---------------------------------------------------------------------------
# generate_finding_recommendation
# ---------------------------------------------------------------------------


async def test_generate_finding_recommendation_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "recommendationType": "UPDATE_POLICY",
        "recommendedSteps": [
            {"suggestedAction": "Remove wildcard"}
        ],
        "ResponseMetadata": {},
    }
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await generate_finding_recommendation(
        ANALYZER_ARN, "f1"
    )
    assert isinstance(result, FindingRecommendationResult)
    assert result.recommendation_type == "UPDATE_POLICY"
    assert len(result.recommended_steps) == 1


async def test_generate_finding_recommendation_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_finding_recommendation(
            ANALYZER_ARN, "f1"
        )


async def test_generate_finding_recommendation_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="generate_finding_recommendation failed",
    ):
        await generate_finding_recommendation(
            ANALYZER_ARN, "f1"
        )


async def test_cancel_policy_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_policy_generation("test-job_id", )
    mock_client.call.assert_called_once()


async def test_cancel_policy_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_policy_generation("test-job_id", )


async def test_check_no_public_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await check_no_public_access("test-policy_document", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_check_no_public_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_no_public_access("test-policy_document", "test-resource_type", )


async def test_create_access_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_access_preview("test-analyzer_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_access_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_access_preview("test-analyzer_arn", {}, )


async def test_get_access_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_access_preview("test-access_preview_id", "test-analyzer_arn", )
    mock_client.call.assert_called_once()


async def test_get_access_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_access_preview("test-access_preview_id", "test-analyzer_arn", )


async def test_get_finding_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_finding_recommendation("test-analyzer_arn", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_finding_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_recommendation("test-analyzer_arn", "test-id", )


async def test_get_finding_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_finding_v2("test-analyzer_arn", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_finding_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_v2("test-analyzer_arn", "test-id", )


async def test_get_findings_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_findings_statistics("test-analyzer_arn", )
    mock_client.call.assert_called_once()


async def test_get_findings_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_findings_statistics("test-analyzer_arn", )


async def test_get_generated_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_generated_policy("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_generated_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_generated_policy("test-job_id", )


async def test_list_access_preview_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", )
    mock_client.call.assert_called_once()


async def test_list_access_preview_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", )


async def test_list_access_previews(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_previews("test-analyzer_arn", )
    mock_client.call.assert_called_once()


async def test_list_access_previews_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_previews("test-analyzer_arn", )


async def test_list_findings_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_findings_v2("test-analyzer_arn", )
    mock_client.call.assert_called_once()


async def test_list_findings_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_findings_v2("test-analyzer_arn", )


async def test_list_policy_generations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policy_generations()
    mock_client.call.assert_called_once()


async def test_list_policy_generations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policy_generations()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_start_policy_generation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_policy_generation({}, )
    mock_client.call.assert_called_once()


async def test_start_policy_generation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_policy_generation({}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.access_analyzer.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_list_analyzers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_analyzers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_analyzers(type="test-type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_findings("test-analyzer_arn", filter="test-filter", sort="test-sort", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_analyzed_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_analyzed_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_analyzed_resources("test-analyzer_arn", resource_type="test-resource_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import validate_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await validate_policy("test-policy_document", locale="test-locale", validate_policy_resource_type="test-validate_policy_resource_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_access_preview_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import create_access_preview
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await create_access_preview("test-analyzer_arn", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_finding_recommendation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import get_finding_recommendation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await get_finding_recommendation("test-analyzer_arn", "test-id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_finding_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import get_finding_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await get_finding_v2("test-analyzer_arn", "test-id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_generated_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import get_generated_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await get_generated_policy("test-job_id", include_resource_placeholders=True, include_service_level_template=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_preview_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_access_preview_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_previews_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_access_previews
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_access_previews("test-analyzer_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_findings_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_findings_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_findings_v2("test-analyzer_arn", filter="test-filter", max_results=1, next_token="test-next_token", sort="test-sort", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policy_generations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import list_policy_generations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await list_policy_generations(principal_arn="test-principal_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_policy_generation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.access_analyzer import start_policy_generation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.access_analyzer.async_client", lambda *a, **kw: mock_client)
    await start_policy_generation("test-policy_generation_details", cloud_trail_details="test-cloud_trail_details", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
