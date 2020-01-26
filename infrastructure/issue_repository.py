from infrastructure.base_repository import BaseRepository
from infrastructure.data_mappers import issue_db_from_entity
from infrastructure.models import Issues


class IssueRepository(BaseRepository):
    def save_issue(self, issue):
        issue_db = issue_db_from_entity(issue)
        self.add_item(issue_db)
        self.session.commit()

    def get_issue(self, issue_id):
        issues = self.session.query(Issues).filter(
            Issues.issue_id == issue_id).all()

        return issues
