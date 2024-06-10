# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .. import schemas, crud, dependencies
from app.database import get_db
from app.auth import get_current_active_user
from app.exeptions_handlers import NotFoundError, ConflictError, InternalServerError

router = APIRouter()


@router.post("/access-request")
async def send_api_access_request(
    request_data: schemas.UserAPIServiceCreate,
    current_user: schemas.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    request_data.user_id = current_user.id

    try:
        api_request = await crud.get_user_api_services_by_userid_and_serviceid(
            db, request_data.user_id, request_data.api_service_id
        )
    except:
        raise InternalServerError

    if api_request:
        raise ConflictError(detail=f"Request already sent. Request status: {api_request.status}")

    try:
        req = await crud.create_user_api_service(db, request_data)
        return req
    except Exception:
        raise InternalServerError

    # return api_request


# @router.post("/users/", response_model=schemas.User)
# async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     return crud.create_user(db=db, user=user)


# @router.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
#     return current_user


# @router.patch("/users/me/", response_model=schemas.User)
# async def update_user_me(user_update: schemas.UserUpdate, db: Session = Depends(dependencies.get_db),
#                          current_user: schemas.User = Depends(dependencies.get_current_active_user)):
#     return crud.update_user(db, user_id=current_user.id, user_update=user_update)
