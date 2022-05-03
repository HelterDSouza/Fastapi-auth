from app.models.domain.users import User
from pydantic import BaseModel, EmailStr


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    email: EmailStr
    password: str


class UserWithTokenInResponse(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithTokenInResponse


class UserInUpdate(BaseModel):
    email: EmailStr | None = None
