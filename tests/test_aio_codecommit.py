"""Tests for aws_util.aio.codecommit module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codecommit import (
    BlobResult,
    BranchResult,
    CommitResult,
    DiffResult,
    FileResult,
    PullRequestResult,
    RepositoryResult,
    create_branch,
    create_commit,
    create_pull_request,
    create_repository,
    delete_branch,
    delete_file,
    delete_repository,
    get_blob,
    get_branch,
    get_commit,
    get_differences,
    get_file,
    get_pull_request,
    get_repository,
    list_branches,
    list_pull_requests,
    list_repositories,
    merge_branches_by_fast_forward,
    merge_branches_by_squash,
    merge_pull_request_by_fast_forward,
    put_file,
    update_repository_description,
    update_repository_name,
    associate_approval_rule_template_with_repository,
    batch_associate_approval_rule_template_with_repositories,
    batch_describe_merge_conflicts,
    batch_disassociate_approval_rule_template_from_repositories,
    batch_get_commits,
    batch_get_repositories,
    create_approval_rule_template,
    create_pull_request_approval_rule,
    create_unreferenced_merge_commit,
    delete_approval_rule_template,
    delete_comment_content,
    delete_pull_request_approval_rule,
    describe_merge_conflicts,
    describe_pull_request_events,
    disassociate_approval_rule_template_from_repository,
    evaluate_pull_request_approval_rules,
    get_approval_rule_template,
    get_comment,
    get_comment_reactions,
    get_comments_for_compared_commit,
    get_comments_for_pull_request,
    get_folder,
    get_merge_commit,
    get_merge_conflicts,
    get_merge_options,
    get_pull_request_approval_states,
    get_pull_request_override_state,
    get_repository_triggers,
    list_approval_rule_templates,
    list_associated_approval_rule_templates_for_repository,
    list_file_commit_history,
    list_repositories_for_approval_rule_template,
    list_tags_for_resource,
    merge_branches_by_three_way,
    merge_pull_request_by_squash,
    merge_pull_request_by_three_way,
    override_pull_request_approval_rules,
    post_comment_for_compared_commit,
    post_comment_for_pull_request,
    post_comment_reply,
    put_comment_reaction,
    put_repository_triggers,
    run_repository_triggers,
    tag_resource,
    untag_resource,
    update_approval_rule_template_content,
    update_approval_rule_template_description,
    update_approval_rule_template_name,
    update_comment,
    update_default_branch,
    update_pull_request_approval_rule_content,
    update_pull_request_approval_state,
    update_pull_request_description,
    update_pull_request_status,
    update_pull_request_title,
    update_repository_encryption_key,
)

REPO_NAME = "test-repo"
REPO_ID = "repo-id-123"
REPO_ARN = "arn:aws:codecommit:us-east-1:123456789012:test-repo"
BRANCH_NAME = "main"
COMMIT_ID = "abc123def456"
PR_ID = "42"
BLOB_ID = "blob-abc123"

_RAW_REPO = {
    "repositoryId": REPO_ID,
    "repositoryName": REPO_NAME,
    "Arn": REPO_ARN,
    "repositoryDescription": "A test repository",
    "cloneUrlHttp": "https://...",
    "cloneUrlSsh": "ssh://...",
    "defaultBranch": "main",
    "lastModifiedDate": "2024-01-01T00:00:00Z",
    "creationDate": "2024-01-01T00:00:00Z",
}

_RAW_BRANCH = {
    "branchName": BRANCH_NAME,
    "commitId": COMMIT_ID,
}

_RAW_COMMIT = {
    "commitId": COMMIT_ID,
    "treeId": "tree-abc123",
    "author": {"name": "Test", "email": "test@example.com"},
    "committer": {"name": "Test", "email": "test@example.com"},
    "message": "Initial commit",
    "parents": [],
}

_RAW_PR = {
    "pullRequestId": PR_ID,
    "title": "Test PR",
    "description": "A test pull request",
    "pullRequestStatus": "OPEN",
    "creationDate": "2024-01-01T00:00:00Z",
    "lastActivityDate": "2024-01-02T00:00:00Z",
    "pullRequestTargets": [
        {
            "repositoryName": REPO_NAME,
            "sourceReference": "refs/heads/feature",
            "destinationReference": "refs/heads/main",
        }
    ],
}

_RAW_DIFF = {
    "beforeBlob": {"blobId": "blob1", "path": "a.txt"},
    "afterBlob": {"blobId": "blob2", "path": "a.txt"},
    "changeType": "M",
}

_AIO_MOD = "aws_util.aio.codecommit"


# ---------------------------------------------------------------------------
# create_repository
# ---------------------------------------------------------------------------


async def test_create_repository_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositoryMetadata": _RAW_REPO,
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_repository(
        REPO_NAME, description="desc", tags={"k": "v"},
    )
    assert isinstance(result, RepositoryResult)
    assert result.repository_name == REPO_NAME


async def test_create_repository_no_optional(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositoryMetadata": _RAW_REPO,
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_repository(REPO_NAME)
    assert result.repository_name == REPO_NAME


async def test_create_repository_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_repository(REPO_NAME)


async def test_create_repository_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_repository failed"):
        await create_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# get_repository
# ---------------------------------------------------------------------------


async def test_get_repository_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositoryMetadata": _RAW_REPO,
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_repository(REPO_NAME)
    assert result.repository_name == REPO_NAME


async def test_get_repository_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository(REPO_NAME)


async def test_get_repository_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_repository failed"):
        await get_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# list_repositories
# ---------------------------------------------------------------------------


async def test_list_repositories_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "repositories": [
            {"repositoryName": "r1", "repositoryId": "id1"},
        ],
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_repositories()
    assert len(result) == 1
    assert result[0]["repositoryName"] == "r1"


async def test_list_repositories_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "repositories": [{"repositoryName": "r1"}],
                "nextToken": "tok",
            }
        return {"repositories": [{"repositoryName": "r2"}]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_repositories(
        sort_by="lastModifiedDate", order="descending",
    )
    assert len(result) == 2


async def test_list_repositories_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_repositories()


async def test_list_repositories_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_repositories failed"):
        await list_repositories()


# ---------------------------------------------------------------------------
# delete_repository
# ---------------------------------------------------------------------------


async def test_delete_repository_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"repositoryId": REPO_ID}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await delete_repository(REPO_NAME)
    assert result == REPO_ID


async def test_delete_repository_no_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await delete_repository(REPO_NAME)
    assert result is None


async def test_delete_repository_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository(REPO_NAME)


async def test_delete_repository_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_repository failed"):
        await delete_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# update_repository_name
# ---------------------------------------------------------------------------


async def test_update_repository_name_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    await update_repository_name("old", "new")
    mock_client.call.assert_awaited_once()


async def test_update_repository_name_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository_name("old", "new")


async def test_update_repository_name_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="update_repository_name failed"
    ):
        await update_repository_name("old", "new")


# ---------------------------------------------------------------------------
# update_repository_description
# ---------------------------------------------------------------------------


async def test_update_repository_description_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    await update_repository_description(REPO_NAME, "New desc")
    mock_client.call.assert_awaited_once()


async def test_update_repository_description_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository_description(REPO_NAME, "d")


async def test_update_repository_description_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="update_repository_description failed",
    ):
        await update_repository_description(REPO_NAME, "d")


# ---------------------------------------------------------------------------
# create_branch
# ---------------------------------------------------------------------------


async def test_create_branch_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    await create_branch(REPO_NAME, "feature", COMMIT_ID)
    mock_client.call.assert_awaited_once()


async def test_create_branch_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_branch(REPO_NAME, "feature", COMMIT_ID)


async def test_create_branch_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_branch failed"):
        await create_branch(REPO_NAME, "feature", COMMIT_ID)


# ---------------------------------------------------------------------------
# get_branch
# ---------------------------------------------------------------------------


async def test_get_branch_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"branch": _RAW_BRANCH}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_branch(REPO_NAME, BRANCH_NAME)
    assert isinstance(result, BranchResult)
    assert result.branch_name == BRANCH_NAME


async def test_get_branch_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_branch(REPO_NAME, BRANCH_NAME)


async def test_get_branch_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_branch failed"):
        await get_branch(REPO_NAME, BRANCH_NAME)


# ---------------------------------------------------------------------------
# list_branches
# ---------------------------------------------------------------------------


async def test_list_branches_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "branches": ["main", "dev"],
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_branches(REPO_NAME)
    assert result == ["main", "dev"]


async def test_list_branches_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"branches": ["main"], "nextToken": "tok"}
        return {"branches": ["dev"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_branches(REPO_NAME)
    assert result == ["main", "dev"]


async def test_list_branches_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_branches(REPO_NAME)


async def test_list_branches_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_branches failed"):
        await list_branches(REPO_NAME)


# ---------------------------------------------------------------------------
# delete_branch
# ---------------------------------------------------------------------------


async def test_delete_branch_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "deletedBranch": _RAW_BRANCH,
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await delete_branch(REPO_NAME, BRANCH_NAME)
    assert isinstance(result, BranchResult)
    assert result.branch_name == BRANCH_NAME


async def test_delete_branch_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_branch(REPO_NAME, BRANCH_NAME)


async def test_delete_branch_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_branch failed"):
        await delete_branch(REPO_NAME, BRANCH_NAME)


# ---------------------------------------------------------------------------
# merge_branches_by_fast_forward
# ---------------------------------------------------------------------------


async def test_merge_branches_by_fast_forward_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commitId": "merged"}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_branches_by_fast_forward(
        REPO_NAME, "src", "dst", target_branch="main",
    )
    assert result == "merged"


async def test_merge_branches_by_fast_forward_no_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commitId": "merged"}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_branches_by_fast_forward(
        REPO_NAME, "src", "dst",
    )
    assert result == "merged"


async def test_merge_branches_by_fast_forward_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_branches_by_fast_forward(
            REPO_NAME, "src", "dst",
        )


async def test_merge_branches_by_fast_forward_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="merge_branches_by_fast_forward failed",
    ):
        await merge_branches_by_fast_forward(
            REPO_NAME, "src", "dst",
        )


# ---------------------------------------------------------------------------
# merge_branches_by_squash
# ---------------------------------------------------------------------------


async def test_merge_branches_by_squash_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commitId": "squashed"}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_branches_by_squash(
        REPO_NAME, "src", "dst",
        target_branch="main",
        author_name="A",
        email="a@a.com",
        commit_message="msg",
    )
    assert result == "squashed"


async def test_merge_branches_by_squash_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commitId": "squashed"}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_branches_by_squash(
        REPO_NAME, "src", "dst",
    )
    assert result == "squashed"


async def test_merge_branches_by_squash_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_branches_by_squash(REPO_NAME, "s", "d")


async def test_merge_branches_by_squash_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="merge_branches_by_squash failed"
    ):
        await merge_branches_by_squash(REPO_NAME, "s", "d")


# ---------------------------------------------------------------------------
# create_commit
# ---------------------------------------------------------------------------


async def test_create_commit_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "commitId": COMMIT_ID,
        "treeId": "tree1",
        "parents": ["p1"],
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_commit(
        REPO_NAME, "main",
        parent_commit_id="p1",
        author_name="A",
        email="a@a.com",
        commit_message="msg",
        put_files=[{"filePath": "a.txt", "fileContent": b"hi"}],
        delete_files=[{"filePath": "b.txt"}],
    )
    assert isinstance(result, CommitResult)
    assert result.commit_id == COMMIT_ID


async def test_create_commit_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commitId": COMMIT_ID}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_commit(REPO_NAME, "main")
    assert result.commit_id == COMMIT_ID


async def test_create_commit_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_commit(REPO_NAME, "main")


async def test_create_commit_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_commit failed"):
        await create_commit(REPO_NAME, "main")


# ---------------------------------------------------------------------------
# get_commit
# ---------------------------------------------------------------------------


async def test_get_commit_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"commit": _RAW_COMMIT}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_commit(REPO_NAME, COMMIT_ID)
    assert result.commit_id == COMMIT_ID
    assert result.message == "Initial commit"


async def test_get_commit_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_commit(REPO_NAME, COMMIT_ID)


async def test_get_commit_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_commit failed"):
        await get_commit(REPO_NAME, COMMIT_ID)


# ---------------------------------------------------------------------------
# get_file
# ---------------------------------------------------------------------------


async def test_get_file_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "filePath": "a.txt",
        "fileSize": 5,
        "fileMode": "NORMAL",
        "blobId": BLOB_ID,
        "commitId": COMMIT_ID,
        "fileContent": b"hello",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_file(
        REPO_NAME, "a.txt", commit_specifier="main",
    )
    assert isinstance(result, FileResult)
    assert result.file_content == b"hello"


async def test_get_file_no_specifier(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "filePath": "a.txt",
        "fileContent": b"hello",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_file(REPO_NAME, "a.txt")
    assert result.file_path == "a.txt"


async def test_get_file_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_file(REPO_NAME, "a.txt")


async def test_get_file_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_file failed"):
        await get_file(REPO_NAME, "a.txt")


# ---------------------------------------------------------------------------
# put_file
# ---------------------------------------------------------------------------


async def test_put_file_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "commitId": COMMIT_ID,
        "blobId": BLOB_ID,
        "treeId": "tree1",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await put_file(
        REPO_NAME, "a.txt", b"hello", "main",
        file_mode="EXECUTABLE",
        parent_commit_id="p1",
        commit_message="add file",
        name="Author",
        email="a@a.com",
    )
    assert result["commitId"] == COMMIT_ID


async def test_put_file_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "commitId": COMMIT_ID,
        "blobId": BLOB_ID,
        "treeId": "tree1",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await put_file(REPO_NAME, "a.txt", b"hello", "main")
    assert result["commitId"] == COMMIT_ID


async def test_put_file_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_file(REPO_NAME, "a.txt", b"hello", "main")


async def test_put_file_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="put_file failed"):
        await put_file(REPO_NAME, "a.txt", b"hello", "main")


# ---------------------------------------------------------------------------
# delete_file
# ---------------------------------------------------------------------------


async def test_delete_file_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "commitId": COMMIT_ID,
        "blobId": BLOB_ID,
        "treeId": "tree1",
        "filePath": "a.txt",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await delete_file(
        REPO_NAME, "a.txt", "main", "parent1",
        commit_message="del",
        name="A",
        email="a@a.com",
        keep_empty_folders=True,
    )
    assert result["commitId"] == COMMIT_ID


async def test_delete_file_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "commitId": COMMIT_ID,
        "blobId": BLOB_ID,
        "treeId": "tree1",
        "filePath": "a.txt",
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await delete_file(
        REPO_NAME, "a.txt", "main", "parent1",
    )
    assert result["filePath"] == "a.txt"


async def test_delete_file_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_file(REPO_NAME, "a.txt", "main", "p1")


async def test_delete_file_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_file failed"):
        await delete_file(REPO_NAME, "a.txt", "main", "p1")


# ---------------------------------------------------------------------------
# get_differences
# ---------------------------------------------------------------------------


async def test_get_differences_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "differences": [_RAW_DIFF],
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_differences(
        REPO_NAME, COMMIT_ID,
        before_commit_specifier="before",
        before_path="old/",
        after_path="new/",
    )
    assert len(result) == 1
    assert isinstance(result[0], DiffResult)


async def test_get_differences_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"differences": [_RAW_DIFF]}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_differences(REPO_NAME, COMMIT_ID)
    assert len(result) == 1


async def test_get_differences_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "differences": [_RAW_DIFF],
                "NextToken": "tok",
            }
        return {"differences": [_RAW_DIFF]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_differences(REPO_NAME, COMMIT_ID)
    assert len(result) == 2


async def test_get_differences_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_differences(REPO_NAME, COMMIT_ID)


async def test_get_differences_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_differences failed"):
        await get_differences(REPO_NAME, COMMIT_ID)


# ---------------------------------------------------------------------------
# create_pull_request
# ---------------------------------------------------------------------------


async def test_create_pull_request_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pullRequest": _RAW_PR}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_pull_request(
        "Test PR",
        [{"repositoryName": REPO_NAME, "sourceReference": "feature"}],
        description="A test",
    )
    assert isinstance(result, PullRequestResult)
    assert result.title == "Test PR"


async def test_create_pull_request_no_description(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pullRequest": _RAW_PR}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await create_pull_request("T", [])
    assert result.title == "Test PR"


async def test_create_pull_request_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_pull_request("T", [])


async def test_create_pull_request_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="create_pull_request failed"
    ):
        await create_pull_request("T", [])


# ---------------------------------------------------------------------------
# get_pull_request
# ---------------------------------------------------------------------------


async def test_get_pull_request_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pullRequest": _RAW_PR}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_pull_request(PR_ID)
    assert result.pull_request_id == PR_ID


async def test_get_pull_request_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_pull_request(PR_ID)


async def test_get_pull_request_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_pull_request failed"
    ):
        await get_pull_request(PR_ID)


# ---------------------------------------------------------------------------
# list_pull_requests
# ---------------------------------------------------------------------------


async def test_list_pull_requests_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pullRequestIds": ["1", "2"],
    }
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_pull_requests(REPO_NAME)
    assert result == ["1", "2"]


async def test_list_pull_requests_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "pullRequestIds": ["1"],
                "nextToken": "tok",
            }
        return {"pullRequestIds": ["2"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await list_pull_requests(
        REPO_NAME, pull_request_status="CLOSED",
    )
    assert result == ["1", "2"]


async def test_list_pull_requests_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_pull_requests(REPO_NAME)


async def test_list_pull_requests_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_pull_requests failed"
    ):
        await list_pull_requests(REPO_NAME)


# ---------------------------------------------------------------------------
# merge_pull_request_by_fast_forward
# ---------------------------------------------------------------------------


async def test_merge_pull_request_by_ff_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pullRequest": _RAW_PR}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_pull_request_by_fast_forward(
        PR_ID, REPO_NAME, source_commit_id=COMMIT_ID,
    )
    assert isinstance(result, PullRequestResult)


async def test_merge_pull_request_by_ff_no_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pullRequest": _RAW_PR}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await merge_pull_request_by_fast_forward(
        PR_ID, REPO_NAME,
    )
    assert result.pull_request_id == PR_ID


async def test_merge_pull_request_by_ff_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_pull_request_by_fast_forward(
            PR_ID, REPO_NAME,
        )


async def test_merge_pull_request_by_ff_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError,
        match="merge_pull_request_by_fast_forward failed",
    ):
        await merge_pull_request_by_fast_forward(
            PR_ID, REPO_NAME,
        )


# ---------------------------------------------------------------------------
# get_blob
# ---------------------------------------------------------------------------


async def test_get_blob_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"content": b"blob-data"}
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )

    result = await get_blob(REPO_NAME, BLOB_ID)
    assert isinstance(result, BlobResult)
    assert result.blob_id == BLOB_ID
    assert result.content == b"blob-data"


async def test_get_blob_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_blob(REPO_NAME, BLOB_ID)


async def test_get_blob_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        f"{_AIO_MOD}.async_client", lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_blob failed"):
        await get_blob(REPO_NAME, BLOB_ID)


async def test_associate_approval_rule_template_with_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_approval_rule_template_with_repository("test-approval_rule_template_name", "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_associate_approval_rule_template_with_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_approval_rule_template_with_repository("test-approval_rule_template_name", "test-repository_name", )


async def test_batch_associate_approval_rule_template_with_repositories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_approval_rule_template_with_repositories("test-approval_rule_template_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_associate_approval_rule_template_with_repositories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_approval_rule_template_with_repositories("test-approval_rule_template_name", [], )


async def test_batch_describe_merge_conflicts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", )
    mock_client.call.assert_called_once()


async def test_batch_describe_merge_conflicts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", )


async def test_batch_disassociate_approval_rule_template_from_repositories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_approval_rule_template_from_repositories("test-approval_rule_template_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_approval_rule_template_from_repositories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_approval_rule_template_from_repositories("test-approval_rule_template_name", [], )


async def test_batch_get_commits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_commits([], "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_batch_get_commits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_commits([], "test-repository_name", )


async def test_batch_get_repositories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_repositories([], )
    mock_client.call.assert_called_once()


async def test_batch_get_repositories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_repositories([], )


async def test_create_approval_rule_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", )
    mock_client.call.assert_called_once()


async def test_create_approval_rule_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", )


async def test_create_pull_request_approval_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", "test-approval_rule_content", )
    mock_client.call.assert_called_once()


async def test_create_pull_request_approval_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", "test-approval_rule_content", )


async def test_create_unreferenced_merge_commit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", )
    mock_client.call.assert_called_once()


async def test_create_unreferenced_merge_commit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", )


async def test_delete_approval_rule_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_approval_rule_template("test-approval_rule_template_name", )
    mock_client.call.assert_called_once()


async def test_delete_approval_rule_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_approval_rule_template("test-approval_rule_template_name", )


async def test_delete_comment_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_comment_content("test-comment_id", )
    mock_client.call.assert_called_once()


async def test_delete_comment_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_comment_content("test-comment_id", )


async def test_delete_pull_request_approval_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", )
    mock_client.call.assert_called_once()


async def test_delete_pull_request_approval_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", )


async def test_describe_merge_conflicts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", )
    mock_client.call.assert_called_once()


async def test_describe_merge_conflicts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", )


async def test_describe_pull_request_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pull_request_events("test-pull_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_pull_request_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pull_request_events("test-pull_request_id", )


async def test_disassociate_approval_rule_template_from_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_approval_rule_template_from_repository("test-approval_rule_template_name", "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_disassociate_approval_rule_template_from_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_approval_rule_template_from_repository("test-approval_rule_template_name", "test-repository_name", )


async def test_evaluate_pull_request_approval_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await evaluate_pull_request_approval_rules("test-pull_request_id", "test-revision_id", )
    mock_client.call.assert_called_once()


async def test_evaluate_pull_request_approval_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await evaluate_pull_request_approval_rules("test-pull_request_id", "test-revision_id", )


async def test_get_approval_rule_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_approval_rule_template("test-approval_rule_template_name", )
    mock_client.call.assert_called_once()


async def test_get_approval_rule_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_approval_rule_template("test-approval_rule_template_name", )


async def test_get_comment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_comment("test-comment_id", )
    mock_client.call.assert_called_once()


async def test_get_comment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_comment("test-comment_id", )


async def test_get_comment_reactions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_comment_reactions("test-comment_id", )
    mock_client.call.assert_called_once()


async def test_get_comment_reactions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_comment_reactions("test-comment_id", )


async def test_get_comments_for_compared_commit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", )
    mock_client.call.assert_called_once()


async def test_get_comments_for_compared_commit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", )


async def test_get_comments_for_pull_request(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_comments_for_pull_request("test-pull_request_id", )
    mock_client.call.assert_called_once()


async def test_get_comments_for_pull_request_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_comments_for_pull_request("test-pull_request_id", )


async def test_get_folder(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_folder("test-repository_name", "test-folder_path", )
    mock_client.call.assert_called_once()


async def test_get_folder_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_folder("test-repository_name", "test-folder_path", )


async def test_get_merge_commit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )
    mock_client.call.assert_called_once()


async def test_get_merge_commit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )


async def test_get_merge_conflicts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", )
    mock_client.call.assert_called_once()


async def test_get_merge_conflicts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", )


async def test_get_merge_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )
    mock_client.call.assert_called_once()


async def test_get_merge_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )


async def test_get_pull_request_approval_states(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_pull_request_approval_states("test-pull_request_id", "test-revision_id", )
    mock_client.call.assert_called_once()


async def test_get_pull_request_approval_states_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_pull_request_approval_states("test-pull_request_id", "test-revision_id", )


async def test_get_pull_request_override_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_pull_request_override_state("test-pull_request_id", "test-revision_id", )
    mock_client.call.assert_called_once()


async def test_get_pull_request_override_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_pull_request_override_state("test-pull_request_id", "test-revision_id", )


async def test_get_repository_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_repository_triggers("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_get_repository_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository_triggers("test-repository_name", )


async def test_list_approval_rule_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_approval_rule_templates()
    mock_client.call.assert_called_once()


async def test_list_approval_rule_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_approval_rule_templates()


async def test_list_associated_approval_rule_templates_for_repository(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associated_approval_rule_templates_for_repository("test-repository_name", )
    mock_client.call.assert_called_once()


async def test_list_associated_approval_rule_templates_for_repository_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associated_approval_rule_templates_for_repository("test-repository_name", )


async def test_list_file_commit_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_file_commit_history("test-repository_name", "test-file_path", )
    mock_client.call.assert_called_once()


async def test_list_file_commit_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_file_commit_history("test-repository_name", "test-file_path", )


async def test_list_repositories_for_approval_rule_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_repositories_for_approval_rule_template("test-approval_rule_template_name", )
    mock_client.call.assert_called_once()


async def test_list_repositories_for_approval_rule_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_repositories_for_approval_rule_template("test-approval_rule_template_name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_merge_branches_by_three_way(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )
    mock_client.call.assert_called_once()


async def test_merge_branches_by_three_way_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", )


async def test_merge_pull_request_by_squash(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_merge_pull_request_by_squash_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", )


async def test_merge_pull_request_by_three_way(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_merge_pull_request_by_three_way_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", )


async def test_override_pull_request_approval_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await override_pull_request_approval_rules("test-pull_request_id", "test-revision_id", "test-override_status", )
    mock_client.call.assert_called_once()


async def test_override_pull_request_approval_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await override_pull_request_approval_rules("test-pull_request_id", "test-revision_id", "test-override_status", )


async def test_post_comment_for_compared_commit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", )
    mock_client.call.assert_called_once()


async def test_post_comment_for_compared_commit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", )


async def test_post_comment_for_pull_request(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", )
    mock_client.call.assert_called_once()


async def test_post_comment_for_pull_request_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", )


async def test_post_comment_reply(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await post_comment_reply("test-in_reply_to", "test-content", )
    mock_client.call.assert_called_once()


async def test_post_comment_reply_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await post_comment_reply("test-in_reply_to", "test-content", )


async def test_put_comment_reaction(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_comment_reaction("test-comment_id", "test-reaction_value", )
    mock_client.call.assert_called_once()


async def test_put_comment_reaction_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_comment_reaction("test-comment_id", "test-reaction_value", )


async def test_put_repository_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_repository_triggers("test-repository_name", [], )
    mock_client.call.assert_called_once()


async def test_put_repository_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_repository_triggers("test-repository_name", [], )


async def test_run_repository_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_repository_triggers("test-repository_name", [], )
    mock_client.call.assert_called_once()


async def test_run_repository_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_repository_triggers("test-repository_name", [], )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_approval_rule_template_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", )
    mock_client.call.assert_called_once()


async def test_update_approval_rule_template_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", )


async def test_update_approval_rule_template_description(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_approval_rule_template_description("test-approval_rule_template_name", "test-approval_rule_template_description", )
    mock_client.call.assert_called_once()


async def test_update_approval_rule_template_description_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_approval_rule_template_description("test-approval_rule_template_name", "test-approval_rule_template_description", )


async def test_update_approval_rule_template_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_approval_rule_template_name("test-old_approval_rule_template_name", "test-new_approval_rule_template_name", )
    mock_client.call.assert_called_once()


async def test_update_approval_rule_template_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_approval_rule_template_name("test-old_approval_rule_template_name", "test-new_approval_rule_template_name", )


async def test_update_comment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_comment("test-comment_id", "test-content", )
    mock_client.call.assert_called_once()


async def test_update_comment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_comment("test-comment_id", "test-content", )


async def test_update_default_branch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_default_branch("test-repository_name", "test-default_branch_name", )
    mock_client.call.assert_called_once()


async def test_update_default_branch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_default_branch("test-repository_name", "test-default_branch_name", )


async def test_update_pull_request_approval_rule_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", )
    mock_client.call.assert_called_once()


async def test_update_pull_request_approval_rule_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", )


async def test_update_pull_request_approval_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_request_approval_state("test-pull_request_id", "test-revision_id", "test-approval_state", )
    mock_client.call.assert_called_once()


async def test_update_pull_request_approval_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_request_approval_state("test-pull_request_id", "test-revision_id", "test-approval_state", )


async def test_update_pull_request_description(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_request_description("test-pull_request_id", "test-description", )
    mock_client.call.assert_called_once()


async def test_update_pull_request_description_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_request_description("test-pull_request_id", "test-description", )


async def test_update_pull_request_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_request_status("test-pull_request_id", "test-pull_request_status", )
    mock_client.call.assert_called_once()


async def test_update_pull_request_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_request_status("test-pull_request_id", "test-pull_request_status", )


async def test_update_pull_request_title(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pull_request_title("test-pull_request_id", "test-title", )
    mock_client.call.assert_called_once()


async def test_update_pull_request_title_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pull_request_title("test-pull_request_id", "test-title", )


async def test_update_repository_encryption_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_repository_encryption_key("test-repository_name", "test-kms_key_id", )
    mock_client.call.assert_called_once()


async def test_update_repository_encryption_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codecommit.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository_encryption_key("test-repository_name", "test-kms_key_id", )


@pytest.mark.asyncio
async def test_merge_branches_by_fast_forward_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import merge_branches_by_fast_forward
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await merge_branches_by_fast_forward("test-repository_name", "test-source_commit", "test-destination_commit", target_branch="test-target_branch", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_merge_branches_by_squash_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import merge_branches_by_squash
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await merge_branches_by_squash("test-repository_name", "test-source_commit", "test-destination_commit", target_branch="test-target_branch", author_name="test-author_name", email="test-email", commit_message="test-commit_message", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_commit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import create_commit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await create_commit("test-repository_name", "test-branch_name", parent_commit_id="test-parent_commit_id", author_name="test-author_name", email="test-email", commit_message="test-commit_message", put_files="test-put_files", delete_files=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_file_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_file
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_file("test-repository_name", "test-file_path", commit_specifier="test-commit_specifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_file_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import put_file
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await put_file("test-repository_name", "test-file_path", "test-file_content", "test-branch_name", file_mode="test-file_mode", parent_commit_id="test-parent_commit_id", commit_message="test-commit_message", name="test-name", email="test-email", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_file_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import delete_file
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await delete_file("test-repository_name", "test-file_path", "test-branch_name", "test-parent_commit_id", commit_message="test-commit_message", name="test-name", email="test-email", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_differences_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_differences
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_differences("test-repository_name", "test-after_commit_specifier", before_commit_specifier="test-before_commit_specifier", before_path="test-before_path", after_path="test-after_path", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_describe_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import batch_describe_merge_conflicts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", max_merge_hunks=1, max_conflict_files=1, file_paths="test-file_paths", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_approval_rule_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import create_approval_rule_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", approval_rule_template_description="test-approval_rule_template_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_unreferenced_merge_commit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import create_unreferenced_merge_commit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", author_name="test-author_name", email="test-email", commit_message="test-commit_message", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import describe_merge_conflicts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", max_merge_hunks=1, conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pull_request_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import describe_pull_request_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await describe_pull_request_events("test-pull_request_id", pull_request_event_type="test-pull_request_event_type", actor_arn="test-actor_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_comment_reactions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_comment_reactions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_comment_reactions("test-comment_id", reaction_user_arn="test-reaction_user_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_comments_for_compared_commit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_comments_for_compared_commit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", before_commit_id="test-before_commit_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_comments_for_pull_request_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_comments_for_pull_request
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_comments_for_pull_request("test-pull_request_id", repository_name="test-repository_name", before_commit_id="test-before_commit_id", after_commit_id="test-after_commit_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_folder_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_folder
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_folder("test-repository_name", "test-folder_path", commit_specifier="test-commit_specifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_merge_commit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_merge_commit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_merge_conflicts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", conflict_detail_level="test-conflict_detail_level", max_conflict_files=1, conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_merge_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import get_merge_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_approval_rule_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import list_approval_rule_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await list_approval_rule_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associated_approval_rule_templates_for_repository_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import list_associated_approval_rule_templates_for_repository
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await list_associated_approval_rule_templates_for_repository("test-repository_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_file_commit_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import list_file_commit_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await list_file_commit_history("test-repository_name", "test-file_path", commit_specifier="test-commit_specifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_repositories_for_approval_rule_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import list_repositories_for_approval_rule_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await list_repositories_for_approval_rule_template("test-approval_rule_template_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_merge_branches_by_three_way_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import merge_branches_by_three_way
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", target_branch="test-target_branch", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", author_name="test-author_name", email="test-email", commit_message="test-commit_message", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_merge_pull_request_by_squash_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import merge_pull_request_by_squash
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", source_commit_id="test-source_commit_id", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", commit_message="test-commit_message", author_name="test-author_name", email="test-email", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_merge_pull_request_by_three_way_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import merge_pull_request_by_three_way
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", source_commit_id="test-source_commit_id", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", commit_message="test-commit_message", author_name="test-author_name", email="test-email", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_post_comment_for_compared_commit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import post_comment_for_compared_commit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", before_commit_id="test-before_commit_id", location="test-location", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_post_comment_for_pull_request_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import post_comment_for_pull_request
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", location="test-location", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_post_comment_reply_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import post_comment_reply
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await post_comment_reply("test-in_reply_to", "test-content", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_approval_rule_template_content_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import update_approval_rule_template_content
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", existing_rule_content_sha256="test-existing_rule_content_sha256", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_pull_request_approval_rule_content_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codecommit import update_pull_request_approval_rule_content
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codecommit.async_client", lambda *a, **kw: mock_client)
    await update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", existing_rule_content_sha256="test-existing_rule_content_sha256", region_name="us-east-1")
    mock_client.call.assert_called_once()
