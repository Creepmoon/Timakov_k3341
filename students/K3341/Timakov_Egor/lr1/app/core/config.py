import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
  DB_URL: str = os.getenv("DB_URL", "postgresql://postgres:123@localhost/collab_platform_db")
  SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
