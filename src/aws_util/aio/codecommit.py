"""Native async CodeCommit utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.codecommit import (
    BatchAssociateApprovalRuleTemplateWithRepositoriesResult,
    BatchDescribeMergeConflictsResult,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesResult,
    BatchGetCommitsResult,
    BatchGetRepositoriesResult,
    BlobResult,
    BranchResult,
    CommitResult,
    CreateApprovalRuleTemplateResult,
    CreatePullRequestApprovalRuleResult,
    CreateUnreferencedMergeCommitResult,
    DeleteApprovalRuleTemplateResult,
    DeleteCommentContentResult,
    DeletePullRequestApprovalRuleResult,
    DescribeMergeConflictsResult,
    DescribePullRequestEventsResult,
    DiffResult,
    EvaluatePullRequestApprovalRulesResult,
    FileResult,
    GetApprovalRuleTemplateResult,
    GetCommentReactionsResult,
    GetCommentResult,
    GetCommentsForComparedCommitResult,
    GetCommentsForPullRequestResult,
    GetFolderResult,
    GetMergeCommitResult,
    GetMergeConflictsResult,
    GetMergeOptionsResult,
    GetPullRequestApprovalStatesResult,
    GetPullRequestOverrideStateResult,
    GetRepositoryTriggersResult,
    ListApprovalRuleTemplatesResult,
    ListAssociatedApprovalRuleTemplatesForRepositoryResult,
    ListFileCommitHistoryResult,
    ListRepositoriesForApprovalRuleTemplateResult,
    ListTagsForResourceResult,
    MergeBranchesByThreeWayResult,
    MergePullRequestBySquashResult,
    MergePullRequestByThreeWayResult,
    PostCommentForComparedCommitResult,
    PostCommentForPullRequestResult,
    PostCommentReplyResult,
    PullRequestResult,
    PutRepositoryTriggersResult,
    RepositoryResult,
    RunRepositoryTriggersResult,
    UpdateApprovalRuleTemplateContentResult,
    UpdateApprovalRuleTemplateDescriptionResult,
    UpdateApprovalRuleTemplateNameResult,
    UpdateCommentResult,
    UpdatePullRequestApprovalRuleContentResult,
    UpdatePullRequestDescriptionResult,
    UpdatePullRequestStatusResult,
    UpdatePullRequestTitleResult,
    UpdateRepositoryEncryptionKeyResult,
    _parse_branch,
    _parse_commit,
    _parse_diff,
    _parse_pull_request,
    _parse_repository,
)
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
# Repository operations
# ---------------------------------------------------------------------------


async def create_repository(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {"repositoryName": repository_name}
    if description is not None:
        kwargs["repositoryDescription"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_repository failed for {repository_name!r}") from exc
    return _parse_repository(resp["repositoryMetadata"])


async def get_repository(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "GetRepository",
            repositoryName=repository_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_repository failed for {repository_name!r}") from exc
    return _parse_repository(resp["repositoryMetadata"])


async def list_repositories(
    *,
    sort_by: str = "repositoryName",
    order: str = "ascending",
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List CodeCommit repositories.

    Args:
        sort_by: Sort field (``"repositoryName"`` or
            ``"lastModifiedDate"``).
        order: ``"ascending"`` or ``"descending"``.
        region_name: AWS region override.

    Returns:
        A list of repository name-ID dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("codecommit", region_name)
    repos: list[dict[str, Any]] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "sortBy": sort_by,
                "order": order,
            }
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListRepositories", **kwargs)
            repos.extend(resp.get("repositories", []))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_repositories failed") from exc
    return repos


async def delete_repository(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "DeleteRepository",
            repositoryName=repository_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"delete_repository failed for {repository_name!r}",
        ) from exc
    return resp.get("repositoryId")


async def update_repository_name(
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
    client = async_client("codecommit", region_name)
    try:
        await client.call(
            "UpdateRepositoryName",
            oldName=old_name,
            newName=new_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_repository_name failed for {old_name!r}",
        ) from exc


async def update_repository_description(
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
    client = async_client("codecommit", region_name)
    try:
        await client.call(
            "UpdateRepositoryDescription",
            repositoryName=repository_name,
            repositoryDescription=description,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_repository_description failed for {repository_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Branch operations
# ---------------------------------------------------------------------------


async def create_branch(
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
    client = async_client("codecommit", region_name)
    try:
        await client.call(
            "CreateBranch",
            repositoryName=repository_name,
            branchName=branch_name,
            commitId=commit_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_branch failed for {branch_name!r}") from exc


async def get_branch(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "GetBranch",
            repositoryName=repository_name,
            branchName=branch_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_branch failed for {branch_name!r}") from exc
    return _parse_branch(resp["branch"])


async def list_branches(
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
    client = async_client("codecommit", region_name)
    branches: list[str] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "repositoryName": repository_name,
            }
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListBranches", **kwargs)
            branches.extend(resp.get("branches", []))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_branches failed") from exc
    return branches


async def delete_branch(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "DeleteBranch",
            repositoryName=repository_name,
            branchName=branch_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_branch failed for {branch_name!r}") from exc
    return _parse_branch(resp["deletedBranch"])


# ---------------------------------------------------------------------------
# Merge operations
# ---------------------------------------------------------------------------


async def merge_branches_by_fast_forward(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "sourceCommitSpecifier": source_commit,
        "destinationCommitSpecifier": destination_commit,
    }
    if target_branch is not None:
        kwargs["targetBranch"] = target_branch
    try:
        resp = await client.call(
            "MergeBranchesByFastForward",
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "merge_branches_by_fast_forward failed") from exc
    return resp.get("commitId", "")


async def merge_branches_by_squash(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call(
            "MergeBranchesBySquash",
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "merge_branches_by_squash failed") from exc
    return resp.get("commitId", "")


# ---------------------------------------------------------------------------
# Commit operations
# ---------------------------------------------------------------------------


async def create_commit(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("CreateCommit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_commit failed") from exc
    return CommitResult(
        commit_id=resp.get("commitId", ""),
        tree_id=resp.get("treeId"),
        parents=resp.get("parents", []),
    )


async def get_commit(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "GetCommit",
            repositoryName=repository_name,
            commitId=commit_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_commit failed for {commit_id!r}") from exc
    return _parse_commit(resp["commit"])


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------


async def get_file(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "repositoryName": repository_name,
        "filePath": file_path,
    }
    if commit_specifier is not None:
        kwargs["commitSpecifier"] = commit_specifier
    try:
        resp = await client.call("GetFile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_file failed for {file_path!r}") from exc
    return FileResult(
        file_path=resp.get("filePath", file_path),
        file_size=resp.get("fileSize"),
        file_mode=resp.get("fileMode"),
        blob_id=resp.get("blobId"),
        commit_id=resp.get("commitId"),
        file_content=resp.get("fileContent"),
    )


async def put_file(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("PutFile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"put_file failed for {file_path!r}") from exc
    return {
        "commitId": resp.get("commitId", ""),
        "blobId": resp.get("blobId", ""),
        "treeId": resp.get("treeId", ""),
    }


async def delete_file(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("DeleteFile", **kwargs)
    except Exception as exc:
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


async def get_differences(
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
    client = async_client("codecommit", region_name)
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
        token: str | None = None
        while True:
            kw = dict(kwargs)
            if token:
                kw["NextToken"] = token
            resp = await client.call("GetDifferences", **kw)
            for d in resp.get("differences", []):
                diffs.append(_parse_diff(d))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "get_differences failed") from exc
    return diffs


# ---------------------------------------------------------------------------
# Pull request operations
# ---------------------------------------------------------------------------


async def create_pull_request(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "title": title,
        "targets": targets,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("CreatePullRequest", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_pull_request failed") from exc
    return _parse_pull_request(resp["pullRequest"])


async def get_pull_request(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "GetPullRequest",
            pullRequestId=pull_request_id,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_pull_request failed for {pull_request_id!r}",
        ) from exc
    return _parse_pull_request(resp["pullRequest"])


async def list_pull_requests(
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
    client = async_client("codecommit", region_name)
    pr_ids: list[str] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "repositoryName": repository_name,
                "pullRequestStatus": pull_request_status,
            }
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListPullRequests", **kwargs)
            pr_ids.extend(resp.get("pullRequestIds", []))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_pull_requests failed") from exc
    return pr_ids


async def merge_pull_request_by_fast_forward(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {
        "pullRequestId": pull_request_id,
        "repositoryName": repository_name,
    }
    if source_commit_id is not None:
        kwargs["sourceCommitId"] = source_commit_id
    try:
        resp = await client.call(
            "MergePullRequestByFastForward",
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "merge_pull_request_by_fast_forward failed",
        ) from exc
    return _parse_pull_request(resp["pullRequest"])


# ---------------------------------------------------------------------------
# Blob operations
# ---------------------------------------------------------------------------


async def get_blob(
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
    client = async_client("codecommit", region_name)
    try:
        resp = await client.call(
            "GetBlob",
            repositoryName=repository_name,
            blobId=blob_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_blob failed for {blob_id!r}") from exc
    return BlobResult(
        blob_id=blob_id,
        content=resp.get("content", b""),
    )


async def associate_approval_rule_template_with_repository(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryName"] = repository_name
    try:
        await client.call("AssociateApprovalRuleTemplateWithRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to associate approval rule template with repository"
        ) from exc
    return None


async def batch_associate_approval_rule_template_with_repositories(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryNames"] = repository_names
    try:
        resp = await client.call("BatchAssociateApprovalRuleTemplateWithRepositories", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch associate approval rule template with repositories"
        ) from exc
    return BatchAssociateApprovalRuleTemplateWithRepositoriesResult(
        associated_repository_names=resp.get("associatedRepositoryNames"),
        errors=resp.get("errors"),
    )


async def batch_describe_merge_conflicts(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("BatchDescribeMergeConflicts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch describe merge conflicts") from exc
    return BatchDescribeMergeConflictsResult(
        conflicts=resp.get("conflicts"),
        next_token=resp.get("nextToken"),
        errors=resp.get("errors"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


async def batch_disassociate_approval_rule_template_from_repositories(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryNames"] = repository_names
    try:
        resp = await client.call("BatchDisassociateApprovalRuleTemplateFromRepositories", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch disassociate approval rule template from repositories"
        ) from exc
    return BatchDisassociateApprovalRuleTemplateFromRepositoriesResult(
        disassociated_repository_names=resp.get("disassociatedRepositoryNames"),
        errors=resp.get("errors"),
    )


async def batch_get_commits(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commitIds"] = commit_ids
    kwargs["repositoryName"] = repository_name
    try:
        resp = await client.call("BatchGetCommits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get commits") from exc
    return BatchGetCommitsResult(
        commits=resp.get("commits"),
        errors=resp.get("errors"),
    )


async def batch_get_repositories(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryNames"] = repository_names
    try:
        resp = await client.call("BatchGetRepositories", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get repositories") from exc
    return BatchGetRepositoriesResult(
        repositories=resp.get("repositories"),
        repositories_not_found=resp.get("repositoriesNotFound"),
        errors=resp.get("errors"),
    )


async def create_approval_rule_template(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["approvalRuleTemplateContent"] = approval_rule_template_content
    if approval_rule_template_description is not None:
        kwargs["approvalRuleTemplateDescription"] = approval_rule_template_description
    try:
        resp = await client.call("CreateApprovalRuleTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create approval rule template") from exc
    return CreateApprovalRuleTemplateResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


async def create_pull_request_approval_rule(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    kwargs["approvalRuleContent"] = approval_rule_content
    try:
        resp = await client.call("CreatePullRequestApprovalRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create pull request approval rule") from exc
    return CreatePullRequestApprovalRuleResult(
        approval_rule=resp.get("approvalRule"),
    )


async def create_unreferenced_merge_commit(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("CreateUnreferencedMergeCommit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create unreferenced merge commit") from exc
    return CreateUnreferencedMergeCommitResult(
        commit_id=resp.get("commitId"),
        tree_id=resp.get("treeId"),
    )


async def delete_approval_rule_template(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    try:
        resp = await client.call("DeleteApprovalRuleTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete approval rule template") from exc
    return DeleteApprovalRuleTemplateResult(
        approval_rule_template_id=resp.get("approvalRuleTemplateId"),
    )


async def delete_comment_content(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    try:
        resp = await client.call("DeleteCommentContent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete comment content") from exc
    return DeleteCommentContentResult(
        comment=resp.get("comment"),
    )


async def delete_pull_request_approval_rule(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    try:
        resp = await client.call("DeletePullRequestApprovalRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete pull request approval rule") from exc
    return DeletePullRequestApprovalRuleResult(
        approval_rule_id=resp.get("approvalRuleId"),
    )


async def describe_merge_conflicts(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("DescribeMergeConflicts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe merge conflicts") from exc
    return DescribeMergeConflictsResult(
        conflict_metadata=resp.get("conflictMetadata"),
        merge_hunks=resp.get("mergeHunks"),
        next_token=resp.get("nextToken"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


async def describe_pull_request_events(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("DescribePullRequestEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe pull request events") from exc
    return DescribePullRequestEventsResult(
        pull_request_events=resp.get("pullRequestEvents"),
        next_token=resp.get("nextToken"),
    )


async def disassociate_approval_rule_template_from_repository(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["repositoryName"] = repository_name
    try:
        await client.call("DisassociateApprovalRuleTemplateFromRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to disassociate approval rule template from repository"
        ) from exc
    return None


async def evaluate_pull_request_approval_rules(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = await client.call("EvaluatePullRequestApprovalRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to evaluate pull request approval rules") from exc
    return EvaluatePullRequestApprovalRulesResult(
        evaluation=resp.get("evaluation"),
    )


async def get_approval_rule_template(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    try:
        resp = await client.call("GetApprovalRuleTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get approval rule template") from exc
    return GetApprovalRuleTemplateResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


async def get_comment(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    try:
        resp = await client.call("GetComment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get comment") from exc
    return GetCommentResult(
        comment=resp.get("comment"),
    )


async def get_comment_reactions(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    if reaction_user_arn is not None:
        kwargs["reactionUserArn"] = reaction_user_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("GetCommentReactions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get comment reactions") from exc
    return GetCommentReactionsResult(
        reactions_for_comment=resp.get("reactionsForComment"),
        next_token=resp.get("nextToken"),
    )


async def get_comments_for_compared_commit(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("GetCommentsForComparedCommit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get comments for compared commit") from exc
    return GetCommentsForComparedCommitResult(
        comments_for_compared_commit_data=resp.get("commentsForComparedCommitData"),
        next_token=resp.get("nextToken"),
    )


async def get_comments_for_pull_request(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("GetCommentsForPullRequest", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get comments for pull request") from exc
    return GetCommentsForPullRequestResult(
        comments_for_pull_request_data=resp.get("commentsForPullRequestData"),
        next_token=resp.get("nextToken"),
    )


async def get_folder(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["folderPath"] = folder_path
    if commit_specifier is not None:
        kwargs["commitSpecifier"] = commit_specifier
    try:
        resp = await client.call("GetFolder", **kwargs)
    except Exception as exc:
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


async def get_merge_commit(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    try:
        resp = await client.call("GetMergeCommit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get merge commit") from exc
    return GetMergeCommitResult(
        source_commit_id=resp.get("sourceCommitId"),
        destination_commit_id=resp.get("destinationCommitId"),
        base_commit_id=resp.get("baseCommitId"),
        merged_commit_id=resp.get("mergedCommitId"),
    )


async def get_merge_conflicts(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("GetMergeConflicts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get merge conflicts") from exc
    return GetMergeConflictsResult(
        mergeable=resp.get("mergeable"),
        destination_commit_id=resp.get("destinationCommitId"),
        source_commit_id=resp.get("sourceCommitId"),
        base_commit_id=resp.get("baseCommitId"),
        conflict_metadata_list=resp.get("conflictMetadataList"),
        next_token=resp.get("nextToken"),
    )


async def get_merge_options(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["sourceCommitSpecifier"] = source_commit_specifier
    kwargs["destinationCommitSpecifier"] = destination_commit_specifier
    if conflict_detail_level is not None:
        kwargs["conflictDetailLevel"] = conflict_detail_level
    if conflict_resolution_strategy is not None:
        kwargs["conflictResolutionStrategy"] = conflict_resolution_strategy
    try:
        resp = await client.call("GetMergeOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get merge options") from exc
    return GetMergeOptionsResult(
        merge_options=resp.get("mergeOptions"),
        source_commit_id=resp.get("sourceCommitId"),
        destination_commit_id=resp.get("destinationCommitId"),
        base_commit_id=resp.get("baseCommitId"),
    )


async def get_pull_request_approval_states(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = await client.call("GetPullRequestApprovalStates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get pull request approval states") from exc
    return GetPullRequestApprovalStatesResult(
        approvals=resp.get("approvals"),
    )


async def get_pull_request_override_state(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    try:
        resp = await client.call("GetPullRequestOverrideState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get pull request override state") from exc
    return GetPullRequestOverrideStateResult(
        overridden=resp.get("overridden"),
        overrider=resp.get("overrider"),
    )


async def get_repository_triggers(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    try:
        resp = await client.call("GetRepositoryTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get repository triggers") from exc
    return GetRepositoryTriggersResult(
        configuration_id=resp.get("configurationId"),
        triggers=resp.get("triggers"),
    )


async def list_approval_rule_templates(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListApprovalRuleTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list approval rule templates") from exc
    return ListApprovalRuleTemplatesResult(
        approval_rule_template_names=resp.get("approvalRuleTemplateNames"),
        next_token=resp.get("nextToken"),
    )


async def list_associated_approval_rule_templates_for_repository(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAssociatedApprovalRuleTemplatesForRepository", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list associated approval rule templates for repository"
        ) from exc
    return ListAssociatedApprovalRuleTemplatesForRepositoryResult(
        approval_rule_template_names=resp.get("approvalRuleTemplateNames"),
        next_token=resp.get("nextToken"),
    )


async def list_file_commit_history(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("ListFileCommitHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list file commit history") from exc
    return ListFileCommitHistoryResult(
        revision_dag=resp.get("revisionDag"),
        next_token=resp.get("nextToken"),
    )


async def list_repositories_for_approval_rule_template(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListRepositoriesForApprovalRuleTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list repositories for approval rule template") from exc
    return ListRepositoriesForApprovalRuleTemplateResult(
        repository_names=resp.get("repositoryNames"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
        next_token=resp.get("nextToken"),
    )


async def merge_branches_by_three_way(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("MergeBranchesByThreeWay", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to merge branches by three way") from exc
    return MergeBranchesByThreeWayResult(
        commit_id=resp.get("commitId"),
        tree_id=resp.get("treeId"),
    )


async def merge_pull_request_by_squash(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("MergePullRequestBySquash", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to merge pull request by squash") from exc
    return MergePullRequestBySquashResult(
        pull_request=resp.get("pullRequest"),
    )


async def merge_pull_request_by_three_way(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("MergePullRequestByThreeWay", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to merge pull request by three way") from exc
    return MergePullRequestByThreeWayResult(
        pull_request=resp.get("pullRequest"),
    )


async def override_pull_request_approval_rules(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    kwargs["overrideStatus"] = override_status
    try:
        await client.call("OverridePullRequestApprovalRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to override pull request approval rules") from exc
    return None


async def post_comment_for_compared_commit(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("PostCommentForComparedCommit", **kwargs)
    except Exception as exc:
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


async def post_comment_for_pull_request(
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
    client = async_client("codecommit", region_name)
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
        resp = await client.call("PostCommentForPullRequest", **kwargs)
    except Exception as exc:
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


async def post_comment_reply(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["inReplyTo"] = in_reply_to
    kwargs["content"] = content
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("PostCommentReply", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to post comment reply") from exc
    return PostCommentReplyResult(
        comment=resp.get("comment"),
    )


async def put_comment_reaction(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    kwargs["reactionValue"] = reaction_value
    try:
        await client.call("PutCommentReaction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put comment reaction") from exc
    return None


async def put_repository_triggers(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["triggers"] = triggers
    try:
        resp = await client.call("PutRepositoryTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put repository triggers") from exc
    return PutRepositoryTriggersResult(
        configuration_id=resp.get("configurationId"),
    )


async def run_repository_triggers(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["triggers"] = triggers
    try:
        resp = await client.call("TestRepositoryTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run repository triggers") from exc
    return RunRepositoryTriggersResult(
        successful_executions=resp.get("successfulExecutions"),
        failed_executions=resp.get("failedExecutions"),
    )


async def tag_resource(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_approval_rule_template_content(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["newRuleContent"] = new_rule_content
    if existing_rule_content_sha256 is not None:
        kwargs["existingRuleContentSha256"] = existing_rule_content_sha256
    try:
        resp = await client.call("UpdateApprovalRuleTemplateContent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template content") from exc
    return UpdateApprovalRuleTemplateContentResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


async def update_approval_rule_template_description(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["approvalRuleTemplateName"] = approval_rule_template_name
    kwargs["approvalRuleTemplateDescription"] = approval_rule_template_description
    try:
        resp = await client.call("UpdateApprovalRuleTemplateDescription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template description") from exc
    return UpdateApprovalRuleTemplateDescriptionResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


async def update_approval_rule_template_name(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["oldApprovalRuleTemplateName"] = old_approval_rule_template_name
    kwargs["newApprovalRuleTemplateName"] = new_approval_rule_template_name
    try:
        resp = await client.call("UpdateApprovalRuleTemplateName", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update approval rule template name") from exc
    return UpdateApprovalRuleTemplateNameResult(
        approval_rule_template=resp.get("approvalRuleTemplate"),
    )


async def update_comment(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commentId"] = comment_id
    kwargs["content"] = content
    try:
        resp = await client.call("UpdateComment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update comment") from exc
    return UpdateCommentResult(
        comment=resp.get("comment"),
    )


async def update_default_branch(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["defaultBranchName"] = default_branch_name
    try:
        await client.call("UpdateDefaultBranch", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update default branch") from exc
    return None


async def update_pull_request_approval_rule_content(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["approvalRuleName"] = approval_rule_name
    kwargs["newRuleContent"] = new_rule_content
    if existing_rule_content_sha256 is not None:
        kwargs["existingRuleContentSha256"] = existing_rule_content_sha256
    try:
        resp = await client.call("UpdatePullRequestApprovalRuleContent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pull request approval rule content") from exc
    return UpdatePullRequestApprovalRuleContentResult(
        approval_rule=resp.get("approvalRule"),
    )


async def update_pull_request_approval_state(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["revisionId"] = revision_id
    kwargs["approvalState"] = approval_state
    try:
        await client.call("UpdatePullRequestApprovalState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pull request approval state") from exc
    return None


async def update_pull_request_description(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["description"] = description
    try:
        resp = await client.call("UpdatePullRequestDescription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pull request description") from exc
    return UpdatePullRequestDescriptionResult(
        pull_request=resp.get("pullRequest"),
    )


async def update_pull_request_status(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["pullRequestStatus"] = pull_request_status
    try:
        resp = await client.call("UpdatePullRequestStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pull request status") from exc
    return UpdatePullRequestStatusResult(
        pull_request=resp.get("pullRequest"),
    )


async def update_pull_request_title(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pullRequestId"] = pull_request_id
    kwargs["title"] = title
    try:
        resp = await client.call("UpdatePullRequestTitle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pull request title") from exc
    return UpdatePullRequestTitleResult(
        pull_request=resp.get("pullRequest"),
    )


async def update_repository_encryption_key(
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
    client = async_client("codecommit", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["repositoryName"] = repository_name
    kwargs["kmsKeyId"] = kms_key_id
    try:
        resp = await client.call("UpdateRepositoryEncryptionKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update repository encryption key") from exc
    return UpdateRepositoryEncryptionKeyResult(
        repository_id=resp.get("repositoryId"),
        kms_key_id=resp.get("kmsKeyId"),
        original_kms_key_id=resp.get("originalKmsKeyId"),
    )
