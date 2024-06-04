from dotenv import load_dotenv
from fastapi import FastAPI
from app.database import async_engine
from app.models import Base

# fake change
# from app.routers import auth, users, admins, api_services
# from app.routers import admins
from app.routers.auth import router as auth_router

app = FastAPI()


# Create the database tables on startup
@app.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(users.router, prefix="/users", tags=["users"])
# app.include_router(admins.router, prefix="/admins", tags=["admins"])
# app.include_router(api_services.router, prefix="/api-services", tags=["api_services"])
