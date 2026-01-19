from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
import random

from .database import get_db
from .models import CurrencyRate, ClientApp
# Importujemy naszą kłódkę z auth.py
from .auth import get_current_client

router = APIRouter(
    prefix="/currency",
    tags=["Currency Rates"]
)

# Mapa nazw
CURRENCY_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "XRP": "Ripple",
    "ADA": "Cardano",
    "DOT": "Polkadot",
    "LINK": "Chainlink",
    "LTC": "Litecoin",
    "BCH": "Bitcoin Cash",
    "XLM": "Stellar",
    "UNI": "Uniswap",
    "DOGE": "Dogecoin",
    "AVAX": "Avalanche"
}

# Prosty model Pydantic do wyświetlania danych
class CurrencyResponse(BaseModel):
    symbol: str
    rate: float
    name: str = "Unknown"
    change_24h: float = 0.0
    updated_at: datetime

    class Config:
        orm_mode = True

def map_currency_to_response(currency: CurrencyRate) -> CurrencyResponse:
    return CurrencyResponse(
        symbol=currency.symbol,
        rate=currency.rate,
        name=CURRENCY_NAMES.get(currency.symbol, currency.symbol),
        change_24h=currency.change_24h if currency.change_24h is not None else 0.0,
        updated_at=currency.last_updated or datetime.utcnow()
    )

@router.get("/", response_model=List[CurrencyResponse])
async def get_all_rates(
    db: AsyncSession = Depends(get_db), 
    current_client: ClientApp = Depends(get_current_client)
):
    # Logika biznesowa: pobierz wszystkie waluty
    result = await db.execute(select(CurrencyRate))
    rates = result.scalars().all()
    
    return [map_currency_to_response(rate) for rate in rates]

@router.get("/{symbol}", response_model=CurrencyResponse)
async def get_single_rate(
    symbol: str, 
    db: AsyncSession = Depends(get_db),
    current_client: ClientApp = Depends(get_current_client)
):
    result = await db.execute(select(CurrencyRate).where(CurrencyRate.symbol == symbol.upper()))
    rate = result.scalars().first()
    
    if not rate:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Waluta nie znaleziona")
        
    return map_currency_to_response(rate)