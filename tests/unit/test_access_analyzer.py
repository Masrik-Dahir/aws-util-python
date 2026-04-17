"""Tests for aws_util.access_analyzer module."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.access_analyzer as aa_mod
from aws_util.access_analyzer import (
    AnalyzerResult,
    ArchiveRuleResult,
    FindingRecommendationResult,
    FindingResult,
    PolicyValidationResult,
    _parse_analyzer,
    _parse_archive_rule,
    _parse_finding,
    _parse_validation_finding,
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

REGION = "us-east-1"
ANALYZER_ARN = "arn:aws:access-analyzer:us-east-1:123456789012:analyzer/my-analyzer"


def _client_error(code: str, message: str = "error") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}}, "TestOp"
    )


def _mock_client() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# Model / parser tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_analyzer_result_frozen(self) -> None:
        ar = AnalyzerResult(
            arn="arn:1", name="a", type="ACCOUNT"
        )
        with pytest.raises(Exception):
            ar.name = "b"  # type: ignore[misc]

    def test_finding_result_defaults(self) -> None:
        fr = FindingResult(id="f1")
        assert fr.status == ""
        assert fr.is_public is False

    def test_archive_rule_result_frozen(self) -> None:
        ar = ArchiveRuleResult(rule_name="r1")
        assert ar.filter == {}

    def test_policy_validation_result_defaults(self) -> None:
        pv = PolicyValidationResult()
        assert pv.finding_type == ""
        assert pv.locations == []

    def test_finding_recommendation_result_defaults(self) -> None:
        fr = FindingRecommendationResult()
        assert fr.recommendation_type == ""
        assert fr.recommended_steps == []


class TestParsers:
    def test_parse_analyzer(self) -> None:
        data = {
            "arn": "arn:1",
            "name": "test",
            "type": "ACCOUNT",
            "status": "ACTIVE",
            "createdAt": "2024-01-01T00:00:00Z",
            "tags": {"env": "dev"},
            "extra_field": "val",
        }
        result = _parse_analyzer(data)
        assert result.name == "test"
        assert result.status == "ACTIVE"
        assert result.extra == {"extra_field": "val"}

    def test_parse_finding(self) -> None:
        data = {
            "id": "f1",
            "analyzerArn": "arn:1",
            "resource": "arn:r",
            "resourceType": "AWS::S3::Bucket",
            "resourceOwnerAccount": "123",
            "principal": {"AWS": "arn:root"},
            "action": ["s3:GetObject"],
            "condition": {"key": "val"},
            "status": "ACTIVE",
            "isPublic": True,
            "bonus": "data",
        }
        result = _parse_finding(data)
        assert result.id == "f1"
        assert result.is_public is True
        assert result.extra == {"bonus": "data"}

    def test_parse_archive_rule(self) -> None:
        data = {
            "ruleName": "r1",
            "filter": {"status": {"eq": ["ACTIVE"]}},
            "other": 42,
        }
        result = _parse_archive_rule(data)
        assert result.rule_name == "r1"
        assert result.extra == {"other": 42}

    def test_parse_validation_finding(self) -> None:
        data = {
            "findingType": "ERROR",
            "findingDetails": "bad",
            "issueCode": "IC1",
            "learnMoreLink": "https://example.com",
            "locations": [{"path": "/"}],
            "bonus": True,
        }
        result = _parse_validation_finding(data)
        assert result.finding_type == "ERROR"
        assert result.extra == {"bonus": True}


# ---------------------------------------------------------------------------
# create_analyzer
# ---------------------------------------------------------------------------


class TestCreateAnalyzer:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.create_analyzer.return_value = {"arn": ANALYZER_ARN}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = create_analyzer(
            "my-analyzer", region_name=REGION
        )
        assert isinstance(result, AnalyzerResult)
        assert result.arn == ANALYZER_ARN
        assert result.name == "my-analyzer"

    def test_with_tags(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.create_analyzer.return_value = {"arn": ANALYZER_ARN}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = create_analyzer(
            "my-analyzer",
            tags={"env": "prod"},
            region_name=REGION,
        )
        assert result.tags == {"env": "prod"}

    def test_with_archive_rules(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.create_analyzer.return_value = {"arn": ANALYZER_ARN}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = create_analyzer(
            "my-analyzer",
            archive_rules=[
                {
                    "ruleName": "r1",
                    "filter": {"status": {"eq": ["ACTIVE"]}},
                }
            ],
            region_name=REGION,
        )
        assert result.arn == ANALYZER_ARN

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.create_analyzer.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to create analyzer"
        ):
            create_analyzer("my-analyzer", region_name=REGION)


# ---------------------------------------------------------------------------
# get_analyzer
# ---------------------------------------------------------------------------


class TestGetAnalyzer:
    def test_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_analyzer.return_value = {
            "analyzer": {
                "arn": ANALYZER_ARN,
                "name": "my-analyzer",
                "type": "ACCOUNT",
                "status": "ACTIVE",
            }
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_analyzer("my-analyzer", region_name=REGION)
        assert result is not None
        assert result.name == "my-analyzer"

    def test_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_analyzer.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_analyzer(
            "nonexistent", region_name=REGION
        )
        assert result is None

    def test_access_denied(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_analyzer.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_analyzer failed"
        ):
            get_analyzer("my-analyzer", region_name=REGION)


# ---------------------------------------------------------------------------
# list_analyzers
# ---------------------------------------------------------------------------


class TestListAnalyzers:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "analyzers": [
                    {
                        "arn": ANALYZER_ARN,
                        "name": "a1",
                        "type": "ACCOUNT",
                        "status": "ACTIVE",
                    }
                ]
            }
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_analyzers(region_name=REGION)
        assert len(results) == 1
        assert results[0].name == "a1"

    def test_with_type_filter(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [{"analyzers": []}]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_analyzers(
            type="ACCOUNT", region_name=REGION
        )
        assert results == []

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_paginator.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_analyzers failed"
        ):
            list_analyzers(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_analyzer
# ---------------------------------------------------------------------------


class TestDeleteAnalyzer:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.delete_analyzer.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        delete_analyzer("my-analyzer", region_name=REGION)
        mock.delete_analyzer.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.delete_analyzer.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to delete analyzer"
        ):
            delete_analyzer("my-analyzer", region_name=REGION)


# ---------------------------------------------------------------------------
# update_analyzer
# ---------------------------------------------------------------------------


class TestUpdateAnalyzer:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_analyzer.return_value = {
            "analyzer": {
                "arn": ANALYZER_ARN,
                "name": "my-analyzer",
                "type": "ACCOUNT",
                "status": "ACTIVE",
            }
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = update_analyzer(
            "my-analyzer", region_name=REGION
        )
        assert result is not None
        assert result.name == "my-analyzer"

    def test_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_analyzer.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = update_analyzer(
            "nonexistent", region_name=REGION
        )
        assert result is None


# ---------------------------------------------------------------------------
# get_finding
# ---------------------------------------------------------------------------


class TestGetFinding:
    def test_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_finding.return_value = {
            "finding": {
                "id": "f1",
                "analyzerArn": ANALYZER_ARN,
                "status": "ACTIVE",
            }
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_finding(
            ANALYZER_ARN, "f1", region_name=REGION
        )
        assert result is not None
        assert result.id == "f1"

    def test_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_finding.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_finding(
            ANALYZER_ARN, "missing", region_name=REGION
        )
        assert result is None

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_finding.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_finding failed"
        ):
            get_finding(
                ANALYZER_ARN, "f1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_findings
# ---------------------------------------------------------------------------


class TestListFindings:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "findings": [
                    {
                        "id": "f1",
                        "status": "ACTIVE",
                    }
                ]
            }
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_findings(
            ANALYZER_ARN, region_name=REGION
        )
        assert len(results) == 1

    def test_with_filter_and_sort(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [{"findings": []}]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_findings(
            ANALYZER_ARN,
            filter={"status": {"eq": ["ACTIVE"]}},
            sort={"attributeName": "createdAt", "orderBy": "ASC"},
            region_name=REGION,
        )
        assert results == []

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_paginator.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_findings failed"
        ):
            list_findings(ANALYZER_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# update_findings
# ---------------------------------------------------------------------------


class TestUpdateFindings:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.update_findings.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        update_findings(
            ANALYZER_ARN,
            ["f1", "f2"],
            "ARCHIVED",
            region_name=REGION,
        )
        mock.update_findings.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.update_findings.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="update_findings failed"
        ):
            update_findings(
                ANALYZER_ARN,
                ["f1"],
                "ARCHIVED",
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# get_analyzed_resource
# ---------------------------------------------------------------------------


class TestGetAnalyzedResource:
    def test_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_analyzed_resource.return_value = {
            "resource": {"resourceArn": "arn:r", "isPublic": False}
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_analyzed_resource(
            ANALYZER_ARN, "arn:r", region_name=REGION
        )
        assert result is not None
        assert result["resourceArn"] == "arn:r"

    def test_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_analyzed_resource.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_analyzed_resource(
            ANALYZER_ARN, "arn:missing", region_name=REGION
        )
        assert result is None

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_analyzed_resource.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_analyzed_resource failed"
        ):
            get_analyzed_resource(
                ANALYZER_ARN, "arn:r", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_analyzed_resources
# ---------------------------------------------------------------------------


class TestListAnalyzedResources:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "analyzedResources": [
                    {"resourceArn": "arn:r1"},
                    {"resourceArn": "arn:r2"},
                ]
            }
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_analyzed_resources(
            ANALYZER_ARN, region_name=REGION
        )
        assert len(results) == 2

    def test_with_resource_type(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"analyzedResources": []}
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_analyzed_resources(
            ANALYZER_ARN,
            resource_type="AWS::S3::Bucket",
            region_name=REGION,
        )
        assert results == []

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_paginator.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_analyzed_resources failed"
        ):
            list_analyzed_resources(
                ANALYZER_ARN, region_name=REGION
            )


# ---------------------------------------------------------------------------
# start_resource_scan
# ---------------------------------------------------------------------------


class TestStartResourceScan:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.start_resource_scan.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        start_resource_scan(
            ANALYZER_ARN, "arn:r", region_name=REGION
        )
        mock.start_resource_scan.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.start_resource_scan.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="start_resource_scan failed"
        ):
            start_resource_scan(
                ANALYZER_ARN, "arn:r", region_name=REGION
            )


# ---------------------------------------------------------------------------
# create_archive_rule
# ---------------------------------------------------------------------------


class TestCreateArchiveRule:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.create_archive_rule.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        create_archive_rule(
            "my-analyzer",
            "my-rule",
            {"status": {"eq": ["ARCHIVED"]}},
            region_name=REGION,
        )
        mock.create_archive_rule.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.create_archive_rule.side_effect = _client_error(
            "ConflictException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to create archive rule"
        ):
            create_archive_rule(
                "a", "r", {}, region_name=REGION
            )


# ---------------------------------------------------------------------------
# get_archive_rule
# ---------------------------------------------------------------------------


class TestGetArchiveRule:
    def test_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_archive_rule.return_value = {
            "archiveRule": {
                "ruleName": "r1",
                "filter": {"status": {"eq": ["ACTIVE"]}},
            }
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_archive_rule(
            "my-analyzer", "r1", region_name=REGION
        )
        assert result is not None
        assert result.rule_name == "r1"

    def test_not_found(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_archive_rule.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = get_archive_rule(
            "my-analyzer", "missing", region_name=REGION
        )
        assert result is None

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_archive_rule.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_archive_rule failed"
        ):
            get_archive_rule(
                "my-analyzer", "r1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_archive_rules
# ---------------------------------------------------------------------------


class TestListArchiveRules:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "archiveRules": [
                    {"ruleName": "r1", "filter": {}},
                    {"ruleName": "r2", "filter": {}},
                ]
            }
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = list_archive_rules(
            "my-analyzer", region_name=REGION
        )
        assert len(results) == 2

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_paginator.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_archive_rules failed"
        ):
            list_archive_rules(
                "my-analyzer", region_name=REGION
            )


# ---------------------------------------------------------------------------
# update_archive_rule
# ---------------------------------------------------------------------------


class TestUpdateArchiveRule:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.update_archive_rule.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        update_archive_rule(
            "my-analyzer",
            "r1",
            {"status": {"eq": ["ACTIVE"]}},
            region_name=REGION,
        )
        mock.update_archive_rule.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.update_archive_rule.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to update archive rule"
        ):
            update_archive_rule(
                "a", "r", {}, region_name=REGION
            )


# ---------------------------------------------------------------------------
# delete_archive_rule
# ---------------------------------------------------------------------------


class TestDeleteArchiveRule:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.delete_archive_rule.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        delete_archive_rule(
            "my-analyzer", "r1", region_name=REGION
        )
        mock.delete_archive_rule.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.delete_archive_rule.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to delete archive rule"
        ):
            delete_archive_rule(
                "a", "r", region_name=REGION
            )


# ---------------------------------------------------------------------------
# apply_archive_rule
# ---------------------------------------------------------------------------


class TestApplyArchiveRule:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.apply_archive_rule.return_value = {}
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        apply_archive_rule(
            ANALYZER_ARN, "r1", region_name=REGION
        )
        mock.apply_archive_rule.assert_called_once()

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.apply_archive_rule.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="Failed to apply archive rule"
        ):
            apply_archive_rule(
                ANALYZER_ARN, "r1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# validate_policy
# ---------------------------------------------------------------------------


class TestValidatePolicy:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "findings": [
                    {
                        "findingType": "WARNING",
                        "findingDetails": "Allow with star",
                        "issueCode": "W1",
                    }
                ]
            }
        ]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = validate_policy(
            '{"Version":"2012-10-17","Statement":[]}',
            region_name=REGION,
        )
        assert len(results) == 1
        assert results[0].finding_type == "WARNING"

    def test_with_locale_and_resource_type(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        paginator = MagicMock()
        paginator.paginate.return_value = [{"findings": []}]
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        results = validate_policy(
            "{}",
            policy_type="RESOURCE_POLICY",
            locale="EN",
            validate_policy_resource_type="AWS::S3::Bucket",
            region_name=REGION,
        )
        assert results == []

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_paginator.side_effect = _client_error(
            "AccessDeniedException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="validate_policy failed"
        ):
            validate_policy("{}", region_name=REGION)


# ---------------------------------------------------------------------------
# check_access_not_granted
# ---------------------------------------------------------------------------


class TestCheckAccessNotGranted:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.check_access_not_granted.return_value = {
            "result": "PASS",
            "message": "No access granted",
            "reasons": [],
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = check_access_not_granted(
            "{}",
            [{"actions": ["s3:GetObject"]}],
            region_name=REGION,
        )
        assert result["result"] == "PASS"

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.check_access_not_granted.side_effect = _client_error(
            "InvalidParameterException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="check_access_not_granted failed"
        ):
            check_access_not_granted(
                "{}", [], region_name=REGION
            )


# ---------------------------------------------------------------------------
# check_no_new_access
# ---------------------------------------------------------------------------


class TestCheckNoNewAccess:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.check_no_new_access.return_value = {
            "result": "PASS",
            "message": "No new access",
            "reasons": [],
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = check_no_new_access(
            "{}", "{}", region_name=REGION
        )
        assert result["result"] == "PASS"

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.check_no_new_access.side_effect = _client_error(
            "InvalidParameterException"
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="check_no_new_access failed"
        ):
            check_no_new_access(
                "{}", "{}", region_name=REGION
            )


# ---------------------------------------------------------------------------
# generate_finding_recommendation
# ---------------------------------------------------------------------------


class TestGenerateFindingRecommendation:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock = _mock_client()
        mock.get_finding_recommendation.return_value = {
            "recommendationType": "UPDATE_POLICY",
            "recommendedSteps": [
                {"suggestedAction": "Remove wildcard"}
            ],
            "ResponseMetadata": {},
        }
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        result = generate_finding_recommendation(
            ANALYZER_ARN, "f1", region_name=REGION
        )
        assert isinstance(result, FindingRecommendationResult)
        assert result.recommendation_type == "UPDATE_POLICY"
        assert len(result.recommended_steps) == 1

    def test_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = _mock_client()
        mock.get_finding_recommendation.side_effect = (
            _client_error("ResourceNotFoundException")
        )
        monkeypatch.setattr(
            aa_mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="generate_finding_recommendation failed",
        ):
            generate_finding_recommendation(
                ANALYZER_ARN, "f1", region_name=REGION
            )


def test_cancel_policy_generation(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_policy_generation.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    cancel_policy_generation("test-job_id", region_name=REGION)
    mock_client.cancel_policy_generation.assert_called_once()


def test_cancel_policy_generation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_policy_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_policy_generation",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel policy generation"):
        cancel_policy_generation("test-job_id", region_name=REGION)


def test_check_no_public_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_no_public_access.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    check_no_public_access("test-policy_document", "test-resource_type", region_name=REGION)
    mock_client.check_no_public_access.assert_called_once()


def test_check_no_public_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_no_public_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "check_no_public_access",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to check no public access"):
        check_no_public_access("test-policy_document", "test-resource_type", region_name=REGION)


def test_create_access_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_preview.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    create_access_preview("test-analyzer_arn", {}, region_name=REGION)
    mock_client.create_access_preview.assert_called_once()


def test_create_access_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_access_preview",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create access preview"):
        create_access_preview("test-analyzer_arn", {}, region_name=REGION)


def test_get_access_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_preview.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_access_preview("test-access_preview_id", "test-analyzer_arn", region_name=REGION)
    mock_client.get_access_preview.assert_called_once()


def test_get_access_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_access_preview",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get access preview"):
        get_access_preview("test-access_preview_id", "test-analyzer_arn", region_name=REGION)


def test_get_finding_recommendation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_recommendation.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_finding_recommendation("test-analyzer_arn", "test-id", region_name=REGION)
    mock_client.get_finding_recommendation.assert_called_once()


def test_get_finding_recommendation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_recommendation",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get finding recommendation"):
        get_finding_recommendation("test-analyzer_arn", "test-id", region_name=REGION)


def test_get_finding_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_v2.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_finding_v2("test-analyzer_arn", "test-id", region_name=REGION)
    mock_client.get_finding_v2.assert_called_once()


def test_get_finding_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_v2",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get finding v2"):
        get_finding_v2("test-analyzer_arn", "test-id", region_name=REGION)


def test_get_findings_statistics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_findings_statistics.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_findings_statistics("test-analyzer_arn", region_name=REGION)
    mock_client.get_findings_statistics.assert_called_once()


def test_get_findings_statistics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_findings_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_findings_statistics",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get findings statistics"):
        get_findings_statistics("test-analyzer_arn", region_name=REGION)


def test_get_generated_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_generated_policy.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_generated_policy("test-job_id", region_name=REGION)
    mock_client.get_generated_policy.assert_called_once()


def test_get_generated_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_generated_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_generated_policy",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get generated policy"):
        get_generated_policy("test-job_id", region_name=REGION)


def test_list_access_preview_findings(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_preview_findings.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", region_name=REGION)
    mock_client.list_access_preview_findings.assert_called_once()


def test_list_access_preview_findings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_preview_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_preview_findings",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access preview findings"):
        list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", region_name=REGION)


def test_list_access_previews(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_previews.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_access_previews("test-analyzer_arn", region_name=REGION)
    mock_client.list_access_previews.assert_called_once()


def test_list_access_previews_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_previews.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_previews",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access previews"):
        list_access_previews("test-analyzer_arn", region_name=REGION)


def test_list_findings_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_findings_v2("test-analyzer_arn", region_name=REGION)
    mock_client.list_findings_v2.assert_called_once()


def test_list_findings_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_findings_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_findings_v2",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list findings v2"):
        list_findings_v2("test-analyzer_arn", region_name=REGION)


def test_list_policy_generations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_generations.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_policy_generations(region_name=REGION)
    mock_client.list_policy_generations.assert_called_once()


def test_list_policy_generations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_generations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policy_generations",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list policy generations"):
        list_policy_generations(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_start_policy_generation(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_policy_generation.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    start_policy_generation({}, region_name=REGION)
    mock_client.start_policy_generation.assert_called_once()


def test_start_policy_generation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_policy_generation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_policy_generation",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start policy generation"):
        start_policy_generation({}, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_create_access_preview_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import create_access_preview
    mock_client = MagicMock()
    mock_client.create_access_preview.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    create_access_preview("test-analyzer_arn", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_access_preview.assert_called_once()

def test_get_finding_recommendation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import get_finding_recommendation
    mock_client = MagicMock()
    mock_client.get_finding_recommendation.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_finding_recommendation("test-analyzer_arn", "test-id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_finding_recommendation.assert_called_once()

def test_get_finding_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import get_finding_v2
    mock_client = MagicMock()
    mock_client.get_finding_v2.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_finding_v2("test-analyzer_arn", "test-id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_finding_v2.assert_called_once()

def test_get_generated_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import get_generated_policy
    mock_client = MagicMock()
    mock_client.get_generated_policy.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    get_generated_policy("test-job_id", include_resource_placeholders=True, include_service_level_template=True, region_name="us-east-1")
    mock_client.get_generated_policy.assert_called_once()

def test_list_access_preview_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import list_access_preview_findings
    mock_client = MagicMock()
    mock_client.list_access_preview_findings.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_access_preview_findings("test-access_preview_id", "test-analyzer_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_access_preview_findings.assert_called_once()

def test_list_access_previews_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import list_access_previews
    mock_client = MagicMock()
    mock_client.list_access_previews.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_access_previews("test-analyzer_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_access_previews.assert_called_once()

def test_list_findings_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import list_findings_v2
    mock_client = MagicMock()
    mock_client.list_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_findings_v2("test-analyzer_arn", filter="test-filter", max_results=1, next_token="test-next_token", sort="test-sort", region_name="us-east-1")
    mock_client.list_findings_v2.assert_called_once()

def test_list_policy_generations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import list_policy_generations
    mock_client = MagicMock()
    mock_client.list_policy_generations.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    list_policy_generations(principal_arn="test-principal_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_policy_generations.assert_called_once()

def test_start_policy_generation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.access_analyzer import start_policy_generation
    mock_client = MagicMock()
    mock_client.start_policy_generation.return_value = {}
    monkeypatch.setattr("aws_util.access_analyzer.get_client", lambda *a, **kw: mock_client)
    start_policy_generation("test-policy_generation_details", cloud_trail_details="test-cloud_trail_details", client_token="test-client_token", region_name="us-east-1")
    mock_client.start_policy_generation.assert_called_once()
