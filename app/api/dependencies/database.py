from typing import AsyncGenerator, Callable

from app.db.repositories.base import BaseRepository
from asyncpg.connection import Connection
from asyncpg.pool import Pool
from fastapi import Depends
from starlette.requests import Request


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


async def _get_connection_from_pool(
    pool: Pool = Depends(_get_db_pool),
) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[Connection], BaseRepository]:
    def get_repo(
        conn: Connection = Depends(_get_connection_from_pool),
    ) -> BaseRepository:
        return repo_type(conn)

    return get_repo
