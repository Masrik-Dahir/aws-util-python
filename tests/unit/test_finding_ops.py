"""Tests for aws_util.finding_ops module — 100% function coverage."""
from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.finding_ops as mod
from aws_util.finding_ops import (
    AnomalyDetectionResult,
    DetectiveExportResult,
    FindingRouterResult,
    FindingSuppressorResult,
    InspectorFindingResult,
    MacieRemediationResult,
    access_analyzer_finding_suppressor,
    cloudtrail_anomaly_detector,
    detective_graph_exporter,
    inspector_finding_to_jira,
    macie_finding_remediation,
    security_hub_finding_router,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str, message: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": message}}, "Op")


def _mock() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_inspector_finding_result(self) -> None:
        r = InspectorFindingResult(findings_count=5, new_findings=2, emails_sent=2)
        assert r.findings_count == 5

    def test_macie_remediation_result(self) -> None:
        r = MacieRemediationResult(
            findings_count=3, remediated_count=1, buckets_affected=["b1"]
        )
        assert r.remediated_count == 1

    def test_detective_export_result(self) -> None:
        r = DetectiveExportResult(
            members_count=4, s3_key="k", glue_table_name="t"
        )
        assert r.members_count == 4

    def test_finding_router_result(self) -> None:
        r = FindingRouterResult(
            total_findings=10, critical_count=2, high_count=3, default_count=5
        )
        assert r.total_findings == 10

    def test_anomaly_detection_result(self) -> None:
        r = AnomalyDetectionResult(
            events_analyzed=100, anomalies_found=1, alert_sent=False
        )
        assert r.anomalies_found == 1

    def test_finding_suppressor_result(self) -> None:
        r = FindingSuppressorResult(
            findings_count=10, suppressed_count=3, unresolved_count=7
        )
        assert r.unresolved_count == 7


# ---------------------------------------------------------------------------
# 1. inspector_finding_to_jira
# ---------------------------------------------------------------------------


class TestInspectorFindingToJira:
    def _factory(
        self,
        inspector: MagicMock,
        ddb: MagicMock,
        ses: MagicMock,
    ):
        def _get_client(service, region_name=None):
            if service == "inspector2":
                return inspector
            if service == "dynamodb":
                return ddb
            if service == "sesv2":
                return ses
            return MagicMock()
        return _get_client

    def test_success_new_finding(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:finding-1",
                    "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-2024-001"},
                    "severity": "HIGH",
                    "title": "Test vuln",
                    "description": "A test vulnerability",
                    "resources": [{"id": "arn:resource-1"}],
                }
            ],
            "nextToken": None,
        }
        ddb = _mock()
        ddb.get_item.return_value = {}  # No existing item -> new finding
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        result = inspector_finding_to_jira(
            table_name="findings-table",
            from_email="sec@example.com",
            to_emails=["team@example.com"],
        )
        assert isinstance(result, InspectorFindingResult)
        assert result.findings_count == 1
        assert result.new_findings == 1
        assert result.emails_sent == 1
        ddb.put_item.assert_called_once()
        ses.send_email.assert_called_once()

    def test_duplicate_finding_skipped(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:f1",
                    "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-DUP"},
                    "severity": "MEDIUM",
                    "title": "Dup",
                    "description": "Dup desc",
                    "resources": [],
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.return_value = {"Item": {"cve_id": {"S": "CVE-DUP"}}}
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        result = inspector_finding_to_jira("t", "from@e.com", ["to@e.com"])
        assert result.new_findings == 0
        assert result.emails_sent == 0
        ddb.put_item.assert_not_called()
        ses.send_email.assert_not_called()

    def test_list_findings_error(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.side_effect = _client_error("AccessDeniedException")
        ddb = _mock()
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        with pytest.raises(RuntimeError, match="list_findings failed"):
            inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])

    def test_ddb_get_item_error(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:f",
                    "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-X"},
                    "severity": "LOW",
                    "title": "T",
                    "description": "D",
                    "resources": [],
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.side_effect = _client_error("ResourceNotFoundException")
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        with pytest.raises(RuntimeError, match="DynamoDB get_item failed"):
            inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])

    def test_ddb_put_item_error(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:f",
                    "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-Y"},
                    "severity": "HIGH",
                    "title": "T",
                    "description": "D",
                    "resources": [],
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.return_value = {}
        ddb.put_item.side_effect = _client_error("ValidationException")
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        with pytest.raises(RuntimeError, match="DynamoDB put_item failed"):
            inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])

    def test_ses_send_email_error(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:f",
                    "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-Z"},
                    "severity": "CRITICAL",
                    "title": "T",
                    "description": "D",
                    "resources": [{"id": "arn:r1"}],
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.return_value = {}
        ses = _mock()
        ses.send_email.side_effect = _client_error("MessageRejected")
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        with pytest.raises(RuntimeError, match="SES send_email failed"):
            inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])

    def test_pagination(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.side_effect = [
            {
                "findings": [
                    {
                        "findingArn": "arn:f1",
                        "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-A"},
                        "severity": "LOW",
                        "title": "A",
                        "description": "DA",
                        "resources": [],
                    }
                ],
                "nextToken": "tok2",
            },
            {
                "findings": [
                    {
                        "findingArn": "arn:f2",
                        "packageVulnerabilityDetails": {"vulnerabilityId": "CVE-B"},
                        "severity": "LOW",
                        "title": "B",
                        "description": "DB",
                        "resources": [],
                    }
                ],
                "nextToken": None,
            },
        ]
        ddb = _mock()
        ddb.get_item.return_value = {}
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))

        result = inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])
        assert result.findings_count == 2
        assert result.new_findings == 2

    def test_finding_without_cve_uses_finding_arn(self, monkeypatch):
        inspector = _mock()
        inspector.list_findings.return_value = {
            "findings": [
                {
                    "findingArn": "arn:f-no-cve",
                    "packageVulnerabilityDetails": {},
                    "severity": "MEDIUM",
                    "title": "No CVE",
                    "description": "Missing CVE",
                    "resources": [],
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.return_value = {}
        ses = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(inspector, ddb, ses))
        result = inspector_finding_to_jira("t", "f@e.com", ["t@e.com"])
        assert result.new_findings == 1


# ---------------------------------------------------------------------------
# 2. macie_finding_remediation
# ---------------------------------------------------------------------------


class TestMacieFindingRemediation:
    def _factory(self, macie, s3, ddb):
        def _get_client(service, region_name=None):
            if service == "macie2":
                return macie
            if service == "s3":
                return s3
            if service == "dynamodb":
                return ddb
            return MagicMock()
        return _get_client

    def test_success(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {
            "findingIds": ["f1"],
            "nextToken": None,
        }
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "sensitive-bucket"},
                        "s3Object": {"key": "data.csv"},
                    },
                }
            ]
        }
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))

        result = macie_finding_remediation(table_name="remediation-log")
        assert isinstance(result, MacieRemediationResult)
        assert result.findings_count == 1
        assert result.remediated_count == 1
        assert "sensitive-bucket" in result.buckets_affected
        s3.put_public_access_block.assert_called_once()
        ddb.put_item.assert_called_once()

    def test_list_findings_error(self, monkeypatch):
        macie = _mock()
        macie.list_findings.side_effect = _client_error("AccessDeniedException")
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        with pytest.raises(RuntimeError, match="list_findings failed"):
            macie_finding_remediation("t")

    def test_get_findings_error(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {
            "findingIds": ["f1"],
            "nextToken": None,
        }
        macie.get_findings.side_effect = _client_error("InternalServerException")
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        with pytest.raises(RuntimeError, match="get_findings failed"):
            macie_finding_remediation("t")

    def test_access_denied_on_put_public_access_block(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": ["f1"]}
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "restricted-bucket"},
                        "s3Object": {"key": "x"},
                    },
                }
            ]
        }
        s3 = _mock()
        s3.put_public_access_block.side_effect = _client_error("AccessDenied")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))

        result = macie_finding_remediation("t")
        # AccessDenied is logged but not raised
        assert result.remediated_count == 0

    def test_other_s3_error_raises(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": ["f1"]}
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "bk"},
                        "s3Object": {"key": "x"},
                    },
                }
            ]
        }
        s3 = _mock()
        s3.put_public_access_block.side_effect = _client_error("InternalError")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        with pytest.raises(RuntimeError, match="put_public_access_block failed"):
            macie_finding_remediation("t")

    def test_ddb_put_item_error(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": ["f1"]}
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "bk"},
                        "s3Object": {"key": "x"},
                    },
                }
            ]
        }
        s3 = _mock()
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("ValidationException")
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        with pytest.raises(RuntimeError, match="DynamoDB put_item failed"):
            macie_finding_remediation("t")

    def test_no_bucket_name_skips(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": ["f1"]}
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "LOW"},
                    "resourcesAffected": {
                        "s3Bucket": {},
                        "s3Object": {},
                    },
                }
            ]
        }
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        result = macie_finding_remediation("t")
        assert result.remediated_count == 0
        s3.put_public_access_block.assert_not_called()

    def test_already_remediated_bucket(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": ["f1", "f2"]}
        macie.get_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "same-bucket"},
                        "s3Object": {"key": "a.csv"},
                    },
                },
                {
                    "id": "f2",
                    "severity": {"description": "HIGH"},
                    "resourcesAffected": {
                        "s3Bucket": {"name": "same-bucket"},
                        "s3Object": {"key": "b.csv"},
                    },
                },
            ]
        }
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        result = macie_finding_remediation("t")
        assert result.remediated_count == 1
        # put_public_access_block called only once for the same bucket
        s3.put_public_access_block.assert_called_once()
        # But DynamoDB should have 2 put_item calls
        assert ddb.put_item.call_count == 2

    def test_empty_finding_ids(self, monkeypatch):
        macie = _mock()
        macie.list_findings.return_value = {"findingIds": []}
        s3 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(macie, s3, ddb))
        result = macie_finding_remediation("t")
        assert result.findings_count == 0


