from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInCreate
from asyncpg.connection import Connection


class UsersRepository(BaseRepository):
    def __init__(self, conn: Connection):

        super().__init__(conn)

    async def register_new_user(self, *, new_user: UserInCreate) -> UserInDB:
        user = UserInDB(email=new_user.email)
        user.change_password(new_user.password)

        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection,
                **user.dict(),
            )

        return user.copy(update=dict(user_row))
