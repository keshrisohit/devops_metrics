from sqlalchemy import BOOLEAN, Column, ForeignKey, Integer, String, UniqueConstraint, VARCHAR
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Many to Many relationship between branch and pull request
class PullRequestBranchAssociationDBModel(Base):
    __tablename__ = 'pull_request_branch_association'
    pull_request_id = Column(Integer, ForeignKey('pull_request.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('branch.id'), primary_key=True)
    branch_type = Column(VARCHAR(128))  # Source branch or target branch
    branch = relationship("BranchDBModel")


# Many to many relationship between branc and commit
class PullRequestCommitAssociationDBModel(Base):
    __tablename__ = 'pull_request_commit_association'
    pull_request_id = Column(Integer, ForeignKey('pull_request.id'), primary_key=True)
    commit_id = Column(Integer, ForeignKey('commit.id'), primary_key=True)
    commit = relationship("CommitDBModel")


class PullRequestDBModel(Base):
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
    no_of_comments = Column("no_of_comments", Integer)
    no_of_commits = Column("no_of_commits", Integer)
    no_of_files_changed = Column("no_of_files_changed", Integer)
    lines_added = Column("lines_added", Integer)
    lines_removed = Column("lines_removed", Integer)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))
    sender_username = Column("sender_username", VARCHAR(128), nullable=False)
    sender_user_id = Column("sender_user_id", VARCHAR(128), nullable=False)

    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    # many  to many relationship
    branches = relationship("PullRequestBranchAssociationDBModel")
    commits = relationship("PullRequestCommitAssociationDBModel")
    participants = relationship("PullRequestParticipantDBModel")

    __table_args__ = (UniqueConstraint('repository_url', 'pull_request_id', name='repo_pull_request_id_unique_key'),)


class CommitDBModel(Base):
    __tablename__ = "commit"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sha_id = Column("sha_id", VARCHAR(128), nullable=False)
    time = Column("time", TIMESTAMP(timezone=False), nullable=False)
    commiter_username = Column("commiter_username", VARCHAR(128), nullable=False)
    commiter_user_id = Column("commiter_user_id", VARCHAR(128), nullable=False)
    description = Column("description", VARCHAR(128), nullable=False)
    message = Column("message", VARCHAR(128), nullable=False)
    repository_url = Column("repository_url", VARCHAR(128), nullable=False)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    __table_args__ = (UniqueConstraint('repository_url', 'sha_id', name='commit_sha_unique_key'),)


class BranchDBModel(Base):
    __tablename__ = "branch"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", VARCHAR(128), nullable=False)
    label = Column("label", VARCHAR(128), nullable=False)
    sha_id = Column("sha_id", VARCHAR(128), nullable=False)
    username = Column("username", VARCHAR(128), nullable=False)
    user_id = Column("user_id", VARCHAR(128), nullable=False)
    repository_url = Column("repository_url", VARCHAR(128), nullable=False)
    row_created_at = Column("row_created_at", TIMESTAMP(timezone=False))
    row_updated_at = Column("row_updated_at", TIMESTAMP(timezone=False))

    __table_args__ = (UniqueConstraint('repository_url', 'name', name='branch_name_unique_key'),)


class BuildDetailsModels(Base):
    __tablename__ = "build_details"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    build_id = Column("build_id", VARCHAR(128), nullable=False)
    project_name = Column("project_name", VARCHAR(128), nullable=False)
    source_type = Column("source_type", VARCHAR(128), nullable=True)
    source_location = Column("source_location", VARCHAR(128), nullable=True)
    branch_name = Column("branch_name", VARCHAR(128), nullable=True)
    commit_id = Column("commit_id", VARCHAR(256), nullable=True)
    start_time = Column("start_time", TIMESTAMP(timezone=False), nullable=False)
    end_time = Column("end_time", TIMESTAMP(timezone=False), nullable=False)
    status = Column("status", VARCHAR(128),nullable=True)

    __table_args__ = (UniqueConstraint('build_id', 'project_name', 'source_type', name='build_details_unique_key'),)


class PullRequestParticipantDBModel(Base):
    __tablename__ = "pull_request_participant"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column('username', String)
    display_name = Column('display_name', String)
    role = Column('role', String)
    participated_on = Column('participated_on', TIMESTAMP(timezone=False),
                             nullable=True)  # if patricipated in PR review
    approved = Column('approved', BOOLEAN)  # true  if PR is approved
    pull_request_id = Column(Integer, ForeignKey('pull_request.id'))


class Issues(Base):
    __tablename__ = "issues"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    issue_id = Column('issue_id', VARCHAR(128))
    title = Column('title', VARCHAR(128))
    description = Column('description', String)
    reported_by = Column('reported_by', String)
    sev = Column('sev', String)
    start_time = Column('start_time', TIMESTAMP(timezone=False))


    end_time = Column('end_time', TIMESTAMP(timezone=False))
