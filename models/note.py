from datetime import datetime

from pydantic import BaseModel

from models.user import User


class Note(BaseModel):
    id: int = None
    author_id: int
    title: str
    text: str
    created_at: datetime = None
    is_published: bool
    views: int = 0
    author: User

    class Config:
        orm_mode = True
