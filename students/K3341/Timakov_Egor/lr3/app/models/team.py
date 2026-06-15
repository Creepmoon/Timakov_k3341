from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from app.models.project import Project
  from app.models.user import User


class TeamRole(str, Enum):
  lead = "lead"
  developer = "developer"
  designer = "designer"
  manager = "manager"
  member = "member"


class TeamBase(SQLModel):
  name: str
  description: str


class Team(TeamBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  project_id: int = Field(foreign_key="project.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  project: Optional["Project"] = Relationship(back_populates="teams")
  members: List["TeamMember"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
  project_id: int


class TeamUpdate(SQLModel):
  name: Optional[str] = None
  description: Optional[str] = None


class TeamMember(SQLModel, table=True):
  """Ассоциативная сущность User <-> Team с полем role."""

  team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
  user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
  role: TeamRole = Field(default=TeamRole.member)
  joined_at: datetime = Field(default_factory=datetime.utcnow)

  team: Optional[Team] = Relationship(back_populates="members")
  user: Optional["User"] = Relationship(back_populates="team_memberships")


class TeamMemberCreate(SQLModel):
  team_id: int
  user_id: int
  role: TeamRole = TeamRole.member


class TeamMemberUpdate(SQLModel):
  role: Optional[TeamRole] = None
