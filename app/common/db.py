from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/music_db"

# движок
engine = create_async_engine(DATABASE_URL, echo=True)

# фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# базовый класс для моделей
Base = declarative_base()

# зависимость для FastAPI
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Function to create tables (for initial setup, not for production use)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)