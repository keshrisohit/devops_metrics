import os

BITBUCKET_CLIENT_ID = os.getenv('BITBUCKET_CLIENT_ID', "")
BITBUCKET_SECRET_KEY = os.getenv('BITBUCKET_SECRET_KEY', "")
GITHUB_ACCCESS_TOKEN = os.getenv('GITHUB_ACCCESS_TOKEN', "")
DB_URL = os.getenv('DB_URL', "sqlite:///metrics.db")
