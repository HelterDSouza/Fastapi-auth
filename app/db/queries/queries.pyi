from email.message import EmailMessage

from asyncpg import Connection, Record
from pydantic import EmailStr

class UserQueriesMixin:
    async def create_new_user(
        self,
        conn: Connection,
        email: EmailStr,
        salt: str,
        hashed_password: str,
        is_superuser: bool,
        is_active: bool,
    ) -> Record: ...
    async def update_user_by_email(
        self,
        conn: Connection,
        email: EmailStr,
        new_email: EmailStr,
    ) -> Record: ...
    async def get_user_by_email(
        self,
        conn: Connection,
        email: EmailStr,
    ) -> Record: ...

class Queries(UserQueriesMixin): ...

queries: Queries
