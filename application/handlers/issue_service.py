from application.utils import make_response
from domain.factory.issue_factory import IssueRequestFactory
from infrastructure.issue_repository import IssueRepository
import json
issue_repo = IssueRepository()


def create_issue(event, context):
    data = json.loads(event['body'])

    issue = IssueRequestFactory().create_issue(data)
    issue_repo.save_issue(issue)

    return make_response(201, "OK", {'Content-Type': 'application/json'})
