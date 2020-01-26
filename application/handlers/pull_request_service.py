import json
import traceback
from urllib.parse import unquote

from application.utils import make_response
from config import GITHUB_ACCCESS_TOKEN
from domain.bitbucket import BitbucketClient
from domain.factory.pull_request_factory import BitBucketEventFactory, GitHubPullRequestFactory
from domain.github import GithubClient
from infrastructure.pull_request_repository import PullRequestRepository

pull_request_repository = PullRequestRepository()

# Use Github access token from config
access_token = GITHUB_ACCCESS_TOKEN


def github_pull_request_service(event, context):
    try:
        print(event)

        body = unquote(event['body'])
        pull_request_webhooh_payload = json.loads(body[8:])
        github_client = GithubClient(access_token)
        pull_request = GitHubPullRequestFactory(github_client).create_pull_request(pull_request_webhooh_payload)
        pull_request_repository.save_or_update_pull_request(pull_request)
        return make_response(200, "OK", {'Content-Type': 'application/json'})
    except Exception as e:
        traceback.print_exc()
        return make_response(500, str(e), {'Content-Type': 'application/json'})


def bitbucket_pull_request_service(event, context):
    try:
        print(event)

        body = unquote(event['body'])
        pull_request_webhooh_payload = json.loads(body[8:])
        bitbucket_client = BitbucketClient()
        pull_request = BitBucketEventFactory(bitbucket_client).create_pull_request(pull_request_webhooh_payload)
        pull_request_repository.save_or_update_pull_request(pull_request)
        return make_response(200, "OK", {'Content-Type': 'application/json'})
    except Exception as e:
        traceback.print_exc()
        return make_response(500, str(e), {'Content-Type': 'application/json'})
