from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel

from app.models.profile import ProficiencyLevel, SkillCategory
from app.models.project import ProjectStatus, TaskStatus
from app.models.team import TeamRole


class SkillRead(SQLModel):
  id: int
  name: str
  description: str
  category: SkillCategory


class ProfileSkillRead(SQLModel):
  skill_id: int
  proficiency_level: ProficiencyLevel
  skill: Optional[SkillRead] = None


class UserBrief(SQLModel):
  id: int
  username: str
  email: str


class ProfileRead(SQLModel):
  id: int
  user_id: int
  bio: str
  experience_years: int
  interests: str
  project_preferences: str
  user: Optional[UserBrief] = None
  skills: List[ProfileSkillRead] = []


class TeamMemberRead(SQLModel):
  team_id: int
  user_id: int
  role: TeamRole
  joined_at: datetime
  user: Optional[UserBrief] = None


class TeamRead(SQLModel):
  id: int
  name: str
  description: str
  project_id: int
  created_at: datetime
  members: List[TeamMemberRead] = []


class TaskRead(SQLModel):
  id: int
  title: str
  description: str
  deadline: Optional[datetime]
  status: TaskStatus
  progress: int
  project_id: int
  assignee_id: Optional[int]
  created_at: datetime
  assignee: Optional[UserBrief] = None


class ProjectRead(SQLModel):
  id: int
  title: str
  description: str
  goals: str
  requirements: str
  expected_results: str
  deadline: Optional[datetime]
  status: ProjectStatus
  creator_id: int
  created_at: datetime
  creator: Optional[UserBrief] = None
  teams: List[TeamRead] = []
  tasks: List[TaskRead] = []


class Token(SQLModel):
  access_token: str
  token_type: str = "bearer"


class TokenData(SQLModel):
  sub: Optional[str] = None
