from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.vpn.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase):
    pass