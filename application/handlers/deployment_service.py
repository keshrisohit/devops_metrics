import json
import traceback

import boto3

from application.utils import make_response
from domain.factory.deployment_factory import BudilDetailRequestFactory, CodeBuildFactory
from infrastructure.deployment_repository import DeploymentRepository

deployment_repository = DeploymentRepository()


def codebuild_service(event, context):
    client = boto3.client('codebuild')
    try:
        build_id = event.get('detail', {}).get('build-id')
        build_info = client.batch_get_builds(ids=[build_id])
        print(build_info)
        build_metrics = CodeBuildFactory().create_build_details(build_info)
        deployment_repository.save_build_metrics(build_metrics)
    except Exception as e:
        traceback.print_exc()
        raise e


def build_detail_service(event, context):
    build_details = BudilDetailRequestFactory().create_build_details(json.loads(event['body']))
    deployment_repository.save_build_metrics(build_details)
    return make_response(200, "OK", {'Content-Type': 'application/json'})
