from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, SQLModel, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User, UserCreate, UserRead
from app.schemas.responses import Token


class LoginRequest(SQLModel):
  email: str
  password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, session: Annotated[Session, Depends(get_session)]) -> User:
  existing = session.exec(
    select(User).where((User.email == user_in.email) | (User.username == user_in.username))
  ).first()
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email или имя уже заняты")

  user = User(
    email=user_in.email,
    username=user_in.username,
    hashed_password=get_password_hash(user_in.password),
  )
  session.add(user)
  session.commit()
  session.refresh(user)
  return user


@router.post("/login", response_model=Token)
def login(
  credentials: LoginRequest,
  session: Annotated[Session, Depends(get_session)],
) -> Token:
  user = session.exec(select(User).where(User.email == credentials.email)).first()
  if user is None or not verify_password(credentials.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Неверный email или пароль",
    )

  if not user.is_active:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Аккаунт деактивирован")

  access_token = create_access_token(data={"sub": str(user.id)})
  return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
  return current_user
