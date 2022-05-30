import logging

from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, lazyload, subqueryload

from config import load_config
from database.models import Base


logger = logging.getLogger(__name__)


class Database:
    """Подключение и работа с базой данных"""
    def __init__(self):
        self.config = load_config('.env')
        self.session = None

    async def make_session(self):
        db_config = self.config.db
        engine = create_async_engine(f'mysql+aiomysql://{db_config.user}:'
                                     f'{db_config.password}@'
                                     f'{db_config.host}:'
                                     f'{db_config.port}/'
                                     f'{db_config.database}')
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        return async_session

    async def create(self, model, obj):
        session = await self.make_session()
        obj_to_create = model(**obj.dict())
        async with session() as session:
            async with session.begin():
                try:
                    session.add(obj_to_create)
                    await session.commit()
                    return obj_to_create
                except IntegrityError as e:
                    return e
                    logger.info(f'Произошла чудовищная ошибка :( {e}')

    async def get(self, stmt):
        session = await self.make_session()
        async with session() as session:
            async with session.begin():
                result = await session.execute(stmt)
                obj = result.scalars().first()
                return obj

    async def get_all(self, stmt):
        session = await self.make_session()
        async with session() as session:
            async with session.begin():
                result = await session.execute(stmt)
                return result.scalars()

    async def update(self, stmt):
        session = await self.make_session()
        async with session() as session:
            async with session.begin():
                await session.execute(stmt)


