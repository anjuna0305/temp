from passlib.context import CryptContext
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies import verify_password, get_password_hash
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# authenticate a user
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = get_user_by_username_or_email(db, username)
    if not isinstance(user, schemas.User):
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# get all users--------------tested
async def get_all_users(db: AsyncSession, skip: int, limit: int = 100):
    results = await db.execute(select(models.User).offset(skip).limit(limit))
    return results.scalars().all()


# get a user by user id------------------tested and copy in test_router
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(user_id == models.User.id))
    return result.scalars().first()


# get a user by username--------------------tested and copy inn test_router
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).filter(or_(username == models.User.username))
    )
    return result.scalars().first()


async def get_user_by_username_or_email(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).filter(
            or_(username == models.User.username, username == models.User.email)
        )
    )
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(models.User).filter(or_(email == models.User.email))
    )
    return result.scalars().first()


# create a new user
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            scopes=user.scopes,
        )
        # print(db_user)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        return e


# update an user
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


# get all api service data--------------tested
async def get_api_services(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(select(models.APIService).offset(skip).limit(limit))
    return result.scalars().all()


async def get_api_service_by_id(db: AsyncSession, api_id: int):
    result = await db.execute(
        select(models.APIService).filter(api_id == models.APIService.id)
    )
    return result.scalars().first()


async def get_api_service_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(models.APIService).filter(name == models.APIService.name)
    )
    return result.scalars().first()


# create an new api service
async def create_api_service(db: AsyncSession, api_service: schemas.APIServiceCreate):
    db_api_service = models.APIService(
        name=api_service.name, description=api_service.description
    )
    db.add(db_api_service)
    await db.commit()
    await db.refresh(db_api_service)
    return db_api_service


# get api services user allowed to use
async def get_user_api_services_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.UserAPIService).filter(user_id == models.UserAPIService.user_id)
    )
    return result.scalars().all()


async def get_user_api_services_by_api_id(db: AsyncSession, api_id: int):
    result = await db.execute(
        select(models.User, models.UserAPIService)
        .join(models.UserAPIService)
        .join(models.APIService)
        .where(models.APIService.id == api_id)
        .limit(5)
    )
    user_api_services = result.all()

    response = []
    for user, user_api_service in user_api_services:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "created_at": user.created_at,
            "disabled": user.disabled,
            "scopes": user.scopes,
            "user_api_service": {
                "status": user_api_service.status,
                "request_per_action": user_api_service.request_per_action,
                "created_at": user_api_service.created_at,
                "exp_date": user_api_service.exp_date,
            },
        }
        response.append(user_data)

    return response


# get api services user allowed to use
async def get_user_api_services_by_userid_and_status(
    db: AsyncSession, user_id: int, status: str
):
    result = await db.execute(
        select(models.UserAPIService)
        .filter(user_id == models.UserAPIService.user_id)
        .filter(status == models.UserAPIService.status)
    )
    return result.scalars().all()


async def get_user_api_services_by_userid_and_serviceid(
    db: AsyncSession, user_id: int, api_service_id: int
):
    result = await db.execute(
        select(models.UserAPIService).where(
            and_(
                user_id == models.UserAPIService.user_id,
                api_service_id == models.UserAPIService.api_service_id,
            )
        )
    )
    return result.scalars().first()


# get api services user allowed to use
async def get_user_api_services_by_status(db: AsyncSession, status: str):
    result = await db.execute(
        select(models.UserAPIService).filter(status == models.UserAPIService.status)
    )
    return result.scalars().all()


# assign a api service for a user
async def create_user_api_service(
    db: AsyncSession, user_api_service: schemas.UserAPIServiceCreate
):
    db_user_api_service = models.UserAPIService(
        user_id=user_api_service.user_id,
        api_service_id=user_api_service.api_service_id,
        status=user_api_service.status,
    )
    db.add(db_user_api_service)
    await db.commit()
    await db.refresh(db_user_api_service)
    return db_user_api_service


# create a log
async def create_activity_log(
    db: AsyncSession, activity_log: schemas.ActivityLogCreate
):
    db_activity_log = models.ActivityLog(
        user_id=activity_log.user_id,
        api_service_id=activity_log.api_service_id,
        action=activity_log.action,
        detail=activity_log.detail,
    )
    db.add(db_activity_log)
    await db.commit()
    await db.refresh(db_activity_log)
    return db_activity_log


# get activity of a user
async def get_activity_of_user(
    db: AsyncSession, user_id: int, skip: int, limit: int = 50
):
    results = await db.execute(
        select(models.ActivityLog)
        .filter(user_id == models.ActivityLog.user_id)
        .offset(skip)
        .limit(limit)
    )


# get activity of a api
async def get_activity_of_user(db: AsyncSession, id: int, skip: int, limit: int = 50):
    results = await db.execute(
        select(models.ActivityLog)
        .filter(id == models.ActivityLog.api_service_id)
        .offset(skip)
        .limit(limit)
    )


# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     user = await get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
