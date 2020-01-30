import os

BITBUCKET_CLIENT_ID = os.getenv('BITBUCKET_CLIENT_ID', "")
BITBUCKET_SECRET_KEY = os.getenv('BITBUCKET_SECRET_KEY', "")
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN', "")
DB_URL = os.getenv('DB_URL', "mysql+pymysql://root:password@localhost/metrics")



