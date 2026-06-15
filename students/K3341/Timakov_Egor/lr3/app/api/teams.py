from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.models.project import Project
from app.models.team import (
  Team,
  TeamCreate,
  TeamMember,
  TeamMemberCreate,
  TeamMemberUpdate,
  TeamUpdate,
)
from app.models.user import User
from app.schemas.responses import TeamRead

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=List[TeamRead])
def list_teams(session: Annotated[Session, Depends(get_session)]) -> List[Team]:
  return session.exec(select(Team)).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, session: Annotated[Session, Depends(get_session)]) -> Team:
  team = session.get(Team, team_id)
  if team is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
  return team


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
  team_in: TeamCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Team:
  project = session.get(Project, team_in.project_id)
  if project is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

  team = Team.model_validate(team_in)
  session.add(team)
  session.commit()
  session.refresh(team)
  return team


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
  team_id: int,
  team_in: TeamUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Team:
  team = session.get(Team, team_id)
  if team is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

  update_data = team_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(team, key, value)

  session.add(team)
  session.commit()
  session.refresh(team)
  return team


@router.delete("/{team_id}", status_code=status.HTTP_200_OK)
def delete_team(
  team_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  team = session.get(Team, team_id)
  if team is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

  session.delete(team)
  session.commit()
  return {"ok": True}


@router.post("/members", response_model=TeamRead)
def add_team_member(
  member_in: TeamMemberCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Team:
  team = session.get(Team, member_in.team_id)
  if team is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

  user = session.get(User, member_in.user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

  existing = session.get(TeamMember, (member_in.team_id, member_in.user_id))
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Участник уже в команде")

  member = TeamMember.model_validate(member_in)
  session.add(member)
  session.commit()
  session.refresh(team)
  return team


@router.patch("/members/{team_id}/{user_id}", response_model=TeamRead)
def update_team_member(
  team_id: int,
  user_id: int,
  member_in: TeamMemberUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Team:
  member = session.get(TeamMember, (team_id, user_id))
  if member is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Участник не найден")

  update_data = member_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(member, key, value)

  session.add(member)
  session.commit()

  team = session.get(Team, team_id)
  return team


@router.delete("/members/{team_id}/{user_id}", status_code=status.HTTP_200_OK)
def remove_team_member(
  team_id: int,
  user_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  member = session.get(TeamMember, (team_id, user_id))
  if member is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Участник не найден")

  session.delete(member)
  session.commit()
  return {"ok": True}
