"""HTTP-сервис парсера (FastAPI)."""

import requests
from fastapi import FastAPI, HTTPException

from parser_service.common import parse_and_save
from parser_service.database import init_db

app = FastAPI(
  title="Parser Service",
  description="Сервис парсинга веб-страниц (ЛР2)",
  version="1.0.0",
)


@app.on_event("startup")
def on_startup() -> None:
  init_db()


@app.get("/")
def health() -> dict:
  return {"status": "ok", "service": "parser"}


@app.post("/parse")
def parse(url: str) -> dict:
  """Загружает страницу по URL, парсит заголовок и сохраняет в БД."""
  try:
    title = parse_and_save(url)
    return {"message": "Parsing completed", "url": url, "title": title}
  except requests.RequestException as error:
    raise HTTPException(status_code=500, detail=str(error)) from error
  except Exception as error:
    raise HTTPException(status_code=500, detail=str(error)) from error
