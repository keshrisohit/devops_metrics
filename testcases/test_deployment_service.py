import unittest

from application.handlers.deployment_service import build_detail_service
from infrastructure.deployment_repository import DeploymentRepository
from infrastructure.models import BuildDetailsModels
from infrastructure.pull_request_repository import PullRequestRepository


class TestDeploymentDetails(unittest.TestCase):

    def setUp(self):
        self.deployment_repo = DeploymentRepository()






    def test_build_details(self):
        data ={
            "body": """{
                \"build_id\": \"sss\",
                \"project_name\": \"ssss\",
                \"source_type\": \"xccc\",
                \"source_location\": \"loc\",
                \"branch_name\": \"branch\",
                \"commit_id\": \"123\",
                \"start_time\": \"2019-05-15T15:20:30Z\",
                \"end_time\": \"2019-05-15T15:20:30Z\",
                \"status\": \"123\"
            }"""
        }

        build_detail_service(data,"")
        deployment_repo = DeploymentRepository()
        build_details=deployment_repo.get_build_details('sss')

        assert build_details[0].branch_name == 'branch'
        assert build_details[0].commit_id == '123'
        assert build_details[0].project_name == 'ssss'
        assert build_details[0].source_location == 'loc'
        assert build_details[0].source_type == 'xccc'


    def tearDown(self):
        self.deployment_repo.session.query(BuildDetailsModels).delete()
