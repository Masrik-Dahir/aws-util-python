"""Integration tests for aws_util.governance against LocalStack."""
from __future__ import annotations

import json

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. kms_key_rotation_auditor
# ---------------------------------------------------------------------------


class TestKmsKeyRotationAuditor:
    def test_audits_key_rotation(self, kms_key, s3_bucket, sns_topic):
        from aws_util.governance import kms_key_rotation_auditor

        result = kms_key_rotation_auditor(
            bucket=s3_bucket,
            report_key="kms-audit/report.json",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.total_keys, int)
        assert isinstance(result.rotation_enabled, int)
        assert isinstance(result.rotation_disabled, int)
        assert isinstance(result.report_s3_key, str)


# ---------------------------------------------------------------------------
# 2. config_rule_remediation_executor
# ---------------------------------------------------------------------------


class TestConfigRuleRemediationExecutor:
    @pytest.mark.skip(reason="AWS Config service not available on LocalStack community")
    def test_executes_remediation(self, dynamodb_table, iam_role):
        from aws_util.governance import config_rule_remediation_executor
        import io, zipfile

        # Create a Lambda function for remediation
        lam = ls_client("lambda")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(e, c): return {'status': 'remediated'}")
        try:
            lam.create_function(
                FunctionName="remediation-fn",
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except lam.exceptions.ResourceConflictException:
            pass  # function already exists

        result = config_rule_remediation_executor(
            config_rule_name="test-config-rule",
            remediation_lambda_arn="remediation-fn",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert isinstance(result.remediated_count, int)


# ---------------------------------------------------------------------------
# 3. organizations_scp_drift_detector (Organizations not available)
# ---------------------------------------------------------------------------


class TestOrganizationsScpDriftDetector:
    @pytest.mark.skip(
        reason="Organizations not available in LocalStack community"
    )
    def test_detects_scp_drift(self, s3_bucket, sns_topic):
        from aws_util.governance import organizations_scp_drift_detector

        # Upload a baseline SCP document to S3
        s3 = ls_client("s3")
        baseline = json.dumps({"p-FullAWSAccess": {"Version": "2012-10-17"}})
        s3.put_object(Bucket=s3_bucket, Key="scp-baseline.json", Body=baseline)

        result = organizations_scp_drift_detector(
            bucket=s3_bucket,
            baseline_key="scp-baseline.json",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.total_policies, int)
        assert isinstance(result.drifted_policies, int)
        assert isinstance(result.drift_details, list)


# ---------------------------------------------------------------------------
# 4. sso_permission_set_auditor (SSO Admin not available)
# ---------------------------------------------------------------------------


class TestSsoPermissionSetAuditor:
    @pytest.mark.skip(
        reason="SSO Admin not available in LocalStack community"
    )
    def test_audits_permission_sets(self, s3_bucket, sns_topic):
        from aws_util.governance import sso_permission_set_auditor

        result = sso_permission_set_auditor(
            instance_arn="arn:aws:sso:::instance/ssoins-1234567890abcdef",
            bucket=s3_bucket,
            report_key="sso-audit/report.json",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.permission_sets_count, int)
        assert isinstance(result.total_assignments, int)
        assert isinstance(result.report_s3_key, str)
