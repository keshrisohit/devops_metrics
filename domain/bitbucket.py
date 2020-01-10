import requests
from config import BITBUCKET_CLIENT_ID, BITBUCKET_SECRET_KEY

from domain.utils import get_access_token

client_id = BITBUCKET_CLIENT_ID
client_secret = BITBUCKET_SECRET_KEY
token_url = "https://bitbucket.org/site/oauth2/access_token"


class BitbucketClient(object):
    def __init__(self, access_token=None):
        self.access_token = access_token
        if not self.access_token:
            self.access_token = get_access_token(client_id, client_secret, token_url)

    def pull_request_commit_list(self, commit_url):

        _next = commit_url
        commits_list = []

        while True:
            values, _next = self._get_pull_request_commits(_next)
            commits_list.extend(values)

            if not _next:
                break

        return commits_list

    def _get_pull_request_commits(self, commits_url):

        next = None
        values = []
        try:
            response = self.call(commits_url)

            response_data = response.json()
            if 'next' in response_data:
                next = response_data['next']

            values = response.json()['values']

        except Exception as e:
            print(e)

        return values, next

    def _get_pull_request_diff_count(self, url):
        lines_added = 0
        lines_removed = 0
        files_changed = 0
        diff_stat_url = '{}{}'.format(url, 'stat')

        try:
            response = self.call(diff_stat_url)

            next = None
            response_data = response.json()
            if 'next' in response_data:
                next = response['next']

            values = response.json()['values']
            for value in values:
                lines_removed += value['lines_removed']
                files_changed += 1
                lines_added += value['lines_added']
        except Exception as e:
            print(e)
        return lines_added, lines_removed, next, files_changed

    def traverse_diff_count(self, url):

        _next = url
        while True:
            lines_added, lines_removed, _next, files_changed = self._get_pull_request_diff_count(
                _next)
            yield lines_added, lines_removed, files_changed
            if not _next:
                break

    def call(self, url):

        response = None
        try:
            response = requests.get(url, headers={'Authorization': 'Bearer {}'.format(self.access_token)})

            if response.status_code == 401:
                # access token  might have expired
                self.access_token = get_access_token(client_id, client_secret, token_url)
                self.call(url)

        except Exception as e:
            print(e)
        return response
