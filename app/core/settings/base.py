from enum import Enum

from pydantic import BaseSettings


class AppEnvironmentType(str, Enum):
    prod = "prod"
    dev = "dev"


class BaseAppSettings(BaseSettings):
    ENVIRONMENT: AppEnvironmentType = AppEnvironmentType.prod

    class Config:
        env_file: str = ".env"
