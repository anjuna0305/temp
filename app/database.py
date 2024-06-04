from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://ltrl:ltrl%40ucsc@localhost/ltrl"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
