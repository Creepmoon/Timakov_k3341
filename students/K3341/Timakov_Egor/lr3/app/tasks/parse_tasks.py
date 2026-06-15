"""Фоновые задачи парсинга через Celery."""

import requests

from app.celery_app import celery_app
from app.core.config import settings


@celery_app.task(name="parse_url")
def parse_url_task(url: str) -> dict:
  """Отправляет URL в сервис парсера и возвращает результат."""
  response = requests.post(
    f"{settings.PARSER_URL}/parse",
    params={"url": url},
    timeout=60,
  )
  response.raise_for_status()
  return response.json()
