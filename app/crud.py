# app/crud.py
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(user_id == models.User.id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(username == models.User.username))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    try:
        hashed_password = await get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        return e


async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    db_user = await get_user(db, user_id)
    if db_user:
        if user_update.full_name:
            db_user.full_name = user_update.full_name
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def get_api_services(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.APIService).offset(skip).limit(limit))
    return result.scalars().all()


async def create_api_service(db: AsyncSession, api_service: schemas.APIServiceCreate):
    db_api_service = models.APIService(
        name=api_service.name,
        description=api_service.description
    )
    db.add(db_api_service)
    await db.commit()
    await db.refresh(db_api_service)
    return db_api_service


async def get_user_api_services(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.UserAPIService).filter(user_id == models.UserAPIService.user_id))
    return result.scalars().all()


async def create_user_api_service(db: AsyncSession, user_api_service: schemas.UserAPIServiceCreate):
    db_user_api_service = models.UserAPIService(
        user_id=user_api_service.user_id,
        api_service_id=user_api_service.api_service_id,
        status=user_api_service.status
    )
    db.add(db_user_api_service)
    await db.commit()
    await db.refresh(db_user_api_service)
    return db_user_api_service


async def create_activity_log(db: AsyncSession, activity_log: schemas.ActivityLogCreate):
    db_activity_log = models.ActivityLog(
        user_id=activity_log.user_id,
        api_service_id=activity_log.api_service_id,
        action=activity_log.action,
        detail=activity_log.detail
    )
    db.add(db_activity_log)
    await db.commit()
    await db.refresh(db_activity_log)
    return db_activity_log


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
