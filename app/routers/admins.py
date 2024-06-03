# app/routers/admins.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import

from .. import schemas, crud, dependencies

router = APIRouter()


@router.get("/admins/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db),
                     current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.patch("/admins/users/{user_id}/block", response_model=schemas.User)
async def block_user(user_id: int, db: AsyncSession = Depends(dependencies.get_db),
                     current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


@router.patch("/admins/users/{user_id}/unblock", response_model=schemas.User)
async def unblock_user(user_id: int, db: Session = Depends(dependencies.get_db),
                       current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

# Other endpoints for granting/removing access, viewing activities, etc.
