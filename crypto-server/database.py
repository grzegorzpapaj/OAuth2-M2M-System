from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    "postgresql+asyncpg://crypto-server:postgres@localhost:5432/crypto-server-db"
)

engine = create_async_engine(
    DATABASE_URL, echo=True
)  # echo=True pokazuje zapytania SQL w konsoli

# Fabryka sesji - tego będziemy używać w endpointach
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Dependency Injection - funkcja dostarczająca sesję do endpointów
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
