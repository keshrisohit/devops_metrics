import requests


class GithubClient(object):
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_commits(self, commit_url):
        # curl 'https://api.github.com/users/whatever?client_id=xxxx&client_secret=yyyy'
        if self.access_token:
            response = requests.get(commit_url,
                                    headers={
                                        'Authorization': 'Bearer {}'.format(
                                            self.access_token)}).json()

        else:
            try:
                reposne = requests.get(commit_url).json()
            except Exception as e:
                raise e

        return reposne
