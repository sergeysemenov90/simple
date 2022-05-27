from database.abs_repository import AbstractRepository
from database.models import Note


class NoteRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.model = Note

    async def get_all(self):
        objs = await self.db.get_all(self.model)
        return objs
