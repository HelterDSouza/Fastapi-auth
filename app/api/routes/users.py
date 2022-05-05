from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import (
    UserInResponse,
    UserInUpdate,
    UserWithTokenInResponse,
)
from app.resources import string
from app.services import jwt
from app.services.authentication import check_email_is_taken
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

router = APIRouter()


@router.get("/me", response_model=UserInResponse, name="users:get-current-user")
async def retrive_current_user(
    user: User = Depends(get_current_user_authorizer()),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    token = jwt.create_access_token_for_user(
        user, str(settings.SECRET_KEY.get_secret_value())
    )

    response = UserInResponse(
        user=UserWithTokenInResponse(
            **user.dict(),
            token=token,
        )
    )

    return response


@router.put("", response_model=UserInResponse, name="users:update-current-user")
async def update_current_user(
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    current_user: User = Depends(get_current_user_authorizer()),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:
    # Check if has email and email is different from current email
    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(users_repo, user_update.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=string.EMAIL_TAKEN,
            )

    user = await users_repo.update_user(
        current_user=current_user,
        updated_user=user_update,
    )

    token = jwt.create_access_token_for_user(
        user, str(settings.SECRET_KEY.get_secret_value())
    )
    response = UserInResponse(
        user=UserWithTokenInResponse(**user.dict(), token=token),
    )
    return response
