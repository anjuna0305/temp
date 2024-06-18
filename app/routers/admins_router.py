# app/routers/admins.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
import uuid

from app.database import get_db
from app.models import User as UserModel
from app.schemas import UserAPIRequest
from app.exeptions_handlers import NotFoundError, ConflictError
from .. import crud

router = APIRouter()


@router.get("/users")
async def read_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    users = await crud.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}")
async def read_users(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    return user


@router.get("/requests")
async def get_requests(
    skip: int = 0,
    limit: int = 10,
    status: str = None,
    db: AsyncSession = Depends(get_db),
):
    requests = await crud.get_user_api_services_by_status(db, skip, limit, status)
    return requests


@router.put("/request/approve")
async def approve_request(
    request_data: UserAPIRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        requests = await crud.approve_request(
            db, request_data.user_id, request_data.api_service_id
        )
        return requests
    except Exception as e:
        raise e


@router.put("/request/reject")
async def reject_request(
    request_data: UserAPIRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        requests = await crud.reject_request(
            db, request_data.user_id, request_data.api_service_id
        )
        return requests
    except Exception as e:
        raise e


@router.get("/users/{user_id}/api")
async def get_user_owned_apis(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    api_services = await crud.get_user_api_services_by_user_id(db, user_id)
    return api_services


@router.patch("/users/{user_id}/block")
async def block_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.disabled = True
    await db.commit()
    await db.refresh(user)
    return user


@router.patch("/users/{user_id}/unblock")
async def unblock_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.disabled = False
    await db.commit()
    await db.refresh(user)
    return user


# block service.
@router.patch("/users/{user_id}/api/{api_id}/block")
async def block_api_service(
    user_id: int, api_id: int, db: AsyncSession = Depends(get_db)
):
    api = await crud.get_user_api_services_by_userid_and_serviceid(db, user_id, api_id)
    if not api:
        raise NotFoundError()
    api.access = False
    await db.commit()
    await db.refresh(api)
    return api


# unblock service.
@router.patch("/users/{user_id}/api/{api_id}/unblock")
async def unblock_api_service(
    user_id: int, api_id: int, db: AsyncSession = Depends(get_db)
):
    api = await crud.get_user_api_services_by_userid_and_serviceid(db, user_id, api_id)
    if not api:
        raise NotFoundError()
    api.access = True
    await db.commit()
    await db.refresh(api)
    return api


@router.post("/services/new")
async def upload_service(
    name: str = Form(...),
    port: int = Form(...),
    description: str = Form(...),
    documentation: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    file_location = f"files/{uuid.uuid4()}.md"
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(documentation.file, file_object)

    service_name = await crud.get_api_service_by_name(db, name)
    if service_name:
        raise ConflictError("Service name already exist")

    service_port = await crud.get_api_service_by_port(db, port)
    if service_port:
        raise ConflictError("Port already in use.")

    new_service = await crud.create_api_service(db, name, description, port, file_location)
    return new_service
