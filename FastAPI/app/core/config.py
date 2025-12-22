import os
import pathlib
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

env = os.getenv("ENVIRONMENT", "dev")

if env == "dev":
    env_file = BASE_DIR / ".env"
else:
    env_file = BASE_DIR / f".env.{env}"


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    SECRET_KEY: str = "default-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_URL: str = "redis://localhost:6379"
    DEBUG_LOGS: bool = False
    PROJECT_NAME: str = "FastAPI App"
    ALLOWED_ORIGINS: List[str] = ["*"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = {
        "env_file": str(env_file),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
