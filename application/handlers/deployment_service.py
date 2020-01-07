import json
import traceback

import boto3

from domain.factory.deployment_factory import CodeBuildFactory
from infrastructure.deployment_repository import DeploymentRepository

deployment_repository = DeploymentRepository()



#TODO vinay to add testcases for code build service

def codebuild_service(event, context):
    client = boto3.client('codebuild')
    try:
        print(event)
        build_id = event.get('detail', {}).get('build-id')
        build_info = client.batch_get_builds(ids=[build_id])
        build_metrics = CodeBuildFactory().create_build_details(build_info)
        deployment_repository.save_build_metrics(build_metrics)
    except Exception as e:
        traceback.print_exc()
        raise e
