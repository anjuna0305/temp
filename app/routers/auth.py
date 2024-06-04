# app/routers/auth.py
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_access_token
from app.database import get_db
from app.dependencies import ACCESS_TOKEN_EXPIRE_MINUTES
from app.exeptions_handlers import InternalServerError
from .. import schemas, crud, auth

router = APIRouter()


@router.post("/create-user", status_code=201)
async def create_user(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # return user_data
    try:
        print("start try")
        user = await crud.create_user(db=db, user=user_data)
        user_base = schemas.UserBase().load(**user)
        # return schemas.UserBase(
        #     username=user.username,
        #     email=user.email
        # )
    except Exception as e:
        raise InternalServerError()


@router.post("/token")
async def login_for_access_token(form_data: schemas.User,
                                 db: AsyncSession = Depends(get_db)) -> schemas.Token:
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not isinstance(user, schemas.User):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
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
