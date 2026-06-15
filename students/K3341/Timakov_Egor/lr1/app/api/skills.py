from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.models.profile import Skill, SkillCategory, SkillCreate, SkillUpdate
from app.models.user import User
from app.schemas.responses import SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=List[SkillRead])
def list_skills(
  session: Annotated[Session, Depends(get_session)],
  category: Optional[SkillCategory] = Query(default=None),
  name: Optional[str] = Query(default=None),
) -> List[Skill]:
  query = select(Skill)
  if category:
    query = query.where(Skill.category == category)
  if name:
    query = query.where(Skill.name.contains(name))
  return session.exec(query).all()


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: int, session: Annotated[Session, Depends(get_session)]) -> Skill:
  skill = session.get(Skill, skill_id)
  if skill is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Навык не найден")
  return skill


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
  skill_in: SkillCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Skill:
  existing = session.exec(select(Skill).where(Skill.name == skill_in.name)).first()
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Навык уже существует")

  skill = Skill.model_validate(skill_in)
  session.add(skill)
  session.commit()
  session.refresh(skill)
  return skill


@router.patch("/{skill_id}", response_model=SkillRead)
def update_skill(
  skill_id: int,
  skill_in: SkillUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Skill:
  skill = session.get(Skill, skill_id)
  if skill is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Навык не найден")

  update_data = skill_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(skill, key, value)

  session.add(skill)
  session.commit()
  session.refresh(skill)
  return skill


@router.delete("/{skill_id}", status_code=status.HTTP_200_OK)
def delete_skill(
  skill_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  skill = session.get(Skill, skill_id)
  if skill is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Навык не найден")

  session.delete(skill)
  session.commit()
  return {"ok": True}
