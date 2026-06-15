"""Эндпоинты для вызова парсера (синхронно и через Celery)."""

import requests
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException

from app.celery_app import celery_app
from app.core.config import settings
from app.tasks.parse_tasks import parse_url_task

router = APIRouter(prefix="/parser", tags=["parser"])


@router.post("/parse")
def parse_sync(url: str) -> dict:
  """Синхронный вызов сервиса парсера по HTTP."""
  try:
    response = requests.post(
      f"{settings.PARSER_URL}/parse",
      params={"url": url},
      timeout=60,
    )
    response.raise_for_status()
    return response.json()
  except requests.RequestException as error:
    raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/parse/async")
def parse_async(url: str) -> dict:
  """Ставит задачу парсинга в очередь Celery и возвращает идентификатор задачи."""
  task = parse_url_task.delay(url)
  return {
    "message": "Parsing started",
    "task_id": task.id,
    "url": url,
  }


@router.get("/parse/status/{task_id}")
def parse_status(task_id: str) -> dict:
  """Возвращает статус и результат фоновой задачи парсинга."""
  result = AsyncResult(task_id, app=celery_app)
  payload: dict = {
    "task_id": task_id,
    "status": result.status,
  }
  if result.ready():
    if result.successful():
      payload["result"] = result.result
    else:
      payload["error"] = str(result.result)
  return payload
