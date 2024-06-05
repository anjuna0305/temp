from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
import app.crud as crud
import app.schemas as schemas
from app.exeptions_handlers import (
    InvalidFormatError,
    InternalServerError,
    NotFoundError,
)

router = APIRouter()

# get user by user_id------------------------------------------------------------------------------------------------------
# @router.get("/test-get/{user_id}")
# async def test_get_router(user_id: int, db: AsyncSession = Depends(get_db)):
#     try:
#         user = await crud.get_user(db, user_id)
#         if user is None:
#              print("this will called")
#              raise NotFoundError
#         return user
#     except Exception as e:
#         raise e


# get user by user_name------------------------------------------------------------------------------------------------------
# @router.get("/test-get/{user_name}")
# async def test_get_router(user_name: str, db: AsyncSession = Depends(get_db)):
#     try:
#         user = await crud.get_user_by_username(db, user_name)
#         if user is None:
#             print("this will called")
#             raise NotFoundError
#         return user
#     except Exception as e:
#         raise e


# get all api service data------------------------------------------------------------------------------------------------------
# @router.get("/test-get")
# async def test_get_router(
#     skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
# ):
#     try:
#         services = await crud.get_api_services(db, skip=skip, limit=limit)
#         return services
#     except Exception as e:
#         raise e


# # get user api service------------------------------------------------------------------------------------------------------
# @router.get("/test-get/user/{user_id}")
# async def test_get_router(user_id: int, db: AsyncSession = Depends(get_db)):
#     try:
#         services = await crud.get_user_api_services(db, user_id)
#         return services
#     except Exception as e:
#         raise e


# #  get_user_api_services_by_api_id by api id------------------------------------------------------------------------------------------------------
@router.get("/test-get/api/{api_id}")
async def test_get_router(api_id: int, db: AsyncSession = Depends(get_db)):
    try:
        print("this called")
        services = await crud.get_user_api_services_by_api_id(db, api_id)
        return services
    except Exception as e:
        raise e


# @router.post("/test-post")
# async def test_router_post(
#     form_data: schemas.APIServiceCreate, db: AsyncSession = Depends(get_db)
# ):
#     try:
#         api_service = await crud.create_api_service(db, form_data)
#         return api_service
#     except Exception as e:
#         raise e


@router.post("/test-post")
async def test_router_post(
    form_data: schemas.UserAPIServiceCreate, db: AsyncSession = Depends(get_db)
):
    try:
        form_data.status = "pending"
        api_service = await crud.create_user_api_service(db, form_data)
        return api_service
    except Exception as e:
        raise e
