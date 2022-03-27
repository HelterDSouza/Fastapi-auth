from typing import Any

from pydantic import PostgresDsn, SecretStr, validator

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    DEBUG: bool = False
    # Api INformations
    TITLE: str = "FastApi Authentication"
    VERSION: str = "0.0.0"

    # Api startup
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ALLOWED_HOSTS: list[str] = ["*"]

    # Api prefix for routes
    API_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: SecretStr

    class Config:
        case_sensitive = True
        validate_assignment: bool = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        config = {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
        }
        return config
