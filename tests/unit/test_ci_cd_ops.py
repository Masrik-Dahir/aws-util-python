"""Tests for aws_util.ci_cd_ops module."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.ci_cd_ops as mod
from aws_util.ci_cd_ops import (
    ApprovalNotifyResult,
    CIDeployResult,
    PRBuildResult,
    PackagePromoteResult,
    codeartifact_package_promoter,
    codebuild_triggered_deploy,
    codecommit_pr_to_codebuild,
    codepipeline_approval_notifier,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str = "AccessDenied", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestCIDeployResult:
    def test_create(self) -> None:
        r = CIDeployResult(
            build_id="build:1",
            build_status="SUCCEEDED",
            deployment_id="d-123",
            deployment_status="Created",
        )
        assert r.build_id == "build:1"
        assert r.deployment_id == "d-123"

    def test_frozen(self) -> None:
        r = CIDeployResult(
            build_id="b", build_status="s", deployment_id=None, deployment_status=None
        )
        with pytest.raises(Exception):
            r.build_id = "x"  # type: ignore[misc]


class TestApprovalNotifyResult:
    def test_create(self) -> None:
        r = ApprovalNotifyResult(
            pending_approvals=2, emails_sent=4, approval_tokens=["t1", "t2"]
        )
        assert r.pending_approvals == 2
        assert len(r.approval_tokens) == 2


class TestPRBuildResult:
    def test_create(self) -> None:
        r = PRBuildResult(build_id="b:1", build_status="SUCCEEDED", comment_id="c-1")
        assert r.comment_id == "c-1"


class TestPackagePromoteResult:
    def test_create(self) -> None:
        r = PackagePromoteResult(
            package_name="pkg", version="1.0.0", promoted=True, ssm_updated=True
        )
        assert r.promoted is True


# ---------------------------------------------------------------------------
# codebuild_triggered_deploy
# ---------------------------------------------------------------------------


class TestCodebuildTriggeredDeploy:
    def _factory(self, cb: MagicMock, cd: MagicMock):
        def get_client(service: str, region=None):
            if service == "codebuild":
                return cb
            if service == "codedeploy":
                return cd
            return MagicMock()

        return get_client

    def test_success_build_and_deploy(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, strftime=MagicMock(), gmtime=MagicMock()))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:abc", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.return_value = {
            "builds": [{"buildStatus": "SUCCEEDED"}]
        }
        cd = _mock()
        cd.create_deployment.return_value = {"deploymentId": "d-xyz"}
        cd.get_deployment.return_value = {
            "deploymentInfo": {"status": "Created"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        result = codebuild_triggered_deploy(
            project_name="proj",
            source_bucket="bucket",
            source_key="key.zip",
            application_name="app",
            deployment_group_name="dg",
            region_name=REGION,
        )
        assert isinstance(result, CIDeployResult)
        assert result.build_id == "proj:abc"
        assert result.build_status == "SUCCEEDED"
        assert result.deployment_id == "d-xyz"
        assert result.deployment_status == "Created"
        cb.start_build.assert_called_once()
        cd.create_deployment.assert_called_once()

    def test_build_failed_skips_deploy(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:def", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.return_value = {
            "builds": [{"buildStatus": "FAILED"}]
        }
        cd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        result = codebuild_triggered_deploy(
            project_name="proj",
            source_bucket="b",
            source_key="k.zip",
            application_name="app",
            deployment_group_name="dg",
        )
        assert result.build_status == "FAILED"
        assert result.deployment_id is None
        assert result.deployment_status is None
        cd.create_deployment.assert_not_called()

    def test_start_build_client_error(self, monkeypatch) -> None:
        cb = _mock()
        cb.start_build.side_effect = _client_error("InvalidInputException")
        cd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        with pytest.raises(RuntimeError, match="Failed to start CodeBuild"):
            codebuild_triggered_deploy(
                "proj", "b", "k.zip", "app", "dg", region_name=REGION
            )

    def test_poll_client_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:abc", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.side_effect = _client_error("ThrottlingException")
        cd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        with pytest.raises(RuntimeError, match="Failed to poll CodeBuild"):
            codebuild_triggered_deploy("proj", "b", "k.zip", "app", "dg")

    def test_deploy_client_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:abc", "buildStatus": "SUCCEEDED"}
        }
        cd = _mock()
        cd.create_deployment.side_effect = _client_error("DeploymentGroupDoesNotExistException")
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        with pytest.raises(RuntimeError, match="Failed to create CodeDeploy"):
            codebuild_triggered_deploy("proj", "b", "k.zip", "app", "dg")

    def test_build_already_terminal(self, monkeypatch) -> None:
        """Build that returns as terminal immediately (no polling loop)."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:instant", "buildStatus": "STOPPED"}
        }
        cd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cb, cd))

        result = codebuild_triggered_deploy("proj", "b", "k.zip", "app", "dg")
        assert result.build_status == "STOPPED"
        cb.batch_get_builds.assert_not_called()
        cd.create_deployment.assert_not_called()


