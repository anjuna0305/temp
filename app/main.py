from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import async_engine
from app.models import Base

# fake change
# from app.routers import auth, users, admins, api_services
# from app.routers import admins
from app.routers.auth_router import router as auth_router
from app.routers.test_router import router as test_router
from app.routers.api_services_router import router as api_router
from app.routers.users_router import router as user_router
from app.routers.admins_router import router as admin_router
from app.routers.outlet_router import router as outlet_router

app = FastAPI()


origins = ["http://localhost:5173", "http://localhost:*", "http://vh2.local"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the database tables on startup
# @app.on_event("startup")
# async def init_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(test_router, prefix="/test", tags=["test"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(admin_router, prefix="/admin", tags=["admins"])
app.include_router(api_router, prefix="/api", tags=["api_services"])
app.include_router(outlet_router, prefix="/outlet", tags=["api_services"])
