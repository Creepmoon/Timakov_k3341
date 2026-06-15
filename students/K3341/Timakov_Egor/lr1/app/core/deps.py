from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import decode_access_token
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
  credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
  session: Annotated[Session, Depends(get_session)],
) -> User:
  if credentials is None or credentials.scheme.lower() != "bearer":
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Не предоставлен токен авторизации",
      headers={"WWW-Authenticate": "Bearer"},
    )

  payload = decode_access_token(credentials.credentials)
  if payload is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Недействительный или просроченный токен",
      headers={"WWW-Authenticate": "Bearer"},
    )

  user_id = payload.get("sub")
  if user_id is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Некорректный токен",
      headers={"WWW-Authenticate": "Bearer"},
    )

  user = session.get(User, int(user_id))
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Пользователь не найден",
      headers={"WWW-Authenticate": "Bearer"},
    )

  if not user.is_active:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Аккаунт деактивирован")

  return user


def get_current_active_user(
  current_user: Annotated[User, Depends(get_current_user)],
) -> User:
  return current_user
