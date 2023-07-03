from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

from app.config.router_configs import ROUTER_CONFIGS

load_dotenv()


class Settings(BaseSettings):
    API_VERSION: str = "0.1.0"
    API_TITLE: str = "Google Keep Clone"
    API_DESCRIPTION: str = "Backend API for Google Keep backend built with FastAPI and Docker"
    ALLOWED_HOSTS: list = ["*"]
    MONGO_HOST: str = "mongodb://localhost:27017/GoogleKeepClone"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()

__all__ = [
    "settings",
    "ROUTER_CONFIGS",
]
