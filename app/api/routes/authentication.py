from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.db.erros import UserDoesNotExit
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
    UserWithTokenInResponse,
)
from app.resources import string
from app.services import jwt
from app.services.authentication import check_email_is_taken
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:

    # Raise error from wrong login input
    wrong_login_input_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST, detail=string.INCORRECT_LOGIN_INPUT
    )

    try:
        user = await user_repo.get_user_by_email(email=user_login.email)
    except UserDoesNotExit as existence_error:
        raise wrong_login_input_error from existence_error

    # Check user password
    if not user.check_password(user_login.password):
        raise wrong_login_input_error

    # Create Login token
    token = jwt.create_access_token_for_user(
        user, str(settings.SECRET_KEY.get_secret_value())
    )

    user_response = UserInResponse(
        user=UserWithTokenInResponse(
            **user.dict(),
            token=token,
        )
    )

    return user_response


@router.post(
    "/",
    response_model=UserInResponse,
    name="auth:register",
    status_code=HTTP_201_CREATED,
)
async def register(
    new_user: UserInCreate = Body(..., embed=True, alias="user"),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: AppSettings = Depends(get_app_settings),
) -> UserInResponse:

    # Check if passed email is already in use
    if await check_email_is_taken(user_repo, new_user.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=string.EMAIL_TAKEN,
        )

    user = await user_repo.register_new_user(new_user=new_user)

    # Generate JWT
    token = jwt.create_access_token_for_user(
        user, str(settings.SECRET_KEY.get_secret_value())
    )

    user_response = UserInResponse(
        user=UserWithTokenInResponse(
            **user.dict(),
            token=token,
        )
    )

    return user_response
