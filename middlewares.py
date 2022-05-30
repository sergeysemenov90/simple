from fastapi import Request
from starlette.responses import Response
import aioredis

from database.user_repository import UserRepository


async def session_middleware(request: Request, call_next):
    aio = await aioredis.from_url('redis://localhost')
    sess_id = request.cookies.get('sess_id')
    user_id = await aio.get(sess_id)
    print(int(user_id))
    response: Response = await call_next(request)
    print('Middleware working!')
    return response
