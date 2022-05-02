from functools import lru_cache

from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnvironmentType, BaseAppSettings
from app.core.settings.development import DevAppSettings

environments: dict[AppEnvironmentType, type[AppSettings]] = {
    AppEnvironmentType.dev: DevAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    """Get app environment setting"""
    base = BaseAppSettings()
    app_env = base.ENVIRONMENT
    config = environments[app_env]
    return config()
