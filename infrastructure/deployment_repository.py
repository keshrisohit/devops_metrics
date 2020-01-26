from infrastructure.base_repository import BaseRepository
from infrastructure.data_mappers import build_details_entities_to_model
from infrastructure.models import BuildDetailsModels


class DeploymentRepository(BaseRepository):
    def save_build_metrics(self, build_metrics):
        build_metrics_db = build_details_entities_to_model(build_metrics)
        self.add_item(build_metrics_db)

    def get_build_details(self, build_id):
        build_details = self.session.query(BuildDetailsModels).filter(
            BuildDetailsModels.build_id == build_id).all()

        return build_details
