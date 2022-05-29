from sqlalchemy import select, update
from sqlalchemy.orm import subqueryload

from database.abs_repository import AbstractRepository
from database.models import Note


class NoteRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.model = Note

    async def get(self, id: int):
        incr_views_stmt = update(self.model).where(self.model.id == id).values(views=self.model.views + 1)
        await self.db.update(incr_views_stmt)
        stmt = select(self.model).where(self.model.id == id).options(subqueryload(self.model.author))
        obj = await self.db.get(stmt)
        return obj

    async def get_all(self):
        stmt = select(self.model).options(subqueryload(self.model.author))
        objs = await self.db.get_all(stmt)
        return objs

    async def edit(self, id: int, note):
        stmt = update(self.model).where(self.model.id == id).values(title=note.title,
                                                                    text=note.text)
        await self.db.update(stmt)