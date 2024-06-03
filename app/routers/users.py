# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud, dependencies

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user


@router.patch("/users/me/", response_model=schemas.User)
async def update_user_me(user_update: schemas.UserUpdate, db: Session = Depends(dependencies.get_db),
                         current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return crud.update_user(db, user_id=current_user.id, user_update=user_update)
