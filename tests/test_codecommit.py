"""Tests for aws_util.codecommit module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.codecommit import (
    BlobResult,
    BranchResult,
    CommitResult,
    DiffResult,
    FileResult,
    PullRequestResult,
    RepositoryResult,
    _parse_branch,
    _parse_commit,
    _parse_diff,
    _parse_pull_request,
    _parse_repository,
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

REGION = "us-east-1"
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
    "cloneUrlHttp": "https://git-codecommit.us-east-1.amazonaws.com/v1/repos/test-repo",
    "cloneUrlSsh": "ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/test-repo",
    "defaultBranch": "main",
    "lastModifiedDate": "2024-01-01T00:00:00Z",
    "creationDate": "2024-01-01T00:00:00Z",
    "accountId": "123456789012",
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
    "additionalData": "extra",
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
    "authorArn": "arn:aws:iam::123456789012:user/test",
}

_RAW_DIFF = {
    "beforeBlob": {"blobId": "blob1", "path": "a.txt", "mode": "100644"},
    "afterBlob": {"blobId": "blob2", "path": "a.txt", "mode": "100644"},
    "changeType": "M",
}


def _make_client_error(code: str, msg: str, op: str) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, op,
    )


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestRepositoryResultModel:
    def test_minimal(self):
        r = RepositoryResult(
            repository_id="id1", repository_name="r1",
        )
        assert r.repository_id == "id1"
        assert r.arn is None
        assert r.description is None
        assert r.clone_url_http is None
        assert r.clone_url_ssh is None
        assert r.default_branch is None
        assert r.last_modified is None
        assert r.creation_date is None
        assert r.extra == {}

    def test_full(self):
        r = RepositoryResult(
            repository_id=REPO_ID,
            repository_name=REPO_NAME,
            arn=REPO_ARN,
            description="desc",
            clone_url_http="https://...",
            clone_url_ssh="ssh://...",
            default_branch="main",
            last_modified="2024-01-01",
            creation_date="2024-01-01",
            extra={"accountId": "123"},
        )
        assert r.description == "desc"
        assert r.default_branch == "main"


class TestBranchResultModel:
    def test_minimal(self):
        b = BranchResult(branch_name="main", commit_id="abc")
        assert b.branch_name == "main"
        assert b.extra == {}

    def test_full(self):
        b = BranchResult(
            branch_name="dev",
            commit_id="abc",
            extra={"x": 1},
        )
        assert b.extra == {"x": 1}


class TestCommitResultModel:
    def test_minimal(self):
        c = CommitResult(commit_id="abc")
        assert c.tree_id is None
        assert c.author is None
        assert c.committer is None
        assert c.message is None
        assert c.parents == []
        assert c.extra == {}

    def test_full(self):
        c = CommitResult(
            commit_id="abc",
            tree_id="tree1",
            author={"name": "A"},
            committer={"name": "B"},
            message="msg",
            parents=["p1"],
            extra={"x": 1},
        )
        assert c.message == "msg"
        assert c.parents == ["p1"]


class TestPullRequestResultModel:
    def test_minimal(self):
        pr = PullRequestResult(
            pull_request_id="1", title="T",
        )
        assert pr.description is None
        assert pr.pull_request_status is None
        assert pr.creation_date is None
        assert pr.last_activity_date is None
        assert pr.pull_request_targets == []
        assert pr.extra == {}

    def test_full(self):
        pr = PullRequestResult(
            pull_request_id="1",
            title="T",
            description="D",
            pull_request_status="OPEN",
            creation_date="2024-01-01",
            last_activity_date="2024-01-02",
            pull_request_targets=[{"repositoryName": "r"}],
            extra={"authorArn": "arn"},
        )
        assert pr.pull_request_status == "OPEN"


class TestFileResultModel:
    def test_minimal(self):
        f = FileResult(file_path="/a.txt")
        assert f.file_size is None
        assert f.file_mode is None
        assert f.blob_id is None
        assert f.commit_id is None
        assert f.file_content is None
        assert f.extra == {}

    def test_full(self):
        f = FileResult(
            file_path="/a.txt",
            file_size=100,
            file_mode="NORMAL",
            blob_id="b1",
            commit_id="c1",
            file_content=b"hello",
            extra={"x": 1},
        )
        assert f.file_content == b"hello"


class TestDiffResultModel:
    def test_minimal(self):
        d = DiffResult()
        assert d.before_blob is None
        assert d.after_blob is None
        assert d.change_type is None
        assert d.extra == {}

    def test_full(self):
        d = DiffResult(
            before_blob={"blobId": "b1"},
            after_blob={"blobId": "b2"},
            change_type="M",
            extra={"x": 1},
        )
        assert d.change_type == "M"


class TestBlobResultModel:
    def test_minimal(self):
        b = BlobResult(blob_id="b1", content=b"hello")
        assert b.blob_id == "b1"
        assert b.content == b"hello"
        assert b.extra == {}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_repository_full(self):
        r = _parse_repository(_RAW_REPO)
        assert r.repository_id == REPO_ID
        assert r.repository_name == REPO_NAME
        assert r.arn == REPO_ARN
        assert r.description == "A test repository"
        assert r.default_branch == "main"
        assert r.last_modified is not None
        assert r.creation_date is not None
        assert "accountId" in r.extra

    def test_parse_repository_minimal(self):
        r = _parse_repository({"repositoryId": "id", "repositoryName": "n"})
        assert r.repository_id == "id"
        assert r.arn is None
        assert r.description is None
        assert r.last_modified is None
        assert r.creation_date is None

    def test_parse_branch(self):
        b = _parse_branch(_RAW_BRANCH)
        assert b.branch_name == BRANCH_NAME
        assert b.commit_id == COMMIT_ID

    def test_parse_branch_extra(self):
        raw = {**_RAW_BRANCH, "extra_field": "val"}
        b = _parse_branch(raw)
        assert "extra_field" in b.extra

    def test_parse_commit(self):
        c = _parse_commit(_RAW_COMMIT)
        assert c.commit_id == COMMIT_ID
        assert c.tree_id == "tree-abc123"
        assert c.message == "Initial commit"
        assert "additionalData" in c.extra

    def test_parse_commit_minimal(self):
        c = _parse_commit({"commitId": "x"})
        assert c.commit_id == "x"
        assert c.tree_id is None
        assert c.parents == []

    def test_parse_pull_request(self):
        pr = _parse_pull_request(_RAW_PR)
        assert pr.pull_request_id == PR_ID
        assert pr.title == "Test PR"
        assert pr.description == "A test pull request"
        assert pr.pull_request_status == "OPEN"
        assert len(pr.pull_request_targets) == 1
        assert "authorArn" in pr.extra

    def test_parse_pull_request_minimal(self):
        pr = _parse_pull_request(
            {"pullRequestId": "1", "title": "T"},
        )
        assert pr.pull_request_id == "1"
        assert pr.description is None
        assert pr.creation_date is None
        assert pr.last_activity_date is None

    def test_parse_diff(self):
        d = _parse_diff(_RAW_DIFF)
        assert d.change_type == "M"
        assert d.before_blob is not None
        assert d.after_blob is not None

    def test_parse_diff_extra(self):
        raw = {**_RAW_DIFF, "extra_key": "val"}
        d = _parse_diff(raw)
        assert "extra_key" in d.extra


# ---------------------------------------------------------------------------
# create_repository
# ---------------------------------------------------------------------------


class TestCreateRepository:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_repository.return_value = {
            "repositoryMetadata": _RAW_REPO,
        }
        mock_gc.return_value = client

        result = create_repository(
            REPO_NAME,
            description="A test repository",
            tags={"env": "test"},
            region_name=REGION,
        )
        assert isinstance(result, RepositoryResult)
        assert result.repository_name == REPO_NAME
        call_kw = client.create_repository.call_args[1]
        assert call_kw["repositoryDescription"] == "A test repository"
        assert call_kw["tags"] == {"env": "test"}

    @patch("aws_util.codecommit.get_client")
    def test_no_optional_args(self, mock_gc):
        client = MagicMock()
        client.create_repository.return_value = {
            "repositoryMetadata": _RAW_REPO,
        }
        mock_gc.return_value = client

        result = create_repository(REPO_NAME)
        assert result.repository_name == REPO_NAME
        call_kw = client.create_repository.call_args[1]
        assert "repositoryDescription" not in call_kw
        assert "tags" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_repository.side_effect = _make_client_error(
            "RepositoryNameExistsException", "exists", "CreateRepository",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="create_repository failed"):
            create_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# get_repository
# ---------------------------------------------------------------------------


class TestGetRepository:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_repository.return_value = {
            "repositoryMetadata": _RAW_REPO,
        }
        mock_gc.return_value = client

        result = get_repository(REPO_NAME, region_name=REGION)
        assert result.repository_name == REPO_NAME

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_repository.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "GetRepository",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="get_repository failed"):
            get_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# list_repositories
# ---------------------------------------------------------------------------


class TestListRepositories:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {
                "repositories": [
                    {"repositoryName": "r1", "repositoryId": "id1"},
                ]
            },
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_repositories(region_name=REGION)
        assert len(result) == 1
        assert result[0]["repositoryName"] == "r1"

    @patch("aws_util.codecommit.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"repositories": [{"repositoryName": "r1", "repositoryId": "id1"}]},
            {"repositories": [{"repositoryName": "r2", "repositoryId": "id2"}]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_repositories(
            sort_by="lastModifiedDate", order="descending",
        )
        assert len(result) == 2

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_paginator.side_effect = _make_client_error(
            "InvalidSortByException", "bad", "ListRepositories",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="list_repositories failed"):
            list_repositories()


# ---------------------------------------------------------------------------
# delete_repository
# ---------------------------------------------------------------------------


class TestDeleteRepository:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.delete_repository.return_value = {
            "repositoryId": REPO_ID,
        }
        mock_gc.return_value = client

        result = delete_repository(REPO_NAME, region_name=REGION)
        assert result == REPO_ID

    @patch("aws_util.codecommit.get_client")
    def test_no_id(self, mock_gc):
        client = MagicMock()
        client.delete_repository.return_value = {}
        mock_gc.return_value = client

        result = delete_repository(REPO_NAME)
        assert result is None

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_repository.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "DeleteRepository",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="delete_repository failed"):
            delete_repository(REPO_NAME)


# ---------------------------------------------------------------------------
# update_repository_name
# ---------------------------------------------------------------------------


class TestUpdateRepositoryName:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.update_repository_name.return_value = {}
        mock_gc.return_value = client

        update_repository_name("old", "new", region_name=REGION)
        client.update_repository_name.assert_called_once_with(
            oldName="old", newName="new",
        )

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.update_repository_name.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "UpdateRepositoryName",
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="update_repository_name failed"
        ):
            update_repository_name("old", "new")


# ---------------------------------------------------------------------------
# update_repository_description
# ---------------------------------------------------------------------------


class TestUpdateRepositoryDescription:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.update_repository_description.return_value = {}
        mock_gc.return_value = client

        update_repository_description(
            REPO_NAME, "New desc", region_name=REGION,
        )
        client.update_repository_description.assert_called_once_with(
            repositoryName=REPO_NAME,
            repositoryDescription="New desc",
        )

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.update_repository_description.side_effect = (
            _make_client_error(
                "RepositoryDoesNotExistException",
                "not found",
                "UpdateRepositoryDescription",
            )
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError,
            match="update_repository_description failed",
        ):
            update_repository_description(REPO_NAME, "desc")


# ---------------------------------------------------------------------------
# create_branch
# ---------------------------------------------------------------------------


class TestCreateBranch:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_branch.return_value = {}
        mock_gc.return_value = client

        create_branch(
            REPO_NAME, "feature", COMMIT_ID, region_name=REGION,
        )
        client.create_branch.assert_called_once_with(
            repositoryName=REPO_NAME,
            branchName="feature",
            commitId=COMMIT_ID,
        )

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_branch.side_effect = _make_client_error(
            "BranchNameExistsException", "exists", "CreateBranch",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="create_branch failed"):
            create_branch(REPO_NAME, "feature", COMMIT_ID)


# ---------------------------------------------------------------------------
# get_branch
# ---------------------------------------------------------------------------


class TestGetBranch:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_branch.return_value = {"branch": _RAW_BRANCH}
        mock_gc.return_value = client

        result = get_branch(
            REPO_NAME, BRANCH_NAME, region_name=REGION,
        )
        assert isinstance(result, BranchResult)
        assert result.branch_name == BRANCH_NAME
        assert result.commit_id == COMMIT_ID

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_branch.side_effect = _make_client_error(
            "BranchDoesNotExistException", "not found", "GetBranch",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="get_branch failed"):
            get_branch(REPO_NAME, BRANCH_NAME)


# ---------------------------------------------------------------------------
# list_branches
# ---------------------------------------------------------------------------


class TestListBranches:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"branches": ["main", "dev"]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_branches(REPO_NAME, region_name=REGION)
        assert result == ["main", "dev"]

    @patch("aws_util.codecommit.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"branches": ["main"]},
            {"branches": ["dev"]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_branches(REPO_NAME)
        assert result == ["main", "dev"]

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_paginator.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "ListBranches",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="list_branches failed"):
            list_branches(REPO_NAME)


# ---------------------------------------------------------------------------
# delete_branch
# ---------------------------------------------------------------------------


class TestDeleteBranch:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.delete_branch.return_value = {
            "deletedBranch": _RAW_BRANCH,
        }
        mock_gc.return_value = client

        result = delete_branch(
            REPO_NAME, BRANCH_NAME, region_name=REGION,
        )
        assert isinstance(result, BranchResult)
        assert result.branch_name == BRANCH_NAME

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_branch.side_effect = _make_client_error(
            "BranchDoesNotExistException", "not found",
            "DeleteBranch",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="delete_branch failed"):
            delete_branch(REPO_NAME, BRANCH_NAME)


# ---------------------------------------------------------------------------
# merge_branches_by_fast_forward
# ---------------------------------------------------------------------------


class TestMergeBranchesByFastForward:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_fast_forward.return_value = {
            "commitId": "merged-commit",
        }
        mock_gc.return_value = client

        result = merge_branches_by_fast_forward(
            REPO_NAME, "src-commit", "dst-commit",
            target_branch="main",
            region_name=REGION,
        )
        assert result == "merged-commit"

    @patch("aws_util.codecommit.get_client")
    def test_no_target_branch(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_fast_forward.return_value = {
            "commitId": "merged-commit",
        }
        mock_gc.return_value = client

        result = merge_branches_by_fast_forward(
            REPO_NAME, "src", "dst",
        )
        assert result == "merged-commit"
        call_kw = client.merge_branches_by_fast_forward.call_args[1]
        assert "targetBranch" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_fast_forward.side_effect = (
            _make_client_error(
                "ManualMergeRequiredException", "conflict",
                "MergeBranchesByFastForward",
            )
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError,
            match="merge_branches_by_fast_forward failed",
        ):
            merge_branches_by_fast_forward(REPO_NAME, "s", "d")


# ---------------------------------------------------------------------------
# merge_branches_by_squash
# ---------------------------------------------------------------------------


class TestMergeBranchesBySquash:
    @patch("aws_util.codecommit.get_client")
    def test_success_all_options(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_squash.return_value = {
            "commitId": "squash-commit",
        }
        mock_gc.return_value = client

        result = merge_branches_by_squash(
            REPO_NAME, "src", "dst",
            target_branch="main",
            author_name="Test",
            email="t@test.com",
            commit_message="squash merge",
            region_name=REGION,
        )
        assert result == "squash-commit"
        call_kw = client.merge_branches_by_squash.call_args[1]
        assert call_kw["targetBranch"] == "main"
        assert call_kw["authorName"] == "Test"
        assert call_kw["email"] == "t@test.com"
        assert call_kw["commitMessage"] == "squash merge"

    @patch("aws_util.codecommit.get_client")
    def test_minimal(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_squash.return_value = {
            "commitId": "squash-commit",
        }
        mock_gc.return_value = client

        result = merge_branches_by_squash(REPO_NAME, "src", "dst")
        assert result == "squash-commit"
        call_kw = client.merge_branches_by_squash.call_args[1]
        assert "targetBranch" not in call_kw
        assert "authorName" not in call_kw
        assert "email" not in call_kw
        assert "commitMessage" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.merge_branches_by_squash.side_effect = (
            _make_client_error(
                "ManualMergeRequiredException", "conflict",
                "MergeBranchesBySquash",
            )
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="merge_branches_by_squash failed",
        ):
            merge_branches_by_squash(REPO_NAME, "s", "d")


# ---------------------------------------------------------------------------
# create_commit
# ---------------------------------------------------------------------------


class TestCreateCommit:
    @patch("aws_util.codecommit.get_client")
    def test_success_all_options(self, mock_gc):
        client = MagicMock()
        client.create_commit.return_value = {
            "commitId": COMMIT_ID,
            "treeId": "tree1",
            "parents": ["parent1"],
        }
        mock_gc.return_value = client

        result = create_commit(
            REPO_NAME, "main",
            parent_commit_id="parent1",
            author_name="Author",
            email="a@a.com",
            commit_message="commit msg",
            put_files=[{"filePath": "a.txt", "fileContent": b"hi"}],
            delete_files=[{"filePath": "b.txt"}],
            region_name=REGION,
        )
        assert isinstance(result, CommitResult)
        assert result.commit_id == COMMIT_ID
        assert result.tree_id == "tree1"
        assert result.parents == ["parent1"]

    @patch("aws_util.codecommit.get_client")
    def test_minimal(self, mock_gc):
        client = MagicMock()
        client.create_commit.return_value = {
            "commitId": COMMIT_ID,
        }
        mock_gc.return_value = client

        result = create_commit(REPO_NAME, "main")
        assert result.commit_id == COMMIT_ID
        call_kw = client.create_commit.call_args[1]
        assert "parentCommitId" not in call_kw
        assert "authorName" not in call_kw
        assert "email" not in call_kw
        assert "commitMessage" not in call_kw
        assert "putFiles" not in call_kw
        assert "deleteFiles" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_commit.side_effect = _make_client_error(
            "BranchDoesNotExistException", "no branch",
            "CreateCommit",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="create_commit failed"):
            create_commit(REPO_NAME, "main")


# ---------------------------------------------------------------------------
# get_commit
# ---------------------------------------------------------------------------


class TestGetCommit:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_commit.return_value = {"commit": _RAW_COMMIT}
        mock_gc.return_value = client

        result = get_commit(
            REPO_NAME, COMMIT_ID, region_name=REGION,
        )
        assert isinstance(result, CommitResult)
        assert result.commit_id == COMMIT_ID
        assert result.message == "Initial commit"

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_commit.side_effect = _make_client_error(
            "CommitDoesNotExistException", "not found",
            "GetCommit",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="get_commit failed"):
            get_commit(REPO_NAME, COMMIT_ID)


# ---------------------------------------------------------------------------
# get_file
# ---------------------------------------------------------------------------


class TestGetFile:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_file.return_value = {
            "filePath": "a.txt",
            "fileSize": 5,
            "fileMode": "NORMAL",
            "blobId": BLOB_ID,
            "commitId": COMMIT_ID,
            "fileContent": b"hello",
        }
        mock_gc.return_value = client

        result = get_file(
            REPO_NAME, "a.txt",
            commit_specifier="main",
            region_name=REGION,
        )
        assert isinstance(result, FileResult)
        assert result.file_path == "a.txt"
        assert result.file_content == b"hello"

    @patch("aws_util.codecommit.get_client")
    def test_no_commit_specifier(self, mock_gc):
        client = MagicMock()
        client.get_file.return_value = {
            "filePath": "a.txt",
            "fileContent": b"hello",
        }
        mock_gc.return_value = client

        result = get_file(REPO_NAME, "a.txt")
        assert result.file_path == "a.txt"
        call_kw = client.get_file.call_args[1]
        assert "commitSpecifier" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_file.side_effect = _make_client_error(
            "FileDoesNotExistException", "not found", "GetFile",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="get_file failed"):
            get_file(REPO_NAME, "a.txt")


# ---------------------------------------------------------------------------
# put_file
# ---------------------------------------------------------------------------


class TestPutFile:
    @patch("aws_util.codecommit.get_client")
    def test_success_all_options(self, mock_gc):
        client = MagicMock()
        client.put_file.return_value = {
            "commitId": COMMIT_ID,
            "blobId": BLOB_ID,
            "treeId": "tree1",
        }
        mock_gc.return_value = client

        result = put_file(
            REPO_NAME, "a.txt", b"hello", "main",
            file_mode="EXECUTABLE",
            parent_commit_id="parent1",
            commit_message="add file",
            name="Author",
            email="a@a.com",
            region_name=REGION,
        )
        assert result["commitId"] == COMMIT_ID
        assert result["blobId"] == BLOB_ID
        call_kw = client.put_file.call_args[1]
        assert call_kw["fileMode"] == "EXECUTABLE"
        assert call_kw["parentCommitId"] == "parent1"
        assert call_kw["commitMessage"] == "add file"
        assert call_kw["name"] == "Author"
        assert call_kw["email"] == "a@a.com"

    @patch("aws_util.codecommit.get_client")
    def test_minimal(self, mock_gc):
        client = MagicMock()
        client.put_file.return_value = {
            "commitId": COMMIT_ID,
            "blobId": BLOB_ID,
            "treeId": "tree1",
        }
        mock_gc.return_value = client

        result = put_file(REPO_NAME, "a.txt", b"hello", "main")
        assert result["commitId"] == COMMIT_ID
        call_kw = client.put_file.call_args[1]
        assert "fileMode" not in call_kw
        assert "parentCommitId" not in call_kw
        assert "commitMessage" not in call_kw
        assert "name" not in call_kw
        assert "email" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.put_file.side_effect = _make_client_error(
            "BranchDoesNotExistException", "no branch", "PutFile",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="put_file failed"):
            put_file(REPO_NAME, "a.txt", b"hello", "main")


# ---------------------------------------------------------------------------
# delete_file
# ---------------------------------------------------------------------------


class TestDeleteFile:
    @patch("aws_util.codecommit.get_client")
    def test_success_all_options(self, mock_gc):
        client = MagicMock()
        client.delete_file.return_value = {
            "commitId": COMMIT_ID,
            "blobId": BLOB_ID,
            "treeId": "tree1",
            "filePath": "a.txt",
        }
        mock_gc.return_value = client

        result = delete_file(
            REPO_NAME, "a.txt", "main", "parent1",
            commit_message="delete file",
            name="Author",
            email="a@a.com",
            keep_empty_folders=True,
            region_name=REGION,
        )
        assert result["commitId"] == COMMIT_ID
        assert result["filePath"] == "a.txt"
        call_kw = client.delete_file.call_args[1]
        assert call_kw["commitMessage"] == "delete file"
        assert call_kw["name"] == "Author"
        assert call_kw["email"] == "a@a.com"
        assert call_kw["keepEmptyFolders"] is True

    @patch("aws_util.codecommit.get_client")
    def test_minimal(self, mock_gc):
        client = MagicMock()
        client.delete_file.return_value = {
            "commitId": COMMIT_ID,
            "blobId": BLOB_ID,
            "treeId": "tree1",
            "filePath": "a.txt",
        }
        mock_gc.return_value = client

        result = delete_file(REPO_NAME, "a.txt", "main", "parent1")
        assert result["commitId"] == COMMIT_ID
        call_kw = client.delete_file.call_args[1]
        assert "commitMessage" not in call_kw
        assert "name" not in call_kw
        assert "email" not in call_kw
        assert call_kw["keepEmptyFolders"] is False

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_file.side_effect = _make_client_error(
            "FileDoesNotExistException", "not found", "DeleteFile",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="delete_file failed"):
            delete_file(REPO_NAME, "a.txt", "main", "parent1")


# ---------------------------------------------------------------------------
# get_differences
# ---------------------------------------------------------------------------


class TestGetDifferences:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"differences": [_RAW_DIFF]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = get_differences(
            REPO_NAME, COMMIT_ID,
            before_commit_specifier="before-commit",
            before_path="old/",
            after_path="new/",
            region_name=REGION,
        )
        assert len(result) == 1
        assert isinstance(result[0], DiffResult)
        assert result[0].change_type == "M"

    @patch("aws_util.codecommit.get_client")
    def test_minimal(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"differences": [_RAW_DIFF]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = get_differences(REPO_NAME, COMMIT_ID)
        assert len(result) == 1

    @patch("aws_util.codecommit.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"differences": [_RAW_DIFF]},
            {"differences": [_RAW_DIFF]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = get_differences(REPO_NAME, COMMIT_ID)
        assert len(result) == 2

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_paginator.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "GetDifferences",
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="get_differences failed"
        ):
            get_differences(REPO_NAME, COMMIT_ID)


# ---------------------------------------------------------------------------
# create_pull_request
# ---------------------------------------------------------------------------


class TestCreatePullRequest:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_pull_request.return_value = {
            "pullRequest": _RAW_PR,
        }
        mock_gc.return_value = client

        targets = [
            {
                "repositoryName": REPO_NAME,
                "sourceReference": "refs/heads/feature",
            }
        ]
        result = create_pull_request(
            "Test PR", targets,
            description="A test",
            region_name=REGION,
        )
        assert isinstance(result, PullRequestResult)
        assert result.title == "Test PR"
        call_kw = client.create_pull_request.call_args[1]
        assert call_kw["description"] == "A test"

    @patch("aws_util.codecommit.get_client")
    def test_no_description(self, mock_gc):
        client = MagicMock()
        client.create_pull_request.return_value = {
            "pullRequest": _RAW_PR,
        }
        mock_gc.return_value = client

        result = create_pull_request("T", [])
        assert result.title == "Test PR"
        call_kw = client.create_pull_request.call_args[1]
        assert "description" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_pull_request.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "CreatePullRequest",
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="create_pull_request failed"
        ):
            create_pull_request("T", [])


# ---------------------------------------------------------------------------
# get_pull_request
# ---------------------------------------------------------------------------


class TestGetPullRequest:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_pull_request.return_value = {
            "pullRequest": _RAW_PR,
        }
        mock_gc.return_value = client

        result = get_pull_request(PR_ID, region_name=REGION)
        assert result.pull_request_id == PR_ID

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_pull_request.side_effect = _make_client_error(
            "PullRequestDoesNotExistException", "not found",
            "GetPullRequest",
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="get_pull_request failed"
        ):
            get_pull_request(PR_ID)


# ---------------------------------------------------------------------------
# list_pull_requests
# ---------------------------------------------------------------------------


class TestListPullRequests:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"pullRequestIds": ["1", "2"]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_pull_requests(REPO_NAME, region_name=REGION)
        assert result == ["1", "2"]

    @patch("aws_util.codecommit.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"pullRequestIds": ["1"]},
            {"pullRequestIds": ["2"]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client

        result = list_pull_requests(
            REPO_NAME, pull_request_status="CLOSED",
        )
        assert result == ["1", "2"]

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_paginator.side_effect = _make_client_error(
            "RepositoryDoesNotExistException", "not found",
            "ListPullRequests",
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError, match="list_pull_requests failed"
        ):
            list_pull_requests(REPO_NAME)


# ---------------------------------------------------------------------------
# merge_pull_request_by_fast_forward
# ---------------------------------------------------------------------------


class TestMergePullRequestByFastForward:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.merge_pull_request_by_fast_forward.return_value = {
            "pullRequest": _RAW_PR,
        }
        mock_gc.return_value = client

        result = merge_pull_request_by_fast_forward(
            PR_ID, REPO_NAME,
            source_commit_id=COMMIT_ID,
            region_name=REGION,
        )
        assert isinstance(result, PullRequestResult)

    @patch("aws_util.codecommit.get_client")
    def test_no_source_commit(self, mock_gc):
        client = MagicMock()
        client.merge_pull_request_by_fast_forward.return_value = {
            "pullRequest": _RAW_PR,
        }
        mock_gc.return_value = client

        result = merge_pull_request_by_fast_forward(PR_ID, REPO_NAME)
        assert result.pull_request_id == PR_ID
        call_kw = (
            client.merge_pull_request_by_fast_forward.call_args[1]
        )
        assert "sourceCommitId" not in call_kw

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.merge_pull_request_by_fast_forward.side_effect = (
            _make_client_error(
                "ManualMergeRequiredException", "conflict",
                "MergePullRequestByFastForward",
            )
        )
        mock_gc.return_value = client

        with pytest.raises(
            RuntimeError,
            match="merge_pull_request_by_fast_forward failed",
        ):
            merge_pull_request_by_fast_forward(PR_ID, REPO_NAME)


# ---------------------------------------------------------------------------
# get_blob
# ---------------------------------------------------------------------------


class TestGetBlob:
    @patch("aws_util.codecommit.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_blob.return_value = {
            "content": b"blob-content",
        }
        mock_gc.return_value = client

        result = get_blob(
            REPO_NAME, BLOB_ID, region_name=REGION,
        )
        assert isinstance(result, BlobResult)
        assert result.blob_id == BLOB_ID
        assert result.content == b"blob-content"

    @patch("aws_util.codecommit.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_blob.side_effect = _make_client_error(
            "BlobIdDoesNotExistException", "not found", "GetBlob",
        )
        mock_gc.return_value = client

        with pytest.raises(RuntimeError, match="get_blob failed"):
            get_blob(REPO_NAME, BLOB_ID)


@patch("aws_util.codecommit.get_client")
def test_associate_approval_rule_template_with_repository(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_approval_rule_template_with_repository.return_value = {}
    associate_approval_rule_template_with_repository("test-approval_rule_template_name", "test-repository_name", region_name=REGION)
    mock_client.associate_approval_rule_template_with_repository.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_associate_approval_rule_template_with_repository_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_approval_rule_template_with_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_approval_rule_template_with_repository",
    )
    with pytest.raises(RuntimeError, match="Failed to associate approval rule template with repository"):
        associate_approval_rule_template_with_repository("test-approval_rule_template_name", "test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_batch_associate_approval_rule_template_with_repositories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_approval_rule_template_with_repositories.return_value = {}
    batch_associate_approval_rule_template_with_repositories("test-approval_rule_template_name", [], region_name=REGION)
    mock_client.batch_associate_approval_rule_template_with_repositories.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_batch_associate_approval_rule_template_with_repositories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_approval_rule_template_with_repositories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_approval_rule_template_with_repositories",
    )
    with pytest.raises(RuntimeError, match="Failed to batch associate approval rule template with repositories"):
        batch_associate_approval_rule_template_with_repositories("test-approval_rule_template_name", [], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_batch_describe_merge_conflicts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_describe_merge_conflicts.return_value = {}
    batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", region_name=REGION)
    mock_client.batch_describe_merge_conflicts.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_batch_describe_merge_conflicts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_describe_merge_conflicts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_describe_merge_conflicts",
    )
    with pytest.raises(RuntimeError, match="Failed to batch describe merge conflicts"):
        batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_batch_disassociate_approval_rule_template_from_repositories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_approval_rule_template_from_repositories.return_value = {}
    batch_disassociate_approval_rule_template_from_repositories("test-approval_rule_template_name", [], region_name=REGION)
    mock_client.batch_disassociate_approval_rule_template_from_repositories.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_batch_disassociate_approval_rule_template_from_repositories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_approval_rule_template_from_repositories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_approval_rule_template_from_repositories",
    )
    with pytest.raises(RuntimeError, match="Failed to batch disassociate approval rule template from repositories"):
        batch_disassociate_approval_rule_template_from_repositories("test-approval_rule_template_name", [], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_batch_get_commits(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_commits.return_value = {}
    batch_get_commits([], "test-repository_name", region_name=REGION)
    mock_client.batch_get_commits.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_batch_get_commits_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_commits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_commits",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get commits"):
        batch_get_commits([], "test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_batch_get_repositories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_repositories.return_value = {}
    batch_get_repositories([], region_name=REGION)
    mock_client.batch_get_repositories.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_batch_get_repositories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_repositories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_repositories",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get repositories"):
        batch_get_repositories([], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_create_approval_rule_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_approval_rule_template.return_value = {}
    create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", region_name=REGION)
    mock_client.create_approval_rule_template.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_create_approval_rule_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_approval_rule_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_approval_rule_template",
    )
    with pytest.raises(RuntimeError, match="Failed to create approval rule template"):
        create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_create_pull_request_approval_rule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_pull_request_approval_rule.return_value = {}
    create_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", "test-approval_rule_content", region_name=REGION)
    mock_client.create_pull_request_approval_rule.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_create_pull_request_approval_rule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_pull_request_approval_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_pull_request_approval_rule",
    )
    with pytest.raises(RuntimeError, match="Failed to create pull request approval rule"):
        create_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", "test-approval_rule_content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_create_unreferenced_merge_commit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_unreferenced_merge_commit.return_value = {}
    create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", region_name=REGION)
    mock_client.create_unreferenced_merge_commit.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_create_unreferenced_merge_commit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_unreferenced_merge_commit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_unreferenced_merge_commit",
    )
    with pytest.raises(RuntimeError, match="Failed to create unreferenced merge commit"):
        create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_delete_approval_rule_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_approval_rule_template.return_value = {}
    delete_approval_rule_template("test-approval_rule_template_name", region_name=REGION)
    mock_client.delete_approval_rule_template.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_delete_approval_rule_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_approval_rule_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_approval_rule_template",
    )
    with pytest.raises(RuntimeError, match="Failed to delete approval rule template"):
        delete_approval_rule_template("test-approval_rule_template_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_delete_comment_content(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_comment_content.return_value = {}
    delete_comment_content("test-comment_id", region_name=REGION)
    mock_client.delete_comment_content.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_delete_comment_content_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_comment_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_comment_content",
    )
    with pytest.raises(RuntimeError, match="Failed to delete comment content"):
        delete_comment_content("test-comment_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_delete_pull_request_approval_rule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_pull_request_approval_rule.return_value = {}
    delete_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", region_name=REGION)
    mock_client.delete_pull_request_approval_rule.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_delete_pull_request_approval_rule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_pull_request_approval_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_pull_request_approval_rule",
    )
    with pytest.raises(RuntimeError, match="Failed to delete pull request approval rule"):
        delete_pull_request_approval_rule("test-pull_request_id", "test-approval_rule_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_describe_merge_conflicts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_merge_conflicts.return_value = {}
    describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", region_name=REGION)
    mock_client.describe_merge_conflicts.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_describe_merge_conflicts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_merge_conflicts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_merge_conflicts",
    )
    with pytest.raises(RuntimeError, match="Failed to describe merge conflicts"):
        describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_describe_pull_request_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pull_request_events.return_value = {}
    describe_pull_request_events("test-pull_request_id", region_name=REGION)
    mock_client.describe_pull_request_events.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_describe_pull_request_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pull_request_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pull_request_events",
    )
    with pytest.raises(RuntimeError, match="Failed to describe pull request events"):
        describe_pull_request_events("test-pull_request_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_disassociate_approval_rule_template_from_repository(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_approval_rule_template_from_repository.return_value = {}
    disassociate_approval_rule_template_from_repository("test-approval_rule_template_name", "test-repository_name", region_name=REGION)
    mock_client.disassociate_approval_rule_template_from_repository.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_disassociate_approval_rule_template_from_repository_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_approval_rule_template_from_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_approval_rule_template_from_repository",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate approval rule template from repository"):
        disassociate_approval_rule_template_from_repository("test-approval_rule_template_name", "test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_evaluate_pull_request_approval_rules(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.evaluate_pull_request_approval_rules.return_value = {}
    evaluate_pull_request_approval_rules("test-pull_request_id", "test-revision_id", region_name=REGION)
    mock_client.evaluate_pull_request_approval_rules.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_evaluate_pull_request_approval_rules_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.evaluate_pull_request_approval_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "evaluate_pull_request_approval_rules",
    )
    with pytest.raises(RuntimeError, match="Failed to evaluate pull request approval rules"):
        evaluate_pull_request_approval_rules("test-pull_request_id", "test-revision_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_approval_rule_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_approval_rule_template.return_value = {}
    get_approval_rule_template("test-approval_rule_template_name", region_name=REGION)
    mock_client.get_approval_rule_template.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_approval_rule_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_approval_rule_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_approval_rule_template",
    )
    with pytest.raises(RuntimeError, match="Failed to get approval rule template"):
        get_approval_rule_template("test-approval_rule_template_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_comment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comment.return_value = {}
    get_comment("test-comment_id", region_name=REGION)
    mock_client.get_comment.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_comment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_comment",
    )
    with pytest.raises(RuntimeError, match="Failed to get comment"):
        get_comment("test-comment_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_comment_reactions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comment_reactions.return_value = {}
    get_comment_reactions("test-comment_id", region_name=REGION)
    mock_client.get_comment_reactions.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_comment_reactions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comment_reactions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_comment_reactions",
    )
    with pytest.raises(RuntimeError, match="Failed to get comment reactions"):
        get_comment_reactions("test-comment_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_comments_for_compared_commit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comments_for_compared_commit.return_value = {}
    get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", region_name=REGION)
    mock_client.get_comments_for_compared_commit.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_comments_for_compared_commit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comments_for_compared_commit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_comments_for_compared_commit",
    )
    with pytest.raises(RuntimeError, match="Failed to get comments for compared commit"):
        get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_comments_for_pull_request(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comments_for_pull_request.return_value = {}
    get_comments_for_pull_request("test-pull_request_id", region_name=REGION)
    mock_client.get_comments_for_pull_request.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_comments_for_pull_request_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_comments_for_pull_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_comments_for_pull_request",
    )
    with pytest.raises(RuntimeError, match="Failed to get comments for pull request"):
        get_comments_for_pull_request("test-pull_request_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_folder(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_folder.return_value = {}
    get_folder("test-repository_name", "test-folder_path", region_name=REGION)
    mock_client.get_folder.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_folder_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_folder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_folder",
    )
    with pytest.raises(RuntimeError, match="Failed to get folder"):
        get_folder("test-repository_name", "test-folder_path", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_merge_commit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_commit.return_value = {}
    get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)
    mock_client.get_merge_commit.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_merge_commit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_commit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_merge_commit",
    )
    with pytest.raises(RuntimeError, match="Failed to get merge commit"):
        get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_merge_conflicts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_conflicts.return_value = {}
    get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", region_name=REGION)
    mock_client.get_merge_conflicts.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_merge_conflicts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_conflicts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_merge_conflicts",
    )
    with pytest.raises(RuntimeError, match="Failed to get merge conflicts"):
        get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_merge_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_options.return_value = {}
    get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)
    mock_client.get_merge_options.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_merge_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_merge_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_merge_options",
    )
    with pytest.raises(RuntimeError, match="Failed to get merge options"):
        get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_pull_request_approval_states(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_pull_request_approval_states.return_value = {}
    get_pull_request_approval_states("test-pull_request_id", "test-revision_id", region_name=REGION)
    mock_client.get_pull_request_approval_states.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_pull_request_approval_states_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_pull_request_approval_states.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_pull_request_approval_states",
    )
    with pytest.raises(RuntimeError, match="Failed to get pull request approval states"):
        get_pull_request_approval_states("test-pull_request_id", "test-revision_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_pull_request_override_state(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_pull_request_override_state.return_value = {}
    get_pull_request_override_state("test-pull_request_id", "test-revision_id", region_name=REGION)
    mock_client.get_pull_request_override_state.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_pull_request_override_state_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_pull_request_override_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_pull_request_override_state",
    )
    with pytest.raises(RuntimeError, match="Failed to get pull request override state"):
        get_pull_request_override_state("test-pull_request_id", "test-revision_id", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_get_repository_triggers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_triggers.return_value = {}
    get_repository_triggers("test-repository_name", region_name=REGION)
    mock_client.get_repository_triggers.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_get_repository_triggers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_repository_triggers",
    )
    with pytest.raises(RuntimeError, match="Failed to get repository triggers"):
        get_repository_triggers("test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_list_approval_rule_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_approval_rule_templates.return_value = {}
    list_approval_rule_templates(region_name=REGION)
    mock_client.list_approval_rule_templates.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_list_approval_rule_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_approval_rule_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_approval_rule_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list approval rule templates"):
        list_approval_rule_templates(region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_list_associated_approval_rule_templates_for_repository(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_approval_rule_templates_for_repository.return_value = {}
    list_associated_approval_rule_templates_for_repository("test-repository_name", region_name=REGION)
    mock_client.list_associated_approval_rule_templates_for_repository.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_list_associated_approval_rule_templates_for_repository_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_approval_rule_templates_for_repository.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associated_approval_rule_templates_for_repository",
    )
    with pytest.raises(RuntimeError, match="Failed to list associated approval rule templates for repository"):
        list_associated_approval_rule_templates_for_repository("test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_list_file_commit_history(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_file_commit_history.return_value = {}
    list_file_commit_history("test-repository_name", "test-file_path", region_name=REGION)
    mock_client.list_file_commit_history.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_list_file_commit_history_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_file_commit_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_file_commit_history",
    )
    with pytest.raises(RuntimeError, match="Failed to list file commit history"):
        list_file_commit_history("test-repository_name", "test-file_path", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_list_repositories_for_approval_rule_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repositories_for_approval_rule_template.return_value = {}
    list_repositories_for_approval_rule_template("test-approval_rule_template_name", region_name=REGION)
    mock_client.list_repositories_for_approval_rule_template.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_list_repositories_for_approval_rule_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repositories_for_approval_rule_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_repositories_for_approval_rule_template",
    )
    with pytest.raises(RuntimeError, match="Failed to list repositories for approval rule template"):
        list_repositories_for_approval_rule_template("test-approval_rule_template_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_merge_branches_by_three_way(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_branches_by_three_way.return_value = {}
    merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)
    mock_client.merge_branches_by_three_way.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_merge_branches_by_three_way_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_branches_by_three_way.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "merge_branches_by_three_way",
    )
    with pytest.raises(RuntimeError, match="Failed to merge branches by three way"):
        merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_merge_pull_request_by_squash(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_pull_request_by_squash.return_value = {}
    merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", region_name=REGION)
    mock_client.merge_pull_request_by_squash.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_merge_pull_request_by_squash_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_pull_request_by_squash.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "merge_pull_request_by_squash",
    )
    with pytest.raises(RuntimeError, match="Failed to merge pull request by squash"):
        merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_merge_pull_request_by_three_way(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_pull_request_by_three_way.return_value = {}
    merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", region_name=REGION)
    mock_client.merge_pull_request_by_three_way.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_merge_pull_request_by_three_way_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_pull_request_by_three_way.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "merge_pull_request_by_three_way",
    )
    with pytest.raises(RuntimeError, match="Failed to merge pull request by three way"):
        merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_override_pull_request_approval_rules(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.override_pull_request_approval_rules.return_value = {}
    override_pull_request_approval_rules("test-pull_request_id", "test-revision_id", "test-override_status", region_name=REGION)
    mock_client.override_pull_request_approval_rules.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_override_pull_request_approval_rules_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.override_pull_request_approval_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "override_pull_request_approval_rules",
    )
    with pytest.raises(RuntimeError, match="Failed to override pull request approval rules"):
        override_pull_request_approval_rules("test-pull_request_id", "test-revision_id", "test-override_status", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_post_comment_for_compared_commit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_for_compared_commit.return_value = {}
    post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", region_name=REGION)
    mock_client.post_comment_for_compared_commit.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_post_comment_for_compared_commit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_for_compared_commit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "post_comment_for_compared_commit",
    )
    with pytest.raises(RuntimeError, match="Failed to post comment for compared commit"):
        post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_post_comment_for_pull_request(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_for_pull_request.return_value = {}
    post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", region_name=REGION)
    mock_client.post_comment_for_pull_request.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_post_comment_for_pull_request_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_for_pull_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "post_comment_for_pull_request",
    )
    with pytest.raises(RuntimeError, match="Failed to post comment for pull request"):
        post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_post_comment_reply(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_reply.return_value = {}
    post_comment_reply("test-in_reply_to", "test-content", region_name=REGION)
    mock_client.post_comment_reply.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_post_comment_reply_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.post_comment_reply.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "post_comment_reply",
    )
    with pytest.raises(RuntimeError, match="Failed to post comment reply"):
        post_comment_reply("test-in_reply_to", "test-content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_put_comment_reaction(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_comment_reaction.return_value = {}
    put_comment_reaction("test-comment_id", "test-reaction_value", region_name=REGION)
    mock_client.put_comment_reaction.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_put_comment_reaction_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_comment_reaction.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_comment_reaction",
    )
    with pytest.raises(RuntimeError, match="Failed to put comment reaction"):
        put_comment_reaction("test-comment_id", "test-reaction_value", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_put_repository_triggers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_repository_triggers.return_value = {}
    put_repository_triggers("test-repository_name", [], region_name=REGION)
    mock_client.put_repository_triggers.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_put_repository_triggers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_repository_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_repository_triggers",
    )
    with pytest.raises(RuntimeError, match="Failed to put repository triggers"):
        put_repository_triggers("test-repository_name", [], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_run_repository_triggers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_repository_triggers.return_value = {}
    run_repository_triggers("test-repository_name", [], region_name=REGION)
    mock_client.test_repository_triggers.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_run_repository_triggers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_repository_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_repository_triggers",
    )
    with pytest.raises(RuntimeError, match="Failed to run repository triggers"):
        run_repository_triggers("test-repository_name", [], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_content(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_content.return_value = {}
    update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", region_name=REGION)
    mock_client.update_approval_rule_template_content.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_content_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_approval_rule_template_content",
    )
    with pytest.raises(RuntimeError, match="Failed to update approval rule template content"):
        update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_description(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_description.return_value = {}
    update_approval_rule_template_description("test-approval_rule_template_name", "test-approval_rule_template_description", region_name=REGION)
    mock_client.update_approval_rule_template_description.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_description_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_description.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_approval_rule_template_description",
    )
    with pytest.raises(RuntimeError, match="Failed to update approval rule template description"):
        update_approval_rule_template_description("test-approval_rule_template_name", "test-approval_rule_template_description", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_name(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_name.return_value = {}
    update_approval_rule_template_name("test-old_approval_rule_template_name", "test-new_approval_rule_template_name", region_name=REGION)
    mock_client.update_approval_rule_template_name.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_approval_rule_template_name_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_approval_rule_template_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_approval_rule_template_name",
    )
    with pytest.raises(RuntimeError, match="Failed to update approval rule template name"):
        update_approval_rule_template_name("test-old_approval_rule_template_name", "test-new_approval_rule_template_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_comment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_comment.return_value = {}
    update_comment("test-comment_id", "test-content", region_name=REGION)
    mock_client.update_comment.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_comment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_comment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_comment",
    )
    with pytest.raises(RuntimeError, match="Failed to update comment"):
        update_comment("test-comment_id", "test-content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_default_branch(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_default_branch.return_value = {}
    update_default_branch("test-repository_name", "test-default_branch_name", region_name=REGION)
    mock_client.update_default_branch.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_default_branch_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_default_branch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_default_branch",
    )
    with pytest.raises(RuntimeError, match="Failed to update default branch"):
        update_default_branch("test-repository_name", "test-default_branch_name", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_approval_rule_content(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_approval_rule_content.return_value = {}
    update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", region_name=REGION)
    mock_client.update_pull_request_approval_rule_content.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_approval_rule_content_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_approval_rule_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_request_approval_rule_content",
    )
    with pytest.raises(RuntimeError, match="Failed to update pull request approval rule content"):
        update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_approval_state(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_approval_state.return_value = {}
    update_pull_request_approval_state("test-pull_request_id", "test-revision_id", "test-approval_state", region_name=REGION)
    mock_client.update_pull_request_approval_state.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_approval_state_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_approval_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_request_approval_state",
    )
    with pytest.raises(RuntimeError, match="Failed to update pull request approval state"):
        update_pull_request_approval_state("test-pull_request_id", "test-revision_id", "test-approval_state", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_description(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_description.return_value = {}
    update_pull_request_description("test-pull_request_id", "test-description", region_name=REGION)
    mock_client.update_pull_request_description.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_description_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_description.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_request_description",
    )
    with pytest.raises(RuntimeError, match="Failed to update pull request description"):
        update_pull_request_description("test-pull_request_id", "test-description", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_status.return_value = {}
    update_pull_request_status("test-pull_request_id", "test-pull_request_status", region_name=REGION)
    mock_client.update_pull_request_status.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_request_status",
    )
    with pytest.raises(RuntimeError, match="Failed to update pull request status"):
        update_pull_request_status("test-pull_request_id", "test-pull_request_status", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_title(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_title.return_value = {}
    update_pull_request_title("test-pull_request_id", "test-title", region_name=REGION)
    mock_client.update_pull_request_title.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_pull_request_title_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_pull_request_title.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pull_request_title",
    )
    with pytest.raises(RuntimeError, match="Failed to update pull request title"):
        update_pull_request_title("test-pull_request_id", "test-title", region_name=REGION)


@patch("aws_util.codecommit.get_client")
def test_update_repository_encryption_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository_encryption_key.return_value = {}
    update_repository_encryption_key("test-repository_name", "test-kms_key_id", region_name=REGION)
    mock_client.update_repository_encryption_key.assert_called_once()


@patch("aws_util.codecommit.get_client")
def test_update_repository_encryption_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository_encryption_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_repository_encryption_key",
    )
    with pytest.raises(RuntimeError, match="Failed to update repository encryption key"):
        update_repository_encryption_key("test-repository_name", "test-kms_key_id", region_name=REGION)


def test_merge_branches_by_fast_forward_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import merge_branches_by_fast_forward
    mock_client = MagicMock()
    mock_client.merge_branches_by_fast_forward.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    merge_branches_by_fast_forward("test-repository_name", "test-source_commit", "test-destination_commit", target_branch="test-target_branch", region_name="us-east-1")
    mock_client.merge_branches_by_fast_forward.assert_called_once()

def test_merge_branches_by_squash_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import merge_branches_by_squash
    mock_client = MagicMock()
    mock_client.merge_branches_by_squash.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    merge_branches_by_squash("test-repository_name", "test-source_commit", "test-destination_commit", target_branch="test-target_branch", author_name="test-author_name", email="test-email", commit_message="test-commit_message", region_name="us-east-1")
    mock_client.merge_branches_by_squash.assert_called_once()

def test_create_commit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import create_commit
    mock_client = MagicMock()
    mock_client.create_commit.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    create_commit("test-repository_name", "test-branch_name", parent_commit_id="test-parent_commit_id", author_name="test-author_name", email="test-email", commit_message="test-commit_message", put_files="test-put_files", delete_files=True, region_name="us-east-1")
    mock_client.create_commit.assert_called_once()

def test_get_file_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_file
    mock_client = MagicMock()
    mock_client.get_file.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_file("test-repository_name", "test-file_path", commit_specifier="test-commit_specifier", region_name="us-east-1")
    mock_client.get_file.assert_called_once()

def test_put_file_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import put_file
    mock_client = MagicMock()
    mock_client.put_file.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    put_file("test-repository_name", "test-file_path", "test-file_content", "test-branch_name", file_mode="test-file_mode", parent_commit_id="test-parent_commit_id", commit_message="test-commit_message", name="test-name", email="test-email", region_name="us-east-1")
    mock_client.put_file.assert_called_once()

def test_delete_file_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import delete_file
    mock_client = MagicMock()
    mock_client.delete_file.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    delete_file("test-repository_name", "test-file_path", "test-branch_name", "test-parent_commit_id", commit_message="test-commit_message", name="test-name", email="test-email", region_name="us-east-1")
    mock_client.delete_file.assert_called_once()

def test_batch_describe_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import batch_describe_merge_conflicts
    mock_client = MagicMock()
    mock_client.batch_describe_merge_conflicts.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    batch_describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", max_merge_hunks=1, max_conflict_files=1, file_paths="test-file_paths", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.batch_describe_merge_conflicts.assert_called_once()

def test_create_approval_rule_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import create_approval_rule_template
    mock_client = MagicMock()
    mock_client.create_approval_rule_template.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    create_approval_rule_template("test-approval_rule_template_name", "test-approval_rule_template_content", approval_rule_template_description="test-approval_rule_template_description", region_name="us-east-1")
    mock_client.create_approval_rule_template.assert_called_once()

def test_create_unreferenced_merge_commit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import create_unreferenced_merge_commit
    mock_client = MagicMock()
    mock_client.create_unreferenced_merge_commit.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    create_unreferenced_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", "test-merge_option", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", author_name="test-author_name", email="test-email", commit_message="test-commit_message", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.create_unreferenced_merge_commit.assert_called_once()

def test_describe_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import describe_merge_conflicts
    mock_client = MagicMock()
    mock_client.describe_merge_conflicts.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    describe_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", "test-file_path", max_merge_hunks=1, conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_merge_conflicts.assert_called_once()

def test_describe_pull_request_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import describe_pull_request_events
    mock_client = MagicMock()
    mock_client.describe_pull_request_events.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    describe_pull_request_events("test-pull_request_id", pull_request_event_type="test-pull_request_event_type", actor_arn="test-actor_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_pull_request_events.assert_called_once()

def test_get_comment_reactions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_comment_reactions
    mock_client = MagicMock()
    mock_client.get_comment_reactions.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_comment_reactions("test-comment_id", reaction_user_arn="test-reaction_user_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_comment_reactions.assert_called_once()

def test_get_comments_for_compared_commit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_comments_for_compared_commit
    mock_client = MagicMock()
    mock_client.get_comments_for_compared_commit.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_comments_for_compared_commit("test-repository_name", "test-after_commit_id", before_commit_id="test-before_commit_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_comments_for_compared_commit.assert_called_once()

def test_get_comments_for_pull_request_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_comments_for_pull_request
    mock_client = MagicMock()
    mock_client.get_comments_for_pull_request.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_comments_for_pull_request("test-pull_request_id", repository_name="test-repository_name", before_commit_id="test-before_commit_id", after_commit_id="test-after_commit_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_comments_for_pull_request.assert_called_once()

def test_get_folder_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_folder
    mock_client = MagicMock()
    mock_client.get_folder.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_folder("test-repository_name", "test-folder_path", commit_specifier="test-commit_specifier", region_name="us-east-1")
    mock_client.get_folder.assert_called_once()

def test_get_merge_commit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_merge_commit
    mock_client = MagicMock()
    mock_client.get_merge_commit.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_merge_commit("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", region_name="us-east-1")
    mock_client.get_merge_commit.assert_called_once()

def test_get_merge_conflicts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_merge_conflicts
    mock_client = MagicMock()
    mock_client.get_merge_conflicts.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_merge_conflicts("test-repository_name", "test-destination_commit_specifier", "test-source_commit_specifier", "test-merge_option", conflict_detail_level="test-conflict_detail_level", max_conflict_files=1, conflict_resolution_strategy="test-conflict_resolution_strategy", next_token="test-next_token", region_name="us-east-1")
    mock_client.get_merge_conflicts.assert_called_once()

def test_get_merge_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import get_merge_options
    mock_client = MagicMock()
    mock_client.get_merge_options.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    get_merge_options("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", region_name="us-east-1")
    mock_client.get_merge_options.assert_called_once()

def test_list_approval_rule_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import list_approval_rule_templates
    mock_client = MagicMock()
    mock_client.list_approval_rule_templates.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    list_approval_rule_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_approval_rule_templates.assert_called_once()

def test_list_associated_approval_rule_templates_for_repository_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import list_associated_approval_rule_templates_for_repository
    mock_client = MagicMock()
    mock_client.list_associated_approval_rule_templates_for_repository.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    list_associated_approval_rule_templates_for_repository("test-repository_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_associated_approval_rule_templates_for_repository.assert_called_once()

def test_list_file_commit_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import list_file_commit_history
    mock_client = MagicMock()
    mock_client.list_file_commit_history.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    list_file_commit_history("test-repository_name", "test-file_path", commit_specifier="test-commit_specifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_file_commit_history.assert_called_once()

def test_list_repositories_for_approval_rule_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import list_repositories_for_approval_rule_template
    mock_client = MagicMock()
    mock_client.list_repositories_for_approval_rule_template.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    list_repositories_for_approval_rule_template("test-approval_rule_template_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_repositories_for_approval_rule_template.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_merge_branches_by_three_way_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import merge_branches_by_three_way
    mock_client = MagicMock()
    mock_client.merge_branches_by_three_way.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    merge_branches_by_three_way("test-repository_name", "test-source_commit_specifier", "test-destination_commit_specifier", target_branch="test-target_branch", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", author_name="test-author_name", email="test-email", commit_message="test-commit_message", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.merge_branches_by_three_way.assert_called_once()

def test_merge_pull_request_by_squash_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import merge_pull_request_by_squash
    mock_client = MagicMock()
    mock_client.merge_pull_request_by_squash.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    merge_pull_request_by_squash("test-pull_request_id", "test-repository_name", source_commit_id="test-source_commit_id", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", commit_message="test-commit_message", author_name="test-author_name", email="test-email", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.merge_pull_request_by_squash.assert_called_once()

def test_merge_pull_request_by_three_way_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import merge_pull_request_by_three_way
    mock_client = MagicMock()
    mock_client.merge_pull_request_by_three_way.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    merge_pull_request_by_three_way("test-pull_request_id", "test-repository_name", source_commit_id="test-source_commit_id", conflict_detail_level="test-conflict_detail_level", conflict_resolution_strategy="test-conflict_resolution_strategy", commit_message="test-commit_message", author_name="test-author_name", email="test-email", keep_empty_folders="test-keep_empty_folders", conflict_resolution="test-conflict_resolution", region_name="us-east-1")
    mock_client.merge_pull_request_by_three_way.assert_called_once()

def test_post_comment_for_compared_commit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import post_comment_for_compared_commit
    mock_client = MagicMock()
    mock_client.post_comment_for_compared_commit.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    post_comment_for_compared_commit("test-repository_name", "test-after_commit_id", "test-content", before_commit_id="test-before_commit_id", location="test-location", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.post_comment_for_compared_commit.assert_called_once()

def test_post_comment_for_pull_request_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import post_comment_for_pull_request
    mock_client = MagicMock()
    mock_client.post_comment_for_pull_request.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    post_comment_for_pull_request("test-pull_request_id", "test-repository_name", "test-before_commit_id", "test-after_commit_id", "test-content", location="test-location", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.post_comment_for_pull_request.assert_called_once()

def test_post_comment_reply_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import post_comment_reply
    mock_client = MagicMock()
    mock_client.post_comment_reply.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    post_comment_reply("test-in_reply_to", "test-content", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.post_comment_reply.assert_called_once()

def test_update_approval_rule_template_content_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import update_approval_rule_template_content
    mock_client = MagicMock()
    mock_client.update_approval_rule_template_content.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    update_approval_rule_template_content("test-approval_rule_template_name", "test-new_rule_content", existing_rule_content_sha256="test-existing_rule_content_sha256", region_name="us-east-1")
    mock_client.update_approval_rule_template_content.assert_called_once()

def test_update_pull_request_approval_rule_content_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codecommit import update_pull_request_approval_rule_content
    mock_client = MagicMock()
    mock_client.update_pull_request_approval_rule_content.return_value = {}
    monkeypatch.setattr("aws_util.codecommit.get_client", lambda *a, **kw: mock_client)
    update_pull_request_approval_rule_content("test-pull_request_id", "test-approval_rule_name", "test-new_rule_content", existing_rule_content_sha256="test-existing_rule_content_sha256", region_name="us-east-1")
    mock_client.update_pull_request_approval_rule_content.assert_called_once()
