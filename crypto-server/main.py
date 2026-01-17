from fastapi import FastAPI, Depends, HTTPException

from .database import engine, Base, get_db
from .models import ClientApp  # Import potrzebny, żeby Base o nich wiedział
from .models import CurrencyRate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

app = FastAPI()

class ClientCreate(BaseModel):
    client_id: str
    client_secret: str
    app_name: str


# To zdarzenie wykona się PRZED startem serwera
@app.on_event("startup")
async def startup():
    # Tworzy tabele w bazie (CREATE TABLE IF NOT EXISTS...)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database and tables created")


@app.post("/register")
async def register_client(client_data: ClientCreate, db: AsyncSession = Depends(get_db)):

    # 1. Sprawdź, czy taki client_id już istnieje
    result = await db.execute(select(ClientApp).where(ClientApp.client_id == client_data.client_id))
    existing_client = result.scalars().first()
    
    if existing_client:
        raise HTTPException(status_code=400, detail="Taki Client ID już istnieje")

    # 2. Utwórz nowy obiekt (trzeba zrobic hashowanie)
    new_client = ClientApp(
        client_id=client_data.client_id,
        client_secret=client_data.client_secret, # Tutaj powinno być hashowanie
        app_name=client_data.app_name
    )

    # 3. Zapisz w bazie
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)

    return {"message": "Klient zarejestrowany", "id": new_client.id, "app_name": new_client.app_name}

@app.get("/")
async def root():
    return {"message": "Crypto Server API works with postgres"}
