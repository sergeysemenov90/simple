from fastapi import Request
from starlette.responses import Response


async def session_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.set_cookie('sess_id', '123456')
    print('Middleware working!')
    return response
