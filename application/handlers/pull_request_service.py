import json
import traceback
from urllib.parse import unquote

from domain.factory.pull_request_factory import GitHubPullRequestFactory
from infrastructure.pull_request_repository import PullRequestRepository


def make_response(status_code, body, headers):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }


def github_pull_request_service(event, context):
    try:
        print(event)

        body = unquote(event['body'])
        pull_request_webhooh_payload = json.loads(body[8:])
        pull_request = GitHubPullRequestFactory().create_pull_request(pull_request_webhooh_payload)
        PullRequestRepository().save_or_update_pull_request(pull_request)
        return make_response(200, "OK", {'Content-Type': 'application/json'})
    except Exception as e:
        print(traceback)
        return make_response(200, str(e), {'Content-Type': 'application/json'})
