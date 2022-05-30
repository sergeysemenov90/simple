from fastapi import APIRouter, status, HTTPException, Response

from database.user_repository import UserRepository
from models.user import UserIn, UserOut, UserLogin
from services.authentication import authenticate_user


router = APIRouter(prefix='/users')
user_repo = UserRepository()


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def user_create(user: UserIn):
    user = await user_repo.create(user)
    if user:
        user = UserOut.from_orm(user)
        return user
    raise HTTPException(status_code=400, detail='This username already taken')


@router.post('/login', response_model=UserOut)
async def user_login(response: Response, user_data: UserLogin):
    user = await user_repo.get_by_username(user_data.username)
    if user is None:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    key = await authenticate_user(user, user_data)
    response.set_cookie('sess_id', key)
    return user
