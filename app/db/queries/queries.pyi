from asyncpg import Connection, Record
from pydantic import EmailStr


class UserQueriesMixin:
    async def create_new_user(
        self,
        conn: Connection,
        email: EmailStr,
        salt: str,
        hashed_password: str,
    ) -> Record: ...

    async def update_user(self,conn:Connection,email:EmailStr,new_email:EmailStr)
class Queries(UserQueriesMixin): ...

queries: Queries
