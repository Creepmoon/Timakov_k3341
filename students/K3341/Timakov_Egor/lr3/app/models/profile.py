from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from app.models.user import User


class SkillCategory(str, Enum):
  programming = "programming"
  design = "design"
  management = "management"
  marketing = "marketing"
  other = "other"


class SkillBase(SQLModel):
  name: str = Field(unique=True, index=True)
  description: str
  category: SkillCategory = SkillCategory.other


class Skill(SkillBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  profiles: List["ProfileSkillLink"] = Relationship(back_populates="skill")


class SkillCreate(SkillBase):
  pass


class SkillUpdate(SQLModel):
  name: Optional[str] = None
  description: Optional[str] = None
  category: Optional[SkillCategory] = None


class ProficiencyLevel(str, Enum):
  beginner = "beginner"
  intermediate = "intermediate"
  advanced = "advanced"
  expert = "expert"


class ProfileBase(SQLModel):
  bio: str = ""
  experience_years: int = Field(default=0, ge=0)
  interests: str = ""
  project_preferences: str = ""


class Profile(ProfileBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  user_id: int = Field(foreign_key="user.id", unique=True)

  user: Optional["User"] = Relationship(back_populates="profile")
  skills: List["ProfileSkillLink"] = Relationship(back_populates="profile")


class ProfileCreate(ProfileBase):
  user_id: int


class ProfileUpdate(SQLModel):
  bio: Optional[str] = None
  experience_years: Optional[int] = Field(default=None, ge=0)
  interests: Optional[str] = None
  project_preferences: Optional[str] = None


class ProfileSkillLink(SQLModel, table=True):
  """Ассоциативная сущность Profile <-> Skill с полем proficiency_level."""

  profile_id: Optional[int] = Field(default=None, foreign_key="profile.id", primary_key=True)
  skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
  proficiency_level: ProficiencyLevel = Field(default=ProficiencyLevel.beginner)

  profile: Optional[Profile] = Relationship(back_populates="skills")
  skill: Optional[Skill] = Relationship(back_populates="profiles")


class ProfileSkillLinkCreate(SQLModel):
  profile_id: int
  skill_id: int
  proficiency_level: ProficiencyLevel = ProficiencyLevel.beginner


class ProfileSkillLinkUpdate(SQLModel):
  proficiency_level: Optional[ProficiencyLevel] = None
