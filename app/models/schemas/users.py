from app.models.domain.users import User
from pydantic import BaseModel, EmailStr


class UserInCreate(BaseModel):
    email: EmailStr
    password: str


class UserWithTokenInResponse(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithTokenInResponse
