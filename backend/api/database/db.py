"""Initialize DB config and async instance"""

import os
import contextlib
from typing import Any
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncConnection,
    create_async_engine,
)
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

from api.utils.custom_exceptions import MissingEnvVariableError

load_dotenv()
DB_URL = os.getenv("DB_URL", "")
DB_PASS = os.getenv("DB_PASS", "")
if DB_URL == "":
    raise MissingEnvVariableError(
        "Database URL environment variable not exist or invalid"
    )
DB_URL = DB_URL.replace("{{DB_PASS}}", DB_PASS)


class Base(DeclarativeBase):
    """Base class for DB models"""

    # setting for execute default func (created) under async scenarip
    __mapper_args__ = {"eager_defaults": True}


class DBSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engin = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engin)

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engin is None:
            raise Exception("Database session manager has not initialized")

        async with self._engin.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("Database session manager has not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        if self._engin is None:
            raise Exception("Database session manager has not initialized")

        await self._engin.dispose()
        self._engin = None
        self._sessionmaker = None


db_engin = create_async_engine(DB_URL, echo=True)
session_manager = DBSessionManager(DB_URL, {"echo": True})


async def get_db():
    """Get DB instance with generator"""
    async with session_manager.session() as session:
        yield session


async def create_all_tables():
    """Create all tables based on schema"""
    async with db_engin.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


def get_session():
    engin = create_async_engine(DB_URL)
    session_maker = async_sessionmaker(bind=engin)
    return session_maker()
