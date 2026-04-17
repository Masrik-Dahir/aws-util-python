"""Tests for aws_util.governance module — 100% function coverage."""
from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.governance as mod
from aws_util.governance import (
    KMSRotationAuditResult,
    RemediationResult,
    SCPDriftResult,
    SSOAuditResult,
    config_rule_remediation_executor,
    kms_key_rotation_auditor,
    organizations_scp_drift_detector,
    sso_permission_set_auditor,
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
    def test_remediation_result(self) -> None:
        r = RemediationResult(
            non_compliant_count=3, remediated_count=2, failed_count=1,
            resource_ids=["r1", "r2", "r3"],
        )
        assert r.non_compliant_count == 3

    def test_scp_drift_result(self) -> None:
        r = SCPDriftResult(total_policies=5, drifted_policies=1)
        assert r.total_policies == 5

    def test_sso_audit_result(self) -> None:
        r = SSOAuditResult(
            permission_sets_count=10, total_assignments=20, report_s3_key="k"
        )
        assert r.permission_sets_count == 10

    def test_kms_rotation_audit_result(self) -> None:
        r = KMSRotationAuditResult(
            total_keys=5, rotation_enabled=3, rotation_disabled=2,
            report_s3_key="k",
        )
        assert r.rotation_disabled == 2


# ---------------------------------------------------------------------------
# 1. config_rule_remediation_executor
# ---------------------------------------------------------------------------


class TestConfigRuleRemediationExecutor:
    def _factory(self, config_client, lambda_client, ddb):
        def _get_client(service, region_name=None):
            if service == "config":
                return config_client
            if service == "lambda":
                return lambda_client
            if service == "dynamodb":
                return ddb
            return MagicMock()
        return _get_client

    def test_success_remediated(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {
                "EvaluationResults": [
                    {
                        "EvaluationResultIdentifier": {
                            "EvaluationResultQualifier": {
                                "ResourceId": "sg-001",
                                "ResourceType": "AWS::EC2::SecurityGroup",
                            }
                        },
                        "Annotation": "Non-compliant SG",
                    }
                ]
            }
        ]
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        lambda_client.invoke.return_value = {"StatusCode": 200}
        ddb = _mock()
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )

        result = config_rule_remediation_executor(
            config_rule_name="restricted-sg",
            remediation_lambda_arn="arn:lambda:fn",
            table_name="remediation-history",
        )
        assert isinstance(result, RemediationResult)
        assert result.non_compliant_count == 1
        assert result.remediated_count == 1
        assert result.failed_count == 0
        assert result.resource_ids == ["sg-001"]
        lambda_client.invoke.assert_called_once()
        ddb.put_item.assert_called_once()

    def test_lambda_function_error(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {
                "EvaluationResults": [
                    {
                        "EvaluationResultIdentifier": {
                            "EvaluationResultQualifier": {
                                "ResourceId": "r1",
                                "ResourceType": "AWS::EC2::Instance",
                            }
                        },
                        "Annotation": "",
                    }
                ]
            }
        ]
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        lambda_client.invoke.return_value = {
            "StatusCode": 200,
            "FunctionError": "Unhandled",
        }
        ddb = _mock()
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )
        result = config_rule_remediation_executor("rule", "arn:fn", "tbl")
        assert result.remediated_count == 0
        assert result.failed_count == 1

    def test_lambda_invoke_client_error(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {
                "EvaluationResults": [
                    {
                        "EvaluationResultIdentifier": {
                            "EvaluationResultQualifier": {
                                "ResourceId": "r1",
                                "ResourceType": "AWS::EC2::Instance",
                            }
                        },
                    }
                ]
            }
        ]
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        lambda_client.invoke.side_effect = _client_error("ResourceNotFoundException")
        ddb = _mock()
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )
        result = config_rule_remediation_executor("rule", "arn:fn", "tbl")
        assert result.failed_count == 1
        assert result.remediated_count == 0

    def test_config_get_compliance_error(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.side_effect = _client_error("NoSuchConfigRuleException")
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        ddb = _mock()
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )
        with pytest.raises(RuntimeError, match="failed to get compliance details"):
            config_rule_remediation_executor("bad-rule", "arn:fn", "tbl")

    def test_ddb_put_item_error(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {
                "EvaluationResults": [
                    {
                        "EvaluationResultIdentifier": {
                            "EvaluationResultQualifier": {
                                "ResourceId": "r1",
                                "ResourceType": "T",
                            }
                        },
                    }
                ]
            }
        ]
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        lambda_client.invoke.return_value = {"StatusCode": 200}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("ValidationException")
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )
        with pytest.raises(RuntimeError, match="DynamoDB put_item failed"):
            config_rule_remediation_executor("rule", "arn:fn", "tbl")

    def test_empty_evaluations(self, monkeypatch):
        config_client = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"EvaluationResults": []}]
        config_client.get_paginator.return_value = paginator
        lambda_client = _mock()
        ddb = _mock()
        monkeypatch.setattr(
            mod, "get_client", self._factory(config_client, lambda_client, ddb)
        )
        result = config_rule_remediation_executor("rule", "arn:fn", "tbl")
        assert result.non_compliant_count == 0


