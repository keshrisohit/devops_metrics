from enum import Enum

import requests

from domain.entities import Branch, Commit, PullRequest, PullRequestParticipant


class PRStatus(Enum):
    OPEN = "OPENED"
    DECLINED = "DECLINED"
    MERGED = "MERGED"


class EventFactory(object):
    def create_pull_request(self, event):
        pass


class GitHubPullRequestFactory(EventFactory):


    def __init__(self, github_client):
        self.github_client = github_client

    def create_pull_request(self, event):
        repository_url = event["repository"]["html_url"]
        pull_request_id = event["number"]

        source_branch = self.parse_branch(event["pull_request"]["head"])
        target_branch = self.parse_branch(event["pull_request"]["base"])
        title = event["pull_request"]["title"]
        participants = []
        sender_username = event["pull_request"]["user"]["login"]
        sender_id = event["pull_request"]["user"]["id"]
        action = event["action"]
        merged_at = event["pull_request"]["merged_at"]
        created_at = event["pull_request"]["created_at"]
        updated_at = event["pull_request"]["updated_at"]
        closed_at = event["pull_request"]["closed_at"]
        merge_commit_sha = event["pull_request"]["merge_commit_sha"]
        commits_url = event["pull_request"]["commits_url"]

        review_comments = event["pull_request"]["review_comments"]
        comments=event["pull_request"]["comments"]
        no_of_commits = event["pull_request"]["commits"]
        no_of_files_changed = event["pull_request"]["changed_files"]
        lines_added = event["pull_request"]["additions"]
        lines_removed = event["pull_request"]["deletions"]
        commits = self.get_commits(commits_url)

        # assigned, unassigned, review_requested, review_request_removed, labeled, unlabeled, opened, edited, closed, ready_for_review, locked, unlocked, or reopened. If the action is closed and the merged key is fals

        if action == "closed" and event["pull_request"]["merged"]:
            action == PRStatus.MERGED.value
        elif action == "closed":
            action = PRStatus.DECLINED.value
        else:
            action = PRStatus.OPEN.value

        pull_request = PullRequest(repository_url, pull_request_id, commits, source_branch, target_branch, title,
                                   participants, sender_username, sender_id, action, commits_url, merged_at, created_at,
                                   updated_at, closed_at, merge_commit_sha, review_comments, comments,no_of_commits,
                                   no_of_files_changed, lines_added, lines_removed)

        return pull_request

    def parse_branch(self, branch_details):
        branch_name = branch_details["ref"]
        branch_user = branch_details["user"]["login"]
        branch_label = branch_details["label"]
        branch_user_id = branch_details["user"]["id"]
        sha_id = branch_details["sha"]
        repository_url = branch_details["repo"]["html_url"]

        branch = Branch(branch_name, branch_user, branch_label, branch_user_id, sha_id, repository_url)
        return branch

    def get_commits(self, commit_url):
        commits = []
        # TODO Use github client for private repo
        commits_response = self.github_client.get_commits(commit_url)
        for commit in commits_response:
            sha_id = commit["sha"]
            commit_time = commit["commit"]["committer"]["date"]
            commiter = commit["commit"]["committer"]["name"]
            description = commit["commit"]["message"]
            commiter_id = commit["committer"]["id"]
            message = commit["commit"]["message"]
            repository_url = commit["url"].rsplit('/', 1)[0]
            c = Commit(sha_id, commit_time, commiter, commiter_id, description, message, repository_url)
            commits.append(c)

        return commits


class BitBucketEventFactory(EventFactory):

    def __init__(self, bitbucket_client):
        self.bitbucket_client = bitbucket_client

    def populate_pull_request_diff_count(self, diff_url):

        total_lines_added = 0
        total_lines_removed = 0
        total_no_of_files_changed = 0
        try:

            for lines_added, lines_removed, no_of_files_changed in self.bitbucket_client.traverse_diff_count(
                    diff_url):
                total_lines_added += lines_added
                total_lines_removed += lines_removed
                total_no_of_files_changed += no_of_files_changed

        except Exception as e:
            print('Error while processing diff url %s  , %s', diff_url, e)

        return total_lines_added, total_lines_removed, total_no_of_files_changed

    def _parse_commit_entity(self, commit_list):
        # logger.info('parsing commit %s for uid %s',commit_value,pull_request_entity_uid)
        commits = []
        for commit in commit_list:
            commiter_id = commit['author']['user']['username']
            commiter = commit['author']['user']['display_name']
            commit_time = commit['date']
            sha_id = commit['hash']
            message = commit['message']
            repository_url = commit['repository']['links']['html']['href']
            c = Commit(sha_id, commit_time, commiter, commiter_id, message, message, repository_url)
            commits.append(c)

        return commits

    def parse_pull_request_participants_entities(self, data):

        if 'participants' in data:
            pull_request_participants = data['participants']
        else:
            return []

        pull_request_participants_entity = []
        for pull_request_participant in pull_request_participants:

            username = pull_request_participant['user']['username']
            role = pull_request_participant['role']
            approved = bool(pull_request_participant['approved'])
            participated_on = None
            if 'participated_on' in pull_request_participant and pull_request_participant['participated_on']:
                participated_on = pull_request_participant['participated_on']
            display_name = pull_request_participant['user']['display_name']
            pull_request_participant_entity = PullRequestParticipant(display_name, username, role, participated_on,
                                                                     approved)
            pull_request_participants_entity.append(pull_request_participant_entity)

        return pull_request_participants_entity

    def parse_branch(self, branch_details):
        branch_name = branch_details["branch"]['name']
        branch_user = "biitbucket_user"
        branch_label = branch_details["repository"]["full_name"]
        branch_user_id = "biitbucket_user"
        sha_id = branch_details["commit"]["hash"]
        repository_url = branch_details["repository"]["links"]["html"]["href"]

        branch = Branch(branch_name, branch_user, branch_label, branch_user_id, sha_id, repository_url)
        return branch

    def parse_pull_request_entity(self, data):

        commit_list = self.bitbucket_client.pull_request_commit_list(data['links']['commits']['href'])
        repository_url = ""
        pull_request_id = data['id']
        commits = self._parse_commit_entity(commit_list)
        source_branch = self.parse_branch(data['source'])
        target_branch = self.parse_branch(data['destination'])
        title = data['title']
        participants = self.parse_pull_request_participants_entities(data)
        sender_username = data['author']['display_name']
        sender_id = data['author']['username']
        action = data['state']
        created_at = data['created_on']
        updated_at = data['updated_on']
        if data['state'] == 'MERGED':
            merged_at = data['updated_on']
        if data['state'] == 'DECLINED' or data['state'] == 'MERGED':
            closed_at = data['updated_on']
        merge_commit_sha = data['merge_commit']['hash']
        commits_url = data['links']['commits']['href']

        review_comments = data['comment_count']

        total_lines_added, total_lines_removed, total_no_of_files_changed = self.populate_pull_request_diff_count("")
        no_of_commits = len(commit_list)
        no_of_files_changed = total_no_of_files_changed
        lines_added = total_lines_added
        lines_removed = total_lines_removed
        description = data['description']

        pull_request = PullRequest(repository_url, pull_request_id, commits, source_branch, target_branch, title,
                                   participants, sender_username, sender_id, action, commits_url, merged_at, created_at,
                                   updated_at, closed_at, merge_commit_sha, review_comments, no_of_commits,
                                   no_of_files_changed, lines_added, lines_removed)
        return pull_request
