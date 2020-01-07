from datetime import datetime

import iso8601

from infrastructure.models import BranchDBModel, BuildDetailsModels, CommitDBModel, PullRequestDBModel, \
    PullRequestParticipantDBModel


# TODO fix  created_at . updated_at issue

def string_to_datetime(str_time):
    if str_time:
        return iso8601.parse_date(str_time)
    return None


def set_pull_request_db_from_entity(pull_request_db, pull_request, created_at, updated_at):
    pull_request_db.lines_added = pull_request.lines_added
    pull_request_db.commits_url = pull_request.commits_url
    pull_request_db.lines_removed = pull_request.lines_removed
    pull_request_db.no_of_files_changed = pull_request.no_of_files_changed
    pull_request_db.no_of_commits = pull_request.no_of_commits
    pull_request_db.no_of_review_comments = pull_request.review_comments
    pull_request_db.no_of_comments = pull_request.comments
    pull_request_db.no_of_files_changed = pull_request.no_of_files_changed
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
    pull_request_db.row_created_at = created_at
    pull_request_db.row_updated_at = updated_at


def pull_request_entities_to_model(pull_request):
    pull_request_db = PullRequestDBModel()
    set_pull_request_db_from_entity(pull_request_db, pull_request, datetime.now(), datetime.now())

    return pull_request_db


def set_commit_db_from_entity(commit_db, commit):
    commit_db.sha_id = commit.sha_id
    commit_db.description = commit.description
    commit_db.message = commit.message
    commit_db.commiter_username = commit.commiter
    commit_db.commiter_user_id = commit.commiter_id
    commit_db.time = string_to_datetime(commit.commit_time)
    commit_db.repository_url = commit.repository_url
    commit_db.row_created_at = datetime.now()
    commit_db.row_updated_at = datetime.now()


def commit_entites_to_model(commit):
    commit_db = CommitDBModel()
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
    branch_db = BranchDBModel()
    set_branch_db_from_entity(branch_db, branch)
    return branch_db


def set_build_metrics_db_from_entity(build_details, build_metrics):
    build_details.build_id = build_metrics.build_id
    build_details.project_name = build_metrics.project_name
    build_details.source_type = build_metrics.source_type
    build_details.source_location = build_metrics.source_location
    build_details.branch_name = build_metrics.branch_name
    build_details.commit_id = build_metrics.commit_id
    build_details.start_time = build_metrics.start_time
    build_details.end_time = build_metrics.end_time


def build_details_entities_to_model(build_metrics):
    build_details = BuildDetailsModels()
    set_build_metrics_db_from_entity(build_details, build_metrics)
    return build_details


def set_pull_request_participant_db_from_entity(pull_request_participant_db, pull_request_participant):
    pull_request_participant_db.display_name = pull_request_participant.username
    pull_request_participant_db.approved = pull_request_participant.approved
    pull_request_participant_db.participated_on = string_to_datetime(pull_request_participant.participated_on)
    pull_request_participant_db.role = pull_request_participant.role
    pull_request_participant_db.username = pull_request_participant.user_id

    return pull_request_participant


def pull_request_particpants_entity_to_model(pull_request_participant):
    pull_request_participant_db = PullRequestParticipantDBModel()
    set_pull_request_participant_db_from_entity(pull_request_participant_db, pull_request_participant)

    return pull_request_participant_db
