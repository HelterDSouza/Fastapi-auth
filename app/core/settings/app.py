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

    # Postgresql
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: str | PostgresDsn

    MAX_CONNECTION_COUNT: int = 10
    MIN_CONNECTION_COUNT: int = 10

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str, values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

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
