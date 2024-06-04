import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()
async_engine = create_async_engine(os.getenv("SQLALCHEMY_DATABASE_URL"), echo=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
