import json
import logging

from fastapi import FastAPI
from pydantic.typing import List

from database.note_repository import NoteRepository
from database.user_repository import UserRepository
from models.note import Note
from models.user import User

logger = logging.getLogger(__name__)
app = FastAPI()

note_repo = NoteRepository()
user_repo = UserRepository()


@app.get('/')
async def main():
    result = await note_repo.get_all()
    print(result[0])
    note = Note.from_orm(result[0])

    # notes = [Note(**(dict(note))) for note in result]
    # if notes:
    #     return notes
    # return {'message': 'Постов пока нет'}


@app.post('/users/', response_model=User)
async def user_create(user: User):
    user = await user_repo.create(user)
    user = User.from_orm(user)
    return user


@app.post('/notes/', response_model=Note)
async def node_create(note: Note):
    note = await note_repo.create(note)
    note = Note.from_orm(note)
    return note