# ---------------------------------------------------------------------------
# 2. organizations_scp_drift_detector
# ---------------------------------------------------------------------------


class TestOrganizationsScpDriftDetector:
    def _factory(self, orgs, s3, sns=None):
        def _get_client(service, region_name=None):
            if service == "organizations":
                return orgs
            if service == "s3":
                return s3
            if service == "sns":
                return sns or MagicMock()
            return MagicMock()
        return _get_client

    def test_no_drift(self, monkeypatch):
        policy_doc = json.dumps({"Version": "2012-10-17", "Statement": []})
        baseline = {"p-1": {"Version": "2012-10-17", "Statement": []}}

        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-1", "Name": "RestrictRoot"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.return_value = {
            "Policy": {"Content": policy_doc}
        }

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3))
        result = organizations_scp_drift_detector("bk", "baseline.json", "arn:sns")
        assert isinstance(result, SCPDriftResult)
        assert result.drifted_policies == 0

    def test_document_changed_drift(self, monkeypatch):
        baseline = {"p-1": {"Version": "2012-10-17", "Statement": [{"old": True}]}}
        current = json.dumps({"Version": "2012-10-17", "Statement": [{"new": True}]})

        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-1", "Name": "Policy1"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.return_value = {"Policy": {"Content": current}}

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3, sns))
        result = organizations_scp_drift_detector("bk", "k", "arn:sns")
        assert result.drifted_policies == 1
        assert result.drift_details[0]["drift_type"] == "DOCUMENT_CHANGED"
        sns.publish.assert_called_once()

    def test_policy_not_in_baseline(self, monkeypatch):
        baseline = {}

        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-new", "Name": "NewPolicy"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.return_value = {"Policy": {"Content": "{}"}}

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3, sns))
        result = organizations_scp_drift_detector("bk", "k", "arn:sns")
        assert result.drifted_policies == 1
        assert result.drift_details[0]["drift_type"] == "POLICY_NOT_IN_BASELINE"

    def test_policy_deleted_from_aws(self, monkeypatch):
        baseline = {"p-deleted": {"Statement": []}}

        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Policies": []}]
        orgs.get_paginator.return_value = paginator

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3, sns))
        result = organizations_scp_drift_detector("bk", "k", "arn:sns")
        assert result.drifted_policies == 1
        assert result.drift_details[0]["drift_type"] == "POLICY_DELETED_FROM_AWS"

    def test_s3_download_error(self, monkeypatch):
        orgs = _mock()
        s3 = _mock()
        s3.get_object.side_effect = _client_error("NoSuchKey")
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3))
        with pytest.raises(RuntimeError, match="failed to download baseline"):
            organizations_scp_drift_detector("bk", "k", "arn:sns")

    def test_s3_invalid_json(self, monkeypatch):
        orgs = _mock()
        s3 = _mock()
        body = _mock()
        body.read.return_value = b"not-json"
        s3.get_object.return_value = {"Body": body}
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3))
        with pytest.raises(ValueError, match="not valid JSON"):
            organizations_scp_drift_detector("bk", "k", "arn:sns")

    def test_list_policies_error(self, monkeypatch):
        orgs = _mock()
        paginator = _mock()
        paginator.paginate.side_effect = _client_error("AccessDeniedException")
        orgs.get_paginator.return_value = paginator

        s3 = _mock()
        body = _mock()
        body.read.return_value = b"{}"
        s3.get_object.return_value = {"Body": body}

        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3))
        with pytest.raises(RuntimeError, match="failed to list SCPs"):
            organizations_scp_drift_detector("bk", "k", "arn:sns")

    def test_describe_policy_error(self, monkeypatch):
        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-1", "Name": "P"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.side_effect = _client_error("PolicyNotFoundException")

        s3 = _mock()
        body = _mock()
        body.read.return_value = b"{}"
        s3.get_object.return_value = {"Body": body}

        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3))
        with pytest.raises(RuntimeError, match="describe_policy failed"):
            organizations_scp_drift_detector("bk", "k", "arn:sns")

    def test_sns_publish_error(self, monkeypatch):
        baseline = {}
        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-1", "Name": "P"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.return_value = {"Policy": {"Content": "{}"}}

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3, sns))
        with pytest.raises(RuntimeError, match="SNS publish failed"):
            organizations_scp_drift_detector("bk", "k", "arn:sns")

    def test_invalid_json_policy_document(self, monkeypatch):
        baseline = {"p-1": {"Statement": []}}
        orgs = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Policies": [{"Id": "p-1", "Name": "P"}]}
        ]
        orgs.get_paginator.return_value = paginator
        orgs.describe_policy.return_value = {
            "Policy": {"Content": "not-json"}
        }

        s3 = _mock()
        body = _mock()
        body.read.return_value = json.dumps(baseline).encode()
        s3.get_object.return_value = {"Body": body}

        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(orgs, s3, sns))
        result = organizations_scp_drift_detector("bk", "k", "arn:sns")
        # Should detect as drift (document changed)
        assert result.drifted_policies == 1


