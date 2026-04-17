"""Integration tests for aws_util.ci_cd_ops against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. codebuild_triggered_deploy
# ---------------------------------------------------------------------------


class TestCodebuildTriggeredDeploy:
    @pytest.mark.skip(reason="CodeBuild/CodeDeploy not available in LocalStack community")
    def test_starts_build_and_triggers_deploy(self, s3_bucket):
        from aws_util.ci_cd_ops import codebuild_triggered_deploy

        # Upload a dummy source artifact
        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="artifacts/source.zip", Body=b"PK\x03\x04")

        result = codebuild_triggered_deploy(
            project_name="test-project",
            source_bucket=s3_bucket,
            source_key="artifacts/source.zip",
            application_name="test-app",
            deployment_group_name="test-dg",
            poll_interval=1,
            region_name=REGION,
        )
        assert isinstance(result.build_id, str)
        assert result.build_status in (
            "SUCCEEDED", "FAILED", "FAULT", "TIMED_OUT", "STOPPED",
        )
        # deployment_id may be None if build did not succeed
        assert result.deployment_id is None or isinstance(result.deployment_id, str)


# ---------------------------------------------------------------------------
# 2. codepipeline_approval_notifier
# ---------------------------------------------------------------------------


class TestCodepipelineApprovalNotifier:
    @pytest.mark.skip(reason="CodePipeline not available in LocalStack community")
    def test_detects_pending_approvals_and_sends_emails(self, dynamodb_pk_table):
        from aws_util.ci_cd_ops import codepipeline_approval_notifier

        result = codepipeline_approval_notifier(
            pipeline_name="test-pipeline",
            table_name=dynamodb_pk_table,
            from_email="sender@example.com",
            to_emails=["recipient@example.com"],
            region_name=REGION,
        )
        assert result.pending_approvals >= 0
        assert result.emails_sent >= 0
        assert isinstance(result.approval_tokens, list)


# ---------------------------------------------------------------------------
# 3. codecommit_pr_to_codebuild
# ---------------------------------------------------------------------------


class TestCodecommitPrToCodebuild:
    @pytest.mark.skip(reason="CodeCommit/CodeBuild not available in LocalStack community")
    def test_triggers_build_from_pr_and_posts_comment(self):
        from aws_util.ci_cd_ops import codecommit_pr_to_codebuild

        result = codecommit_pr_to_codebuild(
            repository_name="test-repo",
            pull_request_id="1",
            project_name="test-project",
            source_reference="feature-branch",
            region_name=REGION,
        )
        assert isinstance(result.build_id, str)
        assert result.build_status in (
            "SUCCEEDED", "FAILED", "FAULT", "TIMED_OUT", "STOPPED",
        )
        assert isinstance(result.comment_id, str)


# ---------------------------------------------------------------------------
# 4. codeartifact_package_promoter
# ---------------------------------------------------------------------------


class TestCodeartifactPackagePromoter:
    @pytest.mark.skip(reason="CodeArtifact not available in LocalStack community")
    def test_promotes_package_and_updates_ssm(self):
        from aws_util.ci_cd_ops import codeartifact_package_promoter

        result = codeartifact_package_promoter(
            source_domain="src-domain",
            source_repository="src-repo",
            dest_domain="dst-domain",
            dest_repository="dst-repo",
            package_format="pypi",
            package_name="my-library",
            package_version="1.0.0",
            ssm_parameter_name="/allowed-packages",
            region_name=REGION,
        )
        assert result.package_name == "my-library"
        assert result.version == "1.0.0"
        assert isinstance(result.promoted, bool)
        assert isinstance(result.ssm_updated, bool)
