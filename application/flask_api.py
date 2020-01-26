import json
from urllib.parse import unquote

from flask import Blueprint, request

from domain.factory.deployment_factory import BudilDetailRequestFactory
from domain.factory.issue_factory import IssueRequestFactory
from domain.factory.pull_request_factory import BitBucketEventFactory, GitHubPullRequestFactory
from infrastructure.deployment_repository import DeploymentRepository
from infrastructure.issue_repository import IssueRepository
from infrastructure.pull_request_repository import PullRequestRepository

api = Blueprint('api', __name__)

pullrequest_repo = PullRequestRepository()
issue_repo = IssueRepository()
deployment_repo = DeploymentRepository()


@api.route("/pull_request/github", methods=['POST'])
def add_pullrequest_details_github():
    body = unquote(request.json)
    data = json.loads(body[8:])
    pull_request = GitHubPullRequestFactory().create_pull_request(data)
    pullrequest_repo.create_pull_request(pull_request)

    return json.dumps({"status": "SUCCESS"}), 201


@api.route("/pull_request/bitbucket", methods=['POST'])
def add_pullrequest_details_bitbucket():
    data = request.json
    pull_request = BitBucketEventFactory().create_pull_request(data)
    pullrequest_repo.create_pull_request(pull_request)

    return json.dumps({"status": "SUCCESS"}), 201


@api.route("/build_detail", methods=['POST'])
def add_build_details():
    data = request.json
    build_details = BudilDetailRequestFactory().create_build_details(data)
    deployment_repo.save_build_metrics(build_details)

    return json.dumps({"status": "SUCCESS"}), 201


@api.route("/issue", methods=['POST'])
def add_issue_details():
    data = request.json
    issue = IssueRequestFactory().create_issue(data)
    issue_repo.save_issue(issue)

    return json.dumps({"status": "SUCCESS"}), 201
