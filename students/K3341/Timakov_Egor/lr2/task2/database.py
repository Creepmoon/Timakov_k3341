"""Подключение к PostgreSQL (та же БД, что в ЛР1)."""

import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from models import ParsedPage  # noqa: F401 — регистрация модели

load_dotenv()

# Та же PostgreSQL, что в ЛР1; для локального запуска без сервера — sqlite:///parsed_pages.db
DB_URL = os.getenv("DB_URL", "sqlite:///parsed_pages.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
  SQLModel.metadata.create_all(engine)


def get_session() -> Session:
  return Session(engine)
