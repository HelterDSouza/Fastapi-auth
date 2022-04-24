from asyncpg.connection import Connection


class BaseRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    @property
    def connection(self) -> Connection:
        return self._conn
