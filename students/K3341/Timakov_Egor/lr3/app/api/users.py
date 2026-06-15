from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.security import get_password_hash, verify_password
from app.models.user import PasswordChange, User, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
def list_users(
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> List[User]:
  return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(
  user_id: int,
  session: Annotated[Session, Depends(get_session)],
  _: Annotated[User, Depends(get_current_active_user)],
) -> User:
  user = session.get(User, user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
  return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
  user_id: int,
  user_in: UserUpdate,
  session: Annotated[Session, Depends(get_session)],
  current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
  if current_user.id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав")

  user = session.get(User, user_id)
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

  update_data = user_in.model_dump(exclude_unset=True)
  for key, value in update_data.items():
    setattr(user, key, value)

  session.add(user)
  session.commit()
  session.refresh(user)
  return user


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
  password_in: PasswordChange,
  session: Annotated[Session, Depends(get_session)],
  current_user: Annotated[User, Depends(get_current_active_user)],
) -> dict[str, str]:
  if not verify_password(password_in.current_password, current_user.hashed_password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный текущий пароль")

  current_user.hashed_password = get_password_hash(password_in.new_password)
  session.add(current_user)
  session.commit()
  return {"message": "Пароль успешно изменён"}
