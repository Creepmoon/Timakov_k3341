from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from app.models.profile import Profile
  from app.models.project import Project, Task
  from app.models.team import TeamMember


class UserBase(SQLModel):
  email: str = Field(unique=True, index=True)
  username: str = Field(unique=True, index=True)


class User(UserBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  hashed_password: str
  is_active: bool = Field(default=True)
  created_at: datetime = Field(default_factory=datetime.utcnow)

  profile: Optional["Profile"] = Relationship(back_populates="user")
  created_projects: List["Project"] = Relationship(back_populates="creator")
  team_memberships: List["TeamMember"] = Relationship(back_populates="user")
  assigned_tasks: List["Task"] = Relationship(back_populates="assignee")


class UserCreate(UserBase):
  password: str


class UserRead(UserBase):
  id: int
  is_active: bool
  created_at: datetime


class UserUpdate(SQLModel):
  email: Optional[str] = None
  username: Optional[str] = None


class PasswordChange(SQLModel):
  current_password: str
  new_password: str
