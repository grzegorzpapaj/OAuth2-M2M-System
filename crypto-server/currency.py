from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from .database import get_db
from .models import CurrencyRate, ClientApp
# Importujemy naszą kłódkę z auth.py
from .auth import get_current_client 

router = APIRouter(
    prefix="/currency",
    tags=["Currency Rates"]
)

# Prosty model Pydantic do wyświetlania danych (żeby nie zwracać surowego obiektu SQLAlchemy)
class CurrencyResponse(BaseModel):
    symbol: str
    rate: float

    class Config:
        orm_mode = True

@router.get("/", response_model=List[CurrencyResponse])
async def get_all_rates(
    db: AsyncSession = Depends(get_db), 
    current_client: ClientApp = Depends(get_current_client) # <--- TO JEST ZABEZPIECZENIE!
):
    # Logika biznesowa: pobierz wszystkie waluty
    result = await db.execute(select(CurrencyRate))
    rates = result.scalars().all()
    
    return rates

@router.get("/{symbol}", response_model=CurrencyResponse)
async def get_single_rate(
    symbol: str, 
    db: AsyncSession = Depends(get_db),
    current_client: ClientApp = Depends(get_current_client)
):
    result = await db.execute(select(CurrencyRate).where(CurrencyRate.symbol == symbol.upper()))
    rate = result.scalars().first()
    
    if not rate:
        # Możesz zwrócić 404, albo pusty obiekt
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Waluta nie znaleziona")
        
    return rate