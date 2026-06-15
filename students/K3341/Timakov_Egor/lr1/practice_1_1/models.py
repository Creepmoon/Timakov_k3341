from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict


class SkillCategory(str, Enum):
  programming = "programming"
  design = "design"
  management = "management"


class Skill(BaseModel):
  id: int
  name: str
  description: str
  category: SkillCategory


class ProfilePreferences(BaseModel):
  id: int
  title: str
  description: str


class Profile(BaseModel):
  id: int
  name: str
  bio: str
  experience_years: int
  preferences: ProfilePreferences
  skills: Optional[List[Skill]] = []


class ProfileCreate(TypedDict):
  id: int
  name: str
  bio: str
  experience_years: int
  preferences: dict
  skills: list
