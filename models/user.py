from datetime import datetime
from pydantic import BaseModel


class UserIn(BaseModel):
    site_owner: bool = False
    username: str
    password: str
    password_again: str
    first_name: int = None
    last_name: str = None

    class Config:
        orm_mode = True

    def __str__(self):
        return f'{self.__class__.__name__}: {self.username}'


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int = None
    site_owner: bool = False
    username: str
    first_name: int = None
    last_name: str = None
    registered: datetime = None

    class Config:
        orm_mode = True
