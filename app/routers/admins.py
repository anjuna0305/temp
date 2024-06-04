# app/routers/admins.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User as UserModel
from .. import crud

router = APIRouter()


@router.get("/users", response_model=List[UserModel])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}/api")
async def get_user_owned_apis(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    api_services = await crud.get_api_services(db, user_id)
    return api_services


@router.patch("/users/{user_id}/block", response_model=UserModel)
async def block_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/users/{user_id}/unblock", response_model=UserModel)
async def unblock_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    return user

# Other endpoints for granting/removing access, viewing activities, etc.
