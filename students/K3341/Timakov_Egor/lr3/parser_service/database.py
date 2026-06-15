"""Подключение к PostgreSQL."""

import os
from contextlib import contextmanager
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from parser_service.models import ParsedPage  # noqa: F401

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost/collab_platform_db")
engine = create_engine(DB_URL, echo=False)


def init_db() -> None:
  SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
  with Session(engine) as session:
    yield session
