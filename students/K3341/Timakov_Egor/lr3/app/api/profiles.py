from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.models.profile import (
  Profile,
  ProfileCreate,
  ProfileSkillLink,
  ProfileSkillLinkCreate,
  ProfileSkillLinkUpdate,
  ProfileUpdate,
  Skill,
)
from app.models.user import User
from app.schemas.responses import ProfileRead

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=List[ProfileRead])
def list_profiles(
  session: Annotated[Session, Depends(get_session)],
  skill_id: Optional[int] = Query(default=None),
  min_experience: Optional[int] = Query(default=None, ge=0),
  interests: Optional[str] = Query(default=None),
) -> List[Profile]:
  query = select(Profile)
  if min_experience is not None:
    query = query.where(Profile.experience_years >= min_experience)
  if interests:
    query = query.where(Profile.interests.contains(interests))

  profiles = session.exec(query).all()

  if skill_id is not None:
    profiles = [
      profile
      for profile in profiles
      if any(link.skill_id == skill_id for link in profile.skills)
    ]

  return profiles


@router.get("/{profile_id}", response_model=ProfileRead)
def get_profile(profile_id: int, session: Annotated[Session, Depends(get_session)]) -> Profile:
  profile = session.get(Profile, profile_id)
  if profile is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден")
  return profile


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def create_profile(
  profile_in: ProfileCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Profile:
  existing = session.exec(select(Profile).where(Profile.user_id == profile_in.user_id)).first()
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Профиль уже существует")

  profile = Profile.model_validate(profile_in)
  session.add(profile)
  session.commit()
  session.refresh(profile)
  return profile


@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(
  profile_id: int,
  profile_in: ProfileUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Profile:
  profile = session.get(Profile, profile_id)
  if profile is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден")

  update_data = profile_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(profile, key, value)

  session.add(profile)
  session.commit()
  session.refresh(profile)
  return profile


@router.delete("/{profile_id}", status_code=status.HTTP_200_OK)
def delete_profile(
  profile_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  profile = session.get(Profile, profile_id)
  if profile is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден")

  session.delete(profile)
  session.commit()
  return {"ok": True}


@router.post("/skills", response_model=ProfileRead)
def add_skill_to_profile(
  link_in: ProfileSkillLinkCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Profile:
  profile = session.get(Profile, link_in.profile_id)
  if profile is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Профиль не найден")

  skill = session.get(Skill, link_in.skill_id)
  if skill is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Навык не найден")

  existing = session.get(ProfileSkillLink, (link_in.profile_id, link_in.skill_id))
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Навык уже добавлен")

  link = ProfileSkillLink.model_validate(link_in)
  session.add(link)
  session.commit()
  session.refresh(profile)
  return profile


@router.patch("/skills/{profile_id}/{skill_id}", response_model=ProfileRead)
def update_profile_skill(
  profile_id: int,
  skill_id: int,
  link_in: ProfileSkillLinkUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Profile:
  link = session.get(ProfileSkillLink, (profile_id, skill_id))
  if link is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Связь не найдена")

  update_data = link_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(link, key, value)

  session.add(link)
  session.commit()

  profile = session.get(Profile, profile_id)
  return profile


@router.delete("/skills/{profile_id}/{skill_id}", status_code=status.HTTP_200_OK)
def remove_skill_from_profile(
  profile_id: int,
  skill_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  link = session.get(ProfileSkillLink, (profile_id, skill_id))
  if link is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Связь не найдена")

  session.delete(link)
  session.commit()
  return {"ok": True}
