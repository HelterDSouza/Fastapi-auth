from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.models.schemas.users import UserInCreate, UserInResponse
from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

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

    user = await user_repo.register_new_user(new_user=new_user)
    return UserInResponse(user=user)
