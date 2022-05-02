from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import (
    UserInCreate,
    UserInResponse,
    UserInUpdate,
    UserWithTokenInResponse,
)
from app.services.authentication import check_email_is_taken
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

router = APIRouter()


@router.post(
    "/",
    response_model=UserInResponse,
    name="users:register-new-user",
    status_code=HTTP_201_CREATED,
)
async def register_new_user(
    new_user: UserInCreate = Body(...),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInResponse:

    # Check if passed email is already in use
    if await check_email_is_taken(user_repo, new_user.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Email is already taken",
        )

    user = await user_repo.register_new_user(new_user=new_user)

    # Generate JWT
    token = "Generated Token"

    return UserInResponse(
        user=UserWithTokenInResponse(
            **user.dict(),
            token=token,
        )
    )


