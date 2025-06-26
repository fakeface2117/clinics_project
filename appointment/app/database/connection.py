from functools import wraps

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.core.custom_logger import logger
from app.database.base import Base

engine = create_async_engine(settings.DB_CONNECTION_STRING)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def db_connection(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as ex:
                logger.exception(f"Exception occurred: {ex}")
                await session.rollback()
                raise
            finally:
                await session.close()

    return wrapper
