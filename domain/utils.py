import requests


def get_access_token(client_id, client_secret, token_url):
    data = {'grant_type': 'client_credentials'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False,
                                          auth=(client_id, client_secret))
    return access_token_response.json()['access_token']
