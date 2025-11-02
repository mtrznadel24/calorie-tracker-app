from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    REDIS_URL: str
    DEBUG_LOGS: bool = False
    PROJECT_NAME: str = "FastAPI App"

    class Config:
        env_file = ".env"

settings = Settings()