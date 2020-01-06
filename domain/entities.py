class PullRequest(object):
    def __init__(self, repository_url, pull_request_id, commits, source_branch, target_branch, title, participants,
                 sender_username, sender_id, action, commits_url, merged_at, created_at, updated_at, closed_at,
                 merge_commit_sha, review_comments, no_of_commits, no_of_files_changed, lines_added, lines_removed,description=""):
        self.__repository_url = repository_url
        self.__pull_request_id = pull_request_id
        self.__commits = commits
        self.__source_branch = source_branch
        self.__target_branch = target_branch
        self.__title = title
        self.__participants = participants
        self.__sender_username = sender_username
        self.__sender_id = sender_id
        self.__action = action
        self.__commits_url = commits_url
        self.__merged_at = merged_at
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.__closed_at = closed_at
        self.__merge_commit_sha = merge_commit_sha
        self.__commits_url = commits_url

        self.__review_comments = review_comments
        self.__no_of_commits = no_of_commits
        self.__no_of_files_changed = no_of_files_changed
        self.__lines_added = lines_added
        self.__lines_removed = lines_removed
        self.__description=description
        #self.__merged_by

    @property
    def repository_url(self):
        return self.__repository_url

    @property
    def pull_request_id(self):
        return self.__pull_request_id

    @property
    def commits(self):
        return self.__commits

    @property
    def source_branch(self):
        return self.__source_branch

    @property
    def target_branch(self):
        return self.__target_branch

    @property
    def title(self):
        return self.__title

    @property
    def participants(self):
        return self.__participants

    @property
    def sender_username(self):
        self.__sender_username

    @property
    def sender_id(self):
        return self.__sender_id

    @property
    def action(self):
        return self.__action

    @property
    def commits_url(self):
        return self.__commits_url

    @property
    def merged_at(self):
        return self.__merged_at

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @property
    def closed_at(self):
        return self.__closed_at

    @property
    def merge_commit_sha(self):
        return self.__merge_commit_sha

    @property
    def commits_url(self):
        return self.__commits_url

    @property
    def review_comments(self):
        return self.__review_comments

    @property
    def no_of_commits(self):
        return self.__no_of_commits

    @property
    def no_of_files_changed(self):
        return self.__no_of_files_changed

    @property
    def lines_added(self):
        return self.__lines_added

    @property
    def lines_removed(self):
        return self.__lines_removed
    @property
    def description(self):
        return self.__description


class PullRequestParticipant(object):

    def __init__(self,  username=None,
                 user_id=None, role=None, participated_on=None,
                 approved=None):

        self.__username = username
        self.__user_id = user_id
        self.__role = role
        self.__participated_on = participated_on
        self.__approved = approved


    @property
    def username(self):
        return self.__username

    @property
    def user_id(self):
        return self.__user_id

    @property
    def role(self):
        return self.__role

    @property
    def participated_on(self):
        return self.__participated_on

    @property
    def approved(self):
        return self.__approved



class Branch(object):
    def __init__(self, branch_name, branch_user, branch_label, branch_user_id, sha_id, repository_url):
        self.__branch_name = branch_name
        self.__branch_user = branch_user
        self.__branch_label = branch_label
        self.__branch_user_id = branch_user_id
        self.__sha_id = sha_id
        self.__repository_url = repository_url

    @property
    def branch_name(self):
        return self.__branch_name

    @property
    def branch_user(self):
        return self.__branch_user

    @property
    def branch_label(self):
        return self.__branch_label

    @property
    def branch_user_id(self):
        return self.__branch_user_id

    @property
    def sha_id(self):
        return self.__sha_id

    @property
    def repository_url(self):
        return self.__repository_url


class Commit(object):

    def __init__(self, sha_id, commit_time, commiter, commiter_id, description, message, repository_url):
        self.__sha_id = sha_id
        self.__commit_time = commit_time
        self.__commiter = commiter
        self.__description = description
        self.__commiter_id = commiter_id
        self.__message = message
        self.__repository_url = repository_url

    @property
    def sha_id(self):
        return self.__sha_id

    @property
    def commit_time(self):
        return self.__commit_time

    @property
    def commiter(self):
        return self.__commiter

    @property
    def description(self):
        return self.__description

    @property
    def message(self):
        return self.__message

    @property
    def commiter_id(self):
        return self.__commiter_id

    @property
    def repository_url(self):
        return self.__repository_url


class BuildDetails(object):
    def __init__(self):
        pass


class Issue(object):
    def __init__(self):
        self.__start_time = ""
        self.__end_time = ""
        self.__title = ""
        self.__description = ""
        self.__sev = ""
        self.__reported_by = ""
