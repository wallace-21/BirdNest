from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "BirdNest API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./birdnest.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
