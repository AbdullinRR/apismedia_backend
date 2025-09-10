from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False,
)

async_session_maker = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
            finally:
                await session.close()

    return wrapper