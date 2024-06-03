# app/main.py
from fastapi import FastAPI

from app.dependencies import async_engine
from app.models import Base
# from app.routers import auth, users, admins, api_services
from app.routers import auth

app = FastAPI()


# Create the database tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=async_engine)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(admins.router, prefix="/admins", tags=["admins"])
# app.include_router(api_services.router, prefix="/api-services", tags=["api_services"])
