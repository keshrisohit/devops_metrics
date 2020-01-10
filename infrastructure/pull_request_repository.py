from datetime import datetime

from infrastructure.base_repository import BaseRepository
from infrastructure.data_mappers import branch_entites_to_model, commit_entites_to_model, \
    pull_request_entities_to_model, pull_request_particpants_entity_to_model, set_branch_db_from_entity, \
    set_commit_db_from_entity, set_pull_request_db_from_entity, set_pull_request_participant_db_from_entity
from infrastructure.models import BranchDBModel, PullRequestBranchAssociationDBModel, \
    PullRequestCommitAssociationDBModel, PullRequestDBModel


class PullRequestRepository(BaseRepository):

    def get_pull_requests(self, pull_request_id, repository_url):
        pull_requests = self.session.query(PullRequestDBModel).filter(
            PullRequestDBModel.pull_request_id == pull_request_id) \
            .filter(PullRequestDBModel.repository_url == repository_url).all()

        return pull_requests

    def update_pull_request(self, pull_request_db, pull_request):

        # update source and target branch

        for branch in pull_request_db.branches:
            if branch.branch_type == "SOURCE":
                set_branch_db_from_entity(branch.branch, pull_request.source_branch)
            elif branch.branch_type == "TARGET":
                set_branch_db_from_entity(branch.branch, pull_request.target_branch)

        # Optimize this query
        for commit in pull_request.commits:
            found = False
            for pull_request_db_commit in pull_request_db.commits:
                db_commit = pull_request_db_commit.commit

                if commit.repository_url == db_commit.commit.repository_url and commit.sha_id == db_commit.sha_id:
                    set_commit_db_from_entity(db_commit, commit)
                    found = True
                    # We can ignore this assuming commits data will not change it will be always incremental
            if not found:
                pull_request_commit_association = PullRequestCommitAssociationDBModel()
                pull_request_commit_association.commit = commit_entites_to_model(commit)
                pull_request.commits.append(pull_request_commit_association)


        for participant in pull_request.participants:
            for participant_db in pull_request_db.participants:

                if participant_db.username == participant.user_id and participant_db.role == participant.role:
                    found = True
                    set_pull_request_participant_db_from_entity(participant_db, participant)

            if not found:
                pull_request_db.participants.append(pull_request_particpants_entity_to_model(participant))

        set_pull_request_db_from_entity(pull_request_db, pull_request, pull_request_db.row_created_at,
                                        datetime.now())

    def create_pull_request(self, pull_request):
        pull_request_db = pull_request_entities_to_model(pull_request)

        source_branch = self.session.query(BranchDBModel).filter(
            BranchDBModel.name == pull_request.source_branch.branch_name).filter(
            BranchDBModel.repository_url == pull_request.source_branch.repository_url).all()
        target_branch = self.session.query(BranchDBModel).filter(
            BranchDBModel.name == pull_request.target_branch.branch_name).filter(
            BranchDBModel.repository_url == pull_request.target_branch.repository_url).all()
        if len(source_branch) > 0:
            set_branch_db_from_entity(source_branch[0], pull_request.source_branch)
            source_branch = source_branch[0]
        else:
            source_branch = branch_entites_to_model(pull_request.source_branch)
        if len(target_branch) > 0:
            set_branch_db_from_entity(target_branch[0], pull_request.target_branch)
            target_branch = target_branch[0]
        else:
            target_branch = branch_entites_to_model(pull_request.target_branch)

        for commit in pull_request.commits:
            commit_db = commit_entites_to_model(commit)
            pull_request_commit_association = PullRequestCommitAssociationDBModel()
            pull_request_commit_association.commit = commit_db
            pull_request_db.commits.append(pull_request_commit_association)

        for pull_request_participant in pull_request.participants:
            pull_request_participant_db = pull_request_particpants_entity_to_model(pull_request_participant)
            pull_request_db.participants.append(pull_request_participant_db)

        pull_request_source_branch_association = PullRequestBranchAssociationDBModel(branch_type="SOURCE")
        pull_request_target_branch_association = PullRequestBranchAssociationDBModel(branch_type="TARGET")
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
            self.update_pull_request(pull_requests_db[0], pull_request)
        else:
            self.create_pull_request(pull_request)
        self.session.commit()
