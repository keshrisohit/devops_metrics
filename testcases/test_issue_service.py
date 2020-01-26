import unittest

from application.handlers.issue_service import create_issue
from infrastructure.issue_repository import IssueRepository
from infrastructure.models import Issues
from infrastructure.pull_request_repository import PullRequestRepository


class TestIssueService(unittest.TestCase):

    def setUp(self):
        self.issue_repo = IssueRepository()

    def test_issue(self):
        data = {"body": """{
            \"issue_id\": \"abc\", \"start_time\": \"2019-05-15T15:20:30Z\", \"end_time\": \"2019-05-15T15:20:30Z\", \"title\": \"def\", \"description\": \"asdsa\", \"sev\": \"sda\",
            \"reported_by\": \"sdas\"
        }"""
                }

        create_issue(data, "")
        issue_repo = IssueRepository()
        issue = issue_repo.get_issue("abc")

        assert issue[0].issue_id == "abc"
        assert issue[0].sev == "sda"
        assert issue[0].title == "def"

    def tearDown(self):
        self.issue_repo.session.query(Issues).delete()
