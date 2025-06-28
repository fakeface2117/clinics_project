import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.database.base import Base


@pytest.fixture
async def in_memory_db():
    assert settings.MODE == "TEST"
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_engine


@pytest.fixture
async def session_factory(in_memory_db):
    yield async_sessionmaker(
        bind=in_memory_db, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False
    )


@pytest.fixture
async def session(session_factory):
    async with session_factory() as s:
        yield s