# ---------------------------------------------------------------------------
# 3. detective_graph_exporter
# ---------------------------------------------------------------------------


class TestDetectiveGraphExporter:
    def _factory(self, detective, s3, glue):
        def _get_client(service, region_name=None):
            if service == "detective":
                return detective
            if service == "s3":
                return s3
            if service == "glue":
                return glue
            return MagicMock()
        return _get_client

    def test_success(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {
            "MemberDetails": [
                {
                    "AccountId": "111",
                    "EmailAddress": "a@b.com",
                    "GraphArn": "arn:graph",
                    "Status": "ENABLED",
                    "DisabledReason": "",
                }
            ],
            "NextToken": None,
        }
        s3 = _mock()
        glue = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))

        result = detective_graph_exporter(
            graph_arn="arn:graph",
            bucket="export-bucket",
            key_prefix="detective/exports",
            database_name="security_db",
            table_name_prefix="det",
        )
        assert isinstance(result, DetectiveExportResult)
        assert result.members_count == 1
        assert result.s3_key == "detective/exports/graph_members.json"
        assert result.glue_table_name == "det_graph_members"
        s3.put_object.assert_called_once()
        glue.create_database.assert_called_once()
        glue.create_table.assert_called_once()

    def test_list_members_error(self, monkeypatch):
        detective = _mock()
        detective.list_members.side_effect = _client_error("AccessDeniedException")
        s3 = _mock()
        glue = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        with pytest.raises(RuntimeError, match="list_members failed"):
            detective_graph_exporter("arn:g", "b", "k", "db", "t")

    def test_s3_put_error(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        glue = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        with pytest.raises(RuntimeError, match="S3 put_object failed"):
            detective_graph_exporter("arn:g", "b", "k", "db", "t")

    def test_glue_database_already_exists(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        glue = _mock()
        glue.create_database.side_effect = _client_error("AlreadyExistsException")
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        # Should not raise — AlreadyExistsException is ignored
        result = detective_graph_exporter("arn:g", "b", "k", "db", "t")
        assert result.members_count == 0

    def test_glue_database_other_error(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        glue = _mock()
        glue.create_database.side_effect = _client_error("AccessDeniedException")
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        with pytest.raises(RuntimeError, match="Glue create_database failed"):
            detective_graph_exporter("arn:g", "b", "k", "db", "t")

    def test_glue_table_already_exists_updates(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        glue = _mock()
        glue.create_table.side_effect = _client_error("AlreadyExistsException")
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        result = detective_graph_exporter("arn:g", "b", "k", "db", "t")
        glue.update_table.assert_called_once()
        assert result.members_count == 0

    def test_glue_table_update_error(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        glue = _mock()
        glue.create_table.side_effect = _client_error("AlreadyExistsException")
        glue.update_table.side_effect = _client_error("AccessDeniedException")
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        with pytest.raises(RuntimeError, match="Glue update_table failed"):
            detective_graph_exporter("arn:g", "b", "k", "db", "t")

    def test_glue_create_table_other_error(self, monkeypatch):
        detective = _mock()
        detective.list_members.return_value = {"MemberDetails": []}
        s3 = _mock()
        glue = _mock()
        glue.create_table.side_effect = _client_error("InternalServiceException")
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        with pytest.raises(RuntimeError, match="Glue create_table failed"):
            detective_graph_exporter("arn:g", "b", "k", "db", "t")

    def test_pagination(self, monkeypatch):
        detective = _mock()
        detective.list_members.side_effect = [
            {
                "MemberDetails": [{"AccountId": "111", "Status": "ENABLED"}],
                "NextToken": "tok2",
            },
            {
                "MemberDetails": [{"AccountId": "222", "Status": "ENABLED"}],
            },
        ]
        s3 = _mock()
        glue = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(detective, s3, glue))
        result = detective_graph_exporter("arn:g", "b", "k", "db", "t")
        assert result.members_count == 2


# ---------------------------------------------------------------------------
# 4. security_hub_finding_router
# ---------------------------------------------------------------------------


class TestSecurityHubFindingRouter:
    def _factory(self, hub, sqs):
        def _get_client(service, region_name=None):
            if service == "securityhub":
                return hub
            if service == "sqs":
                return sqs
            return MagicMock()
        return _get_client

    def test_success_routes_by_severity(self, monkeypatch):
        hub = _mock()
        hub.get_findings.return_value = {
            "Findings": [
                {
                    "Id": "f1",
                    "Severity": {"Label": "CRITICAL"},
                    "Title": "Crit finding",
                    "Description": "desc",
                    "AwsAccountId": "111",
                    "Region": "us-east-1",
                    "Resources": [{"Id": "arn:r1"}],
                },
                {
                    "Id": "f2",
                    "Severity": {"Label": "HIGH"},
                    "Title": "High finding",
                    "Description": "desc",
                    "AwsAccountId": "111",
                    "Region": "us-east-1",
                    "Resources": [],
                },
                {
                    "Id": "f3",
                    "Severity": {"Label": "MEDIUM"},
                    "Title": "Med finding",
                    "Description": "desc",
                    "AwsAccountId": "111",
                    "Region": "us-east-1",
                    "Resources": [],
                },
            ],
            "NextToken": None,
        }
        sqs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))

        result = security_hub_finding_router(
            critical_queue_url="https://sqs/critical",
            high_queue_url="https://sqs/high",
            default_queue_url="https://sqs/default",
        )
        assert isinstance(result, FindingRouterResult)
        assert result.total_findings == 3
        assert result.critical_count == 1
        assert result.high_count == 1
        assert result.default_count == 1
        # 3 queues, each with 1 finding = 3 send_message_batch calls
        assert sqs.send_message_batch.call_count == 3

    def test_get_findings_error(self, monkeypatch):
        hub = _mock()
        hub.get_findings.side_effect = _client_error("AccessDeniedException")
        sqs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))
        with pytest.raises(RuntimeError, match="get_findings failed"):
            security_hub_finding_router("c", "h", "d")

    def test_sqs_send_error(self, monkeypatch):
        hub = _mock()
        hub.get_findings.return_value = {
            "Findings": [
                {
                    "Id": "f1",
                    "Severity": {"Label": "CRITICAL"},
                    "Title": "T",
                    "Description": "D",
                    "Resources": [],
                }
            ]
        }
        sqs = _mock()
        sqs.send_message_batch.side_effect = _client_error("AccessDenied")
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))
        with pytest.raises(RuntimeError, match="SQS send_message_batch failed"):
            security_hub_finding_router("c", "h", "d")

    def test_empty_findings(self, monkeypatch):
        hub = _mock()
        hub.get_findings.return_value = {"Findings": []}
        sqs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))
        result = security_hub_finding_router("c", "h", "d")
        assert result.total_findings == 0
        sqs.send_message_batch.assert_not_called()

    def test_custom_filters(self, monkeypatch):
        hub = _mock()
        hub.get_findings.return_value = {"Findings": []}
        sqs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))
        result = security_hub_finding_router(
            "c", "h", "d",
            filters={"SeverityLabel": [{"Value": "CRITICAL", "Comparison": "EQUALS"}]},
        )
        assert result.total_findings == 0

    def test_pagination(self, monkeypatch):
        hub = _mock()
        hub.get_findings.side_effect = [
            {
                "Findings": [
                    {"Id": "f1", "Severity": {"Label": "LOW"}, "Title": "T",
                     "Description": "D", "Resources": []}
                ],
                "NextToken": "tok2",
            },
            {
                "Findings": [
                    {"Id": "f2", "Severity": {"Label": "INFORMATIONAL"}, "Title": "T",
                     "Description": "D", "Resources": []}
                ],
            },
        ]
        sqs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(hub, sqs))
        result = security_hub_finding_router("c", "h", "d")
        assert result.total_findings == 2
        assert result.default_count == 2


