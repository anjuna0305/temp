# app/routers/auth.py
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exeptions_handlers import InternalServerError
from .. import schemas, crud, dependencies

router = APIRouter()


@router.post("/create-user")
async def create_user(user_data: schemas.UserCreate):
    # return user_data
    try:
        print("start try")
        db = dependencies.get_db
        print("got a database")
        user = await crud.create_user(db, user=user_data)
        return user, 201
    except Exception as e:
        raise InternalServerError()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> schemas.Token:
    user = await dependencies.authenticate_user(db=Depends(dependencies.get_db), username=form_data.username,
                                                password=form_data.password)
    if not isinstance(user, schemas.User):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

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
