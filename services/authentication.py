import datetime
import uuid
from passlib.context import CryptContext
from models.session import Session

import aioredis

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def generate_session_id(num_bytes=16):
    return uuid.uuid4()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(user, user_data):
    if not verify_password(user_data.password, user.password):
        return
    session = Session(key=generate_session_id(),
                      user=user,
                      expires=datetime.datetime.now() + datetime.timedelta(days=10))
    print(session)
    await save_to_redis(session)
    return session.key


async def save_to_redis(session):
    redis = await aioredis.from_url('redis://localhost')
    await redis.set(str(session.key), session.user.id)


