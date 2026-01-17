from fastapi import FastAPI

from .database import Base, engine
from .models import ClientApp  # Import potrzebny, żeby Base o nich wiedział
from .models import CurrencyRate

app = FastAPI()


# To zdarzenie wykona się PRZED startem serwera
@app.on_event("startup")
async def startup():
    # Tworzy tabele w bazie (CREATE TABLE IF NOT EXISTS...)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database and tables created")


@app.get("/")
async def root():
    return {"message": "Crypto Server API works with postgres"}
