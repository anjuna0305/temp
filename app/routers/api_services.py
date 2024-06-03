# app/routers/api_services.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud, dependencies

router = APIRouter()


@router.get("/api-services/", response_model=List[schemas.APIService])
async def read_api_services(skip: int = 0, limit: int = 10, db: Session = Depends(dependencies.get_db)):
    api_services = crud.get_api_services(db, skip=skip, limit=limit)
    return api_services


@router.post("/api-services/", response_model=schemas.APIService)
async def create_api_service(api_service: schemas.APIServiceCreate, db: Session = Depends(dependencies.get_db),
                             current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
    return crud.create_api_service(db=db, api_service=api_service)

# Other endpoints for viewing, adding, removing, and takedown API services.
