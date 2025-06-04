from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    API_V1_STR: str = os.getenv("API_V1_STR")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEBUG: bool = os.getenv("DEBUG")
    AGENT_ENDPOINT: str = os.getenv("AGENT_ENDPOINT")
    AGENT_ACCESS_KEY: str = os.getenv("AGENT_ACCESS_KEY")

    class Config:
        env_file = ".env"


settings = Settings()
