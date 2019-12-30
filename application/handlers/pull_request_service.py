import json
import traceback
from urllib.parse import unquote

from domain.factory.pull_request_factory import GitHubPullRequestFactory
from infrastructure.pull_request_repository import PullRequestRepository


def github_pull_request_service(event, context):
    try:
        print(event)

        body=unquote(event['body'])
        pull_request_webhooh_payload = json.loads(body[8:])
        pull_request = GitHubPullRequestFactory().create_pull_request(pull_request_webhooh_payload)
        PullRequestRepository().save_or_update_pull_request(pull_request)
    except Exception as e:
        print(traceback)
        raise e
