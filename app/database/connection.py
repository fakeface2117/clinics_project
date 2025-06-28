from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.database.base import Base

engine = create_async_engine(settings.DB_CONNECTION_STRING)

async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
