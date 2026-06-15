from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.models.project import Project, ProjectCreate, ProjectStatus, ProjectUpdate
from app.models.user import User
from app.schemas.responses import ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectRead])
def list_projects(
  session: Annotated[Session, Depends(get_session)],
  status_filter: Optional[ProjectStatus] = Query(default=None, alias="status"),
  creator_id: Optional[int] = Query(default=None),
  title: Optional[str] = Query(default=None),
) -> List[Project]:
  query = select(Project)
  if status_filter:
    query = query.where(Project.status == status_filter)
  if creator_id:
    query = query.where(Project.creator_id == creator_id)
  if title:
    query = query.where(Project.title.contains(title))
  return session.exec(query).all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Annotated[Session, Depends(get_session)]) -> Project:
  project = session.get(Project, project_id)
  if project is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")
  return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
  project_in: ProjectCreate,
  session: Annotated[Session, Depends(get_session)],
  current_user: Annotated[User, Depends(get_current_active_user)],
) -> Project:
  if project_in.creator_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

  project = Project.model_validate(project_in)
  session.add(project)
  session.commit()
  session.refresh(project)
  return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
  project_id: int,
  project_in: ProjectUpdate,
  session: Annotated[Session, Depends(get_session)],
  current_user: Annotated[User, Depends(get_current_active_user)],
) -> Project:
  project = session.get(Project, project_id)
  if project is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

  if project.creator_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

  update_data = project_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(project, key, value)

  session.add(project)
  session.commit()
  session.refresh(project)
  return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(
  project_id: int,
  session: Annotated[Session, Depends(get_session)],
  current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  project = session.get(Project, project_id)
  if project is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

  if project.creator_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

  session.delete(project)
  session.commit()
  return {"ok": True}
