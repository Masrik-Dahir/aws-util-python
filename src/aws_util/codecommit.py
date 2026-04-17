"""aws_util.codecommit -- AWS CodeCommit utilities.

Provides helpers for managing CodeCommit repositories, branches, commits,
files, pull requests, merges, and blob retrieval.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchAssociateApprovalRuleTemplateWithRepositoriesResult",
    "BatchDescribeMergeConflictsResult",
    "BatchDisassociateApprovalRuleTemplateFromRepositoriesResult",
    "BatchGetCommitsResult",
    "BatchGetRepositoriesResult",
    "BlobResult",
    "BranchResult",
    "CommitResult",
    "CreateApprovalRuleTemplateResult",
    "CreatePullRequestApprovalRuleResult",
    "CreateUnreferencedMergeCommitResult",
    "DeleteApprovalRuleTemplateResult",
    "DeleteCommentContentResult",
    "DeletePullRequestApprovalRuleResult",
    "DescribeMergeConflictsResult",
    "DescribePullRequestEventsResult",
    "DiffResult",
    "EvaluatePullRequestApprovalRulesResult",
    "FileResult",
    "GetApprovalRuleTemplateResult",
    "GetCommentReactionsResult",
    "GetCommentResult",
    "GetCommentsForComparedCommitResult",
    "GetCommentsForPullRequestResult",
    "GetFolderResult",
    "GetMergeCommitResult",
    "GetMergeConflictsResult",
    "GetMergeOptionsResult",
    "GetPullRequestApprovalStatesResult",
    "GetPullRequestOverrideStateResult",
    "GetRepositoryTriggersResult",
    "ListApprovalRuleTemplatesResult",
    "ListAssociatedApprovalRuleTemplatesForRepositoryResult",
    "ListFileCommitHistoryResult",
    "ListRepositoriesForApprovalRuleTemplateResult",
    "ListTagsForResourceResult",
    "MergeBranchesByThreeWayResult",
    "MergePullRequestBySquashResult",
    "MergePullRequestByThreeWayResult",
    "PostCommentForComparedCommitResult",
    "PostCommentForPullRequestResult",
    "PostCommentReplyResult",
    "PullRequestResult",
    "PutRepositoryTriggersResult",
    "RepositoryResult",
    "RunRepositoryTriggersResult",
    "UpdateApprovalRuleTemplateContentResult",
    "UpdateApprovalRuleTemplateDescriptionResult",
    "UpdateApprovalRuleTemplateNameResult",
    "UpdateCommentResult",
    "UpdatePullRequestApprovalRuleContentResult",
    "UpdatePullRequestDescriptionResult",
    "UpdatePullRequestStatusResult",
    "UpdatePullRequestTitleResult",
    "UpdateRepositoryEncryptionKeyResult",
    "associate_approval_rule_template_with_repository",
    "batch_associate_approval_rule_template_with_repositories",
    "batch_describe_merge_conflicts",
    "batch_disassociate_approval_rule_template_from_repositories",
    "batch_get_commits",
    "batch_get_repositories",
    "create_approval_rule_template",
    "create_branch",
    "create_commit",
    "create_pull_request",
    "create_pull_request_approval_rule",
    "create_repository",
    "create_unreferenced_merge_commit",
    "delete_approval_rule_template",
    "delete_branch",
    "delete_comment_content",
    "delete_file",
    "delete_pull_request_approval_rule",
    "delete_repository",
    "describe_merge_conflicts",
    "describe_pull_request_events",
    "disassociate_approval_rule_template_from_repository",
    "evaluate_pull_request_approval_rules",
    "get_approval_rule_template",
    "get_blob",
    "get_branch",
    "get_comment",
    "get_comment_reactions",
    "get_comments_for_compared_commit",
    "get_comments_for_pull_request",
    "get_commit",
    "get_differences",
    "get_file",
    "get_folder",
    "get_merge_commit",
    "get_merge_conflicts",
    "get_merge_options",
    "get_pull_request",
    "get_pull_request_approval_states",
    "get_pull_request_override_state",
    "get_repository",
    "get_repository_triggers",
    "list_approval_rule_templates",
    "list_associated_approval_rule_templates_for_repository",
    "list_branches",
    "list_file_commit_history",
    "list_pull_requests",
    "list_repositories",
    "list_repositories_for_approval_rule_template",
    "list_tags_for_resource",
    "merge_branches_by_fast_forward",
    "merge_branches_by_squash",
    "merge_branches_by_three_way",
    "merge_pull_request_by_fast_forward",
    "merge_pull_request_by_squash",
    "merge_pull_request_by_three_way",
    "override_pull_request_approval_rules",
    "post_comment_for_compared_commit",
    "post_comment_for_pull_request",
    "post_comment_reply",
    "put_comment_reaction",
    "put_file",
    "put_repository_triggers",
    "run_repository_triggers",
    "tag_resource",
    "untag_resource",
    "update_approval_rule_template_content",
    "update_approval_rule_template_description",
    "update_approval_rule_template_name",
    "update_comment",
    "update_default_branch",
    "update_pull_request_approval_rule_content",
    "update_pull_request_approval_state",
    "update_pull_request_description",
    "update_pull_request_status",
    "update_pull_request_title",
    "update_repository_description",
    "update_repository_encryption_key",
    "update_repository_name",
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class RepositoryResult(BaseModel):
    """Metadata for a CodeCommit repository."""

    model_config = ConfigDict(frozen=True)

    repository_id: str
    repository_name: str
    arn: str | None = None
    description: str | None = None
    clone_url_http: str | None = None
    clone_url_ssh: str | None = None
    default_branch: str | None = None
    last_modified: str | None = None
    creation_date: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class BranchResult(BaseModel):
    """A CodeCommit branch."""

    model_config = ConfigDict(frozen=True)

    branch_name: str
    commit_id: str
    extra: dict[str, Any] = Field(default_factory=dict)


class CommitResult(BaseModel):
    """A CodeCommit commit."""

    model_config = ConfigDict(frozen=True)

    commit_id: str
    tree_id: str | None = None
    author: dict[str, Any] | None = None
    committer: dict[str, Any] | None = None
    message: str | None = None
    parents: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class PullRequestResult(BaseModel):
    """A CodeCommit pull request."""

    model_config = ConfigDict(frozen=True)

    pull_request_id: str
    title: str
    description: str | None = None
    pull_request_status: str | None = None
    creation_date: str | None = None
    last_activity_date: str | None = None
    pull_request_targets: list[dict[str, Any]] = Field(
        default_factory=list,
    )
    extra: dict[str, Any] = Field(default_factory=dict)


class FileResult(BaseModel):
    """A file retrieved from CodeCommit."""

    model_config = ConfigDict(frozen=True)

    file_path: str
    file_size: int | None = None
    file_mode: str | None = None
    blob_id: str | None = None
    commit_id: str | None = None
    file_content: bytes | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class DiffResult(BaseModel):
    """A single difference entry from CodeCommit."""

    model_config = ConfigDict(frozen=True)

    before_blob: dict[str, Any] | None = None
    after_blob: dict[str, Any] | None = None
    change_type: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class BlobResult(BaseModel):
    """A blob retrieved from CodeCommit."""

    model_config = ConfigDict(frozen=True)

    blob_id: str
    content: bytes
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_REPO_KNOWN_KEYS = frozenset(
    {
        "repositoryId",
        "repositoryName",
        "Arn",
        "repositoryDescription",
        "cloneUrlHttp",
        "cloneUrlSsh",
        "defaultBranch",
        "lastModifiedDate",
        "creationDate",
    }
)

_BRANCH_KNOWN_KEYS = frozenset({"branchName", "commitId"})

_COMMIT_KNOWN_KEYS = frozenset(
    {
        "commitId",
        "treeId",
        "author",
        "committer",
        "message",
        "parents",
    }
)

_PR_KNOWN_KEYS = frozenset(
    {
        "pullRequestId",
        "title",
        "description",
        "pullRequestStatus",
        "creationDate",
        "lastActivityDate",
        "pullRequestTargets",
    }
)


def _parse_repository(data: dict[str, Any]) -> RepositoryResult:
    """Convert a raw CodeCommit repository dict to a ``RepositoryResult``."""
    return RepositoryResult(
        repository_id=data.get("repositoryId", ""),
        repository_name=data.get("repositoryName", ""),
        arn=data.get("Arn"),
        description=data.get("repositoryDescription"),
        clone_url_http=data.get("cloneUrlHttp"),
        clone_url_ssh=data.get("cloneUrlSsh"),
        default_branch=data.get("defaultBranch"),
        last_modified=(str(data["lastModifiedDate"]) if data.get("lastModifiedDate") else None),
        creation_date=(str(data["creationDate"]) if data.get("creationDate") else None),
        extra={k: v for k, v in data.items() if k not in _REPO_KNOWN_KEYS},
    )


def _parse_branch(data: dict[str, Any]) -> BranchResult:
    """Convert a raw CodeCommit branch dict to a ``BranchResult``."""
    return BranchResult(
        branch_name=data.get("branchName", ""),
        commit_id=data.get("commitId", ""),
        extra={k: v for k, v in data.items() if k not in _BRANCH_KNOWN_KEYS},
    )


def _parse_commit(data: dict[str, Any]) -> CommitResult:
    """Convert a raw CodeCommit commit dict to a ``CommitResult``."""
    return CommitResult(
        commit_id=data.get("commitId", ""),
        tree_id=data.get("treeId"),
        author=data.get("author"),
        committer=data.get("committer"),
        message=data.get("message"),
        parents=data.get("parents", []),
        extra={k: v for k, v in data.items() if k not in _COMMIT_KNOWN_KEYS},
    )


def _parse_pull_request(data: dict[str, Any]) -> PullRequestResult:
    """Convert a raw CodeCommit pull request dict."""
    return PullRequestResult(
        pull_request_id=data.get("pullRequestId", ""),
        title=data.get("title", ""),
        description=data.get("description"),
        pull_request_status=data.get("pullRequestStatus"),
        creation_date=(str(data["creationDate"]) if data.get("creationDate") else None),
        last_activity_date=(
            str(data["lastActivityDate"]) if data.get("lastActivityDate") else None
        ),
        pull_request_targets=data.get("pullRequestTargets", []),
        extra={k: v for k, v in data.items() if k not in _PR_KNOWN_KEYS},
    )


def _parse_diff(data: dict[str, Any]) -> DiffResult:
    """Convert a raw CodeCommit difference entry."""
    return DiffResult(
        before_blob=data.get("beforeBlob"),
        after_blob=data.get("afterBlob"),
        change_type=data.get("changeType"),
        extra={k: v for k, v in data.items() if k not in {"beforeBlob", "afterBlob", "changeType"}},
    )


# ---------------------------------------------------------------------------
# Repository operations
# ---------------------------------------------------------------------------


def create_repository(
    repository_name: str,
    *,
    description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> RepositoryResult:
    """Create a new CodeCommit repository.

    Args:
        repository_name: The name of the new repository.
        description: Optional repository description.
        tags: Optional tags to attach.
        region_name: AWS region override.

    Returns:
        A :class:`RepositoryResult` for the created repository.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {"repositoryName": repository_name}
    if description is not None:
        kwargs["repositoryDescription"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_repository failed for {repository_name!r}") from exc
    return _parse_repository(resp["repositoryMetadata"])


def get_repository(
    repository_name: str,
    *,
    region_name: str | None = None,
) -> RepositoryResult:
    """Get metadata for a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        region_name: AWS region override.

    Returns:
        A :class:`RepositoryResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.get_repository(repositoryName=repository_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_repository failed for {repository_name!r}") from exc
    return _parse_repository(resp["repositoryMetadata"])


def list_repositories(
    *,
    sort_by: str = "repositoryName",
    order: str = "ascending",
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List CodeCommit repositories.

    Args:
        sort_by: Sort field (``"repositoryName"`` or ``"lastModifiedDate"``).
        order: ``"ascending"`` or ``"descending"``.
        region_name: AWS region override.

    Returns:
        A list of repository name-ID dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    repos: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("list_repositories")
        for page in paginator.paginate(sortBy=sort_by, order=order):
            repos.extend(page.get("repositories", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_repositories failed") from exc
    return repos


def delete_repository(
    repository_name: str,
    *,
    region_name: str | None = None,
) -> str | None:
    """Delete a CodeCommit repository.

    Args:
        repository_name: Name of the repository to delete.
        region_name: AWS region override.

    Returns:
        The repository ID of the deleted repository, or ``None``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.delete_repository(
            repositoryName=repository_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_repository failed for {repository_name!r}") from exc
    return resp.get("repositoryId")


def update_repository_name(
    old_name: str,
    new_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Rename a CodeCommit repository.

    Args:
        old_name: Current repository name.
        new_name: Desired new name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        client.update_repository_name(
            oldName=old_name,
            newName=new_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"update_repository_name failed for {old_name!r}",
        ) from exc


def update_repository_description(
    repository_name: str,
    description: str,
    *,
    region_name: str | None = None,
) -> None:
    """Update the description of a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        description: New description text.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        client.update_repository_description(
            repositoryName=repository_name,
            repositoryDescription=description,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"update_repository_description failed for {repository_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Branch operations
# ---------------------------------------------------------------------------


def create_branch(
    repository_name: str,
    branch_name: str,
    commit_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Create a branch in a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        branch_name: Name of the new branch.
        commit_id: Commit ID to point the branch at.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        client.create_branch(
            repositoryName=repository_name,
            branchName=branch_name,
            commitId=commit_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_branch failed for {branch_name!r}",
        ) from exc


def get_branch(
    repository_name: str,
    branch_name: str,
    *,
    region_name: str | None = None,
) -> BranchResult:
    """Get information about a branch.

    Args:
        repository_name: Name of the repository.
        branch_name: Name of the branch.
        region_name: AWS region override.

    Returns:
        A :class:`BranchResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.get_branch(
            repositoryName=repository_name,
            branchName=branch_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_branch failed for {branch_name!r}") from exc
    return _parse_branch(resp["branch"])


def list_branches(
    repository_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List branch names in a repository.

    Args:
        repository_name: Name of the repository.
        region_name: AWS region override.

    Returns:
        A list of branch name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    branches: list[str] = []
    try:
        paginator = client.get_paginator("list_branches")
        for page in paginator.paginate(
            repositoryName=repository_name,
        ):
            branches.extend(page.get("branches", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_branches failed") from exc
    return branches


def delete_branch(
    repository_name: str,
    branch_name: str,
    *,
    region_name: str | None = None,
) -> BranchResult:
    """Delete a branch from a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        branch_name: Name of the branch to delete.
        region_name: AWS region override.

    Returns:
        A :class:`BranchResult` for the deleted branch.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.delete_branch(
            repositoryName=repository_name,
            branchName=branch_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_branch failed for {branch_name!r}") from exc
    return _parse_branch(resp["deletedBranch"])


# ---------------------------------------------------------------------------
# Merge operations
# ---------------------------------------------------------------------------


def merge_branches_by_fast_forward(
    repository_name: str,
    source_commit: str,
    destination_commit: str,
    *,
    target_branch: str | None = None,
    region_name: str | None = None,
) -> str:
    """Merge two branches using fast-forward.

    Args:
        repository_name: Name of the repository.
        source_commit: Commit specifier for the source.
        destination_commit: Commit specifier for the destination.
        target_branch: Optional branch to update.
        region_name: AWS region override.

    Returns:
        The resulting commit ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "sourceCommitSpecifier": source_commit,
        "destinationCommitSpecifier": destination_commit,
    }
    if target_branch is not None:
        kwargs["targetBranch"] = target_branch
    try:
        resp = client.merge_branches_by_fast_forward(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "merge_branches_by_fast_forward failed") from exc
    return resp.get("commitId", "")


def merge_branches_by_squash(
    repository_name: str,
    source_commit: str,
    destination_commit: str,
    *,
    target_branch: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    commit_message: str | None = None,
    region_name: str | None = None,
) -> str:
    """Merge two branches using squash.

    Args:
        repository_name: Name of the repository.
        source_commit: Commit specifier for the source.
        destination_commit: Commit specifier for the destination.
        target_branch: Optional branch to update.
        author_name: Optional author name.
        email: Optional author email.
        commit_message: Optional commit message.
        region_name: AWS region override.

    Returns:
        The resulting commit ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "sourceCommitSpecifier": source_commit,
        "destinationCommitSpecifier": destination_commit,
    }
    if target_branch is not None:
        kwargs["targetBranch"] = target_branch
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    try:
        resp = client.merge_branches_by_squash(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "merge_branches_by_squash failed") from exc
    return resp.get("commitId", "")


# ---------------------------------------------------------------------------
# Commit operations
# ---------------------------------------------------------------------------


def create_commit(
    repository_name: str,
    branch_name: str,
    *,
    parent_commit_id: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    commit_message: str | None = None,
    put_files: list[dict[str, Any]] | None = None,
    delete_files: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CommitResult:
    """Create a commit in a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        branch_name: Branch to commit to.
        parent_commit_id: Optional parent commit ID.
        author_name: Optional author name.
        email: Optional author email.
        commit_message: Optional commit message.
        put_files: Files to add or update.
        delete_files: Files to delete.
        region_name: AWS region override.

    Returns:
        A :class:`CommitResult` for the new commit.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "branchName": branch_name,
    }
    if parent_commit_id is not None:
        kwargs["parentCommitId"] = parent_commit_id
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if put_files is not None:
        kwargs["putFiles"] = put_files
    if delete_files is not None:
        kwargs["deleteFiles"] = delete_files
    try:
        resp = client.create_commit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_commit failed") from exc
    return CommitResult(
        commit_id=resp.get("commitId", ""),
        tree_id=resp.get("treeId"),
        parents=resp.get("parents", []),
    )


def get_commit(
    repository_name: str,
    commit_id: str,
    *,
    region_name: str | None = None,
) -> CommitResult:
    """Get details of a commit.

    Args:
        repository_name: Name of the repository.
        commit_id: The full commit ID.
        region_name: AWS region override.

    Returns:
        A :class:`CommitResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.get_commit(
            repositoryName=repository_name,
            commitId=commit_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_commit failed for {commit_id!r}") from exc
    return _parse_commit(resp["commit"])


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------


def get_file(
    repository_name: str,
    file_path: str,
    *,
    commit_specifier: str | None = None,
    region_name: str | None = None,
) -> FileResult:
    """Get a file from a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        file_path: Path to the file.
        commit_specifier: Optional commit, branch, or tag.
        region_name: AWS region override.

    Returns:
        A :class:`FileResult` containing the file content.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "filePath": file_path,
    }
    if commit_specifier is not None:
        kwargs["commitSpecifier"] = commit_specifier
    try:
        resp = client.get_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_file failed for {file_path!r}") from exc
    return FileResult(
        file_path=resp.get("filePath", file_path),
        file_size=resp.get("fileSize"),
        file_mode=resp.get("fileMode"),
        blob_id=resp.get("blobId"),
        commit_id=resp.get("commitId"),
        file_content=resp.get("fileContent"),
    )


def put_file(
    repository_name: str,
    file_path: str,
    file_content: bytes,
    branch_name: str,
    *,
    file_mode: str | None = None,
    parent_commit_id: str | None = None,
    commit_message: str | None = None,
    name: str | None = None,
    email: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Put a file into a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        file_path: Path for the file in the repository.
        file_content: Raw file content bytes.
        branch_name: Branch to commit to.
        file_mode: Optional file mode (``"EXECUTABLE"``, ``"NORMAL"``
            or ``"SYMLINK"``).
        parent_commit_id: Optional parent commit ID.
        commit_message: Optional commit message.
        name: Optional committer name.
        email: Optional committer email.
        region_name: AWS region override.

    Returns:
        A dict with ``commitId``, ``blobId``, and ``treeId``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "filePath": file_path,
        "fileContent": file_content,
        "branchName": branch_name,
    }
    if file_mode is not None:
        kwargs["fileMode"] = file_mode
    if parent_commit_id is not None:
        kwargs["parentCommitId"] = parent_commit_id
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if name is not None:
        kwargs["name"] = name
    if email is not None:
        kwargs["email"] = email
    try:
        resp = client.put_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"put_file failed for {file_path!r}") from exc
    return {
        "commitId": resp.get("commitId", ""),
        "blobId": resp.get("blobId", ""),
        "treeId": resp.get("treeId", ""),
    }


def delete_file(
    repository_name: str,
    file_path: str,
    branch_name: str,
    parent_commit_id: str,
    *,
    commit_message: str | None = None,
    name: str | None = None,
    email: str | None = None,
    keep_empty_folders: bool = False,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete a file from a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        file_path: Path of the file to delete.
        branch_name: Branch to commit the deletion to.
        parent_commit_id: The parent commit ID.
        commit_message: Optional commit message.
        name: Optional committer name.
        email: Optional committer email.
        keep_empty_folders: Whether to keep empty folders.
        region_name: AWS region override.

    Returns:
        A dict with ``commitId``, ``blobId``, ``treeId``,
        and ``filePath``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "filePath": file_path,
        "branchName": branch_name,
        "parentCommitId": parent_commit_id,
        "keepEmptyFolders": keep_empty_folders,
    }
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if name is not None:
        kwargs["name"] = name
    if email is not None:
        kwargs["email"] = email
    try:
        resp = client.delete_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_file failed for {file_path!r}") from exc
    return {
        "commitId": resp.get("commitId", ""),
        "blobId": resp.get("blobId", ""),
        "treeId": resp.get("treeId", ""),
        "filePath": resp.get("filePath", file_path),
    }


# ---------------------------------------------------------------------------
# Differences
# ---------------------------------------------------------------------------


def get_differences(
    repository_name: str,
    after_commit_specifier: str,
    *,
    before_commit_specifier: str | None = None,
    before_path: str | None = None,
    after_path: str | None = None,
    region_name: str | None = None,
) -> list[DiffResult]:
    """Get differences between commits or commit and working tree.

    Args:
        repository_name: Name of the repository.
        after_commit_specifier: The commit to diff to.
        before_commit_specifier: Optional commit to diff from.
        before_path: Optional before path filter.
        after_path: Optional after path filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`DiffResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "afterCommitSpecifier": after_commit_specifier,
    }
    if before_commit_specifier is not None:
        kwargs["beforeCommitSpecifier"] = before_commit_specifier
    if before_path is not None:
        kwargs["beforePath"] = before_path
    if after_path is not None:
        kwargs["afterPath"] = after_path
    diffs: list[DiffResult] = []
    try:
        paginator = client.get_paginator("get_differences")
        for page in paginator.paginate(**kwargs):
            for d in page.get("differences", []):
                diffs.append(_parse_diff(d))
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_differences failed") from exc
    return diffs


# ---------------------------------------------------------------------------
# Pull request operations
# ---------------------------------------------------------------------------


def create_pull_request(
    title: str,
    targets: list[dict[str, Any]],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> PullRequestResult:
    """Create a pull request in CodeCommit.

    Args:
        title: Title of the pull request.
        targets: A list of target dicts, each with
            ``repositoryName``, ``sourceReference``, and optionally
            ``destinationReference``.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        A :class:`PullRequestResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "title": title,
        "targets": targets,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_pull_request(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_pull_request failed") from exc
    return _parse_pull_request(resp["pullRequest"])


def get_pull_request(
    pull_request_id: str,
    *,
    region_name: str | None = None,
) -> PullRequestResult:
    """Get details for a pull request.

    Args:
        pull_request_id: The system-generated ID of the pull request.
        region_name: AWS region override.

    Returns:
        A :class:`PullRequestResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.get_pull_request(
            pullRequestId=pull_request_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_pull_request failed for {pull_request_id!r}",
        ) from exc
    return _parse_pull_request(resp["pullRequest"])


def list_pull_requests(
    repository_name: str,
    *,
    pull_request_status: str = "OPEN",
    region_name: str | None = None,
) -> list[str]:
    """List pull request IDs for a repository.

    Args:
        repository_name: Name of the repository.
        pull_request_status: Filter by status
            (``"OPEN"`` or ``"CLOSED"``).
        region_name: AWS region override.

    Returns:
        A list of pull request ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    pr_ids: list[str] = []
    try:
        paginator = client.get_paginator("list_pull_requests")
        for page in paginator.paginate(
            repositoryName=repository_name,
            pullRequestStatus=pull_request_status,
        ):
            pr_ids.extend(page.get("pullRequestIds", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_pull_requests failed") from exc
    return pr_ids


def merge_pull_request_by_fast_forward(
    pull_request_id: str,
    repository_name: str,
    *,
    source_commit_id: str | None = None,
    region_name: str | None = None,
) -> PullRequestResult:
    """Merge a pull request using fast-forward.

    Args:
        pull_request_id: The system-generated pull request ID.
        repository_name: Name of the repository.
        source_commit_id: Optional source commit ID.
        region_name: AWS region override.

    Returns:
        A :class:`PullRequestResult` for the merged pull request.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "pullRequestId": pull_request_id,
        "repositoryName": repository_name,
    }
    if source_commit_id is not None:
        kwargs["sourceCommitId"] = source_commit_id
    try:
        resp = client.merge_pull_request_by_fast_forward(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "merge_pull_request_by_fast_forward failed",
        ) from exc
    return _parse_pull_request(resp["pullRequest"])


# ---------------------------------------------------------------------------
# Blob operations
# ---------------------------------------------------------------------------


def get_blob(
    repository_name: str,
    blob_id: str,
    *,
    region_name: str | None = None,
) -> BlobResult:
    """Get the content of a blob from a CodeCommit repository.

    Args:
        repository_name: Name of the repository.
        blob_id: The ID of the blob.
        region_name: AWS region override.

    Returns:
        A :class:`BlobResult` containing the blob content.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    try:
        resp = client.get_blob(
            repositoryName=repository_name,
            blobId=blob_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_blob failed for {blob_id!r}") from exc
    return BlobResult(
        blob_id=blob_id,
        content=resp.get("content", b""),
    )


class BatchAssociateApprovalRuleTemplateWithRepositoriesResult(BaseModel):
    """Result of batch_associate_approval_rule_template_with_repositories."""

    model_config = ConfigDict(frozen=True)

    associated_repository_names: list[str] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchDescribeMergeConflictsResult(BaseModel):
    """Result of batch_describe_merge_conflicts."""

    model_config = ConfigDict(frozen=True)

    conflicts: list[dict[str, Any]] | None = None
    next_token: str | None = None
    errors: list[dict[str, Any]] | None = None
    destination_commit_id: str | None = None
    source_commit_id: str | None = None
    base_commit_id: str | None = None


class BatchDisassociateApprovalRuleTemplateFromRepositoriesResult(BaseModel):
    """Result of batch_disassociate_approval_rule_template_from_repositories."""

    model_config = ConfigDict(frozen=True)

    disassociated_repository_names: list[str] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchGetCommitsResult(BaseModel):
    """Result of batch_get_commits."""

    model_config = ConfigDict(frozen=True)

    commits: list[dict[str, Any]] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchGetRepositoriesResult(BaseModel):
    """Result of batch_get_repositories."""

    model_config = ConfigDict(frozen=True)

    repositories: list[dict[str, Any]] | None = None
    repositories_not_found: list[str] | None = None
    errors: list[dict[str, Any]] | None = None


class CreateApprovalRuleTemplateResult(BaseModel):
    """Result of create_approval_rule_template."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template: dict[str, Any] | None = None


class CreatePullRequestApprovalRuleResult(BaseModel):
    """Result of create_pull_request_approval_rule."""

    model_config = ConfigDict(frozen=True)

    approval_rule: dict[str, Any] | None = None


class CreateUnreferencedMergeCommitResult(BaseModel):
    """Result of create_unreferenced_merge_commit."""

    model_config = ConfigDict(frozen=True)

    commit_id: str | None = None
    tree_id: str | None = None


class DeleteApprovalRuleTemplateResult(BaseModel):
    """Result of delete_approval_rule_template."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template_id: str | None = None


class DeleteCommentContentResult(BaseModel):
    """Result of delete_comment_content."""

    model_config = ConfigDict(frozen=True)

    comment: dict[str, Any] | None = None


class DeletePullRequestApprovalRuleResult(BaseModel):
    """Result of delete_pull_request_approval_rule."""

    model_config = ConfigDict(frozen=True)

    approval_rule_id: str | None = None


class DescribeMergeConflictsResult(BaseModel):
    """Result of describe_merge_conflicts."""

    model_config = ConfigDict(frozen=True)

    conflict_metadata: dict[str, Any] | None = None
    merge_hunks: list[dict[str, Any]] | None = None
    next_token: str | None = None
    destination_commit_id: str | None = None
    source_commit_id: str | None = None
    base_commit_id: str | None = None


class DescribePullRequestEventsResult(BaseModel):
    """Result of describe_pull_request_events."""

    model_config = ConfigDict(frozen=True)

    pull_request_events: list[dict[str, Any]] | None = None
    next_token: str | None = None


class EvaluatePullRequestApprovalRulesResult(BaseModel):
    """Result of evaluate_pull_request_approval_rules."""

    model_config = ConfigDict(frozen=True)

    evaluation: dict[str, Any] | None = None


class GetApprovalRuleTemplateResult(BaseModel):
    """Result of get_approval_rule_template."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template: dict[str, Any] | None = None


class GetCommentResult(BaseModel):
    """Result of get_comment."""

    model_config = ConfigDict(frozen=True)

    comment: dict[str, Any] | None = None


class GetCommentReactionsResult(BaseModel):
    """Result of get_comment_reactions."""

    model_config = ConfigDict(frozen=True)

    reactions_for_comment: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetCommentsForComparedCommitResult(BaseModel):
    """Result of get_comments_for_compared_commit."""

    model_config = ConfigDict(frozen=True)

    comments_for_compared_commit_data: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetCommentsForPullRequestResult(BaseModel):
    """Result of get_comments_for_pull_request."""

    model_config = ConfigDict(frozen=True)

    comments_for_pull_request_data: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetFolderResult(BaseModel):
    """Result of get_folder."""

    model_config = ConfigDict(frozen=True)

    commit_id: str | None = None
    folder_path: str | None = None
    tree_id: str | None = None
    sub_folders: list[dict[str, Any]] | None = None
    files: list[dict[str, Any]] | None = None
    symbolic_links: list[dict[str, Any]] | None = None
    sub_modules: list[dict[str, Any]] | None = None


class GetMergeCommitResult(BaseModel):
    """Result of get_merge_commit."""

    model_config = ConfigDict(frozen=True)

    source_commit_id: str | None = None
    destination_commit_id: str | None = None
    base_commit_id: str | None = None
    merged_commit_id: str | None = None


class GetMergeConflictsResult(BaseModel):
    """Result of get_merge_conflicts."""

    model_config = ConfigDict(frozen=True)

    mergeable: bool | None = None
    destination_commit_id: str | None = None
    source_commit_id: str | None = None
    base_commit_id: str | None = None
    conflict_metadata_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetMergeOptionsResult(BaseModel):
    """Result of get_merge_options."""

    model_config = ConfigDict(frozen=True)

    merge_options: list[str] | None = None
    source_commit_id: str | None = None
    destination_commit_id: str | None = None
    base_commit_id: str | None = None


class GetPullRequestApprovalStatesResult(BaseModel):
    """Result of get_pull_request_approval_states."""

    model_config = ConfigDict(frozen=True)

    approvals: list[dict[str, Any]] | None = None


class GetPullRequestOverrideStateResult(BaseModel):
    """Result of get_pull_request_override_state."""

    model_config = ConfigDict(frozen=True)

    overridden: bool | None = None
    overrider: str | None = None


class GetRepositoryTriggersResult(BaseModel):
    """Result of get_repository_triggers."""

    model_config = ConfigDict(frozen=True)

    configuration_id: str | None = None
    triggers: list[dict[str, Any]] | None = None


class ListApprovalRuleTemplatesResult(BaseModel):
    """Result of list_approval_rule_templates."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template_names: list[str] | None = None
    next_token: str | None = None


class ListAssociatedApprovalRuleTemplatesForRepositoryResult(BaseModel):
    """Result of list_associated_approval_rule_templates_for_repository."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template_names: list[str] | None = None
    next_token: str | None = None


class ListFileCommitHistoryResult(BaseModel):
    """Result of list_file_commit_history."""

    model_config = ConfigDict(frozen=True)

    revision_dag: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRepositoriesForApprovalRuleTemplateResult(BaseModel):
    """Result of list_repositories_for_approval_rule_template."""

    model_config = ConfigDict(frozen=True)

    repository_names: list[str] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None
    next_token: str | None = None


class MergeBranchesByThreeWayResult(BaseModel):
    """Result of merge_branches_by_three_way."""

    model_config = ConfigDict(frozen=True)

    commit_id: str | None = None
    tree_id: str | None = None


class MergePullRequestBySquashResult(BaseModel):
    """Result of merge_pull_request_by_squash."""

    model_config = ConfigDict(frozen=True)

    pull_request: dict[str, Any] | None = None


class MergePullRequestByThreeWayResult(BaseModel):
    """Result of merge_pull_request_by_three_way."""

    model_config = ConfigDict(frozen=True)

    pull_request: dict[str, Any] | None = None


class PostCommentForComparedCommitResult(BaseModel):
    """Result of post_comment_for_compared_commit."""

    model_config = ConfigDict(frozen=True)

    repository_name: str | None = None
    before_commit_id: str | None = None
    after_commit_id: str | None = None
    before_blob_id: str | None = None
    after_blob_id: str | None = None
    location: dict[str, Any] | None = None
    comment: dict[str, Any] | None = None


class PostCommentForPullRequestResult(BaseModel):
    """Result of post_comment_for_pull_request."""

    model_config = ConfigDict(frozen=True)

    repository_name: str | None = None
    pull_request_id: str | None = None
    before_commit_id: str | None = None
    after_commit_id: str | None = None
    before_blob_id: str | None = None
    after_blob_id: str | None = None
    location: dict[str, Any] | None = None
    comment: dict[str, Any] | None = None


class PostCommentReplyResult(BaseModel):
    """Result of post_comment_reply."""

    model_config = ConfigDict(frozen=True)

    comment: dict[str, Any] | None = None


class PutRepositoryTriggersResult(BaseModel):
    """Result of put_repository_triggers."""

    model_config = ConfigDict(frozen=True)

    configuration_id: str | None = None


class RunRepositoryTriggersResult(BaseModel):
    """Result of run_repository_triggers."""

    model_config = ConfigDict(frozen=True)

    successful_executions: list[str] | None = None
    failed_executions: list[dict[str, Any]] | None = None


class UpdateApprovalRuleTemplateContentResult(BaseModel):
    """Result of update_approval_rule_template_content."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template: dict[str, Any] | None = None


class UpdateApprovalRuleTemplateDescriptionResult(BaseModel):
    """Result of update_approval_rule_template_description."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template: dict[str, Any] | None = None


class UpdateApprovalRuleTemplateNameResult(BaseModel):
    """Result of update_approval_rule_template_name."""

    model_config = ConfigDict(frozen=True)

    approval_rule_template: dict[str, Any] | None = None


class UpdateCommentResult(BaseModel):
    """Result of update_comment."""

    model_config = ConfigDict(frozen=True)

    comment: dict[str, Any] | None = None


class UpdatePullRequestApprovalRuleContentResult(BaseModel):
    """Result of update_pull_request_approval_rule_content."""

    model_config = ConfigDict(frozen=True)

    approval_rule: dict[str, Any] | None = None


class UpdatePullRequestDescriptionResult(BaseModel):
    """Result of update_pull_request_description."""

    model_config = ConfigDict(frozen=True)

    pull_request: dict[str, Any] | None = None


class UpdatePullRequestStatusResult(BaseModel):
    """Result of update_pull_request_status."""

    model_config = ConfigDict(frozen=True)

    pull_request: dict[str, Any] | None = None


class UpdatePullRequestTitleResult(BaseModel):
    """Result of update_pull_request_title."""

    model_config = ConfigDict(frozen=True)

    pull_request: dict[str, Any] | None = None


class UpdateRepositoryEncryptionKeyResult(BaseModel):
    """Result of update_repository_encryption_key."""

    model_config = ConfigDict(frozen=True)

    repository_id: str | None = None
    kms_key_id: str | None = None
    original_kms_key_id: str | None = None


def associate_approval_rule_template_with_repository(
    approval_rule_template_name: str,
    repository_name: str,
    region_name: str | None = None,
) -> None:
    """Associate approval rule template with repository.

    Args:
        approval_rule_template_name: Approval rule template name.
        repository_name: Repository name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryName"] = repository_name
    try:
        client.associate_approval_rule_template_with_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to associate approval rule template with repository"
        ) from exc
    return None


def batch_associate_approval_rule_template_with_repositories(
    approval_rule_template_name: str,
    repository_names: list[str],
    region_name: str | None = None,
) -> BatchAssociateApprovalRuleTemplateWithRepositoriesResult:
    """Batch associate approval rule template with repositories.

    Args:
        approval_rule_template_name: Approval rule template name.
        repository_names: Repository names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryNames"] = repository_names
    try:
        resp = client.batch_associate_approval_rule_template_with_repositories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to batch associate approval rule template with repositories"
        ) from exc
    return BatchAssociateApprovalRuleTemplateWithRepositoriesResult(
        associated_repository_names=resp.get("associatedRepositoryNames"),
        errors=resp.get("errors"),
    )


def batch_describe_merge_conflicts(
    repository_name: str,
    destination_commit_specifier: str,
    source_commit_specifier: str,
    merge_option: str,
    *,
    max_merge_hunks: int | None = None,
    max_conflict_files: int | None = None,
    file_paths: list[str] | None = None,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> BatchDescribeMergeConflictsResult:
    """Batch describe merge conflicts.

    Args:
        repository_name: Repository name.
        destination_commit_specifier: Destination commit specifier.
        source_commit_specifier: Source commit specifier.
        merge_option: Merge option.
        max_merge_hunks: Max merge hunks.
        max_conflict_files: Max conflict files.
        file_paths: File paths.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["mergeOption"] = merge_option
    if max_merge_hunks is not None:
        kwargs["maxMergeHunks"] = max_merge_hunks
    if max_conflict_files is not None:
        kwargs["maxConflictFiles"] = max_conflict_files
    if file_paths is not None:
        kwargs["filePaths"] = file_paths
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.batch_describe_merge_conflicts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch describe merge conflicts") from exc
    return BatchDescribeMergeConflictsResult(
        conflicts=resp.get("conflicts"),
        next_token=resp.get("nextToken"),
        errors=resp.get("errors"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


def batch_disassociate_approval_rule_template_from_repositories(
    approval_rule_template_name: str,
    repository_names: list[str],
    region_name: str | None = None,
) -> BatchDisassociateApprovalRuleTemplateFromRepositoriesResult:
    """Batch disassociate approval rule template from repositories.

    Args:
        approval_rule_template_name: Approval rule template name.
        repository_names: Repository names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryNames"] = repository_names
    try:
        resp = client.batch_disassociate_approval_rule_template_from_repositories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to batch disassociate approval rule template from repositories"
        ) from exc
    return BatchDisassociateApprovalRuleTemplateFromRepositoriesResult(
        disassociated_repository_names=resp.get("disassociatedRepositoryNames"),
        errors=resp.get("errors"),
    )


def batch_get_commits(
    commit_ids: list[str],
    repository_name: str,
    region_name: str | None = None,
) -> BatchGetCommitsResult:
    """Batch get commits.

    Args:
        commit_ids: Commit ids.
        repository_name: Repository name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commitIds"] = commit_ids
    kwargs["repositoryName"] = repository_name
    try:
        resp = client.batch_get_commits(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get commits") from exc
    return BatchGetCommitsResult(
        commits=resp.get("commits"),
        errors=resp.get("errors"),
    )


def batch_get_repositories(
    repository_names: list[str],
    region_name: str | None = None,
) -> BatchGetRepositoriesResult:
    """Batch get repositories.

    Args:
        repository_names: Repository names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryNames"] = repository_names
    try:
        resp = client.batch_get_repositories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get repositories") from exc
    return BatchGetRepositoriesResult(
        repositories=resp.get("repositories"),
        repositories_not_found=resp.get("repositoriesNotFound"),
        errors=resp.get("errors"),
    )


def create_approval_rule_template(
    approval_rule_template_name: str,
    approval_rule_template_content: str,
    *,
    approval_rule_template_description: str | None = None,
    region_name: str | None = None,
) -> CreateApprovalRuleTemplateResult:
    """Create approval rule template.

    Args:
        approval_rule_template_name: Approval rule template name.
        approval_rule_template_content: Approval rule template content.
        approval_rule_template_description: Approval rule template description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["approvalRuleTemplateContent"] = approval_rule_template_content
    if approval_rule_template_description is not None:
        kwargs["approvalRuleTemplateDescription"] = approval_rule_template_description
    try:
        resp = client.create_approval_rule_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create approval rule template") from exc
    return CreateApprovalRuleTemplateResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


def create_pull_request_approval_rule(
    pull_request_id: str,
    approval_rule_name: str,
    approval_rule_content: str,
    region_name: str | None = None,
) -> CreatePullRequestApprovalRuleResult:
    """Create pull request approval rule.

    Args:
        pull_request_id: Pull request id.
        approval_rule_name: Approval rule name.
        approval_rule_content: Approval rule content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    kwargs["approvalRuleContent"] = approval_rule_content
    try:
        resp = client.create_pull_request_approval_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create pull request approval rule") from exc
    return CreatePullRequestApprovalRuleResult(
        approval_rule=resp.get("approvalRule"),
    )


def create_unreferenced_merge_commit(
    repository_name: str,
    source_commit_specifier: str,
    destination_commit_specifier: str,
    merge_option: str,
    *,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    commit_message: str | None = None,
    keep_empty_folders: bool | None = None,
    conflict_resolution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUnreferencedMergeCommitResult:
    """Create unreferenced merge commit.

    Args:
        repository_name: Repository name.
        source_commit_specifier: Source commit specifier.
        destination_commit_specifier: Destination commit specifier.
        merge_option: Merge option.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        author_name: Author name.
        email: Email.
        commit_message: Commit message.
        keep_empty_folders: Keep empty folders.
        conflict_resolution: Conflict resolution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    kwargs["mergeOption"] = merge_option
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if keep_empty_folders is not None:
        kwargs["keepEmptyFolders"] = keep_empty_folders
    if conflict_resolution is not None:
        kwargs["conflictResolution"] = conflict_resolution
    try:
        resp = client.create_unreferenced_merge_commit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create unreferenced merge commit") from exc
    return CreateUnreferencedMergeCommitResult(
        commit_id=resp.get("commitId"),
        tree_id=resp.get("treeId"),
    )


def delete_approval_rule_template(
    approval_rule_template_name: str,
    region_name: str | None = None,
) -> DeleteApprovalRuleTemplateResult:
    """Delete approval rule template.

    Args:
        approval_rule_template_name: Approval rule template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    try:
        resp = client.delete_approval_rule_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete approval rule template") from exc
    return DeleteApprovalRuleTemplateResult(
        approval_rule_template_id=resp.get("approvalRuleTemplateId"),
    )


def delete_comment_content(
    comment_id: str,
    region_name: str | None = None,
) -> DeleteCommentContentResult:
    """Delete comment content.

    Args:
        comment_id: Comment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    try:
        resp = client.delete_comment_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete comment content") from exc
    return DeleteCommentContentResult(
        comment=resp.get("comment"),
    )


def delete_pull_request_approval_rule(
    pull_request_id: str,
    approval_rule_name: str,
    region_name: str | None = None,
) -> DeletePullRequestApprovalRuleResult:
    """Delete pull request approval rule.

    Args:
        pull_request_id: Pull request id.
        approval_rule_name: Approval rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    try:
        resp = client.delete_pull_request_approval_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete pull request approval rule") from exc
    return DeletePullRequestApprovalRuleResult(
        approval_rule_id=resp.get("approvalRuleId"),
    )


def describe_merge_conflicts(
    repository_name: str,
    destination_commit_specifier: str,
    source_commit_specifier: str,
    merge_option: str,
    file_path: str,
    *,
    max_merge_hunks: int | None = None,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMergeConflictsResult:
    """Describe merge conflicts.

    Args:
        repository_name: Repository name.
        destination_commit_specifier: Destination commit specifier.
        source_commit_specifier: Source commit specifier.
        merge_option: Merge option.
        file_path: File path.
        max_merge_hunks: Max merge hunks.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["mergeOption"] = merge_option
    kwargs["filePath"] = file_path
    if max_merge_hunks is not None:
        kwargs["maxMergeHunks"] = max_merge_hunks
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.describe_merge_conflicts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe merge conflicts") from exc
    return DescribeMergeConflictsResult(
        conflict_metadata=resp.get("conflictMetadata"),
        merge_hunks=resp.get("mergeHunks"),
        next_token=resp.get("nextToken"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


def describe_pull_request_events(
    pull_request_id: str,
    *,
    pull_request_event_type: str | None = None,
    actor_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribePullRequestEventsResult:
    """Describe pull request events.

    Args:
        pull_request_id: Pull request id.
        pull_request_event_type: Pull request event type.
        actor_arn: Actor arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    if pull_request_event_type is not None:
        kwargs["pullRequestEventType"] = pull_request_event_type
    if actor_arn is not None:
        kwargs["actorArn"] = actor_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.describe_pull_request_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pull request events") from exc
    return DescribePullRequestEventsResult(
        pull_request_events=resp.get("pullRequestEvents"),
        next_token=resp.get("nextToken"),
    )


def disassociate_approval_rule_template_from_repository(
    approval_rule_template_name: str,
    repository_name: str,
    region_name: str | None = None,
) -> None:
    """Disassociate approval rule template from repository.

    Args:
        approval_rule_template_name: Approval rule template name.
        repository_name: Repository name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryName"] = repository_name
    try:
        client.disassociate_approval_rule_template_from_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to disassociate approval rule template from repository"
        ) from exc
    return None


def evaluate_pull_request_approval_rules(
    pull_request_id: str,
    revision_id: str,
    region_name: str | None = None,
) -> EvaluatePullRequestApprovalRulesResult:
    """Evaluate pull request approval rules.

    Args:
        pull_request_id: Pull request id.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = client.evaluate_pull_request_approval_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to evaluate pull request approval rules") from exc
    return EvaluatePullRequestApprovalRulesResult(
        evaluation=resp.get("evaluation"),
    )


def get_approval_rule_template(
    approval_rule_template_name: str,
    region_name: str | None = None,
) -> GetApprovalRuleTemplateResult:
    """Get approval rule template.

    Args:
        approval_rule_template_name: Approval rule template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    try:
        resp = client.get_approval_rule_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get approval rule template") from exc
    return GetApprovalRuleTemplateResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


def get_comment(
    comment_id: str,
    region_name: str | None = None,
) -> GetCommentResult:
    """Get comment.

    Args:
        comment_id: Comment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    try:
        resp = client.get_comment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get comment") from exc
    return GetCommentResult(
        comment=resp.get("comment"),
    )


def get_comment_reactions(
    comment_id: str,
    *,
    reaction_user_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetCommentReactionsResult:
    """Get comment reactions.

    Args:
        comment_id: Comment id.
        reaction_user_arn: Reaction user arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    if reaction_user_arn is not None:
        kwargs["reactionUserArn"] = reaction_user_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.get_comment_reactions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get comment reactions") from exc
    return GetCommentReactionsResult(
        reactions_for_comment=resp.get("reactionsForComment"),
        next_token=resp.get("nextToken"),
    )


def get_comments_for_compared_commit(
    repository_name: str,
    after_commit_id: str,
    *,
    before_commit_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetCommentsForComparedCommitResult:
    """Get comments for compared commit.

    Args:
        repository_name: Repository name.
        after_commit_id: After commit id.
        before_commit_id: Before commit id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["afterCommitId"] = after_commit_id
    if before_commit_id is not None:
        kwargs["beforeCommitId"] = before_commit_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.get_comments_for_compared_commit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get comments for compared commit") from exc
    return GetCommentsForComparedCommitResult(
        comments_for_compared_commit_data=resp.get("commentsForComparedCommitData"),
        next_token=resp.get("nextToken"),
    )


def get_comments_for_pull_request(
    pull_request_id: str,
    *,
    repository_name: str | None = None,
    before_commit_id: str | None = None,
    after_commit_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetCommentsForPullRequestResult:
    """Get comments for pull request.

    Args:
        pull_request_id: Pull request id.
        repository_name: Repository name.
        before_commit_id: Before commit id.
        after_commit_id: After commit id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    if repository_name is not None:
        kwargs["repositoryName"] = repository_name
    if before_commit_id is not None:
        kwargs["beforeCommitId"] = before_commit_id
    if after_commit_id is not None:
        kwargs["afterCommitId"] = after_commit_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.get_comments_for_pull_request(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get comments for pull request") from exc
    return GetCommentsForPullRequestResult(
        comments_for_pull_request_data=resp.get("commentsForPullRequestData"),
        next_token=resp.get("nextToken"),
    )


def get_folder(
    repository_name: str,
    folder_path: str,
    *,
    commit_specifier: str | None = None,
    region_name: str | None = None,
) -> GetFolderResult:
    """Get folder.

    Args:
        repository_name: Repository name.
        folder_path: Folder path.
        commit_specifier: Commit specifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["folderPath"] = folder_path
    if commit_specifier is not None:
        kwargs["commitSpecifier"] = commit_specifier
    try:
        resp = client.get_folder(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get folder") from exc
    return GetFolderResult(
        commit_id=resp.get("commitId"),
        folder_path=resp.get("folderPath"),
        tree_id=resp.get("treeId"),
        sub_folders=resp.get("subFolders"),
        files=resp.get("files"),
        symbolic_links=resp.get("symbolicLinks"),
        sub_modules=resp.get("subModules"),
    )


def get_merge_commit(
    repository_name: str,
    source_commit_specifier: str,
    destination_commit_specifier: str,
    *,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    region_name: str | None = None,
) -> GetMergeCommitResult:
    """Get merge commit.

    Args:
        repository_name: Repository name.
        source_commit_specifier: Source commit specifier.
        destination_commit_specifier: Destination commit specifier.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    try:
        resp = client.get_merge_commit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get merge commit") from exc
    return GetMergeCommitResult(
        source_commit_id=resp.get("sourceCommitId"),
        destination_commit_id=resp.get("destinationCommitId"),
        base_commit_id=resp.get("baseCommitId"),
        merged_commit_id=resp.get("mergedCommitId"),
    )


def get_merge_conflicts(
    repository_name: str,
    destination_commit_specifier: str,
    source_commit_specifier: str,
    merge_option: str,
    *,
    conflict_detail_level: str | None = None,
    max_conflict_files: int | None = None,
    conflict_resolution_strategy: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetMergeConflictsResult:
    """Get merge conflicts.

    Args:
        repository_name: Repository name.
        destination_commit_specifier: Destination commit specifier.
        source_commit_specifier: Source commit specifier.
        merge_option: Merge option.
        conflict_detail_level: Conflict detail level.
        max_conflict_files: Max conflict files.
        conflict_resolution_strategy: Conflict resolution strategy.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["mergeOption"] = merge_option
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if max_conflict_files is not None:
        kwargs["maxConflictFiles"] = max_conflict_files
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.get_merge_conflicts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get merge conflicts") from exc
    return GetMergeConflictsResult(
        mergeable=resp.get("mergeable"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
        conflict_metadata_list=resp.get("conflictMetadataList"),
        next_token=resp.get("nextToken"),
    )


def get_merge_options(
    repository_name: str,
    source_commit_specifier: str,
    destination_commit_specifier: str,
    *,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    region_name: str | None = None,
) -> GetMergeOptionsResult:
    """Get merge options.

    Args:
        repository_name: Repository name.
        source_commit_specifier: Source commit specifier.
        destination_commit_specifier: Destination commit specifier.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    try:
        resp = client.get_merge_options(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get merge options") from exc
    return GetMergeOptionsResult(
        merge_options=resp.get("mergeOptions"),
        source_commit_id=resp.get("sourceCommitId"),
        destination_commit_id=resp.get("destinationCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


def get_pull_request_approval_states(
    pull_request_id: str,
    revision_id: str,
    region_name: str | None = None,
) -> GetPullRequestApprovalStatesResult:
    """Get pull request approval states.

    Args:
        pull_request_id: Pull request id.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = client.get_pull_request_approval_states(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get pull request approval states") from exc
    return GetPullRequestApprovalStatesResult(
        approvals=resp.get("approvals"),
    )


def get_pull_request_override_state(
    pull_request_id: str,
    revision_id: str,
    region_name: str | None = None,
) -> GetPullRequestOverrideStateResult:
    """Get pull request override state.

    Args:
        pull_request_id: Pull request id.
        revision_id: Revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = client.get_pull_request_override_state(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get pull request override state") from exc
    return GetPullRequestOverrideStateResult(
        overridden=resp.get("overridden"),
        overrider=resp.get("overrider"),
    )


def get_repository_triggers(
    repository_name: str,
    region_name: str | None = None,
) -> GetRepositoryTriggersResult:
    """Get repository triggers.

    Args:
        repository_name: Repository name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    try:
        resp = client.get_repository_triggers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get repository triggers") from exc
    return GetRepositoryTriggersResult(
        configuration_id=resp.get("configurationId"),
        triggers=resp.get("triggers"),
    )


def list_approval_rule_templates(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListApprovalRuleTemplatesResult:
    """List approval rule templates.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_approval_rule_templates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list approval rule templates") from exc
    return ListApprovalRuleTemplatesResult(
        approval_rule_template_names=resp.get("approvalRuleTemplateNames"),
        next_token=resp.get("nextToken"),
    )


def list_associated_approval_rule_templates_for_repository(
    repository_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAssociatedApprovalRuleTemplatesForRepositoryResult:
    """List associated approval rule templates for repository.

    Args:
        repository_name: Repository name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_associated_approval_rule_templates_for_repository(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list associated approval rule templates for repository"
        ) from exc
    return ListAssociatedApprovalRuleTemplatesForRepositoryResult(
        approval_rule_template_names=resp.get("approvalRuleTemplateNames"),
        next_token=resp.get("nextToken"),
    )


def list_file_commit_history(
    repository_name: str,
    file_path: str,
    *,
    commit_specifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListFileCommitHistoryResult:
    """List file commit history.

    Args:
        repository_name: Repository name.
        file_path: File path.
        commit_specifier: Commit specifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["filePath"] = file_path
    if commit_specifier is not None:
        kwargs["commitSpecifier"] = commit_specifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_file_commit_history(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list file commit history") from exc
    return ListFileCommitHistoryResult(
        revision_dag=resp.get("revisionDag"),
        next_token=resp.get("nextToken"),
    )


def list_repositories_for_approval_rule_template(
    approval_rule_template_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRepositoriesForApprovalRuleTemplateResult:
    """List repositories for approval rule template.

    Args:
        approval_rule_template_name: Approval rule template name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_repositories_for_approval_rule_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list repositories for approval rule template") from exc
    return ListRepositoriesForApprovalRuleTemplateResult(
        repository_names=resp.get("repositoryNames"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
        next_token=resp.get("nextToken"),
    )


def merge_branches_by_three_way(
    repository_name: str,
    source_commit_specifier: str,
    destination_commit_specifier: str,
    *,
    target_branch: str | None = None,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    commit_message: str | None = None,
    keep_empty_folders: bool | None = None,
    conflict_resolution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> MergeBranchesByThreeWayResult:
    """Merge branches by three way.

    Args:
        repository_name: Repository name.
        source_commit_specifier: Source commit specifier.
        destination_commit_specifier: Destination commit specifier.
        target_branch: Target branch.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        author_name: Author name.
        email: Email.
        commit_message: Commit message.
        keep_empty_folders: Keep empty folders.
        conflict_resolution: Conflict resolution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    if target_branch is not None:
        kwargs["targetBranch"] = target_branch
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if keep_empty_folders is not None:
        kwargs["keepEmptyFolders"] = keep_empty_folders
    if conflict_resolution is not None:
        kwargs["conflictResolution"] = conflict_resolution
    try:
        resp = client.merge_branches_by_three_way(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to merge branches by three way") from exc
    return MergeBranchesByThreeWayResult(
        commit_id=resp.get("commitId"),
        tree_id=resp.get("treeId"),
    )


def merge_pull_request_by_squash(
    pull_request_id: str,
    repository_name: str,
    *,
    source_commit_id: str | None = None,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    commit_message: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    keep_empty_folders: bool | None = None,
    conflict_resolution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> MergePullRequestBySquashResult:
    """Merge pull request by squash.

    Args:
        pull_request_id: Pull request id.
        repository_name: Repository name.
        source_commit_id: Source commit id.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        commit_message: Commit message.
        author_name: Author name.
        email: Email.
        keep_empty_folders: Keep empty folders.
        conflict_resolution: Conflict resolution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["repositoryName"] = repository_name
    if source_commit_id is not None:
        kwargs["sourceCommitId"] = source_commit_id
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if keep_empty_folders is not None:
        kwargs["keepEmptyFolders"] = keep_empty_folders
    if conflict_resolution is not None:
        kwargs["conflictResolution"] = conflict_resolution
    try:
        resp = client.merge_pull_request_by_squash(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to merge pull request by squash") from exc
    return MergePullRequestBySquashResult(
        pull_request=resp.get("pullRequest"),
    )


def merge_pull_request_by_three_way(
    pull_request_id: str,
    repository_name: str,
    *,
    source_commit_id: str | None = None,
    conflict_detail_level: str | None = None,
    conflict_resolution_strategy: str | None = None,
    commit_message: str | None = None,
    author_name: str | None = None,
    email: str | None = None,
    keep_empty_folders: bool | None = None,
    conflict_resolution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> MergePullRequestByThreeWayResult:
    """Merge pull request by three way.

    Args:
        pull_request_id: Pull request id.
        repository_name: Repository name.
        source_commit_id: Source commit id.
        conflict_detail_level: Conflict detail level.
        conflict_resolution_strategy: Conflict resolution strategy.
        commit_message: Commit message.
        author_name: Author name.
        email: Email.
        keep_empty_folders: Keep empty folders.
        conflict_resolution: Conflict resolution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["repositoryName"] = repository_name
    if source_commit_id is not None:
        kwargs["sourceCommitId"] = source_commit_id
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    if commit_message is not None:
        kwargs["commitMessage"] = commit_message
    if author_name is not None:
        kwargs["authorName"] = author_name
    if email is not None:
        kwargs["email"] = email
    if keep_empty_folders is not None:
        kwargs["keepEmptyFolders"] = keep_empty_folders
    if conflict_resolution is not None:
        kwargs["conflictResolution"] = conflict_resolution
    try:
        resp = client.merge_pull_request_by_three_way(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to merge pull request by three way") from exc
    return MergePullRequestByThreeWayResult(
        pull_request=resp.get("pullRequest"),
    )


def override_pull_request_approval_rules(
    pull_request_id: str,
    revision_id: str,
    override_status: str,
    region_name: str | None = None,
) -> None:
    """Override pull request approval rules.

    Args:
        pull_request_id: Pull request id.
        revision_id: Revision id.
        override_status: Override status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    kwargs["overrideStatus"] = override_status
    try:
        client.override_pull_request_approval_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to override pull request approval rules") from exc
    return None


def post_comment_for_compared_commit(
    repository_name: str,
    after_commit_id: str,
    content: str,
    *,
    before_commit_id: str | None = None,
    location: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> PostCommentForComparedCommitResult:
    """Post comment for compared commit.

    Args:
        repository_name: Repository name.
        after_commit_id: After commit id.
        content: Content.
        before_commit_id: Before commit id.
        location: Location.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["afterCommitId"] = after_commit_id
    kwargs["content"] = content
    if before_commit_id is not None:
        kwargs["beforeCommitId"] = before_commit_id
    if location is not None:
        kwargs["location"] = location
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.post_comment_for_compared_commit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to post comment for compared commit") from exc
    return PostCommentForComparedCommitResult(
        repository_name=resp.get("repositoryName"),
        before_commit_id=resp.get("beforeCommitId"),
        after_commit_id=resp.get("afterCommitId"),
        before_blob_id=resp.get("beforeBlobId"),
        after_blob_id=resp.get("afterBlobId"),
        location=resp.get("location"),
        comment=resp.get("comment"),
    )


def post_comment_for_pull_request(
    pull_request_id: str,
    repository_name: str,
    before_commit_id: str,
    after_commit_id: str,
    content: str,
    *,
    location: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> PostCommentForPullRequestResult:
    """Post comment for pull request.

    Args:
        pull_request_id: Pull request id.
        repository_name: Repository name.
        before_commit_id: Before commit id.
        after_commit_id: After commit id.
        content: Content.
        location: Location.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["repositoryName"] = repository_name
    kwargs["beforeCommitId"] = before_commit_id
    kwargs["afterCommitId"] = after_commit_id
    kwargs["content"] = content
    if location is not None:
        kwargs["location"] = location
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.post_comment_for_pull_request(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to post comment for pull request") from exc
    return PostCommentForPullRequestResult(
        repository_name=resp.get("repositoryName"),
        pull_request_id=resp.get("pullRequestId"),
        before_commit_id=resp.get("beforeCommitId"),
        after_commit_id=resp.get("afterCommitId"),
        before_blob_id=resp.get("beforeBlobId"),
        after_blob_id=resp.get("afterBlobId"),
        location=resp.get("location"),
        comment=resp.get("comment"),
    )


def post_comment_reply(
    in_reply_to: str,
    content: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> PostCommentReplyResult:
    """Post comment reply.

    Args:
        in_reply_to: In reply to.
        content: Content.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["inReplyTo"] = in_reply_to
    kwargs["content"] = content
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.post_comment_reply(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to post comment reply") from exc
    return PostCommentReplyResult(
        comment=resp.get("comment"),
    )


def put_comment_reaction(
    comment_id: str,
    reaction_value: str,
    region_name: str | None = None,
) -> None:
    """Put comment reaction.

    Args:
        comment_id: Comment id.
        reaction_value: Reaction value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    kwargs["reactionValue"] = reaction_value
    try:
        client.put_comment_reaction(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put comment reaction") from exc
    return None


def put_repository_triggers(
    repository_name: str,
    triggers: list[dict[str, Any]],
    region_name: str | None = None,
) -> PutRepositoryTriggersResult:
    """Put repository triggers.

    Args:
        repository_name: Repository name.
        triggers: Triggers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["triggers"] = triggers
    try:
        resp = client.put_repository_triggers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put repository triggers") from exc
    return PutRepositoryTriggersResult(
        configuration_id=resp.get("configurationId"),
    )


def run_repository_triggers(
    repository_name: str,
    triggers: list[dict[str, Any]],
    region_name: str | None = None,
) -> RunRepositoryTriggersResult:
    """Run repository triggers.

    Args:
        repository_name: Repository name.
        triggers: Triggers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["triggers"] = triggers
    try:
        resp = client.test_repository_triggers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run repository triggers") from exc
    return RunRepositoryTriggersResult(
        successful_executions=resp.get("successfulExecutions"),
        failed_executions=resp.get("failedExecutions"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_approval_rule_template_content(
    approval_rule_template_name: str,
    new_rule_content: str,
    *,
    existing_rule_content_sha256: str | None = None,
    region_name: str | None = None,
) -> UpdateApprovalRuleTemplateContentResult:
    """Update approval rule template content.

    Args:
        approval_rule_template_name: Approval rule template name.
        new_rule_content: New rule content.
        existing_rule_content_sha256: Existing rule content sha256.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["newRuleContent"] = new_rule_content
    if existing_rule_content_sha256 is not None:
        kwargs["existingRuleContentSha256"] = existing_rule_content_sha256
    try:
        resp = client.update_approval_rule_template_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template content") from exc
    return UpdateApprovalRuleTemplateContentResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


def update_approval_rule_template_description(
    approval_rule_template_name: str,
    approval_rule_template_description: str,
    region_name: str | None = None,
) -> UpdateApprovalRuleTemplateDescriptionResult:
    """Update approval rule template description.

    Args:
        approval_rule_template_name: Approval rule template name.
        approval_rule_template_description: Approval rule template description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["approvalRuleTemplateDescription"] = approval_rule_template_description
    try:
        resp = client.update_approval_rule_template_description(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template description") from exc
    return UpdateApprovalRuleTemplateDescriptionResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


def update_approval_rule_template_name(
    old_approval_rule_template_name: str,
    new_approval_rule_template_name: str,
    region_name: str | None = None,
) -> UpdateApprovalRuleTemplateNameResult:
    """Update approval rule template name.

    Args:
        old_approval_rule_template_name: Old approval rule template name.
        new_approval_rule_template_name: New approval rule template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["oldApprovalRuleTemplateName"] = old_approval_rule_template_name
    kwargs["newApprovalRuleTemplateName"] = new_approval_rule_template_name
    try:
        resp = client.update_approval_rule_template_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template name") from exc
    return UpdateApprovalRuleTemplateNameResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


def update_comment(
    comment_id: str,
    content: str,
    region_name: str | None = None,
) -> UpdateCommentResult:
    """Update comment.

    Args:
        comment_id: Comment id.
        content: Content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    kwargs["content"] = content
    try:
        resp = client.update_comment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update comment") from exc
    return UpdateCommentResult(
        comment=resp.get("comment"),
    )


def update_default_branch(
    repository_name: str,
    default_branch_name: str,
    region_name: str | None = None,
) -> None:
    """Update default branch.

    Args:
        repository_name: Repository name.
        default_branch_name: Default branch name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["defaultBranchName"] = default_branch_name
    try:
        client.update_default_branch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update default branch") from exc
    return None


def update_pull_request_approval_rule_content(
    pull_request_id: str,
    approval_rule_name: str,
    new_rule_content: str,
    *,
    existing_rule_content_sha256: str | None = None,
    region_name: str | None = None,
) -> UpdatePullRequestApprovalRuleContentResult:
    """Update pull request approval rule content.

    Args:
        pull_request_id: Pull request id.
        approval_rule_name: Approval rule name.
        new_rule_content: New rule content.
        existing_rule_content_sha256: Existing rule content sha256.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    kwargs["newRuleContent"] = new_rule_content
    if existing_rule_content_sha256 is not None:
        kwargs["existingRuleContentSha256"] = existing_rule_content_sha256
    try:
        resp = client.update_pull_request_approval_rule_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull request approval rule content") from exc
    return UpdatePullRequestApprovalRuleContentResult(
        approval_rule=resp.get("approvalRule"),
    )


def update_pull_request_approval_state(
    pull_request_id: str,
    revision_id: str,
    approval_state: str,
    region_name: str | None = None,
) -> None:
    """Update pull request approval state.

    Args:
        pull_request_id: Pull request id.
        revision_id: Revision id.
        approval_state: Approval state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    kwargs["approvalState"] = approval_state
    try:
        client.update_pull_request_approval_state(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull request approval state") from exc
    return None


def update_pull_request_description(
    pull_request_id: str,
    description: str,
    region_name: str | None = None,
) -> UpdatePullRequestDescriptionResult:
    """Update pull request description.

    Args:
        pull_request_id: Pull request id.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["description"] = description
    try:
        resp = client.update_pull_request_description(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull request description") from exc
    return UpdatePullRequestDescriptionResult(
        pull_request=resp.get("pullRequest"),
    )


def update_pull_request_status(
    pull_request_id: str,
    pull_request_status: str,
    region_name: str | None = None,
) -> UpdatePullRequestStatusResult:
    """Update pull request status.

    Args:
        pull_request_id: Pull request id.
        pull_request_status: Pull request status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["pullRequestStatus"] = pull_request_status
    try:
        resp = client.update_pull_request_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull request status") from exc
    return UpdatePullRequestStatusResult(
        pull_request=resp.get("pullRequest"),
    )


def update_pull_request_title(
    pull_request_id: str,
    title: str,
    region_name: str | None = None,
) -> UpdatePullRequestTitleResult:
    """Update pull request title.

    Args:
        pull_request_id: Pull request id.
        title: Title.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["title"] = title
    try:
        resp = client.update_pull_request_title(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pull request title") from exc
    return UpdatePullRequestTitleResult(
        pull_request=resp.get("pullRequest"),
    )


def update_repository_encryption_key(
    repository_name: str,
    kms_key_id: str,
    region_name: str | None = None,
) -> UpdateRepositoryEncryptionKeyResult:
    """Update repository encryption key.

    Args:
        repository_name: Repository name.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["kmsKeyId"] = kms_key_id
    try:
        resp = client.update_repository_encryption_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update repository encryption key") from exc
    return UpdateRepositoryEncryptionKeyResult(
        repository_id=resp.get("repositoryId"),
        kms_key_id=resp.get("kmsKeyId"),
        original_kms_key_id=resp.get("originalKmsKeyId"),
    )
