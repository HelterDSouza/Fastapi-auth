from app.db.erros import UserDoesNotExit
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import User, UserInDB
from asyncpg.connection import Connection
from pydantic import EmailStr


class UsersRepository(BaseRepository):
    def __init__(self, conn: Connection):

        super().__init__(conn)

    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_row = await queries.get_user_by_email(self.connection, email=email)

        if user_row:
            return UserInDB(**user_row)

        raise UserDoesNotExit(f"user with email {email} does not exist")

    async def register_new_user(self, *, new_user: UserInCreate) -> UserInDB:
        user = UserInDB(email=new_user.email)
        user.change_password(new_user.password)

        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection,
                **user.dict(),
            )

        return user.copy(update=dict(user_row))