# ---------------------------------------------------------------------------
# codepipeline_approval_notifier
# ---------------------------------------------------------------------------


class TestCodepipelineApprovalNotifier:
    def _factory(self, cp: MagicMock, sesv2: MagicMock, ddb: MagicMock):
        def get_client(service: str, region=None):
            return {"codepipeline": cp, "sesv2": sesv2, "dynamodb": ddb}.get(
                service, MagicMock()
            )

        return get_client

    def test_success_with_one_approval(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "Prod",
                    "actionStates": [
                        {
                            "actionName": "ManualApproval",
                            "latestExecution": {
                                "status": "InProgress",
                                "token": "tok-123",
                            },
                        }
                    ],
                }
            ]
        }
        sesv2 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        result = codepipeline_approval_notifier(
            pipeline_name="my-pipeline",
            table_name="approvals",
            from_email="sender@example.com",
            to_emails=["dev@example.com"],
            region_name=REGION,
        )
        assert isinstance(result, ApprovalNotifyResult)
        assert result.pending_approvals == 1
        assert result.emails_sent == 1
        assert result.approval_tokens == ["tok-123"]
        sesv2.send_email.assert_called_once()
        ddb.put_item.assert_called_once()

    def test_no_pending_approvals(self, monkeypatch) -> None:
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "Build",
                    "actionStates": [
                        {
                            "actionName": "Source",
                            "latestExecution": {"status": "Succeeded"},
                        }
                    ],
                }
            ]
        }
        sesv2 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        result = codepipeline_approval_notifier(
            "pipe", "tbl", "sender@e.com", ["r@e.com"]
        )
        assert result.pending_approvals == 0
        assert result.emails_sent == 0
        assert result.approval_tokens == []
        sesv2.send_email.assert_not_called()

    def test_no_token_skipped(self, monkeypatch) -> None:
        """InProgress but no token should be skipped."""
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "S",
                    "actionStates": [
                        {
                            "actionName": "A",
                            "latestExecution": {"status": "InProgress"},
                        }
                    ],
                }
            ]
        }
        sesv2 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        result = codepipeline_approval_notifier("p", "t", "f@e.com", ["r@e.com"])
        assert result.pending_approvals == 0

    def test_get_pipeline_state_error(self, monkeypatch) -> None:
        cp = _mock()
        cp.get_pipeline_state.side_effect = _client_error("PipelineNotFoundException")
        sesv2 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        with pytest.raises(RuntimeError, match="Failed to get pipeline state"):
            codepipeline_approval_notifier("pipe", "t", "f@e.com", ["r@e.com"])

    def test_ses_send_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "S",
                    "actionStates": [
                        {
                            "actionName": "Approve",
                            "latestExecution": {
                                "status": "InProgress",
                                "token": "tok-1",
                            },
                        }
                    ],
                }
            ]
        }
        sesv2 = _mock()
        sesv2.send_email.side_effect = _client_error("MessageRejected")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        with pytest.raises(RuntimeError, match="Failed to send approval email"):
            codepipeline_approval_notifier("pipe", "t", "f@e.com", ["r@e.com"])

    def test_dynamodb_put_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "S",
                    "actionStates": [
                        {
                            "actionName": "Approve",
                            "latestExecution": {
                                "status": "InProgress",
                                "token": "tok-2",
                            },
                        }
                    ],
                }
            ]
        }
        sesv2 = _mock()
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("ConditionalCheckFailedException")
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        with pytest.raises(RuntimeError, match="Failed to record approval token"):
            codepipeline_approval_notifier("pipe", "t", "f@e.com", ["r@e.com"])

    def test_multiple_approvals(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        cp = _mock()
        cp.get_pipeline_state.return_value = {
            "stageStates": [
                {
                    "stageName": "S1",
                    "actionStates": [
                        {
                            "actionName": "A1",
                            "latestExecution": {
                                "status": "InProgress",
                                "token": "tok-a",
                            },
                        }
                    ],
                },
                {
                    "stageName": "S2",
                    "actionStates": [
                        {
                            "actionName": "A2",
                            "latestExecution": {
                                "status": "InProgress",
                                "token": "tok-b",
                            },
                        }
                    ],
                },
            ]
        }
        sesv2 = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cp, sesv2, ddb))

        result = codepipeline_approval_notifier(
            "pipe", "t", "f@e.com", ["a@e.com", "b@e.com"]
        )
        assert result.pending_approvals == 2
        assert result.emails_sent == 4  # 2 recipients x 2 approvals
        assert result.approval_tokens == ["tok-a", "tok-b"]


