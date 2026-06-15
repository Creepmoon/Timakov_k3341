from fastapi import APIRouter

from app.api import auth, profiles, projects, skills, tasks, teams, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(profiles.router)
api_router.include_router(skills.router)
api_router.include_router(projects.router)
api_router.include_router(teams.router)
api_router.include_router(tasks.router)