# ---------------------------------------------------------------------------
# 3. sso_permission_set_auditor
# ---------------------------------------------------------------------------


class TestSsoPermissionSetAuditor:
    def _factory(self, sso, s3, sns=None):
        def _get_client(service, region_name=None):
            if service == "sso-admin":
                return sso
            if service == "s3":
                return s3
            if service == "sns":
                return sns or MagicMock()
            return MagicMock()
        return _get_client

    def test_success(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [
            {"PermissionSets": ["arn:ps-1", "arn:ps-2"]}
        ]
        assign_paginator = _mock()
        assign_paginator.paginate.return_value = [
            {"AccountIds": ["111", "222"]}
        ]
        sso.get_paginator.side_effect = lambda name: (
            ps_paginator if name == "list_permission_sets" else assign_paginator
        )
        sso.describe_permission_set.return_value = {
            "PermissionSet": {
                "Name": "AdminAccess",
                "Description": "Full admin",
                "SessionDuration": "PT4H",
            }
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3))

        result = sso_permission_set_auditor(
            instance_arn="arn:sso:instance",
            bucket="audit-bucket",
            report_key="sso/report.json",
        )
        assert isinstance(result, SSOAuditResult)
        assert result.permission_sets_count == 2
        assert result.total_assignments == 4  # 2 accounts x 2 sets
        assert result.report_s3_key == "sso/report.json"
        s3.put_object.assert_called_once()

    def test_with_sns_notification(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [{"PermissionSets": ["arn:ps-1"]}]
        assign_paginator = _mock()
        assign_paginator.paginate.return_value = [{"AccountIds": ["111"]}]
        sso.get_paginator.side_effect = lambda name: (
            ps_paginator if name == "list_permission_sets" else assign_paginator
        )
        sso.describe_permission_set.return_value = {
            "PermissionSet": {"Name": "ReadOnly"}
        }
        s3 = _mock()
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3, sns))

        result = sso_permission_set_auditor(
            "arn:inst", "bk", "k", sns_topic_arn="arn:topic"
        )
        sns.publish.assert_called_once()
        assert result.permission_sets_count == 1

    def test_list_permission_sets_error(self, monkeypatch):
        sso = _mock()
        paginator = _mock()
        paginator.paginate.side_effect = _client_error("AccessDeniedException")
        sso.get_paginator.return_value = paginator
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3))
        with pytest.raises(RuntimeError, match="failed to list permission sets"):
            sso_permission_set_auditor("arn:inst", "bk", "k")

    def test_describe_permission_set_error(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [{"PermissionSets": ["arn:ps-1"]}]
        sso.get_paginator.return_value = ps_paginator
        sso.describe_permission_set.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3))
        with pytest.raises(RuntimeError, match="describe_permission_set failed"):
            sso_permission_set_auditor("arn:inst", "bk", "k")

    def test_list_accounts_error(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [{"PermissionSets": ["arn:ps-1"]}]
        assign_paginator = _mock()
        assign_paginator.paginate.side_effect = _client_error("InternalServerError")
        sso.get_paginator.side_effect = lambda name: (
            ps_paginator if name == "list_permission_sets" else assign_paginator
        )
        sso.describe_permission_set.return_value = {
            "PermissionSet": {"Name": "Admin"}
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3))
        with pytest.raises(RuntimeError, match="list_accounts_for_provisioned"):
            sso_permission_set_auditor("arn:inst", "bk", "k")

    def test_s3_upload_error(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [{"PermissionSets": []}]
        sso.get_paginator.return_value = ps_paginator
        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3))
        with pytest.raises(RuntimeError, match="S3 put_object failed"):
            sso_permission_set_auditor("arn:inst", "bk", "k")

    def test_sns_publish_error(self, monkeypatch):
        sso = _mock()
        ps_paginator = _mock()
        ps_paginator.paginate.return_value = [{"PermissionSets": []}]
        sso.get_paginator.return_value = ps_paginator
        s3 = _mock()
        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(sso, s3, sns))
        with pytest.raises(RuntimeError, match="SNS publish failed"):
            sso_permission_set_auditor("arn:inst", "bk", "k", sns_topic_arn="arn:t")