# ---------------------------------------------------------------------------
# 5. cloudtrail_anomaly_detector
# ---------------------------------------------------------------------------


class TestCloudtrailAnomalyDetector:
    def _factory(self, ct, sns=None):
        def _get_client(service, region_name=None):
            if service == "cloudtrail":
                return ct
            if service == "sns":
                return sns or MagicMock()
            return MagicMock()
        return _get_client

    def test_no_events_no_anomalies(self, monkeypatch):
        ct = _mock()
        ct.lookup_events.return_value = {"Events": []}
        monkeypatch.setattr(mod, "get_client", self._factory(ct))

        result = cloudtrail_anomaly_detector()
        assert isinstance(result, AnomalyDetectionResult)
        assert result.events_analyzed == 0
        assert result.anomalies_found == 0
        assert result.alert_sent is False

    def test_high_error_rate_anomaly(self, monkeypatch):
        events = []
        for i in range(10):
            ct_event = {"errorCode": "AccessDenied"} if i < 5 else {}
            events.append({
                "EventName": "DescribeInstances",
                "CloudTrailEvent": json.dumps(ct_event),
            })
        ct = _mock()
        ct.lookup_events.return_value = {"Events": events}
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ct, sns))

        result = cloudtrail_anomaly_detector(
            error_rate_threshold=0.3,
            sns_topic_arn="arn:sns:topic",
        )
        assert result.anomalies_found >= 1
        assert result.alert_sent is True
        found_types = [a["anomaly_type"] for a in result.anomaly_details]
        assert "HIGH_ERROR_RATE" in found_types

    def test_unusual_api_calls_anomaly(self, monkeypatch):
        events = [
            {"EventName": "DeleteTrail", "CloudTrailEvent": "{}"},
            {"EventName": "CreateUser", "CloudTrailEvent": "{}"},
            {"EventName": "DescribeInstances", "CloudTrailEvent": "{}"},
        ]
        ct = _mock()
        ct.lookup_events.return_value = {"Events": events}
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ct, sns))

        result = cloudtrail_anomaly_detector(sns_topic_arn="arn:sns:t")
        found_types = [a["anomaly_type"] for a in result.anomaly_details]
        assert "UNUSUAL_API_CALLS" in found_types

    def test_unusual_regions_anomaly(self, monkeypatch):
        events = [
            {"EventName": "X", "CloudTrailEvent": json.dumps({"awsRegion": "us-east-1"})},
            {"EventName": "X", "CloudTrailEvent": json.dumps({"awsRegion": "us-east-1"})},
            {"EventName": "X", "CloudTrailEvent": json.dumps({"awsRegion": "cn-north-1"})},
        ]
        ct = _mock()
        ct.lookup_events.return_value = {"Events": events}
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ct, sns))

        result = cloudtrail_anomaly_detector(sns_topic_arn="arn:t")
        found_types = [a["anomaly_type"] for a in result.anomaly_details]
        assert "UNUSUAL_REGIONS" in found_types

    def test_lookup_events_error(self, monkeypatch):
        ct = _mock()
        ct.lookup_events.side_effect = _client_error("InvalidTimeRangeException")
        monkeypatch.setattr(mod, "get_client", self._factory(ct))
        with pytest.raises(RuntimeError, match="lookup_events failed"):
            cloudtrail_anomaly_detector()

    def test_sns_publish_error(self, monkeypatch):
        events = [
            {"EventName": "DeleteTrail", "CloudTrailEvent": "{}"},
        ]
        ct = _mock()
        ct.lookup_events.return_value = {"Events": events}
        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(ct, sns))
        with pytest.raises(RuntimeError, match="SNS publish failed"):
            cloudtrail_anomaly_detector(sns_topic_arn="arn:t")

    def test_no_alert_without_topic(self, monkeypatch):
        events = [
            {"EventName": "DeleteTrail", "CloudTrailEvent": "{}"},
        ]
        ct = _mock()
        ct.lookup_events.return_value = {"Events": events}
        monkeypatch.setattr(mod, "get_client", self._factory(ct))
        result = cloudtrail_anomaly_detector()
        assert result.alert_sent is False
        assert result.anomalies_found >= 1

    def test_pagination(self, monkeypatch):
        ct = _mock()
        ct.lookup_events.side_effect = [
            {"Events": [{"EventName": "X", "CloudTrailEvent": "{}"}], "NextToken": "t2"},
            {"Events": [{"EventName": "Y", "CloudTrailEvent": "{}"}]},
        ]
        monkeypatch.setattr(mod, "get_client", self._factory(ct))
        result = cloudtrail_anomaly_detector()
        assert result.events_analyzed == 2


