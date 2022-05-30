from sqlalchemy import select

from database.abs_repository import AbstractRepository
from database.models import User
from services.authentication import get_password_hash


class UserRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.model = User

    async def create(self, user):
        user_exists = await self.get_by_username(user.username)
        if user_exists:
            return
        user.password = get_password_hash(user.password)
        delattr(user, 'password_again')
        user = await self.db.create(self.model, user)
        return user

    async def get_by_username(self, username):
        stmt = select(self.model).where(self.model.username == username)
        user = await self.db.get(stmt)
        return user

