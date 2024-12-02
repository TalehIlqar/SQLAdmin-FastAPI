from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://fastapi_user:strong_password@postgres-db-fastapi/fastapi_db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Declarative Base yaradılır
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
