from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.models.project import Project, Task, TaskCreate, TaskStatus, TaskUpdate
from app.models.user import User
from app.schemas.responses import TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def list_tasks(
  session: Annotated[Session, Depends(get_session)],
  project_id: Optional[int] = Query(default=None),
  assignee_id: Optional[int] = Query(default=None),
  status_filter: Optional[TaskStatus] = Query(default=None, alias="status"),
) -> List[Task]:
  query = select(Task)
  if project_id:
    query = query.where(Task.project_id == project_id)
  if assignee_id:
    query = query.where(Task.assignee_id == assignee_id)
  if status_filter:
    query = query.where(Task.status == status_filter)
  return session.exec(query).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Annotated[Session, Depends(get_session)]) -> Task:
  task = session.get(Task, task_id)
  if task is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
  return task


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
  task_in: TaskCreate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Task:
  project = session.get(Project, task_in.project_id)
  if project is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден")

  task = Task.model_validate(task_in)
  session.add(task)
  session.commit()
  session.refresh(task)
  return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
  task_id: int,
  task_in: TaskUpdate,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> Task:
  task = session.get(Task, task_id)
  if task is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

  update_data = task_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(task, key, value)

  session.add(task)
  session.commit()
  session.refresh(task)
  return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
  task_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, bool]:
  task = session.get(Task, task_id)
  if task is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

  session.delete(task)
  session.commit()
  return {"ok": True}
