from domain.entities import PullRequest, Branch, Commit
import requests


class EventFactory(object):
    def create_pull_request(self, event):
        pass


class GitHubPullRequestFactory(EventFactory):

    def create_pull_request(self, event):
        repository_url = event["repository"]["html_url"]
        pull_request_id = event["number"]

        source_branch = self.parse_branch(event["pull_request"]["head"])
        target_branch = self.parse_branch(event["pull_request"]["base"])
        title = event["pull_request"]["title"]
        reviewers = None
        sender_name = event["pull_request"]["user"]["login"]
        sender_id = event["pull_request"]["user"]["id"]
        action = event["action"]
        merged_at = event["pull_request"]["merged_at"]
        created_at = event["pull_request"]["created_at"]
        updated_at = event["pull_request"]["updated_at"]
        closed_at = event["pull_request"]["closed_at"]
        merge_commit_sha = event["pull_request"]["merge_commit_sha"]
        commits_url = event["pull_request"]["commits_url"]

        review_comments = event["pull_request"]["review_comments"]
        no_of_commits = event["pull_request"]["commits"]
        no_of_files_changed = event["pull_request"]["changed_files"]
        lines_added = event["pull_request"]["additions"]
        lines_removed = event["pull_request"]["deletions"]
        commits = self.get_commits(commits_url)

        pull_request = PullRequest(repository_url, pull_request_id, commits, source_branch, target_branch, title,
                                   reviewers, sender_name, sender_id, action, commits_url, merged_at, created_at,
                                   updated_at, closed_at, merge_commit_sha, review_comments, no_of_commits,
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
        commits_response = requests.get(commit_url).json()
        for commit in commits_response:
            sha_id = commit["sha"]
            commit_time = commit["commit"]["committer"]["date"]
            commiter = commit["commit"]["committer"]["name"]
            description = commit["commit"]["message"]
            commiter_id = commit["committer"]["id"]
            message = commit["commit"]["message"]
            repository_url = commit["url"]
            c = Commit(sha_id, commit_time, commiter, commiter_id, description, message, repository_url)
            commits.append(c)

        return commits


class BitBucketEventFactory(EventFactory):

    def create_pull_request(self, event):
        pass
