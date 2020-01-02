import json
import boto3
import traceback
from domain.factory.deployment_factory import CodeBuildFactory
from infrastructure.deployment_repository import DeploymentRepository

def codebuild_service(event, context):
    client = boto3.client('codebuild')
    try:
        print(event)
        build_id = json.loads(event).get('detail',{}).get('build-id')
        build_info = client.batch_get_builds(ids=[build_id])
        build_metrics = CodeBuildFactory().save_metrics(build_info)
        DeploymentRepository().save_build_metrics(build_metrics)
    except:
        print(traceback)
        raise e
