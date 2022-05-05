from typing import Callable, Optional

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.erros import UserDoesNotExit
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.resources import string
from app.services import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

HEADER_KEY = "Authorization"


class ApiKeyHeader(APIKeyHeader):
    async def __call__(self, request: requests.Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=string.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:
    if required:
        _get_current_user

    return _get_current_user_optional


def _get_authorization_header_retriever(*, required: bool = True) -> Callable:
    if required:
        return _get_authorization_header
    return _get_authorization_header_optional


def _get_authorization_header_optional(
    authorization: str
    | None = Security(
        ApiKeyHeader(
            name=HEADER_KEY,
            auto_error=False,
        )
    ),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    if authorization:
        return _get_authorization_header(authorization, settings)
    return ""


def _get_authorization_header(
    api_key: str = Security(ApiKeyHeader(name=HEADER_KEY)),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=string.WRONG_TOKEN_PREFIX
        )
    if token_prefix != settings.JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=string.WRONG_TOKEN_PREFIX
        )

    return token


async def _get_current_user(
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_header_retriever),
    settings: AppSettings = Depends(get_app_settings),
) -> User:
    try:
        email = jwt.get_email_from_token(
            token, str(settings.SECRET_KEY.get_secret_value())
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=string.MALFORMED_PAYLOAD
        )

    try:
        return await user_repo.get_user_by_email(email=email)
    except UserDoesNotExit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=string.MALFORMED_PAYLOAD
        )


async def _get_current_user_optional(
    repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_authorization_header_retriever(required=False)),
    settings: AppSettings = Depends(get_app_settings),
) -> Optional[User]:
    if token:
        return await _get_current_user(repo, token, settings)

    return None
