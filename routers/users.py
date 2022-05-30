from fastapi import APIRouter, status

from database.user_repository import UserRepository
from models.user import User

router = APIRouter()
user_repo = UserRepository()


@router.post('/users/', response_model=User, status_code=status.HTTP_201_CREATED)
async def user_create(user: User):
    user = await user_repo.create(user)
    user = User.from_orm(user)
    return user
