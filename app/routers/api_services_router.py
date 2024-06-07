# app/routers/api_services.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud, dependencies
from app.database import get_db

router = APIRouter()


@router.get("/api-services/", response_model=List[schemas.APIService])
async def read_api_services(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    api_services = await crud.get_api_services(db, skip=skip, limit=limit)
    return api_services


@router.get("/api-service/{service_id}")
async def read_api_services(service_id: int, db: Session = Depends(get_db)):
    api_services = await crud.get_api_service_by_id(db, service_id)
    return api_services


# @router.post("/api-services/", response_model=schemas.APIService)
# async def create_api_service(api_service: schemas.APIServiceCreate, db: Session = Depends(get_db),
#                              current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
#     return crud.create_api_service(db=db, api_service=api_service)

# Other endpoints for viewing, adding, removing, and takedown API services.
