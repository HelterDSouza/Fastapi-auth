from asyncio.log import logger

import asyncpg
from app.core.settings.app import AppSettings
from fastapi import FastAPI


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:

    logger.info("Connecting to PostgreSQL")
    app.state.pool = await asyncpg.create_pool(
        str(settings.SQLALCHEMY_DATABASE_URI),
        min_size=settings.MIN_CONNECTION_COUNT,
        max_size=settings.MAX_CONNECTION_COUNT,
    )
    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
