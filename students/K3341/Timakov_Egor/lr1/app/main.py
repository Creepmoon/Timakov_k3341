from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
  title="CollabPlatform API",
  description="Платформа для поиска партнёров и совместной работы над проектами",
  version="1.0.0",
)

app.include_router(api_router)


@app.get("/")
def hello() -> str:
  return "Hello, CollabPlatform!"
