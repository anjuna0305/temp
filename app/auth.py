import datetime
from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.dependencies import verify_password,SECRET_KEY, ALGORITHM
from app.schemas import User
from app.crud import get_user_by_username


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = get_user_by_username(db, username)
    if not isinstance(user, User):
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
