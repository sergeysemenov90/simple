import logging

from fastapi import FastAPI, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from routers import users
from database.note_repository import NoteRepository
from database.user_repository import UserRepository
from models.note import Note
from middlewares import session_middleware

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=session_middleware)
app.include_router(users.router)

note_repo = NoteRepository()
user_repo = UserRepository()


@app.get('/')
async def main():
    result = await note_repo.get_all()
    notes = [Note.from_orm(note) for note in result]
    if notes:
        return notes
    return {'message': 'There are still no notes here'}


@app.post('/notes/', response_model=Note, status_code=status.HTTP_201_CREATED)
async def node_create(note: Note):
    note = await note_repo.create(note)
    note = Note.from_orm(note)
    return note


@app.get('/note/{note_id}', response_model=Note)
async def node_get(note_id):
    note = await note_repo.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note = Note.from_orm(note)
    return note


@app.post('/notes/{note_id}/edit', response_model=Note)
async def note_edit(note_id, note: Note):
    await note_repo.edit(note_id, note)
    note = await note_repo.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")