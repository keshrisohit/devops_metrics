from xmlrpc.client import _iso8601_format

from infrastructure.models import PullRequest, PullRequestBranchAssociation, PullRequestCommitAssociation, Commit, \
    Branch
from datetime import datetime
import iso8601


def string_to_datetime(str_time):
    if str_time:
        return iso8601.parse_date(str_time)
    return None


def set_pull_request_db_from_entity(pull_request_db, pull_request):
    pull_request_db.lines_added = pull_request.lines_added
    pull_request_db.commits_url = pull_request.commits_url
    pull_request_db.lines_removed = pull_request.lines_removed
    pull_request_db.no_of_files_changed = pull_request.no_of_files_changed
    pull_request_db.no_of_commits = pull_request.no_of_commits
    pull_request_db.review_comments = pull_request.review_comments
    pull_request_db.merge_commit_sha = pull_request.merge_commit_sha

    pull_request_db.closed_at = string_to_datetime(pull_request.closed_at)
    pull_request_db.merged_at = string_to_datetime(pull_request.merged_at)
    pull_request_db.updated_at = string_to_datetime(pull_request.updated_at)
    pull_request_db.created_at = string_to_datetime(pull_request.created_at)

    pull_request_db.action = pull_request.action
    pull_request_db.sender_user_id = pull_request.sender_id
    pull_request_db.sender_username = "fix this bug"
    pull_request_db.title = pull_request.title
    pull_request_db.repository_url = pull_request.repository_url
    pull_request_db.pull_request_id = pull_request.pull_request_id
    pull_request_db.row_created_at = datetime.now()
    pull_request_db.row_updated_at = datetime.now()


def pull_request_entities_to_model(pull_request):
    pull_request_db = PullRequest()
    set_pull_request_db_from_entity(pull_request_db, pull_request)

    return pull_request_db


def set_commit_db_from_entity(commit_db, commit):
    commit_db.sha_id = commit.sha_id
    commit_db.description = commit.description
    commit_db.message = commit.message
    commit_db.commiter_username = commit.commiter
    commit_db.commiter_user_id = commit.commiter_id
    commit_db.time = commit.commit_time
    commit_db.repository_url = commit.repository_url
    commit_db.row_created_at = datetime.now()
    commit_db.row_updated_at = datetime.now()


def commit_entites_to_model(commit):
    commit_db = Commit()
    set_commit_db_from_entity(commit_db, commit)
    return commit_db


def set_branch_db_from_entity(branch_db, branch):
    branch_db.sha_id = branch.sha_id

    branch_db.name = branch.branch_name
    branch_db.username = branch.branch_user
    branch_db.label = branch.branch_label
    branch_db.user_id = branch.branch_user_id
    branch_db.repository_url = branch.repository_url
    branch_db.row_updated_at = datetime.now()
    branch_db.row_created_at = datetime.now()


def branch_entites_to_model(branch):
    branch_db = Branch()
    set_branch_db_from_entity(branch_db, branch)
    return branch_db
