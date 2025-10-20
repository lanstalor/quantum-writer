import asyncio
import importlib
import pathlib
import sys

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core import settings
from app.db import database

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_auth.db"


@pytest.fixture(scope="session", autouse=True)
def override_database():
    repo_root = pathlib.Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    importlib.import_module("aiosqlite")

    settings.DATABASE_URL = TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    database.engine = engine
    database.AsyncSessionLocal = session_factory

    async def prepare_schema():
        async with engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.drop_all)
            await conn.run_sync(database.Base.metadata.create_all)

    asyncio.run(prepare_schema())

    yield

    asyncio.run(engine.dispose())
