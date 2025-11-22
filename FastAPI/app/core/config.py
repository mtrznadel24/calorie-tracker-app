from pydantic_settings import BaseSettings
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    DEBUG_LOGS: bool = False
    PROJECT_NAME: str = "FastAPI App"

    model_config = {"env_file": str(BASE_DIR / ".env"),
                    "env_file_encoding": "utf-8",
                    "extra": "ignore"}


settings = Settings()