# ---------------------------------------------------------------------------
# 4. kms_key_rotation_auditor
# ---------------------------------------------------------------------------


class TestKmsKeyRotationAuditor:
    def _factory(self, kms, s3, sns=None):
        def _get_client(service, region_name=None):
            if service == "kms":
                return kms
            if service == "s3":
                return s3
            if service == "sns":
                return sns or MagicMock()
            return MagicMock()
        return _get_client

    def test_success_with_rotation_enabled(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Keys": [{"KeyId": "k-1"}, {"KeyId": "k-2"}]}
        ]
        kms.get_paginator.return_value = paginator
        kms.describe_key.side_effect = [
            {
                "KeyMetadata": {
                    "KeyManager": "CUSTOMER",
                    "KeyState": "Enabled",
                    "KeyUsage": "ENCRYPT_DECRYPT",
                    "Arn": "arn:k-1",
                    "Description": "Key 1",
                }
            },
            {
                "KeyMetadata": {
                    "KeyManager": "CUSTOMER",
                    "KeyState": "Enabled",
                    "KeyUsage": "ENCRYPT_DECRYPT",
                    "Arn": "arn:k-2",
                    "Description": "Key 2",
                }
            },
        ]
        kms.get_key_rotation_status.side_effect = [
            {"KeyRotationEnabled": True},
            {"KeyRotationEnabled": False},
        ]
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))

        result = kms_key_rotation_auditor(bucket="audit-bk", report_key="kms/report.json")
        assert isinstance(result, KMSRotationAuditResult)
        assert result.total_keys == 2
        assert result.rotation_enabled == 1
        assert result.rotation_disabled == 1
        assert result.report_s3_key == "kms/report.json"
        s3.put_object.assert_called_once()

    def test_with_sns_alert_on_disabled(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
                "Description": "Disabled rotation",
            }
        }
        kms.get_key_rotation_status.return_value = {"KeyRotationEnabled": False}
        s3 = _mock()
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3, sns))

        result = kms_key_rotation_auditor("bk", "k", sns_topic_arn="arn:topic")
        assert result.rotation_disabled == 1
        sns.publish.assert_called_once()

    def test_no_sns_when_all_enabled(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
            }
        }
        kms.get_key_rotation_status.return_value = {"KeyRotationEnabled": True}
        s3 = _mock()
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3, sns))
        result = kms_key_rotation_auditor("bk", "k", sns_topic_arn="arn:t")
        assert result.rotation_disabled == 0
        sns.publish.assert_not_called()

    def test_skips_aws_managed_keys(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [
            {"Keys": [{"KeyId": "k-aws"}, {"KeyId": "k-cust"}]}
        ]
        kms.get_paginator.return_value = paginator
        kms.describe_key.side_effect = [
            {"KeyMetadata": {"KeyManager": "AWS", "KeyState": "Enabled"}},
            {
                "KeyMetadata": {
                    "KeyManager": "CUSTOMER",
                    "KeyState": "Enabled",
                    "Arn": "arn:k-cust",
                }
            },
        ]
        kms.get_key_rotation_status.return_value = {"KeyRotationEnabled": True}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        result = kms_key_rotation_auditor("bk", "k")
        assert result.total_keys == 1  # only customer-managed counted

    def test_skips_pending_deletion(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "PendingDeletion",
            }
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        result = kms_key_rotation_auditor("bk", "k")
        assert result.total_keys == 0

    def test_unsupported_operation_rotation_check(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
            }
        }
        kms.get_key_rotation_status.side_effect = _client_error(
            "UnsupportedOperationException"
        )
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        result = kms_key_rotation_auditor("bk", "k")
        assert result.rotation_disabled == 1

    def test_access_denied_rotation_check(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
            }
        }
        kms.get_key_rotation_status.side_effect = _client_error(
            "AccessDeniedException"
        )
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        result = kms_key_rotation_auditor("bk", "k")
        assert result.rotation_disabled == 1

    def test_rotation_check_other_error(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
            }
        }
        kms.get_key_rotation_status.side_effect = _client_error("InternalError")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        with pytest.raises(RuntimeError, match="get_key_rotation_status failed"):
            kms_key_rotation_auditor("bk", "k")

    def test_list_keys_error(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.side_effect = _client_error("AccessDeniedException")
        kms.get_paginator.return_value = paginator
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        with pytest.raises(RuntimeError, match="failed to list keys"):
            kms_key_rotation_auditor("bk", "k")

    def test_describe_key_error(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.side_effect = _client_error("NotFoundException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        with pytest.raises(RuntimeError, match="describe_key failed"):
            kms_key_rotation_auditor("bk", "k")

    def test_s3_upload_error(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": []}]
        kms.get_paginator.return_value = paginator
        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        with pytest.raises(RuntimeError, match="S3 put_object failed"):
            kms_key_rotation_auditor("bk", "k")

    def test_sns_publish_error(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": [{"KeyId": "k-1"}]}]
        kms.get_paginator.return_value = paginator
        kms.describe_key.return_value = {
            "KeyMetadata": {
                "KeyManager": "CUSTOMER",
                "KeyState": "Enabled",
                "Arn": "arn:k-1",
            }
        }
        kms.get_key_rotation_status.return_value = {"KeyRotationEnabled": False}
        s3 = _mock()
        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3, sns))
        with pytest.raises(RuntimeError, match="SNS publish failed"):
            kms_key_rotation_auditor("bk", "k", sns_topic_arn="arn:t")

    def test_empty_keys(self, monkeypatch):
        kms = _mock()
        paginator = _mock()
        paginator.paginate.return_value = [{"Keys": []}]
        kms.get_paginator.return_value = paginator
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(kms, s3))
        result = kms_key_rotation_auditor("bk", "k")
        assert result.total_keys == 0
        assert result.rotation_enabled == 0
        assert result.rotation_disabled == 0