# ---------------------------------------------------------------------------
# 6. access_analyzer_finding_suppressor
# ---------------------------------------------------------------------------


class TestAccessAnalyzerFindingSuppressor:
    def _factory(self, aa, ddb, logs):
        def _get_client(service, region_name=None):
            if service == "accessanalyzer":
                return aa
            if service == "dynamodb":
                return ddb
            if service == "logs":
                return logs
            return MagicMock()
        return _get_client

    def test_success_suppresses_matching(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {
                    "id": "find-1",
                    "resource": "arn:aws:s3:::approved-bucket",
                    "principal": {"AWS": "arn:aws:iam::111:root"},
                },
                {
                    "id": "find-2",
                    "resource": "arn:aws:s3:::other-bucket",
                    "principal": {},
                },
            ]
        }
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [
            {"Items": [{"pattern": {"S": "approved-bucket"}}]}
        ]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))

        result = access_analyzer_finding_suppressor(
            analyzer_arn="arn:analyzer",
            table_name="patterns-table",
            log_group_name="/analyzer/logs",
        )
        assert isinstance(result, FindingSuppressorResult)
        assert result.findings_count == 2
        assert result.suppressed_count == 1
        assert result.unresolved_count == 1
        aa.update_findings.assert_called_once()
        logs.put_log_events.assert_called_once()

    def test_no_matching_patterns(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {
                    "id": "find-1",
                    "resource": "arn:aws:s3:::bucket",
                    "principal": {},
                }
            ]
        }
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [
            {"Items": [{"pattern": {"S": "not-matching"}}]}
        ]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))

        result = access_analyzer_finding_suppressor("arn:a", "t", "/logs")
        assert result.suppressed_count == 0
        assert result.unresolved_count == 1
        logs.put_log_events.assert_not_called()

    def test_create_log_group_already_exists(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {"findings": []}
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [{"Items": []}]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        logs.create_log_group.side_effect = _client_error(
            "ResourceAlreadyExistsException"
        )
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        # Should not raise
        result = access_analyzer_finding_suppressor("arn:a", "t", "/logs")
        assert result.findings_count == 0

    def test_create_log_group_other_error(self, monkeypatch):
        aa = _mock()
        ddb = _mock()
        logs = _mock()
        logs.create_log_group.side_effect = _client_error("AccessDeniedException")
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="create_log_group failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_create_log_stream_already_exists(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {"findings": []}
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [{"Items": []}]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        logs.create_log_stream.side_effect = _client_error(
            "ResourceAlreadyExistsException"
        )
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        result = access_analyzer_finding_suppressor("arn:a", "t", "/logs")
        assert result.findings_count == 0

    def test_create_log_stream_other_error(self, monkeypatch):
        aa = _mock()
        ddb = _mock()
        logs = _mock()
        logs.create_log_stream.side_effect = _client_error("ServiceUnavailableException")
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="create_log_stream failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_ddb_scan_error(self, monkeypatch):
        aa = _mock()
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.side_effect = _client_error("ResourceNotFoundException")
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="DynamoDB scan failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_list_findings_error(self, monkeypatch):
        aa = _mock()
        aa.list_findings.side_effect = _client_error("AccessDeniedException")
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [{"Items": []}]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="list_findings failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_update_findings_error(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {"id": "f1", "resource": "arn:match-this", "principal": {}}
            ]
        }
        aa.update_findings.side_effect = _client_error("AccessDeniedException")
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [
            {"Items": [{"pattern": {"S": "match-this"}}]}
        ]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="update_findings failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_put_log_events_error(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {"id": "f1", "resource": "arn:match-this", "principal": {}}
            ]
        }
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [
            {"Items": [{"pattern": {"S": "match-this"}}]}
        ]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        logs.put_log_events.side_effect = _client_error("InvalidSequenceTokenException")
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        with pytest.raises(RuntimeError, match="put_log_events failed"):
            access_analyzer_finding_suppressor("arn:a", "t", "/logs")

    def test_principal_pattern_match(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {
                    "id": "f1",
                    "resource": "arn:unrelated",
                    "principal": {"AWS": "arn:aws:iam::trusted-account:root"},
                }
            ]
        }
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [
            {"Items": [{"pattern": {"S": "trusted-account"}}]}
        ]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        result = access_analyzer_finding_suppressor("arn:a", "t", "/logs")
        assert result.suppressed_count == 1

    def test_empty_patterns(self, monkeypatch):
        aa = _mock()
        aa.list_findings.return_value = {
            "findings": [
                {"id": "f1", "resource": "arn:r", "principal": {}}
            ]
        }
        ddb = _mock()
        ddb_paginator = _mock()
        ddb_paginator.paginate.return_value = [{"Items": []}]
        ddb.get_paginator.return_value = ddb_paginator
        logs = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(aa, ddb, logs))
        result = access_analyzer_finding_suppressor("arn:a", "t", "/logs")
        assert result.suppressed_count == 0
        assert result.unresolved_count == 1