# ---------------------------------------------------------------------------
# codecommit_pr_to_codebuild
# ---------------------------------------------------------------------------


class TestCodecommitPrToCodebuild:
    def _factory(self, cc: MagicMock, cb: MagicMock):
        def get_client(service: str, region=None):
            return {"codecommit": cc, "codebuild": cb}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b1", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.return_value = {
            "builds": [{"buildStatus": "SUCCEEDED"}]
        }
        cc = _mock()
        cc.get_pull_request.return_value = {
            "pullRequest": {
                "pullRequestTargets": [
                    {
                        "mergeBase": "base-sha",
                        "sourceCommit": "src-sha",
                        "destinationCommit": "dest-sha",
                    }
                ]
            }
        }
        cc.post_comment_for_pull_request.return_value = {
            "comment": {"commentId": "cid-1"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        result = codecommit_pr_to_codebuild(
            repository_name="repo",
            pull_request_id="42",
            project_name="proj",
            source_reference="feature-branch",
            region_name=REGION,
        )
        assert isinstance(result, PRBuildResult)
        assert result.build_id == "proj:b1"
        assert result.build_status == "SUCCEEDED"
        assert result.comment_id == "cid-1"
        cc.post_comment_for_pull_request.assert_called_once()

    def test_start_build_error(self, monkeypatch) -> None:
        cb = _mock()
        cb.start_build.side_effect = _client_error("ResourceNotFoundException")
        cc = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        with pytest.raises(RuntimeError, match="Failed to start CodeBuild"):
            codecommit_pr_to_codebuild("repo", "1", "proj", "main")

    def test_poll_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b1", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.side_effect = _client_error()
        cc = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        with pytest.raises(RuntimeError, match="Failed to poll CodeBuild"):
            codecommit_pr_to_codebuild("repo", "1", "proj", "main")

    def test_get_pull_request_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b1", "buildStatus": "SUCCEEDED"}
        }
        cc = _mock()
        cc.get_pull_request.side_effect = _client_error("PullRequestDoesNotExistException")
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        with pytest.raises(RuntimeError, match="Failed to fetch PR"):
            codecommit_pr_to_codebuild("repo", "99", "proj", "main")

    def test_post_comment_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b1", "buildStatus": "SUCCEEDED"}
        }
        cc = _mock()
        cc.get_pull_request.return_value = {
            "pullRequest": {
                "pullRequestTargets": [
                    {"mergeBase": "m", "sourceCommit": "s", "destinationCommit": "d"}
                ]
            }
        }
        cc.post_comment_for_pull_request.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        with pytest.raises(RuntimeError, match="Failed to post comment"):
            codecommit_pr_to_codebuild("repo", "1", "proj", "main")

    def test_no_targets_empty_commits(self, monkeypatch) -> None:
        """PR with no targets should still succeed with empty commit IDs."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b2", "buildStatus": "SUCCEEDED"}
        }
        cc = _mock()
        cc.get_pull_request.return_value = {
            "pullRequest": {"pullRequestTargets": []}
        }
        cc.post_comment_for_pull_request.return_value = {
            "comment": {"commentId": "cid-2"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        result = codecommit_pr_to_codebuild("repo", "1", "proj", "main")
        assert result.comment_id == "cid-2"
        # Should pass empty strings for before/after commit
        call_kwargs = cc.post_comment_for_pull_request.call_args
        assert call_kwargs.kwargs.get("beforeCommitId", call_kwargs[1].get("beforeCommitId", "")) == ""

    def test_build_failed_still_posts_comment(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        cb = _mock()
        cb.start_build.return_value = {
            "build": {"id": "proj:b3", "buildStatus": "IN_PROGRESS"}
        }
        cb.batch_get_builds.return_value = {
            "builds": [{"buildStatus": "FAILED"}]
        }
        cc = _mock()
        cc.get_pull_request.return_value = {
            "pullRequest": {
                "pullRequestTargets": [
                    {"mergeBase": "m", "sourceCommit": "s"}
                ]
            }
        }
        cc.post_comment_for_pull_request.return_value = {
            "comment": {"commentId": "cid-3"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(cc, cb))

        result = codecommit_pr_to_codebuild("repo", "1", "proj", "main")
        assert result.build_status == "FAILED"
        cc.post_comment_for_pull_request.assert_called_once()


# ---------------------------------------------------------------------------
# codeartifact_package_promoter
# ---------------------------------------------------------------------------


class TestCodeartifactPackagePromoter:
    def _factory(self, ca: MagicMock, ssm: MagicMock):
        def get_client(service: str, region=None):
            return {"codeartifact": ca, "ssm": ssm}.get(service, MagicMock())

        return get_client

    def test_success_new_entry(self, monkeypatch) -> None:
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": json.dumps(["other==1.0.0"])}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            source_domain="src-domain",
            source_repository="src-repo",
            dest_domain="dst-domain",
            dest_repository="dst-repo",
            package_format="pypi",
            package_name="mylib",
            package_version="2.0.0",
            ssm_parameter_name="/packages/allowed",
            region_name=REGION,
        )
        assert isinstance(result, PackagePromoteResult)
        assert result.promoted is True
        assert result.ssm_updated is True
        assert result.package_name == "mylib"
        assert result.version == "2.0.0"
        ca.copy_package_versions.assert_called_once()
        ssm.put_parameter.assert_called_once()

    def test_already_in_list_skips_update(self, monkeypatch) -> None:
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": json.dumps(["mylib==2.0.0"])}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            "sd", "sr", "dd", "dr", "pypi", "mylib", "2.0.0", "/param"
        )
        assert result.promoted is True
        assert result.ssm_updated is False
        ssm.put_parameter.assert_not_called()

    def test_copy_error(self, monkeypatch) -> None:
        ca = _mock()
        ca.copy_package_versions.side_effect = _client_error("ResourceNotFoundException")
        ssm = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        with pytest.raises(RuntimeError, match="Failed to copy"):
            codeartifact_package_promoter(
                "sd", "sr", "dd", "dr", "pypi", "pkg", "1.0.0", "/p"
            )

    def test_ssm_get_parameter_not_found(self, monkeypatch) -> None:
        """ParameterNotFound should start a fresh list."""
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.side_effect = _client_error("ParameterNotFound")
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            "sd", "sr", "dd", "dr", "npm", "pkg", "3.0.0", "/p"
        )
        assert result.promoted is True
        assert result.ssm_updated is True
        ssm.put_parameter.assert_called_once()
        # Verify the put_parameter value is a JSON list with just the new entry
        call_kwargs = ssm.put_parameter.call_args
        value = call_kwargs.kwargs.get("Value") or call_kwargs[1].get("Value")
        assert json.loads(value) == ["pkg==3.0.0"]

    def test_ssm_get_parameter_other_error(self, monkeypatch) -> None:
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        with pytest.raises(RuntimeError, match="Failed to get SSM parameter"):
            codeartifact_package_promoter(
                "sd", "sr", "dd", "dr", "npm", "pkg", "1.0.0", "/p"
            )

    def test_ssm_put_parameter_error(self, monkeypatch) -> None:
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": json.dumps([])}
        }
        ssm.put_parameter.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        with pytest.raises(RuntimeError, match="Failed to update SSM parameter"):
            codeartifact_package_promoter(
                "sd", "sr", "dd", "dr", "npm", "pkg", "1.0.0", "/p"
            )

    def test_ssm_non_json_value(self, monkeypatch) -> None:
        """If SSM value is not valid JSON, wrap it in a list."""
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": "not-json-at-all"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            "sd", "sr", "dd", "dr", "pypi", "new-pkg", "1.0.0", "/p"
        )
        assert result.ssm_updated is True
        call_kwargs = ssm.put_parameter.call_args
        value = call_kwargs.kwargs.get("Value") or call_kwargs[1].get("Value")
        parsed = json.loads(value)
        assert "not-json-at-all" in parsed
        assert "new-pkg==1.0.0" in parsed

    def test_ssm_json_non_list_value(self, monkeypatch) -> None:
        """If SSM value is valid JSON but not a list, wrap it."""
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": json.dumps({"key": "val"})}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            "sd", "sr", "dd", "dr", "pypi", "pkg", "1.0.0", "/p"
        )
        assert result.ssm_updated is True

    def test_ssm_empty_string_value(self, monkeypatch) -> None:
        """If SSM value is empty string, start fresh."""
        ca = _mock()
        ssm = _mock()
        ssm.get_parameter.return_value = {
            "Parameter": {"Value": ""}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(ca, ssm))

        result = codeartifact_package_promoter(
            "sd", "sr", "dd", "dr", "pypi", "pkg", "1.0.0", "/p"
        )
        assert result.ssm_updated is True
