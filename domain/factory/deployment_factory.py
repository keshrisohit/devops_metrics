from domain.entities import BuildDetails


class DeploymentFactory(object):
    def create_build_details(self, metrics):
        pass


class CodeBuildFactory(DeploymentFactory):

    def create_build_details(self, metrics):
        build_id = metrics.get('builds', {})[0].get('id')
        project_name = metrics.get('builds', {})[0].get('projectName')
        source_type = metrics.get('builds', {})[0].get('source').get('type')
        source_location = metrics.get('builds', {})[0].get('source').get('location')
        branch_name = metrics.get('builds', {})[0].get('sourceVersion')
        commit_id = metrics.get('builds', {})[0].get('resolvedSourceVersion')
        start_time = metrics.get('builds', {})[0].get('startTime')
        end_time = metrics.get('builds', {})[0].get('endTime')
        status = "SUCCESS"

        build_details = BuildDetails(build_id, project_name, source_type, source_location,
                                     branch_name, commit_id, start_time, end_time, status)

        return build_details


class BudilDetailRequestFactory(DeploymentFactory):

    def create_build_details(self, payload):
        build_id = payload.get('build_id')
        project_name = payload.get('project_name')
        source_type = payload.get('source_type')
        source_location = payload.get('source_location')
        branch_name = payload.get('branch_name')
        commit_id = payload.get('commit_id')
        start_time = payload.get('start_time')
        end_time = payload.get('end_time')
        status = payload.get('status')

        build_details = BuildDetails(build_id, project_name, source_type, source_location,
                                     branch_name, commit_id, start_time, end_time, status)

        return build_details
