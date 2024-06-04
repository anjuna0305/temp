# app/routers/auth.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth import create_access_token, authenticate_user, get_current_user, get_current_active_admin
from app.database import get_db
from app.exeptions_handlers import InternalServerError
from app.models import User
from .. import schemas, crud

router = APIRouter()


@router.post("/create-user", status_code=201)
async def create_user(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # return user_data
    try:
        print(user_data)
        user = await crud.create_user(db=db, user=user_data)
        return schemas.UserBase(
            username=user.username,
            email=user.email
        )
    except Exception as e:
        raise InternalServerError()


# @router.post("/login", status_code=200)
@router.post("/token")
async def login_for_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)) -> schemas.Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not isinstance(user, User):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [user.scopes], "email": user.email},
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/status/")
async def read_system_status(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/items")
async def read_own_items(
        current_user: User = Security(get_current_active_admin),
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# @router.post("/token", response_model=schemas.Token)
# async def login_for_access_token(db: Session = Depends(dependencies.get_db),
#                                  form_data: OAuth2PasswordRequestForm = Depends()):
#     print(form_data)
#     user = crud.authenticate_user(db, form_data.username, form_data.password)
#     print(user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = dependencies.create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
