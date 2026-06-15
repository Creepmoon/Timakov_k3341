import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
  DB_URL: str = os.getenv("DB_URL", "postgresql://postgres:123@localhost/collab_platform_db")
  SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
  PARSER_URL: str = os.getenv("PARSER_URL", "http://localhost:8001")
  CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
  CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")


settings = Settings()
