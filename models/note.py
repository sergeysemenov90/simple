from datetime import datetime

from pydantic import BaseModel

from models.user import UserIn


class Note(BaseModel):
    id: int = None
    author_id: int
    title: str
    text: str
    created_at: datetime = None
    is_published: bool
    views: int = 0
    author: UserIn = None

    class Config:
        orm_mode = True
