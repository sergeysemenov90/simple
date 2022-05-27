from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int = None
    site_owner: bool
    username: str
    first_name: int = None
    last_name: str = None
    registered: datetime = None

    class Config:
        orm_mode = True

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id}, {self.username}'
