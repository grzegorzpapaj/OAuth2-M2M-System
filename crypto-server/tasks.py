import asyncio
import random
from sqlalchemy.future import select
from .database import AsyncSessionLocal
from .models import CurrencyRate

async def currency_generator():
    async with AsyncSessionLocal() as db:
        # 1. SEEDOWANIE: Sprawdź czy mamy jakieś waluty, jak nie to dodaj startowe
        result = await db.execute(select(CurrencyRate))
        if not result.scalars().first():
            print("🌱 Inicjalizacja walut startowych...")
            db.add_all([
                CurrencyRate(symbol="BTC", rate=45000.0),
                CurrencyRate(symbol="ETH", rate=3200.0),
                CurrencyRate(symbol="SOL", rate=144.0),
            ])
            await db.commit()
        
        print("🚀 Start generatora kursów!")

        # 2. PĘTLA NIESKOŃCZONA (Symulacja rynku)
        while True:
            # Pobierz wszystkie waluty
            result = await db.execute(select(CurrencyRate))
            rates = result.scalars().all()

            # Zmień kurs każdej o losowy procent (np. +/- 0.5%)
            for currency in rates:
                change_percent = random.uniform(-0.005, 0.005) 
                currency.rate = currency.rate * (1 + change_percent)
            
            # Zapisz zmiany w bazie
            await db.commit()
            
            # Czekaj 3 sekundy
            await asyncio.sleep(3)