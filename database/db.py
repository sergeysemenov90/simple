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
        self.engine = None

    async def make_engine(self):
        db_config = self.config.db
        engine = create_async_engine(f'mysql+aiomysql://{db_config.user}:'
                                     f'{db_config.password}@'
                                     f'{db_config.host}:'
                                     f'{db_config.port}/'
                                     f'{db_config.database}')
        return engine

    async def base_metadata_save(self):
        engine = await self.make_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        return async_session

    async def create(self, model, obj):
        async_session = await self.base_metadata_save()
        print(f'Obj to create = {obj.dict()}')
        obj_to_create = model(**obj.dict())
        print('дойдем ли мы сюда')
        async with async_session() as session:
            async with session.begin():
                try:
                    session.add(obj_to_create)
                    await session.commit()
                    return obj_to_create
                except IntegrityError as e:
                    print('Все прошло НЕ ОК!')
                    print(f'Произошла ошибка :( {e}')

    async def get(self, model, id):
        async_session = await self.base_metadata_save()
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(model).where(model.user_id == id))
                user = result.scalars().first()
                return user

    async def get_all(self, model):
        async_session = await self.base_metadata_save()
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(model).options(subqueryload(model.author)))
                return result.all()


