from sqlalchemy import select

from database.db import Database


class AbstractRepository:
    """abstract repository for extension"""
    def __init__(self):
        self.db = Database()
        self.model = None

    async def create(self, obj_to_save):
        obj = await self.db.create(self.model, obj_to_save)
        return obj

    async def get(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        obj = await self.db.get(stmt)
        return obj
