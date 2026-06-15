from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from app.models.team import Team
  from app.models.user import User


class ProjectStatus(str, Enum):
  draft = "draft"
  recruiting = "recruiting"
  in_progress = "in_progress"
  completed = "completed"
  archived = "archived"


class TaskStatus(str, Enum):
  todo = "todo"
  in_progress = "in_progress"
  review = "review"
  done = "done"


class ProjectBase(SQLModel):
  title: str
  description: str
  goals: str
  requirements: str
  expected_results: str
  deadline: Optional[datetime] = None
  status: ProjectStatus = ProjectStatus.draft


class Project(ProjectBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  creator_id: int = Field(foreign_key="user.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  creator: Optional["User"] = Relationship(back_populates="created_projects")
  teams: List["Team"] = Relationship(back_populates="project")  # noqa: F821
  tasks: List["Task"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
  creator_id: int


class ProjectUpdate(SQLModel):
  title: Optional[str] = None
  description: Optional[str] = None
  goals: Optional[str] = None
  requirements: Optional[str] = None
  expected_results: Optional[str] = None
  deadline: Optional[datetime] = None
  status: Optional[ProjectStatus] = None


class TaskBase(SQLModel):
  title: str
  description: str
  deadline: Optional[datetime] = None
  status: TaskStatus = TaskStatus.todo
  progress: int = Field(default=0, ge=0, le=100)


class Task(TaskBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  project_id: int = Field(foreign_key="project.id")
  assignee_id: Optional[int] = Field(default=None, foreign_key="user.id")
  created_at: datetime = Field(default_factory=datetime.utcnow)

  project: Optional[Project] = Relationship(back_populates="tasks")
  assignee: Optional["User"] = Relationship(back_populates="assigned_tasks")


class TaskCreate(TaskBase):
  project_id: int
  assignee_id: Optional[int] = None


class TaskUpdate(SQLModel):
  title: Optional[str] = None
  description: Optional[str] = None
  deadline: Optional[datetime] = None
  status: Optional[TaskStatus] = None
  progress: Optional[int] = Field(default=None, ge=0, le=100)
  assignee_id: Optional[int] = None
