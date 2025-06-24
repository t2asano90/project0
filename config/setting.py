from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    ENV: str = "development"
    LOG_LEVEL: str = "DEBUG"
    DB_PATH: str = "search_history.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()