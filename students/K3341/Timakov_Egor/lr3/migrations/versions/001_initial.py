"""initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-06-15

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    "user",
    sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("is_active", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
  op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)

  op.create_table(
    "skill",
    sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("category", sa.Enum("programming", "design", "management", "marketing", "other", name="skillcategory"), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
  )
  op.create_index(op.f("ix_skill_name"), "skill", ["name"], unique=True)

  op.create_table(
    "profile",
    sa.Column("bio", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("experience_years", sa.Integer(), nullable=False),
    sa.Column("interests", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("project_preferences", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("user_id"),
  )

  op.create_table(
    "project",
    sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("goals", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("requirements", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("expected_results", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("deadline", sa.DateTime(), nullable=True),
    sa.Column("status", sa.Enum("draft", "recruiting", "in_progress", "completed", "archived", name="projectstatus"), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("creator_id", sa.Integer(), nullable=False),
    sa.Column("created_at", sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(["creator_id"], ["user.id"]),
    sa.PrimaryKeyConstraint("id"),
  )

  op.create_table(
    "profileskilllink",
    sa.Column("profile_id", sa.Integer(), nullable=False),
    sa.Column("skill_id", sa.Integer(), nullable=False),
    sa.Column("proficiency_level", sa.Enum("beginner", "intermediate", "advanced", "expert", name="proficiencylevel"), nullable=False),
    sa.ForeignKeyConstraint(["profile_id"], ["profile.id"]),
    sa.ForeignKeyConstraint(["skill_id"], ["skill.id"]),
    sa.PrimaryKeyConstraint("profile_id", "skill_id"),
  )

  op.create_table(
    "team",
    sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("project_id", sa.Integer(), nullable=False),
    sa.Column("created_at", sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
    sa.PrimaryKeyConstraint("id"),
  )

  op.create_table(
    "task",
    sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column("deadline", sa.DateTime(), nullable=True),
    sa.Column("status", sa.Enum("todo", "in_progress", "review", "done", name="taskstatus"), nullable=False),
    sa.Column("progress", sa.Integer(), nullable=False),
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("project_id", sa.Integer(), nullable=False),
    sa.Column("assignee_id", sa.Integer(), nullable=True),
    sa.Column("created_at", sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(["assignee_id"], ["user.id"]),
    sa.ForeignKeyConstraint(["project_id"], ["project.id"]),
    sa.PrimaryKeyConstraint("id"),
  )

  op.create_table(
    "teammember",
    sa.Column("team_id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("role", sa.Enum("lead", "developer", "designer", "manager", "member", name="teamrole"), nullable=False),
    sa.Column("joined_at", sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(["team_id"], ["team.id"]),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    sa.PrimaryKeyConstraint("team_id", "user_id"),
  )


def downgrade() -> None:
  op.drop_table("teammember")
  op.drop_table("task")
  op.drop_table("team")
  op.drop_table("profileskilllink")
  op.drop_table("project")
  op.drop_table("profile")
  op.drop_index(op.f("ix_skill_name"), table_name="skill")
  op.drop_table("skill")
  op.drop_index(op.f("ix_user_username"), table_name="user")
  op.drop_index(op.f("ix_user_email"), table_name="user")
  op.drop_table("user")
  op.execute("DROP TYPE IF EXISTS teamrole")
  op.execute("DROP TYPE IF EXISTS taskstatus")
  op.execute("DROP TYPE IF EXISTS proficiencylevel")
  op.execute("DROP TYPE IF EXISTS projectstatus")
  op.execute("DROP TYPE IF EXISTS skillcategory")
