from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from sqlalchemy.sql import text

from src.core.config import settings 

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

engine = create_async_engine(settings.DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

# TODO: Include Alembic for migrations
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    try:
        # Метод 1: Выполнение SQL команд по отдельности
        async with engine.begin() as conn:
            await conn.execute(text("DROP SCHEMA public CASCADE;"))
            await conn.execute(text("CREATE SCHEMA public;"))
    except Exception as e:
        print(f"Failed to drop schema: {str(e)}")
        # Метод 2: Попробуем использовать SQLAlchemy metadata напрямую
        try:
            async with engine.begin() as conn:
                # Это выполнит DROP TABLE для всех таблиц, определенных в метаданных
                # в обратном порядке зависимостей
                await conn.run_sync(Model.metadata.drop_all)
        except Exception as e2:
            print(f"Failed to drop tables: {str(e2)}")
