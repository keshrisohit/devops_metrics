from datetime import datetime

from infrastructure.base_repository import BaseRepository
from infrastructure.data_mappers import pull_request_entities_to_model, set_branch_db_from_entity, \
    set_commit_db_from_entity, commit_entites_to_model, branch_entites_to_model, set_pull_request_db_from_entity
from infrastructure.models import PullRequest, Branch, Commit, PullRequestCommitAssociation, \
    PullRequestBranchAssociation


class PullRequestRepository(BaseRepository):

    def get_pull_requests(self, pull_request_id, repository_url):
        pull_requests = self.session.query(PullRequest).filter(PullRequest.pull_request_id == pull_request_id) \
            .filter(PullRequest.repository_url == repository_url).all()

        return pull_requests

    def update_pull_request(self, pull_request_db, pull_request):

        # update source and target branch
        source_branch = self.session.query(Branch).filter(Branch.name == pull_request.source_branch.branch_name).filter(
            Branch.repository_url == pull_request.source_branch.repository_url).all()
        target_branch = self.session.query(Branch).filter(Branch.name == pull_request.target_branch.branch_name).filter(
            Branch.repository_url == pull_request.target_branch.repository_url).all()
        set_branch_db_from_entity(source_branch[0], pull_request.source_branch)
        set_branch_db_from_entity(target_branch[0], pull_request.target_branch)

        # update commits
        for commit in pull_request.commits:

            commit_db = self.session.query(Commit).filter(Commit.sha_id == commit.sha_id).filter(
                Commit.repository_url == commit.repository_url).all()

            if len(commit_db) > 0:
                set_commit_db_from_entity(commit_db[0], commit)
            else:
                pull_request_db.commits.append(commit_entites_to_model(commit))

    def create_pull_request(self, pull_request):
        pull_request_db = pull_request_entities_to_model(pull_request)

        source_branch = branch_entites_to_model(pull_request.source_branch)
        target_branch = branch_entites_to_model(pull_request.target_branch)

        pull_request_commit_associations = []
        for commit in pull_request.commits:
            commit_db = commit_entites_to_model(commit)
            pull_request_commit_association = PullRequestCommitAssociation()
            pull_request_commit_association.commit = commit_db
            pull_request_db.commits.append(pull_request_commit_association)

        pull_request_source_branch_association = PullRequestBranchAssociation(branch_type="SOURCE")
        pull_request_target_branch_association = PullRequestBranchAssociation(branch_type="TARGET")
        pull_request_source_branch_association.branch = source_branch
        pull_request_target_branch_association.branch = target_branch

        pull_request_db.branches.append(pull_request_source_branch_association)
        pull_request_db.branches.append(pull_request_target_branch_association)
        self.add_item(pull_request_db)

    def save_or_update_pull_request(self, pull_request):
        pull_request_id = pull_request.pull_request_id
        repository_url = pull_request.repository_url
        pull_requests_db = self.get_pull_requests(pull_request_id, repository_url)

        if len(pull_requests_db) > 0:
            # update source and target branch
            self.update_pull_request(pull_requests_db, pull_request)
        else:
            self.create_pull_request(pull_request)
        self.session.commit()
