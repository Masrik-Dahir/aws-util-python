"""ci_cd_ops — Multi-service CI/CD pipeline utilities.

Provides high-level helpers that span multiple AWS developer tools:

- **codebuild_triggered_deploy** — Start a CodeBuild build from an S3 artifact,
  wait for completion, then trigger a CodeDeploy deployment on success.
- **codepipeline_approval_notifier** — Detect pending CodePipeline manual-approval
  actions, send SES v2 emails, and record tokens in DynamoDB.
- **codecommit_pr_to_codebuild** — Trigger a CodeBuild build from a CodeCommit
  PR's source branch and post the result as a PR comment.
- **codeartifact_package_promoter** — Copy a package version between CodeArtifact
  repositories and update the allowed-package list in SSM Parameter Store.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "ApprovalNotifyResult",
    "CIDeployResult",
    "PRBuildResult",
    "PackagePromoteResult",
    "codeartifact_package_promoter",
    "codebuild_triggered_deploy",
    "codecommit_pr_to_codebuild",
    "codepipeline_approval_notifier",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CIDeployResult(BaseModel):
    """Result of :func:`codebuild_triggered_deploy`."""

    model_config = ConfigDict(frozen=True)

    build_id: str
    build_status: str
    deployment_id: str | None
    deployment_status: str | None


class ApprovalNotifyResult(BaseModel):
    """Result of :func:`codepipeline_approval_notifier`."""

    model_config = ConfigDict(frozen=True)

    pending_approvals: int
    emails_sent: int
    approval_tokens: list[str]


class PRBuildResult(BaseModel):
    """Result of :func:`codecommit_pr_to_codebuild`."""

    model_config = ConfigDict(frozen=True)

    build_id: str
    build_status: str
    comment_id: str


class PackagePromoteResult(BaseModel):
    """Result of :func:`codeartifact_package_promoter`."""

    model_config = ConfigDict(frozen=True)

    package_name: str
    version: str
    promoted: bool
    ssm_updated: bool


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def codebuild_triggered_deploy(
    project_name: str,
    source_bucket: str,
    source_key: str,
    application_name: str,
    deployment_group_name: str,
    poll_interval: int = 15,
    region_name: str | None = None,
) -> CIDeployResult:
    """Start a CodeBuild build from an S3 source artifact, poll until completion, and trigger a CodeDeploy deployment on success.

    Starts a CodeBuild project build with an S3 source override pointing at
    *source_bucket*/*source_key*.  Polls ``batch_get_builds`` until the build
    reaches a terminal state.  On ``SUCCEEDED``, calls ``create_deployment``
    to deploy the artifact via CodeDeploy.

    Args:
        project_name: CodeBuild project name.
        source_bucket: S3 bucket holding the source artifact.
        source_key: S3 key of the source artifact (ZIP file).
        application_name: CodeDeploy application name.
        deployment_group_name: CodeDeploy deployment group name.
        poll_interval: Seconds between build-status polls (default ``15``).
        region_name: AWS region override.

    Returns:
        A :class:`CIDeployResult` with build_id, build_status, deployment_id,
        and deployment_status.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    cb = get_client("codebuild", region_name)
    cd = get_client("codedeploy", region_name)

    # ------------------------------------------------------------------
    # 1. Start CodeBuild build with S3 source override
    # ------------------------------------------------------------------
    logger.info(
        "Starting CodeBuild project %r from s3://%s/%s",
        project_name,
        source_bucket,
        source_key,
    )
    try:
        start_resp = cb.start_build(
            projectName=project_name,
            sourceTypeOverride="S3",
            sourceLocationOverride=f"{source_bucket}/{source_key}",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start CodeBuild project {project_name!r}") from exc

    build = start_resp["build"]
    build_id: str = build["id"]
    logger.info("Build started: %s", build_id)

    # ------------------------------------------------------------------
    # 2. Poll batch_get_builds until build reaches a terminal state
    # ------------------------------------------------------------------
    terminal_statuses = {"SUCCEEDED", "FAILED", "FAULT", "TIMED_OUT", "STOPPED"}
    build_status: str = build.get("buildStatus", "IN_PROGRESS")

    while build_status not in terminal_statuses:
        time.sleep(poll_interval)
        try:
            batch_resp = cb.batch_get_builds(ids=[build_id])
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll CodeBuild build {build_id!r}") from exc
        builds = batch_resp.get("builds", [])
        if builds:
            build_status = builds[0].get("buildStatus", build_status)
        logger.debug("Build %s status: %s", build_id, build_status)

    logger.info("Build %s finished with status: %s", build_id, build_status)

    # ------------------------------------------------------------------
    # 3. On SUCCEEDED, create a CodeDeploy deployment
    # ------------------------------------------------------------------
    deployment_id: str | None = None
    deployment_status: str | None = None

    if build_status == "SUCCEEDED":
        logger.info(
            "Triggering CodeDeploy deployment for %r / %r",
            application_name,
            deployment_group_name,
        )
        try:
            deploy_resp = cd.create_deployment(
                applicationName=application_name,
                deploymentGroupName=deployment_group_name,
                revision={
                    "revisionType": "S3",
                    "s3Location": {
                        "bucket": source_bucket,
                        "key": source_key,
                        "bundleType": "zip",
                    },
                },
                description=f"Triggered by CodeBuild build {build_id}",
            )
            deployment_id = deploy_resp["deploymentId"]
            logger.info("Deployment created: %s", deployment_id)

            dep_info = cd.get_deployment(deploymentId=deployment_id)
            deployment_status = dep_info.get("deploymentInfo", {}).get("status")
        except ClientError as exc:
            raise wrap_aws_error(
                exc,
                f"Failed to create CodeDeploy deployment for {application_name!r}",
            ) from exc

    return CIDeployResult(
        build_id=build_id,
        build_status=build_status,
        deployment_id=deployment_id,
        deployment_status=deployment_status,
    )


def codepipeline_approval_notifier(
    pipeline_name: str,
    table_name: str,
    from_email: str,
    to_emails: list[str],
    region_name: str | None = None,
) -> ApprovalNotifyResult:
    """List pending CodePipeline approval actions, send emails via SES v2, and record in DynamoDB.

    Retrieves the pipeline state via ``get_pipeline_state``, finds actions with
    ``"Approval"`` actionType whose ``latestExecution`` status is
    ``"InProgress"``, sends a formatted email via SES v2 ``send_email``, and
    stores each token with pipeline/stage info in DynamoDB.

    Args:
        pipeline_name: Name of the CodePipeline pipeline.
        table_name: DynamoDB table name for recording approval tokens.
        from_email: Verified SES sender address.
        to_emails: List of recipient email addresses.
        region_name: AWS region override.

    Returns:
        An :class:`ApprovalNotifyResult` with pending_approvals count,
        emails_sent count, and approval_tokens list.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    cp = get_client("codepipeline", region_name)
    sesv2 = get_client("sesv2", region_name)
    ddb = get_client("dynamodb", region_name)

    # ------------------------------------------------------------------
    # 1. Fetch pipeline state
    # ------------------------------------------------------------------
    logger.info("Fetching pipeline state for %r", pipeline_name)
    try:
        state_resp = cp.get_pipeline_state(name=pipeline_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get pipeline state for {pipeline_name!r}") from exc

    stage_states: list[dict[str, Any]] = state_resp.get("stageStates", [])

    # ------------------------------------------------------------------
    # 2. Find actions with Approval actionType in latestExecution
    # ------------------------------------------------------------------
    pending_approvals = 0
    emails_sent = 0
    approval_tokens: list[str] = []

    for stage in stage_states:
        stage_name: str = stage.get("stageName", "")
        for action_state in stage.get("actionStates", []):
            latest = action_state.get("latestExecution", {})
            if latest.get("status") != "InProgress":
                continue

            # Filter for Approval action type
            action_name: str = action_state.get("actionName", "Unknown")
            token: str | None = latest.get("token")
            if token is None:
                continue

            pending_approvals += 1
            approval_tokens.append(token)

            # ------------------------------------------------------------------
            # 3. Send approval request email via SES v2
            # ------------------------------------------------------------------
            subject = (
                f"[Action Required] CodePipeline approval needed: "
                f"{pipeline_name} / {stage_name} / {action_name}"
            )
            body_html = (
                f"<h2>CodePipeline Manual Approval Required</h2>"
                f"<p><strong>Pipeline:</strong> {pipeline_name}</p>"
                f"<p><strong>Stage:</strong> {stage_name}</p>"
                f"<p><strong>Action:</strong> {action_name}</p>"
                f"<p><strong>Token:</strong> {token}</p>"
                f"<p>Please log in to the AWS Console to approve or reject this action.</p>"
            )
            body_text = (
                f"CodePipeline Manual Approval Required\n"
                f"Pipeline: {pipeline_name}\n"
                f"Stage: {stage_name}\n"
                f"Action: {action_name}\n"
                f"Token: {token}\n"
                f"Please log in to the AWS Console to approve or reject."
            )
            logger.info(
                "Sending approval notification for action %r to %d recipients",
                action_name,
                len(to_emails),
            )
            try:
                sesv2.send_email(
                    FromEmailAddress=from_email,
                    Destination={"ToAddresses": to_emails},
                    Content={
                        "Simple": {
                            "Subject": {"Data": subject, "Charset": "UTF-8"},
                            "Body": {
                                "Text": {"Data": body_text, "Charset": "UTF-8"},
                                "Html": {"Data": body_html, "Charset": "UTF-8"},
                            },
                        }
                    },
                )
                emails_sent += len(to_emails)
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"Failed to send approval email for action {action_name!r}"
                ) from exc

            # ------------------------------------------------------------------
            # 4. Store token + pipeline + stage in DynamoDB
            # ------------------------------------------------------------------
            record: dict[str, Any] = {
                "approval_token": {"S": token},
                "pipeline_name": {"S": pipeline_name},
                "stage_name": {"S": stage_name},
                "action_name": {"S": action_name},
                "recorded_at": {"S": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
            }
            try:
                ddb.put_item(TableName=table_name, Item=record)
                logger.debug("Recorded approval token in DynamoDB: %s", token)
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"Failed to record approval token in DynamoDB table {table_name!r}"
                ) from exc

    logger.info(
        "Pipeline %r: %d pending approvals, %d emails sent",
        pipeline_name,
        pending_approvals,
        emails_sent,
    )
    return ApprovalNotifyResult(
        pending_approvals=pending_approvals,
        emails_sent=emails_sent,
        approval_tokens=approval_tokens,
    )


def codecommit_pr_to_codebuild(
    repository_name: str,
    pull_request_id: str,
    project_name: str,
    source_reference: str,
    region_name: str | None = None,
) -> PRBuildResult:
    """Create or trigger a CodeBuild build from a CodeCommit PR's source, post build result as a PR comment.

    Starts a CodeBuild build using the CodeCommit source with the specified
    *source_reference* (branch/commit), polls until done, then posts
    the build result as a comment on the pull request.

    Args:
        repository_name: CodeCommit repository name.
        pull_request_id: Pull request ID string.
        project_name: CodeBuild project name to trigger.
        source_reference: Branch name or commit SHA to build.
        region_name: AWS region override.

    Returns:
        A :class:`PRBuildResult` with build_id, build_status, and comment_id.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    cc = get_client("codecommit", region_name)
    cb = get_client("codebuild", region_name)

    # ------------------------------------------------------------------
    # 1. Start CodeBuild with CodeCommit source
    # ------------------------------------------------------------------
    logger.info(
        "Starting CodeBuild project %r for PR %s (ref %r) in repo %r",
        project_name,
        pull_request_id,
        source_reference,
        repository_name,
    )
    try:
        build_resp = cb.start_build(
            projectName=project_name,
            sourceVersion=source_reference,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start CodeBuild project {project_name!r}") from exc

    build = build_resp["build"]
    build_id: str = build["id"]
    build_status: str = build.get("buildStatus", "IN_PROGRESS")
    logger.info("Build started: %s", build_id)

    # ------------------------------------------------------------------
    # 2. Poll until build reaches a terminal state
    # ------------------------------------------------------------------
    terminal_statuses = {"SUCCEEDED", "FAILED", "FAULT", "TIMED_OUT", "STOPPED"}

    while build_status not in terminal_statuses:
        time.sleep(15)
        try:
            batch_resp = cb.batch_get_builds(ids=[build_id])
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll CodeBuild build {build_id!r}") from exc
        builds = batch_resp.get("builds", [])
        if builds:
            build_status = builds[0].get("buildStatus", build_status)
        logger.debug("Build %s status: %s", build_id, build_status)

    logger.info("Build %s finished with status: %s", build_id, build_status)

    # ------------------------------------------------------------------
    # 3. Get PR details for comment anchoring
    # ------------------------------------------------------------------
    try:
        pr_detail = cc.get_pull_request(pullRequestId=pull_request_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to fetch PR {pull_request_id!r} from {repository_name!r}"
        ) from exc

    pr_info = pr_detail.get("pullRequest", {})
    targets: list[dict[str, Any]] = pr_info.get("pullRequestTargets", [])
    before_commit = ""
    after_commit = ""
    if targets:
        before_commit = targets[0].get("mergeBase") or targets[0].get("destinationCommit", "")
        after_commit = targets[0].get("sourceCommit", "")

    # ------------------------------------------------------------------
    # 4. Post build result as PR comment
    # ------------------------------------------------------------------
    comment_content = (
        f"CodeBuild result for `{source_reference}`.\n"
        f"**Build ID:** `{build_id}`\n"
        f"**Status:** `{build_status}`"
    )
    logger.info("Posting build result comment on PR %s", pull_request_id)
    try:
        comment_resp = cc.post_comment_for_pull_request(
            pullRequestId=pull_request_id,
            repositoryName=repository_name,
            beforeCommitId=before_commit,
            afterCommitId=after_commit,
            content=comment_content,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to post comment on PR {pull_request_id!r}") from exc

    comment_id: str = comment_resp.get("comment", {}).get("commentId", "")
    logger.info("Comment posted: %s", comment_id)

    return PRBuildResult(
        build_id=build_id,
        build_status=build_status,
        comment_id=comment_id,
    )


def codeartifact_package_promoter(
    source_domain: str,
    source_repository: str,
    dest_domain: str,
    dest_repository: str,
    package_format: str,
    package_name: str,
    package_version: str,
    ssm_parameter_name: str,
    region_name: str | None = None,
) -> PackagePromoteResult:
    """Copy a package version between CodeArtifact repositories and update the allowed-package list in SSM.

    Copies *package_name*=*package_version* from *source_repository* to
    *dest_repository* via ``copy_package_versions``, then reads the SSM
    parameter at *ssm_parameter_name*, appends the package to the JSON list
    if not present, and writes it back via ``put_parameter``.

    Args:
        source_domain: Source CodeArtifact domain name.
        source_repository: Source CodeArtifact repository name.
        dest_domain: Destination CodeArtifact domain name.
        dest_repository: Destination CodeArtifact repository name.
        package_format: CodeArtifact package format (``"npm"``, ``"pypi"``,
            or ``"maven"``).
        package_name: Package name (e.g. ``"my-library"``).
        package_version: Version string (e.g. ``"1.2.3"``).
        ssm_parameter_name: SSM Parameter Store key holding the JSON allowed
            package list.
        region_name: AWS region override.

    Returns:
        A :class:`PackagePromoteResult` with package_name, version, promoted
        flag, and ssm_updated flag.

    Raises:
        RuntimeError: If any underlying AWS API call fails.
    """
    ca = get_client("codeartifact", region_name)
    ssm = get_client("ssm", region_name)

    # ------------------------------------------------------------------
    # 1. Copy the package version to the destination repository
    # ------------------------------------------------------------------
    logger.info(
        "Copying %s==%s (%s) from %s/%s to %s/%s",
        package_name,
        package_version,
        package_format,
        source_domain,
        source_repository,
        dest_domain,
        dest_repository,
    )
    promoted = False
    try:
        ca.copy_package_versions(
            sourceDomain=source_domain,
            sourceRepository=source_repository,
            destinationDomain=dest_domain,
            destinationRepository=dest_repository,
            format=package_format,
            package=package_name,
            versions=[package_version],
            allowOverwrite=False,
            includeFromUpstream=False,
        )
        promoted = True
        logger.info("Package copied successfully")
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to copy {package_name}=={package_version} "
            f"from {source_domain}/{source_repository} to {dest_domain}/{dest_repository}",
        ) from exc

    # ------------------------------------------------------------------
    # 2. Get existing SSM parameter and append package to JSON list
    # ------------------------------------------------------------------
    ssm_updated = False
    package_entry = f"{package_name}=={package_version}"

    try:
        param_resp = ssm.get_parameter(Name=ssm_parameter_name)
        existing_value: str = param_resp["Parameter"]["Value"]
        try:
            package_list: list[str] = json.loads(existing_value)
            if not isinstance(package_list, list):
                package_list = [existing_value]
        except json.JSONDecodeError:
            package_list = [existing_value] if existing_value else []
    except ClientError as exc:
        error_code = exc.response.get("Error", {}).get("Code", "")
        if error_code == "ParameterNotFound":
            package_list = []
        else:
            raise wrap_aws_error(
                exc, f"Failed to get SSM parameter {ssm_parameter_name!r}"
            ) from exc

    if package_entry not in package_list:
        package_list.append(package_entry)
        logger.info(
            "Updating SSM parameter %r with new entry %r",
            ssm_parameter_name,
            package_entry,
        )
        try:
            ssm.put_parameter(
                Name=ssm_parameter_name,
                Value=json.dumps(package_list),
                Type="String",
                Overwrite=True,
                Description="Allowed CodeArtifact packages — updated by codeartifact_package_promoter",
            )
            ssm_updated = True
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"Failed to update SSM parameter {ssm_parameter_name!r}"
            ) from exc
    else:
        logger.info(
            "Package %r already present in SSM parameter — skipping update",
            package_entry,
        )
        ssm_updated = False

    logger.info("Promotion complete: promoted=%s ssm_updated=%s", promoted, ssm_updated)
    return PackagePromoteResult(
        package_name=package_name,
        version=package_version,
        promoted=promoted,
        ssm_updated=ssm_updated,
    )
