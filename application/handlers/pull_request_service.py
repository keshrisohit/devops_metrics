import json
import traceback
from urllib.parse import unquote

from domain.factory.pull_request_factory import GitHubPullRequestFactory
from domain.github import GithubClient
from infrastructure.pull_request_repository import PullRequestRepository


def make_response(status_code, body, headers):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }


pull_request_repository = PullRequestRepository()


def github_pull_request_service(event, context):
    try:
        print(event)

        body = unquote(event['body'])
        pull_request_webhooh_payload = json.loads(body[8:])
        github_client = GithubClient()
        pull_request = GitHubPullRequestFactory(github_client).create_pull_request(pull_request_webhooh_payload)
        pull_request_repository.save_or_update_pull_request(pull_request)
        return make_response(200, "OK", {'Content-Type': 'application/json'})
    except Exception as e:
        traceback.print_exc()
        return make_response(500, str(e), {'Content-Type': 'application/json'})
