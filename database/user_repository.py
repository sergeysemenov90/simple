from database.abs_repository import AbstractRepository

from database.db import Database
from database.models import User


class UserRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        self.model = User

