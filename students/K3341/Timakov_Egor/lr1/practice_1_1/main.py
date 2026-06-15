"""Практика 1.1 — базовое FastAPI-приложение с временной БД и Pydantic-моделями."""

from typing import List

from fastapi import FastAPI
from typing_extensions import TypedDict

from models import Profile, ProfileCreate, ProfilePreferences, Skill, SkillCategory

app = FastAPI(title="CollabPlatform Practice 1.1")

temp_bd: list[dict] = [
  {
    "id": 1,
    "name": "Алексей Иванов",
    "bio": "Full-stack разработчик, интересуюсь стартапами",
    "experience_years": 3,
    "preferences": {
      "id": 1,
      "title": "Веб-разработка",
      "description": "Ищу проекты на React и FastAPI",
    },
    "skills": [
      {"id": 1, "name": "Python", "description": "Backend", "category": "programming"},
      {"id": 2, "name": "React", "description": "Frontend", "category": "programming"},
    ],
  },
  {
    "id": 2,
    "name": "Мария Петрова",
    "bio": "UI/UX дизайнер",
    "experience_years": 2,
    "preferences": {
      "id": 2,
      "title": "Дизайн",
      "description": "Предпочитаю мобильные приложения",
    },
    "skills": [
      {"id": 3, "name": "Figma", "description": "Прототипирование", "category": "design"},
    ],
  },
]

skills_temp_bd: list[dict] = [
  {"id": 1, "name": "Python", "description": "Backend", "category": "programming"},
  {"id": 2, "name": "React", "description": "Frontend", "category": "programming"},
  {"id": 3, "name": "Figma", "description": "Прототипирование", "category": "design"},
]


@app.get("/")
def hello() -> str:
  return "Hello, CollabPlatform!"


@app.get("/profiles_list", response_model=List[Profile])
def profiles_list() -> list[dict]:
  return temp_bd


@app.get("/profile/{profile_id}", response_model=Profile)
def profile_get(profile_id: int) -> dict:
  for profile in temp_bd:
    if profile.get("id") == profile_id:
      return profile
  return {}


@app.post("/profile")
def profile_create(profile: ProfileCreate) -> TypedDict("Response", {"status": int, "data": Profile}):
  temp_bd.append(dict(profile))
  return {"status": 200, "data": profile}


@app.put("/profile{profile_id}")
def profile_update(profile_id: int, profile: ProfileCreate) -> list[dict]:
  for i, item in enumerate(temp_bd):
    if item.get("id") == profile_id:
      temp_bd[i] = dict(profile)
  return temp_bd


@app.delete("/profile/delete{profile_id}")
def profile_delete(profile_id: int) -> TypedDict("Response", {"status": int, "message": str}):
  for i, profile in enumerate(temp_bd):
    if profile.get("id") == profile_id:
      temp_bd.pop(i)
      break
  return {"status": 201, "message": "deleted"}


@app.get("/skills_list", response_model=List[Skill])
def skills_list() -> list[dict]:
  return skills_temp_bd


@app.get("/skill/{skill_id}", response_model=Skill)
def skill_get(skill_id: int) -> dict:
  for skill in skills_temp_bd:
    if skill.get("id") == skill_id:
      return skill
  return {}


@app.post("/skill")
def skill_create(skill: Skill) -> TypedDict("Response", {"status": int, "data": Skill}):
  skills_temp_bd.append(skill.model_dump())
  return {"status": 200, "data": skill}
