from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.mysql import JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Many to Many relationship between branch and pull request
class PullRequestBranchAssociation(Base):
    __tablename__ = 'pull_request_branch_association'
    pull_request_id = Column(Integer, ForeignKey('pull_request.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('branch.id'), primary_key=True)
    branch_type = Column(VARCHAR(128))  # Source branch or target branch
    branch = relationship("Branch")


# Many to many relationship between branc and commit
class PullRequestCommitAssociation(Base):
    __tablename__ = 'pull_request_commit_association'
    pull_request_id = Column(Integer, ForeignKey('pull_request.id'), primary_key=True)
    commit_id = Column(Integer, ForeignKey('commit.id'), primary_key=True)
    commit = relationship("Commit")


class PullRequest(Base):
    __tablename__ = "pull_request"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    repository_url = Column("repository_url", VARCHAR(128), nullable=False)
    pull_request_id = Column("pull_request_id", Integer)
    title = Column("title", VARCHAR(128), nullable=False)
    action = Column("action", VARCHAR(128), nullable=False)
    commits_url = Column("commits_urls", VARCHAR(1024), nullable=False)
    merged_at = Column("merged_at", TIMESTAMP(timezone=False), nullable=True)
    created_at = Column("created_at", TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column("update_at", TIMESTAMP(timezone=False), nullable=False)
    closed_at = Column("closed_at", TIMESTAMP(timezone=False), nullable=True)
    merge_commit_sha = Column("merge_commit_sha", VARCHAR(255))
    no_of_review_comments = Column("no_of_review_comments", Integer)
    no_of_commits = Column("no_of_commits", Integer)
    lines_added = Column("lines_added", Integer)
    lines_removed = Column("lines_removed", Integer)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))
    sender_username = Column("sender_username", VARCHAR(128), nullable=False)
    sender_user_id = Column("sender_user_id", VARCHAR(128), nullable=False)

    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    # many  to many relationship
    branches = relationship("PullRequestBranchAssociation")
    commits = relationship("PullRequestCommitAssociation")

    __table_args__ = (UniqueConstraint('repository_url', 'pull_request_id', name='repo_pull_request_id_unique_key'),)


class Commit(Base):
    __tablename__ = "commit"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sha_id = Column("sha_id", VARCHAR(128), nullable=False)
    time = Column("time",TIMESTAMP(timezone=False), nullable=False)
    commiter_username = Column("commiter_username", VARCHAR(128), nullable=False)
    commiter_user_id = Column("commiter_user_id", VARCHAR(128), nullable=False)
    description = Column("description", VARCHAR(128), nullable=False)
    message = Column("message", VARCHAR(128), nullable=False)
    repository_url = Column("repository_url", VARCHAR(128), nullable=False)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    __table_args__ = (UniqueConstraint('repository_url', 'sha_id', name='commit_sha_unique_key'),)

class Branch(Base):
    __tablename__ = "branch"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(128), nullable=False)
    label = Column("label", VARCHAR(128), nullable=False)
    sha_id = Column("sha_id", VARCHAR(128), nullable=False)
    username = Column("username", VARCHAR(128), nullable=False)
    user_id = Column("user_id", VARCHAR(128), nullable=False)
    repository_url=  Column("repository_url", VARCHAR(128), nullable=False)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    __table_args__ = (UniqueConstraint('repository_url', 'name', name='branch_name_unique_key'),)


class BuildHistory(object):
    __tablename__ = "build_history"
    build_id = Column("branch_label", VARCHAR(128), nullable=False)
    repo_url = Column("branch_label", VARCHAR(128), nullable=False)
    status = Column("branch_label", VARCHAR(128), nullable=False)
    commit_id = Column("branch_label", VARCHAR(128), nullable=False)
    branch = Column("branch_label", VARCHAR(128), nullable=False)
